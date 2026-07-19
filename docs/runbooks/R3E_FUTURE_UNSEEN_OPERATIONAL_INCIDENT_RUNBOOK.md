# R3E Future-Unseen Operational Incident Runbook

```text
RELEASE = R3E
BACKLOG_ITEM = B5
SUBTASK = B5-P1
TASK_ID = PARALLEL-OPERATIONAL-HARDENING-001
DOCUMENT = OPERATIONAL_INCIDENT_RUNBOOK
PHASE = PREPARATION_ONLY
VALIDATE_AUTHORIZED = false
SCHEDULER_ACTIVATION_AUTHORIZED = false
```

Do not include secret values in tickets, chat, or git.

## Common first actions

1. Stop further destructive actions.
2. Preserve evidence: run dirs, `automation_state.json`, lock file copy, health/backup logs.
3. Classify with `docs/operations/R3E_FUTURE_UNSEEN_FAILURE_TAXONOMY.md`.
4. Do **not** run `validate`.
5. Do **not** enable/activate scheduler without separate human authorization.

## Scenarios

### Repeated failures

- Pull last N statuses via `python -m wick.r3e.future_unseen history`.
- Identify dominant `failure_category`.
- If provider/network: allow retries; alert if persistent.
- If store/config: fail-closed; escalate.

### Stale lock

- Run `python -m wick.r3e.future_unseen lock-status` (read-only).
- If `STALE` and owner pid dead: human-authorized lock removal only.
- Never auto-delete from diagnostic tooling.

### Disk full / disk space low

- Fail-closed collection writes if store at risk.
- Run retention **dry-run** first.
- Never delete latest valid backup or store observations.
- Free space, then re-run healthcheck.

### Provider outage

- Category: `NETWORK_UNAVAILABLE` / `PROVIDER_DATA_UNAVAILABLE` / rate-limit/auth as applicable.
- Keep scheduler inactive if not already authorized.
- Resume collection cycles when provider recovers.

### Suspected store corruption

- Category: `STORE_CORRUPTION_SUSPECTED`.
- Freeze writers.
- Preserve hashes/manifests/backups.
- Restore only with human authorization; no validate.

### Backup failure

- Category: `BACKUP_FAILED`.
- Block activation checklist `BACKUP_PASS`.
- Fix root cause; recreate backup; run verification script.

### Accidental scheduler overlap

- Expect `LOCK_ACTIVE` / `SKIPPED_LOCKED`.
- Confirm only one owner path is enabled.
- Disable any accidental second schedule immediately.

### Accidental secret exposure

- Rotate exposed credentials immediately outside git.
- Remove secrets from logs/tickets if possible.
- Do not commit remediation secrets.
- Record incident without pasting secret material.

### Unexpected READY transition

- Emit READY notification per contract only.
- Set human review required.
- Do **not** run validate.
- Do **not** treat READY as scheduler authorization.

### Machine shutdown or sleep

- Next cycle should recover or report lock/stale state.
- Confirm persistent root survived reboot.
- Re-run healthcheck before any activation discussion.

### Local-host loss before HostGator migration

- Treat as potential evidence loss.
- Locate latest verified backup.
- Do not invent replacement host values.
- Follow migration verification checklist; dual ownership forbidden.

## Escalation

| Level | When | Action |
|---|---|---|
| L1 Operator | Single retryable failure | Observe next cycle |
| L2 Owner | Repeated failures, stale lock, backup fail, READY transition | Human decision + evidence pack |
| L3 Freeze | Corruption suspected, secret exposure, dual schedule | Stop writers/schedulers; preserve evidence |

## Evidence pack (minimum)

```text
history summary JSON
lock-status JSON
latest cycle_report.json path
automation_state.json
backup verification output (if relevant)
failure_category
timestamps UTC
```

No secrets in the pack.
