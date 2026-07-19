#!/usr/bin/env bash
# Verify an existing future-unseen backup archive.
# Does NOT create backups. Does NOT restore onto production paths. Does NOT validate.
set -euo pipefail

WICK_ROOT="${WICK_ROOT:-.}"
BACKUP_ROOT="${WICK_ROOT}/backups"
ARCHIVE="${1:-}"

if [[ -z "${ARCHIVE}" ]]; then
  ARCHIVE="$(ls -1t "${BACKUP_ROOT}"/fu_backup_*.tar.gz 2>/dev/null | head -n1 || true)"
fi

if [[ -z "${ARCHIVE}" ]]; then
  echo "ERROR: no backup archive found under ${BACKUP_ROOT}" >&2
  exit 1
fi

python - "$ARCHIVE" <<'PY'
import json
import sys
from pathlib import Path

from wick.r3e.future_unseen.ops_hardening import verify_backup_archive

archive = Path(sys.argv[1])
result = verify_backup_archive(archive)
print(json.dumps(result, indent=2))
raise SystemExit(0 if result.get("BACKUP_VERIFICATION") == "PASS" else 1)
PY
