"""OHLCV validation and closed-candle eligibility."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

from wick.timeframes import timeframe_duration


@dataclass(frozen=True)
class RawCandle:
    """Normalized candle payload from a provider."""

    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    adjusted_close: Decimal | None = None
    adjustment_factor: Decimal | None = None
    source_updated_at: datetime | None = None


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    reason: str | None = None


def ensure_utc(ts: datetime) -> datetime:
    if ts.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware (UTC)")
    return ts.astimezone(UTC)


def validate_ohlcv(candle: RawCandle) -> ValidationResult:
    try:
        ts = ensure_utc(candle.timestamp)
    except ValueError as exc:
        return ValidationResult(False, str(exc))

    prices = [candle.open, candle.high, candle.low, candle.close, candle.volume]
    if any(p is None for p in prices):
        return ValidationResult(False, "missing OHLCV field")
    if any(p < 0 for p in prices):
        return ValidationResult(False, "negative price or volume")
    if candle.high < candle.low:
        return ValidationResult(False, "high < low")
    if candle.high < max(candle.open, candle.close):
        return ValidationResult(False, "high < max(open, close)")
    if candle.low > min(candle.open, candle.close):
        return ValidationResult(False, "low > min(open, close)")
    if ts.year < 1970:
        return ValidationResult(False, "timestamp before epoch")
    return ValidationResult(True)


def is_candle_closed(
    open_time: datetime,
    timeframe: str,
    *,
    now_utc: datetime | None = None,
    safety_delay_seconds: int = 30,
) -> bool:
    """A candle is eligible when open_time + duration <= now_utc - safety_delay."""
    open_utc = ensure_utc(open_time)
    now = ensure_utc(now_utc or datetime.now(UTC))
    close_deadline = open_utc + timeframe_duration(timeframe)
    return close_deadline <= now - timedelta(seconds=safety_delay_seconds)


def filter_closed_candles(
    candles: list[RawCandle],
    timeframe: str,
    *,
    now_utc: datetime | None = None,
    safety_delay_seconds: int = 30,
) -> tuple[list[RawCandle], list[RawCandle]]:
    """Return (accepted_closed, rejected_open)."""
    accepted: list[RawCandle] = []
    rejected: list[RawCandle] = []
    for c in candles:
        if is_candle_closed(
            c.timestamp,
            timeframe,
            now_utc=now_utc,
            safety_delay_seconds=safety_delay_seconds,
        ):
            accepted.append(c)
        else:
            rejected.append(c)
    return accepted, rejected


def ohlcv_dict(candle: RawCandle | Any) -> dict[str, str]:
    return {
        "open": str(candle.open),
        "high": str(candle.high),
        "low": str(candle.low),
        "close": str(candle.close),
        "volume": str(candle.volume),
    }


def ohlcv_equal(a: Any, b: RawCandle) -> bool:
    fields = ("open", "high", "low", "close", "volume")
    for field in fields:
        if Decimal(str(getattr(a, field))) != getattr(b, field):
            return False
    # Optional adjusted fields
    a_adj = getattr(a, "adjusted_close", None)
    b_adj = b.adjusted_close
    if a_adj is None and b_adj is None:
        return True
    if a_adj is None or b_adj is None:
        return False
    return Decimal(str(a_adj)) == b_adj
