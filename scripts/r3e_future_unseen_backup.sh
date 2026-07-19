#!/usr/bin/env bash
# Backup durable future-unseen store + automation reports.
# Does NOT include /etc/wick secrets. Does NOT run validate.
# Fail-closed. Never deletes the last valid backup.
set -euo pipefail

WICK_ROOT="${WICK_ROOT:-/srv/wick}"
DATA_DIR="${WICK_ROOT}/data/future_unseen"
REPORTS_DIR="${WICK_ROOT}/reports/r3e_future_unseen"
BACKUP_ROOT="${WICK_ROOT}/backups"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-14}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
TMP_ARCHIVE="${BACKUP_ROOT}/.tmp_fu_backup_${STAMP}.tar.gz"
FINAL_ARCHIVE="${BACKUP_ROOT}/fu_backup_${STAMP}.tar.gz"

log() { printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" >&2; }

die() {
  log "ERROR: $*"
  exit 1
}

[[ -d "${DATA_DIR}" ]] || die "missing data dir: ${DATA_DIR}"
[[ -d "${REPORTS_DIR}" ]] || die "missing reports dir: ${REPORTS_DIR}"
mkdir -p "${BACKUP_ROOT}"

# Create archive to temp path then atomic rename.
# Exclude lock files and any accidental env copies under reports.
if ! tar -czf "${TMP_ARCHIVE}" \
  -C "${WICK_ROOT}" \
  --exclude='reports/r3e_future_unseen/automation.lock' \
  --exclude='*.env' \
  --exclude='*secret*' \
  "data/future_unseen" \
  "reports/r3e_future_unseen"
then
  rm -f "${TMP_ARCHIVE}" || true
  die "tar failed"
fi

mv -f "${TMP_ARCHIVE}" "${FINAL_ARCHIVE}"
log "CREATED ${FINAL_ARCHIVE}"

# Retention: delete only archives older than RETENTION_DAYS, but keep at least one.
mapfile -t ARCHIVES < <(ls -1t "${BACKUP_ROOT}"/fu_backup_*.tar.gz 2>/dev/null || true)
if ((${#ARCHIVES[@]} == 0)); then
  die "no backup archive present after create"
fi

if [[ "${RETENTION_DAYS}" =~ ^[0-9]+$ ]] && ((RETENTION_DAYS > 0)); then
  # Find candidates older than retention; never remove the newest archive.
  NEWEST="${ARCHIVES[0]}"
  while IFS= read -r -d '' old; do
    [[ "${old}" == "${NEWEST}" ]] && continue
    rm -f -- "${old}"
    log "REMOVED_OLD ${old}"
  done < <(find "${BACKUP_ROOT}" -maxdepth 1 -type f -name 'fu_backup_*.tar.gz' -mtime "+${RETENTION_DAYS}" -print0 2>/dev/null || true)
fi

# Ensure at least one valid archive remains.
mapfile -t REMAINING < <(ls -1t "${BACKUP_ROOT}"/fu_backup_*.tar.gz 2>/dev/null || true)
((${#REMAINING[@]} >= 1)) || die "retention removed last valid backup"
log "OK newest=${REMAINING[0]} count=${#REMAINING[@]}"
exit 0
