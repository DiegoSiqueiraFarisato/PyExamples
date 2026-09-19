from fastapi import APIRouter, Depends

from app.broker import Broker
from app.core.deps import get_broker

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/broker/stats")
async def broker_stats(broker: Broker = Depends(get_broker)):
    return await broker.stats()


@router.get("/broker/dead-letters")
async def dead_letters(broker: Broker = Depends(get_broker)):
    return await broker.dead_letters()
