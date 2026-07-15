"""Generate an offline sample quality report (requires migrated DB, no network)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from wick.config import get_settings
from wick.db.session import session_scope
from wick.ingestion.providers.base import FetchResult, MarketDataProvider
from wick.ingestion.service import IngestionService, IngestRequest
from wick.ingestion.validators import RawCandle


class DemoProvider(MarketDataProvider):
    name = "binance"
    asset_type = "crypto"

    def fetch_ohlcv(self, symbol, timeframe, start, end):
        base = datetime(2024, 1, 1, tzinfo=UTC)
        candles = [
            RawCandle(
                timestamp=base + timedelta(days=i),
                open=Decimal("40000"),
                high=Decimal("41000"),
                low=Decimal("39000"),
                close=Decimal(str(40000 + i * 10)),
                volume=Decimal("100"),
            )
            for i in range(10)
        ]
        return FetchResult(
            candles=candles,
            pages_fetched=1,
            known_limitation="Demo provider returns a short synthetic window",
            actual_start=candles[0].timestamp,
            actual_end=candles[-1].timestamp,
        )


def main() -> None:
    settings = get_settings()
    with session_scope(settings) as session:
        service = IngestionService(session, DemoProvider(), settings, sleep_fn=lambda _: None)
        outcome = service.run(
            IngestRequest(
                source="binance",
                symbols=["BTC/USDT"],
                timeframes=["1d"],
                start=datetime(2020, 1, 1, tzinfo=UTC),
                end=datetime(2024, 6, 1, tzinfo=UTC),
                incremental=False,
            )
        )
        out = Path("reports/example_ingestion_quality.json")
        outcome.report.write(out)
        print(outcome.report.render_text())
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
