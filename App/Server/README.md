# PyExamples Server

A FastAPI back end with a pluggable message broker. Choose between an in-memory broker (no dependencies) and a Redis Streams broker (durable, multi-process) with a single setting.

## Features

- **Automatic service discovery**: drop a `*_service.py` file into `app/services/` and it is loaded at startup. Each service exposes a `router` and, optionally, a `register(broker)` function to subscribe to topics.
- **Pluggable broker**: in-memory or Redis Streams, selected by `BROKER_BACKEND`.
- **Reliable delivery** (Redis): consumer groups, ack after success, retry with backoff, reclaim of idle messages after 30s, and a dead-letter queue. Delivery is at-least-once, so handlers should be idempotent.
- **Simple configuration**: `config.env`, overridable by environment variables.
- **Example flow**: `POST /orders` → `order.created` → shipping service → `order.shipped` → order marked `shipped`.

## Requirements

- Windows with PowerShell
- Python 3.10+ (`setup.ps1` finds or installs it)
- Redis (optional, only for `BROKER_BACKEND=redis`)

## Quick start

From `App/Server/`:

```powershell
.\setup.ps1
```

This creates `.venv`, installs `requirements.txt` and starts the server. Use `-NoRun` to install only.

Afterwards, start the server with:

```powershell
.\server.cmd
# or
.\.venv\Scripts\python.exe -m app.main
```

Interactive API docs: http://127.0.0.1:8000/docs

## Configuration

Settings are read from `config.env`, or from the file named by the `APP_CONFIG` environment variable. Real environment variables take precedence over the file.

| Setting | Description |
| --- | --- |
| `BROKER_BACKEND` | `memory` or `redis` |

See `config.env` for the full list of options, and [GUIDE.md](GUIDE.md) for a step-by-step walkthrough (Redis setup, settings, Postman).

## Tests

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Tests always use the in-memory broker; Redis behaviour is exercised with `fakeredis`, so no Redis server is needed.

## Project layout

```
app/
  main.py        # FastAPI app, lifespan, service discovery
  core/          # config and dependency helpers
  broker/        # BaseBroker, memory and Redis backends, factory
  services/      # *_service.py modules (auto-loaded)
tests/           # pytest suite
```

## Adding a service

1. Create `app/services/my_service.py`.
2. Define `router = APIRouter()` with your endpoints.
3. Optionally define `register(broker)` to subscribe to topics (use a unique subscription `name=`).

No other wiring is needed.
