#!/usr/bin/env bash
# Operational healthcheck for HostGator VPS collector layout.
# Does NOT print secrets. Does NOT run validate.
set -euo pipefail

WICK_ROOT="${WICK_ROOT:-/srv/wick}"
APP_DIR="${WICK_ROOT}/app"
DATA_DIR="${WICK_ROOT}/data/future_unseen"
REPORTS_DIR="${WICK_ROOT}/reports/r3e_future_unseen"
LOG_DIR="${WICK_ROOT}/logs"
BACKUP_DIR="${WICK_ROOT}/backups"
ENV_FILE="${ENV_FILE:-/etc/wick/r3e-collector.env}"
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

require_dir() {
  local p="$1"
  if [[ ! -d "${p}" ]]; then
    note "MISSING_DIR:${p}"
    bump FAILED
  fi
}

require_dir "${APP_DIR}"
require_dir "${DATA_DIR}"
require_dir "${REPORTS_DIR}"
require_dir "${LOG_DIR}"
require_dir "${BACKUP_DIR}"

# Permissions: service dirs should not be world-writable
for p in "${DATA_DIR}" "${REPORTS_DIR}" "${LOG_DIR}" "${BACKUP_DIR}"; do
  if [[ -d "${p}" ]]; then
    mode="$(stat -c '%a' "${p}" 2>/dev/null || stat -f '%OLp' "${p}")"
    if [[ "${mode}" =~ [2367]$ ]]; then
      note "WORLD_WRITABLE:${p}:${mode}"
      bump DEGRADED
    fi
  fi
done

# Symlink layout (recommended): app paths point to durable roots
APP_DATA="${APP_DIR}/data/future_unseen"
APP_REPORTS="${APP_DIR}/reports/r3e_future_unseen"
if [[ -e "${APP_DATA}" && ! -d "${APP_DATA}" ]]; then
  note "APP_DATA_NOT_DIR"
  bump FAILED
fi
if [[ -L "${APP_DATA}" ]]; then
  target="$(readlink -f "${APP_DATA}" || true)"
  if [[ "${target}" != "$(readlink -f "${DATA_DIR}")" ]]; then
    note "APP_DATA_SYMLINK_MISMATCH"
    bump DEGRADED
  fi
elif [[ -d "${APP_DATA}" ]]; then
  note "APP_DATA_NOT_SYMLINK"
  bump DEGRADED
fi
if [[ -L "${APP_REPORTS}" ]]; then
  target="$(readlink -f "${APP_REPORTS}" || true)"
  if [[ "${target}" != "$(readlink -f "${REPORTS_DIR}")" ]]; then
    note "APP_REPORTS_SYMLINK_MISMATCH"
    bump DEGRADED
  fi
elif [[ -d "${APP_REPORTS}" ]]; then
  note "APP_REPORTS_NOT_SYMLINK"
  bump DEGRADED
fi

# Env file presence without dumping contents
if [[ ! -f "${ENV_FILE}" ]]; then
  note "ENV_FILE_MISSING"
  bump BLOCKED
else
  env_mode="$(stat -c '%a' "${ENV_FILE}" 2>/dev/null || stat -f '%OLp' "${ENV_FILE}")"
  if [[ "${env_mode}" != "600" && "${env_mode}" != "0400" && "${env_mode}" != "400" ]]; then
    note "ENV_FILE_PERMS:${env_mode}"
    bump DEGRADED
  fi
fi

# Python / run-cycle availability
if ! command -v python >/dev/null 2>&1 && ! command -v python3 >/dev/null 2>&1; then
  note "PYTHON_MISSING"
  bump FAILED
fi
CYCLE_SCRIPT="${APP_DIR}/scripts/r3e_future_unseen_run_cycle.sh"
if [[ ! -x "${CYCLE_SCRIPT}" && ! -f "${CYCLE_SCRIPT}" ]]; then
  note "RUN_CYCLE_SCRIPT_MISSING"
  bump FAILED
elif grep -Eq 'wick\.r3e\.future_unseen[[:space:]]+validate|[[:space:]]validate[[:space:]]*$' "${CYCLE_SCRIPT}"; then
  # Fail closed only on real validate invocation patterns (ignore comments)
  note "VALIDATE_INVOCATION_IN_RUNNER"
  bump BLOCKED
fi

# Lock
LOCK_FILE="${REPORTS_DIR}/automation.lock"
if [[ -f "${LOCK_FILE}" ]]; then
  note "LOCK_PRESENT"
  bump DEGRADED
fi

# Last run freshness from automation_state.json when present
STATE_FILE="${REPORTS_DIR}/automation_state.json"
if [[ -f "${STATE_FILE}" ]]; then
  if command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1; then
    PY="$(command -v python3 || command -v python)"
    AGE="$("${PY}" - <<PY
import json, time
from pathlib import Path
p = Path(${STATE_FILE@Q})
try:
    data = json.loads(p.read_text(encoding="utf-8"))
except Exception:
    print("BAD_JSON")
    raise SystemExit(0)
ts = data.get("updated_at") or data.get("last_as_of")
if not ts:
    print("NO_TIMESTAMP")
    raise SystemExit(0)
from datetime import datetime, timezone
s = str(ts).replace("Z", "+00:00")
dt = datetime.fromisoformat(s)
if dt.tzinfo is None:
    dt = dt.replace(tzinfo=timezone.utc)
age = int((datetime.now(timezone.utc) - dt).total_seconds())
print(age)
PY
)"
    if [[ "${AGE}" == "BAD_JSON" ]]; then
      note "STATE_JSON_INVALID"
      bump DEGRADED
    elif [[ "${AGE}" == "NO_TIMESTAMP" ]]; then
      note "STATE_TIMESTAMP_MISSING"
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

# Readiness snapshot (informational; NOT_READY is expected until window complete)
READY_FILE="${REPORTS_DIR}/readiness_report.json"
if [[ -f "${READY_FILE}" ]]; then
  if grep -q '"readiness_status"[[:space:]]*:[[:space:]]*"BLOCKED"' "${READY_FILE}"; then
    note "READINESS_BLOCKED"
    bump BLOCKED
  fi
fi

# Disk space on WICK_ROOT filesystem
if command -v df >/dev/null 2>&1; then
  AVAIL_MB="$(df -Pm "${WICK_ROOT}" 2>/dev/null | awk 'NR==2{print $4}')"
  if [[ "${AVAIL_MB}" =~ ^[0-9]+$ ]] && ((AVAIL_MB < MIN_DISK_MB)); then
    note "DISK_LOW_MB:${AVAIL_MB}"
    bump FAILED
  fi
fi

# Store non-empty check (existence of manifests dir is enough structurally)
if [[ -d "${DATA_DIR}/manifests" ]]; then
  :
else
  note "STORE_MANIFESTS_MISSING"
  bump DEGRADED
fi

printf 'STATUS=%s\n' "${STATUS}"
if ((${#REASONS[@]} > 0)); then
  printf 'REASONS=%s\n' "$((IFS=','; echo "${REASONS[*]}"))"
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
