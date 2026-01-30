"""Bottle service for collection management."""

import uuid
from typing import Any

from sqlalchemy import Select, asc, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.bottle import Bottle
from src.models.distillery import Distillery
from src.schemas.bottle import BottleCreate, BottleUpdate


async def create_bottle(
    session: AsyncSession,
    user_id: uuid.UUID,
    data: BottleCreate,
) -> Bottle:
    """Create a new bottle in the user's collection."""
    bottle = Bottle(
        user_id=user_id,
        name=data.name,
        distillery_name=data.distillery_name,
        age_statement=data.age_statement,
        region=data.region,
        country=data.country,
        size_ml=data.size_ml,
        abv=data.abv,
        flavor_profile=data.flavor_profile.to_dict() if data.flavor_profile else None,
        tasting_notes=data.tasting_notes,
        rating=data.rating,
        status=data.status.value,
        purchase_price=data.purchase_price,
        purchase_date=data.purchase_date,
        purchase_location=data.purchase_location,
    )

    # Try to link to reference distillery
    bottle.distillery_id = await _find_distillery_id(session, data.distillery_name)

    session.add(bottle)
    await session.flush()
    await session.refresh(bottle)
    return bottle


async def get_bottle(
    session: AsyncSession,
    bottle_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Bottle | None:
    """Get a bottle by ID, filtered by user ownership."""
    result = await session.execute(
        select(Bottle).where(Bottle.id == bottle_id, Bottle.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def update_bottle(
    session: AsyncSession,
    bottle: Bottle,
    data: BottleUpdate,
) -> Bottle:
    """Update a bottle with provided fields."""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "flavor_profile" and value is not None:
            value = value.to_dict() if hasattr(value, "to_dict") else value
        if field == "status" and value is not None:
            value = value.value if hasattr(value, "value") else value
        setattr(bottle, field, value)

    # Re-link distillery if name changed
    if "distillery_name" in update_data:
        bottle.distillery_id = await _find_distillery_id(
            session, bottle.distillery_name
        )

    await session.flush()
    await session.refresh(bottle)
    return bottle


async def delete_bottle(
    session: AsyncSession,
    bottle: Bottle,
) -> None:
    """Delete a bottle."""
    await session.delete(bottle)
    await session.flush()


async def list_bottles(
    session: AsyncSession,
    user_id: uuid.UUID,
    search: str | None = None,
    region: str | None = None,
    status: str | None = None,
    sort: str = "created_at",
    order: str = "desc",
    cursor: str | None = None,
    limit: int = 20,
) -> tuple[list[Bottle], bool]:
    """List bottles with search, filter, sort, and pagination.

    Returns (bottles, has_more).
    """
    query: Select[tuple[Bottle]] = select(Bottle).where(Bottle.user_id == user_id)

    # Search
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Bottle.name.ilike(search_term),
                Bottle.distillery_name.ilike(search_term),
                Bottle.region.ilike(search_term),
            )
        )

    # Filters
    if region:
        query = query.where(Bottle.region == region)
    if status:
        query = query.where(Bottle.status == status)

    # Sort
    sort_column = _get_sort_column(sort)
    order_func = desc if order == "desc" else asc
    query = query.order_by(order_func(sort_column), desc(Bottle.id))

    # Cursor-based pagination using offset approach for simplicity
    if cursor:
        from src.api.pagination import decode_cursor

        cursor_data = decode_cursor(cursor)
        offset = int(cursor_data.get("offset", 0))
        query = query.offset(offset)

    # Fetch limit + 1 to check for more
    query = query.limit(limit + 1)
    result = await session.execute(query)
    bottles = list(result.scalars().all())

    has_more = len(bottles) > limit
    if has_more:
        bottles = bottles[:limit]

    return bottles, has_more


def _get_sort_column(sort: str) -> Any:
    """Map sort parameter to column."""
    mapping: dict[str, Any] = {
        "name": Bottle.name,
        "distillery": Bottle.distillery_name,
        "age": Bottle.age_statement,
        "created_at": Bottle.created_at,
        "rating": Bottle.rating,
    }
    return mapping.get(sort, Bottle.created_at)


async def _find_distillery_id(
    session: AsyncSession, distillery_name: str
) -> uuid.UUID | None:
    """Try to match a distillery name to a reference distillery."""
    result = await session.execute(
        select(Distillery.id).where(
            func.lower(Distillery.name) == func.lower(distillery_name)
        )
    )
    row = result.one_or_none()
    return row[0] if row else None
