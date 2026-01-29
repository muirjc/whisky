"""Integration tests for bottle add/edit flow."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestBottleFlow:
    async def test_add_and_retrieve_bottle(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        bottle = {
            "name": "Ardbeg 10",
            "distillery_name": "Ardbeg",
            "region": "Islay",
            "country": "Scotland",
            "age_statement": 10,
            "abv": 46.0,
            "rating": 4,
        }
        create_resp = await client.post(
            "/api/v1/bottles", json=bottle, headers=auth_headers
        )
        assert create_resp.status_code == 201
        bottle_id = create_resp.json()["id"]

        get_resp = await client.get(
            f"/api/v1/bottles/{bottle_id}", headers=auth_headers
        )
        assert get_resp.status_code == 200
        data = get_resp.json()
        assert data["name"] == "Ardbeg 10"
        assert data["age_statement"] == 10

    async def test_edit_bottle(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        bottle = {
            "name": "Test Edit",
            "distillery_name": "Test",
            "region": "Islay",
            "country": "Scotland",
            "status": "sealed",
        }
        create_resp = await client.post(
            "/api/v1/bottles", json=bottle, headers=auth_headers
        )
        bottle_id = create_resp.json()["id"]

        update_resp = await client.put(
            f"/api/v1/bottles/{bottle_id}",
            json={"status": "opened", "tasting_notes": "Lovely peat smoke"},
            headers=auth_headers,
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["status"] == "opened"
        assert update_resp.json()["tasting_notes"] == "Lovely peat smoke"

    async def test_delete_bottle(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        bottle = {
            "name": "To Delete",
            "distillery_name": "Test",
            "region": "Highland",
            "country": "Scotland",
        }
        create_resp = await client.post(
            "/api/v1/bottles", json=bottle, headers=auth_headers
        )
        bottle_id = create_resp.json()["id"]

        delete_resp = await client.delete(
            f"/api/v1/bottles/{bottle_id}", headers=auth_headers
        )
        assert delete_resp.status_code == 204

        get_resp = await client.get(
            f"/api/v1/bottles/{bottle_id}", headers=auth_headers
        )
        assert get_resp.status_code == 404
