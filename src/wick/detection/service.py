"""R2 detection orchestration — closed candles only, zero look-ahead."""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from wick.db.models import Candle, PatternConfirmation, PatternDetected
from wick.features.context import OHLCV, build_geometries, compute_all_contexts
from wick.patterns.confirmation import OFFICIAL_CONFIRMATION_RULES, evaluate_confirmation
from wick.patterns.detectors import detect_all_at_anchor
from wick.patterns.params import DEFAULT_PARAMS, DETECTOR_VERSION, DetectorParams
from wick.timeframes import timeframe_duration


@dataclass
class DetectionSummary:
    run_id: str
    patterns_inserted: int = 0
    patterns_unchanged: int = 0
    confirmations_upserted: int = 0
    candles_scanned: int = 0
    dry_run: bool = False
    notes: list[str] = field(default_factory=list)
    hits: list[dict[str, Any]] = field(default_factory=list)


def _bars_from_candles(candles: Sequence[Candle]) -> list[OHLCV]:
    return [
        OHLCV(
            open=float(c.open),
            high=float(c.high),
            low=float(c.low),
            close=float(c.close),
            volume=float(c.volume),
        )
        for c in candles
    ]


def load_closed_candles(
    session: Session,
    *,
    asset_id,
    timeframe: str,
    start: datetime | None = None,
    end: datetime | None = None,
    now_utc: datetime | None = None,
    safety_delay_seconds: int = 30,
) -> list[Candle]:
    """Load candles ordered by timestamp; filter to closed by time formula."""
    now = now_utc or datetime.now(UTC)
    stmt = (
        select(Candle)
        .where(
            Candle.asset_id == asset_id, Candle.timeframe == timeframe, Candle.is_closed.is_(True)
        )
        .order_by(Candle.timestamp.asc())
    )
    if start is not None:
        stmt = stmt.where(Candle.timestamp >= start)
    if end is not None:
        stmt = stmt.where(Candle.timestamp <= end)
    rows = list(session.execute(stmt).scalars().all())
    # Sort defensively (spec: order internally and note)
    rows.sort(key=lambda c: c.timestamp)
    duration = timeframe_duration(timeframe)
    closed: list[Candle] = []
    for c in rows:
        ts = c.timestamp if c.timestamp.tzinfo else c.timestamp.replace(tzinfo=UTC)
        if ts + duration <= now - timedelta(seconds=safety_delay_seconds):
            closed.append(c)
    return closed


class DetectionService:
    def __init__(
        self,
        session: Session,
        *,
        params: DetectorParams | None = None,
        detector_version: str = DETECTOR_VERSION,
        dry_run: bool = False,
        safety_delay_seconds: int = 30,
    ) -> None:
        self.session = session
        self.params = params or DEFAULT_PARAMS
        self.detector_version = detector_version
        self.parameters_hash = self.params.parameters_hash()
        self.dry_run = dry_run
        self.safety_delay_seconds = safety_delay_seconds

    def detect_asset_timeframe(
        self,
        *,
        asset_id,
        timeframe: str,
        start: datetime | None = None,
        end: datetime | None = None,
        incremental: bool = True,
        reprocess: bool = False,
        run_id: str | None = None,
    ) -> DetectionSummary:
        run = run_id or f"det_{uuid.uuid4().hex[:16]}"
        summary = DetectionSummary(run_id=run, dry_run=self.dry_run)

        candles = load_closed_candles(
            self.session,
            asset_id=asset_id,
            timeframe=timeframe,
            start=start,
            end=end,
            safety_delay_seconds=self.safety_delay_seconds,
        )
        if not candles:
            summary.notes.append("No closed candles in range")
            return summary

        # Incremental: skip anchors already processed for this version+hash
        start_idx = 0
        if incremental and not reprocess:
            last = self._latest_detected_anchor_ts(asset_id, timeframe)
            if last is not None:
                for i, c in enumerate(candles):
                    if c.timestamp > last:
                        start_idx = i
                        break
                else:
                    start_idx = len(candles)
                    summary.notes.append("Already up to date for this detector version/hash")

        bars = _bars_from_candles(candles)
        geoms = build_geometries(bars, self.params)
        contexts = compute_all_contexts(bars, self.params, geoms)

        for i in range(start_idx, len(candles)):
            summary.candles_scanned += 1
            hits = detect_all_at_anchor(geoms, i, self.params)
            ctx = contexts[i]
            anchor = candles[i]
            for hit in hits:
                start_candle = candles[i - hit.length + 1]
                if self.dry_run:
                    summary.hits.append(
                        {
                            "pattern_type": hit.pattern_type,
                            "signal": hit.signal,
                            "length": hit.length,
                            "anchor_ts": anchor.timestamp.isoformat(),
                            "trend_context": ctx.trend_direction,
                        }
                    )
                    continue
                inserted = self._upsert_pattern(
                    anchor=anchor,
                    start_candle=start_candle,
                    hit=hit,
                    trend_context=ctx.trend_direction,
                    context_features=ctx.to_dict(),
                    run_id=run,
                )
                if inserted:
                    summary.patterns_inserted += 1
                else:
                    summary.patterns_unchanged += 1
            if not self.dry_run and (i + 1) % 500 == 0:
                self.session.flush()

        # Confirmation pass — only for patterns whose t+1 is closed and present
        if not self.dry_run:
            summary.confirmations_upserted += self._process_confirmations(
                asset_id=asset_id,
                timeframe=timeframe,
                candles=candles,
            )
        return summary

    def _latest_detected_anchor_ts(self, asset_id, timeframe: str) -> datetime | None:
        stmt = (
            select(Candle.timestamp)
            .join(PatternDetected, PatternDetected.anchor_candle_id == Candle.id)
            .where(
                Candle.asset_id == asset_id,
                Candle.timeframe == timeframe,
                PatternDetected.detector_version == self.detector_version,
                PatternDetected.parameters_hash == self.parameters_hash,
            )
            .order_by(Candle.timestamp.desc())
            .limit(1)
        )
        return self.session.execute(stmt).scalar_one_or_none()

    def _upsert_pattern(
        self,
        *,
        anchor: Candle,
        start_candle: Candle,
        hit,
        trend_context: str,
        context_features: dict[str, Any],
        run_id: str,
    ) -> bool:
        initial_status = "NOT_APPLICABLE" if hit.pattern_type == "DOJI" else "PENDING"
        stmt = (
            insert(PatternDetected)
            .values(
                id=uuid.uuid4(),
                anchor_candle_id=anchor.id,
                start_candle_id=start_candle.id,
                pattern_length=hit.length,
                pattern_type=hit.pattern_type,
                signal=hit.signal,
                trend_context=trend_context,
                detector_version=self.detector_version,
                parameters_hash=self.parameters_hash,
                detected_at=datetime.now(UTC),
                confirmation_status=initial_status,
                context_features=context_features,
                run_id=run_id,
            )
            .on_conflict_do_nothing(constraint="uq_pattern_detected_logical")
            .returning(PatternDetected.id)
        )
        row_id = self.session.execute(stmt).scalar_one_or_none()
        return row_id is not None

    def _process_confirmations(
        self,
        *,
        asset_id,
        timeframe: str,
        candles: list[Candle],
    ) -> int:
        by_ts = {c.timestamp: c for c in candles}
        ordered_ts = sorted(by_ts)
        upserts = 0
        stmt = (
            select(PatternDetected)
            .join(Candle, Candle.id == PatternDetected.anchor_candle_id)
            .where(
                Candle.asset_id == asset_id,
                Candle.timeframe == timeframe,
                PatternDetected.detector_version == self.detector_version,
                PatternDetected.parameters_hash == self.parameters_hash,
            )
        )
        patterns = list(self.session.execute(stmt).scalars().all())
        for pat in patterns:
            anchor = self.session.get(Candle, pat.anchor_candle_id)
            if anchor is None:
                continue
            # Find t+1 among closed candles
            try:
                idx = ordered_ts.index(anchor.timestamp)
            except ValueError:
                continue
            if idx + 1 >= len(ordered_ts):
                # Confirm candle not yet available / not closed in this set
                continue
            confirm = by_ts[ordered_ts[idx + 1]]
            for rule in OFFICIAL_CONFIRMATION_RULES:
                status = evaluate_confirmation(
                    signal=pat.signal,
                    pattern_type=pat.pattern_type,
                    anchor_close=float(anchor.close),
                    anchor_high=float(anchor.high),
                    anchor_low=float(anchor.low),
                    confirm_close=float(confirm.close),
                    rule=rule,
                )
                now = datetime.now(UTC)
                cstmt = (
                    insert(PatternConfirmation)
                    .values(
                        id=uuid.uuid4(),
                        pattern_detected_id=pat.id,
                        confirmation_rule_version=rule,
                        confirmation_status=status,
                        confirmation_candle_id=confirm.id if status != "NOT_APPLICABLE" else None,
                        evaluated_at=now if status != "NOT_APPLICABLE" else None,
                    )
                    .on_conflict_do_update(
                        constraint="uq_pattern_confirmation_logical",
                        set_={
                            "confirmation_status": status,
                            "confirmation_candle_id": confirm.id
                            if status != "NOT_APPLICABLE"
                            else None,
                            "evaluated_at": now if status != "NOT_APPLICABLE" else None,
                            "updated_at": now,
                        },
                    )
                )
                self.session.execute(cstmt)
                upserts += 1
            # Mirror primary status on pattern_detected using CLOSE rule for convenience
            primary = evaluate_confirmation(
                signal=pat.signal,
                pattern_type=pat.pattern_type,
                anchor_close=float(anchor.close),
                anchor_high=float(anchor.high),
                anchor_low=float(anchor.low),
                confirm_close=float(confirm.close),
                rule=OFFICIAL_CONFIRMATION_RULES[0],
            )
            pat.confirmation_status = primary
            pat.confirmation_rule_version = OFFICIAL_CONFIRMATION_RULES[0]
            if primary in {"CONFIRMED", "NOT_CONFIRMED"}:
                pat.confirmation_candle_id = confirm.id
                pat.confirmed_at = datetime.now(UTC)
            elif primary == "NOT_APPLICABLE":
                pat.confirmation_candle_id = None
                pat.confirmed_at = None
        self.session.flush()
        return upserts
