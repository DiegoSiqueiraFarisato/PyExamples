import importlib
import logging
import pkgutil
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import services
from app.broker import create_broker
from app.core import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    broker = create_broker()
    app.state.broker = broker

    for info in pkgutil.iter_modules(services.__path__):
        if not info.name.endswith("_service"):
            continue
        module = importlib.import_module(f"app.services.{info.name}")
        app.include_router(module.router)
        if hasattr(module, "register"):
            module.register(broker)

    await broker.start()
    yield
    await broker.stop()


app = FastAPI(title="App Server", lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=config.HOST, port=config.PORT)
