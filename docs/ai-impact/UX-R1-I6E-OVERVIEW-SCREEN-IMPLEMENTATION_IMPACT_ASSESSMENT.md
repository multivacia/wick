# UX-R1-I6E-OVERVIEW-SCREEN-IMPLEMENTATION — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = I6D-SCREEN-IMPLEMENTATION-AUTHORIZATION-ASSESSMENT-001
TASK_ID = OVERVIEW-SCREEN-IMPLEMENTATION-001
TITLE = Overview Screen Implementation
INCREMENT = I6E
PHASE = IMPLEMENTATION
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = true
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = true
I6_OVERVIEW_SCREEN_IMPLEMENTATION_AUTHORIZED = true
I6_OVERVIEW_SCREEN_MERGE_AUTHORIZED = false
RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED = false
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
BASE_SHA = 502f4c2080a02941993a6faa2028ac6b07e3efb6
ANALYZED_AT = 2026-07-20T14:52:00Z
ANALYZED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTHORIZATION_DECISION = HUMAN_AUTHORIZED_FOR_THIS_TASK
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
FRONTEND_LOCATION = web/
I6D_DECISION = AUTHORIZED_WITH_CONDITIONS
I6D_RECOMMENDED_SCREEN_SEQUENCE = OVERVIEW_FIRST
I6D_FIRST_AUTHORIZED_SCREEN = Visão Geral
FIXTURE_ID = current_project_state_illustrative
```

G1 note: authorization covers **only** the read-only fixture-backed Visão Geral (`/overview`) screen. It does **not** authorize Runs/Readiness/Host-Scheduler screens, fixture UI selectors, real-data adapters, operational buttons, scheduler activation, or scientific validation.

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
REPLACE_OVERVIEW_PLACEHOLDER_ONLY = true
PRESERVE_OTHER_ROUTE_PLACEHOLDERS = true
NOT_READY_IS_NOT_FAULT = true
BLOCKED_IS_NOT_FAULT = true
DEFERRED_IS_NOT_FAULT = true
RED_ONLY_FOR_CONFIRMED_FAULT = true
NO_FAKE_ZEROES = true
NO_FABRICATED_LINKS_OR_METRICS = true
NEXT_SAFE_ACTION_ADVISORY_ONLY = true
WCAG_2_2_AA = true
PARALLEL_TASKS_ALLOWED = false
HOST_DISCOVERY = DEFERRED
SCHEDULER_ACTIVATION = BLOCKED
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## SUMMARY

Implement the first Wick product screen Visão Geral at `/overview`, consuming merged Overview ViewModel + synthetic fixture `current_project_state_illustrative` + shell/router + tokens + accessible primitives. Read-only. Clearly labeled synthetic. No other screens.

## 1. Objetivo

Entregar a tela Visão Geral com seções PageHeader, SyntheticDataNotice, OverallOperationalState, CollectionSummary, ReadinessSummary, HostSchedulerSummary, ActiveBlockers, LatestEvidence e NextSafeAction; testes de rota, a11y e fronteira; sem dados reais nem ações operacionais.

## 2. Contexto técnico

- I6D assessment MERGED (PR #87): AUTHORIZED_WITH_CONDITIONS / OVERVIEW_FIRST / first screen Visão Geral.
- I6B ViewModels MERGED (PR #81); I6C fixtures MERGED (PR #84); I5 shell MERGED (PR #77); I3 primitives MERGED (PR #72); I2 tokens MERGED (PR #69).
- Post-merge I6D closure MERGED (PRs #88/#89). Human task authorizes I6E Overview implementation only.
- Screen mounts inside ApplicationShell outlet; replaces only `/overview` placeholder.

## 3. Componentes afetados

| Componente | Impacto |
|------------|---------|
| `web/src/screens/overview/**` | Nova tela e componentes de tela |
| `web/src/app/AppRoutes.tsx` | Troca placeholder Overview pela tela real |
| `web/tests/screens/**`, `web/tests/a11y/**` | Testes de tela / a11y / fronteira |
| `web/tests/shell/shell.test.tsx`, `web/tests/App.test.tsx` | Ajuste de asserções Overview |
| `docs/PROJECT.md` | Estado I6E / flags / NEXT |
| Governance I6E | Impact / spec / review / handoff |
| Backend / R3E / scheduler | Não afetados |

## 4. Arquivos previstos

```text
web/src/screens/overview/**
web/src/app/AppRoutes.tsx
web/tests/screens/overview/**
web/tests/a11y/overview.a11y.test.tsx
docs/ai-impact/UX-R1-I6E-OVERVIEW-SCREEN-IMPLEMENTATION_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-I6E-OVERVIEW-SCREEN-IMPLEMENTATION_SPEC.md
docs/ai-reviews/UX-R1-I6E-OVERVIEW-SCREEN-IMPLEMENTATION_REVIEW.md
reports/ai-implementation/UX-R1-I6E-OVERVIEW-SCREEN-IMPLEMENTATION_HANDOFF.md
docs/PROJECT.md
```

## 5. Contratos e interfaces

```text
ROUTE = /overview
SCREEN = OverviewScreen
DATA = buildFixtureViewModels("current_project_state_illustrative").overview + metadata
VISIBLE_LABELS = "Dados ilustrativos" | "Synthetic fixture" | "Não representa evidência operacional real"
SECTIONS =
  PageHeader
  SyntheticDataNotice
  OverallOperationalState
  CollectionSummary
  ReadinessSummary
  HostSchedulerSummary
  ActiveBlockers
  LatestEvidence
  NextSafeAction
STATUS_SEMANTICS = I2/I3 StatusBadge + I6B presentation mapping
NEXT_SAFE_ACTION = advisory text only; no buttons that execute
```

## 6. Persistência e dados

Nenhuma persistência. Fonte única: fixture sintético I6C via `buildFixtureViewModels`. Sem fetch, axios, WebSocket, filesystem runtime, localStorage operacional ou env payload.

## 7. Concorrência, locks e idempotência

N/A backend. Montagem determinística do ViewModel a partir do fixture fixo; sem clock implícito além do nowIso do cenário.

## 8. Segurança

```text
NO_SECRETS = true
NO_AUTH = true
NO_OPERATIONAL_COMMANDS = true
pnpm audit --audit-level high required
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
```

## 9. Observabilidade

Sem telemetria. Testes unitários + axe smoke na rota Overview.

## 10. Operação

Não altera scheduler, host discovery, coleta, validate ou estado científico R3E. Next safe action é apenas texto consultivo.

## 11. Rollback

```text
ROLLBACK = revert PR; restaurar PlaceholderPage em /overview; remover web/src/screens/overview/**
NEVER via R3E / validate / scheduler
```

## 12. Compatibilidade

- Consome I2 tokens, I3 primitives, I5 shell/outlet, I6B OverviewViewModel, I6C fixture catalog.
- Não redefine tokens/primitivos/builders/fixtures.
- Outras rotas MVP permanecem placeholders.

## 13. Testes necessários

```text
overview route renders real screen
synthetic notice visible
fixture clearly illustrative
overall state / collection / readiness / host-scheduler
NOT_READY not fault/red
host deferred / scheduler blocked
active blockers / latest evidence / next safe action
missing metrics not zero-filled
no operational buttons
other routes remain placeholders
semantic headings / responsive / axe smoke
architecture boundary: no network/ops/scheduler/scientific imports
```

## 14. Alternativas consideradas

| Alternativa | Decisão |
|-------------|--------|
| Implementar todas as telas MVP | REJECTED — OVERVIEW_FIRST only |
| Seletor visível de fixtures | REJECTED — fixture fixo interno |
| Dados reais / API | REJECTED — not authorized |
| Botões de ação operacional | REJECTED — advisory only |
| Dependências novas | REJECTED |

## 15. Riscos

| Risco | Severidade | Mitigação |
|-------|------------|-----------|
| Scope creep to other screens | HIGH | Route wiring limited to /overview |
| Confusing synthetic with real | HIGH | Mandatory SyntheticDataNotice labels |
| NOT_READY rendered as fault/red | HIGH | StatusBadge + presentation mapping tests |
| Accidental operational controls | MEDIUM | No Button for actions; advisory panel only |

## 16. Questões abertas

```text
NONE_BLOCKING
OTHER_SCREENS = remain unauthorized until separate human tasks
```

## 17. Decisão arquitetural recomendada

Screen module under `web/src/screens/overview/`; assemble ViewModel via I6C `buildFixtureViewModels("current_project_state_illustrative")`; reuse I3 primitives; token-only CSS; replace `/overview` placeholder only; WCAG 2.2 AA; zero new dependencies.

## 18. Critérios para autorizar implementação

```text
1. This impact IMPACT_ASSESSMENT_STATUS = APPROVED
2. IMPLEMENTATION_AUTHORIZED = true
3. I6_OVERVIEW_SCREEN_IMPLEMENTATION_AUTHORIZED = true (human task)
4. I6D OVERVIEW_FIRST assessment MERGED
5. Scope limited to Overview screen + tests + governance
6. I6_OVERVIEW_SCREEN_MERGE_AUTHORIZED remains false until human merge
```

All criteria satisfied for proceeding with I6E Overview screen code in this task/PR.
