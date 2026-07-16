"""Yahoo Finance provider via yfinance (no API key)."""

from __future__ import annotations

import math
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from typing import Any

from wick.ingestion.providers.base import (
    AssetRef,
    FetchResult,
    MarketDataProvider,
    ProviderError,
)
from wick.ingestion.validators import RawCandle

# yfinance interval mapping
_TF_MAP = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "1h": "1h",
    "4h": "1h",  # yfinance has no native 4h; resample later if needed — mark limitation
    "1d": "1d",
    "1w": "1wk",
}

# Known intraday history limits (approximate, documented by Yahoo)
_INTRADAY_MAX_LOOKBACK = {
    "1m": timedelta(days=7),
    "5m": timedelta(days=60),
    "15m": timedelta(days=60),
    "1h": timedelta(days=730),
}


class YahooProvider(MarketDataProvider):
    name = "yahoo"
    asset_type = "stock"

    def __init__(self, downloader: Any | None = None) -> None:
        self._downloader = downloader

    def resolve_asset(self, symbol: str) -> AssetRef:
        return AssetRef(
            symbol=symbol.upper(),
            asset_type="stock",
            exchange="yahoo",
            currency=None,
            timezone="UTC",
        )

    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> FetchResult:
        if timeframe not in _TF_MAP:
            raise ProviderError(f"Unsupported timeframe for Yahoo: {timeframe}", retryable=False)

        start_utc = start.astimezone(UTC)
        end_utc = end.astimezone(UTC)
        known_limitation: str | None = None
        effective_start = start_utc

        if timeframe in _INTRADAY_MAX_LOOKBACK:
            earliest = datetime.now(UTC) - _INTRADAY_MAX_LOOKBACK[timeframe]
            if effective_start < earliest:
                effective_start = earliest
                known_limitation = (
                    f"Yahoo intraday ({timeframe}) history is limited; "
                    f"requested start {start_utc.isoformat()} clamped to "
                    f"{effective_start.isoformat()}"
                )

        if timeframe == "4h":
            known_limitation = (
                known_limitation + "; " if known_limitation else ""
            ) + "Yahoo has no native 4h; returning 1h bars (caller should not treat as 4h)"
            # Refuse to silently mislabel — raise for 4h
            raise ProviderError(
                "Yahoo provider does not support native 4h timeframe",
                retryable=False,
            )

        interval = _TF_MAP[timeframe]
        try:
            rows = self._download(symbol, interval, effective_start, end_utc)
        except Exception as exc:
            msg = str(exc)
            lower = msg.lower()
            retryable = True
            retry_after = None
            if "401" in lower or "403" in lower or "unauthorized" in lower:
                retryable = False
            if "429" in lower or "too many requests" in lower or "rate limit" in lower:
                retryable = True
                retry_after = 5.0
            err = ProviderError(msg, retryable=retryable)
            if retry_after is not None:
                err.retry_after = retry_after  # type: ignore[attr-defined]
            raise err from exc

        candles: list[RawCandle] = []
        for row in rows:
            ts = row["timestamp"]
            ts = ts.replace(tzinfo=UTC) if ts.tzinfo is None else ts.astimezone(UTC)
            if ts < start_utc or ts > end_utc:
                continue
            adj = row.get("adjusted_close")
            candles.append(
                RawCandle(
                    timestamp=ts,
                    open=Decimal(str(row["open"])),
                    high=Decimal(str(row["high"])),
                    low=Decimal(str(row["low"])),
                    close=Decimal(str(row["close"])),
                    volume=Decimal(str(row["volume"])),
                    adjusted_close=Decimal(str(adj)) if adj is not None else None,
                    adjustment_factor=(
                        (Decimal(str(adj)) / Decimal(str(row["close"])))
                        if adj is not None and Decimal(str(row["close"])) != 0
                        else None
                    ),
                )
            )

        candles.sort(key=lambda c: c.timestamp)
        actual_start = candles[0].timestamp if candles else None
        actual_end = candles[-1].timestamp if candles else None

        # Partial if we got less coverage than requested (common for stocks/intraday)
        if candles and known_limitation is None and actual_start > start_utc + timedelta(days=1):
            known_limitation = (
                f"Partial history: requested {start_utc.isoformat()}–"
                f"{end_utc.isoformat()}, got {actual_start.isoformat()}–"
                f"{actual_end.isoformat() if actual_end else 'n/a'}"
            )

        return FetchResult(
            candles=candles,
            pages_fetched=1,
            known_limitation=known_limitation,
            actual_start=actual_start,
            actual_end=actual_end,
            metadata={"series_used": "adjusted_close_when_available"},
        )

    def _download(
        self,
        symbol: str,
        interval: str,
        start: datetime,
        end: datetime,
    ) -> list[dict[str, Any]]:
        if self._downloader is not None:
            return self._downloader(symbol, interval, start, end)

        import yfinance as yf

        ticker = yf.Ticker(symbol)
        # yfinance end is exclusive for some intervals; add a day buffer for daily
        end_inclusive = end + timedelta(days=1)
        df = ticker.history(
            start=start.strftime("%Y-%m-%d"),
            end=end_inclusive.strftime("%Y-%m-%d"),
            interval=interval,
            auto_adjust=False,
        )
        if df is None or df.empty:
            return []

        rows: list[dict[str, Any]] = []
        for idx, rec in df.iterrows():
            ts = idx.to_pydatetime() if hasattr(idx, "to_pydatetime") else idx
            adj = rec.get("Adj Close", None)
            if adj is not None and math.isnan(float(adj)):
                adj = None
            vol = rec.get("Volume", 0)
            if vol is not None and math.isnan(float(vol)):
                vol = 0
            rows.append(
                {
                    "timestamp": ts,
                    "open": float(rec["Open"]),
                    "high": float(rec["High"]),
                    "low": float(rec["Low"]),
                    "close": float(rec["Close"]),
                    "volume": float(vol or 0),
                    "adjusted_close": float(adj) if adj is not None else None,
                }
            )
        return rows
