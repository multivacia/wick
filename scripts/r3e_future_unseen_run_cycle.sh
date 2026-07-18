#!/usr/bin/env bash
# Local/host runner for R3E future-unseen automation cycle (B4).
# Intended for cron/systemd on a durable host that owns the official store.
# Does NOT authorize or invoke scientific validate.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

AS_OF_ARG=()
if [[ -n "${FU_AS_OF:-}" ]]; then
  AS_OF_ARG=(--as-of "$FU_AS_OF")
fi

EXTRA=()
if [[ "${FU_DRY_RUN_ONLY:-0}" == "1" ]]; then
  EXTRA+=(--dry-run-only)
fi

exec python -m wick.r3e.future_unseen run-cycle --json "${AS_OF_ARG[@]}" "${EXTRA[@]}" "$@"
