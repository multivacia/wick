"""R1 initial schema: asset, candle, ingestion_run, candle_revision_event.

Revision ID: 20260715_0001
Revises:
Create Date: 2026-07-15
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260715_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "asset",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("asset_type", sa.String(length=16), nullable=False),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.Column("exchange", sa.String(length=64), nullable=True),
        sa.Column("currency", sa.String(length=16), nullable=True),
        sa.Column("timezone", sa.String(length=64), nullable=False, server_default="UTC"),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.UniqueConstraint("symbol", "source", "exchange", name="uq_asset_symbol_source_exchange"),
    )
    op.create_index("ix_asset_symbol", "asset", ["symbol"])

    op.create_table(
        "ingestion_run",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.Column("requested_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("requested_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "assets_requested",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "timeframes_requested",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("candles_received", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("candles_inserted", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("candles_updated", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("candles_rejected", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("pages_fetched", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("retries", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="FAILED"),
        sa.Column("error_summary", sa.Text(), nullable=True),
        sa.Column("coverage", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("gaps", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("quality_report", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("run_id", name="uq_ingestion_run_run_id"),
    )

    op.create_table(
        "candle",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("asset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("timeframe", sa.String(length=8), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("open", sa.Numeric(36, 18), nullable=False),
        sa.Column("high", sa.Numeric(36, 18), nullable=False),
        sa.Column("low", sa.Numeric(36, 18), nullable=False),
        sa.Column("close", sa.Numeric(36, 18), nullable=False),
        sa.Column("volume", sa.Numeric(36, 18), nullable=False),
        sa.Column("adjusted_close", sa.Numeric(36, 18), nullable=True),
        sa.Column("adjustment_factor", sa.Numeric(36, 18), nullable=True),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.Column("is_closed", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "first_ingested_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "last_ingested_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("source_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("data_revision", sa.Integer(), nullable=False, server_default="1"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["asset_id"], ["asset.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("asset_id", "timeframe", "timestamp", "source", name="uq_candle_key"),
    )
    op.create_index("ix_candle_asset_tf_ts", "candle", ["asset_id", "timeframe", "timestamp"])

    op.create_table(
        "candle_revision_event",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("candle_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("previous_revision", sa.Integer(), nullable=False),
        sa.Column("new_revision", sa.Integer(), nullable=False),
        sa.Column("previous_ohlcv", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("new_ohlcv", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["candle_id"], ["candle.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("candle_revision_event")
    op.drop_index("ix_candle_asset_tf_ts", table_name="candle")
    op.drop_table("candle")
    op.drop_table("ingestion_run")
    op.drop_index("ix_asset_symbol", table_name="asset")
    op.drop_table("asset")
