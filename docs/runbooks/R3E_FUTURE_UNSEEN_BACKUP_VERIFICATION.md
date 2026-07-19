# R3E Future-Unseen Backup Verification Runbook

```text
RELEASE = R3E
BACKLOG_ITEM = B5
SUBTASK = B5-P1
TASK_ID = PARALLEL-OPERATIONAL-HARDENING-001
DOCUMENT = BACKUP_VERIFICATION_RUNBOOK
PHASE = PREPARATION_ONLY
RESTORE_EXECUTION = false
VALIDATE_AUTHORIZED = false
```

## Purpose

Verify an existing backup archive **without creating a new backup** and **without restoring**.

## Command

```bash
WICK_ROOT="${WICK_ROOT:-.}" \
  bash scripts/r3e_future_unseen_backup_verify.sh [path/to/fu_backup_YYYYMMDDThhmmssZ.tar.gz]
```

If no path is given, the newest `fu_backup_*.tar.gz` under `${WICK_ROOT}/backups` is selected.

## Required checks

| Check | Pass condition |
|---|---|
| `archive_exists` | File exists and is a regular file |
| `archive_nonempty` | Size > 0 |
| `manifest_exists` | Sidecar checksum/manifest present, or archive contains expected manifest paths |
| `checksum_valid` | SHA-256 matches sidecar when present; otherwise recorded as `CHECKSUM_SIDECAR_ABSENT` with archive hash computed for evidence |
| `expected_directories_present` | Archive lists `data/future_unseen/` and `reports/r3e_future_unseen/` |
| `secret_files_absent` | No `*.env`, `*secret*`, or obvious credential filenames in archive listing |
| `restore_target_not_overwritten` | Verification uses a temp listing/extract probe only; production paths untouched |

## Pass / fail

```text
BACKUP_VERIFICATION = PASS | FAIL
```

Any failed required check => `FAIL`.
`FAIL` blocks scheduler activation checklist item `BACKUP_VERIFICATION_PASS`.

## Explicitly out of scope

- Creating backups (use `scripts/r3e_future_unseen_backup.sh`)
- Restoring backups onto production paths
- Running `validate`
- Host-specific path invention

## Evidence to preserve

- Script stdout/stderr
- Computed checksum
- Archive path and size
- Timestamp UTC
