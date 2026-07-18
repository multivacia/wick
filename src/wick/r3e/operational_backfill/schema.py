"""Structural validators for ingest-json compatible records (no effect metrics)."""

from __future__ import annotations

import math
from typing import Any

from wick.r3e.future_unseen.protections import parse_market_ts
from wick.r3e.operational_backfill.config import SERIES_UNIVERSE
from wick.r3e.operational_backfill.policy import (
    HistoricalBackfillPolicyError,
    HistoricalOperationalBackfillPolicy,
)

REQUIRED_FIELDS = (
    "symbol",
    "timeframe",
    "source",
    "market_ts",
    "open",
    "high",
    "low",
    "close",
    "volume",
)


class StructuralValidationError(ValueError):
    pass


def validate_structural_record(
    raw: dict[str, Any],
    *,
    policy: HistoricalOperationalBackfillPolicy | None = None,
) -> dict[str, Any]:
    """Validate schema + OHLC + historical temporal policy. Returns normalized dict."""
    missing = [k for k in REQUIRED_FIELDS if k not in raw]
    if missing:
        raise StructuralValidationError(f"missing fields: {missing}")

    symbol = str(raw["symbol"])
    timeframe = str(raw["timeframe"])
    source = str(raw["source"])
    if (symbol, timeframe, source) not in set(SERIES_UNIVERSE):
        raise StructuralValidationError(
            f"series not in official universe: {source}|{symbol}|{timeframe}"
        )

    pol = policy or HistoricalOperationalBackfillPolicy()
    try:
        market_ts = pol.assert_eligible(raw["market_ts"])
    except HistoricalBackfillPolicyError as exc:
        raise StructuralValidationError(str(exc)) from exc

    try:
        ohlcv = {k: float(raw[k]) for k in ("open", "high", "low", "close", "volume")}
    except (TypeError, ValueError) as exc:
        raise StructuralValidationError(f"non-numeric OHLCV: {exc}") from exc

    for name, val in ohlcv.items():
        if not math.isfinite(val):
            raise StructuralValidationError(f"non-finite {name}")
    if ohlcv["volume"] < 0:
        raise StructuralValidationError("volume < 0")
    if ohlcv["high"] < ohlcv["open"]:
        raise StructuralValidationError("high < open")
    if ohlcv["high"] < ohlcv["close"]:
        raise StructuralValidationError("high < close")
    if ohlcv["high"] < ohlcv["low"]:
        raise StructuralValidationError("high < low")
    if ohlcv["low"] > ohlcv["open"]:
        raise StructuralValidationError("low > open")
    if ohlcv["low"] > ohlcv["close"]:
        raise StructuralValidationError("low > close")

    revision = int(raw.get("revision", 1))
    if revision < 1:
        raise StructuralValidationError("revision must be >= 1")

    # Ensure timezone survived parse (parse_market_ts already enforces aware UTC).
    _ = parse_market_ts(market_ts)

    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "source": source,
        "market_ts": market_ts.isoformat(),
        "open": ohlcv["open"],
        "high": ohlcv["high"],
        "low": ohlcv["low"],
        "close": ohlcv["close"],
        "volume": ohlcv["volume"],
        "revision": revision,
    }


def is_structurally_compatible_with_future_unseen(record: dict[str, Any]) -> bool:
    """True when record has the ingest-json contract fields with finite OHLCV."""
    try:
        for k in REQUIRED_FIELDS:
            if k not in record:
                return False
        for k in ("open", "high", "low", "close", "volume"):
            if not math.isfinite(float(record[k])):
                return False
        parse_market_ts(record["market_ts"])
        return True
    except Exception:
        return False
