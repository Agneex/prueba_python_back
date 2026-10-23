from httpx import AsyncClient


async def register_and_login(client: AsyncClient, username: str) -> tuple[int, dict[str, str]]:
    response = await client.post(
        "/auth/register",
        json={"username": username, "email": f"{username}@example.com", "password": "s3cret-pass"},
    )
    user_id = response.json()["id"]
    token_response = await client.post(
        "/auth/token", data={"username": username, "password": "s3cret-pass"}
    )
    return user_id, {"Authorization": f"Bearer {token_response.json()['access_token']}"}
