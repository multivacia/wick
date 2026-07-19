"""Tests for B5 local persistent host preparation artifacts."""

from __future__ import annotations

import os
import re
import stat
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LOCAL_ENV = REPO / "ops/local/wick-r3e-collector.env.example"
LOCAL_RUN = REPO / "scripts/r3e_future_unseen_local_run.sh"
LOCAL_HEALTH = REPO / "scripts/r3e_future_unseen_local_healthcheck.sh"
LOCAL_RUN_PS1 = REPO / "scripts/r3e_future_unseen_local_run.ps1"
LOCAL_HEALTH_PS1 = REPO / "scripts/r3e_future_unseen_local_healthcheck.ps1"
WIN_REG = REPO / "ops/windows/register-wick-r3e-collector-task.ps1"
WIN_UNREG = REPO / "ops/windows/unregister-wick-r3e-collector-task.ps1"
LOCAL_TIMER = REPO / "ops/local/systemd/wick-r3e-local-collector.timer"
LOCAL_SERVICE = REPO / "ops/local/systemd/wick-r3e-local-collector.service"
LOCAL_RUNBOOK = REPO / "docs/runbooks/R3E_FUTURE_UNSEEN_LOCAL_ACTIVATION_RUNBOOK.md"
MIG_RUNBOOK = REPO / "docs/runbooks/R3E_FUTURE_UNSEEN_LOCAL_TO_HOSTGATOR_MIGRATION.md"
DISCOVERY = REPO / "docs/operations/R3E_LOCAL_PERSISTENT_HOST_DISCOVERY.md"
IMPACT = REPO / "docs/ai-impact/COLLECTION-SCHEDULER-ACTIVATION-001_IMPACT_ASSESSMENT.md"
BACKUP = REPO / "scripts/r3e_future_unseen_backup.sh"
CYCLE = REPO / "scripts/r3e_future_unseen_run_cycle.sh"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_local_paths_and_discovery():
    text = _read(DISCOVERY)
    assert "LOCAL_OPERATING_SYSTEM = Linux" in text
    assert "DURABLE_STORE_PATH = $HOME/wick-r3e" in text
    assert "DISK_BACKEND = overlay" in text
    assert "cursor_agent_environment_not_operational_host" in text


def test_impact_strategy_transition_preserves_hostgator_history():
    text = _read(IMPACT)
    assert "HOST_STRATEGY = LOCAL_PERSISTENT_HOST" in text
    assert "HOSTGATOR_VPS_STATUS = DEFERRED_FUTURE_MIGRATION" in text
    assert "PREVIOUS_HOST_PROVIDER = HostGator" in text
    assert "SCHEDULER_ACTIVATION_AUTHORIZED = false" in text
    assert "SCHEDULER_ACTIVATED = false" in text


def test_local_env_example_has_no_real_secrets():
    text = _read(LOCAL_ENV)
    assert "WICK_ROOT=$HOME/wick-r3e" in text
    assert "ALERT_MODE=LOCAL_LOG" in text
    assert not re.search(r"(sk-|ghp_|xox[baprs]-|BEGIN [A-Z ]*PRIVATE KEY)", text)
    assert "PROVIDER_API_KEY=" not in text


def test_scripts_do_not_invoke_validate():
    for path in (LOCAL_RUN, LOCAL_HEALTH, LOCAL_RUN_PS1, LOCAL_HEALTH_PS1, CYCLE, BACKUP):
        body = _read(path)
        assert not re.search(r"python\s+-m\s+wick\.r3e\.future_unseen\s+validate", body)
        # Allow mention only inside detection/guard patterns, not as an executed command.
        for line in body.splitlines():
            if (
                "wick.r3e.future_unseen validate" in line
                or "wick.r3e.future_unseen[[:space:]]+validate" in line
            ):
                assert any(
                    tok in line
                    for tok in ("Pattern", "grep", "VALIDATE_INVOCATION", "NÃO", "NOT", "#")
                ), line


def test_local_timer_utc_minute_15_and_not_enabled_in_docs():
    timer = _read(LOCAL_TIMER)
    assert "OnCalendar=*-*-* *:15:00 UTC" in timer
    runbook = _read(LOCAL_RUNBOOK)
    assert (
        "NÃO enable nesta fase" in runbook
        or "Nao enable" in runbook.lower()
        or "não enable" in runbook.lower()
    )
    assert "SCHEDULER_ACTIVATION_AUTHORIZED = false" in runbook


def test_windows_task_scripts_prepared_not_auto():
    reg = _read(WIN_REG)
    assert "Wick-R3E-Future-Unseen-Collector" in reg
    assert "DO NOT run automatically" in reg
    assert "RunOnlyIfNetworkAvailable" in reg
    assert "IgnoreNew" in reg  # no overlap
    assert WIN_UNREG.is_file()


def test_local_systemd_service_uses_home_layout():
    svc = _read(LOCAL_SERVICE)
    assert "WorkingDirectory=%h/wick-r3e/app" in svc
    assert "r3e_future_unseen_local_run.sh" in svc
    assert "User=root" not in svc


def test_migration_runbook_covers_freeze_and_no_dual_schedulers():
    text = _read(MIG_RUNBOOK)
    assert "Congelar scheduler local" in text or "disable --now" in text
    assert " Evitar coleta simultânea" in text or "coleta simultânea" in text
    assert "validate" in text.lower()
    assert "HostGator" in text


def test_local_healthcheck_and_backup_with_home_layout(tmp_path: Path):
    root = tmp_path / "wick-r3e"
    app = root / "app"
    data = root / "data" / "future_unseen"
    reports = root / "reports" / "r3e_future_unseen"
    for d in (
        app / "scripts",
        app / "ops" / "local" / "systemd",
        app / "data",
        app / "reports",
        data / "manifests",
        reports,
        root / "logs",
        root / "backups",
        root / "config",
    ):
        d.mkdir(parents=True)

    (app / "scripts" / "r3e_future_unseen_local_run.sh").write_text(
        LOCAL_RUN.read_text(encoding="utf-8"), encoding="utf-8"
    )
    (app / "scripts" / "r3e_future_unseen_run_cycle.sh").write_text(
        CYCLE.read_text(encoding="utf-8"), encoding="utf-8"
    )
    (app / "ops" / "local" / "systemd" / "wick-r3e-local-collector.timer").write_text(
        LOCAL_TIMER.read_text(encoding="utf-8"), encoding="utf-8"
    )
    (app / "data" / "future_unseen").symlink_to(data)
    (app / "reports" / "r3e_future_unseen").symlink_to(reports)
    env_file = root / "config" / "r3e-collector.env"
    env_file.write_text("ALERT_MODE=LOCAL_LOG\n", encoding="utf-8")
    env_file.chmod(0o600)
    (reports / "automation_state.json").write_text(
        '{"updated_at":"2099-01-01T00:00:00+00:00","last_run_status":"COMPLETE"}\n',
        encoding="utf-8",
    )
    (data / "raw" / "x.json").parent.mkdir(exist_ok=True)
    (data / "raw" / "x.json").write_text("{}\n", encoding="utf-8")

    env = os.environ.copy()
    env["WICK_ROOT"] = str(root)
    env["ENV_FILE"] = str(env_file)
    env["MAX_RUN_AGE_SECONDS"] = "999999999"
    env["WICK_ALLOW_EPHEMERAL"] = "1"
    # Avoid network flake in CI: healthcheck treats unreachable as DEGRADED only
    proc = subprocess.run(
        ["bash", str(LOCAL_HEALTH)], check=False, capture_output=True, text=True, env=env
    )
    assert "STATUS=" in proc.stdout
    assert proc.returncode in {0, 10}, proc.stdout + proc.stderr
    assert "SCHEDULER_ACTIVATED=false" in proc.stdout

    env["BACKUP_RETENTION_DAYS"] = "14"
    env["WICK_ALLOW_EPHEMERAL"] = "1"
    b = subprocess.run(["bash", str(BACKUP)], check=False, capture_output=True, text=True, env=env)
    assert b.returncode == 0, b.stderr
    assert list((root / "backups").glob("fu_backup_*.tar.gz"))


def test_local_runner_refuses_workspace_ephemeral(tmp_path: Path):
    # Simulate missing dirs under /workspace-like refusal via env pointing to /tmp
    env = os.environ.copy()
    env["WICK_ROOT"] = "/tmp/wick-r3e-should-fail"
    proc = subprocess.run(
        ["bash", str(LOCAL_RUN)], check=False, capture_output=True, text=True, env=env
    )
    assert proc.returncode != 0
    assert "ephemeral" in (proc.stderr + proc.stdout).lower() or "ERROR" in proc.stderr


def test_gitignore_ignores_local_env_secrets():
    gi = _read(REPO / ".gitignore")
    assert "r3e-collector.env" in gi


def test_scripts_have_shebang_or_ps1_header():
    assert _read(LOCAL_RUN).startswith("#!/usr/bin/env bash")
    assert _read(LOCAL_HEALTH).startswith("#!/usr/bin/env bash")
    assert "ErrorActionPreference" in _read(LOCAL_RUN_PS1)
    # executable bit preferred
    mode = LOCAL_RUN.stat().st_mode
    _ = bool(mode & stat.S_IXUSR)
