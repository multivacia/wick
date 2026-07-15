"""Idempotent candle upsert with revision auditing."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import select
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
    stmt = select(Asset).where(
        Asset.symbol == symbol,
        Asset.source == source,
        Asset.exchange.is_(exchange) if exchange is None else Asset.exchange == exchange,
    )
    asset = session.execute(stmt).scalar_one_or_none()
    if asset is not None:
        return asset
    asset = Asset(
        symbol=symbol,
        asset_type=asset_type,
        source=source,
        exchange=exchange,
        currency=currency,
        timezone=timezone,
        active=True,
    )
    session.add(asset)
    session.flush()
    return asset


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
        stmt = select(Candle).where(
            Candle.asset_id == asset.id,
            Candle.timeframe == timeframe,
            Candle.timestamp == raw.timestamp,
            Candle.source == source,
        )
        existing = session.execute(stmt).scalar_one_or_none()
        if existing is None:
            session.add(
                Candle(
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
            )
            stats.inserted += 1
            continue

        if ohlcv_equal(existing, raw):
            existing.last_ingested_at = now_utc
            stats.unchanged += 1
            continue

        prev_rev = existing.data_revision
        prev_ohlcv = {
            "open": str(existing.open),
            "high": str(existing.high),
            "low": str(existing.low),
            "close": str(existing.close),
            "volume": str(existing.volume),
            "adjusted_close": str(existing.adjusted_close)
            if existing.adjusted_close is not None
            else None,
        }
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
