"""Integration tests for bottle CRUD operations."""

import uuid

import pytest
from httpx import AsyncClient


BOTTLE_DATA = {
    "name": "Lagavulin 16",
    "distillery_name": "Lagavulin",
    "region": "Islay",
    "country": "Scotland",
    "rating": 5,
    "status": "opened",
}


@pytest.mark.asyncio
class TestBottleCRUD:
    async def test_create_bottle(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        resp = await client.post("/api/v1/bottles", json=BOTTLE_DATA, headers=auth_headers)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Lagavulin 16"
        assert data["region"] == "Islay"
        assert "id" in data

    async def test_get_bottle(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        create_resp = await client.post("/api/v1/bottles", json=BOTTLE_DATA, headers=auth_headers)
        bottle_id = create_resp.json()["id"]

        resp = await client.get(f"/api/v1/bottles/{bottle_id}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["name"] == "Lagavulin 16"

    async def test_get_nonexistent_bottle_returns_404(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        resp = await client.get(f"/api/v1/bottles/{uuid.uuid4()}", headers=auth_headers)
        assert resp.status_code == 404

    async def test_update_bottle(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        create_resp = await client.post("/api/v1/bottles", json=BOTTLE_DATA, headers=auth_headers)
        bottle_id = create_resp.json()["id"]

        resp = await client.put(
            f"/api/v1/bottles/{bottle_id}",
            json={"name": "Lagavulin 16 Updated", "rating": 4},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Lagavulin 16 Updated"

    async def test_update_nonexistent_returns_404(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        resp = await client.put(
            f"/api/v1/bottles/{uuid.uuid4()}",
            json={"name": "No"},
            headers=auth_headers,
        )
        assert resp.status_code == 404

    async def test_delete_bottle(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        create_resp = await client.post("/api/v1/bottles", json=BOTTLE_DATA, headers=auth_headers)
        bottle_id = create_resp.json()["id"]

        resp = await client.delete(f"/api/v1/bottles/{bottle_id}", headers=auth_headers)
        assert resp.status_code == 204

        # Verify deleted
        get_resp = await client.get(f"/api/v1/bottles/{bottle_id}", headers=auth_headers)
        assert get_resp.status_code == 404

    async def test_delete_nonexistent_returns_404(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        resp = await client.delete(f"/api/v1/bottles/{uuid.uuid4()}", headers=auth_headers)
        assert resp.status_code == 404
