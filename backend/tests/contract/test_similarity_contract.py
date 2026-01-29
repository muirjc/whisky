"""Contract tests for similarity endpoint."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestSimilarityContracts:
    async def test_similar_returns_items(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        # Create a bottle with flavor profile
        bottle_data = {
            "name": "Test Peated",
            "distillery_name": "Test Distillery",
            "region": "Islay",
            "country": "Scotland",
            "flavor_profile": {
                "smoky_peaty": 5,
                "fruity": 2,
                "sherried": 1,
                "spicy": 2,
                "floral_grassy": 0,
                "maritime": 4,
                "honey_sweet": 1,
                "vanilla_caramel": 1,
                "oak_woody": 2,
                "nutty": 0,
                "malty_biscuity": 1,
                "medicinal_iodine": 4,
            },
        }
        create_resp = await client.post(
            "/api/v1/bottles", json=bottle_data, headers=auth_headers
        )
        bottle_id = create_resp.json()["id"]

        response = await client.get(
            f"/api/v1/bottles/{bottle_id}/similar", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    async def test_no_profile_returns_400(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        bottle_data = {
            "name": "No Profile",
            "distillery_name": "Test",
            "region": "Islay",
            "country": "Scotland",
        }
        create_resp = await client.post(
            "/api/v1/bottles", json=bottle_data, headers=auth_headers
        )
        bottle_id = create_resp.json()["id"]

        response = await client.get(
            f"/api/v1/bottles/{bottle_id}/similar", headers=auth_headers
        )
        assert response.status_code == 400
