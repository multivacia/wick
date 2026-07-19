# UX-R1-I6A — Overview ViewModel Contract

```text
DOCUMENT = UX-R1-I6A-OVERVIEW-VIEWMODEL-CONTRACT
VERSION = 1.0.0
RELEASE = UX-R1
WORKSTREAM = I6A
TASK_ID = OVERVIEW-SCREEN-DATA-AND-FIXTURE-PREPARATION-001
SCREEN = Visão Geral
ROUTE_KEY = / or /overview
PHASE = DATA_CONTRACT_AND_FIXTURE_PREPARATION
UI_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
NO_VIEWMODEL_IMPLEMENTATION = true
NO_SCREEN_IMPLEMENTATION = true
NO_OPERATIONAL_INDEX = true
NO_ADAPTER = true
NO_REAL_DATA_INTEGRATION = true
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
EFFECTIVE_AT = 2026-07-19T16:54:39Z
```

## 1. Purpose

Define the **read-only** ViewModel field contract for Visão Geral so a future UI can render operational state without inventing scientific or economic meaning.

This document is a data contract. It does **not** implement TypeScript types, hooks, adapters, or screens.

## 2. Normative sources

- `docs/ux/UX-R1-OPERATIONAL-MVP_DATA-CONTRACT-CATALOG.md` — Screen 1
- `docs/ai-specs/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS_SPEC.md` — §4
- `docs/ux/UX-R1-OPERATIONAL-MVP_STATE-MATRIX.md` — Visão Geral states
- UX-B4 language catalogs (labels and microcopy)

## 3. ViewModel shape (logical)

```text
OverviewViewModel (read-only)
├── overall_operational_state
├── collection_status
├── last_completed_execution { id, status, finished_at, evidence_link }
├── last_failed_execution { id, status, finished_at, evidence_link } | null
├── store_summary { future_unseen_cutoff, store_observation_count }
├── readiness_summary { status, primary_reason, window_days, required_window_days, window_progress_ratio }
├── host_state
├── scheduler_state
├── open_incidents_count
├── operational_debt_status
├── scientific_gate { r3e_gate, validate_authorized, economic_interpretation_allowed }
├── next_safe_action
├── freshness { generated_at, stale_flag, data_mode, freshness_label }
└── evidence { evidence_links[], provenance_footer, fixture_label? }
```

## 4. Field catalog

Legend — NULLABILITY: `REQUIRED` | `NULLABLE`  
ACCESS: `PUBLIC_OPERATIONAL` | `INTERNAL_OPERATIONAL` | `SENSITIVE`

| FIELD | USER_LABEL | TECHNICAL | TYPE | NULLABILITY | SOURCE (B3) | ACCESS | NOTES |
|-------|------------|-----------|------|-------------|-------------|--------|-------|
| overall_operational_state | Estado operacional | overall_operational_state | enum | REQUIRED | DERIVED_READ_ONLY | PUBLIC_OPERATIONAL | See §5; NOT_READY ≠ ERROR |
| overall_visual_semantic | Semântica visual | visual_semantic | enum | REQUIRED | DERIVED | PUBLIC_OPERATIONAL | NEUTRAL/INFO/ATTENTION/SUCCESS_OPS/ERROR/BLOCKED/DEFERRED |
| collection_status | Coleta | collection_status | enum/string | REQUIRED | STORE_METADATA | PUBLIC_OPERATIONAL | collecting ≠ validated |
| last_completed_execution_id | Última execução concluída | last_completed_run_id | string | NULLABLE | RUN_ARTIFACT | INTERNAL_OPERATIONAL | null → “Nenhuma” |
| last_completed_execution_status | Status da última conclusão | last_completed_run_status | enum | NULLABLE | RUN_ARTIFACT | PUBLIC_OPERATIONAL | SUCCESS ≠ profit |
| last_completed_execution_finished_at | Fim da última conclusão | last_completed_finished_at | datetime TZ | NULLABLE | RUN_ARTIFACT | PUBLIC_OPERATIONAL | ISO-8601 + offset |
| last_completed_execution_evidence_link | Evidência da conclusão | last_completed_evidence_link | link | NULLABLE | RUN_ARTIFACT | SENSITIVE (path masked) | read-only |
| last_failed_execution_id | Última execução falha | last_failed_run_id | string | NULLABLE | DERIVED | INTERNAL_OPERATIONAL | null → “Nenhuma falha registrada” |
| last_failed_execution_status | Status da falha | last_failed_run_status | enum | NULLABLE | DERIVED | PUBLIC_OPERATIONAL | do not invent failures |
| last_failed_execution_finished_at | Fim da falha | last_failed_finished_at | datetime TZ | NULLABLE | DERIVED | PUBLIC_OPERATIONAL | — |
| last_failed_execution_evidence_link | Evidência da falha | last_failed_evidence_link | link | NULLABLE | DERIVED | SENSITIVE (path masked) | — |
| future_unseen_cutoff | Corte future-unseen | FUTURE_UNSEEN_CUTOFF | datetime TZ | NULLABLE | STORE_METADATA | PUBLIC_OPERATIONAL | immutable cutoff |
| store_observation_count | Observações no store | n_observations_total | int | NULLABLE | READINESS/RUN | PUBLIC_OPERATIONAL | 0 valid; count ≠ readiness |
| readiness_status_summary | Prontidão | readiness_status | enum | NULLABLE | READINESS_REPORT | PUBLIC_OPERATIONAL | missing → UNAVAILABLE not NOT_READY |
| readiness_primary_reason | Motivo principal | readiness_reason | string/code | NULLABLE | READINESS_REPORT | PUBLIC_OPERATIONAL | plain language primary |
| window_days | Janela decorrida | window_days | number | NULLABLE | READINESS_REPORT | PUBLIC_OPERATIONAL | — |
| required_window_days | Janela mínima | required_window_days | int | NULLABLE | READINESS_REPORT | PUBLIC_OPERATIONAL | typically 90 |
| window_progress | Progresso da janela | window_progress_ratio | ratio | NULLABLE | DERIVED | PUBLIC_OPERATIONAL | progress ≠ READY authorize |
| host_state | Host | host_discovery_status | enum | REQUIRED | DOC/RESULT | PUBLIC_OPERATIONAL | default DEFERRED; deferred ≠ failed |
| scheduler_state | Automação | scheduler_activation_state | enum | REQUIRED | DOC/META | PUBLIC_OPERATIONAL | force blocked defaults; never active without evidence |
| open_incidents_count | Incidentes abertos | open_incidents_count | int / UNAVAILABLE | REQUIRED | DERIVED | PUBLIC_OPERATIONAL | EMPTY/UNAVAILABLE until UX-B7; do not invent |
| operational_debt_status | Dívida operacional | OPERATIONAL_DEBT | enum | REQUIRED | DERIVED | PUBLIC_OPERATIONAL | OPEN while deferred/blocked |
| scientific_gate_state | Gate científico | R3E_GATE | enum/string | REQUIRED | STORE/READINESS | PUBLIC_OPERATIONAL | pending ≠ rejected edge claim |
| validate_authorized | Validate autorizado | VALIDATE_AUTHORIZED | boolean | REQUIRED | READINESS/RUN | PUBLIC_OPERATIONAL | default false |
| economic_interpretation_allowed | Interpretação econômica | ECONOMIC_INTERPRETATION_ALLOWED | boolean | REQUIRED | STORE/SAFETY | PUBLIC_OPERATIONAL | always false in MVP |
| next_safe_action | Próxima ação segura | next_safe_action | string | REQUIRED | DERIVED §4 | PUBLIC_OPERATIONAL | never suggest validate |
| next_safe_action_code | Código da ação | next_safe_action_code | enum | NULLABLE | DERIVED | PUBLIC_OPERATIONAL | for tests/fixtures |
| generated_at | Gerado em | generated_at | datetime TZ | REQUIRED | DERIVED | PUBLIC_OPERATIONAL | composition time or newest source |
| stale_flag | Desatualizado | stale_flag | boolean | REQUIRED | DERIVED | PUBLIC_OPERATIONAL | true if sources older than 6h |
| data_mode | Modo de dados | data_mode | enum | REQUIRED | DERIVED | PUBLIC_OPERATIONAL | LIVE_ARTIFACTS \| PARTIAL \| DEMONSTRATION_FIXTURE |
| freshness_label | Atualidade | freshness_label | string | REQUIRED | DERIVED | PUBLIC_OPERATIONAL | FRESH / STALE / UNAVAILABLE / PARTIAL |
| evidence_links | Links de evidência | evidence_links[] | list | REQUIRED | DERIVED | SENSITIVE (masked) | existing or synthetic-demo only |
| provenance_footer | Proveniência | provenance_footer | string[] | REQUIRED | DERIVED | INTERNAL_OPERATIONAL | SOURCE_PATH heads |
| fixture_label | Rótulo demo | fixture_label | string | NULLABLE | FIXTURE | PUBLIC_OPERATIONAL | required when DEMONSTRATION_FIXTURE = `DADOS_DEMONSTRATIVOS` |

## 5. overall_operational_state values

| Value | Visual semantic | Plain-language (pt-BR) | When |
|-------|-----------------|------------------------|------|
| ERROR | ERROR | Falha operacional real detectada. | last failed cycle or critical integrity |
| BLOCKED | BLOCKED | Uma condição impede avançar. | hard blockers / forbidden activation context |
| NOT_READY | ATTENTION | Ainda não há dados suficientes ou critérios atendidos. | readiness NOT_READY |
| DEGRADED | ATTENTION | Coleta com avisos; sem falha dura. | warnings / PARTIAL without hard fail |
| HEALTHY_COLLECTION | SUCCESS_OPS | Coleta operacional saudável. | recent COMPLETE/PARTIAL/NO_NEW_DATA, no hard errors |
| UNKNOWN | NEUTRAL / INFO | Estado operacional desconhecido. | core sources missing |
| PARTIAL | ATTENTION | Resumo parcial: alguns blocos indisponíveis. | subset of sources missing |
| EMPTY | INFO | Ainda não há resumo operacional. | no automation_state and no readiness |

Composition priority (highest first) matches Spec §4: ERROR → BLOCKED → NOT_READY/ATTENTION → DEGRADED → HEALTHY_COLLECTION → UNKNOWN.

`HEALTHY_COLLECTION` may coexist with readiness `NOT_READY` displayed in the readiness summary block — never collapse NOT_READY into ERROR.

## 6. next_safe_action_code values

| Code | Plain-language action |
|------|----------------------|
| RUN_HOST_DISCOVERY | Executar discovery no host persistente (runbook) |
| KEEP_SCHEDULER_INACTIVE | Manter scheduler inativo; completar checklist |
| CONTINUE_COLLECTION | Continuar coleta; aguardar critérios |
| INVESTIGATE_FAILED_EXECUTION | Investigar execução falha (abrir Execuções) |
| DO_NOT_VALIDATE | Não executar validate; aguardar autorização humana |
| MONITOR_COLLECTION | Nenhuma ação urgente; monitorar próxima coleta |
| PARTIAL_DATA_UNAVAILABLE | Indisponível — dados parciais |

## 7. Freshness rules

```text
overview_stale_threshold = 6 hours
stale_flag = true when primary source generated_at/updated_at older than threshold
freshness_label = STALE when stale_flag
freshness_label = PARTIAL when data_mode=PARTIAL
freshness_label = UNAVAILABLE when core sources unreadable
freshness_label = FRESH otherwise
```

All timestamps include timezone (prefer ISO-8601 with offset).

## 8. Evidence links

Each evidence link object:

| Field | Rule |
|-------|------|
| label | plain-language short name |
| technical_path | masked path string |
| kind | automation_state \| readiness_report \| cycle_report \| collection_state \| runbook \| other |
| available | boolean — false → show UNAVAILABLE, do not fabricate |

## 9. Prohibited ViewModel content

- profit, return, expectancy, accuracy-as-model-quality, risk-adjusted return, P&L
- “sistema pronto para operar capital”
- auto-start validate CTA or `next_safe_action` that starts validate
- scheduler_state = activated/live without authorization evidence
- invented open incidents
- invented failed executions
- green / SUCCESS implying edge or money

## 10. Mapping to UX-B4 microcopy (Visão Geral)

| ViewModel condition | Prefer B4 string |
|---------------------|------------------|
| screen title | Visão Geral |
| EMPTY | Ainda não há resumo operacional para mostrar. |
| LOADING (future UI) | Carregando o estado operacional… |
| PARTIAL | Parte dos painéis ainda não tem dados. Os disponíveis estão abaixo. |
| STALE | Este resumo pode estar desatualizado. Atualize ou confira a última execução. |
| UNAVAILABLE | O resumo operacional está temporariamente indisponível. |
| BLOCKED | Há bloqueios registrados. Bloqueado não significa necessariamente falha. |
| ERROR | Não foi possível montar a visão geral. Preserve evidências e tente atualizar. / or failure microcopy when last cycle FAILED |

## 11. Future implementation note

When `I6_SCREEN_IMPLEMENTATION_AUTHORIZED=true` and `UI_SCREEN_IMPLEMENTATION_AUTHORIZED=true`, implementers may materialize this contract as TypeScript types and mappers. Until then:

```text
NO_VIEWMODEL_IMPLEMENTATION = true
NO_SCREEN_IMPLEMENTATION = true
NO_TYPESCRIPT_FIXTURE_FILES = true
```
