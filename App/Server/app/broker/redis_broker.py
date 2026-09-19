"""Redis-backed broker built on Redis Streams.

- Every message is appended to one stream ("<prefix>:events").
- Each subscription is a *consumer group* on that stream, so every subscriber sees every
  matching message, and several server processes sharing a subscription name split the work.
- A message is acknowledged only after its handler succeeds (or it is dead-lettered), so
  messages survive a server restart, and messages left unacknowledged by a crashed process
  are claimed by another one after `claim_idle_ms`.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import socket
from fnmatch import fnmatch
from typing import Any

import redis.asyncio as aioredis
from redis.exceptions import ResponseError

from .base import BaseBroker, Message, Subscription

log = logging.getLogger("broker")


class RedisBroker(BaseBroker):
    def __init__(
        self,
        *,
        host: str = "127.0.0.1",
        port: int = 6379,
        db: int = 0,
        password: str | None = None,
        ssl: bool = False,
        prefix: str = "appserver",
        max_retries: int = 3,
        retry_delay: float = 0.5,
        stream_maxlen: int = 10000,
        claim_idle_ms: int = 30000,
        client: Any = None,  # inject a ready client (used by tests)
    ):
        super().__init__(max_retries, retry_delay)
        self._target = f"{host}:{port}/{db}"
        self._r = client or aioredis.Redis(
            host=host, port=port, db=db, password=password or None, ssl=ssl,
            decode_responses=True, socket_connect_timeout=5,
        )
        self.stream = f"{prefix}:events"
        self.dead_key = f"{prefix}:dead"
        self.stream_maxlen = stream_maxlen
        self.claim_idle_ms = claim_idle_ms
        self.consumer = f"{socket.gethostname()}-{os.getpid()}"

    def _spawn(self, sub: Subscription) -> None:
        sub.task = asyncio.create_task(self._worker(sub))

    async def start(self) -> None:
        try:
            await self._r.ping()
        except Exception as exc:
            raise RuntimeError(
                f"Cannot reach Redis at {self._target} ({exc}). "
                "Check REDIS_HOST / REDIS_PORT / REDIS_PASSWORD in config.env, "
                "that Redis is running, and that the firewall allows the port."
            ) from exc
        self._running = True
        for sub in self._subs:
            if sub.task is None:
                self._spawn(sub)
        log.info("redis broker connected to %s with %d subscription(s)", self._target, len(self._subs))

    async def stop(self) -> None:
        self._running = False
        tasks = [s.task for s in self._subs if s.task]
        if tasks:
            _, pending = await asyncio.wait(tasks, timeout=5)  # let in-flight handlers finish
            for t in pending:
                t.cancel()
        await self._r.aclose()
        log.info("redis broker stopped")

    async def publish(self, topic: str, payload: Any) -> Message:
        msg = Message(topic=topic, payload=payload)
        await self._r.xadd(
            self.stream,
            {
                "id": msg.id,
                "topic": topic,
                "payload": json.dumps(payload, default=str),
                "ts": str(msg.timestamp),
            },
            maxlen=self.stream_maxlen,
            approximate=True,
        )
        self.published += 1
        return msg

    # ---- consuming ------------------------------------------------------------
    async def _worker(self, sub: Subscription) -> None:
        try:
            # "$" = a brand-new group only receives messages published from now on
            await self._r.xgroup_create(self.stream, sub.name, id="$", mkstream=True)
        except ResponseError as exc:
            if "BUSYGROUP" not in str(exc):  # group already exists: fine
                raise
        while self._running:
            try:
                entries = await self._claim_stale(sub)
                if not entries:
                    resp = await self._r.xreadgroup(
                        sub.name, self.consumer, {self.stream: ">"}, count=10, block=1000
                    )
                    entries = [e for _, batch in resp for e in batch] if resp else []
                for entry_id, fields in entries:
                    await self._handle(sub, entry_id, fields)
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001 - e.g. Redis briefly unreachable
                log.error("%s: redis error: %s (retrying)", sub.name, exc)
                await asyncio.sleep(2)

    async def _claim_stale(self, sub: Subscription) -> list:
        """Take over messages another (crashed) consumer received but never acknowledged."""
        result = await self._r.xautoclaim(
            self.stream, sub.name, self.consumer, min_idle_time=self.claim_idle_ms, start_id="0-0", count=10
        )
        return [(i, f) for i, f in result[1] if f]  # deleted entries come back as (id, None)

    async def _handle(self, sub: Subscription, entry_id: str, fields: dict) -> None:
        topic = fields["topic"]
        if fnmatch(topic, sub.pattern):
            msg = Message(
                topic=topic,
                payload=json.loads(fields["payload"]),
                id=fields["id"],
                timestamp=float(fields["ts"]),
            )
            await self._deliver(sub, msg)
        await self._r.xack(self.stream, sub.name, entry_id)

    async def _dead_letter(self, sub: Subscription, msg: Message) -> None:
        entry = {"subscription": sub.name, "id": msg.id, "topic": msg.topic, "payload": msg.payload}
        await self._r.lpush(self.dead_key, json.dumps(entry, default=str))
        await self._r.ltrim(self.dead_key, 0, 999)

    async def dead_letters(self) -> list[dict]:
        return [json.loads(x) for x in await self._r.lrange(self.dead_key, 0, 99)]

    async def stats(self) -> dict:
        groups = {}
        try:
            groups = {g["name"]: g for g in await self._r.xinfo_groups(self.stream)}
        except ResponseError:  # stream doesn't exist yet
            pass
        return {
            "backend": "redis",
            "target": self._target,
            "running": self._running,
            "published_by_this_process": self.published,
            "dead_letters": await self._r.llen(self.dead_key),
            "subscriptions": [
                {
                    "name": s.name,
                    "pattern": s.pattern,
                    "in_flight": groups.get(s.name, {}).get("pending", 0),
                    "processed_by_this_process": s.processed,
                    "failed_by_this_process": s.failed,
                }
                for s in self._subs
            ],
        }
