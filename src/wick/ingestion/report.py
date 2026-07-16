"""Quality / coverage report builders."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class AssetCoverage:
    symbol: str
    timeframe: str
    status: str
    requested_start: str | None
    requested_end: str | None
    actual_start: str | None
    actual_end: str | None
    candles_received: int = 0
    candles_inserted: int = 0
    candles_updated: int = 0
    candles_rejected: int = 0
    candles_unchanged: int = 0
    open_candles_rejected: int = 0
    invalid_rejected: int = 0
    known_limitation: str | None = None
    gaps: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None
    series_used: str | None = None


@dataclass
class IngestionQualityReport:
    run_id: str
    source: str
    status: str
    assets: list[str]
    timeframes: list[str]
    coverage: list[AssetCoverage]
    candles_received: int = 0
    candles_inserted: int = 0
    candles_updated: int = 0
    candles_rejected: int = 0
    pages_fetched: int = 0
    retries: int = 0
    gaps: list[dict[str, Any]] = field(default_factory=list)
    error_summary: str | None = None
    started_at: str | None = None
    finished_at: str | None = None
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def write(self, path: Path | str) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.to_json() + "\n", encoding="utf-8")
        return out

    def render_text(self) -> str:
        lines = [
            f"Ingestion run: {self.run_id}",
            f"Source: {self.source}",
            f"Status: {self.status}",
            f"Assets: {', '.join(self.assets)}",
            f"Timeframes: {', '.join(self.timeframes)}",
            (
                f"Candles received={self.candles_received} "
                f"inserted={self.candles_inserted} "
                f"updated={self.candles_updated} "
                f"rejected={self.candles_rejected}"
            ),
            f"Pages={self.pages_fetched} retries={self.retries}",
        ]
        if self.error_summary:
            lines.append(f"Errors: {self.error_summary}")
        for cov in self.coverage:
            lines.append(
                f"  - {cov.symbol} {cov.timeframe}: {cov.status} "
                f"recv={cov.candles_received} ins={cov.candles_inserted} "
                f"upd={cov.candles_updated} rej={cov.candles_rejected}"
            )
            if cov.known_limitation:
                lines.append(f"      limitation: {cov.known_limitation}")
            if cov.error:
                lines.append(f"      error: {cov.error}")
            if cov.gaps:
                lines.append(f"      gaps: {len(cov.gaps)}")
        for note in self.notes:
            lines.append(f"Note: {note}")
        return "\n".join(lines)


def iso(dt: datetime | None) -> str | None:
    return dt.isoformat() if dt is not None else None
