"""Idempotent candle upsert with revision auditing.

Uses PostgreSQL ON CONFLICT / row locks so concurrent ingestions do not raise
IntegrityError and do not lose revisions.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from wick.db.models import Asset, Candle, CandleRevisionEvent
from wick.ingestion.validators import RawCandle, ohlcv_dict, ohlcv_equal


@dataclass
class UpsertStats:
    inserted: int = 0
    updated: int = 0
    unchanged: int = 0
    rejected: int = 0


def get_or_create_asset(
    session: Session,
    *,
    symbol: str,
    asset_type: str,
    source: str,
    exchange: str | None,
    currency: str | None,
    timezone: str = "UTC",
) -> Asset:
    """Idempotent asset create. Safe under concurrency via ON CONFLICT."""
    asset_id = uuid4()
    stmt = (
        insert(Asset)
        .values(
            id=asset_id,
            symbol=symbol,
            asset_type=asset_type,
            source=source,
            exchange=exchange,
            currency=currency,
            timezone=timezone,
            active=True,
        )
        .on_conflict_do_nothing(constraint="uq_asset_symbol_source_exchange")
        .returning(Asset.id)
    )
    inserted_id = session.execute(stmt).scalar_one_or_none()
    if inserted_id is not None:
        asset = session.get(Asset, inserted_id)
        assert asset is not None
        return asset

    existing = session.execute(
        select(Asset).where(
            Asset.symbol == symbol,
            Asset.source == source,
            Asset.exchange.is_(exchange) if exchange is None else Asset.exchange == exchange,
        )
    ).scalar_one()
    return existing


def upsert_candles(
    session: Session,
    *,
    asset: Asset,
    timeframe: str,
    source: str,
    candles: list[RawCandle],
    run_id: str,
    now: datetime | None = None,
) -> UpsertStats:
    stats = UpsertStats()
    now_utc = now or datetime.now(UTC)

    for raw in candles:
        candle_id = uuid4()
        insert_stmt = (
            insert(Candle)
            .values(
                id=candle_id,
                asset_id=asset.id,
                timeframe=timeframe,
                timestamp=raw.timestamp,
                open=raw.open,
                high=raw.high,
                low=raw.low,
                close=raw.close,
                volume=raw.volume,
                adjusted_close=raw.adjusted_close,
                adjustment_factor=raw.adjustment_factor,
                source=source,
                is_closed=True,
                first_ingested_at=now_utc,
                last_ingested_at=now_utc,
                source_updated_at=raw.source_updated_at,
                data_revision=1,
            )
            .on_conflict_do_nothing(constraint="uq_candle_key")
            .returning(Candle.id)
        )
        inserted = session.execute(insert_stmt).scalar_one_or_none()
        if inserted is not None:
            stats.inserted += 1
            continue

        existing = session.execute(
            select(Candle)
            .where(
                Candle.asset_id == asset.id,
                Candle.timeframe == timeframe,
                Candle.timestamp == raw.timestamp,
                Candle.source == source,
            )
            .with_for_update()
        ).scalar_one()

        if ohlcv_equal(existing, raw):
            existing.last_ingested_at = now_utc
            stats.unchanged += 1
            continue

        prev_rev = existing.data_revision
        prev_ohlcv = _snapshot(existing)
        existing.open = raw.open
        existing.high = raw.high
        existing.low = raw.low
        existing.close = raw.close
        existing.volume = raw.volume
        existing.adjusted_close = raw.adjusted_close
        existing.adjustment_factor = raw.adjustment_factor
        existing.last_ingested_at = now_utc
        existing.source_updated_at = raw.source_updated_at
        existing.data_revision = prev_rev + 1
        existing.updated_at = now_utc

        session.add(
            CandleRevisionEvent(
                candle_id=existing.id,
                run_id=run_id,
                previous_revision=prev_rev,
                new_revision=existing.data_revision,
                previous_ohlcv=prev_ohlcv,
                new_ohlcv=ohlcv_dict(raw),
            )
        )
        stats.updated += 1

    session.flush()
    return stats


def _snapshot(candle: Candle) -> dict[str, Any]:
    return {
        "open": str(candle.open),
        "high": str(candle.high),
        "low": str(candle.low),
        "close": str(candle.close),
        "volume": str(candle.volume),
        "adjusted_close": str(candle.adjusted_close) if candle.adjusted_close is not None else None,
        "adjustment_factor": str(candle.adjustment_factor)
        if candle.adjustment_factor is not None
        else None,
    }


def latest_candle_timestamp(
    session: Session,
    *,
    asset_id,
    timeframe: str,
    source: str,
) -> datetime | None:
    stmt = (
        select(Candle.timestamp)
        .where(
            Candle.asset_id == asset_id,
            Candle.timeframe == timeframe,
            Candle.source == source,
        )
        .order_by(Candle.timestamp.desc())
        .limit(1)
    )
    return session.execute(stmt).scalar_one_or_none()


def load_timestamps(
    session: Session,
    *,
    asset_id,
    timeframe: str,
    source: str,
) -> list[datetime]:
    stmt = (
        select(Candle.timestamp)
        .where(
            Candle.asset_id == asset_id,
            Candle.timeframe == timeframe,
            Candle.source == source,
        )
        .order_by(Candle.timestamp.asc())
    )
    return list(session.execute(stmt).scalars().all())


def decimalize(value: Decimal | float | str) -> Decimal:
    return Decimal(str(value))
