"""Integration tests for wishlist endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.distillery import Distillery
from src.models.reference_whisky import ReferenceWhisky


async def _seed_reference_whisky(db_session: AsyncSession) -> str:
    """Create a reference whisky and return its ID."""
    import uuid

    dist_id = uuid.uuid4()
    distillery = Distillery(
        id=dist_id,
        slug="test-distillery",
        name="Test Distillery",
        region="Highland",
        country="Scotland",
        history="A test distillery.",
    )
    db_session.add(distillery)
    await db_session.flush()

    whisky = ReferenceWhisky(
        id=uuid.uuid4(),
        slug="test-whisky-12",
        name="Test Whisky 12",
        distillery_id=dist_id,
        region="Highland",
        country="Scotland",
        flavor_profile={"smoky_peaty": 3, "fruity": 4, "spicy": 2},
    )
    db_session.add(whisky)
    await db_session.flush()
    return str(whisky.id)


@pytest.mark.asyncio
class TestWishlistFlow:
    async def test_add_list_and_remove(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
        db_session: AsyncSession,
    ) -> None:
        whisky_id = await _seed_reference_whisky(db_session)
        await db_session.commit()

        # Add to wishlist
        resp = await client.post(
            "/api/v1/wishlist",
            json={"reference_whisky_id": whisky_id, "notes": "Want to try"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["notes"] == "Want to try"
        item_id = data["id"]

        # List wishlist
        list_resp = await client.get("/api/v1/wishlist", headers=auth_headers)
        assert list_resp.status_code == 200
        items = list_resp.json()["items"]
        assert len(items) == 1

        # Remove
        del_resp = await client.delete(
            f"/api/v1/wishlist/{item_id}", headers=auth_headers
        )
        assert del_resp.status_code == 204

        # Verify empty
        list_resp2 = await client.get("/api/v1/wishlist", headers=auth_headers)
        assert len(list_resp2.json()["items"]) == 0

    async def test_add_duplicate_returns_409(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
        db_session: AsyncSession,
    ) -> None:
        whisky_id = await _seed_reference_whisky(db_session)
        await db_session.commit()

        await client.post(
            "/api/v1/wishlist",
            json={"reference_whisky_id": whisky_id},
            headers=auth_headers,
        )
        resp = await client.post(
            "/api/v1/wishlist",
            json={"reference_whisky_id": whisky_id},
            headers=auth_headers,
        )
        assert resp.status_code == 409

    async def test_remove_nonexistent_returns_404(
        self,
        client: AsyncClient,
        auth_headers: dict[str, str],
    ) -> None:
        import uuid

        resp = await client.delete(
            f"/api/v1/wishlist/{uuid.uuid4()}", headers=auth_headers
        )
        assert resp.status_code == 404
