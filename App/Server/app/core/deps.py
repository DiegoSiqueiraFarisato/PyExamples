from fastapi import Request

from app.broker import Broker


def get_broker(request: Request) -> Broker:
    return request.app.state.broker
