"""Distillery SQLAlchemy model for reference data."""

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Index, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.reference_whisky import ReferenceWhisky


class Distillery(Base):
    """Pre-seeded distillery information (read-only reference data)."""

    __tablename__ = "distilleries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    region: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    founded: Mapped[int | None] = mapped_column(Integer, nullable=True)
    owner: Mapped[str | None] = mapped_column(String(255), nullable=True)
    history: Mapped[str | None] = mapped_column(Text, nullable=True)
    production_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Relationships
    whiskies: Mapped[list["ReferenceWhisky"]] = relationship(
        "ReferenceWhisky",
        back_populates="distillery",
        lazy="selectin",
    )

    __table_args__ = (
        Index("idx_distillery_name", "name"),
    )

    def __repr__(self) -> str:
        return f"<Distillery(id={self.id}, name='{self.name}', region='{self.region}')>"
