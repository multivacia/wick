"""Future-unseen collection automation cycle (B4 / COLLECTION-AUTOMATION-001).

Operational orchestration only. Never imports or executes scientific validate/gate.
"""

from __future__ import annotations

import json
import os
import socket
import time
import uuid
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from wick.r3e.future_unseen.collector import run_collect
from wick.r3e.future_unseen.ops_report import build_ops_report
from wick.r3e.future_unseen.paths import COLLECTION_STATE_PATH, MANIFESTS_DIR, REPORTS_DIR, ensure_dirs
from wick.r3e.future_unseen.readiness import evaluate_readiness

AUTOMATION_VERSION = "0.1.0"

STATUS_COMPLETE = "COMPLETE"
STATUS_PARTIAL = "PARTIAL"
STATUS_NO_NEW_DATA = "NO_NEW_DATA"
STATUS_BLOCKED = "BLOCKED"
STATUS_FAILED = "FAILED"
STATUS_SKIPPED_LOCKED = "SKIPPED_LOCKED"

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_BLOCKED = 3
EXIT_SKIPPED_LOCKED = 4

DEFAULT_LOCK_TTL_SECONDS = 3300  # 55 minutes — under hourly cadence
DEFAULT_TIMEOUT_SECONDS = 3000
DEFAULT_MAX_RETRIES = 3

LOCK_NAME = "automation.lock"
STATE_NAME = "automation_state.json"
RUNS_DIRNAME = "automation_runs"
EVENTS_NAME = "automation_events.jsonl"

FORBIDDEN_AUTOMATION_IMPORTS = (
    "wick.r3e.future_unseen.validate",
    "wick.r3e.future_unseen.gate",
    "wick.r3e.pipeline",
    "wick.r3e.compare",
)

CollectFn = Callable[..., dict[str, Any]]
ReadinessFn = Callable[..., dict[str, Any]]
OpsFn = Callable[..., dict[str, Any]]
NowFn = Callable[[], datetime]


def default_lock_path() -> Path:
    return REPORTS_DIR / LOCK_NAME


def default_state_path() -> Path:
    return REPORTS_DIR / STATE_NAME


def default_runs_dir() -> Path:
    return REPORTS_DIR / RUNS_DIRNAME


def default_events_path() -> Path:
    return REPORTS_DIR / EVENTS_NAME


def exit_code_for_cycle_status(status: str) -> int:
    if status == STATUS_SKIPPED_LOCKED:
        return EXIT_SKIPPED_LOCKED
    if status == STATUS_BLOCKED:
        return EXIT_BLOCKED
    if status == STATUS_FAILED:
        return EXIT_FAILED
    if status in {STATUS_COMPLETE, STATUS_PARTIAL, STATUS_NO_NEW_DATA}:
        return EXIT_OK
    return EXIT_FAILED


def _iso(dt: datetime) -> str:
    return dt.astimezone(UTC).isoformat()


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _write_json(path: Path, doc: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")


def _is_stale_lock(meta: dict[str, Any], *, now: datetime) -> bool:
    expires_raw = meta.get("expires_at")
    if expires_raw:
        try:
            expires = datetime.fromisoformat(str(expires_raw))
            if expires.tzinfo is None:
                expires = expires.replace(tzinfo=UTC)
            if now >= expires.astimezone(UTC):
                return True
        except ValueError:
            return True
    pid = int(meta.get("pid") or 0)
    if pid and not _pid_alive(pid):
        return True
    return False


class AutomationLock:
    """Atomic file lock with TTL and stale recovery."""

    def __init__(
        self,
        path: Path,
        *,
        run_id: str,
        ttl_seconds: int = DEFAULT_LOCK_TTL_SECONDS,
        now_fn: NowFn | None = None,
    ) -> None:
        self.path = path
        self.run_id = run_id
        self.ttl_seconds = ttl_seconds
        self.now_fn = now_fn or (lambda: datetime.now(UTC))
        self.acquired = False
        self.meta: dict[str, Any] | None = None

    def acquire(self) -> tuple[bool, str]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        now = self.now_fn().astimezone(UTC)
        if self.path.exists():
            existing = _read_json(self.path) or {}
            if _is_stale_lock(existing, now=now):
                try:
                    self.path.unlink(missing_ok=True)
                except OSError as exc:
                    return False, f"stale_lock_unlink_failed:{exc}"
            else:
                return False, "lock_held"

        payload = {
            "kind": "FUTURE_UNSEEN_AUTOMATION_LOCK",
            "run_id": self.run_id,
            "owner": f"{socket.gethostname()}:{os.getpid()}",
            "hostname": socket.gethostname(),
            "pid": os.getpid(),
            "acquired_at": _iso(now),
            "expires_at": _iso(now + timedelta(seconds=self.ttl_seconds)),
            "ttl_seconds": self.ttl_seconds,
        }
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        try:
            fd = os.open(self.path, flags, 0o644)
        except FileExistsError:
            return False, "lock_held"
        except OSError as exc:
            return False, f"lock_open_failed:{exc}"
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(json.dumps(payload, indent=2) + "\n")
        except OSError as exc:
            try:
                self.path.unlink(missing_ok=True)
            except OSError:
                pass
            return False, f"lock_write_failed:{exc}"
        self.acquired = True
        self.meta = payload
        return True, "acquired"

    def release(self) -> None:
        if not self.acquired:
            return
        try:
            current = _read_json(self.path) or {}
            if current.get("run_id") == self.run_id:
                self.path.unlink(missing_ok=True)
        except OSError:
            pass
        self.acquired = False


def _preflight(*, ops_fn: OpsFn) -> dict[str, Any]:
    ensure_dirs()
    state = _read_json(COLLECTION_STATE_PATH)
    if state is None:
        return {
            "ok": False,
            "blocked": True,
            "reason": "COLLECTION_STATE_MISSING",
            "hash_status": "UNKNOWN",
            "manifest_status": "UNKNOWN",
        }
    if state.get("R3E_FUTURE_DATA_COLLECTION") not in {"IN_PROGRESS", "COMPLETE"}:
        return {
            "ok": False,
            "blocked": True,
            "reason": f"UNEXPECTED_COLLECTION_STATE:{state.get('R3E_FUTURE_DATA_COLLECTION')}",
            "hash_status": "UNKNOWN",
            "manifest_status": "UNKNOWN",
        }
    ops = ops_fn(out_path=REPORTS_DIR / "ops_collection_report.json")
    hash_ok = bool(ops.get("hash_integrity_ok", False))
    if not hash_ok:
        return {
            "ok": False,
            "blocked": True,
            "reason": "HASH_INTEGRITY_FAILED",
            "hash_status": "INVALID",
            "manifest_status": "INVALID",
            "ops": ops,
        }
    return {
        "ok": True,
        "blocked": False,
        "reason": "OK",
        "hash_status": "OK",
        "manifest_status": "OK",
        "ops": ops,
        "formal_state": state,
    }


def _count_provider_failures(collect_result: dict[str, Any]) -> int:
    n = 0
    for row in collect_result.get("series_status") or []:
        status = str(row.get("status", ""))
        if status in {"PROVIDER_ERROR", "MAPPING_ERROR", "PERSISTENCE_ERROR"}:
            n += 1
    return n


def _classify_cycle(
    *,
    dry_run_only: bool,
    collect_result: dict[str, Any] | None,
    idempotency_status: str,
    readiness: dict[str, Any] | None,
    timed_out: bool,
    hard_error: str | None,
) -> str:
    if timed_out:
        return STATUS_FAILED
    if hard_error:
        return STATUS_FAILED
    if readiness and readiness.get("readiness_status") == STATUS_BLOCKED:
        return STATUS_BLOCKED
    if collect_result is None:
        return STATUS_FAILED
    run_status = collect_result.get("run_status")
    accepted = int(collect_result.get("n_observations_after", 0)) - int(
        collect_result.get("n_observations_before", 0)
    )
    if dry_run_only:
        if run_status == "FAILED":
            return STATUS_FAILED
        if run_status == "PARTIAL":
            return STATUS_PARTIAL
        return STATUS_COMPLETE
    if run_status == "FAILED" and accepted <= 0:
        return STATUS_FAILED
    if run_status == "PARTIAL" or idempotency_status == "FAIL":
        return STATUS_PARTIAL
    if accepted <= 0:
        return STATUS_NO_NEW_DATA
    return STATUS_COMPLETE


def _transition(prev: str | None, new: str) -> str:
    left = prev or "NONE"
    return f"{left}->{new}"


def _append_event(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, sort_keys=True) + "\n")


def _derive_state_from_run(run_doc: dict[str, Any], *, previous: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "kind": "FUTURE_UNSEEN_AUTOMATION_STATE",
        "automation_version": AUTOMATION_VERSION,
        "updated_at": run_doc["finished_at"],
        "last_run_id": run_doc["run_id"],
        "last_run_status": run_doc["status"],
        "last_as_of": run_doc.get("as_of"),
        "last_readiness_status": run_doc.get("readiness_status"),
        "last_readiness_reason": run_doc.get("readiness_reason"),
        "last_window_days": run_doc.get("window_days"),
        "last_eligible_series": run_doc.get("eligible_series"),
        "last_series_with_min_bars": run_doc.get("series_with_min_bars"),
        "last_hash_status": run_doc.get("hash_status"),
        "last_manifest_status": run_doc.get("manifest_status"),
        "last_gap_status": run_doc.get("gap_status"),
        "last_observations_accepted": run_doc.get("observations_accepted"),
        "last_store_after": run_doc.get("store_after"),
        "last_transition": run_doc.get("readiness_transition"),
        "VALIDATE_AUTHORIZED": False,
        "HUMAN_AUTHORIZATION_REQUIRED": bool(
            run_doc.get("readiness_status") == "READY"
            or (run_doc.get("readiness_transition") or "").endswith("->READY")
        ),
        "previous_readiness_status": (previous or {}).get("last_readiness_status"),
        "derived_from_run": run_doc["run_id"],
        "R3E_GATE": "PENDING_FUTURE_UNSEEN_DATA",
        "validation_command_executed": False,
        "effect_peeking_performed": False,
        "R4_STATUS": "BLOCKED",
        "R5_STATUS": "NOT_STARTED",
    }


def run_cycle(
    *,
    as_of: datetime | None = None,
    dry_run_only: bool = False,
    skip_idempotency_check: bool = False,
    output_dir: Path | None = None,
    strict: bool = False,
    max_retries: int = DEFAULT_MAX_RETRIES,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    lock_ttl_seconds: int = DEFAULT_LOCK_TTL_SECONDS,
    lock_path: Path | None = None,
    state_path: Path | None = None,
    runs_dir: Path | None = None,
    events_path: Path | None = None,
    collect_fn: CollectFn | None = None,
    readiness_fn: ReadinessFn | None = None,
    ops_fn: OpsFn | None = None,
    now_fn: NowFn | None = None,
    release_lock: bool = True,
) -> dict[str, Any]:
    """Execute one automation cycle. Never calls scientific validate."""
    ensure_dirs()
    now_fn = now_fn or (lambda: datetime.now(UTC))
    collect_fn = collect_fn or run_collect
    readiness_fn = readiness_fn or evaluate_readiness
    ops_fn = ops_fn or build_ops_report

    started = now_fn().astimezone(UTC)
    as_of_dt = as_of.astimezone(UTC) if as_of is not None else started
    if as_of is not None and as_of.tzinfo is None:
        raise ValueError("--as-of must be timezone-aware")

    run_id = f"fu_auto_{as_of_dt.strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}"
    lock = AutomationLock(
        lock_path or default_lock_path(),
        run_id=run_id,
        ttl_seconds=lock_ttl_seconds,
        now_fn=now_fn,
    )
    runs_root = runs_dir or default_runs_dir()
    state_file = state_path or default_state_path()
    events_file = events_path or default_events_path()
    run_dir = (output_dir or (runs_root / run_id)).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)

    deadline = time.monotonic() + max(1, int(timeout_seconds))
    previous_state = _read_json(state_file)
    previous_readiness = (previous_state or {}).get("last_readiness_status")

    def _timed_out() -> bool:
        return time.monotonic() >= deadline

    acquired, lock_reason = lock.acquire()
    if not acquired:
        finished = now_fn().astimezone(UTC)
        doc = {
            "kind": "FUTURE_UNSEEN_AUTOMATION_RUN",
            "automation_version": AUTOMATION_VERSION,
            "run_id": run_id,
            "started_at": _iso(started),
            "finished_at": _iso(finished),
            "as_of": _iso(as_of_dt),
            "status": STATUS_SKIPPED_LOCKED,
            "lock_reason": lock_reason,
            "dry_run_only": dry_run_only,
            "dry_run_candidates": None,
            "observations_accepted": 0,
            "observations_rejected": 0,
            "store_before": None,
            "store_after": None,
            "idempotency_status": "SKIPPED",
            "readiness_status": None,
            "readiness_reason": None,
            "window_days": None,
            "eligible_series": None,
            "series_with_min_bars": None,
            "hash_status": None,
            "manifest_status": None,
            "gap_status": None,
            "provider_failures": 0,
            "retries": {"max_retries": max_retries},
            "VALIDATE_AUTHORIZED": False,
            "HUMAN_AUTHORIZATION_REQUIRED": False,
            "validation_command_executed": False,
            "effect_peeking_performed": False,
            "R3E_GATE": "PENDING_FUTURE_UNSEEN_DATA",
            "R4_STATUS": "BLOCKED",
            "R5_STATUS": "NOT_STARTED",
        }
        _write_json(run_dir / "cycle_report.json", doc)
        return doc

    dry_result: dict[str, Any] | None = None
    collect_result: dict[str, Any] | None = None
    idem_result: dict[str, Any] | None = None
    readiness: dict[str, Any] | None = None
    ops_after: dict[str, Any] | None = None
    preflight: dict[str, Any] | None = None
    hard_error: str | None = None
    timed_out = False
    idempotency_status = "SKIPPED"
    status = STATUS_FAILED

    try:
        if _timed_out():
            timed_out = True
            raise TimeoutError("automation cycle timed out before preflight")

        preflight = _preflight(ops_fn=ops_fn)
        if preflight.get("blocked"):
            status = STATUS_BLOCKED
            # Still record readiness snapshot when possible for BLOCKED evidence
            try:
                readiness = readiness_fn(as_of=as_of_dt, strict=strict)
            except Exception as exc:  # noqa: BLE001
                hard_error = f"readiness_after_block:{type(exc).__name__}:{exc}"
        else:
            if _timed_out():
                timed_out = True
                raise TimeoutError("automation cycle timed out before dry-run")

            dry_dir = run_dir / "dry_run"
            dry_result = collect_fn(
                dry_run=True,
                as_of=as_of_dt,
                max_retries=max_retries,
                output_report_dir=dry_dir,
            )

            if dry_run_only:
                collect_result = dry_result
                ops_after = ops_fn(out_path=REPORTS_DIR / "ops_collection_report.json")
                readiness = readiness_fn(as_of=as_of_dt, strict=strict)
                idempotency_status = "SKIPPED"
            else:
                if _timed_out():
                    timed_out = True
                    raise TimeoutError("automation cycle timed out before collect")

                live_dir = run_dir / "collect"
                collect_result = collect_fn(
                    dry_run=False,
                    as_of=as_of_dt,
                    max_retries=max_retries,
                    output_report_dir=live_dir,
                )

                if not skip_idempotency_check:
                    if _timed_out():
                        timed_out = True
                        raise TimeoutError("automation cycle timed out before idempotency")
                    idem_dir = run_dir / "idempotency"
                    before_idem = int(collect_result.get("n_observations_after", 0))
                    idem_result = collect_fn(
                        dry_run=False,
                        as_of=as_of_dt,
                        max_retries=max_retries,
                        output_report_dir=idem_dir,
                    )
                    after_idem = int(idem_result.get("n_observations_after", 0))
                    accepted_idem = after_idem - before_idem
                    idempotency_status = "PASS" if accepted_idem == 0 else "FAIL"
                else:
                    idempotency_status = "SKIPPED"

                if _timed_out():
                    timed_out = True
                    raise TimeoutError("automation cycle timed out before ops-report")
                ops_after = ops_fn(out_path=REPORTS_DIR / "ops_collection_report.json")
                alias = REPORTS_DIR / "ops_report.json"
                if (REPORTS_DIR / "ops_collection_report.json").is_file():
                    alias.write_text(
                        (REPORTS_DIR / "ops_collection_report.json").read_text(encoding="utf-8"),
                        encoding="utf-8",
                    )

                if _timed_out():
                    timed_out = True
                    raise TimeoutError("automation cycle timed out before readiness")
                readiness = readiness_fn(as_of=as_of_dt, strict=strict)

            status = _classify_cycle(
                dry_run_only=dry_run_only,
                collect_result=collect_result,
                idempotency_status=idempotency_status,
                readiness=readiness,
                timed_out=False,
                hard_error=None,
            )
    except TimeoutError as exc:
        timed_out = True
        hard_error = str(exc)
        status = STATUS_FAILED
    except Exception as exc:  # noqa: BLE001
        hard_error = f"{type(exc).__name__}: {exc}"
        status = STATUS_FAILED
    finally:
        if release_lock:
            lock.release()

    finished = now_fn().astimezone(UTC)
    store_before = None if collect_result is None else collect_result.get("n_observations_before")
    store_after = None if collect_result is None else collect_result.get("n_observations_after")
    if collect_result is not None and not dry_run_only:
        observations_accepted = int(store_after or 0) - int(store_before or 0)
    else:
        observations_accepted = 0
    observations_rejected = 0
    if collect_result is not None:
        persist = collect_result.get("persist") or {}
        observations_rejected = int(persist.get("n_store_rejected") or 0)
        # Also count collector-stage rejections when present in series_status
        for row in collect_result.get("series_status") or []:
            observations_rejected += int(row.get("n_rejected") or 0)

    readiness_status = None if readiness is None else readiness.get("readiness_status")
    readiness_reason = None if readiness is None else readiness.get("readiness_reason")
    transition = _transition(
        str(previous_readiness) if previous_readiness else None,
        str(readiness_status) if readiness_status else "NONE",
    )

    human_auth_required = readiness_status == "READY" or transition.endswith("->READY")
    if human_auth_required:
        _append_event(
            events_file,
            {
                "event": "READINESS_BECAME_READY",
                "run_id": run_id,
                "at": _iso(finished),
                "transition": transition,
                "VALIDATE_AUTHORIZED": False,
                "HUMAN_AUTHORIZATION_REQUIRED": True,
                "message": (
                    "Readiness is READY. Scientific validate is NOT authorized. "
                    "Human authorization required before any validate execution."
                ),
            },
        )
    if readiness_status == "BLOCKED" or status == STATUS_BLOCKED:
        _append_event(
            events_file,
            {
                "event": "READINESS_OR_CYCLE_BLOCKED",
                "run_id": run_id,
                "at": _iso(finished),
                "transition": transition,
                "reason": readiness_reason or (preflight or {}).get("reason"),
                "VALIDATE_AUTHORIZED": False,
            },
        )

    doc: dict[str, Any] = {
        "kind": "FUTURE_UNSEEN_AUTOMATION_RUN",
        "automation_version": AUTOMATION_VERSION,
        "run_id": run_id,
        "started_at": _iso(started),
        "finished_at": _iso(finished),
        "as_of": _iso(as_of_dt),
        "status": status,
        "dry_run_only": dry_run_only,
        "skip_idempotency_check": skip_idempotency_check,
        "strict": strict,
        "timeout_seconds": timeout_seconds,
        "lock": lock.meta,
        "preflight": {
            "ok": bool((preflight or {}).get("ok")),
            "reason": (preflight or {}).get("reason"),
            "hash_status": (preflight or {}).get("hash_status"),
            "manifest_status": (preflight or {}).get("manifest_status"),
        },
        "dry_run_candidates": None if dry_result is None else dry_result.get("n_candidates"),
        "observations_accepted": observations_accepted,
        "observations_rejected": observations_rejected,
        "store_before": store_before,
        "store_after": store_after,
        "idempotency_status": idempotency_status,
        "collect_run_status": None if collect_result is None else collect_result.get("run_status"),
        "collect_run_id": None if collect_result is None else collect_result.get("collection_run_id"),
        "idempotency_run_id": None if idem_result is None else idem_result.get("collection_run_id"),
        "readiness_status": readiness_status,
        "readiness_reason": readiness_reason,
        "readiness_transition": transition,
        "window_days": None if readiness is None else readiness.get("window_days"),
        "eligible_series": None if readiness is None else readiness.get("eligible_series"),
        "series_with_min_bars": None if readiness is None else readiness.get("series_with_min_bars"),
        "required_series": None if readiness is None else readiness.get("required_series"),
        "required_min_bars": None if readiness is None else readiness.get("required_min_bars"),
        "hash_status": (
            None
            if readiness is None
            else readiness.get("hash_status", (preflight or {}).get("hash_status"))
        ),
        "manifest_status": (
            None
            if readiness is None
            else readiness.get("manifest_status", (preflight or {}).get("manifest_status"))
        ),
        "gap_status": None if readiness is None else readiness.get("gap_status"),
        "collector_status": None if readiness is None else readiness.get("collector_status"),
        "provider_failures": 0 if collect_result is None else _count_provider_failures(collect_result),
        "retries": {"max_retries": max_retries},
        "hard_error": hard_error,
        "timed_out": timed_out,
        "ops_n_observations_total": None
        if ops_after is None
        else ops_after.get("n_observations_total"),
        "VALIDATE_AUTHORIZED": False,
        "HUMAN_AUTHORIZATION_REQUIRED": human_auth_required,
        "validation_command_executed": False,
        "effect_peeking_performed": False,
        "R3E_GATE": "PENDING_FUTURE_UNSEEN_DATA",
        "ECONOMIC_INTERPRETATION_ALLOWED": False,
        "R4_STATUS": "BLOCKED",
        "R5_STATUS": "NOT_STARTED",
        "run_dir": str(run_dir),
    }
    _write_json(run_dir / "cycle_report.json", doc)
    if readiness is not None:
        _write_json(run_dir / "readiness_report.json", readiness)
        # Keep latest readiness alias current for operators
        _write_json(REPORTS_DIR / "readiness_report.json", readiness)

    # Do not overwrite historical automation_state with SKIPPED_LOCKED no-ops beyond last_skip note
    if status != STATUS_SKIPPED_LOCKED:
        state_doc = _derive_state_from_run(doc, previous=previous_state)
        _write_json(state_file, state_doc)
        doc["automation_state_path"] = str(state_file)
    else:
        doc["automation_state_path"] = str(state_file)

    # Touch manifests dir reference so tests can assert no scientific state mutation intent
    _ = MANIFESTS_DIR
    return doc
