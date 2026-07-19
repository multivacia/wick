#!/usr/bin/env bash
# Local persistent host healthcheck. Does NOT print secrets. Does NOT run validate.
set -euo pipefail

WICK_ROOT="${WICK_ROOT:-${HOME}/wick-r3e}"
APP_DIR="${WICK_ROOT}/app"
DATA_DIR="${WICK_ROOT}/data/future_unseen"
REPORTS_DIR="${WICK_ROOT}/reports/r3e_future_unseen"
LOG_DIR="${WICK_ROOT}/logs"
BACKUP_DIR="${WICK_ROOT}/backups"
CONFIG_DIR="${WICK_ROOT}/config"
ENV_FILE="${ENV_FILE:-${WICK_ROOT}/config/r3e-collector.env}"
MAX_RUN_AGE_SECONDS="${MAX_RUN_AGE_SECONDS:-7200}"
MIN_DISK_MB="${MIN_DISK_MB:-512}"

STATUS="HEALTHY"
REASONS=()

bump() {
  local next="$1"
  case "${STATUS}" in
    FAILED) ;;
    BLOCKED) [[ "${next}" == "FAILED" ]] && STATUS="${next}" ;;
    DEGRADED) [[ "${next}" == "FAILED" || "${next}" == "BLOCKED" ]] && STATUS="${next}" ;;
    HEALTHY) STATUS="${next}" ;;
  esac
}
note() { REASONS+=("$1"); }

# Ephemeral root check (skip only when explicitly allowed for offline tests)
if [[ "${WICK_ALLOW_EPHEMERAL:-0}" != "1" ]]; then
  case "${WICK_ROOT}" in
    /tmp/*|/var/tmp/*|/workspace|/workspace/*)
      note "EPHEMERAL_ROOT"
      bump FAILED
      ;;
  esac
fi

for p in "${APP_DIR}" "${DATA_DIR}" "${REPORTS_DIR}" "${LOG_DIR}" "${BACKUP_DIR}" "${CONFIG_DIR}"; do
  if [[ ! -d "${p}" ]]; then
    note "MISSING_DIR:${p}"
    bump FAILED
  fi
done

if [[ ! -f "${ENV_FILE}" ]]; then
  note "ENV_FILE_MISSING"
  bump BLOCKED
else
  mode="$(stat -c '%a' "${ENV_FILE}" 2>/dev/null || stat -f '%OLp' "${ENV_FILE}")"
  if [[ "${mode}" != "600" && "${mode}" != "400" && "${mode}" != "0400" ]]; then
    note "ENV_FILE_PERMS:${mode}"
    bump DEGRADED
  fi
fi

if ! command -v python >/dev/null 2>&1 && ! command -v python3 >/dev/null 2>&1; then
  note "PYTHON_MISSING"
  bump FAILED
fi

RUNNER="${APP_DIR}/scripts/r3e_future_unseen_local_run.sh"
CYCLE="${APP_DIR}/scripts/r3e_future_unseen_run_cycle.sh"
if [[ ! -f "${RUNNER}" || ! -f "${CYCLE}" ]]; then
  note "RUNNER_OR_CYCLE_MISSING"
  bump FAILED
fi
if grep -Eq 'wick\.r3e\.future_unseen[[:space:]]+validate' "${RUNNER}" "${CYCLE}" 2>/dev/null; then
  note "VALIDATE_INVOCATION"
  bump BLOCKED
fi

# Symlinks preferred
if [[ -L "${APP_DIR}/data/future_unseen" ]]; then
  :
elif [[ -d "${APP_DIR}/data/future_unseen" ]]; then
  note "APP_DATA_NOT_SYMLINK"
  bump DEGRADED
fi

LOCK="${REPORTS_DIR}/automation.lock"
if [[ -f "${LOCK}" ]]; then
  note "LOCK_PRESENT"
  bump DEGRADED
fi

STATE="${REPORTS_DIR}/automation_state.json"
if [[ -f "${STATE}" ]]; then
  PY="$(command -v python3 || command -v python || true)"
  if [[ -n "${PY}" ]]; then
    AGE="$("${PY}" - <<PY
import json
from datetime import datetime, timezone
from pathlib import Path
p=Path(${STATE@Q})
try:
  d=json.loads(p.read_text(encoding="utf-8"))
except Exception:
  print("BAD_JSON"); raise SystemExit(0)
ts=d.get("updated_at") or d.get("last_as_of")
if not ts:
  print("NO_TIMESTAMP"); raise SystemExit(0)
dt=datetime.fromisoformat(str(ts).replace("Z","+00:00"))
if dt.tzinfo is None: dt=dt.replace(tzinfo=timezone.utc)
print(int((datetime.now(timezone.utc)-dt).total_seconds()))
PY
)"
    if [[ "${AGE}" == "BAD_JSON" || "${AGE}" == "NO_TIMESTAMP" ]]; then
      note "STATE_${AGE}"
      bump DEGRADED
    elif [[ "${AGE}" =~ ^[0-9]+$ ]] && ((AGE > MAX_RUN_AGE_SECONDS)); then
      note "LAST_RUN_STALE_SECONDS:${AGE}"
      bump DEGRADED
    fi
  fi
else
  note "STATE_MISSING"
  bump DEGRADED
fi

if command -v df >/dev/null 2>&1; then
  AVAIL_MB="$(df -Pm "${WICK_ROOT}" 2>/dev/null | awk 'NR==2{print $4}')"
  if [[ "${AVAIL_MB}" =~ ^[0-9]+$ ]] && ((AVAIL_MB < MIN_DISK_MB)); then
    note "DISK_LOW_MB:${AVAIL_MB}"
    bump FAILED
  fi
fi

# Network reachability (best-effort; offline CI may be DEGRADED)
if command -v curl >/dev/null 2>&1; then
  if ! curl -sI --max-time 5 https://data-api.binance.vision >/dev/null 2>&1; then
    note "NETWORK_BINANCE_UNREACHABLE"
    bump DEGRADED
  fi
fi

# Scheduler prepared vs activated (Linux)
SCHED_PREPARED=false
SCHED_ACTIVATED=false
if [[ -f "${APP_DIR}/ops/local/systemd/wick-r3e-local-collector.timer" ]]; then
  SCHED_PREPARED=true
fi
if command -v systemctl >/dev/null 2>&1; then
  if systemctl --user is-enabled wick-r3e-local-collector.timer >/dev/null 2>&1; then
    SCHED_ACTIVATED=true
  fi
fi
if [[ "${SCHED_ACTIVATED}" == "true" ]]; then
  note "SCHEDULER_ACTIVATED"
  bump DEGRADED
fi
if [[ "${SCHED_PREPARED}" != "true" ]]; then
  note "SCHEDULER_TEMPLATES_MISSING"
  bump DEGRADED
fi

printf 'STATUS=%s\n' "${STATUS}"
printf 'SCHEDULER_PREPARED=%s\n' "${SCHED_PREPARED}"
printf 'SCHEDULER_ACTIVATED=%s\n' "${SCHED_ACTIVATED}"
if ((${#REASONS[@]} > 0)); then
  (IFS=','; printf 'REASONS=%s\n' "${REASONS[*]}")
else
  printf 'REASONS=none\n'
fi

case "${STATUS}" in
  HEALTHY) exit 0 ;;
  DEGRADED) exit 10 ;;
  BLOCKED) exit 20 ;;
  FAILED) exit 30 ;;
  *) exit 30 ;;
esac
