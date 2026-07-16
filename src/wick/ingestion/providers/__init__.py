"""Provider registry."""

from __future__ import annotations

from wick.config import Settings, get_settings
from wick.ingestion.providers.base import MarketDataProvider
from wick.ingestion.providers.binance import BinanceProvider
from wick.ingestion.providers.brapi import BrapiProvider
from wick.ingestion.providers.yahoo import YahooProvider


def get_provider(name: str, settings: Settings | None = None) -> MarketDataProvider:
    cfg = settings or get_settings()
    key = name.strip().lower()
    if key in {"binance", "ccxt", "crypto"}:
        return BinanceProvider()
    if key in {"yahoo", "yfinance"}:
        return YahooProvider()
    if key == "brapi":
        return BrapiProvider(token=cfg.brapi_token, base_url=cfg.brapi_base_url)
    raise ValueError(f"Unknown provider '{name}'. Use: binance, yahoo, brapi")


__all__ = [
    "BinanceProvider",
    "BrapiProvider",
    "MarketDataProvider",
    "YahooProvider",
    "get_provider",
]
