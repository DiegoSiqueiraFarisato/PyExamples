"""Runs the same broker behaviour tests against the memory and Redis backends.
Redis is simulated with fakeredis, so no Redis server is needed to run the tests."""
import asyncio

import fakeredis
import pytest

from app.broker.memory import MemoryBroker
from app.broker.redis_broker import RedisBroker


class _NonBlockingFake(fakeredis.FakeAsyncRedis):
    """fakeredis holds a lock during blocking reads; a real Redis does not."""

    async def xreadgroup(self, *args, block=None, **kwargs):
        result = await super().xreadgroup(*args, **kwargs)
        if not result:
            await asyncio.sleep(0.02)
        return result


def make_memory():
    return MemoryBroker(retry_delay=0.01)


def make_redis():
    return RedisBroker(client=_NonBlockingFake(decode_responses=True), retry_delay=0.01)


@pytest.fixture(params=[make_memory, make_redis], ids=["memory", "redis"])
async def broker(request):
    b = request.param()
    yield b
    await b.stop()


async def test_delivers_only_matching_topics(broker):
    got = []

    async def handler(msg):
        got.append(msg.topic)

    broker.subscribe("order.*", handler, name="t")
    await broker.start()
    await asyncio.sleep(0.2)
    await broker.publish("order.created", {"id": 1})
    await broker.publish("user.created", {"id": 2})
    await asyncio.sleep(0.5)
    assert got == ["order.created"]


async def test_failing_handler_is_retried_then_dead_lettered(broker):
    calls = []

    async def bad(msg):
        calls.append(msg.attempts)
        raise ValueError("boom")

    broker.subscribe("x", bad, name="bad")
    await broker.start()
    await asyncio.sleep(0.2)
    await broker.publish("x", {"n": 1})
    await asyncio.sleep(0.5)
    assert calls == [1, 2, 3]
    dead = await broker.dead_letters()
    assert len(dead) == 1 and dead[0]["subscription"] == "bad"


async def test_duplicate_subscription_name_is_rejected(broker):
    async def h(msg): ...

    broker.subscribe("x", h, name="same")
    with pytest.raises(ValueError):
        broker.subscribe("y", h, name="same")
