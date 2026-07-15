"""Ingestion service tests with fake providers (no network)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, select

from wick.config import Settings
from wick.db.models import Candle, IngestionRun
from wick.ingestion.providers.base import FetchResult, MarketDataProvider, ProviderError
from wick.ingestion.service import IngestionService, IngestRequest
from wick.ingestion.validators import RawCandle


class FakeProvider(MarketDataProvider):
    name = "fake"
    asset_type = "crypto"

    def __init__(self, responses: dict[tuple[str, str], FetchResult | Exception]):
        self.responses = responses
        self.calls: list[tuple[str, str, datetime, datetime]] = []

    def fetch_ohlcv(self, symbol, timeframe, start, end):
        self.calls.append((symbol, timeframe, start, end))
        key = (symbol, timeframe)
        value = self.responses[key]
        if isinstance(value, Exception):
            raise value
        return value


def _bars(start: datetime, n: int, step: timedelta) -> list[RawCandle]:
    out = []
    for i in range(n):
        close = Decimal(str(10 + i))
        out.append(
            RawCandle(
                timestamp=start + step * i,
                open=Decimal("10"),
                high=max(Decimal("12"), close),
                low=Decimal("9"),
                close=close,
                volume=Decimal("100"),
            )
        )
    return out


def test_partial_history_is_not_success(session, settings: Settings):
    start = datetime(2020, 1, 1, tzinfo=UTC)
    end = datetime(2024, 1, 1, tzinfo=UTC)
    actual_start = datetime(2023, 6, 1, tzinfo=UTC)
    candles = _bars(actual_start, 5, timedelta(days=1))
    provider = FakeProvider(
        {
            ("BTC/USDT", "1d"): FetchResult(
                candles=candles,
                pages_fetched=1,
                known_limitation="Source only returns recent history",
                actual_start=candles[0].timestamp,
                actual_end=candles[-1].timestamp,
            )
        }
    )
    service = IngestionService(session, provider, settings, sleep_fn=lambda _: None)
    outcome = service.run(
        IngestRequest(
            source="fake",
            symbols=["BTC/USDT"],
            timeframes=["1d"],
            start=start,
            end=end,
            incremental=False,
        )
    )
    assert outcome.report.status == "PARTIAL"
    assert outcome.run.status == "PARTIAL"
    assert (
        "limitation" in (outcome.report.coverage[0].known_limitation or "").lower()
        or outcome.report.coverage[0].status == "PARTIAL"
    )


def test_open_candle_not_persisted(session, settings: Settings):
    # Freeze "now" via safety: use candles relative to real now — better inject via settings
    # Use a very recent open candle and a closed one
    now = datetime.now(UTC)
    open_ts = now.replace(minute=0, second=0, microsecond=0)
    closed_ts = open_ts - timedelta(hours=5)
    candles = _bars(closed_ts, 1, timedelta(hours=1)) + _bars(open_ts, 1, timedelta(hours=1))
    # Force the second candle to be at open_ts
    candles[1] = RawCandle(
        timestamp=open_ts,
        open=Decimal("10"),
        high=Decimal("11"),
        low=Decimal("9"),
        close=Decimal("10.5"),
        volume=Decimal("1"),
    )
    provider = FakeProvider(
        {
            ("BTC/USDT", "1h"): FetchResult(
                candles=candles,
                pages_fetched=1,
                actual_start=closed_ts,
                actual_end=open_ts,
            )
        }
    )
    service = IngestionService(session, provider, settings, sleep_fn=lambda _: None)
    outcome = service.run(
        IngestRequest(
            source="fake",
            symbols=["BTC/USDT"],
            timeframes=["1h"],
            start=closed_ts - timedelta(hours=1),
            end=now,
            incremental=False,
        )
    )
    count = session.execute(select(func.count()).select_from(Candle)).scalar_one()
    assert count == 1
    assert outcome.report.candles_rejected >= 1


def test_one_asset_failure_does_not_fail_all(session, settings: Settings):
    start = datetime(2024, 1, 1, tzinfo=UTC)
    end = datetime(2024, 1, 5, tzinfo=UTC)
    good = _bars(start, 5, timedelta(days=1))
    provider = FakeProvider(
        {
            ("BTC/USDT", "1d"): FetchResult(
                candles=good,
                pages_fetched=1,
                actual_start=good[0].timestamp,
                actual_end=good[-1].timestamp,
            ),
            ("ETH/USDT", "1d"): ProviderError("upstream down", retryable=False),
        }
    )
    service = IngestionService(session, provider, settings, sleep_fn=lambda _: None)
    outcome = service.run(
        IngestRequest(
            source="fake",
            symbols=["BTC/USDT", "ETH/USDT"],
            timeframes=["1d"],
            start=start,
            end=end,
            incremental=False,
        )
    )
    assert outcome.report.status == "PARTIAL"
    assert outcome.report.candles_inserted == 5
    statuses = {c.symbol: c.status for c in outcome.report.coverage}
    assert statuses["BTC/USDT"] == "SUCCESS"
    assert statuses["ETH/USDT"] == "FAILED"


def test_incremental_fetches_only_missing(session, settings: Settings):
    start = datetime(2024, 1, 1, tzinfo=UTC)
    end = datetime(2024, 1, 10, tzinfo=UTC)
    first_batch = _bars(start, 5, timedelta(days=1))
    provider = FakeProvider(
        {
            ("BTC/USDT", "1d"): FetchResult(
                candles=first_batch,
                pages_fetched=1,
                actual_start=first_batch[0].timestamp,
                actual_end=first_batch[-1].timestamp,
            )
        }
    )
    service = IngestionService(session, provider, settings, sleep_fn=lambda _: None)
    service.run(
        IngestRequest(
            source="fake",
            symbols=["BTC/USDT"],
            timeframes=["1d"],
            start=start,
            end=end,
            incremental=True,
        )
    )

    more = _bars(start + timedelta(days=5), 3, timedelta(days=1))
    provider.responses[("BTC/USDT", "1d")] = FetchResult(
        candles=more,
        pages_fetched=1,
        actual_start=more[0].timestamp,
        actual_end=more[-1].timestamp,
    )
    provider.calls.clear()
    service.run(
        IngestRequest(
            source="fake",
            symbols=["BTC/USDT"],
            timeframes=["1d"],
            start=start,
            end=end,
            incremental=True,
        )
    )
    # Second call should start after latest stored candle
    assert provider.calls
    _, _, fetch_start, _ = provider.calls[0]
    assert fetch_start > first_batch[-1].timestamp
    count = session.execute(select(func.count()).select_from(Candle)).scalar_one()
    assert count == 8


def test_invalid_ohlcv_rejected(session, settings: Settings):
    start = datetime(2024, 1, 1, tzinfo=UTC)
    bad = RawCandle(
        timestamp=start,
        open=Decimal("100"),
        high=Decimal("50"),  # invalid
        low=Decimal("40"),
        close=Decimal("90"),
        volume=Decimal("1"),
    )
    provider = FakeProvider(
        {
            ("BTC/USDT", "1d"): FetchResult(
                candles=[bad],
                pages_fetched=1,
                actual_start=start,
                actual_end=start,
            )
        }
    )
    service = IngestionService(session, provider, settings, sleep_fn=lambda _: None)
    outcome = service.run(
        IngestRequest(
            source="fake",
            symbols=["BTC/USDT"],
            timeframes=["1d"],
            start=start,
            end=start + timedelta(days=1),
            incremental=False,
        )
    )
    assert outcome.report.candles_inserted == 0
    assert outcome.report.candles_rejected == 1
    assert session.execute(select(func.count()).select_from(Candle)).scalar_one() == 0


def test_ingestion_run_persisted(session, settings: Settings):
    start = datetime(2024, 1, 1, tzinfo=UTC)
    candles = _bars(start, 2, timedelta(days=1))
    provider = FakeProvider(
        {
            ("BTC/USDT", "1d"): FetchResult(
                candles=candles,
                pages_fetched=2,
                actual_start=candles[0].timestamp,
                actual_end=candles[-1].timestamp,
            )
        }
    )
    service = IngestionService(session, provider, settings, sleep_fn=lambda _: None)
    outcome = service.run(
        IngestRequest(
            source="fake",
            symbols=["BTC/USDT"],
            timeframes=["1d"],
            start=start,
            end=start + timedelta(days=5),
            incremental=False,
        )
    )
    run = session.execute(
        select(IngestionRun).where(IngestionRun.run_id == outcome.report.run_id)
    ).scalar_one()
    assert run.pages_fetched == 2
    assert run.quality_report is not None
    assert run.status in {"SUCCESS", "PARTIAL"}
