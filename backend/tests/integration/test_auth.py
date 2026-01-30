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
        reg_resp = await client.post(
            "/api/v1/auth/register",
            json={"email": "pwchange@example.com", "password": "oldpass123"},
        )
        token = reg_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        change_resp = await client.put(
            "/api/v1/auth/password",
            json={"current_password": "oldpass123", "new_password": "newpass123"},
            headers=headers,
        )
        assert change_resp.status_code == 204

        login_resp = await client.post(
            "/api/v1/auth/login",
            json={"email": "pwchange@example.com", "password": "newpass123"},
        )
        assert login_resp.status_code == 200

    async def test_data_isolation(self, client: AsyncClient) -> None:
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

        resp = await client.get("/api/v1/bottles", headers=h2)
        assert resp.status_code == 200
        assert len(resp.json()["items"]) == 0

    async def test_login_wrong_password(self, client: AsyncClient) -> None:
        await client.post(
            "/api/v1/auth/register",
            json={"email": "wrongpw@example.com", "password": "correctpass1"},
        )
        resp = await client.post(
            "/api/v1/auth/login",
            json={"email": "wrongpw@example.com", "password": "wrongpassword"},
        )
        assert resp.status_code == 401

    async def test_login_nonexistent_user(self, client: AsyncClient) -> None:
        resp = await client.post(
            "/api/v1/auth/login",
            json={"email": "nobody@example.com", "password": "password123"},
        )
        assert resp.status_code == 401

    async def test_register_duplicate_email(self, client: AsyncClient) -> None:
        await client.post(
            "/api/v1/auth/register",
            json={"email": "dupe@example.com", "password": "dupepass123"},
        )
        resp = await client.post(
            "/api/v1/auth/register",
            json={"email": "dupe@example.com", "password": "dupepass456"},
        )
        assert resp.status_code == 409

    async def test_refresh_token(self, client: AsyncClient) -> None:
        resp = await client.post(
            "/api/v1/auth/register",
            json={"email": "refresh@example.com", "password": "refreshpass123"},
        )
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        refresh_resp = await client.post("/api/v1/auth/refresh", headers=headers)
        assert refresh_resp.status_code == 200
        assert "access_token" in refresh_resp.json()

    async def test_invalid_bearer_token(self, client: AsyncClient) -> None:
        resp = await client.get(
            "/api/v1/bottles",
            headers={"Authorization": "Bearer invalid.token.value"},
        )
        assert resp.status_code in (401, 403)

    async def test_change_password_wrong_current(self, client: AsyncClient) -> None:
        reg = await client.post(
            "/api/v1/auth/register",
            json={"email": "badchange@example.com", "password": "badchange123"},
        )
        headers = {"Authorization": f"Bearer {reg.json()['access_token']}"}
        resp = await client.put(
            "/api/v1/auth/password",
            json={"current_password": "wrongpass123", "new_password": "newpass12345"},
            headers=headers,
        )
        assert resp.status_code == 401

    async def test_logout(self, client: AsyncClient) -> None:
        reg = await client.post(
            "/api/v1/auth/register",
            json={"email": "logout@example.com", "password": "logoutpass123"},
        )
        headers = {"Authorization": f"Bearer {reg.json()['access_token']}"}
        resp = await client.post("/api/v1/auth/logout", headers=headers)
        assert resp.status_code == 204

    async def test_password_reset_request(self, client: AsyncClient) -> None:
        resp = await client.post(
            "/api/v1/auth/password/reset",
            json={"email": "anyone@example.com"},
        )
        assert resp.status_code == 202
