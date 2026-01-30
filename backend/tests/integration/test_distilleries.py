"""Integration tests for distillery browsing."""

import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.distillery import Distillery
from src.models.reference_whisky import ReferenceWhisky


async def _seed_distilleries(db_session: AsyncSession) -> None:
    """Seed test distilleries and whiskies."""
    lag_id = uuid.uuid4()
    for did, slug, name, region in [
        (lag_id, "lagavulin", "Lagavulin", "Islay"),
        (uuid.uuid4(), "macallan", "Macallan", "Speyside"),
        (uuid.uuid4(), "talisker", "Talisker", "Islands"),
    ]:
        db_session.add(Distillery(
            id=did,
            slug=slug,
            name=name,
            region=region,
            country="Scotland",
            history=f"{name} distillery.",
        ))

    db_session.add(ReferenceWhisky(
        id=uuid.uuid4(),
        slug="lagavulin-16",
        name="Lagavulin 16",
        distillery_id=lag_id,
        region="Islay",
        country="Scotland",
        flavor_profile={"smoky_peaty": 5, "fruity": 1},
    ))
    await db_session.flush()
    await db_session.commit()


@pytest.mark.asyncio
class TestDistilleryBrowsing:
    async def test_list_distilleries(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _seed_distilleries(db_session)
        response = await client.get("/api/v1/distilleries")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3

    async def test_search_distilleries(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _seed_distilleries(db_session)
        response = await client.get("/api/v1/distilleries?search=lag")
        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == 1
        assert items[0]["name"] == "Lagavulin"

    async def test_filter_by_region(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _seed_distilleries(db_session)
        response = await client.get("/api/v1/distilleries?region=Islay")
        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == 1

    async def test_get_distillery_by_slug(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _seed_distilleries(db_session)
        response = await client.get("/api/v1/distilleries/lagavulin")
        assert response.status_code == 200
        assert response.json()["name"] == "Lagavulin"

    async def test_get_nonexistent_returns_404(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/distilleries/does-not-exist")
        assert response.status_code == 404

    async def test_filter_by_country(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _seed_distilleries(db_session)
        response = await client.get("/api/v1/distilleries?country=Scotland")
        assert response.status_code == 200
        assert len(response.json()["items"]) == 3

    async def test_pagination(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _seed_distilleries(db_session)
        response = await client.get("/api/v1/distilleries?limit=2")
        data = response.json()
        assert len(data["items"]) == 2
        assert data["has_more"] is True

        resp2 = await client.get(f"/api/v1/distilleries?limit=2&cursor={data['next_cursor']}")
        data2 = resp2.json()
        assert len(data2["items"]) == 1

    async def test_distillery_whiskies(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _seed_distilleries(db_session)
        response = await client.get("/api/v1/distilleries/lagavulin/whiskies")
        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) == 1
        assert items[0]["name"] == "Lagavulin 16"
