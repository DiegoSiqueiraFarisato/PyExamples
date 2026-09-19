"""In-process broker: no external dependencies, but messages are lost on restart
and cannot be shared between several server processes."""
from __future__ import annotations

import asyncio
import copy
import logging
from fnmatch import fnmatch
from typing import Any

from .base import BaseBroker, Message, Subscription

log = logging.getLogger("broker")


class MemoryBroker(BaseBroker):
    def __init__(self, max_retries: int = 3, retry_delay: float = 0.5, queue_size: int = 1000):
        super().__init__(max_retries, retry_delay)
        self.queue_size = queue_size
        self._dead: list[dict] = []

    def _setup(self, sub: Subscription) -> None:
        sub.queue = asyncio.Queue(self.queue_size)

    def _spawn(self, sub: Subscription) -> None:
        sub.task = asyncio.create_task(self._worker(sub))

    async def publish(self, topic: str, payload: Any) -> Message:
        msg = Message(topic=topic, payload=payload)
        self.published += 1
        for sub in self._subs:
            if fnmatch(topic, sub.pattern):
                await sub.queue.put(msg)
        return msg

    async def start(self) -> None:
        self._running = True
        for sub in self._subs:
            if sub.task is None:
                self._spawn(sub)
        log.info("memory broker started with %d subscription(s)", len(self._subs))

    async def stop(self) -> None:
        """Drain pending messages, then stop workers."""
        for sub in self._subs:
            await sub.queue.join()
        self._running = False
        for sub in self._subs:
            if sub.task:
                sub.task.cancel()
                sub.task = None
        log.info("memory broker stopped")

    async def _worker(self, sub: Subscription) -> None:
        while True:
            msg = await sub.queue.get()
            try:
                # each subscriber gets its own copy so attempt counters don't mix
                await self._deliver(sub, copy.copy(msg))
            finally:
                sub.queue.task_done()

    async def _dead_letter(self, sub: Subscription, msg: Message) -> None:
        self._dead.append(
            {"subscription": sub.name, "id": msg.id, "topic": msg.topic, "payload": msg.payload}
        )

    async def dead_letters(self) -> list[dict]:
        return list(self._dead)

    async def stats(self) -> dict:
        return {
            "backend": "memory",
            "running": self._running,
            "published": self.published,
            "dead_letters": len(self._dead),
            "subscriptions": [
                {
                    "name": s.name,
                    "pattern": s.pattern,
                    "pending": s.queue.qsize(),
                    "processed": s.processed,
                    "failed": s.failed,
                }
                for s in self._subs
            ],
        }
