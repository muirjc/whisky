"""Wishlist Pydantic schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel

from src.schemas.bottle import DistillerySummary


class ReferenceWhiskyResponse(BaseModel):
    """Reference whisky response."""

    id: uuid.UUID
    slug: str
    name: str
    distillery: DistillerySummary | None = None
    age_statement: int | None = None
    region: str
    country: str
    flavor_profile: dict[str, int]
    description: str | None = None

    class Config:
        from_attributes = True


class WishlistItemCreate(BaseModel):
    """Request to add a whisky to wishlist."""

    reference_whisky_id: uuid.UUID
    notes: str | None = None


class WishlistItemResponse(BaseModel):
    """Wishlist item response."""

    id: uuid.UUID
    whisky: ReferenceWhiskyResponse
    notes: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
