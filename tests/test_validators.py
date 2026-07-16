"""OHLCV and closed-candle validation tests (no network)."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from wick.ingestion.validators import (
    RawCandle,
    filter_closed_candles,
    is_candle_closed,
    validate_ohlcv,
)


def test_valid_ohlcv():
    c = RawCandle(
        timestamp=datetime(2024, 1, 1, tzinfo=UTC),
        open=Decimal("100"),
        high=Decimal("110"),
        low=Decimal("90"),
        close=Decimal("105"),
        volume=Decimal("10"),
    )
    assert validate_ohlcv(c).ok


def test_reject_high_below_open_close():
    c = RawCandle(
        timestamp=datetime(2024, 1, 1, tzinfo=UTC),
        open=Decimal("100"),
        high=Decimal("99"),
        low=Decimal("90"),
        close=Decimal("105"),
        volume=Decimal("10"),
    )
    result = validate_ohlcv(c)
    assert not result.ok
    assert "high" in (result.reason or "")


def test_reject_negative_volume():
    c = RawCandle(
        timestamp=datetime(2024, 1, 1, tzinfo=UTC),
        open=Decimal("100"),
        high=Decimal("110"),
        low=Decimal("90"),
        close=Decimal("105"),
        volume=Decimal("-1"),
    )
    assert not validate_ohlcv(c).ok


def test_reject_naive_timestamp():
    c = RawCandle(
        timestamp=datetime(2024, 1, 1),
        open=Decimal("100"),
        high=Decimal("110"),
        low=Decimal("90"),
        close=Decimal("105"),
        volume=Decimal("1"),
    )
    assert not validate_ohlcv(c).ok


def test_open_candle_rejected_by_time_not_api_position():
    now = datetime(2024, 6, 15, 12, 0, 30, tzinfo=UTC)
    # 1h candle that opened at 12:00 — not closed yet (needs 12:00+1h+30s)
    open_candle = RawCandle(
        timestamp=datetime(2024, 6, 15, 12, 0, 0, tzinfo=UTC),
        open=Decimal("1"),
        high=Decimal("2"),
        low=Decimal("0.5"),
        close=Decimal("1.5"),
        volume=Decimal("10"),
    )
    closed_candle = RawCandle(
        timestamp=datetime(2024, 6, 15, 10, 0, 0, tzinfo=UTC),
        open=Decimal("1"),
        high=Decimal("2"),
        low=Decimal("0.5"),
        close=Decimal("1.5"),
        volume=Decimal("10"),
    )
    assert not is_candle_closed(open_candle.timestamp, "1h", now_utc=now, safety_delay_seconds=30)
    assert is_candle_closed(closed_candle.timestamp, "1h", now_utc=now, safety_delay_seconds=30)

    accepted, rejected = filter_closed_candles(
        [open_candle, closed_candle], "1h", now_utc=now, safety_delay_seconds=30
    )
    assert len(accepted) == 1
    assert accepted[0].timestamp == closed_candle.timestamp
    assert len(rejected) == 1


def test_safety_delay_boundary():
    # open 10:00, duration 1h => close at 11:00; with delay 30s eligible at 11:00:30
    open_time = datetime(2024, 6, 15, 10, 0, 0, tzinfo=UTC)
    assert not is_candle_closed(
        open_time, "1h", now_utc=open_time + timedelta(hours=1, seconds=29), safety_delay_seconds=30
    )
    assert is_candle_closed(
        open_time, "1h", now_utc=open_time + timedelta(hours=1, seconds=30), safety_delay_seconds=30
    )
