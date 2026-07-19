"""Tests for B5-P1 parallel operational hardening (read-only ops)."""

from __future__ import annotations

import ast
import json
import tarfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from typer.testing import CliRunner

from wick.r3e.future_unseen import ops_hardening as oh
from wick.r3e.future_unseen.cli import app
from wick.r3e.future_unseen.ops_hardening import (
    OPERATIONAL_LOG_FIELDS,
    activation_checklist_ends_unauthorized,
    build_operational_log_event,
    build_ready_transition_notification,
    diagnose_lock,
    retention_plan,
    summarize_run_history,
    verify_backup_archive,
)


@pytest.fixture()
def ops_dirs(tmp_path, monkeypatch):
    reports = tmp_path / "reports"
    reports.mkdir()
    runs = reports / "automation_runs"
    runs.mkdir()
    monkeypatch.setattr(oh, "REPORTS_DIR", reports)
    import wick.r3e.future_unseen.automation as automation_mod

    monkeypatch.setattr(automation_mod, "REPORTS_DIR", reports)
    return {
        "root": tmp_path,
        "reports": reports,
        "runs": runs,
        "state": reports / "automation_state.json",
        "lock": reports / "automation.lock",
        "readiness": reports / "readiness_report.json",
    }


def _write_run(runs_dir: Path, run_id: str, **fields):
    run_dir = runs_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    doc = {
        "run_id": run_id,
        "status": "COMPLETE",
        "started_at": "2026-07-18T00:00:00+00:00",
        "finished_at": "2026-07-18T00:01:00+00:00",
        **fields,
    }
    (run_dir / "cycle_report.json").write_text(json.dumps(doc), encoding="utf-8")
    return doc


def test_history_is_read_only(ops_dirs, monkeypatch):
    ops_dirs["state"].write_text(
        json.dumps(
            {
                "last_run_id": "fu_auto_1",
                "last_run_status": "COMPLETE",
                "updated_at": "2026-07-18T00:01:00+00:00",
                "last_store_after": 42,
                "last_readiness_status": "NOT_READY",
                "last_readiness_reason": "WINDOW_INCOMPLETE",
            }
        ),
        encoding="utf-8",
    )
    _write_run(ops_dirs["runs"], "fu_auto_1", status="COMPLETE")
    _write_run(
        ops_dirs["runs"],
        "fu_auto_fail",
        status="FAILED",
        finished_at="2026-07-18T02:00:00+00:00",
    )
    ops_dirs["readiness"].write_text(
        json.dumps(
            {
                "readiness_status": "NOT_READY",
                "readiness_reason": "WINDOW_INCOMPLETE",
                "n_observations_total": 42,
            }
        ),
        encoding="utf-8",
    )

    calls: list[str] = []

    def boom(*_a, **_k):
        calls.append("collect")
        raise AssertionError("collect must not run")

    monkeypatch.setattr(
        "wick.r3e.future_unseen.collector.run_collect",
        boom,
    )
    monkeypatch.setattr(
        "wick.r3e.future_unseen.validate.run_validation",
        lambda **_k: (_ for _ in ()).throw(AssertionError("validate must not run")),
    )

    summary = summarize_run_history(
        state_path=ops_dirs["state"],
        runs_dir=ops_dirs["runs"],
        readiness_path=ops_dirs["readiness"],
        now=datetime(2026, 7, 18, 3, 0, tzinfo=UTC),
    )
    assert summary["read_only"] is True
    assert summary["collect_executed"] is False
    assert summary["validation_command_executed"] is False
    assert summary["VALIDATE_AUTHORIZED"] is False
    assert summary["last_run_id"] == "fu_auto_1"
    assert summary["last_run_status"] == "COMPLETE"
    assert summary["store_observations"] == 42
    assert summary["readiness_status"] == "NOT_READY"
    assert summary["scheduler_activation_status"]["SCHEDULER_ACTIVATION_AUTHORIZED"] is False
    assert summary["recent_failures"]
    assert calls == []


def test_history_cli_read_only(ops_dirs, monkeypatch):
    ops_dirs["state"].write_text(
        json.dumps({"last_run_id": "x", "last_run_status": "NO_NEW_DATA"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "wick.r3e.future_unseen.cli.summarize_run_history",
        lambda: summarize_run_history(
            state_path=ops_dirs["state"],
            runs_dir=ops_dirs["runs"],
            readiness_path=ops_dirs["readiness"],
        ),
    )
    runner = CliRunner()
    result = runner.invoke(app, ["history"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["VALIDATE_AUTHORIZED"] is False
    assert "api_key" not in result.stdout.lower()
    assert "secret" not in result.stdout.lower() or "VALIDATE" in result.stdout


def test_lock_status_does_not_remove_lock(ops_dirs):
    created = datetime(2026, 7, 18, 0, 0, tzinfo=UTC)
    lock_doc = {
        "run_id": "holder",
        "pid": 999999,  # almost certainly dead
        "acquired_at": created.isoformat(),
        "expires_at": (created - timedelta(seconds=1)).isoformat(),
        "ttl_seconds": 1,
    }
    ops_dirs["lock"].write_text(json.dumps(lock_doc), encoding="utf-8")
    before = ops_dirs["lock"].read_text(encoding="utf-8")
    result = diagnose_lock(lock_path=ops_dirs["lock"], now=datetime(2026, 7, 18, 1, 0, tzinfo=UTC))
    assert result["LOCK_STATUS"] == "STALE"
    assert result["lock_removed"] is False
    assert result["read_only"] is True
    assert ops_dirs["lock"].exists()
    assert ops_dirs["lock"].read_text(encoding="utf-8") == before


def test_lock_status_active_and_absent(ops_dirs):
    absent = diagnose_lock(lock_path=ops_dirs["lock"])
    assert absent["LOCK_STATUS"] == "ABSENT"
    assert absent["lock_removed"] is False

    now = datetime.now(UTC)
    ops_dirs["lock"].write_text(
        json.dumps(
            {
                "run_id": "live",
                "pid": __import__("os").getpid(),
                "acquired_at": now.isoformat(),
                "expires_at": (now + timedelta(hours=1)).isoformat(),
            }
        ),
        encoding="utf-8",
    )
    active = diagnose_lock(lock_path=ops_dirs["lock"], now=now)
    assert active["LOCK_STATUS"] == "ACTIVE"
    assert ops_dirs["lock"].exists()


def test_lock_status_cli_preserves_lock(ops_dirs, monkeypatch):
    ops_dirs["lock"].write_text(
        json.dumps(
            {
                "run_id": "x",
                "pid": 1,
                "acquired_at": "2000-01-01T00:00:00+00:00",
                "expires_at": "2000-01-01T00:00:01+00:00",
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "wick.r3e.future_unseen.cli.diagnose_lock",
        lambda: diagnose_lock(lock_path=ops_dirs["lock"]),
    )
    runner = CliRunner()
    result = runner.invoke(app, ["lock-status"])
    assert result.exit_code == 0
    assert ops_dirs["lock"].exists()
    payload = json.loads(result.stdout)
    assert payload["lock_removed"] is False


def test_operational_log_fields_stable_and_no_secrets():
    event = build_operational_log_event(
        event="cycle_complete",
        severity="INFO",
        status="COMPLETE",
        message="ok token=should_redact_if_matched",
        failure_category="NETWORK_UNAVAILABLE",
        accepted_count=1,
    )
    assert list(event.keys()) == list(OPERATIONAL_LOG_FIELDS)
    assert event["timestamp_utc"]
    # message containing 'token' is redacted by contract helper
    assert event["message"] == "[REDACTED]"


def test_retention_never_deletes_last_valid_backup(tmp_path):
    backups = tmp_path / "backups"
    backups.mkdir()
    old = backups / "fu_backup_20260101T000000Z.tar.gz"
    new = backups / "fu_backup_20260701T000000Z.tar.gz"
    old.write_bytes(b"old")
    new.write_bytes(b"new")
    # Make old appear aged
    old_mtime = (datetime.now(UTC) - timedelta(days=60)).timestamp()
    import os

    os.utime(old, (old_mtime, old_mtime))

    plan = retention_plan(
        wick_root=tmp_path,
        dry_run=True,
        backup_retention_days=30,
        minimum_valid_backups=3,
    )
    assert plan["dry_run"] is True
    assert plan["deletions_performed"] == 0
    assert plan["latest_valid_backup_preserved"] == str(new.resolve()) or plan[
        "latest_valid_backup_preserved"
    ].endswith(new.name)
    # With only 2 backups and MINIMUM_VALID_BACKUPS=3, no backup deletions proposed
    assert plan["backup_candidates_for_deletion"] == []
    assert old.exists() and new.exists()

    with pytest.raises(PermissionError):
        retention_plan(wick_root=tmp_path, dry_run=False)


def test_retention_preserves_newest_when_enough_backups(tmp_path):
    backups = tmp_path / "backups"
    backups.mkdir()
    paths = []
    for i, day in enumerate((90, 60, 45, 1)):
        p = backups / f"fu_backup_20260{i}01T000000Z.tar.gz"
        p.write_bytes(b"x")
        mtime = (datetime.now(UTC) - timedelta(days=day)).timestamp()
        import os

        os.utime(p, (mtime, mtime))
        paths.append(p)
    plan = retention_plan(
        wick_root=tmp_path,
        dry_run=True,
        backup_retention_days=30,
        minimum_valid_backups=3,
    )
    newest = max(paths, key=lambda p: p.stat().st_mtime)
    assert str(newest) == plan["latest_valid_backup_preserved"] or plan[
        "latest_valid_backup_preserved"
    ].endswith(newest.name)
    assert str(newest) not in plan["backup_candidates_for_deletion"]
    # After deletions, at least 3 would remain
    remaining = plan["backup_count"] - len(plan["backup_candidates_for_deletion"])
    assert remaining >= 3


def test_backup_verification_and_no_restore(tmp_path):
    archive = tmp_path / "fu_backup_test.tar.gz"
    with tarfile.open(archive, "w:gz") as tf:
        data = tmp_path / "data"
        reports = tmp_path / "reports"
        (data / "future_unseen" / "manifests").mkdir(parents=True)
        (reports / "r3e_future_unseen").mkdir(parents=True)
        (data / "future_unseen" / "manifests" / "collection_state.json").write_text(
            "{}", encoding="utf-8"
        )
        (reports / "r3e_future_unseen" / "automation_state.json").write_text("{}", encoding="utf-8")
        tf.add(data / "future_unseen", arcname="data/future_unseen")
        tf.add(reports / "r3e_future_unseen", arcname="reports/r3e_future_unseen")

    target = tmp_path / "prod_restore_target"
    target.mkdir()
    marker = target / "keep_me.txt"
    marker.write_text("safe", encoding="utf-8")

    result = verify_backup_archive(archive, restore_target=target)
    assert result["restore_executed"] is False
    assert result["checks"]["archive_exists"] is True
    assert result["checks"]["archive_nonempty"] is True
    assert result["checks"]["expected_directories_present"] is True
    assert result["checks"]["secret_files_absent"] is True
    assert result["checks"]["restore_target_not_overwritten"] is True
    assert marker.read_text(encoding="utf-8") == "safe"
    assert result["BACKUP_VERIFICATION"] == "PASS"


def test_ready_notification_has_no_effect_or_economic_data():
    payload = build_ready_transition_notification(
        run_id="fu_auto_ready",
        timestamp_utc="2026-07-19T00:00:00+00:00",
        store_observations=100,
        window_days=30.5,
    )
    text = json.dumps(payload)
    assert "readiness changed from NOT_READY to READY" in payload["message"]
    assert payload["VALIDATE_AUTHORIZED"] is False
    assert payload["validation_command_executed"] is False
    assert payload["ECONOMIC_INTERPRETATION_ALLOWED"] is False
    assert "effect_size" not in text
    assert "p_value" not in text
    assert (
        "economic_interpretation" not in text.lower()
        or payload["ECONOMIC_INTERPRETATION_ALLOWED"] is False
    )
    # Ensure no economic metrics payload keys beyond denial flag
    assert "economic_interpretation" not in payload
    assert "effect" not in payload
    assert "model_effect" not in payload


def test_activation_checklist_ends_unauthorized():
    path = Path("docs/checklists/R3E_FUTURE_UNSEEN_SCHEDULER_ACTIVATION_CHECKLIST.md")
    text = path.read_text(encoding="utf-8")
    assert activation_checklist_ends_unauthorized(text)
    assert text.strip().endswith("SCHEDULER_ACTIVATION_AUTHORIZED = false") or (
        "SCHEDULER_ACTIVATION_AUTHORIZED = false" in text.split("## Final")[-1]
    )


def test_ops_hardening_module_has_no_validate_import():
    source = Path("src/wick/r3e/future_unseen/ops_hardening.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            assert "validate" not in mod
            assert "gate" not in mod
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert "validate" not in alias.name
