#!/usr/bin/env bash
# Dry-run retention planner for future-unseen ops artifacts.
# Never deletes. Never touches store observations. Never runs validate.
set -euo pipefail

WICK_ROOT="${WICK_ROOT:-.}"
export WICK_ROOT

python - <<'PY'
from pathlib import Path
import json
import os

from wick.r3e.future_unseen.ops_hardening import retention_plan

root = Path(os.environ.get("WICK_ROOT", ".")).resolve()
plan = retention_plan(wick_root=root, dry_run=True)
print(json.dumps(plan, indent=2))
if plan.get("deletions_performed", 0) != 0:
    raise SystemExit("dry-run unexpectedly performed deletions")
PY
