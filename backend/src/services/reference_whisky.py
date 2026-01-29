"""Reference whisky service for read-only data access."""

from typing import Any

from sqlalchemy import Select, asc, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.reference_whisky import ReferenceWhisky


async def get_whisky_by_slug(
    session: AsyncSession, slug: str
) -> ReferenceWhisky | None:
    """Get a reference whisky by slug."""
    result = await session.execute(
        select(ReferenceWhisky).where(ReferenceWhisky.slug == slug)
    )
    return result.scalar_one_or_none()


async def list_whiskies(
    session: AsyncSession,
    search: str | None = None,
    region: str | None = None,
    flavor: str | None = None,
    distillery_slug: str | None = None,
    cursor: str | None = None,
    limit: int = 20,
) -> tuple[list[ReferenceWhisky], bool]:
    """List reference whiskies with optional search and filter."""
    query: Select[tuple[ReferenceWhisky]] = select(ReferenceWhisky)

    if search:
        term = f"%{search}%"
        query = query.where(
            or_(
                ReferenceWhisky.name.ilike(term),
                ReferenceWhisky.region.ilike(term),
            )
        )
    if region:
        query = query.where(ReferenceWhisky.region == region)

    if flavor:
        # Filter by dominant flavor (value >= 3)
        from sqlalchemy import cast, Integer as SAInt
        query = query.where(
            ReferenceWhisky.flavor_profile[flavor].astext.cast(SAInt) >= 3
        )

    if distillery_slug:
        from src.models.distillery import Distillery

        query = query.join(Distillery).where(Distillery.slug == distillery_slug)

    query = query.order_by(asc(ReferenceWhisky.name))

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
