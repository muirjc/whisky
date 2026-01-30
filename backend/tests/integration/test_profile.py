"""Integration tests for taste profile endpoint."""

import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.distillery import Distillery
from src.models.reference_whisky import ReferenceWhisky


BOTTLE_WITH_PROFILE = {
    "name": "Laphroaig 10",
    "distillery_name": "Laphroaig",
    "region": "Islay",
    "country": "Scotland",
    "flavor_profile": {
        "smoky_peaty": 5,
        "fruity": 1,
        "sherried": 0,
        "spicy": 2,
        "floral_grassy": 0,
        "maritime": 4,
        "honey_sweet": 0,
        "vanilla_caramel": 1,
        "oak_woody": 2,
        "nutty": 0,
        "malty_biscuity": 0,
        "medicinal_iodine": 3,
    },
}


@pytest.mark.asyncio
class TestTasteProfile:
    async def test_empty_collection_returns_zeros(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        resp = await client.get("/api/v1/profile/taste", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_bottles"] == 0
        assert data["bottles_with_profiles"] == 0
        assert all(v == 0.0 for v in data["average_profile"].values())

    async def test_profile_with_bottles(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        # Add bottle with flavor profile
        await client.post(
            "/api/v1/bottles", json=BOTTLE_WITH_PROFILE, headers=auth_headers
        )

        resp = await client.get("/api/v1/profile/taste", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_bottles"] == 1
        assert data["bottles_with_profiles"] == 1
        assert data["average_profile"]["smoky_peaty"] == 5.0
        assert len(data["dominant_flavors"]) > 0
        assert "Islay" in data["region_distribution"]

    async def test_profile_with_recommendations(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
        db_session: AsyncSession,
    ) -> None:
        # Seed reference whiskies so recommendations can be generated
        dist_id = uuid.uuid4()
        db_session.add(Distillery(
            id=dist_id, slug="ardbeg", name="Ardbeg",
            region="Islay", country="Scotland", history="Peaty.",
        ))
        db_session.add(ReferenceWhisky(
            id=uuid.uuid4(), slug="ardbeg-10", name="Ardbeg 10",
            distillery_id=dist_id, region="Islay", country="Scotland",
            flavor_profile={"smoky_peaty": 5, "fruity": 2, "maritime": 3},
        ))
        await db_session.flush()
        await db_session.commit()

        # Add bottle with flavor profile
        await client.post(
            "/api/v1/bottles", json=BOTTLE_WITH_PROFILE, headers=auth_headers
        )

        resp = await client.get("/api/v1/profile/taste", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["bottles_with_profiles"] == 1
        assert len(data["recommendations"]) > 0
