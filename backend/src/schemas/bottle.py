"""Bottle Pydantic schemas for request/response validation."""

import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from src.schemas.enums import BottleStatus
from src.schemas.flavor_profile import FlavorProfile


class BottleCreate(BaseModel):
    """Request schema for creating a bottle."""

    name: str = Field(max_length=255)
    distillery_name: str = Field(max_length=255)
    age_statement: int | None = Field(None, ge=0)
    region: str = Field(max_length=100)
    country: str = Field(max_length=100)
    size_ml: int | None = Field(None, gt=0)
    abv: Decimal | None = Field(None, ge=0, le=100)
    flavor_profile: FlavorProfile | None = None
    tasting_notes: str | None = None
    rating: int | None = Field(None, ge=1, le=5)
    status: BottleStatus = BottleStatus.SEALED
    purchase_price: Decimal | None = None
    purchase_date: date | None = None
    purchase_location: str | None = Field(None, max_length=255)


class BottleUpdate(BaseModel):
    """Request schema for updating a bottle (all fields optional)."""

    name: str | None = Field(None, max_length=255)
    distillery_name: str | None = Field(None, max_length=255)
    age_statement: int | None = Field(None, ge=0)
    region: str | None = Field(None, max_length=100)
    country: str | None = Field(None, max_length=100)
    size_ml: int | None = Field(None, gt=0)
    abv: Decimal | None = Field(None, ge=0, le=100)
    flavor_profile: FlavorProfile | None = None
    tasting_notes: str | None = None
    rating: int | None = Field(None, ge=1, le=5)
    status: BottleStatus | None = None
    purchase_price: Decimal | None = None
    purchase_date: date | None = None
    purchase_location: str | None = Field(None, max_length=255)


class DistillerySummary(BaseModel):
    """Summary distillery info embedded in bottle response."""

    id: uuid.UUID
    slug: str
    name: str
    region: str
    country: str

    class Config:
        from_attributes = True


class BottleResponse(BaseModel):
    """Response schema for a bottle."""

    id: uuid.UUID
    name: str
    distillery_name: str
    distillery: DistillerySummary | None = None
    age_statement: int | None = None
    region: str
    country: str
    size_ml: int | None = None
    abv: Decimal | None = None
    flavor_profile: dict[str, int] | None = None
    tasting_notes: str | None = None
    rating: int | None = None
    status: str
    purchase_price: Decimal | None = None
    purchase_date: date | None = None
    purchase_location: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
