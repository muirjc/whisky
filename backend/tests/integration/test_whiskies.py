"""Integration tests for reference whisky endpoints."""

import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.distillery import Distillery
from src.models.reference_whisky import ReferenceWhisky


async def _seed_whiskies(db_session: AsyncSession) -> None:
    """Seed test distillery and whiskies."""
    dist_id = uuid.uuid4()
    dist = Distillery(
        id=dist_id,
        slug="highland-park",
        name="Highland Park",
        region="Islands",
        country="Scotland",
        history="Orkney distillery.",
    )
    db_session.add(dist)

    for i, (name, slug) in enumerate([
        ("Highland Park 12", "highland-park-12"),
        ("Highland Park 18", "highland-park-18"),
        ("Highland Park 25", "highland-park-25"),
    ]):
        w = ReferenceWhisky(
            id=uuid.uuid4(),
            slug=slug,
            name=name,
            distillery_id=dist_id,
            region="Islands",
            country="Scotland",
            flavor_profile={"smoky_peaty": 2 + i, "honey_sweet": 3},
        )
        db_session.add(w)

    await db_session.flush()
    await db_session.commit()


@pytest.mark.asyncio
class TestReferenceWhiskies:
    async def test_list_whiskies(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _seed_whiskies(db_session)
        resp = await client.get("/api/v1/whiskies")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["items"]) == 3

    async def test_search_whiskies(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _seed_whiskies(db_session)
        resp = await client.get("/api/v1/whiskies?search=18")
        assert resp.status_code == 200
        items = resp.json()["items"]
        assert len(items) == 1
        assert "18" in items[0]["name"]

    async def test_get_whisky_by_slug(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _seed_whiskies(db_session)
        resp = await client.get("/api/v1/whiskies/highland-park-12")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Highland Park 12"

    async def test_filter_by_region(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _seed_whiskies(db_session)
        resp = await client.get("/api/v1/whiskies?region=Islands")
        assert resp.status_code == 200
        assert len(resp.json()["items"]) == 3

    async def test_pagination(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _seed_whiskies(db_session)
        resp = await client.get("/api/v1/whiskies?limit=2")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["items"]) == 2
        assert data["has_more"] is True

        resp2 = await client.get(f"/api/v1/whiskies?limit=2&cursor={data['next_cursor']}")
        data2 = resp2.json()
        assert len(data2["items"]) == 1

    async def test_get_nonexistent_whisky(self, client: AsyncClient) -> None:
        resp = await client.get("/api/v1/whiskies/does-not-exist")
        assert resp.status_code == 404
