"""Add bottles table.

Revision ID: 003
Revises: 002
Create Date: 2026-01-17
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bottles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("distillery_name", sa.String(255), nullable=False),
        sa.Column(
            "distillery_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("distilleries.id"),
            nullable=True,
        ),
        sa.Column("age_statement", sa.Integer(), nullable=True),
        sa.Column("region", sa.String(100), nullable=False),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("size_ml", sa.Integer(), nullable=True),
        sa.Column("abv", sa.Numeric(4, 1), nullable=True),
        sa.Column("flavor_profile", postgresql.JSONB(), nullable=True),
        sa.Column("tasting_notes", sa.Text(), nullable=True),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column(
            "status",
            sa.String(20),
            nullable=False,
            server_default="sealed",
        ),
        sa.Column("purchase_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("purchase_date", sa.Date(), nullable=True),
        sa.Column("purchase_location", sa.String(255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("age_statement >= 0", name="ck_bottle_age_positive"),
        sa.CheckConstraint("size_ml > 0", name="ck_bottle_size_positive"),
        sa.CheckConstraint("abv >= 0 AND abv <= 100", name="ck_bottle_abv_range"),
        sa.CheckConstraint("rating >= 1 AND rating <= 5", name="ck_bottle_rating_range"),
    )
    op.create_index("idx_bottle_user_id", "bottles", ["user_id"])
    op.create_index("idx_bottle_distillery", "bottles", ["distillery_name"])
    op.create_index("idx_bottle_region", "bottles", ["region"])
    op.create_index("idx_bottle_status", "bottles", ["status"])
    op.create_index("idx_bottle_created", "bottles", ["created_at"])


def downgrade() -> None:
    op.drop_table("bottles")
