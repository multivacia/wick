#!/usr/bin/env python3
"""R3E real-OHLCV exploratory development run.

Reuses official R3D universe bars + R2 detections. Nested walk-forward runs only
on the development portion (first 70%). The R3D holdout (final 30%) is identified
and excluded from confirmatory claims — it is NOT treated as a new final test.

Does not authorize R4/R5. Maximum gate remains PENDING_FUTURE_UNSEEN_DATA.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from sqlalchemy import select

from wick.backtest.engine import Bar
from wick.config import get_settings
from wick.db.models import Asset, Candle, PatternDetected
from wick.db.session import session_scope
from wick.detection.service import load_closed_candles
from wick.patterns.params import DEFAULT_PARAMS, DETECTOR_VERSION
from wick.r3d.universe import UNIVERSE
from wick.r3e.dataset import build_observations
from wick.r3e.pipeline import run_r3e_experiment
from wick.r3e.snapshot import build_data_snapshot, identify_r3d_holdout_intervals

OUT = Path("reports/r3e_real")


def _pattern_map(session, asset_id, timeframe: str, id_to_index: dict) -> dict[int, dict[str, str]]:
    """Map bar index -> pattern features; prefer confirmed when both exist."""
    out: dict[int, dict[str, str]] = {}
    rows = session.execute(
        select(PatternDetected)
        .join(Candle, PatternDetected.anchor_candle_id == Candle.id)
        .where(
            Candle.asset_id == asset_id,
            Candle.timeframe == timeframe,
            PatternDetected.detector_version == DETECTOR_VERSION,
            PatternDetected.parameters_hash == DEFAULT_PARAMS.parameters_hash(),
        )
    ).scalars()
    for p in rows:
        idx = id_to_index.get(p.anchor_candle_id)
        if idx is None:
            continue
        variant = "confirmed" if p.confirmation_status == "CONFIRMED" else "raw"
        existing = out.get(idx)
        if existing is None or (
            existing.get("confirmation_variant") != "confirmed" and variant == "confirmed"
        ):
            out[idx] = {
                "pattern_type": p.pattern_type,
                "signal": p.signal.lower(),
                "confirmation_variant": variant,
            }
    return out


def _load_series(session, *, safety_delay: int = 30) -> list[dict[str, Any]]:
    series: list[dict[str, Any]] = []
    for spec in UNIVERSE:
        asset = session.execute(
            select(Asset).where(Asset.symbol == spec.symbol, Asset.source == spec.source)
        ).scalar_one_or_none()
        if asset is None:
            print(f"SKIP missing asset {spec.symbol} {spec.source}", flush=True)
            continue
        candles = load_closed_candles(
            session,
            asset_id=asset.id,
            timeframe=spec.timeframe,
            safety_delay_seconds=safety_delay,
        )
        if len(candles) < 150:
            print(
                f"SKIP short series {spec.symbol} {spec.timeframe} n={len(candles)}",
                flush=True,
            )
            continue
        bars = [Bar(float(c.open), float(c.high), float(c.low), float(c.close)) for c in candles]
        vols = [float(c.volume) for c in candles]
        timestamps = [c.timestamp.isoformat() for c in candles]
        id_to_index = {c.id: i for i, c in enumerate(candles)}
        patterns = _pattern_map(session, asset.id, spec.timeframe, id_to_index)

        obs = build_observations(
            bars,
            vols,
            asset_id=spec.symbol,
            timeframe=spec.timeframe,
            pattern_at_index=patterns,
            timestamps=timestamps,
            warmup=100,
        )
        holdout_n = sum(1 for o in obs if o.in_r3d_holdout)
        print(
            f"loaded {spec.symbol} {spec.timeframe}: bars={len(bars)} "
            f"obs={len(obs)} patterns={len(patterns)} holdout_obs={holdout_n}",
            flush=True,
        )
        series.append(
            {
                "bars": bars,
                "volumes": vols,
                "observations": obs,
                "asset_id": spec.symbol,
                "timeframe": spec.timeframe,
                "source": spec.source,
                "n_bars": len(bars),
            }
        )
    return series


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    settings = get_settings()
    # Allow clean re-runs: archived frozen manifesto must not block a new freeze.
    for stale in (
        "experiment_manifest.json",
        "executive_report.json",
        "technical_report.json",
    ):
        p = OUT / stale
        if p.exists():
            bak = OUT / f"{stale}.prev"
            bak.write_bytes(p.read_bytes())
            p.unlink()

    with session_scope(settings) as session:
        snapshot = build_data_snapshot(session, out_dir=OUT)
        holdouts = identify_r3d_holdout_intervals(session)
        (OUT / "r3d_holdout_intervals.json").write_text(
            json.dumps(
                {
                    "policy": "R3D final 30% per series; confirmatory reuse forbidden",
                    "intervals": holdouts,
                },
                indent=2,
                default=str,
            )
            + "\n",
            encoding="utf-8",
        )

        identified = [h for h in holdouts if h.get("status") == "IDENTIFIED"]
        if len(identified) == 0:
            print("STOP: could not identify R3D holdout intervals", flush=True)
            return 2
        missing = [h for h in holdouts if h.get("status") != "IDENTIFIED"]
        if missing:
            print(
                f"WARN: {len(missing)} series without identified holdout; "
                f"continuing only if coverage allows",
                flush=True,
            )

        # Fail hard if any official series is missing entirely
        hard_fail = [h for h in holdouts if h.get("status") in ("MISSING_INSTRUMENT", "EMPTY")]
        if hard_fail:
            print(f"STOP: material reconstruction gaps: {hard_fail}", flush=True)
            return 3

        series = _load_series(session)

    if len(series) < 10:
        print(f"STOP: too few series loaded ({len(series)}); expected ~20", flush=True)
        return 4

    executive = run_r3e_experiment(
        series,
        OUT,
        real_data=True,
        data_origin="REAL_OHLCV_HISTORICAL",
        extra_manifest={
            "run_kind": "R3E_REAL_DATA_DEVELOPMENT",
            "data_snapshot_id": snapshot["data_snapshot_id"],
            "aggregate_hash_sha256": snapshot["aggregate_hash_sha256"],
            "provider_versions": snapshot["provider_versions"],
            "r3d_holdout_intervals_ref": "r3d_holdout_intervals.json",
            "confirmatory_use_of_r3d_holdout": False,
            "r4_authorized": False,
            "grids_thresholds_costs_seed_frozen": True,
        },
    )
    # Attach snapshot id into executive
    executive["data_snapshot_id"] = snapshot["data_snapshot_id"]
    executive["aggregate_hash_sha256"] = snapshot["aggregate_hash_sha256"]
    (OUT / "executive_report.json").write_text(
        json.dumps(executive, indent=2, default=str) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                k: executive[k]
                for k in (
                    "classification",
                    "R3E_GATE",
                    "R3E_REAL_DATA_RUN",
                    "R4_STATUS",
                    "classification_counts",
                    "n_series",
                    "n_result_rows",
                    "DATA_ORIGIN",
                )
                if k in executive
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
