# UX-R1 — Operational MVP Data Contract Catalog

```text
DOCUMENT = UX-R1-OPERATIONAL-MVP_DATA-CONTRACT-CATALOG
VERSION = 1.0.0
RELEASE = UX-R1
BACKLOG_ITEM = UX-B3
TASK_ID = OPERATIONAL-MVP-SCREEN-CONTRACTS-001
UI_IMPLEMENTATION_AUTHORIZED = false
EFFECTIVE_AT = 2026-07-19T13:45:00Z
```

Legend — SOURCE_TYPE: `REPOSITORY_DOCUMENT` | `RUN_ARTIFACT` | `STORE_METADATA` | `READINESS_REPORT` | `SCHEDULER_METADATA` | `HOST_DISCOVERY_RESULT` | `DERIVED_READ_ONLY` | `DEMONSTRATION_FIXTURE`

Security: `PUBLIC_OPERATIONAL` | `INTERNAL_OPERATIONAL` | `SENSITIVE` | `SECRET`

Availability notes refer to checkout discovery at BASE_SHA of the impact assessment.

---

## Screen 1 — Visão Geral

| FIELD_NAME | USER_LABEL | TECHNICAL_LABEL | SOURCE_TYPE | SOURCE_PATH | SOURCE_FIELD | TRANSFORM | FRESHNESS | NULL_BEHAVIOR | EMPTY_STATE | ERROR_STATE | SECURITY_CLASSIFICATION | SCIENTIFIC_SAFETY_NOTE |
|------------|------------|-----------------|-------------|-------------|--------------|-----------|-----------|---------------|-------------|-------------|-------------------------|------------------------|
| overall_operational_state | Estado operacional | overall_operational_state | DERIVED_READ_ONLY | compose readiness + automation_state + host/scheduler docs | multiple | priority rules in SPEC §4 | on refresh | show UNKNOWN | show EMPTY overview | show ERROR banner | PUBLIC_OPERATIONAL | NOT_READY ≠ ERROR |
| collection_status | Coleta | collection_status | STORE_METADATA | data/future_unseen/manifests/collection_state.json | R3E_FUTURE_DATA_COLLECTION | passthrough | artifact mtime | UNAVAILABLE | EMPTY | ERROR if unreadable | PUBLIC_OPERATIONAL | collecting ≠ validated |
| last_completed_execution_id | Última execução concluída | last_completed_run_id | RUN_ARTIFACT | reports/r3e_future_unseen/automation_state.json | last_run_id when last_run_status in COMPLETE/PARTIAL/NO_NEW_DATA | filter by status | automation_state.updated_at | null → “Nenhuma” | EMPTY | UNAVAILABLE if state missing | INTERNAL_OPERATIONAL | dry_run may count as completed ops cycle |
| last_completed_execution_status | Status da última conclusão | last_completed_run_status | RUN_ARTIFACT | automation_state.json / cycle_report.json | last_run_status / status | passthrough | same | null | EMPTY | UNAVAILABLE | PUBLIC_OPERATIONAL | SUCCESS ≠ profit |
| last_failed_execution_id | Última execução falha | last_failed_run_id | DERIVED_READ_ONLY | automation_runs/*/cycle_report.json | run_id where status=FAILED | scan newest first | on refresh | null → “Nenhuma falha registrada” | EMPTY | UNAVAILABLE | INTERNAL_OPERATIONAL | do not invent failures |
| future_unseen_cutoff | Corte future-unseen | FUTURE_UNSEEN_CUTOFF | STORE_METADATA | data/future_unseen/manifests/cutoff_manifest.json | FUTURE_UNSEEN_CUTOFF | ISO display w/ TZ | immutable | UNAVAILABLE | EMPTY | ERROR | PUBLIC_OPERATIONAL | cutoff immutable |
| store_observation_count | Observações no store | n_observations_total | READINESS_REPORT / RUN_ARTIFACT | readiness_report.json or ops_report.json | n_observations_total / last_store_after | prefer readiness | report generated_at | UNAVAILABLE | 0 is valid EMPTY store | ERROR | PUBLIC_OPERATIONAL | count ≠ readiness |
| readiness_status_summary | Prontidão | readiness_status | READINESS_REPORT | reports/r3e_future_unseen/readiness_report.json | readiness_status | map language guide | generated_at | UNAVAILABLE | treat missing as UNAVAILABLE not NOT_READY | ERROR | PUBLIC_OPERATIONAL | NOT_READY ≠ failure |
| readiness_primary_reason | Motivo principal | readiness_reason | READINESS_REPORT | readiness_report.json | readiness_reason | plain-language map | generated_at | null | EMPTY | ERROR | PUBLIC_OPERATIONAL | reason codes technical secondary |
| window_progress | Janela de dias | window_days / required_window_days | READINESS_REPORT | readiness_report.json | window_days, required_window_days | ratio display | generated_at | UNAVAILABLE | EMPTY | ERROR | PUBLIC_OPERATIONAL | progress ≠ READY authorize |
| host_state | Host | host_discovery_status | REPOSITORY_DOCUMENT / HOST_DISCOVERY_RESULT | docs/PROJECT.md + discovery result if present | HOST_DISCOVERY / HOST_DISCOVERY_STATUS | default DEFERRED | doc/result | DEFERRED | EMPTY result file expected | ERROR only if result invalid | PUBLIC_OPERATIONAL | deferred ≠ failed host |
| scheduler_state | Automação | scheduler_activation_state | REPOSITORY_DOCUMENT / SCHEDULER_METADATA | checklist + history CLI | SCHEDULER_ACTIVATION / AUTHORIZED/ACTIVATED | force blocked defaults | on refresh | BLOCKED | not activated | ERROR if contradictory activated without auth | PUBLIC_OPERATIONAL | never show active without evidence |
| open_incidents_count | Incidentes abertos | open_incidents_count | DERIVED_READ_ONLY | incident store not present in MVP | — | always EMPTY/UNAVAILABLE until UX-B7 | — | 0 / UNAVAILABLE | EMPTY | ERROR | PUBLIC_OPERATIONAL | do not invent incidents |
| operational_debt_status | Dívida operacional | OPERATIONAL_DEBT | DERIVED_READ_ONLY | discovery + checklist + scheduler flags | constellation | fixed OPEN while deferred/blocked | on refresh | OPEN | never COMPLETED while deferred | ERROR | PUBLIC_OPERATIONAL | OPEN ≠ scientific fail |
| scientific_gate_state | Gate científico | R3E_GATE | STORE_METADATA / READINESS_REPORT | collection_state.json / readiness scientific_safety | R3E_GATE | passthrough | artifact | UNAVAILABLE | EMPTY | ERROR | PUBLIC_OPERATIONAL | pending ≠ rejected edge claim |
| validate_authorized | Validate autorizado | VALIDATE_AUTHORIZED | READINESS_REPORT / RUN_ARTIFACT | scientific_safety / automation_state | VALIDATE_AUTHORIZED | boolean display | artifact | false default | false | ERROR | PUBLIC_OPERATIONAL | must stay false unless explicit auth |
| next_safe_action | Próxima ação segura | next_safe_action | DERIVED_READ_ONLY | SPEC §4 rules | multiple | rule table | on refresh | “Indisponível — dados parciais” | EMPTY | ERROR | PUBLIC_OPERATIONAL | never suggest validate |
| economic_interpretation_allowed | Interpretação econômica | ECONOMIC_INTERPRETATION_ALLOWED | STORE_METADATA | collection_state / scientific_safety | ECONOMIC_INTERPRETATION_ALLOWED | always show false badge | artifact | false | false | ERROR | PUBLIC_OPERATIONAL | always false in MVP |

---

## Screen 2 — Execuções

| FIELD_NAME | USER_LABEL | TECHNICAL_LABEL | SOURCE_TYPE | SOURCE_PATH | SOURCE_FIELD | TRANSFORM | FRESHNESS | NULL_BEHAVIOR | EMPTY_STATE | ERROR_STATE | SECURITY_CLASSIFICATION | SCIENTIFIC_SAFETY_NOTE |
|------------|------------|-----------------|-------------|-------------|--------------|-----------|-----------|---------------|-------------|-------------|-------------------------|------------------------|
| execution_list | Lista de execuções | executions[] | RUN_ARTIFACT | reports/r3e_future_unseen/automation_runs/*/cycle_report.json (+ collection_runs) | run_id, status, … | index scan | on refresh | empty list | EMPTY list message | ERROR if dir unreadable | INTERNAL_OPERATIONAL | only evidenced runs |
| run_id | ID da execução | run_id | RUN_ARTIFACT | cycle_report.json / collection_run.json | run_id / collection_run_id | passthrough | run finished_at | UNAVAILABLE | — | ERROR | INTERNAL_OPERATIONAL | copy allowed |
| status | Status | status | RUN_ARTIFACT | cycle_report.json | status | enum map | finished_at | UNAVAILABLE | — | FAILED→ERROR semantic | PUBLIC_OPERATIONAL | COMPLETE ≠ edge |
| started_at | Início | started_at | RUN_ARTIFACT | cycle_report.json | started_at | TZ display | — | UNAVAILABLE | — | ERROR | PUBLIC_OPERATIONAL | UTC+offset |
| finished_at | Fim | finished_at | RUN_ARTIFACT | cycle_report.json | finished_at | TZ display | — | null if running/unknown | — | ERROR | PUBLIC_OPERATIONAL | UTC+offset |
| duration | Duração | duration_seconds | DERIVED_READ_ONLY | started_at, finished_at | — | subtract | — | UNAVAILABLE | — | ERROR | PUBLIC_OPERATIONAL | — |
| trigger_type | Origem | trigger_type | DERIVED_READ_ONLY | dry_run_only + scheduler evidence | dry_run_only | SPEC §5 rules | — | UNKNOWN | UNKNOWN | ERROR | PUBLIC_OPERATIONAL | do not mark SCHEDULER while blocked without proof |
| host_identity | Host | hostname | RUN_ARTIFACT / HOST_DISCOVERY_RESULT | lock meta / discovery | hostname / host | mask | — | UNKNOWN | EMPTY | ERROR | SENSITIVE | masked |
| command_type | Comando | command_type | DERIVED_READ_ONLY | kind / dry_run_only | kind | map run-cycle/collect/dry-run | — | UNKNOWN | — | ERROR | PUBLIC_OPERATIONAL | — |
| observations_accepted | Barras aceitas | observations_accepted | RUN_ARTIFACT | cycle_report.json | observations_accepted | int | — | 0 | 0 | ERROR | PUBLIC_OPERATIONAL | — |
| observations_rejected | Barras rejeitadas | observations_rejected | RUN_ARTIFACT | cycle_report.json | observations_rejected | int | — | 0 | 0 | ERROR | PUBLIC_OPERATIONAL | — |
| store_before | Store antes | store_before | RUN_ARTIFACT | cycle_report.json | store_before | int | — | UNAVAILABLE | — | ERROR | PUBLIC_OPERATIONAL | — |
| store_after | Store depois | store_after | RUN_ARTIFACT | cycle_report.json | store_after | int | — | UNAVAILABLE | — | ERROR | PUBLIC_OPERATIONAL | — |
| idempotency_status | Idempotência | idempotency_status | RUN_ARTIFACT | cycle_report.json | idempotency_status | passthrough | — | UNAVAILABLE | EMPTY | ERROR | PUBLIC_OPERATIONAL | — |
| readiness_before_after | Prontidão antes/depois | readiness_transition | RUN_ARTIFACT | cycle_report.json | readiness_transition / readiness_status | split display | — | UNAVAILABLE | EMPTY | ERROR | PUBLIC_OPERATIONAL | transition ≠ validate |
| warnings | Avisos | provider_failures / soft gaps | RUN_ARTIFACT | cycle_report.json + gap_report.json | provider_failures, gaps | list | — | empty list | EMPTY | — | INTERNAL_OPERATIONAL | warning ≠ ERROR |
| failures | Falhas | hard_error / timed_out / rejections | RUN_ARTIFACT | cycle_report + rejections.json | hard_error, timed_out, rejections | map taxonomy | — | empty | EMPTY | ERROR semantic | INTERNAL_OPERATIONAL | plain language + code |
| failure_category | Categoria de falha | failure_category | DERIVED_READ_ONLY | taxonomy + ops_hardening | failure_category | map | — | null | EMPTY | ERROR | PUBLIC_OPERATIONAL | use taxonomy doc |
| lock_result | Resultado do lock | lock | RUN_ARTIFACT | cycle_report.json | lock / status SKIPPED_LOCKED | summarize | — | ABSENT ok | EMPTY | STALE/INVALID attention | INTERNAL_OPERATIONAL | UI must not clear lock |
| backup_evidence | Evidência de backup | backup_verification | RUN_ARTIFACT / DERIVED_READ_ONLY | backups/ + verify script output | BACKUP_VERIFICATION | link or UNAVAILABLE | — | UNAVAILABLE | EMPTY not FAIL | FAIL only if verify FAIL | INTERNAL_OPERATIONAL | missing ≠ fail |
| artifact_links | Artefatos | run_dir + files | RUN_ARTIFACT | run_dir | paths | list existing files only | — | empty | EMPTY | ERROR | SENSITIVE (paths masked) | read-only open |
| filter_date_range | Período | from/to | DERIVED_READ_ONLY | URL query | started_at | filter | — | no filter | — | ERROR invalid range | PUBLIC_OPERATIONAL | — |
| filter_status | Filtro status | status | DERIVED_READ_ONLY | URL query | status | filter | — | all | — | ERROR | PUBLIC_OPERATIONAL | — |
| filter_trigger | Filtro origem | trigger | DERIVED_READ_ONLY | URL query | trigger_type | filter | — | all | — | ERROR | PUBLIC_OPERATIONAL | — |
| filter_host | Filtro host | host | DERIVED_READ_ONLY | URL query | host_identity | filter masked | — | all | — | ERROR | SENSITIVE | — |
| filter_command | Filtro comando | command | DERIVED_READ_ONLY | URL query | command_type | filter | — | all | — | ERROR | PUBLIC_OPERATIONAL | — |
| filter_failure_category | Filtro falha | failure_category | DERIVED_READ_ONLY | URL query | failure_category | filter | — | all | — | ERROR | PUBLIC_OPERATIONAL | — |
| filter_readiness_transition | Filtro transição | readiness_transition | DERIVED_READ_ONLY | URL query | readiness_transition | filter | — | all | — | ERROR | PUBLIC_OPERATIONAL | — |
| pagination | Paginação | page/page_size | DERIVED_READ_ONLY | URL query | — | page_size default 25 | — | page 1 | EMPTY page | ERROR | PUBLIC_OPERATIONAL | no invented pages |

---

## Screen 3 — Readiness

| FIELD_NAME | USER_LABEL | TECHNICAL_LABEL | SOURCE_TYPE | SOURCE_PATH | SOURCE_FIELD | TRANSFORM | FRESHNESS | NULL_BEHAVIOR | EMPTY_STATE | ERROR_STATE | SECURITY_CLASSIFICATION | SCIENTIFIC_SAFETY_NOTE |
|------------|------------|-----------------|-------------|-------------|--------------|-----------|-----------|---------------|-------------|-------------|-------------------------|------------------------|
| readiness_status | Status de prontidão | readiness_status | READINESS_REPORT | reports/r3e_future_unseen/readiness_report.json | readiness_status | language map | generated_at | UNAVAILABLE | — | ERROR if parse fail | PUBLIC_OPERATIONAL | NOT_READY ≠ failure; READY ≠ validate |
| not_ready_reasons | Motivos de não pronto | not_ready_reasons[] | READINESS_REPORT | readiness_report.json | not_ready_reasons | code+detail+plain | generated_at | empty list | EMPTY | ERROR | PUBLIC_OPERATIONAL | ATTENTION semantic |
| blockers | Bloqueios | blockers[] | READINESS_REPORT | readiness_report.json | blockers | code+detail+plain | generated_at | empty list | EMPTY | BLOCKED semantic | PUBLIC_OPERATIONAL | BLOCKED ≠ ERROR unless integrity |
| window_days | Dias decorridos | window_days | READINESS_REPORT | readiness_report.json | window_days | float display | generated_at | UNAVAILABLE | — | ERROR | PUBLIC_OPERATIONAL | — |
| required_window_days | Dias mínimos | required_window_days | READINESS_REPORT | readiness_report.json | required_window_days | int (90) | generated_at | UNAVAILABLE | — | ERROR | PUBLIC_OPERATIONAL | threshold frozen |
| series_completeness | Completude de séries | series_complete/partial/missing/blocked | READINESS_REPORT | readiness_report.json | series_* | tables | generated_at | empty arrays | EMPTY | ERROR | PUBLIC_OPERATIONAL | — |
| coverage | Cobertura | series_counts / n_observations_total | READINESS_REPORT | readiness_report.json | series_counts, n_observations_total | tables | generated_at | 0 | EMPTY | ERROR | PUBLIC_OPERATIONAL | — |
| freshness | Atualidade da avaliação | as_of / generated_at | READINESS_REPORT | readiness_report.json | as_of, generated_at | TZ + stale check | generated_at | UNAVAILABLE | — | STALE warning | PUBLIC_OPERATIONAL | — |
| gaps | Lacunas | gap_status | READINESS_REPORT | readiness_report.json | gap_status | counts + critical flag | generated_at | empty | EMPTY | CRITICAL→BLOCKED | PUBLIC_OPERATIONAL | informational gaps ≠ fail |
| duplicates | Duplicatas | duplicates_flagged | READINESS_REPORT | readiness_report.json | duplicates_flagged | int | generated_at | 0 | EMPTY | >0 attention/block per rules | PUBLIC_OPERATIONAL | — |
| store_integrity | Integridade do store | hash_status / manifest_status | READINESS_REPORT | readiness_report.json | hash_status, manifest_status | OK/ERR | generated_at | UNAVAILABLE | — | ERROR | PUBLIC_OPERATIONAL | integrity ERROR real |
| last_readiness_evaluation | Última avaliação | generated_at + derived_from_run | READINESS_REPORT / RUN_ARTIFACT | readiness_report + automation_state | generated_at, derived_from_run | link to run | generated_at | UNAVAILABLE | EMPTY | ERROR | INTERNAL_OPERATIONAL | — |
| historical_readiness_evaluations | Histórico de avaliações | history[] | RUN_ARTIFACT | automation_runs/*/readiness_report.json | readiness_status, generated_at | list newest first | on refresh | empty | EMPTY | ERROR | INTERNAL_OPERATIONAL | do not invent |
| ready_transition_evidence | Evidência de transição READY | READY transition | RUN_ARTIFACT | cycle_report readiness_transition | readiness_transition | show only if evidenced | — | null | EMPTY | ERROR | PUBLIC_OPERATIONAL | READY still no validate |
| scientific_gate_consequence | Consequência científica | scientific_safety | READINESS_REPORT | readiness_report.json | scientific_safety.* | mandatory copy block | generated_at | show defaults false/blocked | — | ERROR | PUBLIC_OPERATIONAL | never imply validate unlocked |
| collector_status | Estado do coletor | collector_status | READINESS_REPORT | readiness_report.json | collector_status | passthrough | generated_at | UNAVAILABLE | EMPTY | ERROR | PUBLIC_OPERATIONAL | IN_PROGRESS expected |
| store_roots | Raízes do store | store_roots | READINESS_REPORT | readiness_report.json | store_roots | mask paths | generated_at | UNAVAILABLE | EMPTY | ERROR | SENSITIVE | masked paths |
| thresholds_source | Origem dos limiares | thresholds_source | READINESS_REPORT | readiness_report.json | thresholds_source | expand technical | generated_at | UNAVAILABLE | EMPTY | ERROR | INTERNAL_OPERATIONAL | frozen thresholds |

---

## Screen 4 — Host e Scheduler

| FIELD_NAME | USER_LABEL | TECHNICAL_LABEL | SOURCE_TYPE | SOURCE_PATH | SOURCE_FIELD | TRANSFORM | FRESHNESS | NULL_BEHAVIOR | EMPTY_STATE | ERROR_STATE | SECURITY_CLASSIFICATION | SCIENTIFIC_SAFETY_NOTE |
|------------|------------|-----------------|-------------|-------------|--------------|-----------|-----------|---------------|-------------|-------------|-------------------------|------------------------|
| host_strategy | Estratégia de host | ACTIVE_HOST_STRATEGY | REPOSITORY_DOCUMENT | docs/operations/R3E_HOSTGATOR_VPS_READINESS_DECISIONS.md | ACTIVE_HOST_STRATEGY | passthrough LOCAL_PERSISTENT_HOST | doc | UNAVAILABLE | EMPTY | ERROR | PUBLIC_OPERATIONAL | HostGator deferred |
| host_identity | Identidade do host | host identity | HOST_DISCOVERY_RESULT | R3E_LOCAL_HOST_DISCOVERY_RESULT.md | hostname/OS fields | mask | result mtime | UNKNOWN / DEFERRED | EMPTY expected | ERROR if invalid result | SENSITIVE | masked |
| host_discovery_status | Discovery | HOST_DISCOVERY | REPOSITORY_DOCUMENT / HOST_DISCOVERY_RESULT | docs/PROJECT.md / result | HOST_DISCOVERY / HOST_DISCOVERY_STATUS | default DEFERRED | doc/result | DEFERRED | EMPTY | ERROR | PUBLIC_OPERATIONAL | deferred ≠ failed |
| operational_debt_status | Dívida operacional | OPERATIONAL_DEBT | DERIVED_READ_ONLY | discovery+checklist+scheduler | constellation | OPEN while deferred/blocked | on refresh | OPEN | never done | ERROR | PUBLIC_OPERATIONAL | OPEN visible |
| durable_store_path_state | Store persistente | durable_store_path | HOST_DISCOVERY_RESULT / REPOSITORY_DOCUMENT | discovery / R3E_LOCAL_PERSISTENT_HOST_DISCOVERY.md | LOCAL_ROOT / template $HOME/wick-r3e | mask path + exists? | result | UNAVAILABLE | EMPTY | ERROR if exists=false after discovery | SENSITIVE | masked |
| log_path_state | Caminho de logs | log_path | HOST_DISCOVERY_RESULT / SCHEDULER_METADATA | discovery / healthcheck | logs path | mask | result | UNAVAILABLE | EMPTY | ERROR | SENSITIVE | masked |
| backup_path_state | Caminho de backups | backup_path | DERIVED_READ_ONLY | backups/ or discovery | path | mask; missing→UNAVAILABLE | on refresh | UNAVAILABLE | EMPTY not FAIL | FAIL only verify FAIL | SENSITIVE | missing ≠ fail |
| lock_path_state | Lock | LOCK_STATUS | DERIVED_READ_ONLY | lock-status CLI / automation.lock | LOCK_STATUS | ABSENT/ACTIVE/STALE/INVALID | on refresh | ABSENT idle OK | EMPTY | STALE/INVALID attention | INTERNAL_OPERATIONAL | no unlock action |
| scheduler_type | Tipo de scheduler | SCHEDULER_MECHANISM | HOST_DISCOVERY_RESULT / REPOSITORY_DOCUMENT | discovery / ops/local/systemd | systemd timer etc | passthrough | result/doc | UNAVAILABLE | EMPTY | ERROR | PUBLIC_OPERATIONAL | prepared template ≠ active |
| scheduler_registered | Registrado | scheduler_registered | SCHEDULER_METADATA / HOST_DISCOVERY_RESULT | healthcheck / discovery | registered flag | default false | on refresh | false | false | ERROR | PUBLIC_OPERATIONAL | false while blocked |
| scheduler_enabled | Habilitado | scheduler_enabled | SCHEDULER_METADATA | healthcheck / checklist | enabled / ACTIVATED | **must be false** without auth evidence | on refresh | false | false | contradict→ERROR | PUBLIC_OPERATIONAL | do not show active |
| scheduler_last_trigger | Último disparo | scheduler_last_trigger | SCHEDULER_METADATA / RUN_ARTIFACT | timer status / runs | last trigger ts | TZ; null if none | on refresh | null → “Nenhum” | EMPTY | ERROR | PUBLIC_OPERATIONAL | — |
| scheduler_next_trigger | Próximo disparo | scheduler_next_trigger | SCHEDULER_METADATA | timer status | next | null while disabled | on refresh | null | EMPTY | ERROR | PUBLIC_OPERATIONAL | null while blocked |
| scheduler_health | Saúde do scheduler | scheduler_health | DERIVED_READ_ONLY | healthcheck KEY=VALUE | STATUS / SCHEDULER_* | map HEALTHY/DEGRADED/BLOCKED/FAILED/UNAVAILABLE | on refresh | UNAVAILABLE | EMPTY | FAILED | PUBLIC_OPERATIONAL | prepared ≠ healthy-active |
| manual_run_availability | Execução manual | manual_run_available | REPOSITORY_DOCUMENT | runbooks / CLI docs | — | informational true on ops host | doc | UNAVAILABLE | EMPTY | ERROR | PUBLIC_OPERATIONAL | UI must not execute |
| activation_authorization_state | Autorização de ativação | SCHEDULER_ACTIVATION_AUTHORIZED | REPOSITORY_DOCUMENT / SCHEDULER_METADATA | checklist + history | AUTHORIZED | false / NOT_AUTHORIZED | doc | false | false | ERROR if true without checklist | PUBLIC_OPERATIONAL | BLOCKED |
| hostgator_status | HostGator | HOST_READINESS_STATUS | REPOSITORY_DOCUMENT | R3E_HOSTGATOR_VPS_READINESS_DECISIONS.md | HOST_READINESS_STATUS | DEFERRED_FUTURE_MIGRATION | doc | DEFERRED | EMPTY | ERROR | PUBLIC_OPERATIONAL | deferred migration |
| systemd_templates_prepared | Templates preparados | templates_present | REPOSITORY_DOCUMENT | ops/local/systemd/* | file presence | boolean prepared | repo | false | EMPTY | ERROR | PUBLIC_OPERATIONAL | prepared ≠ enabled |

---

## Cross-cutting derived fields

| FIELD_NAME | Notes |
|------------|-------|
| stale_flag | true if primary artifact older than screen threshold |
| data_mode | LIVE_ARTIFACTS \| PARTIAL \| DEMONSTRATION_FIXTURE |
| provenance_footer | list SOURCE_PATH heads used for the render |

Fixtures override SOURCE_TYPE to `DEMONSTRATION_FIXTURE` and must set `fixture_label=DADOS_DEMONSTRATIVOS`.
