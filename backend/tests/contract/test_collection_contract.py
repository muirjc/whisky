"""Contract tests for collection list/search/filter endpoints."""

import pytest
from httpx import AsyncClient


BOTTLES = [
    {
        "name": "Lagavulin 16",
        "distillery_name": "Lagavulin",
        "region": "Islay",
        "country": "Scotland",
        "status": "sealed",
    },
    {
        "name": "Macallan 18",
        "distillery_name": "Macallan",
        "region": "Speyside",
        "country": "Scotland",
        "status": "opened",
    },
    {
        "name": "Buffalo Trace",
        "distillery_name": "Buffalo Trace",
        "region": "Kentucky",
        "country": "USA",
        "status": "finished",
    },
]


@pytest.mark.asyncio
class TestCollectionContracts:
    async def _setup_bottles(
        self, client: AsyncClient, headers: dict[str, str]
    ) -> None:
        for b in BOTTLES:
            await client.post("/api/v1/bottles", json=b, headers=headers)

    async def test_search_by_name(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        await self._setup_bottles(client, auth_headers)
        response = await client.get(
            "/api/v1/bottles?search=lagavulin", headers=auth_headers
        )
        assert response.status_code == 200
        items = response.json()["items"]
        assert len(items) >= 1
        assert items[0]["name"] == "Lagavulin 16"

    async def test_filter_by_region(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        await self._setup_bottles(client, auth_headers)
        response = await client.get(
            "/api/v1/bottles?region=Islay", headers=auth_headers
        )
        assert response.status_code == 200
        items = response.json()["items"]
        assert all(i["region"] == "Islay" for i in items)

    async def test_filter_by_status(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        await self._setup_bottles(client, auth_headers)
        response = await client.get(
            "/api/v1/bottles?status=opened", headers=auth_headers
        )
        assert response.status_code == 200
        items = response.json()["items"]
        assert all(i["status"] == "opened" for i in items)

    async def test_sort_by_name(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        await self._setup_bottles(client, auth_headers)
        response = await client.get(
            "/api/v1/bottles?sort=name&order=asc", headers=auth_headers
        )
        assert response.status_code == 200
        items = response.json()["items"]
        names = [i["name"] for i in items]
        assert names == sorted(names)

    async def test_pagination(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        await self._setup_bottles(client, auth_headers)
        response = await client.get(
            "/api/v1/bottles?limit=2", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["has_more"] is True
        assert data["next_cursor"] is not None
