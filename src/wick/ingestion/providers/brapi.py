"""brapi provider — optional Brazilian equity source (token optional)."""

from __future__ import annotations

import contextlib
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import httpx

from wick.ingestion.providers.base import (
    AssetRef,
    AuthConfigError,
    FetchResult,
    MarketDataProvider,
    ProviderError,
)
from wick.ingestion.validators import RawCandle

_TF_MAP = {
    "1d": "1d",
    "1w": "1wk",
    "1h": "1h",
}


class BrapiProvider(MarketDataProvider):
    name = "brapi"
    asset_type = "stock"

    def __init__(
        self,
        token: str | None = None,
        base_url: str = "https://brapi.dev/api",
        client: httpx.Client | None = None,
    ) -> None:
        self.token = token
        self.base_url = base_url.rstrip("/")
        self._client = client

    def resolve_asset(self, symbol: str) -> AssetRef:
        return AssetRef(
            symbol=symbol.upper(),
            asset_type="stock",
            exchange="B3",
            currency="BRL",
            timezone="America/Sao_Paulo",
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
                f"Unsupported timeframe for brapi: {timeframe}",
                retryable=False,
            )

        params: dict[str, Any] = {
            "range": "max",
            "interval": _TF_MAP[timeframe],
        }
        if self.token:
            params["token"] = self.token

        url = f"{self.base_url}/quote/{symbol}"
        try:
            data = self._get_json(url, params)
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status in {401, 403}:
                raise AuthConfigError(
                    f"brapi authentication failed ({status}); "
                    "set BRAPI_TOKEN or use another provider"
                ) from exc
            retry_after = exc.response.headers.get("Retry-After")
            err = ProviderError(
                f"brapi HTTP {status}: {exc}", retryable=status >= 500 or status == 429
            )
            if retry_after:
                with contextlib.suppress(ValueError):
                    err.retry_after = float(retry_after)  # type: ignore[attr-defined]
            raise err from exc
        except httpx.HTTPError as exc:
            raise ProviderError(str(exc), retryable=True) from exc

        results = data.get("results") or []
        if not results:
            return FetchResult(
                candles=[],
                pages_fetched=1,
                known_limitation="brapi returned no results (token may be required for this symbol)",
            )

        historical = results[0].get("historicalDataPrice") or []
        start_utc = start.astimezone(UTC)
        end_utc = end.astimezone(UTC)
        candles: list[RawCandle] = []
        for item in historical:
            # brapi date is unix seconds
            raw_date = item.get("date")
            if raw_date is None:
                continue
            ts = datetime.fromtimestamp(int(raw_date), tz=UTC)
            if ts < start_utc or ts > end_utc:
                continue
            candles.append(
                RawCandle(
                    timestamp=ts,
                    open=Decimal(str(item["open"])),
                    high=Decimal(str(item["high"])),
                    low=Decimal(str(item["low"])),
                    close=Decimal(str(item["close"])),
                    volume=Decimal(str(item.get("volume") or 0)),
                    adjusted_close=(
                        Decimal(str(item["adjustedClose"]))
                        if item.get("adjustedClose") is not None
                        else None
                    ),
                )
            )

        candles.sort(key=lambda c: c.timestamp)
        limitation = None
        if not self.token:
            limitation = "brapi used without token; coverage may be limited"
        return FetchResult(
            candles=candles,
            pages_fetched=1,
            known_limitation=limitation,
            actual_start=candles[0].timestamp if candles else None,
            actual_end=candles[-1].timestamp if candles else None,
        )

    def _get_json(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        if self._client is not None:
            resp = self._client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()

        with httpx.Client(timeout=30.0) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
