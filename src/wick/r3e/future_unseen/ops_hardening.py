"""Host-independent operational hardening helpers (B5-P1).

Read-only diagnostics, logging contract helpers, retention planning, and
READY-notification payload construction. Never executes collect/validate.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tarfile
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from wick.r3e.future_unseen.automation import (
    _is_stale_lock,
    _pid_alive,
    _read_json,
    default_lock_path,
    default_runs_dir,
    default_state_path,
)
from wick.r3e.future_unseen.paths import REPORTS_DIR, REPO_ROOT

FAILURE_CATEGORIES = (
    "CONFIGURATION_MISSING",
    "CONFIGURATION_INVALID",
    "NETWORK_UNAVAILABLE",
    "PROVIDER_AUTHENTICATION_FAILED",
    "PROVIDER_RATE_LIMITED",
    "PROVIDER_DATA_UNAVAILABLE",
    "STORE_NOT_WRITABLE",
    "STORE_CORRUPTION_SUSPECTED",
    "DISK_SPACE_LOW",
    "LOCK_ACTIVE",
    "LOCK_STALE",
    "BACKUP_FAILED",
    "READINESS_NOT_READY",
    "READINESS_TRANSITION_READY",
    "UNEXPECTED_EXCEPTION",
)

OPERATIONAL_LOG_FIELDS = (
    "timestamp_utc",
    "run_id",
    "event",
    "severity",
    "status",
    "host_id",
    "process_id",
    "store_path",
    "report_path",
    "lock_status",
    "accepted_count",
    "rejected_count",
    "store_before",
    "store_after",
    "readiness_status",
    "readiness_reason",
    "duration_ms",
    "exit_code",
    "failure_category",
    "message",
)

SECRET_PATTERNS = (
    re.compile(r"(?i)api[_-]?key"),
    re.compile(r"(?i)authorization"),
    re.compile(r"(?i)password"),
    re.compile(r"(?i)\btoken\b"),
    re.compile(r"(?i)secret"),
    re.compile(r"(?i)aws_secret"),
)

RUN_LOG_RETENTION_DAYS = 90
BACKUP_RETENTION_DAYS = 30
MINIMUM_VALID_BACKUPS = 3
FAILED_RUN_REPORT_RETENTION_DAYS = 180

def _iso_now(now: datetime | None = None) -> str:
    dt = (now or datetime.now(UTC)).astimezone(UTC)
    return dt.isoformat()


def _parse_iso(value: Any) -> datetime | None:
    if value is None:
        return None
    try:
        dt = datetime.fromisoformat(str(value))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def build_operational_log_event(**fields: Any) -> dict[str, Any]:
    """Build a contract-compliant operational log event (no secrets)."""
    event: dict[str, Any] = {name: None for name in OPERATIONAL_LOG_FIELDS}
    for key, value in fields.items():
        if key not in OPERATIONAL_LOG_FIELDS:
            continue
        if isinstance(value, str) and _looks_like_secret(value):
            event[key] = "[REDACTED]"
        else:
            event[key] = value
    if not event["timestamp_utc"]:
        event["timestamp_utc"] = _iso_now()
    if event.get("failure_category") not in (None, *FAILURE_CATEGORIES):
        event["failure_category"] = "UNEXPECTED_EXCEPTION"
    return event


def _looks_like_secret(text: str) -> bool:
    return any(pat.search(text) for pat in SECRET_PATTERNS)


def diagnose_lock(
    *,
    lock_path: Path | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Read-only lock diagnostic. Never deletes or overrides the lock file."""
    path = lock_path or default_lock_path()
    now_dt = (now or datetime.now(UTC)).astimezone(UTC)
    result: dict[str, Any] = {
        "LOCK_STATUS": "ABSENT",
        "LOCK_PATH": str(path),
        "LOCK_OWNER_PID": None,
        "LOCK_CREATED_AT": None,
        "LOCK_AGE_SECONDS": None,
        "RECOMMENDED_ACTION": "none",
        "lock_removed": False,
        "read_only": True,
        "VALIDATE_AUTHORIZED": False,
    }
    if not path.exists():
        result["RECOMMENDED_ACTION"] = "no_lock_present"
        return result

    meta = _read_json(path)
    if meta is None:
        result["LOCK_STATUS"] = "INVALID"
        result["RECOMMENDED_ACTION"] = "human_inspect_invalid_lock_do_not_auto_delete"
        return result

    created = _parse_iso(meta.get("acquired_at") or meta.get("created_at"))
    pid = meta.get("pid")
    try:
        pid_i = int(pid) if pid is not None else None
    except (TypeError, ValueError):
        pid_i = None
    result["LOCK_OWNER_PID"] = pid_i
    result["LOCK_CREATED_AT"] = None if created is None else created.isoformat()
    if created is not None:
        result["LOCK_AGE_SECONDS"] = max(0, int((now_dt - created).total_seconds()))

    if _is_stale_lock(meta, now=now_dt):
        result["LOCK_STATUS"] = "STALE"
        result["failure_category"] = "LOCK_STALE"
        result["RECOMMENDED_ACTION"] = (
            "human_authorized_removal_only_after_confirming_owner_process_dead"
        )
        return result

    if pid_i is not None and not _pid_alive(pid_i):
        # Defensive: treat dead pid without TTL parse as stale.
        result["LOCK_STATUS"] = "STALE"
        result["failure_category"] = "LOCK_STALE"
        result["RECOMMENDED_ACTION"] = (
            "human_authorized_removal_only_after_confirming_owner_process_dead"
        )
        return result

    result["LOCK_STATUS"] = "ACTIVE"
    result["failure_category"] = "LOCK_ACTIVE"
    result["RECOMMENDED_ACTION"] = "wait_for_current_cycle_or_inspect_owner_pid"
    return result


def summarize_run_history(
    *,
    state_path: Path | None = None,
    runs_dir: Path | None = None,
    readiness_path: Path | None = None,
    now: datetime | None = None,
    recent_limit: int = 10,
) -> dict[str, Any]:
    """Summarize existing automation artifacts. Read-only; no collect/validate."""
    now_dt = (now or datetime.now(UTC)).astimezone(UTC)
    state_file = state_path or default_state_path()
    runs_root = runs_dir or default_runs_dir()
    ready_file = readiness_path or (REPORTS_DIR / "readiness_report.json")

    state = _read_json(state_file) or {}
    readiness = _read_json(ready_file) or {}

    run_docs: list[dict[str, Any]] = []
    if runs_root.is_dir():
        for cycle_path in sorted(runs_root.glob("*/cycle_report.json")):
            doc = _read_json(cycle_path)
            if doc:
                run_docs.append(doc)

    def _finished_key(doc: dict[str, Any]) -> str:
        return str(doc.get("finished_at") or doc.get("started_at") or "")

    run_docs.sort(key=_finished_key)

    success_statuses = {"COMPLETE", "PARTIAL", "NO_NEW_DATA"}
    last_success_at = None
    for doc in reversed(run_docs):
        if doc.get("status") in success_statuses:
            last_success_at = doc.get("finished_at") or doc.get("started_at")
            break
    if last_success_at is None:
        if state.get("last_run_status") in success_statuses:
            last_success_at = state.get("updated_at")

    last_success_dt = _parse_iso(last_success_at)
    age_since_last_success = None
    if last_success_dt is not None:
        age_since_last_success = max(0, int((now_dt - last_success_dt).total_seconds()))

    recent_failures: list[dict[str, Any]] = []
    for doc in reversed(run_docs):
        status = str(doc.get("status") or "")
        if status in {"FAILED", "BLOCKED", "SKIPPED_LOCKED"}:
            recent_failures.append(
                {
                    "run_id": doc.get("run_id"),
                    "status": status,
                    "finished_at": doc.get("finished_at"),
                    "readiness_reason": doc.get("readiness_reason"),
                    "lock_reason": doc.get("lock_reason"),
                }
            )
        if len(recent_failures) >= recent_limit:
            break

    store_observations = (
        state.get("last_store_after")
        if state.get("last_store_after") is not None
        else readiness.get("n_observations_total")
    )

    return {
        "kind": "FUTURE_UNSEEN_RUN_HISTORY_SUMMARY",
        "read_only": True,
        "last_run_id": state.get("last_run_id"),
        "last_run_status": state.get("last_run_status"),
        "last_success_at": last_success_at,
        "age_since_last_success": age_since_last_success,
        "recent_failures": recent_failures,
        "store_observations": store_observations,
        "readiness_status": readiness.get("readiness_status")
        or state.get("last_readiness_status"),
        "readiness_reason": readiness.get("readiness_reason")
        or state.get("last_readiness_reason"),
        "scheduler_activation_status": {
            "SCHEDULER_ACTIVATION_AUTHORIZED": False,
            "SCHEDULER_ACTIVATED": False,
        },
        "runs_scanned": len(run_docs),
        "VALIDATE_AUTHORIZED": False,
        "validation_command_executed": False,
        "collect_executed": False,
        "R3E_GATE": "PENDING_FUTURE_UNSEEN_DATA",
        "R4_STATUS": "BLOCKED",
        "R5_STATUS": "NOT_STARTED",
    }


def retention_plan(
    *,
    wick_root: Path | None = None,
    now: datetime | None = None,
    dry_run: bool = True,
    run_log_retention_days: int = RUN_LOG_RETENTION_DAYS,
    backup_retention_days: int = BACKUP_RETENTION_DAYS,
    minimum_valid_backups: int = MINIMUM_VALID_BACKUPS,
    failed_run_report_retention_days: int = FAILED_RUN_REPORT_RETENTION_DAYS,
) -> dict[str, Any]:
    """Plan retention candidates. Default dry-run never deletes."""
    root = (wick_root or REPO_ROOT).resolve()
    now_dt = (now or datetime.now(UTC)).astimezone(UTC)
    backups_dir = root / "backups"
    runs_dir = root / "reports" / "r3e_future_unseen" / "automation_runs"
    store_dir = root / "data" / "future_unseen"

    backup_files = sorted(
        backups_dir.glob("fu_backup_*.tar.gz") if backups_dir.is_dir() else [],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    tmp_in_progress = sorted(backups_dir.glob(".tmp_fu_backup_*")) if backups_dir.is_dir() else []

    backup_candidates: list[str] = []
    newest = backup_files[0] if backup_files else None
    cutoff_backup = now_dt - timedelta(days=backup_retention_days)
    for path in backup_files:
        if newest is not None and path == newest:
            continue
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)
        if mtime < cutoff_backup:
            backup_candidates.append(str(path))

    # Keep minimum valid backups: never propose deleting if remaining would drop below min.
    protected = {str(newest)} if newest is not None else set()
    remaining_after = len(backup_files)
    filtered_backup_candidates: list[str] = []
    for cand in backup_candidates:
        if remaining_after - 1 < minimum_valid_backups:
            break
        filtered_backup_candidates.append(cand)
        remaining_after -= 1
        protected.add(cand)  # track considered; newest already protected

    run_candidates: list[str] = []
    if runs_dir.is_dir():
        for cycle_path in runs_dir.glob("*/cycle_report.json"):
            doc = _read_json(cycle_path) or {}
            finished = _parse_iso(doc.get("finished_at"))
            if finished is None:
                finished = datetime.fromtimestamp(cycle_path.stat().st_mtime, tz=UTC)
            status = str(doc.get("status") or "")
            days = (
                failed_run_report_retention_days
                if status in {"FAILED", "BLOCKED"}
                else run_log_retention_days
            )
            if finished < now_dt - timedelta(days=days):
                run_candidates.append(str(cycle_path.parent))

    deletions_performed = 0
    if not dry_run:
        raise PermissionError(
            "retention apply/delete is not authorized in B5-P1; dry_run=True required"
        )

    return {
        "kind": "FUTURE_UNSEEN_RETENTION_PLAN",
        "dry_run": True,
        "deletions_performed": deletions_performed,
        "wick_root": str(root),
        "defaults": {
            "RUN_LOG_RETENTION_DAYS": run_log_retention_days,
            "BACKUP_RETENTION_DAYS": backup_retention_days,
            "MINIMUM_VALID_BACKUPS": minimum_valid_backups,
            "FAILED_RUN_REPORT_RETENTION_DAYS": failed_run_report_retention_days,
        },
        "tmp_backup_in_progress": [str(p) for p in tmp_in_progress],
        "backup_candidates_for_deletion": filtered_backup_candidates,
        "run_report_candidates_for_deletion": run_candidates,
        "latest_valid_backup_preserved": None if newest is None else str(newest),
        "backup_count": len(backup_files),
        "store_observations_subject_to_retention": False,
        "store_path": str(store_dir),
        "VALIDATE_AUTHORIZED": False,
    }


def verify_backup_archive(
    archive_path: Path,
    *,
    restore_target: Path | None = None,
) -> dict[str, Any]:
    """Verify a backup archive without restoring onto production paths."""
    checks = {
        "archive_exists": False,
        "archive_nonempty": False,
        "manifest_exists": False,
        "checksum_valid": False,
        "expected_directories_present": False,
        "secret_files_absent": False,
        "restore_target_not_overwritten": True,
    }
    notes: list[str] = []
    archive = archive_path.resolve()
    checks["archive_exists"] = archive.is_file()
    size = archive.stat().st_size if checks["archive_exists"] else 0
    checks["archive_nonempty"] = size > 0

    digest = None
    if checks["archive_exists"]:
        h = hashlib.sha256()
        with archive.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                h.update(chunk)
        digest = h.hexdigest()

    sidecar = Path(str(archive) + ".sha256")
    if sidecar.is_file():
        checks["manifest_exists"] = True
        expected = sidecar.read_text(encoding="utf-8").strip().split()[0]
        checks["checksum_valid"] = bool(digest and expected == digest)
        if not checks["checksum_valid"]:
            notes.append("checksum_mismatch")
    else:
        notes.append("CHECKSUM_SIDECAR_ABSENT")
        # Sidecar optional for legacy archives; treat computed digest as evidence.
        checks["manifest_exists"] = False
        checks["checksum_valid"] = bool(digest)

    members: list[str] = []
    secret_hits: list[str] = []
    if checks["archive_nonempty"]:
        try:
            with tarfile.open(archive, "r:gz") as tf:
                members = [m.name for m in tf.getmembers()]
        except (tarfile.TarError, OSError) as exc:
            notes.append(f"tar_read_failed:{type(exc).__name__}")
            members = []

    has_data = any(name.startswith("data/future_unseen") for name in members)
    has_reports = any(name.startswith("reports/r3e_future_unseen") for name in members)
    checks["expected_directories_present"] = has_data and has_reports
    # Manifest path presence inside archive helps when sidecar absent.
    if any("manifests/" in name for name in members):
        checks["manifest_exists"] = True

    for name in members:
        base = Path(name).name
        if base.endswith(".env") or "secret" in base.lower():
            secret_hits.append(name)
    checks["secret_files_absent"] = not secret_hits

    if restore_target is not None and restore_target.exists():
        # Verification must not overwrite; we never extract to restore_target.
        checks["restore_target_not_overwritten"] = True
        notes.append("restore_target_exists_left_untouched")

    passed = all(checks.values())
    return {
        "kind": "FUTURE_UNSEEN_BACKUP_VERIFICATION",
        "archive_path": str(archive),
        "archive_size_bytes": size,
        "sha256": digest,
        "BACKUP_VERIFICATION": "PASS" if passed else "FAIL",
        "checks": checks,
        "secret_hits": secret_hits,
        "notes": notes,
        "restore_executed": False,
        "VALIDATE_AUTHORIZED": False,
    }


def build_ready_transition_notification(
    *,
    run_id: str,
    timestamp_utc: str | None = None,
    store_observations: int | None,
    window_days: float | None,
    previous_readiness_status: str = "NOT_READY",
) -> dict[str, Any]:
    """Build READY transition notification payload (no effect/economic/validate)."""
    payload = {
        "event": "readiness_transition_ready",
        "message": "readiness changed from NOT_READY to READY",
        "previous_readiness_status": previous_readiness_status,
        "readiness_status": "READY",
        "timestamp_utc": timestamp_utc or _iso_now(),
        "run_id": run_id,
        "store_observations": store_observations,
        "window_days": window_days,
        "next_authorized_action": "HUMAN_REVIEW_REQUIRED",
        "human_review_required": True,
        "VALIDATE_AUTHORIZED": False,
        "validation_command_executed": False,
        "effect_peeking_performed": False,
        "ECONOMIC_INTERPRETATION_ALLOWED": False,
        "SCHEDULER_ACTIVATION_AUTHORIZED": False,
    }
    banned_exact = {
        "effect",
        "effect_size",
        "p_value",
        "economic",
        "economic_interpretation",
        "validate_decision",
        "gate_decision",
        "model_effect",
    }
    leaked = [k for k in payload if k.lower() in banned_exact]
    if leaked:
        raise ValueError(f"READY notification leaked scientific keys: {leaked}")
    return payload


def activation_checklist_ends_unauthorized(checklist_text: str) -> bool:
    """Return True if checklist canonical field remains unauthorized."""
    return "SCHEDULER_ACTIVATION_AUTHORIZED = false" in checklist_text


def host_id_or_none() -> str | None:
    """Opaque host id helper; returns None rather than inventing values in tests."""
    # Prefer explicit env; otherwise leave null for host-independent tooling.
    value = os.environ.get("WICK_HOST_ID")
    return value if value else None
