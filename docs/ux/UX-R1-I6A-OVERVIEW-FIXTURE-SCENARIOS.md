# UX-R1-I6A — Overview Fixture Scenarios

```text
DOCUMENT = UX-R1-I6A-OVERVIEW-FIXTURE-SCENARIOS
VERSION = 1.1.0
RELEASE = UX-R1
WORKSTREAM = I6A
TASK_ID = OVERVIEW-SCREEN-DATA-AND-FIXTURE-PREPARATION-001
PHASE = DATA_CONTRACT_AND_FIXTURE_PREPARATION
BASE_SHA = 6ff45b9bd50349cc12061346c24a86fec0cf7645
DATA_CONTRACT_DECISION = AUTHORIZED_WITH_CONDITIONS
I6A_DOCUMENTATION_MERGE_RECOMMENDED = true
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_SCOPE = DOCUMENTATION_AND_DATA_CONTRACT_ONLY
RUNTIME_IMPLEMENTATION_AUTHORIZED = false
EXECUTABLE_FIXTURES_IN_THIS_TASK = false
NO_TYPESCRIPT_FIXTURE_FILES = true
TYPESCRIPT_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
NO_REAL_DATA_INTEGRATION = true
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
ROUTER_INSTALLATION_AUTHORIZED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
SCIENTIFIC_INTERPRETATION_ALLOWED = false
WCAG = 2.2 AA
EFFECTIVE_AT = 2026-07-19T19:00:00Z
```

## Policy

These are **markdown specifications only**. Do not create `.ts`, `.tsx`, or JSON fixture code files in this task.

Do not add realistic-looking invented production timestamps for financial results, returns, or success rates. Synthetic demo timestamps below are labeled SYNTHETIC and carry `DADOS_DEMONSTRATIVOS`.

Every scenario MUST include:

```text
FIXTURE_ID =
DADOS_DEMONSTRATIVOS = true
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
PURPOSE =
EXPECTED_OPERATIONAL_STATE =
EXPECTED_PRIMARY_MESSAGE =
EXPECTED_TECHNICAL_DETAIL =
EXPECTED_NEXT_SAFE_ACTION =
EXPECTED_STATUS_SEMANTICS =
MISSING_FIELDS =
ACCESSIBILITY_EXPECTATIONS =
```

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
source_type = SYNTHETIC
```

Unless a scenario explicitly focuses host discovery deferred messaging, `host_state=DEFERRED` remains the default.

Shared accessibility baseline (every fixture):

```text
ACCESSIBILITY_BASELINE =
  semantic h1 Visão Geral; section headings for panels
  status text + technical code (not color alone)
  DADOS_DEMONSTRATIVOS badge with accessible name
  next-safe-action keyboard focusable with plain-language name
  evidence links with accessible_name
  announce stale/partial/error via live region when applicable
```

---

## 1. healthy_collection_not_ready

```text
FIXTURE_ID = fx_overview_healthy_not_ready_001
DADOS_DEMONSTRATIVOS = true
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
PURPOSE = Show healthy collection coexisting with NOT_READY without alarmism
EXPECTED_OPERATIONAL_STATE = HEALTHY_COLLECTION (readiness block NOT_READY)
EXPECTED_PRIMARY_MESSAGE = Coleta operacional saudável; prontidão ainda não atendida
EXPECTED_TECHNICAL_DETAIL = overall_operational_state=HEALTHY_COLLECTION; readiness_status=NOT_READY; WINDOW_DAYS_INSUFFICIENT
EXPECTED_NEXT_SAFE_ACTION = Continuar coleta; aguardar critérios (CONTINUE_COLLECTION)
EXPECTED_STATUS_SEMANTICS = SUCCESS_OPS on collection; ATTENTION on readiness; NOT_READY != ERROR
MISSING_FIELDS = none for primary panels; open_incidents=UNAVAILABLE
ACCESSIBILITY_EXPECTATIONS = ACCESSIBILITY_BASELINE; announce dual status (healthy + not ready) without ERROR tone
```

| Overview ViewModel field | Value |
|--------------------------|-------|
| overall_operational_state | HEALTHY_COLLECTION (with readiness NOT_READY shown separately) |
| overall_visual_semantic | SUCCESS_OPS + ATTENTION on readiness block |
| collection_status | IN_PROGRESS |
| last_completed_execution_id | synth-run-healthy-001 |
| last_completed_execution_status | COMPLETE |
| last_completed_execution_finished_at | 2026-07-18T12:00:00+00:00 (SYNTHETIC) |
| last_failed_execution_id | null |
| future_unseen_cutoff | 2026-07-18T01:30:00+00:00 (SYNTHETIC) |
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
| data_availability | DATA_CURRENT |
| evidence_links | synthetic readiness + automation_state + cycle_report (demo paths) |

---

## 2. collection_warning

```text
FIXTURE_ID = fx_overview_collection_warning_001
DADOS_DEMONSTRATIVOS = true
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
PURPOSE = Soft collection warnings map to ATTENTION / DEGRADED — not ERROR
EXPECTED_OPERATIONAL_STATE = DEGRADED
EXPECTED_PRIMARY_MESSAGE = Coleta com avisos; sem falha dura
EXPECTED_TECHNICAL_DETAIL = overall_operational_state=DEGRADED; last_completed=PARTIAL; soft provider timeout (synthetic)
EXPECTED_NEXT_SAFE_ACTION = Continuar coleta; revisar avisos (CONTINUE_COLLECTION)
EXPECTED_STATUS_SEMANTICS = ATTENTION; warning != ERROR; BLOCKED != FAILED
MISSING_FIELDS = none critical
ACCESSIBILITY_EXPECTATIONS = ACCESSIBILITY_BASELINE; announce ATTENTION not ERROR
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
| data_availability | DATA_CURRENT |

---

## 3. collection_failure

```text
FIXTURE_ID = fx_overview_collection_failure_001
DADOS_DEMONSTRATIVOS = true
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
PURPOSE = Real ops failure shows ERROR without inventing scientific invalidation
EXPECTED_OPERATIONAL_STATE = ERROR
EXPECTED_PRIMARY_MESSAGE = Falha operacional real detectada na última execução
EXPECTED_TECHNICAL_DETAIL = last_failed_execution_status=FAILED; failure_category=PROVIDER (synthetic)
EXPECTED_NEXT_SAFE_ACTION = Investigar execução falha (INVESTIGATE_FAILED_EXECUTION)
EXPECTED_STATUS_SEMANTICS = ERROR for ops failure; does not claim scientific rejection beyond ops
MISSING_FIELDS = open_incidents=UNAVAILABLE
ACCESSIBILITY_EXPECTATIONS = ACCESSIBILITY_BASELINE; error announcement via live region; evidence link named
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
| last_failed_execution_finished_at | 2026-07-18T15:30:00+00:00 (SYNTHETIC) |
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
| data_availability | DATA_CURRENT |

---

## 4. host_discovery_deferred

```text
FIXTURE_ID = fx_overview_host_discovery_deferred_001
DADOS_DEMONSTRATIVOS = true
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
PURPOSE = Host deferred is debt/attention, not host failure
EXPECTED_OPERATIONAL_STATE = NOT_READY
EXPECTED_PRIMARY_MESSAGE = Discovery do host ainda diferida
EXPECTED_TECHNICAL_DETAIL = host_state=DEFERRED; operational_debt=OPEN; scheduler=BLOCKED
EXPECTED_NEXT_SAFE_ACTION = Executar discovery no host persistente (RUN_HOST_DISCOVERY)
EXPECTED_STATUS_SEMANTICS = ATTENTION + DEFERRED; DEFERRED != FAILED
MISSING_FIELDS = live discovery result
ACCESSIBILITY_EXPECTATIONS = ACCESSIBILITY_BASELINE; deferred announced as not failure
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
| data_availability | DATA_CURRENT |

---

## 5. scheduler_not_activated

```text
FIXTURE_ID = fx_overview_scheduler_not_activated_001
DADOS_DEMONSTRATIVOS = true
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
PURPOSE = Prepared templates ≠ activated; never show timer as active
EXPECTED_OPERATIONAL_STATE = NOT_READY
EXPECTED_PRIMARY_MESSAGE = Scheduler permanece inativo / não autorizado
EXPECTED_TECHNICAL_DETAIL = scheduler_state=BLOCKED; activation_authorization_state=NOT_AUTHORIZED; templates prepared
EXPECTED_NEXT_SAFE_ACTION = Manter scheduler inativo (KEEP_SCHEDULER_INACTIVE)
EXPECTED_STATUS_SEMANTICS = BLOCKED on scheduler pill; BLOCKED != FAILED
MISSING_FIELDS = scheduler_last_trigger; scheduler_next_trigger
ACCESSIBILITY_EXPECTATIONS = ACCESSIBILITY_BASELINE; blocked announced without failure tone
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
| data_availability | DATA_CURRENT |

---

## 6. readiness_ready_but_validation_not_authorized

```text
FIXTURE_ID = fx_overview_ready_no_validate_001
DADOS_DEMONSTRATIVOS = true
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
PURPOSE = READY ≠ validate; no economic/scientific success claim
EXPECTED_OPERATIONAL_STATE = BLOCKED (validate unauthorized) with readiness READY
EXPECTED_PRIMARY_MESSAGE = READY não autoriza validate
EXPECTED_TECHNICAL_DETAIL = readiness_status=READY; validate_authorized=false; human_authorization_required=true
EXPECTED_NEXT_SAFE_ACTION = Não executar validate (DO_NOT_VALIDATE)
EXPECTED_STATUS_SEMANTICS = SUCCESS_OPS on readiness + BLOCKED on validate; READY != VALIDATION_AUTHORIZED
MISSING_FIELDS = none; validation_command_executed=false always
ACCESSIBILITY_EXPECTATIONS = ACCESSIBILITY_BASELINE; primary message plain-language first; no validate CTA
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
| data_availability | DATA_CURRENT |

---

## 7. no_execution_history

```text
FIXTURE_ID = fx_overview_no_execution_history_001
DADOS_DEMONSTRATIVOS = true
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
PURPOSE = EMPTY overview without fabricating history; NO_HISTORY != SYSTEM_FAILURE
EXPECTED_OPERATIONAL_STATE = EMPTY
EXPECTED_PRIMARY_MESSAGE = Ainda não há resumo operacional para mostrar
EXPECTED_TECHNICAL_DETAIL = last_completed=null; last_failed=null; readiness=UNAVAILABLE; DATA_ABSENT
EXPECTED_NEXT_SAFE_ACTION = Continuar coleta; aguardar critérios (CONTINUE_COLLECTION)
EXPECTED_STATUS_SEMANTICS = INFO / EMPTY; UNKNOWN/EMPTY != FAILED
MISSING_FIELDS = last_completed_execution; last_failed_execution; readiness_report; timeline_items
ACCESSIBILITY_EXPECTATIONS = ACCESSIBILITY_BASELINE; empty state announced; no fabricated evidence links
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
| data_availability | DATA_ABSENT |
| timeline_items | [] |

---

## 8. partial_metadata

```text
FIXTURE_ID = fx_overview_partial_metadata_001
DADOS_DEMONSTRATIVOS = true
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
PURPOSE = PARTIAL/UNAVAILABLE explicit; PARTIAL_METADATA != FABRICATED_DATA
EXPECTED_OPERATIONAL_STATE = PARTIAL
EXPECTED_PRIMARY_MESSAGE = Parte dos painéis ainda não tem dados
EXPECTED_TECHNICAL_DETAIL = automation_state missing; readiness present; host discovery missing; DATA_PARTIAL
EXPECTED_NEXT_SAFE_ACTION = Indisponível — dados parciais (PARTIAL_DATA_UNAVAILABLE)
EXPECTED_STATUS_SEMANTICS = ATTENTION / PARTIAL; missing fields marked NOT_AVAILABLE
MISSING_FIELDS = automation_state; last_completed_execution; discovery result; lock_state; backups
ACCESSIBILITY_EXPECTATIONS = ACCESSIBILITY_BASELINE; announce partial; do not present missing as current
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
| data_availability | DATA_PARTIAL |
| provenance_footer | readiness_report present; automation_state missing; host discovery missing |

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

```text
TYPESCRIPT_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
```

When UI work is authorized, materialize these as JSON under a demo fixtures directory (path decided then). This task ships **scenario specs only** — no executable fixture files.
