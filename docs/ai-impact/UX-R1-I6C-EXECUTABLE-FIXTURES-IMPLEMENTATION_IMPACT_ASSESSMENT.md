# UX-R1-I6C-EXECUTABLE-FIXTURES-IMPLEMENTATION — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = I6A-OVERVIEW-SCREEN-DATA-AND-FIXTURE-PREPARATION-001
TASK_ID = EXECUTABLE-FIXTURES-IMPLEMENTATION-001
TITLE = Executable Fixtures Implementation
INCREMENT = I6C
PHASE = IMPLEMENTATION
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
I6_FIXTURE_IMPLEMENTATION_AUTHORIZED = true
I6_FIXTURE_MERGE_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE_CHANGE = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 0bb358f6df6d42759a051f8eb87ad58de52c8ddb
ANALYZED_AT = 2026-07-20T13:00:00Z
ANALYZED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTHORIZATION_DECISION = HUMAN_AUTHORIZED_FOR_THIS_TASK
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
FRONTEND_LOCATION = web/
I6_VIEWMODEL_IMPLEMENTATION_STATUS = MERGED
I6C_DECISION = AUTHORIZED_WITH_CONDITIONS
```

G1 note: `I6_FIXTURE_IMPLEMENTATION_AUTHORIZED=true` covers **typed synthetic fixture scenarios and a pure fixture catalog/runner that feeds I6B ViewModels only**. It does **not** authorize product screens, fixture UI selectors, real-data adapters, shell visuals, scheduler activation, or scientific validation.

## MANDATORY_CONSTRAINTS

```text
TYPED = true
DETERMINISTIC = true
SERIALIZABLE = true
IMMUTABLE = true
NO_NETWORK = true
NO_FILESYSTEM_RUNTIME_READS = true
NO_RANDOMNESS = true
NO_CURRENT_CLOCK_IMPLICITLY = true
CLEARLY_SYNTHETIC = true
NO_REACT_IMPORTS_IN_FIXTURES
NO_ROUTER_IMPORTS_IN_FIXTURES
NO_SCREEN_CONTENT_IMPLEMENTATION
NO_FIXTURE_UI_SELECTOR
NO_OPERATIONAL_DATA_INTEGRATION
NO_EXTRA_RUNTIME_OR_DEV_DEPENDENCIES
USES_I6B_INPUT_CONTRACTS = true
FIXED_ISO_TIMESTAMPS = true
NOT_READY_IS_NOT_FAULT
BLOCKED_IS_NOT_FAULT
DEFERRED_IS_NOT_FAULT
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
HOST_DISCOVERY = DEFERRED
SCHEDULER_ACTIVATION = BLOCKED
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## SUMMARY

Implement deterministic typed fixtures under `web/src/fixtures/` that produce I6B domain inputs and can build ViewModels via a pure catalog API. Include current-project illustrative scenario and fault/non-fault coverage. No screens or real data.

## 1. Objetivo

Entregar metadados sintéticos, cenários nomeados, famílias overview/runs/readiness/host-scheduler, catálogo `listFixtureScenarios` / `getFixtureScenario` / `buildFixtureViewModels`, e testes de fronteira.

## 2. Contexto técnico

- I6B ViewModel MERGED (PR #81); builders puros em `web/src/viewmodels/`.
- I6A docs definem cenários markdown; I6C materializa TypeScript executável claramente sintético.
- Fixtures consomem contratos de input I6B; não inventam payloads de API.

## 3. Componentes afetados

| Componente | Impacto |
|------------|---------|
| `web/src/fixtures/**` | Novo catálogo de fixtures |
| `web/tests/fixtures/**` | Testes |
| `docs/PROJECT.md` | Estado I6C / flags / NEXT |
| Governance I6C | Impact / spec / review / handoff |

## 4. Decisão arquitetural recomendada

```text
DECISION = APPROVED_FOR_IMPLEMENTATION
LOCATION = web/src/fixtures/
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
IMPLEMENTATION_STATUS = AUTHORIZED
```
