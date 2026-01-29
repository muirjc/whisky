"""Contract tests for distillery endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestDistilleryContracts:
    async def test_list_distilleries_returns_200(self, client: AsyncClient) -> None:
        response = await client.get("/api/v1/distilleries")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "has_more" in data

    async def test_get_nonexistent_distillery_returns_404(
        self, client: AsyncClient
    ) -> None:
        response = await client.get("/api/v1/distilleries/nonexistent-slug")
        assert response.status_code == 404
