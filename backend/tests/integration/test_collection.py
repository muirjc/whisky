"""Integration tests for collection management."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestCollectionManagement:
    async def _create_bottles(
        self, client: AsyncClient, headers: dict[str, str]
    ) -> list[str]:
        bottles = [
            {"name": "Lagavulin 16", "distillery_name": "Lagavulin", "region": "Islay", "country": "Scotland", "rating": 5},
            {"name": "Macallan 12", "distillery_name": "Macallan", "region": "Speyside", "country": "Scotland", "rating": 4},
            {"name": "Talisker 10", "distillery_name": "Talisker", "region": "Islands", "country": "Scotland", "rating": 4},
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
