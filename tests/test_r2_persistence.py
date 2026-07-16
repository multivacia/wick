"""R2 persistence / confirmation / idempotency against PostgreSQL."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, select

from wick.db.models import Asset, Candle, PatternConfirmation, PatternDetected
from wick.detection.service import DetectionService


def _seed_candles(session, n: int = 30):
    asset = Asset(
        symbol="R2TEST/USDT",
        asset_type="crypto",
        source="binance",
        exchange="binance",
        currency="USDT",
        timezone="UTC",
    )
    session.add(asset)
    session.flush()
    base = datetime(2024, 1, 1, tzinfo=UTC)
    candles = []
    for i in range(n):
        # mostly trending with a hammer-like bar near the end
        o = Decimal(100 + i)
        c = Decimal(100 + i + 1)
        h = c + Decimal("0.5")
        low = o - Decimal("0.5")
        if i == n - 2:
            # hammer shape
            o = Decimal("110")
            c = Decimal("110.5")
            h = Decimal("110.6")
            low = Decimal("108")
        candle = Candle(
            asset_id=asset.id,
            timeframe="1d",
            timestamp=base + timedelta(days=i),
            open=o,
            high=h,
            low=low,
            close=c,
            volume=Decimal("1000"),
            source="binance",
            is_closed=True,
            data_revision=1,
        )
        session.add(candle)
        candles.append(candle)
    session.flush()
    return asset, candles


def test_detection_persist_idempotent(session, settings):
    asset, _ = _seed_candles(session)
    svc = DetectionService(session, dry_run=False, safety_delay_seconds=0)
    svc.detect_asset_timeframe(asset_id=asset.id, timeframe="1d", incremental=False)
    count1 = session.execute(select(func.count()).select_from(PatternDetected)).scalar_one()
    s2 = svc.detect_asset_timeframe(
        asset_id=asset.id, timeframe="1d", incremental=False, reprocess=True
    )
    count2 = session.execute(select(func.count()).select_from(PatternDetected)).scalar_one()
    assert count1 == count2
    assert s2.patterns_inserted == 0
    assert count1 >= 1
    # confirmations exist for non-doji when t+1 available
    confs = session.execute(select(func.count()).select_from(PatternConfirmation)).scalar_one()
    assert confs >= 1


def test_dry_run_does_not_persist(session, settings):
    asset, _ = _seed_candles(session, n=25)
    svc = DetectionService(session, dry_run=True, safety_delay_seconds=0)
    summary = svc.detect_asset_timeframe(asset_id=asset.id, timeframe="1d", incremental=False)
    assert summary.dry_run
    assert session.execute(select(func.count()).select_from(PatternDetected)).scalar_one() == 0


def test_open_candle_excluded(session, settings):
    asset = Asset(
        symbol="OPEN/USDT",
        asset_type="crypto",
        source="binance",
        exchange="binance",
        currency="USDT",
        timezone="UTC",
    )
    session.add(asset)
    session.flush()
    now = datetime.now(UTC)
    # closed old candle
    session.add(
        Candle(
            asset_id=asset.id,
            timeframe="1h",
            timestamp=now - timedelta(hours=5),
            open=Decimal("1"),
            high=Decimal("2"),
            low=Decimal("0.5"),
            close=Decimal("1.5"),
            volume=Decimal("10"),
            source="binance",
            is_closed=True,
            data_revision=1,
        )
    )
    # currently open-ish candle (timestamp now)
    session.add(
        Candle(
            asset_id=asset.id,
            timeframe="1h",
            timestamp=now.replace(minute=0, second=0, microsecond=0),
            open=Decimal("1"),
            high=Decimal("2"),
            low=Decimal("0.5"),
            close=Decimal("1.5"),
            volume=Decimal("10"),
            source="binance",
            is_closed=True,  # even if flagged closed, time formula rejects
            data_revision=1,
        )
    )
    session.flush()
    from wick.detection.service import load_closed_candles

    closed = load_closed_candles(
        session, asset_id=asset.id, timeframe="1h", safety_delay_seconds=30, now_utc=now
    )
    assert len(closed) == 1
