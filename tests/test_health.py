async def test_health_returns_ok(client):
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_health_propagates_request_id(client):
    response = await client.get("/health", headers={"X-Request-ID": "abc123"})

    assert response.headers["X-Request-ID"] == "abc123"


async def test_viewer_is_served(client):
    response = await client.get("/viewer")

    assert response.status_code == 200
    assert "Visor de volúmenes" in response.text
