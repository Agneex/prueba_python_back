from tests.helpers import register_and_login


async def test_list_examples(client):
    response = await client.get("/functions/examples")

    assert response.status_code == 200
    slugs = [example["slug"] for example in response.json()]
    assert {"esfera", "toro", "gyroide"} <= set(slugs)


async def test_add_example_creates_function_for_user(client):
    _, headers = await register_and_login(client, "ana")

    response = await client.post("/functions/examples/toro", headers=headers)
    functions = (await client.get("/functions", headers=headers)).json()

    assert response.status_code == 201
    assert [function["name"] for function in functions] == ["Toro"]


async def test_add_unknown_example_returns_404(client):
    _, headers = await register_and_login(client, "ana")

    response = await client.post("/functions/examples/cubo", headers=headers)

    assert response.status_code == 404
