"""Integration tests for distillery browsing."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestDistilleryBrowsing:
    async def test_list_distilleries(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/distilleries")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    async def test_search_distilleries(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/distilleries?search=lag")
        assert response.status_code == 200

    async def test_list_whiskies(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/whiskies")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
