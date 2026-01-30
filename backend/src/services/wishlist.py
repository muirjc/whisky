"""Wishlist service."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.wishlist import WishlistItem


async def add_to_wishlist(
    session: AsyncSession,
    user_id: uuid.UUID,
    reference_whisky_id: uuid.UUID,
    notes: str | None = None,
) -> WishlistItem:
    """Add a reference whisky to the user's wishlist."""
    item = WishlistItem(
        user_id=user_id,
        reference_whisky_id=reference_whisky_id,
        notes=notes,
    )
    session.add(item)
    await session.flush()
    await session.refresh(item)
    return item


async def get_wishlist_item(
    session: AsyncSession,
    item_id: uuid.UUID,
    user_id: uuid.UUID,
) -> WishlistItem | None:
    """Get a wishlist item by ID, filtered by user."""
    result = await session.execute(
        select(WishlistItem).where(
            WishlistItem.id == item_id,
            WishlistItem.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def list_wishlist(
    session: AsyncSession,
    user_id: uuid.UUID,
    cursor: str | None = None,
    limit: int = 20,
) -> tuple[list[WishlistItem], bool]:
    """List wishlist items for a user."""
    query = (
        select(WishlistItem)
        .where(WishlistItem.user_id == user_id)
        .order_by(WishlistItem.created_at.desc())
        .limit(limit + 1)
    )

    if cursor:
        from src.api.pagination import decode_cursor

        cursor_data = decode_cursor(cursor)
        offset = int(cursor_data.get("offset", 0))
        query = query.offset(offset)

    result = await session.execute(query)
    items = list(result.scalars().all())

    has_more = len(items) > limit
    if has_more:
        items = items[:limit]

    return items, has_more


async def remove_from_wishlist(
    session: AsyncSession,
    item: WishlistItem,
) -> None:
    """Remove an item from the wishlist."""
    await session.delete(item)
    await session.flush()


async def check_duplicate(
    session: AsyncSession,
    user_id: uuid.UUID,
    reference_whisky_id: uuid.UUID,
) -> bool:
    """Check if a whisky is already in the user's wishlist."""
    result = await session.execute(
        select(WishlistItem.id).where(
            WishlistItem.user_id == user_id,
            WishlistItem.reference_whisky_id == reference_whisky_id,
        )
    )
    return result.scalar_one_or_none() is not None
