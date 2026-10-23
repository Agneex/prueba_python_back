from tests.helpers import register_and_login

SPHERE = {
    "name": "Esfera",
    "expression": "x**2 + y**2 + z**2 - 1",
    "domain": [[-1.5, 1.5], [-1.5, 1.5], [-1.5, 1.5]],
}


async def test_create_function_uses_default_resolution(client):
    _, headers = await register_and_login(client, "ana")

    response = await client.post("/functions", json=SPHERE, headers=headers)

    assert response.status_code == 201
    body = response.json()
    assert body["resolution"] == 64
    assert body["version"] == 1


async def test_list_only_returns_own_functions(client):
    _, ana_headers = await register_and_login(client, "ana")
    _, bob_headers = await register_and_login(client, "bob")
    await client.post("/functions", json=SPHERE, headers=ana_headers)

    response = await client.get("/functions", headers=bob_headers)

    assert response.status_code == 200
    assert response.json() == []


async def test_create_rejects_inverted_domain(client):
    _, headers = await register_and_login(client, "ana")
    payload = {**SPHERE, "domain": [[1, -1], [-1, 1], [-1, 1]]}

    response = await client.post("/functions", json=payload, headers=headers)

    assert response.status_code == 422


async def test_create_rejects_resolution_out_of_range(client):
    _, headers = await register_and_login(client, "ana")

    response = await client.post("/functions", json={**SPHERE, "resolution": 4}, headers=headers)

    assert response.status_code == 422


async def test_update_increments_version(client):
    _, headers = await register_and_login(client, "ana")
    created = (await client.post("/functions", json=SPHERE, headers=headers)).json()

    response = await client.patch(
        f"/functions/{created['id']}", json={"expression": "x**2 + y**2 + z**2 - 4"}, headers=headers
    )

    assert response.status_code == 200
    assert response.json()["version"] == 2
