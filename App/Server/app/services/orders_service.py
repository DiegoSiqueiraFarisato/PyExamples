from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.broker import Broker, Message
from app.core.deps import get_broker

router = APIRouter(prefix="/orders", tags=["orders"])

_orders: dict[int, dict] = {}


class OrderIn(BaseModel):
    item: str
    quantity: int = Field(gt=0)


@router.post("", status_code=201)
async def create_order(body: OrderIn, broker: Broker = Depends(get_broker)):
    order = {"id": len(_orders) + 1, **body.model_dump(), "status": "created"}
    _orders[order["id"]] = order
    await broker.publish("order.created", order)
    return order


@router.get("/{order_id}")
async def get_order(order_id: int):
    if order_id not in _orders:
        raise HTTPException(404, "order not found")
    return _orders[order_id]


def register(broker: Broker) -> None:
    broker.subscribe("order.shipped", _on_shipped, name="orders.on_shipped")


async def _on_shipped(msg: Message) -> None:
    order = _orders.get(msg.payload["id"])
    if order:
        order["status"] = "shipped"
