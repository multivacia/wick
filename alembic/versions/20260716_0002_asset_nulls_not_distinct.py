"""Enforce NULLS NOT DISTINCT on asset uniqueness.

Revision ID: 20260716_0002
Revises: 20260715_0001
Create Date: 2026-07-16
"""

from collections.abc import Sequence

from alembic import op

revision: str = "20260716_0002"
down_revision: str | None = "20260715_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint("uq_asset_symbol_source_exchange", "asset", type_="unique")
    op.create_unique_constraint(
        "uq_asset_symbol_source_exchange",
        "asset",
        ["symbol", "source", "exchange"],
        postgresql_nulls_not_distinct=True,
    )


def downgrade() -> None:
    op.drop_constraint("uq_asset_symbol_source_exchange", "asset", type_="unique")
    op.create_unique_constraint(
        "uq_asset_symbol_source_exchange",
        "asset",
        ["symbol", "source", "exchange"],
    )
