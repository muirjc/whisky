"""Bottle SQLAlchemy model for user's collection."""

import uuid
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from src.models.distillery import Distillery
    from src.models.user import User


class Bottle(Base, TimestampMixin):
    """An individual whisky in the user's collection."""

    __tablename__ = "bottles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    distillery_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    distillery_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("distilleries.id"),
        nullable=True,
    )
    age_statement: Mapped[int | None] = mapped_column(Integer, nullable=True)
    region: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    size_ml: Mapped[int | None] = mapped_column(Integer, nullable=True)
    abv: Mapped[Decimal | None] = mapped_column(Numeric(4, 1), nullable=True)
    flavor_profile: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    tasting_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="sealed",
        server_default="sealed",
        index=True,
    )
    purchase_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    purchase_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    purchase_location: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    distillery: Mapped["Distillery | None"] = relationship(
        "Distillery",
        lazy="joined",
    )

    __table_args__ = (
        Index("idx_bottle_created", "created_at"),
        CheckConstraint("age_statement >= 0", name="ck_bottle_age_positive"),
        CheckConstraint("size_ml > 0", name="ck_bottle_size_positive"),
        CheckConstraint("abv >= 0 AND abv <= 100", name="ck_bottle_abv_range"),
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_bottle_rating_range"),
    )

    def __repr__(self) -> str:
        return f"<Bottle(id={self.id}, name='{self.name}')>"
