"""Wishlist API routes."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user_id
from src.api.pagination import PaginatedResponse, encode_cursor, decode_cursor
from src.db import get_db
from src.schemas.wishlist import WishlistItemCreate, WishlistItemResponse, ReferenceWhiskyResponse
from src.services.wishlist import (
    add_to_wishlist,
    check_duplicate,
    get_wishlist_item,
    list_wishlist,
    remove_from_wishlist,
)

router = APIRouter()


@router.post("", response_model=WishlistItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_wishlist_endpoint(
    data: WishlistItemCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> WishlistItemResponse:
    """Add a reference whisky to the wishlist."""
    if await check_duplicate(db, user_id, data.reference_whisky_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Whisky already in wishlist",
        )

    item = await add_to_wishlist(db, user_id, data.reference_whisky_id, data.notes)
    return _to_response(item)


@router.get("", response_model=PaginatedResponse[WishlistItemResponse])
async def list_wishlist_endpoint(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
    cursor: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
) -> PaginatedResponse[WishlistItemResponse]:
    """List wishlist items."""
    items, has_more = await list_wishlist(db, user_id, cursor=cursor, limit=limit)

    responses = [_to_response(item) for item in items]
    next_cursor = None
    if has_more:
        current_offset = 0
        if cursor:
            cursor_data = decode_cursor(cursor)
            current_offset = int(cursor_data.get("offset", 0))
        next_cursor = encode_cursor({"offset": current_offset + limit})

    return PaginatedResponse(items=responses, next_cursor=next_cursor, has_more=has_more)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_wishlist_endpoint(
    item_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Remove an item from the wishlist."""
    item = await get_wishlist_item(db, item_id, user_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    await remove_from_wishlist(db, item)


def _to_response(item: object) -> WishlistItemResponse:
    """Convert a WishlistItem to response, mapping reference_whisky to whisky."""
    from src.models.wishlist import WishlistItem as WLModel

    assert isinstance(item, WLModel)
    whisky = item.reference_whisky
    whisky_resp = ReferenceWhiskyResponse.model_validate(whisky)
    return WishlistItemResponse(
        id=item.id,
        whisky=whisky_resp,
        notes=item.notes,
        created_at=item.created_at,
    )
