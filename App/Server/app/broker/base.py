"""Common pieces shared by every broker backend (in-memory and Redis)."""
from __future__ import annotations

import asyncio
import logging
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable

log = logging.getLogger("broker")


@dataclass
class Message:
    topic: str
    payload: Any
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    timestamp: float = field(default_factory=time.time)
    attempts: int = 0


Handler = Callable[[Message], Awaitable[None]]


@dataclass
class Subscription:
    name: str  # must be unique; the Redis backend uses it as the consumer-group name
    pattern: str
    handler: Handler
    processed: int = 0
    failed: int = 0
    task: asyncio.Task | None = None
    queue: asyncio.Queue | None = None  # in-memory backend only


class BaseBroker(ABC):
    def __init__(self, max_retries: int = 3, retry_delay: float = 0.5):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.published = 0
        self._subs: list[Subscription] = []
        self._running = False

    # ---- API used by services -------------------------------------------------
    def subscribe(self, pattern: str, handler: Handler, name: str | None = None) -> None:
        sub = Subscription(
            name=name or f"{handler.__module__}.{handler.__qualname__}",
            pattern=pattern,
            handler=handler,
        )
        if any(s.name == sub.name for s in self._subs):
            raise ValueError(f"duplicate subscription name: {sub.name}")
        self._setup(sub)
        self._subs.append(sub)
        if self._running:
            self._spawn(sub)

    def on(self, pattern: str):
        """Decorator form of subscribe()."""
        def decorator(fn: Handler) -> Handler:
            self.subscribe(pattern, fn)
            return fn
        return decorator

    @abstractmethod
    async def publish(self, topic: str, payload: Any) -> Message: ...

    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def stop(self) -> None: ...

    @abstractmethod
    async def stats(self) -> dict: ...

    @abstractmethod
    async def dead_letters(self) -> list[dict]: ...

    # ---- backend hooks --------------------------------------------------------
    def _setup(self, sub: Subscription) -> None:
        """Called once when a subscription is created."""

    @abstractmethod
    def _spawn(self, sub: Subscription) -> None:
        """Start the worker task for a subscription."""

    @abstractmethod
    async def _dead_letter(self, sub: Subscription, msg: Message) -> None: ...

    # ---- shared delivery logic ------------------------------------------------
    async def _deliver(self, sub: Subscription, msg: Message) -> None:
        """Call the handler, retrying with backoff; dead-letter the message if it keeps failing."""
        for attempt in range(1, self.max_retries + 1):
            msg.attempts = attempt
            try:
                await sub.handler(msg)
                sub.processed += 1
                return
            except Exception as exc:  # noqa: BLE001 - handler errors must not kill the worker
                log.warning("%s failed on %s (attempt %d): %s", sub.name, msg.id, attempt, exc)
                if attempt < self.max_retries:
                    await asyncio.sleep(self.retry_delay * attempt)
        sub.failed += 1
        await self._dead_letter(sub, msg)
