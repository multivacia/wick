"""Timeframe helpers."""

from __future__ import annotations

from datetime import timedelta

SUPPORTED_TIMEFRAMES: dict[str, timedelta] = {
    "1m": timedelta(minutes=1),
    "5m": timedelta(minutes=5),
    "15m": timedelta(minutes=15),
    "1h": timedelta(hours=1),
    "4h": timedelta(hours=4),
    "1d": timedelta(days=1),
    "1w": timedelta(weeks=1),
}


def timeframe_duration(timeframe: str) -> timedelta:
    key = timeframe.strip().lower()
    if key not in SUPPORTED_TIMEFRAMES:
        raise ValueError(
            f"Unsupported timeframe '{timeframe}'. Supported: {', '.join(SUPPORTED_TIMEFRAMES)}"
        )
    return SUPPORTED_TIMEFRAMES[key]


def normalize_timeframe(timeframe: str) -> str:
    key = timeframe.strip().lower()
    if key not in SUPPORTED_TIMEFRAMES:
        raise ValueError(f"Unsupported timeframe '{timeframe}'")
    return key
