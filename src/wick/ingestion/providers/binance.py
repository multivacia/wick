"""Binance market-data provider (public klines, no API key).

Uses Binance public data API (`data-api.binance.vision`) by default. An optional
ccxt-like exchange object can be injected for tests (`fetch_ohlcv` interface).
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import httpx

from wick.ingestion.providers.base import (
    AssetRef,
    FetchResult,
    MarketDataProvider,
    ProviderError,
)
from wick.ingestion.validators import RawCandle

_TF_MAP = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "1h": "1h",
    "4h": "4h",
    "1d": "1d",
    "1w": "1w",
}

_DEFAULT_BASE_URL = "https://data-api.binance.vision"


class BinanceProvider(MarketDataProvider):
    name = "binance"
    asset_type = "crypto"

    def __init__(
        self,
        exchange: Any | None = None,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        client: httpx.Client | None = None,
    ) -> None:
        self._exchange = exchange
        self._base_url = base_url.rstrip("/")
        self._client = client

    def resolve_asset(self, symbol: str) -> AssetRef:
        sym = symbol.upper().replace("-", "").replace("_", "")
        if "/" not in sym and sym.endswith("USDT") and len(sym) > 4:
            base = sym[:-4]
            sym = f"{base}/USDT"
        elif "/" not in sym:
            sym = symbol.upper()
        return AssetRef(
            symbol=sym,
            asset_type="crypto",
            exchange="binance",
            currency="USDT" if "USDT" in sym else None,
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
            raise ProviderError(
                f"Unsupported timeframe for Binance: {timeframe}",
                retryable=False,
            )

        asset = self.resolve_asset(symbol)
        if self._exchange is not None:
            return self._fetch_via_exchange(asset.symbol, timeframe, start, end)
        return self._fetch_via_rest(asset.symbol, timeframe, start, end)

    def _to_binance_symbol(self, symbol: str) -> str:
        return symbol.replace("/", "")

    def _fetch_via_exchange(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> FetchResult:
        since_ms = int(start.astimezone(UTC).timestamp() * 1000)
        end_ms = int(end.astimezone(UTC).timestamp() * 1000)
        limit = 1000
        all_rows: list[list[Any]] = []
        pages = 0
        while since_ms < end_ms:
            try:
                batch = self._exchange.fetch_ohlcv(
                    symbol, _TF_MAP[timeframe], since=since_ms, limit=limit
                )
            except Exception as exc:
                msg = str(exc).lower()
                retryable = "auth" not in msg and "api key" not in msg
                raise ProviderError(str(exc), retryable=retryable) from exc
            pages += 1
            if not batch:
                break
            all_rows.extend(batch)
            last_ts = batch[-1][0]
            next_since = last_ts + 1
            if next_since <= since_ms:
                break
            since_ms = next_since
            if len(batch) < limit:
                break
        return self._rows_to_result(all_rows, start, end, pages)

    def _fetch_via_rest(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> FetchResult:
        # Binance public klines — same payload shape as ccxt/binance spot.
        market = self._to_binance_symbol(symbol)
        since_ms = int(start.astimezone(UTC).timestamp() * 1000)
        end_ms = int(end.astimezone(UTC).timestamp() * 1000)
        limit = 1000
        all_rows: list[list[Any]] = []
        pages = 0
        url = f"{self._base_url}/api/v3/klines"

        while since_ms < end_ms:
            params = {
                "symbol": market,
                "interval": _TF_MAP[timeframe],
                "startTime": since_ms,
                "endTime": end_ms,
                "limit": limit,
            }
            try:
                data = self._get_json(url, params)
            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code
                retryable = status >= 500 or status == 429
                raise ProviderError(
                    f"binance HTTP {status}: {exc.response.text[:200]}",
                    retryable=retryable,
                ) from exc
            except httpx.HTTPError as exc:
                raise ProviderError(str(exc), retryable=True) from exc

            pages += 1
            if not data:
                break
            all_rows.extend(data)
            last_ts = int(data[-1][0])
            next_since = last_ts + 1
            if next_since <= since_ms:
                break
            since_ms = next_since
            if len(data) < limit:
                break

        return self._rows_to_result(all_rows, start, end, pages)

    def _get_json(self, url: str, params: dict[str, Any]) -> list[Any]:
        if self._client is not None:
            resp = self._client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
        with httpx.Client(timeout=30.0) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()

    def _rows_to_result(
        self,
        all_rows: list[list[Any]],
        start: datetime,
        end: datetime,
        pages: int,
    ) -> FetchResult:
        start_utc = start.astimezone(UTC)
        end_utc = end.astimezone(UTC)
        candles: list[RawCandle] = []
        for row in all_rows:
            ts = datetime.fromtimestamp(int(row[0]) / 1000, tz=UTC)
            if ts < start_utc or ts > end_utc:
                continue
            candles.append(
                RawCandle(
                    timestamp=ts,
                    open=Decimal(str(row[1])),
                    high=Decimal(str(row[2])),
                    low=Decimal(str(row[3])),
                    close=Decimal(str(row[4])),
                    volume=Decimal(str(row[5])),
                )
            )
        candles.sort(key=lambda c: c.timestamp)
        return FetchResult(
            candles=candles,
            pages_fetched=pages,
            actual_start=candles[0].timestamp if candles else None,
            actual_end=candles[-1].timestamp if candles else None,
            metadata={"api": "binance_public_klines", "base_url": self._base_url},
        )
