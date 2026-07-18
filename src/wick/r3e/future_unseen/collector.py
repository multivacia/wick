"""Official incremental collector for future-unseen OHLCV.

Acquisition → normalization → eligibility → persistence → ops report.
Does not import validate/gate/models/effect metrics.
"""

from __future__ import annotations

import json
import subprocess
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from wick.ingestion.gaps import detect_gaps
from wick.ingestion.providers import get_provider
from wick.ingestion.providers.base import MarketDataProvider
from wick.ingestion.providers.retry import retry_call
from wick.ingestion.validators import RawCandle, filter_closed_candles, validate_ohlcv
from wick.r3d.universe import UNIVERSE, SeriesSpec
from wick.r3e.future_unseen.config import (
    EXPERIMENT_ID,
    FUTURE_UNSEEN_CUTOFF_ISO,
    SERIES_UNIVERSE,
)
from wick.r3e.future_unseen.discovery import compute_fetch_window, last_accepted_by_series
from wick.r3e.future_unseen.hashing import sha256_json
from wick.r3e.future_unseen.ingest import ingest_batch, load_all_validated_records
from wick.r3e.future_unseen.ops_report import build_ops_report
from wick.r3e.future_unseen.paths import MANIFESTS_DIR, REPO_ROOT, REPORTS_DIR, ensure_dirs
from wick.r3e.future_unseen.protections import (
    FutureUnseenProtectionError,
    assert_strictly_after_cutoff,
)
from wick.r3e.operational_backfill.mapping import build_provider_mapping

COLLECTOR_VERSION = "0.1.0"
DEFAULT_MAX_RETRIES = 3
DEFAULT_SAFETY_DELAY = 30
DEFAULT_REVISION_OVERLAP = 1

FORBIDDEN_COLLECTOR_IMPORTS = (
    "wick.r3e.future_unseen.validate",
    "wick.r3e.future_unseen.gate",
    "wick.r3e.pipeline",
    "wick.r3e.compare",
)

FORBIDDEN_REPORT_KEYS = frozenset(
    {
        "delta",
        "m5_minus_m4",
        "delta_candle",
        "p_value",
        "p_adj",
        "fdr",
        "economic",
        "pnl",
        "sharpe",
        "gate_decision",
        "approved",
        "rejected",
        "mean_net",
        "hit_rate",
    }
)

ProviderFactory = Callable[[str], MarketDataProvider]
SleepFn = Callable[[float], None]


def _git_commit() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "UNKNOWN"


def _candle_to_record(
    candle: RawCandle, *, symbol: str, timeframe: str, source: str
) -> dict[str, Any]:
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "source": source,
        "market_ts": candle.timestamp.astimezone(UTC).isoformat(),
        "open": float(candle.open),
        "high": float(candle.high),
        "low": float(candle.low),
        "close": float(candle.close),
        "volume": float(candle.volume),
        "revision": 1,
    }


def _classify_gap(
    *,
    asset_class: str,
    severity: str,
    note: str,
) -> str:
    text = (note or "").lower()
    if "weekend" in text or "session" in text or "holiday" in text or "overnight" in text:
        return "EXPECTED_MARKET_CLOSURE"
    if asset_class == "crypto" and severity == "alert":
        return "PROVIDER_MISSING_DATA"
    if severity == "info":
        return "UNEXPLAINED_GAP"
    return "UNEXPLAINED_GAP"


def _assert_report_clean(doc: dict[str, Any]) -> None:
    def walk(obj: Any) -> set[str]:
        keys: set[str] = set()
        if isinstance(obj, dict):
            for k, v in obj.items():
                keys.add(str(k).lower())
                keys |= walk(v)
        elif isinstance(obj, list):
            for item in obj:
                keys |= walk(item)
        return keys

    leaked = walk(doc) & FORBIDDEN_REPORT_KEYS
    # Allow operational rejection reason codes that contain "rejected" only as values, not keys.
    # Keys like "rejected" / "approved" are forbidden as report field names.
    if leaked:
        raise RuntimeError(f"forbidden scientific keys in collector report: {sorted(leaked)}")


def collect_series(
    spec: SeriesSpec,
    *,
    provider: MarketDataProvider,
    last_accepted: datetime | None,
    now_utc: datetime,
    max_retries: int = DEFAULT_MAX_RETRIES,
    safety_delay_seconds: int = DEFAULT_SAFETY_DELAY,
    revision_overlap_bars: int = DEFAULT_REVISION_OVERLAP,
    sleep_fn: SleepFn | None = None,
) -> dict[str, Any]:
    """Fetch and filter one series; never raises for provider failures."""
    import time as _time

    sleep = sleep_fn or _time.sleep
    window = compute_fetch_window(
        symbol=spec.symbol,
        timeframe=spec.timeframe,
        source=spec.source,
        now_utc=now_utc,
        last_accepted=last_accepted,
        safety_delay_seconds=safety_delay_seconds,
        revision_overlap_bars=revision_overlap_bars,
    )
    series_key = window["series_key"]
    status = {
        "series_key": series_key,
        "symbol": spec.symbol,
        "timeframe": spec.timeframe,
        "source": spec.source,
        "asset_class": spec.asset_class,
        "status": "SUCCESS",
        "last_market_ts_accepted_before": window["last_accepted"],
        "requested_start": window["requested_start"].isoformat(),
        "requested_end": window["requested_end"].isoformat(),
        "first_returned_ts": None,
        "last_returned_ts": None,
        "n_returned": 0,
        "n_eligible": 0,
        "n_accepted_candidates": 0,
        "n_rejected": 0,
        "rejection_reasons": [],
        "retries": 0,
        "provider_error": None,
        "gaps": [],
        "last_closed_candle_boundary": window["last_closed_candle_boundary"],
        "decision_rule": window["decision_rule"],
        "mode": window["mode"],
    }
    records: list[dict[str, Any]] = []
    rejections: list[dict[str, Any]] = []

    if window["no_new_closed_possible"]:
        status["status"] = "NO_NEW_CLOSED_CANDLES"
        return {"status": status, "records": records, "rejections": rejections}

    def _fetch() -> Any:
        return provider.fetch_ohlcv(
            spec.symbol,
            spec.timeframe,
            window["requested_start"],
            window["requested_end"],
        )

    try:
        result, retries = retry_call(
            _fetch,
            max_retries=max_retries,
            base_seconds=0.5,
            sleep_fn=sleep,
        )
        status["retries"] = retries
    except Exception as exc:  # noqa: BLE001 — isolate series
        status["status"] = "PROVIDER_ERROR"
        status["provider_error"] = f"{type(exc).__name__}: {exc}"
        return {"status": status, "records": records, "rejections": rejections}

    candles = list(result.candles)
    status["n_returned"] = len(candles)
    if candles:
        status["first_returned_ts"] = min(c.timestamp for c in candles).astimezone(UTC).isoformat()
        status["last_returned_ts"] = max(c.timestamp for c in candles).astimezone(UTC).isoformat()

    closed, opened = filter_closed_candles(
        candles,
        spec.timeframe,
        now_utc=now_utc,
        safety_delay_seconds=safety_delay_seconds,
    )
    for c in opened:
        rejections.append(
            {
                "series": series_key,
                "reason": "CANDLE_NOT_CLOSED",
                "market_ts": c.timestamp.astimezone(UTC).isoformat(),
            }
        )

    eligible_ts: list[datetime] = []
    for candle in closed:
        v = validate_ohlcv(candle)
        if not v.ok:
            rejections.append(
                {
                    "series": series_key,
                    "reason": f"SCHEMA_ERROR:{v.reason}",
                    "market_ts": candle.timestamp.astimezone(UTC).isoformat(),
                }
            )
            continue
        try:
            ts = assert_strictly_after_cutoff(candle.timestamp)
        except FutureUnseenProtectionError:
            rejections.append(
                {
                    "series": series_key,
                    "reason": "NOT_STRICTLY_AFTER_FUTURE_UNSEEN_CUTOFF",
                    "market_ts": candle.timestamp.astimezone(UTC).isoformat(),
                }
            )
            continue
        # Skip bars already covered without overlap intent (before last_accepted)
        if last_accepted is not None and ts < last_accepted:
            rejections.append(
                {
                    "series": series_key,
                    "reason": "BEFORE_LAST_ACCEPTED_OUTSIDE_OVERLAP",
                    "market_ts": ts.isoformat(),
                }
            )
            continue
        records.append(
            _candle_to_record(
                candle, symbol=spec.symbol, timeframe=spec.timeframe, source=spec.source
            )
        )
        eligible_ts.append(ts)

    status["n_eligible"] = len(records)
    status["n_accepted_candidates"] = len(records)
    status["n_rejected"] = len(rejections)
    status["rejection_reasons"] = sorted({r["reason"] for r in rejections})

    gaps = detect_gaps(
        eligible_ts,
        asset_symbol=spec.symbol,
        timeframe=spec.timeframe,
        asset_type=spec.asset_class,
    )
    status["gaps"] = [
        {
            "series": series_key,
            "class": _classify_gap(asset_class=spec.asset_class, severity=g.severity, note=g.note),
            "gap_start": g.gap_start.isoformat(),
            "gap_end": g.gap_end.isoformat(),
            "expected_bars": g.expected_bars,
            "severity": g.severity,
            "note": g.note,
        }
        for g in gaps
    ]

    if not records and not rejections and status["n_returned"] == 0 or not records and rejections:
        status["status"] = "NO_NEW_CLOSED_CANDLES"
    elif status["gaps"]:
        status["status"] = "PARTIAL" if records else status["status"]
    return {"status": status, "records": records, "rejections": rejections}


def run_collect(
    *,
    dry_run: bool = False,
    series_filter: str | None = None,
    provider_filter: str | None = None,
    as_of: datetime | None = None,
    max_retries: int = DEFAULT_MAX_RETRIES,
    provider_factory: ProviderFactory | None = None,
    sleep_fn: SleepFn | None = None,
    output_report_dir: Path | None = None,
) -> dict[str, Any]:
    """Run incremental collection across the frozen universe."""
    ensure_dirs()
    now_utc = as_of.astimezone(UTC) if as_of else datetime.now(UTC)
    if as_of is not None and as_of.tzinfo is None:
        raise ValueError("--as-of must be timezone-aware")

    # as-of cannot make historical timestamps eligible; cutoff policy still applied.
    collection_run_id = f"fu_collect_{now_utc.strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}"
    commit = _git_commit()
    mapping = build_provider_mapping()
    mapping_by_key = {row["series_key"]: row for row in mapping["series"]}

    before_records = load_all_validated_records()
    last_map = last_accepted_by_series(before_records)
    n_before = len(before_records)

    factory = provider_factory or get_provider
    providers: dict[str, MarketDataProvider] = {}

    series_results: list[dict[str, Any]] = []
    all_records: list[dict[str, Any]] = []
    all_rejections: list[dict[str, Any]] = []
    all_gaps: list[dict[str, Any]] = []

    universe = list(UNIVERSE)
    if series_filter:
        universe = [s for s in universe if s.symbol == series_filter]
        if not universe:
            raise ValueError(f"series filter {series_filter!r} matches no frozen universe series")
    if provider_filter:
        universe = [s for s in universe if s.source == provider_filter]
        if not universe:
            raise ValueError(
                f"provider filter {provider_filter!r} matches no frozen universe series"
            )

    for spec in universe:
        sk = f"{spec.source}|{spec.symbol}|{spec.timeframe}"
        row = mapping_by_key.get(sk)
        if row is None or not row.get("located"):
            series_results.append(
                {
                    "status": {
                        "series_key": sk,
                        "status": "MAPPING_ERROR",
                        "provider_error": "missing provider mapping",
                        "n_accepted_candidates": 0,
                        "n_rejected": 0,
                        "gaps": [],
                    },
                    "records": [],
                    "rejections": [
                        {
                            "series": sk,
                            "reason": "MAPPING_ERROR",
                            "market_ts": None,
                        }
                    ],
                }
            )
            continue
        if spec.source not in providers:
            try:
                providers[spec.source] = factory(spec.source)
            except Exception as exc:  # noqa: BLE001
                series_results.append(
                    {
                        "status": {
                            "series_key": sk,
                            "status": "PROVIDER_ERROR",
                            "provider_error": str(exc),
                            "n_accepted_candidates": 0,
                            "n_rejected": 0,
                            "gaps": [],
                        },
                        "records": [],
                        "rejections": [],
                    }
                )
                continue
        out = collect_series(
            spec,
            provider=providers[spec.source],
            last_accepted=last_map.get(sk),
            now_utc=now_utc,
            max_retries=max_retries,
            sleep_fn=sleep_fn,
        )
        series_results.append(out)
        all_records.extend(out["records"])
        all_rejections.extend(out["rejections"])
        all_gaps.extend(out["status"].get("gaps") or [])

    persist: dict[str, Any] | None = None
    if dry_run:
        persist = {
            "dry_run": True,
            "would_accept_candidates": len(all_records),
            "written": False,
            "batch_id": None,
        }
    else:
        if all_records:
            try:
                batch = ingest_batch(
                    all_records,
                    origin="future-unseen-incremental-collect",
                    batch_id=collection_run_id,
                )
                persist = {
                    "dry_run": False,
                    "written": True,
                    "batch_id": batch.batch_id,
                    "n_accepted": batch.accepted,
                    "n_store_rejected": batch.rejected,
                    "duplicates_in_batch_rejections": sum(
                        1 for r in batch.rejections if "duplicate" in r.reason.lower()
                    ),
                    "file_sha256": batch.file_sha256,
                    "batch_sha256": batch.batch_sha256,
                    "raw_path": batch.raw_path,
                    "validated_path": batch.validated_path,
                    "manifest_path": batch.manifest_path,
                    "store_rejection_reasons": [r.reason for r in batch.rejections],
                }
                # Merge store-level rejections into audit list
                for r in batch.rejections:
                    all_rejections.append(
                        {
                            "series": (
                                f"{r.record.get('source')}|{r.record.get('symbol')}|"
                                f"{r.record.get('timeframe')}"
                                if r.record
                                else None
                            ),
                            "reason": r.reason,
                            "market_ts": r.record.get("market_ts") if r.record else None,
                            "stage": "store",
                        }
                    )
            except Exception as exc:  # noqa: BLE001
                persist = {
                    "dry_run": False,
                    "written": False,
                    "status": "PERSISTENCE_ERROR",
                    "error": f"{type(exc).__name__}: {exc}",
                }
        else:
            persist = {
                "dry_run": False,
                "written": False,
                "batch_id": None,
                "n_accepted": 0,
                "n_store_rejected": 0,
                "note": "no eligible closed candidates",
            }

    after_records = before_records if dry_run else load_all_validated_records()
    n_after = len(after_records)
    ops = build_ops_report(out_path=REPORTS_DIR / "ops_collection_report.json")

    # Overlay formal lifecycle + validation flags
    state_path = MANIFESTS_DIR / "collection_state.json"
    formal = "IN_PROGRESS"
    if state_path.exists():
        prev = json.loads(state_path.read_text(encoding="utf-8"))
        formal = prev.get("R3E_FUTURE_DATA_COLLECTION", formal)
        # Keep scientific locks
        prev.update(
            {
                "R3E_GATE": "PENDING_FUTURE_UNSEEN_DATA",
                "ECONOMIC_INTERPRETATION_ALLOWED": False,
                "R4_STATUS": "BLOCKED",
                "R5_STATUS": "NOT_STARTED",
                "validation_command_executed": False,
                "effect_peeking_performed": False,
                "validation_status": "NOT_RUN",
                "updated_at": datetime.now(UTC).isoformat(),
            }
        )
        if not dry_run:
            state_path.write_text(json.dumps(prev, indent=2) + "\n", encoding="utf-8")

    statuses = [r["status"]["status"] for r in series_results]
    if any(s in {"PROVIDER_ERROR", "MAPPING_ERROR", "PERSISTENCE_ERROR"} for s in statuses):
        if any(r["records"] for r in series_results) or (persist or {}).get("n_accepted", 0) > 0:
            run_status = "PARTIAL"
        elif all(s in {"PROVIDER_ERROR", "MAPPING_ERROR", "PERSISTENCE_ERROR"} for s in statuses):
            run_status = "FAILED"
        else:
            run_status = "PARTIAL"
    elif persist and persist.get("status") == "PERSISTENCE_ERROR":
        run_status = "FAILED"
    else:
        run_status = "COMPLETE"

    series_status = [r["status"] for r in series_results]
    run_doc = {
        "kind": "FUTURE_UNSEEN_COLLECTION_RUN",
        "collection_run_id": collection_run_id,
        "experiment_id": EXPERIMENT_ID,
        "collector_version": COLLECTOR_VERSION,
        "cutoff": FUTURE_UNSEEN_CUTOFF_ISO,
        "collection_run_at": now_utc.isoformat(),
        "commit": commit,
        "dry_run": dry_run,
        "run_status": run_status,
        "n_series": len(series_status),
        "n_observations_before": n_before,
        "n_observations_after": n_after,
        "n_candidate_records": len(all_records),
        "persist": persist,
        "formal_collection_state": formal,
        "data_driven_status": ops.get("collection_status"),
        "validation_status": "NOT_RUN",
        "validate_executed": False,
        "effect_peeking_performed": False,
        "R3E_GATE": "PENDING_FUTURE_UNSEEN_DATA",
        "ECONOMIC_INTERPRETATION_ALLOWED": False,
        "R4_STATUS": "BLOCKED",
        "R5_STATUS": "NOT_STARTED",
        "universe_size": len(SERIES_UNIVERSE),
    }
    _assert_report_clean(run_doc)

    report_root = output_report_dir or (REPORTS_DIR / "collection_runs" / collection_run_id)
    if dry_run and output_report_dir is None:
        report_root = REPORTS_DIR / "collection_runs" / f"dry_{collection_run_id}"
    report_root.mkdir(parents=True, exist_ok=True)

    def _write(name: str, doc: dict[str, Any]) -> Path:
        _assert_report_clean(doc)
        payload = {**doc, "sha256": sha256_json(doc)}
        path = report_root / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    paths = {
        "collection_run": _write("collection_run.json", run_doc),
        "series_status": _write(
            "series_status.json",
            {"collection_run_id": collection_run_id, "series": series_status},
        ),
        "data_quality": _write(
            "data_quality.json",
            {
                "collection_run_id": collection_run_id,
                "n_rejections": len(all_rejections),
                "n_gaps": len(all_gaps),
                "hash_integrity_ok": ops.get("hash_integrity_ok"),
                "duplicates_flagged": ops.get("duplicates_flagged"),
            },
        ),
        "gap_report": _write(
            "gap_report.json",
            {"collection_run_id": collection_run_id, "gaps": all_gaps},
        ),
        "rejections": _write(
            "rejections.json",
            {
                "collection_run_id": collection_run_id,
                "n": len(all_rejections),
                "rejections": all_rejections[:5000],
                "truncated": len(all_rejections) > 5000,
            },
        ),
        "hash_manifest": _write(
            "hash_manifest.json",
            {
                "collection_run_id": collection_run_id,
                "persist": persist,
                "ops_hash_integrity_ok": ops.get("hash_integrity_ok"),
                "ops_hash_errors": ops.get("hash_errors"),
            },
        ),
    }

    # Refresh ops report overlay
    ops_overlay = {
        **ops,
        "formal_collection_state": formal,
        "validation_status": "NOT_RUN",
        "effect_evaluation_status": "NOT_EVALUATED",
        "last_collection_run_id": collection_run_id,
        "effect_metrics_disclosed": False,
        "gate_preview_disclosed": False,
    }
    (REPORTS_DIR / "ops_collection_report.json").write_text(
        json.dumps(ops_overlay, indent=2) + "\n", encoding="utf-8"
    )
    # Also write ops_report.json alias requested by spec
    (REPORTS_DIR / "ops_report.json").write_text(
        json.dumps(ops_overlay, indent=2) + "\n", encoding="utf-8"
    )

    return {
        "collection_run_id": collection_run_id,
        "run_status": run_status,
        "dry_run": dry_run,
        "n_observations_before": n_before,
        "n_observations_after": n_after,
        "n_candidates": len(all_records),
        "persist": persist,
        "series_status": series_status,
        "report_paths": {k: str(v) for k, v in paths.items()},
        "ops": {
            "n_observations_total": ops_overlay["n_observations_total"],
            "collection_status": ops_overlay["collection_status"],
            "formal_collection_state": formal,
            "hash_integrity_ok": ops_overlay["hash_integrity_ok"],
            "validation_status": "NOT_RUN",
        },
        "cutoff": FUTURE_UNSEEN_CUTOFF_ISO,
    }


# Re-export for typing clarity in tests
__all__ = [
    "COLLECTOR_VERSION",
    "FORBIDDEN_COLLECTOR_IMPORTS",
    "FORBIDDEN_REPORT_KEYS",
    "collect_series",
    "run_collect",
]
