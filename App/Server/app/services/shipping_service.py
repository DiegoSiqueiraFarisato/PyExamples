"""Reacts to new orders via the broker; its only endpoint is a read-only status view."""
import logging

from fastapi import APIRouter

from app.broker import Broker, Message

log = logging.getLogger("shipping")
router = APIRouter(prefix="/shipping", tags=["shipping"])

_shipped: list[int] = []
_broker: Broker | None = None


@router.get("")
async def shipped_orders():
    return _shipped


def register(broker: Broker) -> None:
    global _broker
    _broker = broker
    broker.subscribe("order.created", _on_order_created, name="shipping.on_order_created")


async def _on_order_created(msg: Message) -> None:
    order = msg.payload
    log.info("shipping order %s", order["id"])
    _shipped.append(order["id"])
    await _broker.publish("order.shipped", order)
