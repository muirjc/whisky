"""WishlistItem SQLAlchemy model."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from src.models.reference_whisky import ReferenceWhisky


class WishlistItem(Base, TimestampMixin):
    """A reference whisky the user wants to acquire."""

    __tablename__ = "wishlist_items"

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
    reference_whisky_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("reference_whiskies.id"),
        nullable=False,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    reference_whisky: Mapped["ReferenceWhisky"] = relationship(
        "ReferenceWhisky",
        lazy="joined",
    )

    __table_args__ = (
        UniqueConstraint("user_id", "reference_whisky_id", name="uq_wishlist_user_whisky"),
    )

    def __repr__(self) -> str:
        return f"<WishlistItem(id={self.id}, user_id={self.user_id})>"
