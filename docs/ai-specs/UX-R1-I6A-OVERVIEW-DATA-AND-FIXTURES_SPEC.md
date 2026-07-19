# UX-R1-I6A — Overview Data and Fixtures Spec

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
WORKSTREAM = I6A
TASK_ID = OVERVIEW-SCREEN-DATA-AND-FIXTURE-PREPARATION-001
DOCUMENT = UX-R1-I6A-OVERVIEW-DATA-AND-FIXTURES_SPEC
DOCUMENT_VERSION = 1.0.0
PHASE = DATA_CONTRACT_AND_FIXTURE_PREPARATION
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-I6A-OVERVIEW-DATA-AND-FIXTURES_IMPACT_ASSESSMENT.md
IMPLEMENTATION_STATUS = DATA_PREPARATION_COMPLETE
IMPLEMENTATION_AUTHORIZED = true
UI_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
NO_TYPESCRIPT_FIXTURE_FILES = true
NO_VIEWMODEL_IMPLEMENTATION = true
NO_SCREEN_IMPLEMENTATION = true
NO_OPERATIONAL_INDEX = true
NO_ADAPTER = true
NO_REAL_DATA_INTEGRATION = true
R3E_SCIENTIFIC_STATE_CHANGE = false
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTOMATIC_MERGE_AUTHORIZED = false
BASE_BRANCH = main
BASE_SHA = 221aacc7141697403e9bbbc9f8690953b683e3a9
EFFECTIVE_AT = 2026-07-19T16:54:39Z
```

## 1. Purpose

Specify the read-only Overview (Visão Geral) ViewModel contract and the eight demonstration fixture scenarios required for a future screen prototype, without shipping TypeScript fixtures, ViewModel code, adapters, or live data integration.

```text
IMPLEMENTATION_AUTHORIZED=true authorizes only this documentation package.
I6 screen / UI screen implementation remains prohibited.
```

## 2. Normative references

| Document | Role |
|----------|------|
| `docs/ai-specs/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS_SPEC.md` §4 | Screen purpose, blocks, overall state priority, next safe action |
| `docs/ux/UX-R1-OPERATIONAL-MVP_DATA-CONTRACT-CATALOG.md` Screen 1 | Field provenance and NULL/EMPTY/ERROR behavior |
| `docs/ux/UX-R1-OPERATIONAL-MVP_STATE-MATRIX.md` | Overview state applications |
| `docs/ux/UX-R1-OPERATIONAL-MVP_SAFE-FIXTURE-CATALOG.md` | Base eight scenarios (extended by I6A) |
| `docs/ux/UX-R1-OPERATIONAL-LANGUAGE-GUIDE.md` | Visão Geral microcopy |
| `docs/ux/UX-R1-STATUS-MESSAGE-CATALOG.md` | Status semantics |
| `docs/ux/UX-R1-EMPTY-STATE-CATALOG.md` | Empty/partial/unavailable copy |
| `docs/ux/UX-R1-FAILURE-AND-WARNING-MICROCOPY.md` | Failure/warning language |
| `docs/ux/UX-R1-SCIENTIFIC-AND-ECONOMIC-LANGUAGE-GUARDRAILS.md` | Scientific/economic bans |
| `docs/ux/UX-R1-I6A-OVERVIEW-VIEWMODEL-CONTRACT.md` | Normative ViewModel fields (this workstream) |
| `docs/ux/UX-R1-I6A-OVERVIEW-FIXTURE-SCENARIOS.md` | Normative fixture field matrices (this workstream) |

Where I6A and B3 differ on Overview ViewModel detail, I6A refines presentation/fixture values; B3 remains authoritative for source provenance and scientific safety rules.

## 3. Deliverables

```text
docs/ux/UX-R1-I6A-OVERVIEW-VIEWMODEL-CONTRACT.md
docs/ux/UX-R1-I6A-OVERVIEW-FIXTURE-SCENARIOS.md
docs/ux/UX-R1-OPERATIONAL-MVP_SAFE-FIXTURE-CATALOG.md (Overview ViewModel extension)
docs/ai-impact/UX-R1-I6A-OVERVIEW-DATA-AND-FIXTURES_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-I6A-OVERVIEW-DATA-AND-FIXTURES_SPEC.md
docs/ai-reviews/UX-R1-I6A-OVERVIEW-DATA-AND-FIXTURES_REVIEW.md
reports/ai-implementation/UX-R1-I6A-OVERVIEW-DATA-AND-FIXTURES_HANDOFF.md
docs/PROJECT.md (I6A_STATUS only)
```

## 4. Overview ViewModel (summary)

The Overview ViewModel is a **read-only** composition surface answering:

```text
O sistema está coletando?
A coleta está saudável?
Os dados estão prontos?
Existe algum bloqueio?
Qual é a próxima ação segura?
```

Required field groups (normative detail in ViewModel contract):

| Group | Fields (technical) |
|-------|--------------------|
| Overall state | `overall_operational_state`, `collection_status`, visual semantic |
| Last completed execution | `last_completed_execution_id`, `last_completed_execution_status`, timestamps, evidence link |
| Last failed execution | `last_failed_execution_id`, `last_failed_execution_status`, evidence link (nullable) |
| Store summary | `future_unseen_cutoff`, `store_observation_count` |
| Readiness summary | `readiness_status_summary`, `readiness_primary_reason`, `window_progress` |
| Host state | `host_state` (default DEFERRED) |
| Scheduler state | `scheduler_state` (default BLOCKED / not activated) |
| Open incidents | `open_incidents_count` (EMPTY/UNAVAILABLE until UX-B7) |
| Operational debt | `operational_debt_status` (OPEN while deferred/blocked) |
| Scientific gate | `scientific_gate_state`, `validate_authorized`, `economic_interpretation_allowed` |
| Next safe action | `next_safe_action` (derived; never validate) |
| Freshness | `generated_at`, `stale_flag`, `data_mode`, `freshness_label` |
| Evidence / provenance | `evidence_links[]`, `provenance_footer`, `fixture_label` when demo |

### Overall state priority (inherited, non-negotiable)

1. ERROR — last cycle FAILED or critical integrity blocker
2. BLOCKED — hard blockers or forbidden activation context
3. ATTENTION / NOT_READY — readiness NOT_READY
4. DEGRADED — collection warnings without hard fail
5. HEALTHY_COLLECTION — recent COMPLETE/PARTIAL/NO_NEW_DATA without hard errors (still show NOT_READY separately when applicable)
6. UNKNOWN — core artifacts missing

Never map NOT_READY → ERROR.

### Next safe action (inherited)

| Condition | Plain-language action |
|-----------|----------------------|
| HOST_DISCOVERY missing / deferred | Executar discovery no host persistente (runbook) |
| Scheduler prepared but not authorized | Manter scheduler inativo; completar checklist |
| readiness NOT_READY (window/series) | Continuar coleta; aguardar critérios |
| last cycle FAILED | Investigar execução falha (abrir Execuções) |
| readiness READY and VALIDATE_AUTHORIZED=false | Não executar validate; aguardar autorização humana |
| All quiet + collecting | Nenhuma ação urgente; monitorar próxima coleta |
| Partial metadata | Indisponível — dados parciais |

## 5. Fixture scenarios (summary)

Exactly these eight scenarios (markdown specs only):

```text
healthy_collection_not_ready
collection_warning
collection_failure
host_discovery_deferred
scheduler_not_activated
readiness_ready_but_validation_not_authorized
no_execution_history
partial_metadata
```

Every fixture MUST declare:

```text
DADOS_DEMONSTRATIVOS
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

Cross-fixture constants:

```text
SCHEDULER_ACTIVATION = BLOCKED
HOST_DISCOVERY = DEFERRED (unless scenario explicitly focuses host deferred; still not “activated”)
OPERATIONAL_DEBT = OPEN
VALIDATE_AUTHORIZED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
```

Prohibited in fixtures:

- profit / return / expectancy / accuracy-as-quality / risk-adjusted return
- fabricated validate success
- `ECONOMIC_INTERPRETATION_ALLOWED=true`
- scheduler presented as live-active
- inventing repository evidence IDs without SYNTHETIC labeling

## 6. Explicit non-goals

```text
NO_TYPESCRIPT_FIXTURE_FILES
NO_VIEWMODEL_IMPLEMENTATION
NO_SCREEN_IMPLEMENTATION
NO_OPERATIONAL_INDEX
NO_ADAPTER
NO_REAL_DATA_INTEGRATION
HOST_DISCOVERY remains DEFERRED
SCHEDULER_ACTIVATION remains BLOCKED
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## 7. Language and accessibility (contract-level)

- Consume UX-B4 wording for Visão Geral screen strings.
- Status never by color alone; pair plain language + technical code.
- WCAG 2.2 AA remains the target for future UI (UX-B10); I6A does not implement UI.
- Demonstration badge must be visible when `data_mode=DEMONSTRATION_FIXTURE`.

## 8. Security

- Mask paths/hostnames in evidence links for future UI.
- No secrets in fixture specs.
- `INTERNAL_OPERATIONAL` fields (run IDs) may be shown; copy allowed; do not invent.

## 9. Testing expectations for this package

| Check | Required |
|-------|----------|
| Governance validator on impact/spec/review/handoff | yes |
| pytest + ruff (no regression) | yes |
| web smoke (unchanged code) | yes |
| Materialized fixture unit tests | no (out of scope) |
| Screen snapshot tests | no (out of scope) |

## 10. Authorization and merge

```text
DOCS_MERGE = AWAITING_HUMAN_AUTHORIZATION
AUTOMATIC_MERGE_AUTHORIZED = false
This package does not authorize automatic merge.
UI / I6 screen implementation remains unauthorized after docs merge.
```

## 11. Exit criteria

I6A data-preparation exit (docs) is met when:

1. ViewModel contract covers all required Overview groups listed in §4.
2. All eight fixture scenarios have complete ViewModel field matrices.
3. B3 safe fixture catalog carries Overview ViewModel extension notes.
4. Impact / review / handoff APPROVED for docs merge.
5. `I6A_STATUS=DATA_PREPARATION_IN_PROGRESS` recorded in PROJECT.md.
6. No `.ts`/`.tsx`/executable fixture files added.
7. All implementation authorization flags for UI/screen/integration remain false.
