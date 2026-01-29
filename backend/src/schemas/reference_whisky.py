"""Reference whisky Pydantic schemas."""

import uuid

from pydantic import BaseModel

from src.schemas.distillery import DistilleryListItem


class ReferenceWhiskyResponse(BaseModel):
    """Reference whisky response."""

    id: uuid.UUID
    slug: str
    name: str
    distillery: DistilleryListItem | None = None
    age_statement: int | None = None
    region: str
    country: str
    flavor_profile: dict[str, int]
    description: str | None = None

    class Config:
        from_attributes = True


class SimilarWhiskyResponse(BaseModel):
    """A similar whisky with its similarity score."""

    whisky: ReferenceWhiskyResponse
    similarity_score: float
