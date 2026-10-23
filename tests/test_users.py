import re

from tests.helpers import register_and_login

DATETIME_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")


async def test_get_own_user_includes_generated_at(client):
    user_id, headers = await register_and_login(client, "ana")

    response = await client.get(f"/users/{user_id}", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == user_id
    assert DATETIME_PATTERN.match(body["generated_at"])


async def test_get_user_requires_token(client):
    user_id, _ = await register_and_login(client, "ana")

    response = await client.get(f"/users/{user_id}")

    assert response.status_code == 401


async def test_get_other_user_is_forbidden(client):
    ana_id, _ = await register_and_login(client, "ana")
    _, bob_headers = await register_and_login(client, "bob")

    response = await client.get(f"/users/{ana_id}", headers=bob_headers)

    assert response.status_code == 403
