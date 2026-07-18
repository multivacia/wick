"""Future-unseen operational readiness gate (B2 / R3E-READINESS-001).

Read-only evaluation. Does not execute scientific validate, effect metrics,
or mutate the official store. Returns READY | NOT_READY | BLOCKED.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from wick.r3e.future_unseen.config import (
    FORBIDDEN_DATA_ROOTS,
    FUTURE_UNSEEN_CUTOFF,
    FUTURE_UNSEEN_CUTOFF_ISO,
    MIN_BARS_PER_SERIES,
    MIN_CALENDAR_DAYS_AFTER_CUTOFF,
    MIN_SERIES_COMPLETE,
    SERIES_UNIVERSE,
)
from wick.r3e.future_unseen.hashing import verify_file_hash
from wick.r3e.future_unseen.ops_report import FORBIDDEN_OPS_KEYS
from wick.r3e.future_unseen.paths import (
    COLLECTION_STATE_PATH,
    MANIFESTS_DIR,
    RAW_DIR,
    REPORTS_DIR,
    VALIDATED_DIR,
    ensure_dirs,
)
from wick.r3e.future_unseen.protections import (
    FutureUnseenProtectionError,
    parse_market_ts,
)

STATUS_READY = "READY"
STATUS_NOT_READY = "NOT_READY"
STATUS_BLOCKED = "BLOCKED"

EXIT_READY = 0
EXIT_NOT_READY = 2
EXIT_BLOCKED = 3

GAP_INFORMATIONAL = "INFORMATIONAL"
GAP_EXPECTED_MARKET_CLOSURE = "EXPECTED_MARKET_CLOSURE"
GAP_DATA_PROVIDER_LIMITATION = "DATA_PROVIDER_LIMITATION"
GAP_CRITICAL = "CRITICAL"

BACKFILL_MARKERS = (
    "operational_backfill",
    "operational-backfill",
    "data/operational",
    "reports/r3e_operational",
)

FORBIDDEN_SCIENCE_TOUCH = frozenset(
    {
        "delta_candle",
        "DELTA_CANDLE",
        "m4",
        "m5",
        "p_value",
        "p_raw",
        "p_adj",
        "fdr",
        "bootstrap",
        "mean_net",
        "sharpe",
        "gate_decision",
    }
)


def _series_key(symbol: str, timeframe: str, source: str) -> str:
    return f"{source}|{symbol}|{timeframe}"


def _classify_gap(raw: dict[str, Any]) -> str:
    kind = str(raw.get("kind", "")).lower()
    classification = str(raw.get("classification", "")).upper()
    text = " ".join(str(raw.get(k, "")) for k in ("reason", "note", "message", "kind")).lower()
    if classification in {
        GAP_INFORMATIONAL,
        GAP_EXPECTED_MARKET_CLOSURE,
        GAP_DATA_PROVIDER_LIMITATION,
        GAP_CRITICAL,
    }:
        return classification
    if kind == "non_monotonic" or "non_monotonic" in text:
        return GAP_CRITICAL
    if classification == "EXPECTED_MARKET_CLOSURE" or "weekend" in text or "session" in text:
        return GAP_EXPECTED_MARKET_CLOSURE
    if (
        classification in {"PROVIDER_MISSING_DATA", "DATA_PROVIDER_LIMITATION"}
        or "provider" in text
    ):
        return GAP_DATA_PROVIDER_LIMITATION
    if classification == "UNEXPLAINED_GAP":
        return GAP_INFORMATIONAL
    return GAP_INFORMATIONAL


def _contains_forbidden_science(obj: Any) -> list[str]:
    found: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                if str(k).lower() in {
                    x.lower() for x in FORBIDDEN_SCIENCE_TOUCH | FORBIDDEN_OPS_KEYS
                }:
                    found.append(str(k))
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(obj)
    return found


def evaluate_readiness(
    *,
    as_of: datetime | None = None,
    strict: bool = False,
    store_root: Path | None = None,
) -> dict[str, Any]:
    """Evaluate operational readiness of the official future_unseen store.

    Read-only with respect to raw/validated/manifests. Optional report writing
    is handled by the CLI caller only.
    """
    ensure_dirs()
    as_of_dt = as_of.astimezone(UTC) if as_of is not None else datetime.now(UTC)
    if as_of_dt.tzinfo is None:
        raise FutureUnseenProtectionError("as_of must be timezone-aware UTC")

    manifests_dir = MANIFESTS_DIR if store_root is None else store_root / "manifests"
    validated_dir = VALIDATED_DIR if store_root is None else store_root / "validated"
    raw_dir = RAW_DIR if store_root is None else store_root / "raw"
    state_path = (
        COLLECTION_STATE_PATH if store_root is None else manifests_dir / "collection_state.json"
    )

    blockers: list[dict[str, str]] = []
    not_ready_reasons: list[dict[str, str]] = []
    gap_summary = {
        GAP_INFORMATIONAL: 0,
        GAP_EXPECTED_MARKET_CLOSURE: 0,
        GAP_DATA_PROVIDER_LIMITATION: 0,
        GAP_CRITICAL: 0,
    }

    official = [_series_key(s, t, src) for s, t, src in SERIES_UNIVERSE]
    counts: dict[str, int] = {k: 0 for k in official}
    first_ts: dict[str, str] = {}
    last_ts: dict[str, str] = {}
    open_candle_hits = 0
    pre_cutoff_hits = 0
    duplicates = 0
    hash_ok = True
    hash_errors: list[str] = []
    manifest_ok = True
    manifest_errors: list[str] = []
    backfill_hits: list[str] = []
    origins: list[str] = []

    # Collection state / scientific safety locks
    state: dict[str, Any] = {}
    if state_path.is_file():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        if state.get("validation_command_executed") is True:
            blockers.append(
                {
                    "code": "VALIDATE_EXECUTED",
                    "detail": "collection_state.validation_command_executed=true",
                }
            )
        if state.get("effect_peeking_performed") is True:
            blockers.append(
                {
                    "code": "EFFECT_PEEKING",
                    "detail": "collection_state.effect_peeking_performed=true",
                }
            )
        if state.get("R4_STATUS") not in (None, "BLOCKED"):
            blockers.append(
                {"code": "R4_NOT_BLOCKED", "detail": f"R4_STATUS={state.get('R4_STATUS')!r}"}
            )
        if state.get("R5_STATUS") not in (None, "NOT_STARTED"):
            blockers.append(
                {"code": "R5_STARTED", "detail": f"R5_STATUS={state.get('R5_STATUS')!r}"}
            )
        science_leaks = _contains_forbidden_science(state)
        if science_leaks:
            blockers.append(
                {
                    "code": "SCIENCE_KEYS_IN_STATE",
                    "detail": ",".join(sorted(set(science_leaks))),
                }
            )
    else:
        not_ready_reasons.append({"code": "COLLECTION_STATE_MISSING", "detail": str(state_path)})

    # Batch manifests + hash integrity + origin / backfill checks
    for man in sorted(manifests_dir.glob("batch_*.json")):
        try:
            meta = json.loads(man.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            manifest_ok = False
            manifest_errors.append(f"{man.name}: invalid json ({exc})")
            continue
        origin = str(meta.get("origin", ""))
        if origin:
            origins.append(origin)
        for marker in BACKFILL_MARKERS + FORBIDDEN_DATA_ROOTS:
            blob = json.dumps(meta, sort_keys=True)
            if marker in blob or marker in origin:
                backfill_hits.append(f"{man.name}:{marker}")
        validated_path = meta.get("validated_path")
        file_sha = meta.get("file_sha256")
        if not validated_path or not file_sha:
            manifest_ok = False
            manifest_errors.append(f"{man.name}: missing validated_path/file_sha256")
            continue
        try:
            verify_file_hash(Path(validated_path), file_sha)
        except (ValueError, FileNotFoundError) as exc:
            hash_ok = False
            hash_errors.append(f"{man.name}: {exc}")
        for gap in meta.get("gaps_detected", []) or []:
            klass = _classify_gap(gap if isinstance(gap, dict) else {"kind": str(gap)})
            gap_summary[klass] = gap_summary.get(klass, 0) + 1
            if klass == GAP_CRITICAL:
                blockers.append(
                    {
                        "code": "CRITICAL_GAP",
                        "detail": f"{man.name}:{gap}",
                    }
                )
        # Rejection logs may mention duplicates rejected at ingest; that is healthy
        # fail-closed behavior and must not by itself BLOCK readiness.

    if backfill_hits:
        blockers.append(
            {
                "code": "BACKFILL_OR_FORBIDDEN_MIX",
                "detail": ";".join(backfill_hits[:20]),
            }
        )
    if not manifest_ok:
        blockers.append(
            {
                "code": "MANIFEST_INCONSISTENT",
                "detail": ";".join(manifest_errors[:20]),
            }
        )
    if not hash_ok:
        blockers.append(
            {
                "code": "HASH_INVALID",
                "detail": ";".join(hash_errors[:20]),
            }
        )

    # Validated records scan
    seen_keys: set[str] = set()
    for path in sorted(validated_dir.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            sk = _series_key(rec["symbol"], rec["timeframe"], rec["source"])
            uk = sk + "|" + rec["market_ts"] + "|r" + str(rec.get("revision", 1))
            if uk in seen_keys:
                duplicates += 1
            seen_keys.add(uk)
            try:
                ts = parse_market_ts(rec["market_ts"])
            except FutureUnseenProtectionError as exc:
                blockers.append({"code": "INVALID_TIMESTAMP", "detail": str(exc)})
                continue
            if ts <= FUTURE_UNSEEN_CUTOFF:
                pre_cutoff_hits += 1
            # Open-candle heuristic: bar end must be <= as_of
            # For 1h assume close at market_ts; if market_ts > as_of → open/future
            if ts > as_of_dt:
                open_candle_hits += 1
            if sk in counts:
                counts[sk] += 1
                iso = ts.isoformat()
                first_ts[sk] = iso if sk not in first_ts else min(first_ts[sk], iso)
                last_ts[sk] = iso if sk not in last_ts else max(last_ts[sk], iso)
            origin = str(rec.get("origin", ""))
            for marker in BACKFILL_MARKERS + FORBIDDEN_DATA_ROOTS:
                if marker in origin:
                    backfill_hits.append(f"record:{sk}:{marker}")

    if pre_cutoff_hits:
        blockers.append(
            {
                "code": "PRE_OR_AT_CUTOFF_DATA",
                "detail": f"n={pre_cutoff_hits}",
            }
        )
    if open_candle_hits:
        # Official store should not hold open candles; treat as NOT_READY unless strict→BLOCKED
        if strict:
            blockers.append(
                {
                    "code": "OPEN_OR_FUTURE_CANDLE",
                    "detail": f"n={open_candle_hits}",
                }
            )
        else:
            not_ready_reasons.append(
                {
                    "code": "OPEN_OR_FUTURE_CANDLE",
                    "detail": f"n={open_candle_hits}",
                }
            )
    if duplicates:
        # Explicit treatment: duplicates are integrity concerns → BLOCKED when present in store
        blockers.append(
            {
                "code": "DUPLICATES_PRESENT",
                "detail": f"n={duplicates}",
            }
        )
    if backfill_hits and not any(b["code"] == "BACKFILL_OR_FORBIDDEN_MIX" for b in blockers):
        blockers.append(
            {
                "code": "BACKFILL_OR_FORBIDDEN_MIX",
                "detail": ";".join(sorted(set(backfill_hits))[:20]),
            }
        )

    # Raw/validated presence consistency (manifest points into validated)
    if manifests_dir.exists() and validated_dir.exists():
        for man in sorted(manifests_dir.glob("batch_*.json")):
            try:
                meta = json.loads(man.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            vp = meta.get("validated_path")
            if vp and not Path(vp).is_file():
                manifest_ok = False
                blockers.append(
                    {
                        "code": "MANIFEST_VALIDATED_MISSING",
                        "detail": f"{man.name}:{vp}",
                    }
                )

    complete_series = [k for k, n in counts.items() if n >= MIN_BARS_PER_SERIES]
    partial_series = [k for k, n in counts.items() if 0 < n < MIN_BARS_PER_SERIES]
    missing_series = [k for k, n in counts.items() if n == 0]
    days_elapsed = max(0.0, (as_of_dt - FUTURE_UNSEEN_CUTOFF).total_seconds() / 86400.0)
    calendar_ready = days_elapsed >= MIN_CALENDAR_DAYS_AFTER_CUTOFF
    series_ready = len(complete_series) >= MIN_SERIES_COMPLETE
    total_obs = sum(counts.values())

    if not calendar_ready:
        not_ready_reasons.append(
            {
                "code": "WINDOW_DAYS_INSUFFICIENT",
                "detail": f"days={days_elapsed:.4f} < {MIN_CALENDAR_DAYS_AFTER_CUTOFF}",
            }
        )
    if not series_ready:
        not_ready_reasons.append(
            {
                "code": "SERIES_INSUFFICIENT",
                "detail": f"complete={len(complete_series)} < {MIN_SERIES_COMPLETE}",
            }
        )
    bars_short = [k for k in partial_series]
    if bars_short and len(complete_series) < MIN_SERIES_COMPLETE:
        not_ready_reasons.append(
            {
                "code": "BARS_INSUFFICIENT",
                "detail": f"partial_series={len(partial_series)} min_bars={MIN_BARS_PER_SERIES}",
            }
        )
    if total_obs == 0:
        not_ready_reasons.append({"code": "NO_OBSERVATIONS", "detail": "store empty"})

    collector_status = state.get("R3E_FUTURE_DATA_COLLECTION", "UNKNOWN")
    if collector_status not in {"IN_PROGRESS", "COMPLETE"}:
        not_ready_reasons.append(
            {
                "code": "COLLECTOR_STATE",
                "detail": f"R3E_FUTURE_DATA_COLLECTION={collector_status!r}",
            }
        )

    # Deduplicate blockers by code+detail
    uniq_blockers: list[dict[str, str]] = []
    seen_b: set[str] = set()
    for b in blockers:
        key = b["code"] + "|" + b["detail"]
        if key in seen_b:
            continue
        seen_b.add(key)
        uniq_blockers.append(b)

    if uniq_blockers:
        status = STATUS_BLOCKED
        primary_reason = uniq_blockers[0]["code"]
    elif not_ready_reasons:
        status = STATUS_NOT_READY
        primary_reason = not_ready_reasons[0]["code"]
    else:
        status = STATUS_READY
        primary_reason = "ALL_CRITERIA_SATISFIED"

    report: dict[str, Any] = {
        "report_kind": "FUTURE_UNSEEN_READINESS_GATE",
        "task_id": "R3E-READINESS-001",
        "backlog_item": "B2",
        "cutoff": FUTURE_UNSEEN_CUTOFF_ISO,
        "as_of": as_of_dt.isoformat(),
        "generated_at": datetime.now(UTC).isoformat(),
        "readiness_status": status,
        "readiness_reason": primary_reason,
        "strict": strict,
        "window_days": days_elapsed,
        "required_window_days": MIN_CALENDAR_DAYS_AFTER_CUTOFF,
        "eligible_series": len([k for k, n in counts.items() if n > 0]),
        "required_series": MIN_SERIES_COMPLETE,
        "series_with_min_bars": len(complete_series),
        "required_min_bars": MIN_BARS_PER_SERIES,
        "series_complete": complete_series,
        "series_partial": partial_series,
        "series_missing": missing_series,
        "series_blocked": [b["detail"] for b in uniq_blockers if "SERIES" in b["code"]],
        "series_counts": counts,
        "n_observations_total": total_obs,
        "hash_status": "OK" if hash_ok else "INVALID",
        "hash_errors": hash_errors,
        "manifest_status": "OK" if manifest_ok else "INCONSISTENT",
        "manifest_errors": manifest_errors,
        "gap_status": {
            "counts": gap_summary,
            "critical_present": gap_summary.get(GAP_CRITICAL, 0) > 0,
        },
        "duplicates_flagged": duplicates,
        "pre_cutoff_hits": pre_cutoff_hits,
        "open_or_future_candle_hits": open_candle_hits,
        "collector_status": collector_status,
        "origins_seen": sorted(set(origins)),
        "blockers": uniq_blockers,
        "not_ready_reasons": not_ready_reasons,
        "thresholds_source": {
            "MIN_CALENDAR_DAYS_AFTER_CUTOFF": MIN_CALENDAR_DAYS_AFTER_CUTOFF,
            "MIN_SERIES_COMPLETE": MIN_SERIES_COMPLETE,
            "MIN_BARS_PER_SERIES": MIN_BARS_PER_SERIES,
            "authority": "src/wick/r3e/future_unseen/config.py + docs/specs/R3E_FUTURE_UNSEEN_VALIDATION_SPEC.md",
        },
        "scientific_safety": {
            "validation_command_executed": bool(state.get("validation_command_executed", False)),
            "effect_peeking_performed": bool(state.get("effect_peeking_performed", False)),
            "R3E_GATE": state.get("R3E_GATE", "PENDING_FUTURE_UNSEEN_DATA"),
            "ECONOMIC_INTERPRETATION_ALLOWED": state.get("ECONOMIC_INTERPRETATION_ALLOWED", False),
            "R4_STATUS": state.get("R4_STATUS", "BLOCKED"),
            "R5_STATUS": state.get("R5_STATUS", "NOT_STARTED"),
            "VALIDATE_AUTHORIZED": False,
            "HUMAN_AUTHORIZATION_REQUIRED": True,
        },
        "store_roots": {
            "raw": str(raw_dir),
            "validated": str(validated_dir),
            "manifests": str(manifests_dir),
        },
        "effect_metrics_disclosed": False,
        "gate_preview_disclosed": False,
        "side_effects": False,
        "read_only": True,
    }
    leaks = _contains_forbidden_science(report)
    if leaks:
        raise FutureUnseenProtectionError(f"readiness report leaked science keys: {leaks}")
    return report


def exit_code_for_status(status: str) -> int:
    if status == STATUS_READY:
        return EXIT_READY
    if status == STATUS_BLOCKED:
        return EXIT_BLOCKED
    return EXIT_NOT_READY


def default_report_path() -> Path:
    return REPORTS_DIR / "readiness_report.json"
