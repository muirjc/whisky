"""Integration tests for similar whiskies endpoint."""

import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.distillery import Distillery
from src.models.reference_whisky import ReferenceWhisky


async def _seed_ref_data(db_session: AsyncSession) -> None:
    """Seed reference data for similarity tests."""
    dist_id = uuid.uuid4()
    dist = Distillery(
        id=dist_id,
        slug="ardbeg",
        name="Ardbeg",
        region="Islay",
        country="Scotland",
        history="Peaty Islay distillery.",
    )
    db_session.add(dist)

    for slug, name, profile in [
        ("ardbeg-10", "Ardbeg 10", {"smoky_peaty": 5, "fruity": 2}),
        ("ardbeg-uigeadail", "Ardbeg Uigeadail", {"smoky_peaty": 5, "sherried": 4}),
    ]:
        db_session.add(ReferenceWhisky(
            id=uuid.uuid4(),
            slug=slug,
            name=name,
            distillery_id=dist_id,
            region="Islay",
            country="Scotland",
            flavor_profile=profile,
        ))
    await db_session.flush()
    await db_session.commit()


@pytest.mark.asyncio
class TestSimilarWhiskies:
    async def test_similar_with_profile(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
        db_session: AsyncSession,
    ) -> None:
        await _seed_ref_data(db_session)

        # Create bottle with peaty profile
        resp = await client.post(
            "/api/v1/bottles",
            json={
                "name": "My Peaty Bottle",
                "distillery_name": "Ardbeg",
                "region": "Islay",
                "country": "Scotland",
                "flavor_profile": {
                    "smoky_peaty": 5, "fruity": 1, "sherried": 0,
                    "spicy": 0, "floral_grassy": 0, "maritime": 3,
                    "honey_sweet": 0, "vanilla_caramel": 0, "oak_woody": 1,
                    "nutty": 0, "malty_biscuity": 0, "medicinal_iodine": 4,
                },
            },
            headers=auth_headers,
        )
        bottle_id = resp.json()["id"]

        similar_resp = await client.get(
            f"/api/v1/bottles/{bottle_id}/similar", headers=auth_headers
        )
        assert similar_resp.status_code == 200
        data = similar_resp.json()
        assert len(data["items"]) > 0
        assert "similarity_score" in data["items"][0]

    async def test_similar_without_profile_returns_400(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
    ) -> None:
        # Create bottle with no profile
        resp = await client.post(
            "/api/v1/bottles",
            json={
                "name": "No Profile",
                "distillery_name": "Test",
                "region": "Islay",
                "country": "Scotland",
            },
            headers=auth_headers,
        )
        bottle_id = resp.json()["id"]

        similar_resp = await client.get(
            f"/api/v1/bottles/{bottle_id}/similar", headers=auth_headers
        )
        assert similar_resp.status_code == 400
