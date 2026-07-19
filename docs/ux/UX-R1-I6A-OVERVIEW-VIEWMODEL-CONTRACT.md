# UX-R1-I6A — Overview ViewModel Contract

```text
DOCUMENT = UX-R1-I6A-OVERVIEW-VIEWMODEL-CONTRACT
VERSION = 1.1.0
RELEASE = UX-R1
WORKSTREAM = I6A
TASK_ID = OVERVIEW-SCREEN-DATA-AND-FIXTURE-PREPARATION-001
SCREEN = Visão Geral
ROUTE_KEY = /overview (canonical; / redirects — I5A)
PHASE = DATA_CONTRACT_AND_FIXTURE_PREPARATION
BASE_SHA = 6ff45b9bd50349cc12061346c24a86fec0cf7645
DATA_CONTRACT_DECISION = AUTHORIZED_WITH_CONDITIONS
I6A_DOCUMENTATION_MERGE_RECOMMENDED = true
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_SCOPE = DOCUMENTATION_AND_DATA_CONTRACT_ONLY
RUNTIME_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
TYPESCRIPT_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
NO_VIEWMODEL_IMPLEMENTATION = true
NO_TYPESCRIPT_FIXTURE_FILES = true
NO_SCREEN_IMPLEMENTATION = true
NO_OPERATIONAL_INDEX = true
NO_ADAPTER = true
NO_REAL_DATA_INTEGRATION = true
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
SCIENTIFIC_INTERPRETATION_ALLOWED = false
I5A_STATUS = ARCHITECTURE_MERGED
I5_IMPLEMENTATION_AUTHORIZED = false
ROUTER_INSTALLATION_AUTHORIZED = false
WCAG = 2.2 AA
EFFECTIVE_AT = 2026-07-19T19:00:00Z
```

## 1. Purpose

Define the **read-only** ViewModel field contract for Visão Geral so a future UI can render operational state without inventing scientific or economic meaning.

This document is a data contract. It does **not** implement TypeScript types, hooks, adapters, or screens.

## 2. Normative sources

- `docs/ux/UX-R1-OPERATIONAL-MVP_DATA-CONTRACT-CATALOG.md` — Screen 1
- `docs/ai-specs/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS_SPEC.md` — §4
- `docs/ux/UX-R1-OPERATIONAL-MVP_STATE-MATRIX.md` — Visão Geral states
- `docs/ai-specs/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_SPEC.md` — shell/route contracts (MERGED)
- UX-B4 language catalogs (labels and microcopy)

## 3. I5A alignment (shell owns these; ViewModel does not)

Do **not** duplicate shell/navigation responsibilities inside the Overview ViewModel.

```text
OVERVIEW_ROUTE = /overview (canonical; / redirects to /overview)
PAGE_TITLE = Visão Geral
BREADCRUMBS = WICK / Visão Geral
LOADING_BOUNDARY = I5A §13 (shell loading region; Overview supplies content status only)
ERROR_BOUNDARY = I5A §14 (shell recoverable error + link Visão Geral)
NOT_FOUND_BEHAVIOR = I5A §15 (shell 404; Overview is not the router)
FOCUS_RESTORATION = I5A §20 (shell focus after navigation)
```

No route or router implementation is authorized by this contract.

## 4. Required field groups (normative)

Each group below is a contract field. Attributes are mandatory for future implementers.

Legend — NULLABILITY: `REQUIRED` | `NULLABLE`  
DISPLAY_PRIORITY: `P0` (always visible) | `P1` (primary panels) | `P2` (secondary / disclosure)

### 4.1 OVERALL_OPERATIONAL_STATE

```text
FIELD_NAME = OVERALL_OPERATIONAL_STATE
TYPE = enum (ERROR|BLOCKED|NOT_READY|DEGRADED|HEALTHY_COLLECTION|UNKNOWN|PARTIAL|EMPTY)
NULLABILITY = REQUIRED
SOURCE = DERIVED_READ_ONLY (B3 Spec §4 composition)
FRESHNESS_RULE = recomputed whenever any primary source changes; inherits worst freshness of inputs
PLAIN_LANGUAGE_LABEL = Estado operacional
TECHNICAL_LABEL = overall_operational_state
DISPLAY_PRIORITY = P0
SAFE_FALLBACK = UNKNOWN
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

Companion: `overall_visual_semantic` (NEUTRAL/INFO/ATTENTION/SUCCESS_OPS/ERROR/BLOCKED/DEFERRED).

### 4.2 LAST_COMPLETED_EXECUTION

```text
FIELD_NAME = LAST_COMPLETED_EXECUTION
TYPE = object { id?: string, status?: enum, finished_at?: datetime TZ, evidence_link?: link } | null
NULLABILITY = NULLABLE (null = no completed execution)
SOURCE = RUN_ARTIFACT / automation_state
FRESHNESS_RULE = uses finished_at / artifact updated_at; missing timestamp → DATA_ABSENT for this block
PLAIN_LANGUAGE_LABEL = Última execução concluída
TECHNICAL_LABEL = last_completed_execution
DISPLAY_PRIORITY = P1
SAFE_FALLBACK = null with label “Nenhuma”
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

### 4.3 LAST_FAILED_EXECUTION

```text
FIELD_NAME = LAST_FAILED_EXECUTION
TYPE = object { id?: string, status?: enum, finished_at?: datetime TZ, evidence_link?: link } | null
NULLABILITY = NULLABLE
SOURCE = DERIVED from run artifacts
FRESHNESS_RULE = same as LAST_COMPLETED_EXECUTION; never invent failures
PLAIN_LANGUAGE_LABEL = Última execução falha
TECHNICAL_LABEL = last_failed_execution
DISPLAY_PRIORITY = P1
SAFE_FALLBACK = null with label “Nenhuma falha registrada”
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

### 4.4 STORE_SUMMARY

```text
FIELD_NAME = STORE_SUMMARY
TYPE = object { future_unseen_cutoff?: datetime TZ, store_observation_count?: int }
NULLABILITY = NULLABLE fields inside REQUIRED group
SOURCE = STORE_METADATA / READINESS
FRESHNESS_RULE = source_updated_at of store metadata; count=0 is valid (not ERROR)
PLAIN_LANGUAGE_LABEL = Resumo do store
TECHNICAL_LABEL = store_summary
DISPLAY_PRIORITY = P1
SAFE_FALLBACK = fields NOT_AVAILABLE / UNKNOWN; never fabricate counts
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

### 4.5 READINESS_SUMMARY

```text
FIELD_NAME = READINESS_SUMMARY
TYPE = object { status?, primary_reason?, window_days?, required_window_days?, window_progress_ratio? }
NULLABILITY = NULLABLE when readiness report missing → UNAVAILABLE (not NOT_READY invented)
SOURCE = READINESS_REPORT
FRESHNESS_RULE = readiness report generated_at / source_updated_at
PLAIN_LANGUAGE_LABEL = Prontidão
TECHNICAL_LABEL = readiness_summary
DISPLAY_PRIORITY = P0
SAFE_FALLBACK = UNAVAILABLE
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

READY ≠ VALIDATION_AUTHORIZED. Progress ≠ authorize validate.

### 4.6 HOST_STATE

```text
FIELD_NAME = HOST_STATE
TYPE = enum (DEFERRED|UNKNOWN|NOT_AVAILABLE|… documented B3 values)
NULLABILITY = REQUIRED
SOURCE = DOC / discovery result
FRESHNESS_RULE = discovery result observed_at when present; default DEFERRED without inventing failure
PLAIN_LANGUAGE_LABEL = Host
TECHNICAL_LABEL = host_state
DISPLAY_PRIORITY = P1
SAFE_FALLBACK = DEFERRED
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

### 4.7 SCHEDULER_STATE

```text
FIELD_NAME = SCHEDULER_STATE
TYPE = enum (BLOCKED|NOT_AUTHORIZED|…); activation never implied without evidence
NULLABILITY = REQUIRED
SOURCE = DOC / META
FRESHNESS_RULE = config/meta source_updated_at; default BLOCKED
PLAIN_LANGUAGE_LABEL = Automação
TECHNICAL_LABEL = scheduler_state
DISPLAY_PRIORITY = P1
SAFE_FALLBACK = BLOCKED
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

### 4.8 OPEN_INCIDENTS

```text
FIELD_NAME = OPEN_INCIDENTS
TYPE = int | UNAVAILABLE
NULLABILITY = REQUIRED (value may be UNAVAILABLE)
SOURCE = DERIVED (UX-B7 future)
FRESHNESS_RULE = N/A until UX-B7; do not invent incidents
PLAIN_LANGUAGE_LABEL = Incidentes abertos
TECHNICAL_LABEL = open_incidents_count
DISPLAY_PRIORITY = P2
SAFE_FALLBACK = UNAVAILABLE / EMPTY
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

### 4.9 OPERATIONAL_DEBT

```text
FIELD_NAME = OPERATIONAL_DEBT
TYPE = enum (OPEN|…)
NULLABILITY = REQUIRED
SOURCE = DERIVED from deferred/blocked ops
FRESHNESS_RULE = derived continuously from HOST/SCHEDULER/discovery debt
PLAIN_LANGUAGE_LABEL = Dívida operacional
TECHNICAL_LABEL = operational_debt_status
DISPLAY_PRIORITY = P1
SAFE_FALLBACK = OPEN while discovery deferred or scheduler blocked
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

### 4.10 SCIENTIFIC_GATE

```text
FIELD_NAME = SCIENTIFIC_GATE
TYPE = object { r3e_gate, validate_authorized, economic_interpretation_allowed }
NULLABILITY = REQUIRED
SOURCE = STORE / READINESS / SAFETY
FRESHNESS_RULE = gate docs + readiness; pending ≠ rejected edge
PLAIN_LANGUAGE_LABEL = Gate científico
TECHNICAL_LABEL = scientific_gate
DISPLAY_PRIORITY = P0
SAFE_FALLBACK = PENDING_FUTURE_UNSEEN_DATA; validate_authorized=false; economic=false
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

### 4.11 NEXT_SAFE_ACTION

```text
FIELD_NAME = NEXT_SAFE_ACTION
TYPE = object { plain_language: string, code?: enum }
NULLABILITY = REQUIRED
SOURCE = DERIVED Spec §4
FRESHNESS_RULE = recomputed with overall state; never suggests validate
PLAIN_LANGUAGE_LABEL = Próxima ação segura
TECHNICAL_LABEL = next_safe_action
DISPLAY_PRIORITY = P0
SAFE_FALLBACK = MONITOR_COLLECTION / PARTIAL_DATA_UNAVAILABLE when unknown
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

### 4.12 FRESHNESS

```text
FIELD_NAME = FRESHNESS
TYPE = object { generated_at, source_updated_at?, observed_at?, stale_flag, staleness_threshold, freshness_label, data_availability }
NULLABILITY = REQUIRED
SOURCE = DERIVED from source timestamps
FRESHNESS_RULE = see §6
PLAIN_LANGUAGE_LABEL = Atualidade
TECHNICAL_LABEL = freshness
DISPLAY_PRIORITY = P0
SAFE_FALLBACK = DATA_ABSENT / UNKNOWN when timestamps missing
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

### 4.13 EVIDENCE_LINKS

```text
FIELD_NAME = EVIDENCE_LINKS
TYPE = list of { label, technical_path?, evidence_uri?, kind, available, accessible_name }
NULLABILITY = REQUIRED (list may be empty)
SOURCE = DERIVED artifacts / synthetic demo paths only
FRESHNESS_RULE = each link carries source_updated_at when known; unavailable → do not fabricate
PLAIN_LANGUAGE_LABEL = Evidências
TECHNICAL_LABEL = evidence_links
DISPLAY_PRIORITY = P1
SAFE_FALLBACK = [] with UNAVAILABLE messaging
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

### 4.14 DATA_AVAILABILITY

```text
FIELD_NAME = DATA_AVAILABILITY
TYPE = enum (DATA_ABSENT|DATA_STALE|DATA_PARTIAL|DATA_CURRENT)
NULLABILITY = REQUIRED
SOURCE = DERIVED from FRESHNESS + present blocks
FRESHNESS_RULE = canonical availability classification for the Overview composition
PLAIN_LANGUAGE_LABEL = Disponibilidade dos dados
TECHNICAL_LABEL = data_availability
DISPLAY_PRIORITY = P0
SAFE_FALLBACK = DATA_ABSENT
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

No fixture may disguise DATA_STALE or DATA_ABSENT as DATA_CURRENT.

### 4.15 PARTIAL_DATA_BEHAVIOR

```text
FIELD_NAME = PARTIAL_DATA_BEHAVIOR
TYPE = policy enum / ruleset
NULLABILITY = REQUIRED (policy always defined)
SOURCE = CONTRACT
FRESHNESS_RULE = N/A (behavioral)
PLAIN_LANGUAGE_LABEL = Comportamento com dados parciais
TECHNICAL_LABEL = partial_data_behavior
DISPLAY_PRIORITY = P1
SAFE_FALLBACK = show available panels; mark missing as NOT_AVAILABLE; never fill invented values
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

Rules: PARTIAL_METADATA ≠ FABRICATED_DATA; omit missing blocks; set DATA_AVAILABILITY=DATA_PARTIAL.

### 4.16 UNKNOWN_STATE_BEHAVIOR

```text
FIELD_NAME = UNKNOWN_STATE_BEHAVIOR
TYPE = policy enum / ruleset
NULLABILITY = REQUIRED
SOURCE = CONTRACT
FRESHNESS_RULE = N/A (behavioral)
PLAIN_LANGUAGE_LABEL = Comportamento com estado desconhecido
TECHNICAL_LABEL = unknown_state_behavior
DISPLAY_PRIORITY = P1
SAFE_FALLBACK = UNKNOWN / NOT_AVAILABLE / DEFERRED / NOT_AUTHORIZED as appropriate
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

Rules: UNKNOWN ≠ HEALTHY; UNKNOWN ≠ FAILED; never infer from missing evidence.

### 4.17 SOURCE_PROVENANCE

```text
FIELD_NAME = SOURCE_PROVENANCE
TYPE = object { source_type, source_identifier, source_version?, evidence_uri?, provenance_footer[] }
NULLABILITY = REQUIRED
SOURCE = DERIVED
FRESHNESS_RULE = provenance updated with composition generated_at
PLAIN_LANGUAGE_LABEL = Proveniência
TECHNICAL_LABEL = source_provenance
DISPLAY_PRIORITY = P2
SAFE_FALLBACK = source_type=UNKNOWN; footer lists missing sources explicitly
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

For fixtures: `source_type=SYNTHETIC`, `DADOS_DEMONSTRATIVOS=true`.

## 5. Semantic safety (non-negotiable)

```text
NOT_READY != ERROR
BLOCKED != FAILED
READY != VALIDATION_AUTHORIZED
COLLECTION_COMPLETE != SCIENTIFIC_VALIDATION
SCIENTIFIC_VALIDATION != ECONOMIC_RETURN
SUCCESS != PROFIT
NO_HISTORY != SYSTEM_FAILURE
PARTIAL_METADATA != FABRICATED_DATA
UNKNOWN != HEALTHY
UNKNOWN != FAILED
```

When evidence is missing, use `UNKNOWN` | `NOT_AVAILABLE` | `DEFERRED` | `NOT_AUTHORIZED` — never invent.

## 6. Freshness and provenance rules

```text
generated_at = composition time (UTC with offset)
source_updated_at = newest contributing source update time when known
observed_at = observation time of host/discovery evidence when known
staleness_threshold = 6 hours (overview_stale_threshold)
stale_data_label = “Este resumo pode estar desatualizado…” (B4)
missing_timestamp_behavior = treat block as DATA_ABSENT / UNAVAILABLE; never assume current
evidence_uri = masked URI/path when available; synthetic demo paths for fixtures
source_type = LIVE_ARTIFACT | DOC | SYNTHETIC | UNKNOWN
source_identifier = stable id/path head
source_version = artifact version when known else NOT_AVAILABLE
```

Availability mapping:

```text
DATA_ABSENT = core sources unreadable / no timestamps / empty history without fabrication
DATA_STALE = stale_flag true (sources older than staleness_threshold)
DATA_PARTIAL = subset of blocks missing (data_mode PARTIAL)
DATA_CURRENT = sources present, not stale, not partial
```

`freshness_label` may show FRESH|STALE|PARTIAL|UNAVAILABLE for UI copy; `data_availability` is the canonical enum above.

## 7. Accessibility requirements (contract-level; WCAG 2.2 AA)

Future UI (when authorized) MUST satisfy:

```text
semantic heading hierarchy (h1 Visão Geral → section headings)
status text independent from color (plain language + technical code)
screen-reader status announcement (live region for overall state changes)
loading announcement (shell loading + Overview content pending)
error announcement (ERROR / recoverable failure)
stale-data announcement (when DATA_STALE / stale_flag)
evidence-link accessible names (accessible_name required; not path-only)
keyboard-safe next-action links (focusable, named, no validate CTA)
plain-language first; technical detail second
demonstration badge accessible name when DADOS_DEMONSTRATIVOS
```

I6A documents expectations; it does not implement UI.

## 8. overall_operational_state values

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

Composition priority (highest first): ERROR → BLOCKED → NOT_READY/ATTENTION → DEGRADED → HEALTHY_COLLECTION → UNKNOWN.

`HEALTHY_COLLECTION` may coexist with readiness `NOT_READY` — never collapse NOT_READY into ERROR.

## 9. next_safe_action_code values

| Code | Plain-language action |
|------|----------------------|
| RUN_HOST_DISCOVERY | Executar discovery no host persistente (runbook) |
| KEEP_SCHEDULER_INACTIVE | Manter scheduler inativo; completar checklist |
| CONTINUE_COLLECTION | Continuar coleta; aguardar critérios |
| INVESTIGATE_FAILED_EXECUTION | Investigar execução falha (abrir Execuções) |
| DO_NOT_VALIDATE | Não executar validate; aguardar autorização humana |
| MONITOR_COLLECTION | Nenhuma ação urgente; monitorar próxima coleta |
| PARTIAL_DATA_UNAVAILABLE | Indisponível — dados parciais |

## 10. Flattened field catalog (implementation mapping)

The groups in §4 map to these technical leaf fields (B3-compatible):

| TECHNICAL_LABEL | Group | NULLABILITY |
|-----------------|-------|-------------|
| overall_operational_state | OVERALL_OPERATIONAL_STATE | REQUIRED |
| overall_visual_semantic | OVERALL_OPERATIONAL_STATE | REQUIRED |
| collection_status | OVERALL_OPERATIONAL_STATE | REQUIRED |
| last_completed_execution_* | LAST_COMPLETED_EXECUTION | NULLABLE |
| last_failed_execution_* | LAST_FAILED_EXECUTION | NULLABLE |
| future_unseen_cutoff / store_observation_count | STORE_SUMMARY | NULLABLE |
| readiness_* / window_* | READINESS_SUMMARY | NULLABLE |
| host_state | HOST_STATE | REQUIRED |
| scheduler_state | SCHEDULER_STATE | REQUIRED |
| open_incidents_count | OPEN_INCIDENTS | REQUIRED (may be UNAVAILABLE) |
| operational_debt_status | OPERATIONAL_DEBT | REQUIRED |
| scientific_gate_* / validate_authorized | SCIENTIFIC_GATE | REQUIRED |
| next_safe_action / next_safe_action_code | NEXT_SAFE_ACTION | REQUIRED |
| generated_at / source_updated_at / observed_at / stale_flag / freshness_label / data_availability | FRESHNESS / DATA_AVAILABILITY | REQUIRED |
| evidence_links[] | EVIDENCE_LINKS | REQUIRED |
| source_type / source_identifier / source_version / provenance_footer / fixture_label | SOURCE_PROVENANCE | REQUIRED |

## 11. Prohibited ViewModel content

- profit, return, expectancy, accuracy-as-model-quality, risk-adjusted return, P&L
- “sistema pronto para operar capital”
- auto-start validate CTA or `next_safe_action` that starts validate
- scheduler_state = activated/live without authorization evidence
- invented open incidents or failed executions
- green / SUCCESS implying edge or money
- disguising DATA_STALE / DATA_ABSENT as DATA_CURRENT

## 12. Mapping to UX-B4 microcopy (Visão Geral)

| ViewModel condition | Prefer B4 string |
|---------------------|------------------|
| screen title | Visão Geral |
| EMPTY | Ainda não há resumo operacional para mostrar. |
| LOADING (future UI) | Carregando o estado operacional… |
| PARTIAL | Parte dos painéis ainda não tem dados. Os disponíveis estão abaixo. |
| STALE | Este resumo pode estar desatualizado. Atualize ou confira a última execução. |
| UNAVAILABLE | O resumo operacional está temporariamente indisponível. |
| BLOCKED | Há bloqueios registrados. Bloqueado não significa necessariamente falha. |
| ERROR | Não foi possível montar a visão geral. Preserve evidências e tente atualizar. |

## 13. Future implementation note

```text
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_SCOPE = DOCUMENTATION_AND_DATA_CONTRACT_ONLY
RUNTIME_IMPLEMENTATION_AUTHORIZED = false
VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
TYPESCRIPT_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
```

Materialize TypeScript types/mappers/fixtures only after explicit human authorization in a separate task.
