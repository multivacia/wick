"""Coverage and quality assessment for R3D series."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from wick.db.models import Asset, Candle, IngestionRun
from wick.r3d.universe import SeriesSpec
from wick.timeframes import timeframe_duration


@dataclass
class SeriesCoverage:
    source: str
    symbol: str
    timeframe: str
    asset_class: str
    asset_id: str | None
    candle_count: int
    rejected_estimate: int
    first_ts: str | None
    last_ts: str | None
    span_years: float | None
    min_years_required: float
    coverage_status: str  # COMPLETE | PARTIAL | MISSING
    gap_count_estimate: int
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _years_between(a: datetime, b: datetime) -> float:
    return abs((b - a).total_seconds()) / (365.25 * 24 * 3600)


def assess_series(session: Session, spec: SeriesSpec) -> SeriesCoverage:
    notes: list[str] = []
    asset = session.execute(
        select(Asset).where(Asset.symbol == spec.symbol, Asset.source == spec.source)
    ).scalar_one_or_none()
    if asset is None:
        return SeriesCoverage(
            source=spec.source,
            symbol=spec.symbol,
            timeframe=spec.timeframe,
            asset_class=spec.asset_class,
            asset_id=None,
            candle_count=0,
            rejected_estimate=0,
            first_ts=None,
            last_ts=None,
            span_years=None,
            min_years_required=spec.min_years,
            coverage_status="MISSING",
            gap_count_estimate=0,
            notes=["asset not found after ingestion"],
        )

    rows = list(
        session.execute(
            select(Candle)
            .where(
                Candle.asset_id == asset.id,
                Candle.timeframe == spec.timeframe,
                Candle.is_closed.is_(True),
            )
            .order_by(Candle.timestamp.asc())
        ).scalars()
    )
    if not rows:
        return SeriesCoverage(
            source=spec.source,
            symbol=spec.symbol,
            timeframe=spec.timeframe,
            asset_class=spec.asset_class,
            asset_id=str(asset.id),
            candle_count=0,
            rejected_estimate=0,
            first_ts=None,
            last_ts=None,
            span_years=None,
            min_years_required=spec.min_years,
            coverage_status="MISSING",
            gap_count_estimate=0,
            notes=["no closed candles stored"],
        )

    first = rows[0].timestamp
    last = rows[-1].timestamp
    if first.tzinfo is None:
        first = first.replace(tzinfo=UTC)
    if last.tzinfo is None:
        last = last.replace(tzinfo=UTC)
    span = _years_between(first, last)

    # Gap estimate: expected steps vs observed (no artificial fill)
    duration = timeframe_duration(spec.timeframe)
    expected = int((last - first) / duration) + 1 if duration.total_seconds() > 0 else len(rows)
    gap_est = max(0, expected - len(rows))
    # For equities, weekends/holidays inflate "gaps"; note but don't fabricate fills.
    if spec.asset_class == "stock":
        notes.append("equity calendar gaps expected (weekends/holidays); not filled")
        # Use span_years vs min_years as primary COMPLETE/PARTIAL criterion
        status = "COMPLETE" if span + 1e-9 >= spec.min_years else "PARTIAL"
    else:
        # Crypto: flag large gap ratio as PARTIAL even if span ok
        status = "COMPLETE" if span + 1e-9 >= spec.min_years else "PARTIAL"
        if expected > 0 and gap_est / expected > 0.05:
            status = "PARTIAL"
            notes.append(f"gap_ratio={gap_est / expected:.3f} exceeds 5%")

    if span + 1e-9 < spec.min_years:
        notes.append(f"span_years={span:.3f} < min_years={spec.min_years}")

    # Rejected from latest ingestion runs (best-effort)
    rejected = 0
    runs = session.execute(
        select(IngestionRun)
        .where(IngestionRun.source == spec.source)
        .order_by(IngestionRun.started_at.desc())
        .limit(20)
    ).scalars()
    for run in runs:
        meta = run.quality_report or {}
        # quality report structure varies; accumulate if present
        if isinstance(meta, dict):
            rejected += int(meta.get("candles_rejected", 0) or 0)

    return SeriesCoverage(
        source=spec.source,
        symbol=spec.symbol,
        timeframe=spec.timeframe,
        asset_class=spec.asset_class,
        asset_id=str(asset.id),
        candle_count=len(rows),
        rejected_estimate=rejected,
        first_ts=first.isoformat(),
        last_ts=last.isoformat(),
        span_years=span,
        min_years_required=spec.min_years,
        coverage_status=status,
        gap_count_estimate=gap_est,
        notes=notes,
    )


def assess_universe(session: Session, specs: list[SeriesSpec]) -> list[SeriesCoverage]:
    return [assess_series(session, s) for s in specs]


def candle_count(session: Session, asset_id, timeframe: str) -> int:
    return int(
        session.execute(
            select(func.count())
            .select_from(Candle)
            .where(Candle.asset_id == asset_id, Candle.timeframe == timeframe)
        ).scalar_one()
    )
