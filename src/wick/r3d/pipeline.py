"""R3D pipeline: detect → freeze manifest → validate → report (no recalibration)."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from wick.backtest.costs import get_scenario
from wick.backtest.engine import Bar, evaluate_signal
from wick.db.models import Asset, Candle, PatternDetected
from wick.detection.service import DetectionService, load_closed_candles
from wick.patterns.params import DEFAULT_PARAMS, DETECTOR_VERSION
from wick.quant.experiments import (
    SignalEvent,
    apply_fdr_across_reports,
    non_overlapping_events,
    run_strategy_validation,
    write_reports,
)
from wick.r3d.coverage import SeriesCoverage, assess_universe
from wick.r3d.manifest import ExperimentVariant, build_variants, mark_holdout_opened, write_manifest
from wick.r3d.universe import N_BOOTSTRAP, SEED, UNIVERSE
from wick.r3d.vectorbt_compare import TradePoint, compare_trade_sets, vectorbt_net_returns


def run_detection_all(session: Session, *, safety_delay: int = 30) -> list[dict[str, Any]]:
    svc = DetectionService(
        session,
        detector_version=DETECTOR_VERSION,
        params=DEFAULT_PARAMS,
        dry_run=False,
        safety_delay_seconds=safety_delay,
    )
    summaries: list[dict[str, Any]] = []
    for spec in UNIVERSE:
        asset = session.execute(
            select(Asset).where(Asset.symbol == spec.symbol, Asset.source == spec.source)
        ).scalar_one_or_none()
        if asset is None:
            summaries.append(
                {
                    "symbol": spec.symbol,
                    "source": spec.source,
                    "timeframe": spec.timeframe,
                    "error": "asset missing",
                }
            )
            continue
        summary = svc.detect_asset_timeframe(
            asset_id=asset.id,
            timeframe=spec.timeframe,
            incremental=False,
            reprocess=True,
        )
        summaries.append(
            {
                "symbol": spec.symbol,
                "source": spec.source,
                "timeframe": spec.timeframe,
                "candles_scanned": summary.candles_scanned,
                "patterns_inserted": summary.patterns_inserted,
                "patterns_unchanged": summary.patterns_unchanged,
                "confirmations": summary.confirmations_upserted,
                "run_id": summary.run_id,
                "notes": summary.notes,
            }
        )
    return summaries


def _load_bars_and_index(
    session: Session, asset_id, timeframe: str, safety_delay: int
) -> tuple[list[Bar], list[Candle], dict[Any, int]]:
    candles = load_closed_candles(
        session,
        asset_id=asset_id,
        timeframe=timeframe,
        safety_delay_seconds=safety_delay,
    )
    bars = [Bar(float(c.open), float(c.high), float(c.low), float(c.close)) for c in candles]
    idx = {c.id: i for i, c in enumerate(candles)}
    return bars, candles, idx


def _load_patterns_for_series(
    session: Session,
    *,
    asset_id: Any,
    timeframe: str,
) -> list[PatternDetected]:
    return list(
        session.execute(
            select(PatternDetected)
            .join(Candle, PatternDetected.anchor_candle_id == Candle.id)
            .where(
                Candle.asset_id == asset_id,
                Candle.timeframe == timeframe,
                PatternDetected.detector_version == DETECTOR_VERSION,
                PatternDetected.parameters_hash == DEFAULT_PARAMS.parameters_hash(),
            )
        ).scalars()
    )


def _pattern_events_from_rows(
    rows: list[PatternDetected],
    *,
    id_to_index: dict[Any, int],
    pattern_type: str,
    confirmation_used: bool,
) -> list[SignalEvent]:
    events: list[SignalEvent] = []
    for p in rows:
        if p.pattern_type != pattern_type:
            continue
        if p.anchor_candle_id not in id_to_index:
            continue
        if confirmation_used and p.confirmation_status != "CONFIRMED":
            continue
        if p.signal.lower() != "bullish":
            continue
        events.append(
            SignalEvent(
                pattern_index=id_to_index[p.anchor_candle_id],
                signal=p.signal.lower(),
                pattern_type=p.pattern_type,
                confirmation_used=confirmation_used,
            )
        )
    return events


def validate_series(
    session: Session,
    *,
    coverage: SeriesCoverage,
    variants: list[ExperimentVariant],
    safety_delay: int = 30,
) -> dict[str, Any]:
    if coverage.asset_id is None or coverage.coverage_status == "MISSING":
        return {
            "series": coverage.to_dict(),
            "reports": [],
            "pattern_counts": {},
            "vectorbt": [],
            "skipped": True,
        }

    asset_id = coverage.asset_id
    bars, candles, id_to_index = _load_bars_and_index(
        session, asset_id, coverage.timeframe, safety_delay
    )
    pattern_rows = _load_patterns_for_series(
        session, asset_id=asset_id, timeframe=coverage.timeframe
    )
    pattern_counts = dict(Counter(r.pattern_type for r in pattern_rows))

    reports = []
    vbt_results = []
    # Concentration helpers
    month_hits: Counter[str] = Counter()

    for variant in variants:
        events = _pattern_events_from_rows(
            pattern_rows,
            id_to_index=id_to_index,
            pattern_type=variant.pattern_type,
            confirmation_used=variant.confirmation_used,
        )
        for ev in events:
            ts = candles[ev.pattern_index].timestamp
            month_hits[ts.strftime("%Y-%m")] += 1

        report = run_strategy_validation(
            bars,
            events,
            strategy_id=f"{coverage.symbol}|{coverage.timeframe}|{variant.strategy_id}",
            description=(
                f"{coverage.symbol} {coverage.timeframe} {variant.pattern_type} "
                f"N={variant.horizon} conf={variant.confirmation_used} {variant.cost_scenario}"
            ),
            horizon=variant.horizon,
            cost_scenario=variant.cost_scenario,
            seed=SEED,
            n_resamples=N_BOOTSTRAP,
            executable_no_overlap=True,
        )
        reports.append(report)

        # vectorbt complementary check on non-overlapping train-evaluable trades
        use_events = non_overlapping_events(events, variant.horizon)
        own_points: list[TradePoint] = []
        entry_idxs: list[int] = []
        exit_idxs: list[int] = []
        for ev in use_events[:200]:  # cap compare sample for runtime
            r = evaluate_signal(
                bars,
                pattern_index=ev.pattern_index,
                signal=ev.signal,
                pattern_type=ev.pattern_type,
                horizon=variant.horizon,
                confirmation_used=ev.confirmation_used,
                cost_scenario=variant.cost_scenario,
            )
            if (
                r.status != "OK"
                or r.net_return is None
                or r.entry_index is None
                or r.exit_index is None
            ):
                continue
            own_points.append(
                TradePoint(
                    entry_index=r.entry_index,
                    exit_index=r.exit_index,
                    entry_ts=candles[r.entry_index].timestamp.isoformat(),
                    exit_ts=candles[r.exit_index].timestamp.isoformat(),
                    net_return=r.net_return,
                )
            )
            entry_idxs.append(r.entry_index)
            exit_idxs.append(r.exit_index)
        opens = [b.open for b in bars]
        closes = [b.close for b in bars]
        cost = get_scenario(variant.cost_scenario).total_cost
        vbt_rets = vectorbt_net_returns(opens, closes, entry_idxs, exit_idxs, cost)
        cmp = compare_trade_sets(
            own_points,
            vbt_rets,
            vbt_entry_indices=entry_idxs,
            vbt_exit_indices=exit_idxs,
            vbt_entry_ts=[p.entry_ts for p in own_points],
            vbt_exit_ts=[p.exit_ts for p in own_points],
        )
        if not cmp.ok:
            vbt_results.append({"strategy": report.strategy_id, **asdict(cmp)})

    reports = apply_fdr_across_reports(reports)
    if coverage.coverage_status != "COMPLETE":
        for report in reports:
            if report.mechanical_gate == "PASSES_ALL_MECHANICAL_CRITERIA":
                report.mechanical_gate = "REQUIRES_HUMAN_REVIEW"
                report.notes.append("coverage_not_COMPLETE")
    return {
        "series": coverage.to_dict(),
        "n_bars": len(bars),
        "pattern_counts": pattern_counts,
        "reports": [r.to_dict() for r in reports],
        "vectorbt_failures": vbt_results,
        "temporal_concentration": dict(month_hits.most_common(24)),
        "skipped": False,
    }


def summarize_gate(all_series_results: list[dict[str, Any]]) -> dict[str, Any]:
    passed, failed, inconclusive, review = [], [], [], []
    by_asset: dict[str, Counter[str]] = defaultdict(Counter)
    for series_res in all_series_results:
        if series_res.get("skipped"):
            continue
        sym = series_res["series"]["symbol"]
        for r in series_res["reports"]:
            gate = r["mechanical_gate"]
            sid = r["strategy_id"]
            by_asset[sym][gate] += 1
            item = {
                "strategy_id": sid,
                "classification": r["classification"],
                "mechanical_gate": gate,
                "n_signals": r["n_signals"],
                "sample_tier": r["sample_tier"],
                "mean_net_train": r["mean_net_train"],
                "mean_net_holdout": r["mean_net_holdout"],
                "cost_scenario": r["cost_scenario"],
                "coverage_status": series_res["series"]["coverage_status"],
            }
            if gate == "PASSES_ALL_MECHANICAL_CRITERIA":
                passed.append(item)
            elif gate == "FAILS_CRITERIA":
                failed.append(item)
            elif gate == "REQUIRES_HUMAN_REVIEW":
                review.append(item)
            else:
                inconclusive.append(item)
    return {
        "passed": passed,
        "failed": failed,
        "inconclusive": inconclusive,
        "requires_human_review": review,
        "concentration_by_asset_gate": {k: dict(v) for k, v in by_asset.items()},
        "counts": {
            "passed": len(passed),
            "failed": len(failed),
            "inconclusive": len(inconclusive),
            "requires_human_review": len(review),
        },
    }


def run_r3d(
    session: Session,
    out_dir: Path,
    *,
    safety_delay: int = 30,
    skip_detection: bool = False,
) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    detection = [] if skip_detection else run_detection_all(session, safety_delay=safety_delay)
    (out_dir / "detection_summary.json").write_text(
        json.dumps(detection, indent=2) + "\n", encoding="utf-8"
    )

    coverage = assess_universe(session, UNIVERSE)
    cov_dicts = [c.to_dict() for c in coverage]
    (out_dir / "coverage_report.json").write_text(
        json.dumps(cov_dicts, indent=2) + "\n", encoding="utf-8"
    )

    manifest_path = out_dir / "experiment_manifest.json"
    write_manifest(manifest_path, coverage=cov_dicts)
    variants = build_variants()

    # Freeze complete — open holdout exactly once via validation runner
    mark_holdout_opened(manifest_path)

    series_results = []
    for cov in coverage:
        series_results.append(
            validate_series(session, coverage=cov, variants=variants, safety_delay=safety_delay)
        )

    gate_summary = summarize_gate(series_results)
    technical = {
        "generated_at": datetime.now(UTC).isoformat(),
        "detector_version": DETECTOR_VERSION,
        "parameters_hash": DEFAULT_PARAMS.parameters_hash(),
        "coverage": cov_dicts,
        "detection": detection,
        "series_results": series_results,
        "gate_summary": gate_summary,
    }
    (out_dir / "technical_report.json").write_text(
        json.dumps(technical, indent=2, default=str) + "\n", encoding="utf-8"
    )

    # Flatten reports for write_reports compatibility / executive view
    flat_reports = []
    from wick.quant.experiments import StrategyReport

    # Executive already built from gate_summary + coverage
    executive = {
        "generated_at": datetime.now(UTC).isoformat(),
        "R3D_IMPLEMENTATION": "COMPLETE",
        "R3D_AUDIT": "PENDING",
        "R3_GATE": "PENDING_HUMAN_DECISION",
        "R4_STATUS": "BLOCKED_NO_REAL_STRATEGY_APPROVED",
        "coverage_status_counts": dict(Counter(c["coverage_status"] for c in cov_dicts)),
        "gate_counts": gate_summary["counts"],
        "passed": gate_summary["passed"],
        "failed_sample": gate_summary["failed"][:50],
        "inconclusive_sample": gate_summary["inconclusive"][:50],
        "failed_total": len(gate_summary["failed"]),
        "inconclusive_total": len(gate_summary["inconclusive"]),
        "concentration_by_asset": gate_summary["concentration_by_asset_gate"],
        "limitations": [
            "COST_MODEL_VERSION=1.0.0-provisional",
            "Equity 1h limited by Yahoo lookback",
            "PARTIAL series excluded from promotion claims",
            "vectorbt complementary = independent formula oracle (package optional)",
        ],
        "recommendation_r4": (
            "Do not start R4 unless human selects strategies from passed list "
            "after reviewing provisional costs and real-data limitations."
        ),
    }
    (out_dir / "executive_report.json").write_text(
        json.dumps(executive, indent=2) + "\n", encoding="utf-8"
    )
    _ = (flat_reports, StrategyReport, write_reports)
    return executive
