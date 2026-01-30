"""Integration tests for collection management."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestCollectionManagement:
    async def _create_bottles(
        self, client: AsyncClient, headers: dict[str, str]
    ) -> list[str]:
        bottles = [
            {"name": "Lagavulin 16", "distillery_name": "Lagavulin", "region": "Islay", "country": "Scotland", "rating": 5, "status": "opened"},
            {"name": "Macallan 12", "distillery_name": "Macallan", "region": "Speyside", "country": "Scotland", "rating": 4, "status": "sealed"},
            {"name": "Talisker 10", "distillery_name": "Talisker", "region": "Islands", "country": "Scotland", "rating": 4, "status": "sealed"},
        ]
        ids = []
        for b in bottles:
            resp = await client.post("/api/v1/bottles", json=b, headers=headers)
            ids.append(resp.json()["id"])
        return ids

    async def test_search_finds_bottles(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        await self._create_bottles(client, auth_headers)
        resp = await client.get("/api/v1/bottles?search=macallan", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()["items"]) == 1

    async def test_sort_by_rating(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        await self._create_bottles(client, auth_headers)
        resp = await client.get(
            "/api/v1/bottles?sort=rating&order=desc", headers=auth_headers
        )
        items = resp.json()["items"]
        ratings = [i["rating"] for i in items if i["rating"]]
        assert ratings == sorted(ratings, reverse=True)

    async def test_filter_by_region(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        await self._create_bottles(client, auth_headers)
        resp = await client.get("/api/v1/bottles?region=Islay", headers=auth_headers)
        assert resp.status_code == 200
        items = resp.json()["items"]
        assert len(items) == 1
        assert items[0]["region"] == "Islay"

    async def test_filter_by_status(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        await self._create_bottles(client, auth_headers)
        resp = await client.get("/api/v1/bottles?status=sealed", headers=auth_headers)
        assert resp.status_code == 200
        items = resp.json()["items"]
        assert len(items) == 2

    async def test_sort_by_name_asc(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        await self._create_bottles(client, auth_headers)
        resp = await client.get(
            "/api/v1/bottles?sort=name&order=asc", headers=auth_headers
        )
        items = resp.json()["items"]
        names = [i["name"] for i in items]
        assert names == sorted(names)

    async def test_pagination(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        await self._create_bottles(client, auth_headers)
        resp = await client.get("/api/v1/bottles?limit=2", headers=auth_headers)
        data = resp.json()
        assert len(data["items"]) == 2
        assert data["has_more"] is True
        assert data["next_cursor"] is not None

        # Fetch next page
        resp2 = await client.get(
            f"/api/v1/bottles?limit=2&cursor={data['next_cursor']}",
            headers=auth_headers,
        )
        data2 = resp2.json()
        assert len(data2["items"]) == 1
        assert data2["has_more"] is False

    async def test_search_no_results(
        self, client: AsyncClient, auth_headers: dict[str, str]
    ) -> None:
        await self._create_bottles(client, auth_headers)
        resp = await client.get(
            "/api/v1/bottles?search=nonexistent", headers=auth_headers
        )
        assert resp.status_code == 200
        assert len(resp.json()["items"]) == 0
