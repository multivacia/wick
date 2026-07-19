# R3E Local → HostGator Migration Verification Checklist

```text
RELEASE = R3E
BACKLOG_ITEM = B5
SUBTASK = B5-P1
TASK_ID = PARALLEL-OPERATIONAL-HARDENING-001
DOCUMENT = LOCAL_TO_HOSTGATOR_MIGRATION_VERIFICATION
PHASE = PREPARATION_ONLY
HOSTGATOR_STATUS = DEFERRED_FUTURE_MIGRATION
DUAL_OWNERSHIP_ALLOWED = false
SCHEDULER_ACTIVATION_AUTHORIZED = false
VALIDATE_AUTHORIZED = false
```

Use only when a future migration is human-authorized. This checklist does not authorize migration or activation.

## Verification gates

- [ ] `LOCAL_SCHEDULER_FROZEN` — local cadence disabled/stopped before cutover
- [ ] `LATEST_RUN_COMPLETED` — no in-flight cycle on source
- [ ] `BACKUP_CREATED` — durable backup produced on source
- [ ] `BACKUP_CHECKSUM_VERIFIED` — backup verification PASS
- [ ] `SOURCE_STORE_COUNT_RECORDED` — observation count captured before transfer
- [ ] `DESTINATION_RESTORE_VERIFIED` — restore verified on destination (separate auth)
- [ ] `DESTINATION_STORE_COUNT_MATCHED` — counts match source record
- [ ] `NO_SIMULTANEOUS_OWNERSHIP` — only one host owns live collection
- [ ] `DESTINATION_DRY_RUN_PASS` — destination dry-run collect/automation pass
- [ ] `ROLLBACK_PATH_RETAINED` — source backup + rollback plan retained
- [ ] `ACTIVATION_SEPARATELY_AUTHORIZED` — destination scheduler remains unauthorized until distinct human auth

## Final fields

```text
MIGRATION_AUTHORIZED = false
SCHEDULER_ACTIVATION_AUTHORIZED = false
VALIDATION_COMMAND_EXECUTED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
```

## Forbidden during verification

- Enabling schedulers on both hosts
- Inventing hostnames/paths/credentials
- Running `validate`
- Economic interpretation
