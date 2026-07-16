"""Provider unit tests with injected fakes (no network)."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import httpx

from wick.ingestion.providers.binance import BinanceProvider
from wick.ingestion.providers.brapi import BrapiProvider
from wick.ingestion.providers.yahoo import YahooProvider


class FakeExchange:
    def __init__(self, batches):
        self.batches = list(batches)
        self.calls = []

    def fetch_ohlcv(self, symbol, timeframe, since=None, limit=None):
        self.calls.append((symbol, timeframe, since, limit))
        if not self.batches:
            return []
        return self.batches.pop(0)


def test_binance_provider_parses_ccxt_rows():
    start = datetime(2024, 1, 1, tzinfo=UTC)
    ms = int(start.timestamp() * 1000)
    ex = FakeExchange(
        [
            [
                [ms, 100, 110, 90, 105, 1000],
                [ms + 86_400_000, 105, 115, 95, 110, 2000],
            ]
        ]
    )
    provider = BinanceProvider(exchange=ex)
    result = provider.fetch_ohlcv("BTCUSDT", "1d", start, start + timedelta(days=2))
    assert len(result.candles) == 2
    assert result.candles[0].close == Decimal("105")
    assert result.pages_fetched == 1
    assert ex.calls[0][0] == "BTC/USDT"


def test_yahoo_provider_uses_downloader_and_marks_partial():
    start = datetime(2020, 1, 1, tzinfo=UTC)
    end = datetime(2024, 1, 1, tzinfo=UTC)

    def downloader(symbol, interval, effective_start, effective_end):
        assert symbol == "AAPL"
        assert interval == "1h"
        # Simulate clamped start for intraday
        ts = datetime(2023, 12, 1, tzinfo=UTC)
        return [
            {
                "timestamp": ts,
                "open": 100,
                "high": 101,
                "low": 99,
                "close": 100.5,
                "volume": 10,
                "adjusted_close": 100.5,
            }
        ]

    provider = YahooProvider(downloader=downloader)
    result = provider.fetch_ohlcv("AAPL", "1h", start, end)
    assert len(result.candles) == 1
    assert result.known_limitation is not None
    assert "limited" in result.known_limitation.lower()


def test_brapi_works_without_token():
    def handler(request: httpx.Request) -> httpx.Response:
        assert "token" not in str(request.url)
        body = {
            "results": [
                {
                    "historicalDataPrice": [
                        {
                            "date": int(datetime(2024, 1, 2, tzinfo=UTC).timestamp()),
                            "open": 10,
                            "high": 11,
                            "low": 9,
                            "close": 10.5,
                            "volume": 1000,
                            "adjustedClose": 10.5,
                        }
                    ]
                }
            ]
        }
        return httpx.Response(200, json=body)

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)
    provider = BrapiProvider(token=None, client=client)
    result = provider.fetch_ohlcv(
        "PETR4",
        "1d",
        datetime(2024, 1, 1, tzinfo=UTC),
        datetime(2024, 1, 31, tzinfo=UTC),
    )
    assert len(result.candles) == 1
    assert result.known_limitation is not None
