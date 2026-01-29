"""Contract tests for auth endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAuthContracts:
    async def test_register_returns_201(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "new@example.com", "password": "testpass123"},
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
        assert "user" in data
        assert data["user"]["email"] == "new@example.com"
        assert "id" in data["user"]

    async def test_register_duplicate_returns_409(self, client: AsyncClient) -> None:
        await client.post(
            "/api/v1/auth/register",
            json={"email": "dup@example.com", "password": "testpass123"},
        )
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "dup@example.com", "password": "testpass123"},
        )
        assert response.status_code == 409

    async def test_register_invalid_email_returns_422(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "not-an-email", "password": "testpass123"},
        )
        assert response.status_code == 422

    async def test_login_returns_200(self, client: AsyncClient) -> None:
        await client.post(
            "/api/v1/auth/register",
            json={"email": "login@example.com", "password": "testpass123"},
        )
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "login@example.com", "password": "testpass123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    async def test_login_wrong_password_returns_401(self, client: AsyncClient) -> None:
        await client.post(
            "/api/v1/auth/register",
            json={"email": "wrong@example.com", "password": "testpass123"},
        )
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "wrong@example.com", "password": "wrongpass123"},
        )
        assert response.status_code == 401

    async def test_logout_returns_204(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        response = await client.post("/api/v1/auth/logout", headers=auth_headers)
        assert response.status_code == 204

    async def test_password_change_returns_204(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        response = await client.put(
            "/api/v1/auth/password",
            json={"current_password": "testpass123", "new_password": "newpass1234"},
            headers=auth_headers,
        )
        assert response.status_code == 204

    async def test_password_reset_returns_202(self, client: AsyncClient) -> None:
        response = await client.post(
            "/api/v1/auth/password/reset",
            json={"email": "anyone@example.com"},
        )
        assert response.status_code == 202
