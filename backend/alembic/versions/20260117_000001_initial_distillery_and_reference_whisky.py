"""Initial distillery and reference whisky tables.

Revision ID: 001
Revises:
Create Date: 2026-01-17
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "distilleries",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("region", sa.String(100), nullable=False),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("latitude", sa.Numeric(9, 6), nullable=True),
        sa.Column("longitude", sa.Numeric(9, 6), nullable=True),
        sa.Column("founded", sa.Integer(), nullable=True),
        sa.Column("owner", sa.String(255), nullable=True),
        sa.Column("history", sa.Text(), nullable=True),
        sa.Column("production_notes", sa.Text(), nullable=True),
        sa.Column("website", sa.String(500), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index("idx_distillery_name", "distilleries", ["name"])
    op.create_index("idx_distillery_region", "distilleries", ["region"])
    op.create_index("idx_distillery_country", "distilleries", ["country"])

    op.create_table(
        "reference_whiskies",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column(
            "distillery_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("distilleries.id"),
            nullable=False,
        ),
        sa.Column("age_statement", sa.Integer(), nullable=True),
        sa.Column("region", sa.String(100), nullable=False),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("flavor_profile", postgresql.JSONB(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index("idx_ref_whisky_name", "reference_whiskies", ["name"])
    op.create_index("idx_ref_whisky_distillery", "reference_whiskies", ["distillery_id"])
    op.create_index("idx_ref_whisky_region", "reference_whiskies", ["region"])
    op.create_index(
        "idx_ref_whisky_flavor_gin",
        "reference_whiskies",
        ["flavor_profile"],
        postgresql_using="gin",
    )


def downgrade() -> None:
    op.drop_table("reference_whiskies")
    op.drop_table("distilleries")
