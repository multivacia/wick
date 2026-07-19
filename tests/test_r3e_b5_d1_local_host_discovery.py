"""Tests for B5-D1 read-only local host discovery preparation."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SH = REPO / "scripts/r3e_local_host_discovery.sh"
PS1 = REPO / "scripts/r3e_local_host_discovery.ps1"
RUNBOOK = REPO / "docs/runbooks/R3E_LOCAL_HOST_DISCOVERY_RUNBOOK.md"
FINAL_MERGE = (
    REPO
    / "reports/ai-implementation/R3E-B5-LOCAL-PERSISTENT-HOST_PREPARATION_FINAL_MERGE_HANDOFF.md"
)

REQUIRED_FIELDS = [
    "DISCOVERY_EXECUTED_AT_UTC",
    "OPERATING_SYSTEM",
    "OPERATING_SYSTEM_VERSION",
    "HOSTNAME",
    "CURRENT_USERNAME",
    "HOME_DIRECTORY",
    "SHELL",
    "POWERSHELL_VERSION",
    "PYTHON_COMMAND",
    "PYTHON_VERSION",
    "GIT_VERSION",
    "CPU",
    "MEMORY_TOTAL",
    "DISK_TOTAL",
    "DISK_AVAILABLE",
    "FILESYSTEM_TYPE",
    "TIMEZONE",
    "NETWORK_AVAILABLE",
    "OUTBOUND_HTTPS_AVAILABLE",
    "SCHEDULER_MECHANISM",
    "TASK_SCHEDULER_AVAILABLE",
    "SYSTEMD_AVAILABLE",
    "CRON_AVAILABLE",
    "LOCAL_ROOT_CANDIDATE",
    "LOCAL_ROOT_EXISTS",
    "LOCAL_ROOT_WRITABLE",
    "REPOSITORY_PATH",
    "REPOSITORY_PATH_EXISTS",
    "CONFIG_PATH_CANDIDATE",
    "BACKUP_PATH_CANDIDATE",
    "HOST_DISCOVERY_STATUS",
    "RECOMMENDED_LOCAL_ROOT",
    "RECOMMENDED_SCHEDULER_MECHANISM",
    "BLOCKERS",
    "WARNINGS",
    "NEXT_ACTION",
]

FORBIDDEN_PATTERNS = [
    r"apt-get\s+install",
    r"yum\s+install",
    r"pip\s+install",
    r"npm\s+install",
    r"choco\s+install",
    r"winget\s+install",
    r"Register-ScheduledTask",
    r"systemctl\s+enable",
    r"crontab\s+-e",
    r"wick\.r3e\.future_unseen\s+validate",
    r"wick\.r3e\.future_unseen\s+run-cycle",
    r"sudo\s+",
    r"Start-Process\s+.*-Verb\s+RunAs",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_scripts_exist_and_readonly_static_guards():
    assert SH.is_file()
    assert PS1.is_file()
    for path in (SH, PS1):
        body = _read(path)
        for pat in FORBIDDEN_PATTERNS:
            assert re.search(pat, body, flags=re.I) is None, f"{path.name} matched {pat}"
        # must not dump env contents / history
        assert "printenv" not in body
        assert "Get-ChildItem Env:" not in body and "Get-ChildItem env:" not in body
        assert "HISTFILE" not in body
        assert "cat /etc/" not in body


def test_scripts_require_no_elevated_privileges_guards():
    sh = _read(SH)
    ps1 = _read(PS1)
    assert "refuse to run as root" in sh
    assert "Administrator" in ps1
    assert "id -u" in sh


def test_bash_discovery_produces_all_required_fields(tmp_path: Path):
    out = tmp_path / "R3E_LOCAL_HOST_DISCOVERY_RESULT.md"
    env = os.environ.copy()
    env["R3E_DISCOVERY_OUT"] = str(out)
    proc = subprocess.run(
        ["bash", str(SH)],
        check=False,
        capture_output=True,
        text=True,
        env=env,
        cwd=str(REPO),
    )
    assert proc.returncode == 0, proc.stderr
    assert out.is_file()
    text = out.read_text(encoding="utf-8")
    for field in REQUIRED_FIELDS:
        assert re.search(rf"^{field}\s*=", text, flags=re.M), field
    assert "NEXT_ACTION = submit this file for readiness review" in text
    # no secret-looking dumps
    assert "AWS_SECRET" not in text
    assert "PRIVATE KEY" not in text
    assert "password=" not in text.lower()


def test_runbook_documents_windows_and_linux_commands():
    text = _read(RUNBOOK)
    assert "Set-ExecutionPolicy -Scope Process Bypass" in text
    assert (
        r".\scripts\r3e_local_host_discovery.ps1" in text
        or "./scripts/r3e_local_host_discovery.ps1" in text
    )
    assert "r3e_local_host_discovery.sh" in text
    assert "validate" in text.lower()
    assert "SCHEDULER_ACTIVATION_AUTHORIZED = false" in text


def test_final_merge_handoff_records_pr27():
    text = _read(FINAL_MERGE)
    assert "PR27_FINAL_HEAD = 046fcd71b220089a3b450bfc1e20c3e9a4dbaee3" in text
    assert "PR27_MERGE_COMMIT = 134f066b8d8fe0a1b3f935d0a665195367d40f54" in text
    assert "HOST_STRATEGY = LOCAL_PERSISTENT_HOST" in text
    assert "SCHEDULER_ACTIVATED = false" in text
    assert "VALIDATION_COMMAND_EXECUTED = false" in text


def test_powershell_script_mentions_required_fields():
    body = _read(PS1)
    for field in REQUIRED_FIELDS:
        assert field in body
