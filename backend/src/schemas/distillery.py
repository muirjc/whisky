"""Distillery Pydantic schemas."""

import uuid
from decimal import Decimal

from pydantic import BaseModel


class DistilleryListItem(BaseModel):
    """Summary distillery for list views."""

    id: uuid.UUID
    slug: str
    name: str
    region: str
    country: str

    class Config:
        from_attributes = True


class DistilleryDetail(DistilleryListItem):
    """Full distillery detail."""

    latitude: Decimal | None = None
    longitude: Decimal | None = None
    founded: int | None = None
    owner: str | None = None
    history: str | None = None
    production_notes: str | None = None
    website: str | None = None
