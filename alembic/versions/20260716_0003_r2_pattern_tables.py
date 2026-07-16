"""R2 schema: pattern_detected and pattern_confirmation.

Revision ID: 20260716_0003
Revises: 20260716_0002
Create Date: 2026-07-16
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260716_0003"
down_revision: str | None = "20260716_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "pattern_detected",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("anchor_candle_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("start_candle_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("pattern_length", sa.Integer(), nullable=False),
        sa.Column("pattern_type", sa.String(length=64), nullable=False),
        sa.Column("signal", sa.String(length=16), nullable=False),
        sa.Column("trend_context", sa.String(length=16), nullable=False, server_default="UNKNOWN"),
        sa.Column("detector_version", sa.String(length=32), nullable=False),
        sa.Column("parameters_hash", sa.String(length=64), nullable=False),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "confirmation_status", sa.String(length=32), nullable=False, server_default="PENDING"
        ),
        sa.Column("confirmation_candle_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("confirmation_rule_version", sa.String(length=64), nullable=True),
        sa.Column("context_features", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("run_id", sa.String(length=64), nullable=False),
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
        sa.ForeignKeyConstraint(["anchor_candle_id"], ["candle.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["start_candle_id"], ["candle.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["confirmation_candle_id"], ["candle.id"], ondelete="SET NULL"),
        sa.UniqueConstraint(
            "anchor_candle_id",
            "pattern_type",
            "detector_version",
            "parameters_hash",
            name="uq_pattern_detected_logical",
        ),
    )
    op.create_index("ix_pattern_detected_type", "pattern_detected", ["pattern_type"])
    op.create_index("ix_pattern_detected_run", "pattern_detected", ["run_id"])

    op.create_table(
        "pattern_confirmation",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("pattern_detected_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("confirmation_rule_version", sa.String(length=64), nullable=False),
        sa.Column("confirmation_status", sa.String(length=32), nullable=False),
        sa.Column("confirmation_candle_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["pattern_detected_id"], ["pattern_detected.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["confirmation_candle_id"], ["candle.id"], ondelete="SET NULL"),
        sa.UniqueConstraint(
            "pattern_detected_id",
            "confirmation_rule_version",
            name="uq_pattern_confirmation_logical",
        ),
    )


def downgrade() -> None:
    op.drop_table("pattern_confirmation")
    op.drop_index("ix_pattern_detected_run", table_name="pattern_detected")
    op.drop_index("ix_pattern_detected_type", table_name="pattern_detected")
    op.drop_table("pattern_detected")
