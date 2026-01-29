"""Integration tests for auth register/login flow."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAuthFlow:
    async def test_full_register_login_flow(self, client: AsyncClient) -> None:
        # Register
        reg_resp = await client.post(
            "/api/v1/auth/register",
            json={"email": "flow@example.com", "password": "flowpass123"},
        )
        assert reg_resp.status_code == 201
        user_id = reg_resp.json()["user"]["id"]

        # Login
        login_resp = await client.post(
            "/api/v1/auth/login",
            json={"email": "flow@example.com", "password": "flowpass123"},
        )
        assert login_resp.status_code == 200
        assert login_resp.json()["user"]["id"] == user_id

        # Access protected endpoint
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        bottles_resp = await client.get("/api/v1/bottles", headers=headers)
        assert bottles_resp.status_code == 200

    async def test_password_change_flow(self, client: AsyncClient) -> None:
        # Register
        reg_resp = await client.post(
            "/api/v1/auth/register",
            json={"email": "pwchange@example.com", "password": "oldpass123"},
        )
        token = reg_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Change password
        change_resp = await client.put(
            "/api/v1/auth/password",
            json={"current_password": "oldpass123", "new_password": "newpass123"},
            headers=headers,
        )
        assert change_resp.status_code == 204

        # Login with new password
        login_resp = await client.post(
            "/api/v1/auth/login",
            json={"email": "pwchange@example.com", "password": "newpass123"},
        )
        assert login_resp.status_code == 200

    async def test_data_isolation(self, client: AsyncClient) -> None:
        # Register two users
        resp1 = await client.post(
            "/api/v1/auth/register",
            json={"email": "user1@example.com", "password": "testpass123"},
        )
        resp2 = await client.post(
            "/api/v1/auth/register",
            json={"email": "user2@example.com", "password": "testpass123"},
        )
        h1 = {"Authorization": f"Bearer {resp1.json()['access_token']}"}
        h2 = {"Authorization": f"Bearer {resp2.json()['access_token']}"}

        # User 1 adds a bottle
        await client.post(
            "/api/v1/bottles",
            json={
                "name": "User1 Bottle",
                "distillery_name": "Test",
                "region": "Islay",
                "country": "Scotland",
            },
            headers=h1,
        )

        # User 2 should not see it
        resp = await client.get("/api/v1/bottles", headers=h2)
        assert resp.status_code == 200
        assert len(resp.json()["items"]) == 0
