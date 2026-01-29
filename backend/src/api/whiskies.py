"""Reference whisky API routes (read-only)."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.pagination import PaginatedResponse, decode_cursor, encode_cursor
from src.db import get_db
from src.schemas.reference_whisky import ReferenceWhiskyResponse
from src.services.reference_whisky import get_whisky_by_slug, list_whiskies

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ReferenceWhiskyResponse])
async def search_whiskies_endpoint(
    db: AsyncSession = Depends(get_db),
    search: str | None = Query(None),
    region: str | None = Query(None),
    flavor: str | None = Query(None, description="Filter by dominant flavor"),
    cursor: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
) -> PaginatedResponse[ReferenceWhiskyResponse]:
    """Search reference whiskies."""
    items, has_more = await list_whiskies(
        db, search=search, region=region, flavor=flavor, cursor=cursor, limit=limit
    )
    responses = [ReferenceWhiskyResponse.model_validate(w) for w in items]
    next_cursor = None
    if has_more:
        current_offset = 0
        if cursor:
            current_offset = int(decode_cursor(cursor).get("offset", 0))
        next_cursor = encode_cursor({"offset": current_offset + limit})
    return PaginatedResponse(items=responses, next_cursor=next_cursor, has_more=has_more)


@router.get("/{slug}", response_model=ReferenceWhiskyResponse)
async def get_whisky_endpoint(
    slug: str,
    db: AsyncSession = Depends(get_db),
) -> ReferenceWhiskyResponse:
    """Get a reference whisky by slug."""
    whisky = await get_whisky_by_slug(db, slug)
    if not whisky:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Whisky not found")
    return ReferenceWhiskyResponse.model_validate(whisky)
