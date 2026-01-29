"""Distillery API routes (read-only reference data)."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.pagination import PaginatedResponse, decode_cursor, encode_cursor
from src.db import get_db
from src.schemas.distillery import DistilleryDetail, DistilleryListItem
from src.schemas.reference_whisky import ReferenceWhiskyResponse
from src.services.distillery import get_distillery_by_slug, list_distilleries
from src.services.reference_whisky import list_whiskies

router = APIRouter()


@router.get("", response_model=PaginatedResponse[DistilleryListItem])
async def list_distilleries_endpoint(
    db: AsyncSession = Depends(get_db),
    search: str | None = Query(None),
    region: str | None = Query(None),
    country: str | None = Query(None),
    cursor: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
) -> PaginatedResponse[DistilleryListItem]:
    """List distilleries with optional search and filter."""
    items, has_more = await list_distilleries(
        db, search=search, region=region, country=country, cursor=cursor, limit=limit
    )
    responses = [DistilleryListItem.model_validate(d) for d in items]
    next_cursor = None
    if has_more:
        current_offset = 0
        if cursor:
            current_offset = int(decode_cursor(cursor).get("offset", 0))
        next_cursor = encode_cursor({"offset": current_offset + limit})
    return PaginatedResponse(items=responses, next_cursor=next_cursor, has_more=has_more)


@router.get("/{slug}", response_model=DistilleryDetail)
async def get_distillery_endpoint(
    slug: str,
    db: AsyncSession = Depends(get_db),
) -> DistilleryDetail:
    """Get a distillery by slug."""
    distillery = await get_distillery_by_slug(db, slug)
    if not distillery:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Distillery not found")
    return DistilleryDetail.model_validate(distillery)


@router.get("/{slug}/whiskies", response_model=PaginatedResponse[ReferenceWhiskyResponse])
async def get_distillery_whiskies_endpoint(
    slug: str,
    db: AsyncSession = Depends(get_db),
    cursor: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
) -> PaginatedResponse[ReferenceWhiskyResponse]:
    """List whiskies from a specific distillery."""
    items, has_more = await list_whiskies(
        db, distillery_slug=slug, cursor=cursor, limit=limit
    )
    responses = [ReferenceWhiskyResponse.model_validate(w) for w in items]
    next_cursor = None
    if has_more:
        current_offset = 0
        if cursor:
            current_offset = int(decode_cursor(cursor).get("offset", 0))
        next_cursor = encode_cursor({"offset": current_offset + limit})
    return PaginatedResponse(items=responses, next_cursor=next_cursor, has_more=has_more)
