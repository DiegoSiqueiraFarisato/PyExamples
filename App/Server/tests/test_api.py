from tests.conftest import wait_until


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_order_returns_201(client):
    r = client.post("/orders", json={"item": "book", "quantity": 2})
    assert r.status_code == 201
    assert r.json()["item"] == "book"


def test_invalid_quantity_is_rejected(client):
    assert client.post("/orders", json={"item": "book", "quantity": 0}).status_code == 422


def test_unknown_order_is_404(client):
    assert client.get("/orders/999999").status_code == 404


def test_order_is_shipped_through_the_broker(client):
    order_id = client.post("/orders", json={"item": "pen", "quantity": 1}).json()["id"]
    wait_until(lambda: client.get(f"/orders/{order_id}").json()["status"] == "shipped")
    assert order_id in client.get("/shipping").json()


def test_stats_and_no_dead_letters(client):
    stats = client.get("/broker/stats").json()
    assert stats["backend"] == "memory" and stats["running"] is True
    assert client.get("/broker/dead-letters").json() == []
