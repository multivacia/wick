"""ORM models for R1 entities."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wick.db.base import Base


def _uuid() -> uuid.UUID:
    return uuid.uuid4()


class Asset(Base):
    __tablename__ = "asset"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    symbol: Mapped[str] = mapped_column(String(64), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(16), nullable=False)  # crypto|stock
    source: Mapped[str] = mapped_column(String(32), nullable=False)
    exchange: Mapped[str | None] = mapped_column(String(64), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(16), nullable=True)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="UTC")
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    candles: Mapped[list[Candle]] = relationship(back_populates="asset")

    __table_args__ = (
        UniqueConstraint("symbol", "source", "exchange", name="uq_asset_symbol_source_exchange"),
        Index("ix_asset_symbol", "symbol"),
    )


class Candle(Base):
    __tablename__ = "candle"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("asset.id", ondelete="CASCADE"), nullable=False
    )
    timeframe: Mapped[str] = mapped_column(String(8), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    open: Mapped[Decimal] = mapped_column(Numeric(36, 18), nullable=False)
    high: Mapped[Decimal] = mapped_column(Numeric(36, 18), nullable=False)
    low: Mapped[Decimal] = mapped_column(Numeric(36, 18), nullable=False)
    close: Mapped[Decimal] = mapped_column(Numeric(36, 18), nullable=False)
    volume: Mapped[Decimal] = mapped_column(Numeric(36, 18), nullable=False)
    adjusted_close: Mapped[Decimal | None] = mapped_column(Numeric(36, 18), nullable=True)
    adjustment_factor: Mapped[Decimal | None] = mapped_column(Numeric(36, 18), nullable=True)
    source: Mapped[str] = mapped_column(String(32), nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    first_ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    last_ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    source_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    data_revision: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    asset: Mapped[Asset] = relationship(back_populates="candles")

    __table_args__ = (
        UniqueConstraint("asset_id", "timeframe", "timestamp", "source", name="uq_candle_key"),
        Index("ix_candle_asset_tf_ts", "asset_id", "timeframe", "timestamp"),
    )


class IngestionRun(Base):
    __tablename__ = "ingestion_run"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    run_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    source: Mapped[str] = mapped_column(String(32), nullable=False)
    requested_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    requested_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    actual_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    actual_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    assets_requested: Mapped[list[Any]] = mapped_column(
        JSONB, nullable=False, server_default=text("'[]'::jsonb")
    )
    timeframes_requested: Mapped[list[Any]] = mapped_column(
        JSONB, nullable=False, server_default=text("'[]'::jsonb")
    )
    candles_received: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    candles_inserted: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    candles_updated: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    candles_rejected: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pages_fetched: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    retries: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="FAILED")
    error_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    coverage: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    gaps: Mapped[list[Any] | None] = mapped_column(JSONB, nullable=True)
    quality_report: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class CandleRevisionEvent(Base):
    """Audit trail when OHLCV for an existing key is revised by the source."""

    __tablename__ = "candle_revision_event"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=_uuid)
    candle_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candle.id", ondelete="CASCADE"), nullable=False
    )
    run_id: Mapped[str] = mapped_column(String(64), nullable=False)
    previous_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    new_revision: Mapped[int] = mapped_column(Integer, nullable=False)
    previous_ohlcv: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    new_ohlcv: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
