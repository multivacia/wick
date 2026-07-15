"""Upsert idempotency and revision audit tests."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, select

from wick.db.models import Candle, CandleRevisionEvent
from wick.ingestion.upsert import get_or_create_asset, upsert_candles
from wick.ingestion.validators import RawCandle


def _candles(n: int = 3) -> list[RawCandle]:
    base = datetime(2024, 1, 1, tzinfo=UTC)
    return [
        RawCandle(
            timestamp=base + timedelta(days=i),
            open=Decimal("100"),
            high=Decimal("110"),
            low=Decimal("90"),
            close=Decimal(str(100 + i)),
            volume=Decimal("1000"),
        )
        for i in range(n)
    ]


def test_rerun_does_not_duplicate(session):
    asset = get_or_create_asset(
        session,
        symbol="BTC/USDT",
        asset_type="crypto",
        source="binance",
        exchange="binance",
        currency="USDT",
    )
    first = upsert_candles(
        session,
        asset=asset,
        timeframe="1d",
        source="binance",
        candles=_candles(),
        run_id="run1",
    )
    assert first.inserted == 3
    second = upsert_candles(
        session,
        asset=asset,
        timeframe="1d",
        source="binance",
        candles=_candles(),
        run_id="run2",
    )
    assert second.inserted == 0
    assert second.unchanged == 3
    count = session.execute(select(func.count()).select_from(Candle)).scalar_one()
    assert count == 3


def test_revision_increments_and_is_audited(session):
    asset = get_or_create_asset(
        session,
        symbol="ETH/USDT",
        asset_type="crypto",
        source="binance",
        exchange="binance",
        currency="USDT",
    )
    original = _candles(1)
    upsert_candles(
        session,
        asset=asset,
        timeframe="1d",
        source="binance",
        candles=original,
        run_id="run_a",
    )
    revised = [
        RawCandle(
            timestamp=original[0].timestamp,
            open=Decimal("100"),
            high=Decimal("120"),
            low=Decimal("90"),
            close=Decimal("115"),
            volume=Decimal("2000"),
        )
    ]
    stats = upsert_candles(
        session,
        asset=asset,
        timeframe="1d",
        source="binance",
        candles=revised,
        run_id="run_b",
    )
    assert stats.updated == 1
    candle = session.execute(select(Candle)).scalar_one()
    assert candle.data_revision == 2
    assert candle.close == Decimal("115")
    assert candle.first_ingested_at <= candle.last_ingested_at
    events = session.execute(select(CandleRevisionEvent)).scalars().all()
    assert len(events) == 1
    assert events[0].previous_revision == 1
    assert events[0].new_revision == 2
    assert events[0].run_id == "run_b"
