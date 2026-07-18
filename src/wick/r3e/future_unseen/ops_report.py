"""Operational collection monitoring — no effect / gate peeking."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from wick.r3e.future_unseen.config import (
    FUTURE_UNSEEN_CUTOFF,
    FUTURE_UNSEEN_CUTOFF_ISO,
    MIN_BARS_PER_SERIES,
    MIN_CALENDAR_DAYS_AFTER_CUTOFF,
    MIN_SERIES_COMPLETE,
    SERIES_UNIVERSE,
    STATUS_COLLECTION_COMPLETE,
    STATUS_COLLECTION_IN_PROGRESS,
    STATUS_COLLECTION_NOT_STARTED,
)
from wick.r3e.future_unseen.hashing import verify_file_hash
from wick.r3e.future_unseen.paths import MANIFESTS_DIR, REPORTS_DIR, VALIDATED_DIR, ensure_dirs
from wick.r3e.future_unseen.protections import FutureUnseenProtectionError

# Keys that must never appear in ops reports (optional-stopping defense)
FORBIDDEN_OPS_KEYS = frozenset(
    {
        "delta_candle",
        "p_raw",
        "p_adj",
        "p_value",
        "mean_net",
        "hit_rate",
        "DELTA_CANDLE",
        "gate_decision",
        "classification_counts",
    }
)


def _series_key(symbol: str, timeframe: str, source: str) -> str:
    return f"{source}|{symbol}|{timeframe}"


def build_ops_report(*, out_path: Path | None = None) -> dict[str, Any]:
    """Build collection-only integrity report (no model economics)."""
    ensure_dirs()
    official = [_series_key(s, t, src) for s, t, src in SERIES_UNIVERSE]
    counts: dict[str, int] = {k: 0 for k in official}
    first_ts: dict[str, str] = {}
    last_ts: dict[str, str] = {}
    hash_ok = True
    hash_errors: list[str] = []
    gaps: list[dict[str, Any]] = []
    duplicates = 0

    # Verify batch manifests
    for man in sorted(MANIFESTS_DIR.glob("batch_*.json")):
        meta = json.loads(man.read_text(encoding="utf-8"))
        try:
            verify_file_hash(Path(meta["validated_path"]), meta["file_sha256"])
        except (ValueError, KeyError, FileNotFoundError) as exc:
            hash_ok = False
            hash_errors.append(f"{man.name}: {exc}")
        for reason in meta.get("rejections", []):
            if "duplicate" in str(reason.get("reason", "")).lower():
                duplicates += 1
        gaps.extend(meta.get("gaps_detected", []))

    seen_keys: set[str] = set()
    for path in sorted(VALIDATED_DIR.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            sk = _series_key(rec["symbol"], rec["timeframe"], rec["source"])
            uk = sk + "|" + rec["market_ts"] + "|r" + str(rec.get("revision", 1))
            if uk in seen_keys:
                duplicates += 1
            seen_keys.add(uk)
            if sk in counts:
                counts[sk] += 1
                ts = rec["market_ts"]
                first_ts[sk] = ts if sk not in first_ts else min(first_ts[sk], ts)
                last_ts[sk] = ts if sk not in last_ts else max(last_ts[sk], ts)

    received = [k for k, n in counts.items() if n > 0]
    missing = [k for k, n in counts.items() if n == 0]
    complete_series = [k for k, n in counts.items() if n >= MIN_BARS_PER_SERIES]
    total_obs = sum(counts.values())

    now = datetime.now(UTC)
    days_elapsed = max(0, (now - FUTURE_UNSEEN_CUTOFF).total_seconds() / 86400.0)
    calendar_ready = days_elapsed >= MIN_CALENDAR_DAYS_AFTER_CUTOFF
    series_ready = len(complete_series) >= MIN_SERIES_COMPLETE

    if total_obs == 0:
        status = STATUS_COLLECTION_NOT_STARTED
    elif calendar_ready and series_ready and hash_ok:
        status = STATUS_COLLECTION_COMPLETE
    else:
        status = STATUS_COLLECTION_IN_PROGRESS

    report: dict[str, Any] = {
        "report_kind": "OPERATIONAL_COLLECTION_ONLY",
        "cutoff": FUTURE_UNSEEN_CUTOFF_ISO,
        "generated_at": now.isoformat(),
        "collection_status": status,
        "series_received": received,
        "series_missing": missing,
        "series_counts": counts,
        "n_observations_total": total_obs,
        "n_series_complete": len(complete_series),
        "min_bars_per_series": MIN_BARS_PER_SERIES,
        "min_series_complete": MIN_SERIES_COMPLETE,
        "gaps": gaps,
        "duplicates_flagged": duplicates,
        "hash_integrity_ok": hash_ok,
        "hash_errors": hash_errors,
        "temporal_coverage": {
            "first_market_ts_by_series": first_ts,
            "last_market_ts_by_series": last_ts,
            "days_elapsed_since_cutoff": days_elapsed,
            "min_calendar_days_required": MIN_CALENDAR_DAYS_AFTER_CUTOFF,
            "calendar_ready": calendar_ready,
        },
        "completeness": {
            "series_ready": series_ready,
            "calendar_ready": calendar_ready,
            "ready_for_final_validation": status == STATUS_COLLECTION_COMPLETE,
        },
        # Explicit non-disclosure
        "effect_metrics_disclosed": False,
        "gate_preview_disclosed": False,
    }
    _assert_ops_clean(report)

    out = out_path or (REPORTS_DIR / "ops_collection_report.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def _assert_ops_clean(report: dict[str, Any]) -> None:
    def walk(obj: Any) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in FORBIDDEN_OPS_KEYS:
                    raise FutureUnseenProtectionError(f"ops report must not contain effect key {k}")
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(report)


def collection_ready() -> bool:
    return build_ops_report()["completeness"]["ready_for_final_validation"] is True
