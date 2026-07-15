"""Provider interface and shared types."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from wick.ingestion.validators import RawCandle


@dataclass
class FetchResult:
    candles: list[RawCandle]
    pages_fetched: int = 0
    retries: int = 0
    known_limitation: str | None = None
    actual_start: datetime | None = None
    actual_end: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AssetRef:
    symbol: str
    asset_type: str  # crypto|stock
    exchange: str | None = None
    currency: str | None = None
    timezone: str = "UTC"


class ProviderError(Exception):
    """Base provider error."""

    def __init__(self, message: str, *, retryable: bool = True) -> None:
        super().__init__(message)
        self.retryable = retryable


class AuthConfigError(ProviderError):
    def __init__(self, message: str) -> None:
        super().__init__(message, retryable=False)


class MarketDataProvider(ABC):
    name: str
    asset_type: str

    @abstractmethod
    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> FetchResult:
        raise NotImplementedError

    def resolve_asset(self, symbol: str) -> AssetRef:
        return AssetRef(symbol=symbol.upper(), asset_type=self.asset_type)
