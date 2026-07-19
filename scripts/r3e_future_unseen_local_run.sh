#!/usr/bin/env bash
# Local persistent host runner for R3E future-unseen automation.
# Loads protected env, validates paths, optional preflight, runs run-cycle.
# Does NOT invoke validate. Does NOT enable schedulers.
set -euo pipefail

log() { printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" | tee -a "${LOG_FILE:-/dev/null}" >&2; }

die() {
  log "ERROR: $*"
  exit 1
}

# Resolve WICK_ROOT: env > default $HOME/wick-r3e
WICK_ROOT="${WICK_ROOT:-${HOME}/wick-r3e}"
APP_DIR="${WICK_ROOT}/app"
CONFIG_ENV="${WICK_ENV_FILE:-${WICK_ROOT}/config/r3e-collector.env}"
LOG_DIR="${WICK_ROOT}/logs"
mkdir -p "${LOG_DIR}"
LOG_FILE="${LOG_DIR}/local_run_$(date -u +%Y%m%dT%H%M%SZ).log"

log "START wick_root=${WICK_ROOT}"

# Load protected config without printing values
if [[ -f "${CONFIG_ENV}" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "${CONFIG_ENV}"
  set +a
  log "ENV_LOADED path=${CONFIG_ENV}"
else
  log "ENV_MISSING path=${CONFIG_ENV} (continuing with process env)"
fi

WICK_ROOT="${WICK_ROOT:-${HOME}/wick-r3e}"
APP_DIR="${WICK_ROOT}/app"
DATA_DIR="${WICK_ROOT}/data/future_unseen"
REPORTS_DIR="${WICK_ROOT}/reports/r3e_future_unseen"

[[ -d "${APP_DIR}" ]] || die "missing app dir: ${APP_DIR}"
[[ -d "${DATA_DIR}" ]] || die "missing data dir: ${DATA_DIR}"
[[ -d "${REPORTS_DIR}" ]] || die "missing reports dir: ${REPORTS_DIR}"

# Refuse ephemeral roots (tests may set WICK_ALLOW_EPHEMERAL=1)
if [[ "${WICK_ALLOW_EPHEMERAL:-0}" != "1" ]]; then
  case "${WICK_ROOT}" in
    /tmp/*|/var/tmp/*|/workspace|/workspace/*)
      die "refusing ephemeral WICK_ROOT=${WICK_ROOT}"
      ;;
  esac
fi

cd "${APP_DIR}"

if [[ "${SKIP_PREFLIGHT:-0}" != "1" ]]; then
  if [[ -f "${APP_DIR}/scripts/r3e_future_unseen_local_healthcheck.sh" ]]; then
    WICK_ROOT="${WICK_ROOT}" ENV_FILE="${CONFIG_ENV}" \
      bash "${APP_DIR}/scripts/r3e_future_unseen_local_healthcheck.sh" || {
        ec=$?
        # DEGRADED(10) allowed to continue; BLOCKED/FAILED stop
        if ((ec >= 20)); then
          die "preflight blocked/failed exit=${ec}"
        fi
        log "PREFLIGHT_DEGRADED exit=${ec}"
      }
  fi
fi

# Prefer venv python
if [[ -x "${APP_DIR}/.venv/bin/python" ]]; then
  export PATH="${APP_DIR}/.venv/bin:${PATH}"
fi

EXTRA=()
if [[ "${FU_DRY_RUN_ONLY:-0}" == "1" ]]; then
  EXTRA+=(--dry-run-only)
fi
AS_OF_ARG=()
if [[ -n "${FU_AS_OF:-}" ]]; then
  AS_OF_ARG=(--as-of "${FU_AS_OF}")
fi

log "RUN_CYCLE begin"
set +e
python -m wick.r3e.future_unseen run-cycle --json "${AS_OF_ARG[@]}" "${EXTRA[@]}" "$@" | tee -a "${LOG_FILE}"
ec=${PIPESTATUS[0]}
set -e

# Summarize from automation_state without secrets
STATE="${REPORTS_DIR}/automation_state.json"
if [[ -f "${STATE}" ]]; then
  if command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1; then
    PY="$(command -v python3 || command -v python)"
    SUMMARY="$("${PY}" - <<PY
import json
from pathlib import Path
p=Path(${STATE@Q})
try:
  d=json.loads(p.read_text(encoding="utf-8"))
except Exception as e:
  print(f"state_error={e}")
else:
  print(
    "run_id="+str(d.get("last_run_id"))
    +" status="+str(d.get("last_run_status"))
    +" readiness="+str(d.get("last_readiness_status"))
    +" accepted="+str(d.get("last_observations_accepted"))
    +" store_after="+str(d.get("last_store_after"))
  )
PY
)"
    log "SUMMARY ${SUMMARY}"
  fi
fi

LOCK="${REPORTS_DIR}/automation.lock"
if [[ -f "${LOCK}" ]]; then
  log "LOCK_PRESENT path=${LOCK}"
else
  log "LOCK_ABSENT"
fi

log "END exit=${ec}"
exit "${ec}"
