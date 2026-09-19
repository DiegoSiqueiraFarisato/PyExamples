import os
import time

import pytest

# Tests always use the in-memory broker, whatever config.env says.
os.environ["BROKER_BACKEND"] = "memory"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture()
def client():
    with TestClient(app) as c:  # 'with' runs startup/shutdown, so the broker is live
        yield c


def wait_until(fn, timeout=3.0, interval=0.05):
    """Poll fn() until it returns something truthy (messages are delivered asynchronously)."""
    end = time.time() + timeout
    while time.time() < end:
        result = fn()
        if result:
            return result
        time.sleep(interval)
    raise AssertionError("condition not met in time")
