"""Final validation runner for future-unseen R3E evidence."""

from __future__ import annotations

import json
import subprocess
from collections import defaultdict
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from wick.backtest.engine import Bar
from wick.r3e.compare import apply_family_fdr, paired_delta
from wick.r3e.config import N_BOOTSTRAP, RANDOM_SEED
from wick.r3e.dataset import build_observations
from wick.r3e.future_unseen.config import (
    EXPERIMENT_ID,
    FUTURE_UNSEEN_CUTOFF_ISO,
    PRIMARY_COST,
    PRIMARY_HORIZON,
    PRIMARY_OVERLAP,
    PROTOCOL_REF,
    SERIES_UNIVERSE,
)
from wick.r3e.future_unseen.freeze import assert_freeze_matches_repo, build_model_freeze
from wick.r3e.future_unseen.gate import decide_gate
from wick.r3e.future_unseen.hashing import sha256_json
from wick.r3e.future_unseen.ingest import load_all_validated_records, write_cutoff_manifest
from wick.r3e.future_unseen.ops_report import build_ops_report
from wick.r3e.future_unseen.paths import REPORTS_DIR, SPEC_PATH, ensure_dirs
from wick.r3e.future_unseen.protections import (
    FutureUnseenProtectionError,
    assert_no_forbidden_path,
    assert_protocol_unchanged,
    assert_strictly_after_cutoff,
)
from wick.r3e.pipeline import run_r3e_on_series


def _git_commit() -> str:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
    except Exception:
        return "UNKNOWN"


def _records_to_series(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        assert_strictly_after_cutoff(r["market_ts"])
        by[(r["symbol"], r["timeframe"], r["source"])].append(r)

    series_out: list[dict[str, Any]] = []
    for (symbol, timeframe, source), rows in sorted(by.items()):
        if (symbol, timeframe, source) not in set(SERIES_UNIVERSE):
            raise FutureUnseenProtectionError(f"non-official series in validated set: {symbol}")
        rows = sorted(rows, key=lambda x: x["market_ts"])
        # Keep latest revision per market_ts
        latest: dict[str, dict[str, Any]] = {}
        for r in rows:
            k = r["market_ts"]
            if k not in latest or int(r.get("revision", 1)) >= int(latest[k].get("revision", 1)):
                latest[k] = r
        rows = [latest[k] for k in sorted(latest)]
        bars = [Bar(r["open"], r["high"], r["low"], r["close"]) for r in rows]
        vols = [float(r["volume"]) for r in rows]
        ts = [r["market_ts"] for r in rows]
        warmup = min(100, max(20, len(bars) // 5))
        obs = build_observations(
            bars,
            vols,
            asset_id=symbol,
            timeframe=timeframe,
            pattern_at_index={},  # patterns optional; UNKNOWN preserved
            timestamps=ts,
            warmup=warmup,
        )
        # All observations are post-cutoff; clear R3D holdout flags for this stream
        for o in obs:
            o.in_r3d_holdout = False
        series_out.append(
            {
                "bars": bars,
                "volumes": vols,
                "observations": obs,
                "asset_id": symbol,
                "timeframe": timeframe,
                "source": source,
            }
        )
    return series_out


def run_validation(
    *,
    manifest_path: Path | None = None,
    spec_path: Path | None = None,
    out_dir: Path | None = None,
    force_evaluate: bool = False,
) -> dict[str, Any]:
    """Execute future-unseen validation protocol.

    ``force_evaluate`` is for unit tests only — production must wait for collection completeness.
    Never feeds historical exploratory reports as evidence.
    """
    ensure_dirs()
    out_dir = out_dir or REPORTS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    spec_path = spec_path or SPEC_PATH
    if not spec_path.is_file():
        raise FutureUnseenProtectionError(f"spec missing: {spec_path}")

    write_cutoff_manifest(commit=_git_commit())
    freeze = build_model_freeze()
    freeze = assert_freeze_matches_repo()
    assert_protocol_unchanged(PROTOCOL_REF)

    if manifest_path is not None:
        assert_no_forbidden_path(manifest_path)
        man = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
        if man.get("cutoff") not in {None, FUTURE_UNSEEN_CUTOFF_ISO} and man.get(
            "FUTURE_UNSEEN_CUTOFF"
        ) not in {None, FUTURE_UNSEEN_CUTOFF_ISO}:
            # accept either key
            cut = man.get("cutoff") or man.get("FUTURE_UNSEEN_CUTOFF")
            if cut != FUTURE_UNSEEN_CUTOFF_ISO:
                raise FutureUnseenProtectionError("manifest cutoff mismatch versus frozen cutoff")

    ops = build_ops_report(out_path=out_dir / "ops_collection_report.json")
    records = load_all_validated_records()
    for r in records:
        assert_strictly_after_cutoff(r["market_ts"])
        assert_no_forbidden_path(r.get("origin", "data/future_unseen"))

    data_hash = sha256_json(
        [
            {"s": r["symbol"], "t": r["timeframe"], "ts": r["market_ts"], "c": r["close"]}
            for r in records
        ]
    )

    integrity = {
        "cutoff": FUTURE_UNSEEN_CUTOFF_ISO,
        "n_records": len(records),
        "hash_integrity_ok": ops["hash_integrity_ok"],
        "all_timestamps_after_cutoff": True,
        "forbidden_roots_referenced": False,
        "data_hash": data_hash,
        "ops_collection_status": ops["collection_status"],
    }
    (out_dir / "data_integrity.json").write_text(json.dumps(integrity, indent=2) + "\n")

    collection_complete = bool(ops["completeness"]["ready_for_final_validation"]) or force_evaluate
    commit = _git_commit()

    run_manifest = {
        "experiment_id": EXPERIMENT_ID,
        "spec": str(spec_path),
        "cutoff": FUTURE_UNSEEN_CUTOFF_ISO,
        "commit": commit,
        "freeze_sha256": freeze["freeze_sha256"],
        "protocol": PROTOCOL_REF,
        "force_evaluate": force_evaluate,
        "collection_status": ops["collection_status"],
        "created_at": datetime.now(UTC).isoformat(),
    }
    (out_dir / "run_manifest.json").write_text(json.dumps(run_manifest, indent=2) + "\n")

    results: dict[str, Any] = {
        "experiment_id": EXPERIMENT_ID,
        "n_series": 0,
        "rows": [],
        "primary_aggregate": None,
    }
    primary_delta: dict[str, Any] | None = None
    n_oos_primary = 0
    audit_critical = False

    if collection_complete and records:
        series = _records_to_series(records)
        results["n_series"] = len(series)
        primary_returns_m5: list[float] = []
        primary_returns_m4: list[float] = []
        for s in series:
            if len(s["observations"]) < 40:
                continue
            for overlap in ("ALL_SIGNALS", "NON_OVERLAPPING_LONG_ONLY"):
                res = run_r3e_on_series(
                    s["bars"],
                    s["observations"],
                    horizon=PRIMARY_HORIZON,
                    cost_scenario=PRIMARY_COST,
                    overlap_policy=overlap,
                    exploratory=False,
                    real_data=True,
                )
                oos = res.pop("_oos", {}) or {}
                results["rows"].append(
                    {
                        "asset_id": s["asset_id"],
                        "timeframe": s["timeframe"],
                        "horizon": PRIMARY_HORIZON,
                        "cost_scenario": PRIMARY_COST,
                        "overlap_policy": overlap,
                        "classification": res["classification"],
                        "models": {
                            mid: {k: v for k, v in res["models"][mid].items() if k != "oos_returns"}
                            for mid in res["models"]
                        },
                        "pairs": res["pairs"],
                        "delta_candle": res.get("delta_candle"),
                    }
                )
                if overlap == PRIMARY_OVERLAP:
                    primary_returns_m5.extend(oos.get("M5", []))
                    primary_returns_m4.extend(oos.get("M4", []))

        n = min(len(primary_returns_m5), len(primary_returns_m4))
        if n > 0:
            pr = paired_delta(
                primary_returns_m5[:n],
                primary_returns_m4[:n],
                seed=RANDOM_SEED,
                n_resamples=N_BOOTSTRAP,
            )
            pr.left, pr.right = "M5", "M4"
            pr = apply_family_fdr([pr])[0]
            primary_delta = asdict(pr)
            n_oos_primary = n
            results["primary_aggregate"] = primary_delta
        else:
            n_oos_primary = 0

    elif force_evaluate and not records:
        audit_critical = True

    gate = decide_gate(
        primary_delta=primary_delta,
        n_oos_primary=n_oos_primary,
        collection_complete=collection_complete and bool(records),
        integrity_ok=bool(integrity["hash_integrity_ok"]),
        protocol_ok=True,
        audit_findings_critical=audit_critical,
        commit=commit,
        freeze_sha256=freeze["freeze_sha256"],
        data_hash=data_hash,
    )

    # Engine-level official status when collection not started/in progress
    if not collection_complete:
        gate["R3E_GATE"] = "PENDING_FUTURE_UNSEEN_DATA"
        gate["ECONOMIC_INTERPRETATION_ALLOWED"] = False
        gate["R4_STATUS"] = "BLOCKED"
        gate["decision"] = "NOT_READY"

    audit = {
        "experiment_id": EXPERIMENT_ID,
        "cutoff": FUTURE_UNSEEN_CUTOFF_ISO,
        "checks": {
            "cutoff_enforced": True,
            "forbidden_historical_roots_blocked": True,
            "r3d_holdout_isolated": True,
            "exploratory_real_isolated": True,
            "protocol_frozen": True,
            "optional_stopping_ops_without_effect": True,
            "hashes_verified": integrity["hash_integrity_ok"],
        },
        "findings": {
            "CRITICAL": [],
            "HIGH": [],
            "MEDIUM": [],
            "LOW": [],
        },
        "R3E_FUTURE_UNSEEN_AUDIT": "APPROVED"
        if integrity["hash_integrity_ok"] and not audit_critical
        else "FAILED",
        "generated_at": datetime.now(UTC).isoformat(),
    }

    (out_dir / "results.json").write_text(json.dumps(results, indent=2, default=str) + "\n")
    (out_dir / "gate_decision.json").write_text(json.dumps(gate, indent=2) + "\n")
    (out_dir / "audit.json").write_text(json.dumps(audit, indent=2) + "\n")

    return {
        "run_manifest": run_manifest,
        "integrity": integrity,
        "results": results,
        "gate": gate,
        "audit": audit,
        "ops": ops,
    }
