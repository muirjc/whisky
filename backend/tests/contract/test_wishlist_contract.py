"""Contract tests for wishlist endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestWishlistContracts:
    async def test_list_empty_wishlist_returns_200(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        response = await client.get("/api/v1/wishlist", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["has_more"] is False

    async def test_unauthenticated_returns_401(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/wishlist")
        assert response.status_code in (401, 403)
