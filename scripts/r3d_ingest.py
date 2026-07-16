#!/usr/bin/env python3
"""Ingest the R3D universe (full historical windows, no artificial gap fill)."""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from wick.config import get_settings
from wick.db.session import session_scope
from wick.ingestion.providers import get_provider
from wick.ingestion.service import IngestionService, IngestRequest
from wick.r3d.universe import UNIVERSE

OUT = Path("reports/r3d")
END = datetime(2026, 7, 16, 23, 59, 59, tzinfo=UTC)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    settings = get_settings()
    results: list[dict] = []
    # Group by (source, timeframe) to batch symbols
    groups: dict[tuple[str, str], list] = {}
    for spec in UNIVERSE:
        groups.setdefault((spec.source, spec.timeframe), []).append(spec)

    for (source, timeframe), specs in groups.items():
        symbols = [s.symbol for s in specs]
        start = min(s.target_start for s in specs)
        print(
            f"=== ingest {source} {timeframe} n={len(symbols)} start={start.isoformat()} ===",
            flush=True,
        )
        provider = get_provider(source, settings)
        request = IngestRequest(
            source=provider.name,
            symbols=symbols,
            timeframes=[timeframe],
            start=start,
            end=END,
            incremental=False,  # full window for R3D
        )
        try:
            with session_scope(settings) as session:
                service = IngestionService(session, provider, settings)
                outcome = service.run(request)
                report = outcome.report
            path = OUT / f"ingestion_{source}_{timeframe}.json"
            report.write(path)
            print(report.render_text(), flush=True)
            results.append(
                {
                    "source": source,
                    "timeframe": timeframe,
                    "status": report.status,
                    "report": str(path),
                    "candles_inserted": report.candles_inserted,
                    "candles_rejected": report.candles_rejected,
                }
            )
        except Exception as exc:  # noqa: BLE001 — record and continue other groups
            print(f"FAILED {source} {timeframe}: {exc}", flush=True)
            results.append(
                {
                    "source": source,
                    "timeframe": timeframe,
                    "status": "FAILED",
                    "error": str(exc),
                }
            )

    summary_path = OUT / "ingestion_summary.json"
    summary_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {summary_path}", flush=True)
    failed = [r for r in results if r.get("status") == "FAILED"]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
