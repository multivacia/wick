"""Ingestion orchestration service."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from wick.config import Settings, get_settings
from wick.db.models import IngestionRun
from wick.ingestion.gaps import detect_gaps, gaps_to_json
from wick.ingestion.providers.base import MarketDataProvider, ProviderError
from wick.ingestion.providers.retry import retry_call
from wick.ingestion.report import AssetCoverage, IngestionQualityReport, iso
from wick.ingestion.upsert import (
    get_or_create_asset,
    latest_candle_timestamp,
    load_timestamps,
    upsert_candles,
)
from wick.ingestion.validators import filter_closed_candles, validate_ohlcv
from wick.timeframes import normalize_timeframe, timeframe_duration


@dataclass
class IngestRequest:
    source: str
    symbols: list[str]
    timeframes: list[str]
    start: datetime
    end: datetime
    incremental: bool = True


@dataclass
class IngestOutcome:
    report: IngestionQualityReport
    run: IngestionRun


@dataclass
class _Counters:
    received: int = 0
    inserted: int = 0
    updated: int = 0
    rejected: int = 0
    pages: int = 0
    retries: int = 0
    coverages: list[AssetCoverage] = field(default_factory=list)
    all_gaps: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    actual_starts: list[datetime] = field(default_factory=list)
    actual_ends: list[datetime] = field(default_factory=list)
    any_success: bool = False
    any_partial: bool = False
    any_failure: bool = False


class IngestionService:
    def __init__(
        self,
        session: Session,
        provider: MarketDataProvider,
        settings: Settings | None = None,
        *,
        sleep_fn=None,
    ) -> None:
        self.session = session
        self.provider = provider
        self.settings = settings or get_settings()
        self.sleep_fn = sleep_fn

    def run(self, request: IngestRequest) -> IngestOutcome:
        run_id = f"ing_{uuid.uuid4().hex[:16]}"
        started = datetime.now(UTC)
        timeframes = [normalize_timeframe(tf) for tf in request.timeframes]
        start = _require_utc(request.start)
        end = _require_utc(request.end)

        run = IngestionRun(
            run_id=run_id,
            source=self.provider.name,
            requested_start=start,
            requested_end=end,
            assets_requested=list(request.symbols),
            timeframes_requested=timeframes,
            status="FAILED",
            started_at=started,
        )
        self.session.add(run)
        self.session.flush()

        counters = _Counters()
        for symbol in request.symbols:
            for timeframe in timeframes:
                self._ingest_one(
                    run_id=run_id,
                    symbol=symbol,
                    timeframe=timeframe,
                    start=start,
                    end=end,
                    incremental=request.incremental,
                    counters=counters,
                )

        status = _aggregate_status(counters)
        finished = datetime.now(UTC)
        report = IngestionQualityReport(
            run_id=run_id,
            source=self.provider.name,
            status=status,
            assets=list(request.symbols),
            timeframes=timeframes,
            coverage=counters.coverages,
            candles_received=counters.received,
            candles_inserted=counters.inserted,
            candles_updated=counters.updated,
            candles_rejected=counters.rejected,
            pages_fetched=counters.pages,
            retries=counters.retries,
            gaps=counters.all_gaps,
            error_summary="; ".join(counters.errors) if counters.errors else None,
            started_at=iso(started),
            finished_at=iso(finished),
            notes=counters.notes,
        )

        run.status = status
        run.candles_received = counters.received
        run.candles_inserted = counters.inserted
        run.candles_updated = counters.updated
        run.candles_rejected = counters.rejected
        run.pages_fetched = counters.pages
        run.retries = counters.retries
        run.error_summary = report.error_summary
        run.coverage = [c.__dict__ for c in counters.coverages]
        run.gaps = counters.all_gaps
        run.quality_report = report.to_dict()
        run.finished_at = finished
        run.actual_start = min(counters.actual_starts) if counters.actual_starts else None
        run.actual_end = max(counters.actual_ends) if counters.actual_ends else None
        self.session.flush()

        return IngestOutcome(report=report, run=run)

    def _ingest_one(
        self,
        *,
        run_id: str,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
        incremental: bool,
        counters: _Counters,
    ) -> None:
        """Process one symbol/timeframe inside a SAVEPOINT for isolation."""
        try:
            with self.session.begin_nested():
                self._process_symbol_timeframe(
                    run_id=run_id,
                    symbol=symbol,
                    timeframe=timeframe,
                    start=start,
                    end=end,
                    incremental=incremental,
                    counters=counters,
                )
        except Exception as exc:  # noqa: BLE001 — isolate per asset/timeframe
            # SAVEPOINT already rolled back DB writes for this unit.
            # Coverage/error may already be recorded by _process_symbol_timeframe.
            already = any(
                c.symbol.upper() == symbol.upper()
                and c.timeframe == timeframe
                and c.status == "FAILED"
                for c in counters.coverages
            )
            if not already:
                try:
                    resolved = self.provider.resolve_asset(symbol).symbol
                except Exception:  # noqa: BLE001
                    resolved = symbol
                counters.any_failure = True
                counters.errors.append(f"{resolved}/{timeframe}: {exc}")
                counters.coverages.append(
                    AssetCoverage(
                        symbol=resolved,
                        timeframe=timeframe,
                        status="FAILED",
                        requested_start=iso(start),
                        requested_end=iso(end),
                        actual_start=None,
                        actual_end=None,
                        error=str(exc),
                    )
                )

    def _process_symbol_timeframe(
        self,
        *,
        run_id: str,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
        incremental: bool,
        counters: _Counters,
    ) -> None:
        asset_ref = self.provider.resolve_asset(symbol)
        try:
            asset = get_or_create_asset(
                self.session,
                symbol=asset_ref.symbol,
                asset_type=asset_ref.asset_type,
                source=self.provider.name,
                exchange=asset_ref.exchange,
                currency=asset_ref.currency,
                timezone=asset_ref.timezone,
            )

            fetch_start = start
            if incremental:
                latest = latest_candle_timestamp(
                    self.session,
                    asset_id=asset.id,
                    timeframe=timeframe,
                    source=self.provider.name,
                )
                if latest is not None:
                    fetch_start = latest + timeframe_duration(timeframe)
                    if fetch_start >= end:
                        cov = AssetCoverage(
                            symbol=asset_ref.symbol,
                            timeframe=timeframe,
                            status="SUCCESS",
                            requested_start=iso(start),
                            requested_end=iso(end),
                            actual_start=iso(latest),
                            actual_end=iso(latest),
                            known_limitation=(
                                "Already up to date for append-only incremental mode; "
                                "historical gap repair requires --full"
                            ),
                        )
                        counters.coverages.append(cov)
                        counters.any_success = True
                        return

            kwargs: dict[str, Any] = {
                "max_retries": self.settings.ingestion_max_retries,
                "base_seconds": self.settings.ingestion_backoff_base_seconds,
            }
            if self.sleep_fn is not None:
                kwargs["sleep_fn"] = self.sleep_fn

            try:
                fetch, retries = retry_call(
                    lambda: self.provider.fetch_ohlcv(
                        asset_ref.symbol, timeframe, fetch_start, end
                    ),
                    **kwargs,
                )
            except ProviderError as exc:
                counters.any_failure = True
                counters.errors.append(f"{asset_ref.symbol}/{timeframe}: {exc}")
                counters.coverages.append(
                    AssetCoverage(
                        symbol=asset_ref.symbol,
                        timeframe=timeframe,
                        status="FAILED",
                        requested_start=iso(start),
                        requested_end=iso(end),
                        actual_start=None,
                        actual_end=None,
                        error=str(exc),
                    )
                )
                return

            counters.retries += retries
            counters.pages += fetch.pages_fetched
            counters.received += len(fetch.candles)

            closed, open_rejected = filter_closed_candles(
                fetch.candles,
                timeframe,
                safety_delay_seconds=self.settings.candle_close_safety_delay_seconds,
            )
            valid: list = []
            invalid_count = 0
            for c in closed:
                result = validate_ohlcv(c)
                if result.ok:
                    valid.append(c)
                else:
                    invalid_count += 1

            rejected = len(open_rejected) + invalid_count
            counters.rejected += rejected

            stats = upsert_candles(
                self.session,
                asset=asset,
                timeframe=timeframe,
                source=self.provider.name,
                candles=valid,
                run_id=run_id,
            )
            counters.inserted += stats.inserted
            counters.updated += stats.updated

            timestamps = load_timestamps(
                self.session,
                asset_id=asset.id,
                timeframe=timeframe,
                source=self.provider.name,
            )
            gaps = detect_gaps(
                timestamps,
                asset_symbol=asset_ref.symbol,
                timeframe=timeframe,
                asset_type=asset_ref.asset_type,
            )
            gaps_json = gaps_to_json(gaps)
            counters.all_gaps.extend(gaps_json)

            actual_start = fetch.actual_start
            actual_end = fetch.actual_end
            if actual_start:
                counters.actual_starts.append(actual_start)
            if actual_end:
                counters.actual_ends.append(actual_end)

            status, error, notes, _partial = _classify_coverage(
                asset_type=asset_ref.asset_type,
                timeframe=timeframe,
                start=start,
                end=end,
                actual_start=actual_start,
                actual_end=actual_end,
                valid_count=len(valid),
                received_count=len(fetch.candles),
                known_limitation=fetch.known_limitation,
            )
            if status == "FAILED":
                counters.any_failure = True
            elif status == "PARTIAL":
                counters.any_partial = True
                counters.any_success = True
            else:
                counters.any_success = True

            if asset_ref.asset_type == "stock":
                counters.notes.append(
                    f"{asset_ref.symbol}/{timeframe}: stock gap check is partial "
                    "(trading calendar not implemented)"
                )

            series_used = None
            if fetch.metadata:
                series_used = fetch.metadata.get("series_used")

            counters.coverages.append(
                AssetCoverage(
                    symbol=asset_ref.symbol,
                    timeframe=timeframe,
                    status=status,
                    requested_start=iso(start),
                    requested_end=iso(end),
                    actual_start=iso(actual_start),
                    actual_end=iso(actual_end),
                    candles_received=len(fetch.candles),
                    candles_inserted=stats.inserted,
                    candles_updated=stats.updated,
                    candles_rejected=rejected,
                    candles_unchanged=stats.unchanged,
                    open_candles_rejected=len(open_rejected),
                    invalid_rejected=invalid_count,
                    known_limitation="; ".join(notes) if notes else fetch.known_limitation,
                    gaps=gaps_json,
                    error=error,
                    series_used=series_used,
                )
            )
        except Exception as exc:
            counters.any_failure = True
            counters.errors.append(f"{asset_ref.symbol}/{timeframe}: {exc}")
            counters.coverages.append(
                AssetCoverage(
                    symbol=asset_ref.symbol,
                    timeframe=timeframe,
                    status="FAILED",
                    requested_start=iso(start),
                    requested_end=iso(end),
                    actual_start=None,
                    actual_end=None,
                    error=str(exc),
                )
            )
            raise


def _require_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError("ingestion timestamps must be timezone-aware (UTC)")
    return dt.astimezone(UTC)


def _coverage_tolerance(timeframe: str, asset_type: str) -> timedelta:
    """Allowed slack between requested and actual coverage before PARTIAL."""
    if asset_type == "stock":
        return max(timeframe_duration(timeframe) * 2, timedelta(days=5))
    return timeframe_duration(timeframe) * 2


def _classify_coverage(
    *,
    asset_type: str,
    timeframe: str,
    start: datetime,
    end: datetime,
    actual_start: datetime | None,
    actual_end: datetime | None,
    valid_count: int,
    received_count: int,
    known_limitation: str | None,
) -> tuple[str, str | None, list[str], bool]:
    notes: list[str] = []
    if known_limitation:
        notes.append(known_limitation)

    if valid_count == 0:
        if received_count == 0:
            return "FAILED", (known_limitation or "No candles returned"), notes, False
        return (
            "FAILED",
            "All received candles were rejected (open or invalid OHLCV)",
            notes,
            False,
        )

    partial = bool(known_limitation)
    tol = _coverage_tolerance(timeframe, asset_type)
    if actual_start is not None and actual_start > start + tol:
        partial = True
        notes.append(
            f"Actual start {actual_start.isoformat()} later than requested {start.isoformat()}"
        )
    if actual_end is not None and actual_end < end - tol:
        partial = True
        notes.append(
            f"Actual end {actual_end.isoformat()} earlier than requested {end.isoformat()}"
        )

    if partial:
        return "PARTIAL", None, notes, True
    return "SUCCESS", None, notes, False


def _aggregate_status(counters: _Counters) -> str:
    if counters.any_success and not counters.any_failure and not counters.any_partial:
        return "SUCCESS"
    if counters.any_success or counters.inserted > 0 or counters.updated > 0:
        if counters.any_failure or counters.any_partial:
            return "PARTIAL"
        return "SUCCESS"
    return "FAILED"
