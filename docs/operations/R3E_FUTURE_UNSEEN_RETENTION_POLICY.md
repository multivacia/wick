# R3E Future-Unseen Retention Policy

```text
RELEASE = R3E
BACKLOG_ITEM = B5
SUBTASK = B5-P1
TASK_ID = PARALLEL-OPERATIONAL-HARDENING-001
DOCUMENT = RETENTION_POLICY
PHASE = PREPARATION_ONLY
DESTRUCTIVE_DEFAULT = false
VALIDATE_AUTHORIZED = false
```

## Provisional defaults

```text
RUN_LOG_RETENTION_DAYS = 90
BACKUP_RETENTION_DAYS = 30
MINIMUM_VALID_BACKUPS = 3
FAILED_RUN_REPORT_RETENTION_DAYS = 180
```

These are host-independent policy defaults. Operators may tighten them but must not weaken the safety invariants below without human authorization.

## Scope

| Artifact class | Subject to retention | Notes |
|---|---|---|
| Automation run reports under `automation_runs/` | yes (logs/reports) | Prefer failed-run longer retention |
| Operational JSONL / events | yes | Keep enough for incident review |
| Backup archives `fu_backup_*.tar.gz` | yes | See backup rules |
| Store observations (`data/future_unseen/**`) | **no** | Not subject to log retention |
| Cutoff / freeze / collection_state manifests | **no** | Governance evidence |
| Scientific validation outputs | n/a | Validate not authorized in this phase |

## Safety invariants

1. Never delete the latest valid backup.
2. Never delete while a backup temp archive is being written (`.tmp_fu_backup_*`).
3. Dry-run retention command first (`scripts/r3e_future_unseen_retention_dry_run.sh` or Python dry-run helper).
4. Keep at least `MINIMUM_VALID_BACKUPS` valid backups when available.
5. Store observations are never candidates for log retention.
6. Scientific/governance evidence required by AI governance must be preserved.
7. Retention never authorizes `validate`.

## Dry-run command

```bash
# Host-independent defaults; override roots via env when on a real host.
WICK_ROOT="${WICK_ROOT:-.}" \
  bash scripts/r3e_future_unseen_retention_dry_run.sh
```

Or:

```bash
python -c "from wick.r3e.future_unseen.ops_hardening import retention_plan; print(retention_plan(dry_run=True))"
```

Dry-run must list candidates only and perform zero deletions.

## Apply mode

Apply/delete mode is **not authorized** by this preparation task.
Any future apply command requires separate human authorization and must re-check:

```text
latest_valid_backup_preserved
minimum_valid_backups_preserved
no_tmp_backup_in_progress
store_observations_untouched
```
