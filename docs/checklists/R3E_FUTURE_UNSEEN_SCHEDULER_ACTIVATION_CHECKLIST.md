# R3E Future-Unseen Scheduler Activation Checklist

```text
RELEASE = R3E
BACKLOG_ITEM = B5
SUBTASK = B5-P1
TASK_ID = PARALLEL-OPERATIONAL-HARDENING-001
DOCUMENT = SCHEDULER_ACTIVATION_CHECKLIST
PHASE = PREPARATION_ONLY
THIS_DOCUMENT_GRANTS_AUTHORIZATION = false
```

Operator checklist only. Completing boxes in a working copy does **not** grant authorization.
The repository canonical value remains:

```text
SCHEDULER_ACTIVATION_AUTHORIZED = false
```

## Required gates

Mark each item only after evidence exists on the real operational host.

- [ ] `REAL_HOST_DISCOVERY_COMPLETE`
- [ ] `PERSISTENT_ROOT_CONFIRMED`
- [ ] `ENV_FILE_CONFIGURED`
- [ ] `SECRETS_NOT_IN_GIT`
- [ ] `MANUAL_PREFLIGHT_PASS`
- [ ] `MANUAL_DRY_RUN_PASS`
- [ ] `MANUAL_LIVE_RUN_PASS`
- [ ] `BACKUP_PASS`
- [ ] `BACKUP_VERIFICATION_PASS`
- [ ] `HEALTHCHECK_PASS`
- [ ] `LOCK_DIAGNOSTIC_PASS`
- [ ] `DISK_SPACE_PASS`
- [ ] `ALERT_CHANNEL_TEST_PASS_OR_EXPLICIT_WAIVER`
- [ ] `ROLLBACK_TESTED`
- [ ] `HUMAN_FINAL_AUTHORIZATION`

## Forbidden until separately authorized

```text
enable systemd timer/service
register Windows scheduled task for live cadence
run validate
economic interpretation
R4 / R5 work
```

## Notes

- Host values must come from real discovery, never invented.
- READY readiness transition does not authorize validate or scheduler enablement.
- This checklist ending unauthorized is intentional and required.

## Final authorization field (canonical)

```text
SCHEDULER_ACTIVATION_AUTHORIZED = false
```
