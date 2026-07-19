# UX-R1-I6A — Overview Fixture Scenarios

```text
DOCUMENT = UX-R1-I6A-OVERVIEW-FIXTURE-SCENARIOS
VERSION = 1.0.0
RELEASE = UX-R1
WORKSTREAM = I6A
TASK_ID = OVERVIEW-SCREEN-DATA-AND-FIXTURE-PREPARATION-001
PHASE = DATA_CONTRACT_AND_FIXTURE_PREPARATION
EXECUTABLE_FIXTURES_IN_THIS_TASK = false
NO_TYPESCRIPT_FIXTURE_FILES = true
NO_REAL_DATA_INTEGRATION = true
UI_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
EFFECTIVE_AT = 2026-07-19T16:54:39Z
```

## Policy

These are **markdown specifications only**. Do not create `.ts`, `.tsx`, or JSON fixture code files in this task.

Every scenario MUST include:

```text
DADOS_DEMONSTRATIVOS
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

UI (when authorized later) must show badge: `DADOS_DEMONSTRATIVOS` / `DEMONSTRATION DATA`.

### Cross-scenario constants

```text
fixture_label = DADOS_DEMONSTRATIVOS
data_mode = DEMONSTRATION_FIXTURE
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
validate_authorized = false
scientific_gate_state = PENDING_FUTURE_UNSEEN_DATA
scheduler_state = BLOCKED
operational_debt_status = OPEN
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
open_incidents_count = UNAVAILABLE
```

Unless a scenario explicitly focuses host discovery deferred messaging, `host_state=DEFERRED` remains the default.

---

## 1. healthy_collection_not_ready

```text
fixture_id = fx_overview_healthy_not_ready_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = healthy_collection_not_ready
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

| Overview ViewModel field | Value |
|--------------------------|-------|
| overall_operational_state | HEALTHY_COLLECTION (with readiness NOT_READY shown separately) |
| overall_visual_semantic | SUCCESS_OPS + ATTENTION on readiness block |
| collection_status | IN_PROGRESS |
| last_completed_execution_id | synth-run-healthy-001 |
| last_completed_execution_status | COMPLETE |
| last_completed_execution_finished_at | 2026-07-18T12:00:00+00:00 |
| last_failed_execution_id | null |
| future_unseen_cutoff | 2026-07-18T01:30:00+00:00 |
| store_observation_count | 1200 |
| readiness_status_summary | NOT_READY |
| readiness_primary_reason | WINDOW_DAYS_INSUFFICIENT |
| window_days | 12.5 |
| required_window_days | 90 |
| window_progress | 12.5/90 |
| host_state | DEFERRED |
| scheduler_state | BLOCKED |
| open_incidents_count | UNAVAILABLE |
| operational_debt_status | OPEN |
| scientific_gate_state | PENDING_FUTURE_UNSEEN_DATA |
| validate_authorized | false |
| economic_interpretation_allowed | false |
| next_safe_action | Continuar coleta; aguardar critérios |
| next_safe_action_code | CONTINUE_COLLECTION |
| stale_flag | false |
| freshness_label | FRESH |
| evidence_links | synthetic readiness + automation_state + cycle_report (demo paths) |

Purpose: show healthy collection coexisting with NOT_READY without alarmism.

---

## 2. collection_warning

```text
fixture_id = fx_overview_collection_warning_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = collection_warning
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

| Overview ViewModel field | Value |
|--------------------------|-------|
| overall_operational_state | DEGRADED |
| overall_visual_semantic | ATTENTION |
| collection_status | IN_PROGRESS |
| last_completed_execution_id | synth-run-partial-001 |
| last_completed_execution_status | PARTIAL |
| last_failed_execution_id | null |
| store_observation_count | 1243 |
| readiness_status_summary | NOT_READY |
| readiness_primary_reason | WINDOW_DAYS_INSUFFICIENT |
| window_days | 13.0 |
| required_window_days | 90 |
| host_state | DEFERRED |
| scheduler_state | BLOCKED |
| operational_debt_status | OPEN |
| scientific_gate_state | PENDING_FUTURE_UNSEEN_DATA |
| validate_authorized | false |
| economic_interpretation_allowed | false |
| next_safe_action | Continuar coleta; revisar avisos na execução parcial |
| next_safe_action_code | CONTINUE_COLLECTION |
| warning_note | one soft provider timeout (synthetic); observations_accepted=40; rejected=3 |
| freshness_label | FRESH |

Purpose: ATTENTION for soft warnings — not ERROR.

---

## 3. collection_failure

```text
fixture_id = fx_overview_collection_failure_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = collection_failure
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

| Overview ViewModel field | Value |
|--------------------------|-------|
| overall_operational_state | ERROR |
| overall_visual_semantic | ERROR |
| collection_status | IN_PROGRESS |
| last_completed_execution_id | synth-run-ok-before-fail-001 |
| last_completed_execution_status | COMPLETE |
| last_failed_execution_id | synth-run-failed-001 |
| last_failed_execution_status | FAILED |
| last_failed_execution_finished_at | 2026-07-18T15:30:00+00:00 |
| failure_category | PROVIDER (synthetic taxonomy) |
| readiness_status_summary | NOT_READY |
| readiness_primary_reason | WINDOW_DAYS_INSUFFICIENT |
| host_state | DEFERRED |
| scheduler_state | BLOCKED |
| operational_debt_status | OPEN |
| scientific_gate_state | PENDING_FUTURE_UNSEEN_DATA |
| validate_authorized | false |
| economic_interpretation_allowed | false |
| next_safe_action | Investigar execução falha (abrir Execuções) |
| next_safe_action_code | INVESTIGATE_FAILED_EXECUTION |
| open_incidents_count | UNAVAILABLE |
| freshness_label | FRESH |

Purpose: ERROR banner for real ops failure. Must not imply scientific invalidation beyond operational failure.

---

## 4. host_discovery_deferred

```text
fixture_id = fx_overview_host_discovery_deferred_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = host_discovery_deferred
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

| Overview ViewModel field | Value |
|--------------------------|-------|
| overall_operational_state | NOT_READY |
| overall_visual_semantic | ATTENTION + DEFERRED |
| collection_status | IN_PROGRESS |
| last_completed_execution_id | synth-run-host-deferred-001 |
| last_completed_execution_status | COMPLETE |
| last_failed_execution_id | null |
| readiness_status_summary | NOT_READY |
| host_state | DEFERRED |
| scheduler_state | BLOCKED |
| operational_debt_status | OPEN |
| scientific_gate_state | PENDING_FUTURE_UNSEEN_DATA |
| validate_authorized | false |
| economic_interpretation_allowed | false |
| next_safe_action | Executar discovery no host persistente (runbook) |
| next_safe_action_code | RUN_HOST_DISCOVERY |
| store_observation_count | 800 |
| freshness_label | FRESH |

Purpose: host deferred is debt/attention, not host failure.

---

## 5. scheduler_not_activated

```text
fixture_id = fx_overview_scheduler_not_activated_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = scheduler_not_activated
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

| Overview ViewModel field | Value |
|--------------------------|-------|
| overall_operational_state | NOT_READY |
| overall_visual_semantic | BLOCKED on scheduler pill + ATTENTION readiness |
| collection_status | IN_PROGRESS |
| last_completed_execution_id | synth-run-sched-blocked-001 |
| last_completed_execution_status | COMPLETE |
| last_failed_execution_id | null |
| readiness_status_summary | NOT_READY |
| host_state | DEFERRED |
| scheduler_state | BLOCKED |
| scheduler_registered | false |
| scheduler_enabled | false |
| scheduler_last_trigger | null |
| scheduler_next_trigger | null |
| activation_authorization_state | NOT_AUTHORIZED |
| systemd_templates_prepared | true |
| operational_debt_status | OPEN |
| scientific_gate_state | PENDING_FUTURE_UNSEEN_DATA |
| validate_authorized | false |
| economic_interpretation_allowed | false |
| next_safe_action | Manter scheduler inativo; completar checklist |
| next_safe_action_code | KEEP_SCHEDULER_INACTIVE |
| freshness_label | FRESH |

Purpose: prepared templates ≠ activated. Never show timer as active.

---

## 6. readiness_ready_but_validation_not_authorized

```text
fixture_id = fx_overview_ready_no_validate_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = readiness_ready_but_validation_not_authorized
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

| Overview ViewModel field | Value |
|--------------------------|-------|
| overall_operational_state | BLOCKED (validate unauthorized) with readiness READY |
| overall_visual_semantic | SUCCESS_OPS on readiness + BLOCKED on validate/gate |
| collection_status | IN_PROGRESS |
| last_completed_execution_id | synth-run-ready-001 |
| last_completed_execution_status | COMPLETE |
| last_failed_execution_id | null |
| store_observation_count | 48000 |
| readiness_status_summary | READY |
| readiness_primary_reason | null (criteria met) |
| window_days | 90 |
| required_window_days | 90 |
| window_progress | 90/90 |
| series_complete_count | 16 |
| host_state | DEFERRED |
| scheduler_state | BLOCKED |
| operational_debt_status | OPEN |
| scientific_gate_state | PENDING_FUTURE_UNSEEN_DATA |
| validate_authorized | false |
| human_authorization_required | true |
| validation_command_executed | false |
| economic_interpretation_allowed | false |
| next_safe_action | Não executar validate; aguardar autorização humana |
| next_safe_action_code | DO_NOT_VALIDATE |
| mandatory_copy | READY não autoriza validate. |
| freshness_label | FRESH |

Purpose: READY ≠ validate. No economic/scientific success claim.

---

## 7. no_execution_history

```text
fixture_id = fx_overview_no_execution_history_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = no_execution_history
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

| Overview ViewModel field | Value |
|--------------------------|-------|
| overall_operational_state | EMPTY |
| overall_visual_semantic | INFO |
| collection_status | UNAVAILABLE or NOT_STARTED (synthetic) |
| last_completed_execution_id | null |
| last_completed_execution_status | null |
| last_failed_execution_id | null |
| store_observation_count | 0 or UNAVAILABLE |
| readiness_status_summary | UNAVAILABLE |
| host_state | DEFERRED |
| scheduler_state | BLOCKED |
| operational_debt_status | OPEN |
| scientific_gate_state | PENDING_FUTURE_UNSEEN_DATA |
| validate_authorized | false |
| economic_interpretation_allowed | false |
| next_safe_action | Continuar coleta; aguardar critérios |
| next_safe_action_code | CONTINUE_COLLECTION |
| evidence_links | empty or runbook-only |
| freshness_label | UNAVAILABLE |
| timeline_items | [] |

Purpose: EMPTY overview without fabricating history.

---

## 8. partial_metadata

```text
fixture_id = fx_overview_partial_metadata_001
fixture_label = DADOS_DEMONSTRATIVOS
scenario = partial_metadata
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

| Overview ViewModel field | Value |
|--------------------------|-------|
| overall_operational_state | PARTIAL |
| overall_visual_semantic | ATTENTION |
| collection_status | UNAVAILABLE |
| last_completed_execution_id | null (automation_state missing) |
| last_failed_execution_id | null |
| readiness_status_summary | NOT_READY (readiness_report present) |
| readiness_primary_reason | WINDOW_DAYS_INSUFFICIENT |
| window_days | 5.0 |
| required_window_days | 90 |
| store_observation_count | 200 |
| host_state | DEFERRED (discovery result missing) |
| scheduler_state | BLOCKED |
| operational_debt_status | OPEN |
| scientific_gate_state | PENDING_FUTURE_UNSEEN_DATA |
| validate_authorized | false |
| economic_interpretation_allowed | false |
| lock_state | ABSENT |
| backups | UNAVAILABLE |
| next_safe_action | Indisponível — dados parciais |
| next_safe_action_code | PARTIAL_DATA_UNAVAILABLE |
| data_mode | DEMONSTRATION_FIXTURE |
| freshness_label | PARTIAL |
| provenance_footer | readiness_report present; automation_state missing; host discovery missing |

Purpose: PARTIAL/UNAVAILABLE explicit; no fabricated fills.

---

## Scenario → matrix crosswalk

| Scenario | State matrix ID (approx) | Overview banner |
|----------|--------------------------|-----------------|
| healthy_collection_not_ready | C01 | ATTENTION readiness + healthy collection |
| collection_warning | C04 | ATTENTION warnings |
| collection_failure | C05 | ERROR |
| host_discovery_deferred | C01/C10 family | ATTENTION + DEFERRED debt |
| scheduler_not_activated | C01 + scheduler blocked | BLOCKED scheduler |
| readiness_ready_but_validation_not_authorized | C08 | SUCCESS_OPS + BLOCKED validate |
| no_execution_history | C13 | EMPTY |
| partial_metadata | C14 | PARTIAL |

## Materialization note

When UI work is authorized, materialize these as JSON under a demo fixtures directory (path decided then). This task ships **scenario specs only** — no executable fixture files.
