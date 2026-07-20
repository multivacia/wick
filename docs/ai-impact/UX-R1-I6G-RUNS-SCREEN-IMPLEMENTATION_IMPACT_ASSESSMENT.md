# UX-R1-I6G-RUNS-SCREEN-IMPLEMENTATION — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = RUNS-SCREEN-IMPLEMENTATION-AUTHORIZATION-ASSESSMENT-001
TASK_ID = RUNS-SCREEN-IMPLEMENTATION-001
TITLE = Runs Screen Implementation
INCREMENT = I6G
PHASE = IMPLEMENTATION
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = true
RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED = true
RUNS_SCREEN_MERGE_AUTHORIZED = false
READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED = false
HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
REAL_DATA_INTEGRATION_AUTHORIZED = false
OPERATIONAL_ACTIONS_AUTHORIZED = false
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
BASE_SHA = 26dfee723dbca8eb7625b711aa505ca2b10a5e11
FINAL_CANDIDATE_HEAD = 92fb14adf5674167b3922a23ad12018b57859fd6
CONTENT_REVIEWED_THROUGH_HEAD = 92fb14adf5674167b3922a23ad12018b57859fd6
POST_REVIEW_NORMATIVE_CHANGES = 0
ANALYZED_AT = 2026-07-20T17:56:00Z
ANALYZED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTHORIZATION_DECISION = HUMAN_AUTHORIZED_FOR_THIS_TASK
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
FRONTEND_LOCATION = web/
I6F_DECISION = AUTHORIZED_WITH_CONDITIONS
I6F_RECOMMENDED_IMPLEMENTATION_BOUNDARY = RUNS_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; NO_VISIBLE_FIXTURE_SELECTOR; NO_REAL_DATA; NO_OPERATIONAL_ACTIONS
FIXTURE_ID = current_project_state_illustrative
ROUTE = /future-collection/runs
SCREEN = Execuções
```

G1 note: authorization covers **only** the read-only fixture-backed Execuções (`/future-collection/runs`) screen. It does **not** authorize Readiness/Host-Scheduler screens, fixture UI selectors, real-data adapters, operational buttons, scheduler activation, or scientific validation. Overview remains preserved.

## MANDATORY_CONSTRAINTS

```text
READ_ONLY = true
FIXTURE_BACKED = true
FIXTURE_ID = current_project_state_illustrative
NO_VISIBLE_FIXTURE_SELECTOR = true
NO_REAL_DATA = true
NO_OPERATIONAL_ACTIONS = true
NO_NETWORK_CLIENTS = true
NO_BACKEND_API = true
NO_EXTRA_RUNTIME_OR_DEV_DEPENDENCIES = true
TOKEN_ONLY_STYLING = true
REUSE_I3_PRIMITIVES = true
CONSUME_I6B_VIEWMODELS = true
CONSUME_I6C_FIXTURES = true
REPLACE_RUNS_PLACEHOLDER_ONLY = true
PRESERVE_OVERVIEW_SCREEN = true
PRESERVE_OTHER_ROUTE_PLACEHOLDERS = true
IN_PROGRESS_IS_NOT_FAULT = true
UNKNOWN_IS_NOT_FAULT = true
EMPTY_IS_NOT_FAULT = true
RED_ONLY_FOR_CONFIRMED_FAULT = true
NO_FAKE_ZEROES = true
NO_FABRICATED_LINKS_OR_METRICS = true
NO_B3_FILTERS_PAGINATION_DETAIL_PARITY = true
NO_FABRICATED_B3_EXTRA_FIELDS = true
WCAG_2_2_AA = true
PARALLEL_TASKS_ALLOWED = false
HOST_DISCOVERY = DEFERRED
SCHEDULER_ACTIVATION = BLOCKED
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## SUMMARY

Implement the Wick product screen Execuções at `/future-collection/runs`, consuming merged Runs ViewModel + synthetic fixture catalog + shell/router + tokens + accessible primitives. Read-only. Clearly labeled synthetic. No Readiness/Host screens.

## 1. Objetivo

Entregar a tela Execuções com PageHeader, SyntheticDataNotice, RunsSummary, RunsCollection (status/timing/counts/store/idempotency/failure/evidence), EmptyState e PartialUnknownState; testes de rota, a11y e fronteira; sem dados reais nem ações operacionais.

## 2. Contexto técnico

- I6F assessment MERGED (PR #92): AUTHORIZED_WITH_CONDITIONS / RUNS_SCREEN_ONLY / fixture-backed / read-only.
- I6F post-merge closure MERGED (PR #93). Human task authorizes I6G Runs implementation only.
- I6B ViewModels MERGED (PR #81); I6C fixtures MERGED (PR #84); I5 shell MERGED (PR #77); I6E Overview MERGED (PR #90).
- Screen mounts inside ApplicationShell outlet; replaces only `/future-collection/runs` placeholder.

## 3. Componentes afetados

| Componente | Impacto |
|------------|---------|
| `web/src/screens/runs/**` | Nova tela e componentes de tela |
| `web/src/app/AppRoutes.tsx` | Troca placeholder Runs pela tela real |
| `web/src/fixtures/scenarios.ts` | Enrichment opcional `in_progress` na lista Runs de `collection_in_progress` |
| `web/tests/screens/**`, `web/tests/a11y/**` | Testes de tela / a11y / fronteira |
| `docs/PROJECT.md` | Estado I6G / flags / NEXT |
| Governance I6G | Impact / spec / review / handoff |
| Backend / R3E / scheduler | Não afetados |
| Overview screen | Preservada (sem mudança visual/comportamental) |

## 4. Arquivos previstos

```text
web/src/screens/runs/**
web/src/app/AppRoutes.tsx
web/src/fixtures/scenarios.ts
web/tests/screens/runs/**
web/tests/a11y/runs.a11y.test.tsx
web/tests/screens/overview/overviewScreen.test.tsx
web/tests/screens/overview/architectureBoundary.test.ts
docs/ai-impact/UX-R1-I6G-RUNS-SCREEN-IMPLEMENTATION_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-I6G-RUNS-SCREEN-IMPLEMENTATION_SPEC.md
docs/ai-reviews/UX-R1-I6G-RUNS-SCREEN-IMPLEMENTATION_REVIEW.md
reports/ai-implementation/UX-R1-I6G-RUNS-SCREEN-IMPLEMENTATION_HANDOFF.md
docs/PROJECT.md
```

## 5. Contratos e interfaces

```text
ROUTE = /future-collection/runs
SCREEN = RunsScreen
DATA = buildFixtureViewModels("current_project_state_illustrative").runs + metadata
VISIBLE_LABELS = "Dados ilustrativos" | "Synthetic fixture" | "Não representa evidência operacional real"
SECTIONS =
  PageHeader
  SyntheticDataNotice
  RunsSummary
  RunsCollection
  RunStatus
  RunTiming
  RunCounts
  RunStoreDelta
  RunIdempotency
  RunFailureReason
  RunEvidenceReference
  EmptyState
  PartialUnknownState
STATUS_SEMANTICS = I2/I3 StatusBadge + I6B presentation mapping
ACTION_HINT = advisory text only; no buttons that execute
PRODUCT_FIXTURE = current_project_state_illustrative
TEST_SCENARIOS = collection_in_progress; confirmed_collection_fault; partial_unknown_data; empty_no_runs; current_project_state_illustrative
```

## 6. Persistência e dados

Nenhuma persistência. Fonte única: fixture sintético I6C via `buildFixtureViewModels`. Sem fetch, axios, WebSocket, filesystem runtime, localStorage operacional ou env payload.

## 7. Concorrência, locks e idempotência

N/A backend. Montagem determinística do ViewModel a partir do fixture; campo `idempotencyResult` apenas exibido quando fornecido.

## 8. Segurança

```text
NO_SECRETS = true
NO_AUTH = true
NO_OPERATIONAL_COMMANDS = true
pnpm audit --audit-level high required
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
EVIDENCE_AS_TEXT_ONLY = true
```

## 9. Observabilidade

Sem telemetria. Testes unitários + axe smoke na rota Runs + architecture boundary scan.

## 10. Operação

Não altera scheduler, host discovery, coleta, validate ou estado científico R3E. `actionHint` é apenas texto consultivo.

## 11. Rollback

```text
ROLLBACK = revert PR; restaurar PlaceholderPage em /future-collection/runs; remover web/src/screens/runs/**
NEVER via R3E / validate / scheduler
```

## 12. Compatibilidade

- Consome I2 tokens, I3 primitives, I5 shell/outlet, I6B RunsViewModel, I6C fixture catalog.
- Não redefine tokens/primitivos/builders (exceto enrichment de runs list em `collection_in_progress`).
- Overview permanece implementada; Readiness/Host permanecem placeholders.

## 13. Testes necessários

```text
runs route renders real screen
synthetic notice visible
current illustrative state renders
complete / in_progress / fault / empty / partial_unknown scenarios
in_progress not fault/red
confirmed fault is fault/red
missing counts/timestamps not zero-filled
evidence reference does not fabricate links
no operational buttons
Overview remains implemented
Readiness and Host remain placeholders
responsive table/card structure
axe smoke
architecture boundary: no network/ops/scheduler/scientific imports
no visible fixture selector
```

## 14. Alternativas consideradas

| Alternativa | Decisão |
|-------------|--------|
| Implementar Readiness/Host no mesmo PR | REJECTED — RUNS_SCREEN_ONLY |
| Seletor visível de fixtures | REJECTED — fixture fixo interno |
| Dados reais / API | REJECTED — not authorized |
| Botões de ação operacional | REJECTED — advisory only |
| Filters/pagination/detail B3 | REJECTED — out of scope |
| Dependências novas | REJECTED |

## 15. Riscos

| Risco | Severidade | Mitigação |
|-------|------------|-----------|
| Scope creep to other screens | HIGH | Route wiring limited to /future-collection/runs |
| Confusing synthetic with real | HIGH | Mandatory SyntheticDataNotice labels |
| IN_PROGRESS rendered as fault/red | HIGH | StatusBadge informational + tests |
| Empty/unknown painted as fault | HIGH | Distinct empty copy + unknown badge |
| Accidental operational controls | MEDIUM | No Button; advisory hint only |

## 16. Questões abertas

```text
NONE_BLOCKING
READINESS_HOST = remain unauthorized until separate human tasks
```

## 17. Decisão arquitetural recomendada

Screen module under `web/src/screens/runs/`; assemble ViewModel via I6C `buildFixtureViewModels("current_project_state_illustrative")`; reuse I3 primitives; token-only CSS; replace `/future-collection/runs` placeholder only; WCAG 2.2 AA; zero new dependencies.

## 18. Critérios para autorizar implementação

```text
1. This impact IMPACT_ASSESSMENT_STATUS = APPROVED
2. IMPLEMENTATION_AUTHORIZED = true
3. RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED = true (human task)
4. I6F AUTHORIZED_WITH_CONDITIONS assessment MERGED
5. Scope limited to Runs screen + tests + governance
6. RUNS_SCREEN_MERGE_AUTHORIZED remains false until human merge
```

All criteria satisfied for proceeding with I6G Runs screen code in this task/PR.
