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
VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
TYPESCRIPT_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
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
DATA_CONTRACT_DECISION = AUTHORIZED_WITH_CONDITIONS
AUTHORIZATION_CONDITIONS = C1-C8
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTOMATIC_MERGE_AUTHORIZED = false
BASE_BRANCH = main
BASE_SHA = 6ff45b9bd50349cc12061346c24a86fec0cf7645
I5A_STATUS = ARCHITECTURE_MERGED
I5_IMPLEMENTATION_AUTHORIZED = false
ROUTER_INSTALLATION_AUTHORIZED = false
WCAG = 2.2 AA
EFFECTIVE_AT = 2026-07-19T18:25:00Z
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
| `docs/ai-specs/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_SPEC.md` | Shell/route/title/breadcrumb/boundary contracts (MERGED) |

Where I6A and B3 differ on Overview ViewModel detail, I6A refines presentation/fixture values; B3 remains authoritative for source provenance and scientific safety rules. Shell responsibilities remain owned by I5A.

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

| Group | Coverage |
|-------|----------|
| OVERALL_OPERATIONAL_STATE | overall state + visual semantic + collection_status |
| LAST_COMPLETED_EXECUTION | id/status/finished_at/evidence |
| LAST_FAILED_EXECUTION | nullable failed run block |
| STORE_SUMMARY | cutoff + observation count |
| READINESS_SUMMARY | status/reason/window progress |
| HOST_STATE | default DEFERRED |
| SCHEDULER_STATE | default BLOCKED / not activated |
| OPEN_INCIDENTS | UNAVAILABLE until UX-B7 |
| OPERATIONAL_DEBT | OPEN while deferred/blocked |
| SCIENTIFIC_GATE | R3E gate + validate_authorized + economic flag |
| NEXT_SAFE_ACTION | never validate |
| FRESHNESS | generated_at, source_updated_at, observed_at, staleness |
| EVIDENCE_LINKS | labeled/masked links |
| DATA_AVAILABILITY | DATA_ABSENT\|STALE\|PARTIAL\|CURRENT |
| PARTIAL_DATA_BEHAVIOR | no fabrication |
| UNKNOWN_STATE_BEHAVIOR | UNKNOWN ≠ HEALTHY/FAILED |
| SOURCE_PROVENANCE | source_type/id/version/footer |

### I5A alignment (shell owns; ViewModel does not duplicate)

```text
OVERVIEW_ROUTE = /overview (/ redirects)
PAGE_TITLE = Visão Geral
BREADCRUMBS = WICK / Visão Geral
LOADING_BOUNDARY = I5A §13
ERROR_BOUNDARY = I5A §14
NOT_FOUND_BEHAVIOR = I5A §15
FOCUS_RESTORATION = I5A §20
```

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
FIXTURE_ID
DADOS_DEMONSTRATIVOS = true
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
PURPOSE
EXPECTED_OPERATIONAL_STATE
EXPECTED_PRIMARY_MESSAGE
EXPECTED_TECHNICAL_DETAIL
EXPECTED_NEXT_SAFE_ACTION
EXPECTED_STATUS_SEMANTICS
MISSING_FIELDS
ACCESSIBILITY_EXPECTATIONS
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
VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
TYPESCRIPT_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
NO_SCREEN_IMPLEMENTATION
NO_OPERATIONAL_INDEX
NO_ADAPTER
NO_REAL_DATA_INTEGRATION
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
HOST_DISCOVERY remains DEFERRED
SCHEDULER_ACTIVATION remains BLOCKED
R3E_SCIENTIFIC_STATE_CHANGE = false
ROUTER_INSTALLATION_AUTHORIZED = false
```

## 7. Language and accessibility (contract-level)

```text
WCAG = 2.2 AA
```

- Consume UX-B4 wording for Visão Geral screen strings.
- Status never by color alone; pair plain language + technical code.
- Semantic heading hierarchy (h1 Visão Geral → section headings).
- Screen-reader announcements for status, loading, error, and stale data.
- Evidence-link accessible names; keyboard-safe next-action links.
- Plain language first; technical detail second.
- Demonstration badge must be visible and named when `data_mode=DEMONSTRATION_FIXTURE`.
- I6A documents expectations; UI implementation remains unauthorized (UX-B10 / future I6).

## 7.1 Freshness and provenance (summary)

```text
generated_at / source_updated_at / observed_at
staleness_threshold = 6h
stale_data_label (B4)
missing_timestamp_behavior = DATA_ABSENT / UNAVAILABLE
evidence_uri / source_type / source_identifier / source_version
DATA_ABSENT | DATA_STALE | DATA_PARTIAL | DATA_CURRENT
```

No fixture may disguise stale or absent data as current.

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
DATA_CONTRACT_DECISION = AUTHORIZED_WITH_CONDITIONS
AUTHORIZATION_CONDITIONS = C1-C8
DOCS_MERGE = AWAITING_HUMAN_AUTHORIZATION
AUTOMATIC_MERGE_AUTHORIZED = false
This package does not authorize automatic merge.
UI / I6 screen / ViewModel / TS fixture / live data remain unauthorized after docs merge.
```

## 11. Exit criteria

I6A data-preparation exit (docs) is met when:

1. ViewModel contract covers all 17 required Overview groups with attribute matrix.
2. All eight fixture scenarios have complete EXPECTED_* / MISSING_FIELDS / ACCESSIBILITY_EXPECTATIONS.
3. Freshness/provenance and I5A alignment sections are present.
4. B3 safe fixture catalog carries Overview ViewModel extension notes.
5. Impact / review / handoff APPROVED with `DATA_CONTRACT_DECISION=AUTHORIZED_WITH_CONDITIONS`.
6. `I6A_STATUS=DATA_PREPARATION_IN_PROGRESS` recorded in PROJECT.md (unchanged from main until merge).
7. No `.ts`/`.tsx`/executable fixture files added.
8. All implementation authorization flags for UI/screen/ViewModel/fixtures/integration remain false.
