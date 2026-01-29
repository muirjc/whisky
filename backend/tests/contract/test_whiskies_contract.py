"""Contract tests for reference whisky endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestWhiskiesContracts:
    async def test_list_whiskies_returns_200(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/whiskies")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "has_more" in data

    async def test_get_nonexistent_whisky_returns_404(
        self, client: AsyncClient
    ) -> None:
        response = await client.get("/api/v1/whiskies/nonexistent-slug")
        assert response.status_code == 404
