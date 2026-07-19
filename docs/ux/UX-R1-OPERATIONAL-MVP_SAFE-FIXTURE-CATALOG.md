# UX-R1 — Operational MVP Safe Fixture Catalog

```text
DOCUMENT = UX-R1-OPERATIONAL-MVP_SAFE-FIXTURE-CATALOG
VERSION = 1.0.0
RELEASE = UX-R1
BACKLOG_ITEM = UX-B3
TASK_ID = OPERATIONAL-MVP-SCREEN-CONTRACTS-001
UI_IMPLEMENTATION_AUTHORIZED = false
EXECUTABLE_FIXTURES_IN_THIS_TASK = false
EFFECTIVE_AT = 2026-07-19T13:45:00Z
```

## Policy

Every fixture must include:

```text
fixture_id
fixture_label = DADOS_DEMONSTRATIVOS
scenario
source = SYNTHETIC
scientific_interpretation_allowed = false
economic_interpretation_allowed = false
```

UI must show visible badge: `DADOS_DEMONSTRATIVOS` / `DEMONSTRATION DATA`.

### Prohibited in all fixtures

- fake profit / return / expectancy
- accuracy or hit-rate presented as model quality
- risk-adjusted return ratios
- fabricated validation success (`validate` executed)
- `ECONOMIC_INTERPRETATION_ALLOWED=true`
- `SCHEDULER_ACTIVATED=true` presented as live truth without demo labeling (required scenarios keep inactive)
- invented execution IDs claimed as repository evidence

### Allowed

- synthetic operational metadata shaped like real artifacts
- `readiness_status=READY` **with** `VALIDATE_AUTHORIZED=false` and scientific gate pending
- warnings and failures for UX of ERROR/ATTENTION
- deferred host and blocked scheduler

No executable fixture files are created in this task — catalog only.

---

## Scenario catalog

### 1. healthy_collection_not_ready

```text
fixture_id = fx_overview_healthy_not_ready_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = healthy_collection_not_ready
source = SYNTHETIC
scientific_interpretation_allowed = false
economic_interpretation_allowed = false
```

| Field | Value |
|-------|-------|
| collection_status | IN_PROGRESS |
| last_run_status | COMPLETE |
| readiness_status | NOT_READY |
| readiness_reason | WINDOW_DAYS_INSUFFICIENT |
| window_days | 12.5 |
| required_window_days | 90 |
| n_observations_total | 1200 |
| HOST_DISCOVERY | DEFERRED |
| SCHEDULER_ACTIVATION | BLOCKED |
| VALIDATE_AUTHORIZED | false |
| R3E_GATE | PENDING_FUTURE_UNSEEN_DATA |

Screens exercised: Visão Geral, Readiness, Execuções (one success), Host (deferred).

---

### 2. collection_warning

```text
fixture_id = fx_runs_collection_warning_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = collection_warning
source = SYNTHETIC
scientific_interpretation_allowed = false
economic_interpretation_allowed = false
```

| Field | Value |
|-------|-------|
| last_run_status | PARTIAL |
| provider_failures | one soft provider timeout |
| observations_accepted | 40 |
| observations_rejected | 3 |
| readiness_status | NOT_READY |
| visual | ATTENTION (not ERROR) |

Screens: Visão Geral, Execuções detail warnings.

---

### 3. collection_failure

```text
fixture_id = fx_runs_collection_failure_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = collection_failure
source = SYNTHETIC
scientific_interpretation_allowed = false
economic_interpretation_allowed = false
```

| Field | Value |
|-------|-------|
| last_run_status | FAILED |
| hard_error | present (synthetic) |
| failure_category | PROVIDER or STORAGE (taxonomy) |
| readiness_status | NOT_READY |
| open incident block | EMPTY or synthetic label only as demo |

Screens: Visão Geral ERROR banner, Execuções failure detail. Must not imply scientific invalidation beyond ops failure.

---

### 4. host_discovery_deferred

```text
fixture_id = fx_host_discovery_deferred_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = host_discovery_deferred
source = SYNTHETIC
scientific_interpretation_allowed = false
economic_interpretation_allowed = false
```

| Field | Value |
|-------|-------|
| HOST_DISCOVERY | DEFERRED |
| host_identity | UNKNOWN |
| durable_store_path_state | UNAVAILABLE |
| OPERATIONAL_DEBT | OPEN |
| SCHEDULER_ACTIVATION | BLOCKED |
| next_safe_action | Executar discovery no host persistente |

Screens: Host primary; Visão Geral host pill.

---

### 5. scheduler_not_activated

```text
fixture_id = fx_host_scheduler_not_activated_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = scheduler_not_activated
source = SYNTHETIC
scientific_interpretation_allowed = false
economic_interpretation_allowed = false
```

| Field | Value |
|-------|-------|
| scheduler_registered | false |
| scheduler_enabled | false |
| scheduler_last_trigger | null |
| scheduler_next_trigger | null |
| activation_authorization_state | NOT_AUTHORIZED |
| systemd_templates_prepared | true |
| SCHEDULER_ACTIVATION | BLOCKED |

Screens: Host stepper all gates unchecked. Must not show timer as active.

---

### 6. readiness_ready_but_validation_not_authorized

```text
fixture_id = fx_readiness_ready_no_validate_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = readiness_ready_but_validation_not_authorized
source = SYNTHETIC
scientific_interpretation_allowed = false
economic_interpretation_allowed = false
```

| Field | Value |
|-------|-------|
| readiness_status | READY |
| window_days | 90 |
| required_window_days | 90 |
| series_complete count | 16 |
| VALIDATE_AUTHORIZED | false |
| HUMAN_AUTHORIZATION_REQUIRED | true |
| validation_command_executed | false |
| R3E_GATE | PENDING_FUTURE_UNSEEN_DATA |
| ECONOMIC_INTERPRETATION_ALLOWED | false |
| R4_STATUS | BLOCKED |

Mandatory copy: “READY não autoriza validate.” Screens: Readiness, Visão Geral.

---

### 7. no_execution_history

```text
fixture_id = fx_runs_empty_history_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = no_execution_history
source = SYNTHETIC
scientific_interpretation_allowed = false
economic_interpretation_allowed = false
```

| Field | Value |
|-------|-------|
| executions | [] |
| last_completed_execution_id | null |
| last_failed_execution_id | null |
| automation_state | missing or empty synthetic |
| list state | EMPTY |

Screens: Execuções EMPTY; Visão Geral without timeline items.

---

### 8. partial_metadata

```text
fixture_id = fx_overview_partial_metadata_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = partial_metadata
source = SYNTHETIC
scientific_interpretation_allowed = false
economic_interpretation_allowed = false
```

| Field | Value |
|-------|-------|
| readiness_report | present |
| automation_state | missing |
| host discovery | missing |
| lock | ABSENT |
| backups | UNAVAILABLE |
| raw/validated | UNAVAILABLE |
| overview state | PARTIAL |

Screens: all four show PARTIAL/UNAVAILABLE explicitly; no fabricated fills.

---

## Cross-fixture constants

```text
fixture_label = DADOS_DEMONSTRATIVOS
source = SYNTHETIC
scientific_interpretation_allowed = false
economic_interpretation_allowed = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
SCHEDULER_ACTIVATION = BLOCKED
OPERATIONAL_DEBT = OPEN
```

## Future implementation note

When UI work is authorized, materialize these as JSON under a demo fixtures directory (path decided then). This task ships **catalog only**.
