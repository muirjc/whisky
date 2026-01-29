"""Integration tests for recommendation flow."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRecommendationFlow:
    async def test_similar_whiskies_endpoint(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        # Create a bottle with flavor profile
        bottle = {
            "name": "Test Peated",
            "distillery_name": "Test",
            "region": "Islay",
            "country": "Scotland",
            "flavor_profile": {
                "smoky_peaty": 5,
                "fruity": 1,
                "sherried": 1,
                "spicy": 2,
                "floral_grassy": 0,
                "maritime": 5,
                "honey_sweet": 0,
                "vanilla_caramel": 1,
                "oak_woody": 2,
                "nutty": 0,
                "malty_biscuity": 1,
                "medicinal_iodine": 4,
            },
        }
        resp = await client.post("/api/v1/bottles", json=bottle, headers=auth_headers)
        bottle_id = resp.json()["id"]

        similar_resp = await client.get(
            f"/api/v1/bottles/{bottle_id}/similar?limit=5", headers=auth_headers
        )
        assert similar_resp.status_code == 200
        assert "items" in similar_resp.json()
