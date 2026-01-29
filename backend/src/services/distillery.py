"""Distillery service for reference data access."""

from typing import Any

from sqlalchemy import Select, asc, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.distillery import Distillery


async def get_distillery_by_slug(
    session: AsyncSession, slug: str
) -> Distillery | None:
    """Get a distillery by slug."""
    result = await session.execute(
        select(Distillery).where(Distillery.slug == slug)
    )
    return result.scalar_one_or_none()


async def list_distilleries(
    session: AsyncSession,
    search: str | None = None,
    region: str | None = None,
    country: str | None = None,
    cursor: str | None = None,
    limit: int = 20,
) -> tuple[list[Distillery], bool]:
    """List distilleries with optional search and filter."""
    query: Select[tuple[Distillery]] = select(Distillery)

    if search:
        term = f"%{search}%"
        query = query.where(
            or_(
                Distillery.name.ilike(term),
                Distillery.region.ilike(term),
            )
        )
    if region:
        query = query.where(Distillery.region == region)
    if country:
        query = query.where(Distillery.country == country)

    query = query.order_by(asc(Distillery.name))

    if cursor:
        from src.api.pagination import decode_cursor

        offset = int(decode_cursor(cursor).get("offset", 0))
        query = query.offset(offset)

    query = query.limit(limit + 1)
    result = await session.execute(query)
    items = list(result.scalars().all())

    has_more = len(items) > limit
    if has_more:
        items = items[:limit]

    return items, has_more
