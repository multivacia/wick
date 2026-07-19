# R3E Future-Unseen Operational Failure Taxonomy

```text
RELEASE = R3E
BACKLOG_ITEM = B5
SUBTASK = B5-P1
TASK_ID = PARALLEL-OPERATIONAL-HARDENING-001
DOCUMENT = FAILURE_TAXONOMY
PHASE = PREPARATION_ONLY
HOST_BINDING = NONE
VALIDATE_AUTHORIZED = false
SCHEDULER_ACTIVATION_AUTHORIZED = false
```

Host-independent failure categories for collection automation and local operations.
No category authorizes `validate`, effect peeking, economic interpretation, R4, or R5.

## Exit-code families

| Family | Codes | Meaning |
|---|---|---|
| OK | 0 | Cycle completed without hard failure (`COMPLETE`, `PARTIAL`, `NO_NEW_DATA`) |
| FAILED | 1 | Retryable or non-retryable operational failure |
| READINESS_BLOCKED | 3 | Preflight/readiness blocked; do not treat as success |
| SKIPPED_LOCKED | 4 | Another cycle holds an active lock |
| CONFIG | 10–19 | Configuration missing/invalid |
| STORAGE | 20–29 | Store/disk/backup problems |
| PROVIDER | 30–39 | External data provider problems |
| LOCK | 40–49 | Lock diagnostic / stale-lock human follow-up |
| UNEXPECTED | 90–99 | Unexpected exception / unknown |

## Categories

### CONFIGURATION_MISSING

| Field | Value |
|---|---|
| Severity | HIGH |
| Retryable | no (until operator supplies config) |
| Exit-code family | CONFIG (10) |
| Operator action | Create required env/config from examples; do not invent host values |
| Scheduler next cycle | continue only after config present; otherwise skip/fail-closed |
| Human alert | required |
| Scientific state changes | no |
| Validate authorized | false |

### CONFIGURATION_INVALID

| Field | Value |
|---|---|
| Severity | HIGH |
| Retryable | no (until corrected) |
| Exit-code family | CONFIG (11) |
| Operator action | Fix invalid keys/paths/types; re-run preflight |
| Scheduler next cycle | fail-closed until fixed |
| Human alert | required |
| Scientific state changes | no |
| Validate authorized | false |

### NETWORK_UNAVAILABLE

| Field | Value |
|---|---|
| Severity | MEDIUM |
| Retryable | yes |
| Exit-code family | PROVIDER (30) |
| Operator action | Check connectivity; allow next cycle retry |
| Scheduler next cycle | continue |
| Human alert | required after repeated cycles |
| Scientific state changes | no |
| Validate authorized | false |

### PROVIDER_AUTHENTICATION_FAILED

| Field | Value |
|---|---|
| Severity | HIGH |
| Retryable | no (until credentials fixed) |
| Exit-code family | PROVIDER (31) |
| Operator action | Rotate/repair provider credentials outside git; never commit secrets |
| Scheduler next cycle | fail-closed until fixed |
| Human alert | required |
| Scientific state changes | no |
| Validate authorized | false |

### PROVIDER_RATE_LIMITED

| Field | Value |
|---|---|
| Severity | MEDIUM |
| Retryable | yes (backoff) |
| Exit-code family | PROVIDER (32) |
| Operator action | Reduce cadence or wait; inspect provider limits |
| Scheduler next cycle | continue with backoff |
| Human alert | optional unless persistent |
| Scientific state changes | no |
| Validate authorized | false |

### PROVIDER_DATA_UNAVAILABLE

| Field | Value |
|---|---|
| Severity | MEDIUM |
| Retryable | yes |
| Exit-code family | PROVIDER (33) |
| Operator action | Confirm market holiday/outage; keep collecting |
| Scheduler next cycle | continue |
| Human alert | required after repeated cycles |
| Scientific state changes | no |
| Validate authorized | false |

### STORE_NOT_WRITABLE

| Field | Value |
|---|---|
| Severity | CRITICAL |
| Retryable | no (until permissions/path fixed) |
| Exit-code family | STORAGE (20) |
| Operator action | Fix ownership/permissions/mount; preserve existing store |
| Scheduler next cycle | fail-closed |
| Human alert | required |
| Scientific state changes | no |
| Validate authorized | false |

### STORE_CORRUPTION_SUSPECTED

| Field | Value |
|---|---|
| Severity | CRITICAL |
| Retryable | no |
| Exit-code family | STORAGE (21) |
| Operator action | Freeze writes; preserve evidence; run hash/manifest checks; restore only with human auth |
| Scheduler next cycle | stop |
| Human alert | required immediate |
| Scientific state changes | no (do not run validate) |
| Validate authorized | false |

### DISK_SPACE_LOW

| Field | Value |
|---|---|
| Severity | HIGH |
| Retryable | no (until space freed per retention policy) |
| Exit-code family | STORAGE (22) |
| Operator action | Free space using retention dry-run first; never delete last valid backup or store observations |
| Scheduler next cycle | fail-closed until space recovered |
| Human alert | required |
| Scientific state changes | no |
| Validate authorized | false |

### LOCK_ACTIVE

| Field | Value |
|---|---|
| Severity | LOW |
| Retryable | yes (next cycle) |
| Exit-code family | SKIPPED_LOCKED (4) / LOCK (40) |
| Operator action | Confirm overlapping run is expected; do not force-unlock |
| Scheduler next cycle | continue (skip this cycle) |
| Human alert | optional unless prolonged |
| Scientific state changes | no |
| Validate authorized | false |

### LOCK_STALE

| Field | Value |
|---|---|
| Severity | MEDIUM |
| Retryable | conditional (automation may recover on acquire; diagnostic never deletes) |
| Exit-code family | LOCK (41) |
| Operator action | Run `lock-status`; if stale and owner dead, human-authorized removal only |
| Scheduler next cycle | continue after safe recovery |
| Human alert | required if repeated |
| Scientific state changes | no |
| Validate authorized | false |

### BACKUP_FAILED

| Field | Value |
|---|---|
| Severity | HIGH |
| Retryable | yes after root cause fixed |
| Exit-code family | STORAGE (23) |
| Operator action | Inspect backup logs; verify disk; do not activate scheduler |
| Scheduler next cycle | fail-closed for activation gates; collection may continue only if store healthy |
| Human alert | required |
| Scientific state changes | no |
| Validate authorized | false |

### READINESS_NOT_READY

| Field | Value |
|---|---|
| Severity | INFO |
| Retryable | n/a (expected during collection) |
| Exit-code family | OK (0) when cycle otherwise healthy |
| Operator action | Continue collection; do not interpret as validation readiness for science |
| Scheduler next cycle | continue |
| Human alert | no |
| Scientific state changes | no |
| Validate authorized | false |

### READINESS_TRANSITION_READY

| Field | Value |
|---|---|
| Severity | HIGH (operational milestone) |
| Retryable | n/a |
| Exit-code family | OK (0) |
| Operator action | Emit READY notification contract only; require human review; do not run validate |
| Scheduler next cycle | continue collection only if still authorized; never auto-validate |
| Human alert | required |
| Scientific state changes | no (`VALIDATE_AUTHORIZED` remains false) |
| Validate authorized | false |

### UNEXPECTED_EXCEPTION

| Field | Value |
|---|---|
| Severity | HIGH |
| Retryable | conditional |
| Exit-code family | UNEXPECTED (90) / FAILED (1) |
| Operator action | Preserve logs/run dir; classify; escalate if unknown |
| Scheduler next cycle | continue with caution; stop if store risk |
| Human alert | required |
| Scientific state changes | no |
| Validate authorized | false |

## Global invariants

```text
NO_CATEGORY_AUTHORIZES_VALIDATE = true
NO_CATEGORY_AUTHORIZES_EFFECT_PEEKING = true
NO_CATEGORY_AUTHORIZES_ECONOMIC_INTERPRETATION = true
NO_CATEGORY_UNBLOCKS_R4_OR_R5 = true
SCHEDULER_ACTIVATION_AUTHORIZED = false
```
