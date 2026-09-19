from app.core import config

from .base import BaseBroker
from .memory import MemoryBroker


def create_broker() -> BaseBroker:
    backend = config.get("BROKER_BACKEND", "memory").lower()
    retries = int(config.get("BROKER_MAX_RETRIES", "3"))

    if backend == "memory":
        return MemoryBroker(max_retries=retries)

    if backend == "redis":
        from .redis_broker import RedisBroker  # imported here so 'memory' works without redis installed

        return RedisBroker(
            host=config.get("REDIS_HOST", "127.0.0.1"),
            port=int(config.get("REDIS_PORT", "6379")),
            db=int(config.get("REDIS_DB", "0")),
            password=config.get("REDIS_PASSWORD", ""),
            ssl=config.get("REDIS_SSL", "false").lower() in ("1", "true", "yes"),
            prefix=config.get("REDIS_PREFIX", "appserver"),
            max_retries=retries,
        )

    raise ValueError(f"BROKER_BACKEND must be 'memory' or 'redis', got '{backend}'")
