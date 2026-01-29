"""Bottle collection API routes."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user_id
from src.api.pagination import PaginatedResponse, encode_cursor
from src.db import get_db
from src.schemas.bottle import BottleCreate, BottleResponse, BottleUpdate
from src.services.bottle import (
    create_bottle,
    delete_bottle,
    get_bottle,
    list_bottles,
    update_bottle,
)

router = APIRouter()


@router.post("", response_model=BottleResponse, status_code=status.HTTP_201_CREATED)
async def create_bottle_endpoint(
    data: BottleCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> BottleResponse:
    """Add a new bottle to the collection."""
    bottle = await create_bottle(db, user_id, data)
    return BottleResponse.model_validate(bottle)


@router.get("/{bottle_id}", response_model=BottleResponse)
async def get_bottle_endpoint(
    bottle_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> BottleResponse:
    """Get a bottle by ID."""
    bottle = await get_bottle(db, bottle_id, user_id)
    if not bottle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bottle not found")
    return BottleResponse.model_validate(bottle)


@router.put("/{bottle_id}", response_model=BottleResponse)
async def update_bottle_endpoint(
    bottle_id: uuid.UUID,
    data: BottleUpdate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> BottleResponse:
    """Update a bottle."""
    bottle = await get_bottle(db, bottle_id, user_id)
    if not bottle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bottle not found")
    updated = await update_bottle(db, bottle, data)
    return BottleResponse.model_validate(updated)


@router.delete("/{bottle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bottle_endpoint(
    bottle_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a bottle from the collection."""
    bottle = await get_bottle(db, bottle_id, user_id)
    if not bottle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bottle not found")
    await delete_bottle(db, bottle)


@router.get("", response_model=PaginatedResponse[BottleResponse])
async def list_bottles_endpoint(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
    search: str | None = Query(None, description="Search by name or distillery"),
    region: str | None = Query(None, description="Filter by region"),
    bottle_status: str | None = Query(None, alias="status", description="Filter by status"),
    sort: str = Query("created_at", description="Sort field"),
    order: str = Query("desc", description="Sort order"),
    cursor: str | None = Query(None, description="Pagination cursor"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
) -> PaginatedResponse[BottleResponse]:
    """List bottles with search, filter, sort, and pagination."""
    bottles, has_more = await list_bottles(
        db,
        user_id,
        search=search,
        region=region,
        status=bottle_status,
        sort=sort,
        order=order,
        cursor=cursor,
        limit=limit,
    )

    items = [BottleResponse.model_validate(b) for b in bottles]
    next_cursor = None
    if has_more and bottles:
        # Compute offset for next page
        from src.api.pagination import decode_cursor

        current_offset = 0
        if cursor:
            cursor_data = decode_cursor(cursor)
            current_offset = int(cursor_data.get("offset", 0))
        next_cursor = encode_cursor({"offset": current_offset + limit})

    return PaginatedResponse(items=items, next_cursor=next_cursor, has_more=has_more)


@router.get("/{bottle_id}/similar")
async def get_similar_whiskies_endpoint(
    bottle_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(10, ge=1, le=50),
) -> dict[str, list[dict[str, object]]]:
    """Get whiskies similar to a bottle's flavor profile."""
    from src.schemas.reference_whisky import ReferenceWhiskyResponse, SimilarWhiskyResponse
    from src.services.matching import find_similar_whiskies

    bottle = await get_bottle(db, bottle_id, user_id)
    if not bottle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bottle not found")
    if not bottle.flavor_profile or not any(bottle.flavor_profile.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bottle has no flavor profile",
        )

    similar = await find_similar_whiskies(db, bottle.flavor_profile, limit=limit)
    items = [
        {
            "whisky": ReferenceWhiskyResponse.model_validate(whisky),
            "similarity_score": round(score, 3),
        }
        for whisky, score in similar
    ]
    return {"items": items}
