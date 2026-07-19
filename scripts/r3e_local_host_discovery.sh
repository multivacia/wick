#!/usr/bin/env bash
# Read-only local host discovery for B5-D1.
# Does NOT install packages, require root, register schedulers, run collection,
# run validate, print secrets, or transmit results.
set -euo pipefail

OUT="${R3E_DISCOVERY_OUT:-./R3E_LOCAL_HOST_DISCOVERY_RESULT.md}"
UTC_NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Refuse elevated execution
if [[ "$(id -u)" -eq 0 ]]; then
  echo "ERROR: refuse to run as root" >&2
  exit 2
fi

os_name="$(uname -s 2>/dev/null || echo unknown)"
os_ver="$(uname -r 2>/dev/null || echo unknown)"
host_name="$(hostname 2>/dev/null || echo unknown)"
user_name="$(id -un 2>/dev/null || echo unknown)"
home_dir="${HOME:-unknown}"
shell_name="${SHELL:-unknown}"
powershell_version="not_applicable"

python_command="missing"
python_version="missing"
for cand in python3 python; do
  if command -v "${cand}" >/dev/null 2>&1; then
    python_command="${cand}"
    python_version="$("${cand}" --version 2>&1 | head -1 | tr -d '\r')"
    break
  fi
done

git_version="missing"
if command -v git >/dev/null 2>&1; then
  git_version="$(git --version 2>&1 | head -1)"
fi

cpu="$(uname -m 2>/dev/null || echo unknown)"
if [[ -r /proc/cpuinfo ]]; then
  model="$(awk -F: '/model name/ {gsub(/^ /,"",$2); print $2; exit}' /proc/cpuinfo || true)"
  [[ -n "${model}" ]] && cpu="${model}"
fi

memory_total="unknown"
if [[ -r /proc/meminfo ]]; then
  memory_total="$(awk '/MemTotal/ {printf "%.0fMB", $2/1024; exit}' /proc/meminfo || echo unknown)"
fi

disk_total="unknown"
disk_available="unknown"
filesystem_type="unknown"
if command -v df >/dev/null 2>&1; then
  # Portable parse of df -k for home filesystem
  line="$(df -kP "${home_dir}" 2>/dev/null | awk 'NR==2 {print}')"
  if [[ -n "${line}" ]]; then
    # total/avail in 1K blocks
    tot_k="$(echo "${line}" | awk '{print $2}')"
    avail_k="$(echo "${line}" | awk '{print $4}')"
    filesystem_type="$(echo "${line}" | awk '{print $1}')"
    if [[ "${tot_k}" =~ ^[0-9]+$ ]]; then
      disk_total="$(awk -v k="${tot_k}" 'BEGIN{printf "%.1fGB", k/1024/1024}')"
    fi
    if [[ "${avail_k}" =~ ^[0-9]+$ ]]; then
      disk_available="$(awk -v k="${avail_k}" 'BEGIN{printf "%.1fGB", k/1024/1024}')"
    fi
  fi
  if command -v findmnt >/dev/null 2>&1; then
    filesystem_type="$(findmnt -no FSTYPE -T "${home_dir}" 2>/dev/null || echo "${filesystem_type}")"
  fi
fi

timezone="$(date +%Z 2>/dev/null || echo unknown)"

network_available="false"
outbound_https_available="false"
if command -v curl >/dev/null 2>&1; then
  if curl -sI --max-time 5 https://example.com >/dev/null 2>&1; then
    network_available="true"
    outbound_https_available="true"
  fi
elif command -v getent >/dev/null 2>&1; then
  if getent hosts example.com >/dev/null 2>&1; then
    network_available="true"
    outbound_https_available="unknown"
  fi
fi

systemd_available="false"
cron_available="false"
task_scheduler_available="false"
scheduler_mechanism="MANUAL_ONLY"
if command -v systemctl >/dev/null 2>&1; then
  # user-level availability check without changing state
  if systemctl --user status >/dev/null 2>&1 || systemctl --version >/dev/null 2>&1; then
    systemd_available="true"
    scheduler_mechanism="SYSTEMD"
  fi
fi
if command -v crontab >/dev/null 2>&1; then
  cron_available="true"
  if [[ "${scheduler_mechanism}" == "MANUAL_ONLY" ]]; then
    scheduler_mechanism="CRON"
  fi
fi

local_root_candidate="${home_dir}/wick-r3e"
local_root_exists="false"
local_root_writable="false"
if [[ -d "${local_root_candidate}" ]]; then
  local_root_exists="true"
fi
# writable check without creating permanent dirs: test parent home writability for candidate path
if [[ -w "${home_dir}" ]]; then
  local_root_writable="true"
fi

repo_path="$(pwd)"
repo_path_exists="false"
if [[ -d "${repo_path}/.git" ]] || [[ -f "${repo_path}/pyproject.toml" ]]; then
  repo_path_exists="true"
fi
# Prefer detecting wick repo root from script location
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "${script_dir}/../pyproject.toml" ]]; then
  repo_path="$(cd "${script_dir}/.." && pwd)"
  repo_path_exists="true"
fi

config_path_candidate="${local_root_candidate}/config/r3e-collector.env"
backup_path_candidate="${local_root_candidate}/backups"

blockers=()
warnings=()
host_discovery_status="READY_FOR_REVIEW"

case "${filesystem_type}" in
  overlay|tmpfs)
    blockers+=("filesystem_ephemeral_or_overlay:${filesystem_type}")
    host_discovery_status="BLOCKED"
    ;;
esac
case "${local_root_candidate}" in
  /tmp/*|/var/tmp/*|/workspace|/workspace/*)
    blockers+=("local_root_candidate_ephemeral")
    host_discovery_status="BLOCKED"
    ;;
esac
if [[ "${python_command}" == "missing" ]]; then
  blockers+=("python_missing")
  host_discovery_status="BLOCKED"
fi
if [[ "${git_version}" == "missing" ]]; then
  warnings+=("git_missing")
  [[ "${host_discovery_status}" == "READY_FOR_REVIEW" ]] && host_discovery_status="DEGRADED"
fi
if [[ "${outbound_https_available}" != "true" ]]; then
  warnings+=("outbound_https_unconfirmed")
  [[ "${host_discovery_status}" == "READY_FOR_REVIEW" ]] && host_discovery_status="DEGRADED"
fi
if [[ "${local_root_exists}" != "true" ]]; then
  warnings+=("local_root_not_created_yet")
fi

recommended_local_root="${local_root_candidate}"
recommended_scheduler_mechanism="${scheduler_mechanism}"

blocker_str="none"
warning_str="none"
if ((${#blockers[@]} > 0)); then
  _ifs="$IFS"
  IFS=','
  blocker_str="${blockers[*]}"
  IFS="$_ifs"
fi
if ((${#warnings[@]} > 0)); then
  _ifs="$IFS"
  IFS=','
  warning_str="${warnings[*]}"
  IFS="$_ifs"
fi

# Write markdown result only (no secret values)
cat > "${OUT}" <<EOF
# R3E Local Host Discovery Result

\`\`\`text
DISCOVERY_EXECUTED_AT_UTC = ${UTC_NOW}
OPERATING_SYSTEM = ${os_name}
OPERATING_SYSTEM_VERSION = ${os_ver}
HOSTNAME = ${host_name}
CURRENT_USERNAME = ${user_name}
HOME_DIRECTORY = ${home_dir}
SHELL = ${shell_name}
POWERSHELL_VERSION = ${powershell_version}
PYTHON_COMMAND = ${python_command}
PYTHON_VERSION = ${python_version}
GIT_VERSION = ${git_version}
CPU = ${cpu}
MEMORY_TOTAL = ${memory_total}
DISK_TOTAL = ${disk_total}
DISK_AVAILABLE = ${disk_available}
FILESYSTEM_TYPE = ${filesystem_type}
TIMEZONE = ${timezone}
NETWORK_AVAILABLE = ${network_available}
OUTBOUND_HTTPS_AVAILABLE = ${outbound_https_available}
SCHEDULER_MECHANISM = ${scheduler_mechanism}
TASK_SCHEDULER_AVAILABLE = ${task_scheduler_available}
SYSTEMD_AVAILABLE = ${systemd_available}
CRON_AVAILABLE = ${cron_available}
LOCAL_ROOT_CANDIDATE = ${local_root_candidate}
LOCAL_ROOT_EXISTS = ${local_root_exists}
LOCAL_ROOT_WRITABLE = ${local_root_writable}
REPOSITORY_PATH = ${repo_path}
REPOSITORY_PATH_EXISTS = ${repo_path_exists}
CONFIG_PATH_CANDIDATE = ${config_path_candidate}
BACKUP_PATH_CANDIDATE = ${backup_path_candidate}
HOST_DISCOVERY_STATUS = ${host_discovery_status}
RECOMMENDED_LOCAL_ROOT = ${recommended_local_root}
RECOMMENDED_SCHEDULER_MECHANISM = ${recommended_scheduler_mechanism}
BLOCKERS = ${blocker_str}
WARNINGS = ${warning_str}
NEXT_ACTION = submit this file for readiness review
\`\`\`

Notes:

- read-only discovery
- Cursor agent environments with overlay FS are not operational hosts
- no secrets, public IP, tokens, or env contents collected
EOF

echo "WROTE ${OUT}"
echo "HOST_DISCOVERY_STATUS=${host_discovery_status}"
exit 0
