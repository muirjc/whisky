"""Contract tests for bottle CRUD endpoints."""

import pytest
from httpx import AsyncClient


SAMPLE_BOTTLE = {
    "name": "Lagavulin 16",
    "distillery_name": "Lagavulin",
    "region": "Islay",
    "country": "Scotland",
    "age_statement": 16,
    "abv": 43.0,
    "rating": 5,
    "status": "sealed",
}


@pytest.mark.asyncio
class TestBottleCrudContracts:
    async def test_create_bottle_returns_201(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        response = await client.post(
            "/api/v1/bottles", json=SAMPLE_BOTTLE, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Lagavulin 16"
        assert "id" in data
        assert "created_at" in data

    async def test_get_bottle_returns_200(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        create_resp = await client.post(
            "/api/v1/bottles", json=SAMPLE_BOTTLE, headers=auth_headers
        )
        bottle_id = create_resp.json()["id"]
        response = await client.get(
            f"/api/v1/bottles/{bottle_id}", headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Lagavulin 16"

    async def test_update_bottle_returns_200(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        create_resp = await client.post(
            "/api/v1/bottles", json=SAMPLE_BOTTLE, headers=auth_headers
        )
        bottle_id = create_resp.json()["id"]
        response = await client.put(
            f"/api/v1/bottles/{bottle_id}",
            json={"name": "Lagavulin 16 Updated", "status": "opened"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Lagavulin 16 Updated"

    async def test_delete_bottle_returns_204(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        create_resp = await client.post(
            "/api/v1/bottles", json=SAMPLE_BOTTLE, headers=auth_headers
        )
        bottle_id = create_resp.json()["id"]
        response = await client.delete(
            f"/api/v1/bottles/{bottle_id}", headers=auth_headers
        )
        assert response.status_code == 204

    async def test_list_bottles_returns_200(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        await client.post(
            "/api/v1/bottles", json=SAMPLE_BOTTLE, headers=auth_headers
        )
        response = await client.get("/api/v1/bottles", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "has_more" in data
        assert len(data["items"]) >= 1

    async def test_get_nonexistent_bottle_returns_404(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        import uuid

        response = await client.get(
            f"/api/v1/bottles/{uuid.uuid4()}", headers=auth_headers
        )
        assert response.status_code == 404

    async def test_unauthenticated_returns_401(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/bottles")
        assert response.status_code in (401, 403)
