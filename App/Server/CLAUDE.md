# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

The Python project lives in `App/Server/` (the git root is `PyExamples/`). It is a FastAPI back end with a pluggable message broker (in-memory or Redis Streams). `GUIDE.md` is a detailed beginner-oriented guide (setup, Redis, settings, Postman); read it for user-facing details.

## Commands (run from `App/Server/`, Windows/PowerShell)

- Setup + run: `.\setup.ps1` (finds/installs Python 3.10+, creates `.venv`, installs `requirements.txt`, starts server). `-NoRun` installs only.
- Run (after setup): `.\server.cmd` or `.\.venv\Scripts\python.exe -m app.main`. Docs at http://127.0.0.1:8000/docs.
- Install test deps: `.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`
- Tests: `.\.venv\Scripts\python.exe -m pytest -q`
- Single test: `.\.venv\Scripts\python.exe -m pytest tests/test_api.py::test_name -q`

No linter is configured.

## Architecture

- **Service auto-discovery** (`app/main.py`): in the FastAPI lifespan, every module in `app/services/` whose name ends in `_service` is imported; its `router` (required) is included, and its optional `register(broker)` function is called to subscribe to topics. Adding a service = adding a `*_service.py` file; no other wiring.
- **Broker** (`app/broker/`): `BaseBroker` (`base.py`, exported as `Broker`) holds subscriptions and the shared `_deliver` logic (retry with linear backoff, then `_dead_letter`). Backends implement `publish/start/stop/stats/dead_letters/_spawn/_dead_letter`:
  - `memory.py`: per-subscription asyncio queues; messages lost on restart.
  - `redis_broker.py`: one Redis Stream (`<prefix>:events`), each subscription is a consumer group (so subscription `name=` must be unique and stable); ack only after success; idle un-acked messages are reclaimed after 30s; multiple server processes share work per subscription name. Delivery is at-least-once, so handlers must be idempotent.
  - `factory.py` picks the backend from `BROKER_BACKEND`; redis is imported lazily so memory mode works without it.
- **Dependency injection**: the broker lives on `app.state.broker`; endpoints get it via `Depends(get_broker)` from `app/core/deps.py`.
- **Config** (`app/core/config.py`): reads `config.env` (or the file named by `APP_CONFIG`); real environment variables override the file. Use `config.get(key, default)`.
- **Example flow**: `POST /orders` → orders_service publishes `order.created` → shipping_service handles it and publishes `order.shipped` → orders_service marks the order `shipped`. Orders are stored in an in-process dict (not durable); only messages are durable with Redis.

## Testing notes

- `tests/conftest.py` forces `BROKER_BACKEND=memory` before importing the app, so tests ignore `config.env`. The `client` fixture uses `with TestClient(app)` so lifespan (broker start) runs.
- Message delivery is async: use `wait_until(...)` from `conftest.py` to poll for results.
- `tests/test_broker.py` runs the same behaviour against both memory and Redis backends (Redis simulated with `fakeredis`; `RedisBroker` accepts an injected `client`).
- pytest uses `asyncio_mode = auto` (`pytest.ini`).
