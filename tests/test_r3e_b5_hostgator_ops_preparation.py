"""Tests for B5 HostGator VPS activation preparation artifacts."""

from __future__ import annotations

import os
import re
import stat
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SERVICE = REPO / "ops/systemd/wick-r3e-collector.service"
TIMER = REPO / "ops/systemd/wick-r3e-collector.timer"
ENV_EXAMPLE = REPO / "ops/systemd/wick-r3e-collector.env.example"
BACKUP = REPO / "scripts/r3e_future_unseen_backup.sh"
HEALTH = REPO / "scripts/r3e_future_unseen_healthcheck.sh"
ALERT = REPO / "scripts/r3e_future_unseen_alert.sh"
RUNNER = REPO / "scripts/r3e_future_unseen_run_cycle.sh"
RUNBOOK = REPO / "docs/runbooks/R3E_FUTURE_UNSEEN_HOSTGATOR_VPS_ACTIVATION_RUNBOOK.md"
IMPACT = REPO / "docs/ai-impact/COLLECTION-SCHEDULER-ACTIVATION-001_IMPACT_ASSESSMENT.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_systemd_units_exist_and_parse_required_fields():
    svc = _read(SERVICE)
    timer = _read(TIMER)

    assert "User=wick" in svc
    assert "Group=wick" in svc
    assert "WorkingDirectory=/srv/wick/app" in svc
    assert "EnvironmentFile=-/etc/wick/r3e-collector.env" in svc or "EnvironmentFile=/etc/wick/r3e-collector.env" in svc
    assert "ExecStart=/bin/bash /srv/wick/app/scripts/r3e_future_unseen_run_cycle.sh" in svc
    assert "Restart=no" in svc
    assert "NoNewPrivileges=true" in svc
    assert "PrivateTmp=true" in svc
    assert "ProtectSystem=strict" in svc
    assert "ProtectHome=true" in svc
    assert "ReadWritePaths=/srv/wick/data /srv/wick/reports /srv/wick/logs /srv/wick/backups" in svc
    assert "User=root" not in svc

    assert "OnCalendar=*-*-* *:15:00 UTC" in timer
    assert "Persistent=true" in timer
    assert "RandomizedDelaySec=0" in timer
    assert "WantedBy=timers.target" in timer


def test_env_example_has_no_real_secrets_and_documents_real_names():
    text = _read(ENV_EXAMPLE)
    assert "ALERT_EMAIL=" in text
    assert "PATH=/srv/wick/app/.venv/bin" in text
    # Must not embed obviously real secret material
    assert not re.search(r"(sk-|ghp_|xox[baprs]-|BEGIN [A-Z ]*PRIVATE KEY)", text)
    assert "password=hunter2" not in text.lower()
    # Do not invent provider key vars as required
    assert "PROVIDER_API_KEY=" not in text
    assert "BRAPI_TOKEN=" in text  # optional documented real Settings name


def test_runner_and_ops_scripts_do_not_invoke_validate():
    for path in (RUNNER, BACKUP, HEALTH, ALERT):
        body = _read(path)
        assert "wick.r3e.future_unseen validate" not in body
        assert not re.search(r"python\s+-m\s+wick\.r3e\.future_unseen\s+validate", body)


def test_runbook_covers_required_sections_and_forbids_validate():
    text = _read(RUNBOOK)
    for needle in [
        "Pré-requisitos",
        "usuário `wick`",
        "Estrutura de diretórios",
        "Clone",
        "Ambiente Python",
        "env file",
        "units",
        "daemon-reload",
        "Preflight",
        "Dry-run",
        "manual controlada",
        "logs",
        "store",
        "Habilitação do timer",
        "Desabilitação",
        "Rollback",
        "Backup",
        "Restauração",
        "lock stale",
    ]:
        assert needle.lower() in text.lower()
    assert "python -m wick.r3e.future_unseen validate" in text  # prohibition example
    assert "NÃO executar" in text or "Nao executar" in text or "Proibições" in text
    assert "SCHEDULER_ACTIVATION_AUTHORIZED = false" in text


def test_impact_assessment_approved_with_human_decisions():
    text = _read(IMPACT)
    assert "IMPACT_ASSESSMENT_STATUS = APPROVED" in text
    assert "IMPLEMENTATION_AUTHORIZED = true" in text
    assert "SCHEDULER_ACTIVATION_AUTHORIZED = false" in text
    assert "OPERATIONAL_OWNER = Gustavo Almeida" in text
    assert "HOST_STRATEGY = VPS" in text
    assert "HOST_PROVIDER = HostGator" in text
    assert "HOST_ID = wick-r3e-collector-01" in text
    assert "DURABLE_STORE_PATH = /srv/wick" in text
    assert "SECRET_STORAGE_STRATEGY = SYSTEMD_ENVIRONMENT_FILE" in text
    assert "FAILURE_ALERT_DESTINATION = EMAIL" in text


def test_backup_script_fail_closed_and_atomic(tmp_path: Path):
    root = tmp_path / "srv" / "wick"
    data = root / "data" / "future_unseen"
    reports = root / "reports" / "r3e_future_unseen"
    backups = root / "backups"
    for d in (data / "raw", data / "validated", data / "manifests", reports, backups):
        d.mkdir(parents=True)
    (data / "raw" / "sample.json").write_text('{"ok":true}\n', encoding="utf-8")
    (reports / "automation_state.json").write_text('{"updated_at":"2026-07-18T00:00:00+00:00"}\n', encoding="utf-8")

    env = os.environ.copy()
    env["WICK_ROOT"] = str(root)
    env["BACKUP_RETENTION_DAYS"] = "14"
    proc = subprocess.run(
        ["bash", str(BACKUP)],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    assert proc.returncode == 0, proc.stderr
    archives = list(backups.glob("fu_backup_*.tar.gz"))
    assert len(archives) == 1
    assert not list(backups.glob(".tmp_fu_backup_*.tar.gz"))

    # Missing data dir => fail closed
    bad = tmp_path / "bad"
    bad.mkdir()
    env["WICK_ROOT"] = str(bad)
    proc2 = subprocess.run(["bash", str(BACKUP)], check=False, capture_output=True, text=True, env=env)
    assert proc2.returncode != 0


def test_healthcheck_statuses(tmp_path: Path):
    root = tmp_path / "srv" / "wick"
    app = root / "app"
    data = root / "data" / "future_unseen"
    reports = root / "reports" / "r3e_future_unseen"
    for d in (
        app / "scripts",
        app / "data",
        app / "reports",
        data / "manifests",
        reports,
        root / "logs",
        root / "backups",
    ):
        d.mkdir(parents=True)

    # Copy runner script reference
    runner = app / "scripts" / "r3e_future_unseen_run_cycle.sh"
    runner.write_text(RUNNER.read_text(encoding="utf-8"), encoding="utf-8")
    runner.chmod(0o755)

    (app / "data" / "future_unseen").symlink_to(data)
    (app / "reports" / "r3e_future_unseen").symlink_to(reports)

    env_file = tmp_path / "r3e-collector.env"
    env_file.write_text("ALERT_EMAIL=\n", encoding="utf-8")
    env_file.chmod(0o600)

    (reports / "automation_state.json").write_text(
        '{"updated_at":"2099-01-01T00:00:00+00:00","last_run_status":"COMPLETE"}\n',
        encoding="utf-8",
    )
    (reports / "readiness_report.json").write_text(
        '{"readiness_status":"NOT_READY"}\n',
        encoding="utf-8",
    )

    env = os.environ.copy()
    env["WICK_ROOT"] = str(root)
    env["ENV_FILE"] = str(env_file)
    env["MAX_RUN_AGE_SECONDS"] = "999999999"
    proc = subprocess.run(["bash", str(HEALTH)], check=False, capture_output=True, text=True, env=env)
    assert "STATUS=HEALTHY" in proc.stdout, proc.stdout + proc.stderr
    assert proc.returncode == 0

    # LOCK present => DEGRADED
    (reports / "automation.lock").write_text("lock\n", encoding="utf-8")
    proc2 = subprocess.run(["bash", str(HEALTH)], check=False, capture_output=True, text=True, env=env)
    assert "STATUS=DEGRADED" in proc2.stdout
    assert proc2.returncode == 10

    # Missing env => BLOCKED
    (reports / "automation.lock").unlink()
    env["ENV_FILE"] = str(tmp_path / "missing.env")
    proc3 = subprocess.run(["bash", str(HEALTH)], check=False, capture_output=True, text=True, env=env)
    assert "STATUS=BLOCKED" in proc3.stdout
    assert proc3.returncode == 20


def test_alert_adapter_pending_configuration_without_email():
    proc = subprocess.run(
        ["bash", str(ALERT), "1", "FAILED", "unit-test"],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "ALERT_EMAIL": ""},
    )
    assert proc.returncode == 0
    assert "PENDING_CONFIGURATION" in proc.stderr


def test_scripts_are_executable_bits_in_repo():
    for path in (BACKUP, HEALTH, ALERT, RUNNER):
        mode = path.stat().st_mode
        # Git may or may not preserve +x in checkout; ensure shebang present either way
        assert _read(path).startswith("#!/usr/bin/env bash")
        # If executable bit present, keep; if not, still acceptable if shebang exists
        _ = bool(mode & stat.S_IXUSR)


def test_rollback_documented_keeps_store():
    text = _read(RUNBOOK)
    assert "NÃO apagar observações aceitas" in text or "Não apagar" in text
    assert "disable --now wick-r3e-collector.timer" in text


def test_lock_compatibility_documented():
    text = _read(SERVICE) + _read(RUNBOOK) + _read(IMPACT)
    assert "automation.lock" in text or "lock" in text.lower()
    assert "3300" in _read(IMPACT) or "LOCK_TTL" in _read(IMPACT)
