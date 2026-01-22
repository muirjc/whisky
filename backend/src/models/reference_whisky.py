"""ReferenceWhisky SQLAlchemy model for pre-seeded whisky data."""

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.distillery import Distillery


class ReferenceWhisky(Base):
    """Pre-seeded whisky from the reference database (read-only)."""

    __tablename__ = "reference_whiskies"

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
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    distillery_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("distilleries.id"),
        nullable=False,
        index=True,
    )
    age_statement: Mapped[int | None] = mapped_column(Integer, nullable=True)
    region: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    flavor_profile: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    distillery: Mapped["Distillery"] = relationship(
        "Distillery",
        back_populates="whiskies",
        lazy="joined",
    )

    __table_args__ = (
        Index("idx_ref_whisky_flavor_gin", "flavor_profile", postgresql_using="gin"),
    )

    def __repr__(self) -> str:
        return f"<ReferenceWhisky(id={self.id}, name='{self.name}')>"
