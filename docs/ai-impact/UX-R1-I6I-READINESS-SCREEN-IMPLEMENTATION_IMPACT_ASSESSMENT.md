# UX-R1-I6I-READINESS-SCREEN-IMPLEMENTATION — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = READINESS-SCREEN-IMPLEMENTATION-AUTHORIZATION-ASSESSMENT-001
TASK_ID = READINESS-SCREEN-IMPLEMENTATION-001
TITLE = Readiness Screen Implementation
INCREMENT = I6I
PHASE = IMPLEMENTATION
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = true
READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED = true
READINESS_SCREEN_MERGE_AUTHORIZED = false
HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
REAL_DATA_INTEGRATION_AUTHORIZED = false
OPERATIONAL_ACTIONS_AUTHORIZED = false
VALIDATION_EXECUTION_AUTHORIZED = false
COLLECTION_ACTIONS_AUTHORIZED = false
SCHEDULER_ACTIONS_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
COLLECTION = IN_PROGRESS
READINESS = NOT_READY
READINESS_REASON = WINDOW_DAYS_INSUFFICIENT
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE_CHANGE = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 7c050b532997a0ddefebec58236317579c395499
FINAL_CANDIDATE_HEAD = PENDING
CONTENT_REVIEWED_THROUGH_HEAD = PENDING
POST_REVIEW_NORMATIVE_CHANGES = 0
ANALYZED_AT = 2026-07-20T22:58:00Z
ANALYZED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTHORIZATION_DECISION = HUMAN_AUTHORIZED_FOR_THIS_TASK
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
FRONTEND_LOCATION = web/
I6H_DECISION = AUTHORIZED_WITH_CONDITIONS
I6H_RECOMMENDED_IMPLEMENTATION_BOUNDARY = READINESS_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; NO_VISIBLE_FIXTURE_SELECTOR; NO_REAL_DATA; NO_VALIDATION_EXECUTION; NO_COLLECTION_ACTIONS; NO_SCHEDULER_ACTIONS; NO_SCIENTIFIC_INTERPRETATION_CHANGE
FIXTURE_ID = current_project_state_illustrative
ROUTE = /future-collection/readiness
SCREEN = Prontidão
```

G1 note: authorization covers **only** the read-only fixture-backed Prontidão (`/future-collection/readiness`) screen. It does **not** authorize Host-Scheduler, fixture UI selectors, real-data adapters, validation execution, collection/scheduler controls, or scientific interpretation changes. Overview and Runs remain preserved.

## MANDATORY_CONSTRAINTS

```text
READ_ONLY = true
FIXTURE_BACKED = true
FIXTURE_ID = current_project_state_illustrative
NO_VISIBLE_FIXTURE_SELECTOR = true
NO_REAL_DATA = true
NO_VALIDATION_EXECUTION = true
NO_COLLECTION_ACTIONS = true
NO_SCHEDULER_ACTIONS = true
NO_NETWORK_CLIENTS = true
NO_BACKEND_API = true
NO_EXTRA_RUNTIME_OR_DEV_DEPENDENCIES = true
TOKEN_ONLY_STYLING = true
REUSE_I3_PRIMITIVES = true
CONSUME_I6B_VIEWMODELS = true
CONSUME_I6C_FIXTURES = true
REPLACE_READINESS_PLACEHOLDER_ONLY = true
PRESERVE_OVERVIEW_SCREEN = true
PRESERVE_RUNS_SCREEN = true
PRESERVE_HOST_SCHEDULER_PLACEHOLDER = true
NOT_READY_IS_NOT_FAULT = true
READY_IS_NOT_STRATEGY_APPROVAL = true
READY_IS_NOT_PROFITABILITY = true
BLOCKED_IS_NOT_FAULT = true
UNKNOWN_IS_NOT_ZERO = true
MISSING_IS_NOT_ZERO = true
RED_ONLY_FOR_CONFIRMED_FAULT = true
NO_FAKE_ZEROES = true
NO_FABRICATED_COLLECTION_HEALTH = true
NO_FABRICATED_LINKS_OR_METRICS = true
NO_GAUGE_OR_CASINO_PROGRESS = true
ILLUSTRATIVE_WINDOW_DISCLOSURE = true
NO_B3_SERIES_GAPS_DUPLICATES_CUTOFF_PARITY = true
WCAG_2_2_AA = true
PARALLEL_TASKS_ALLOWED = false
HOST_DISCOVERY = DEFERRED
SCHEDULER_ACTIVATION = BLOCKED
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## SUMMARY

Implement the Wick product screen Prontidão at `/future-collection/readiness`, consuming merged Readiness ViewModel + synthetic fixture catalog + shell/router + tokens + accessible primitives. Read-only. Clearly labeled synthetic. No Host screen. No validation/collection/scheduler controls.

## 1. Objetivo

Entregar a tela Prontidão com PageHeader, SyntheticDataNotice, ReadinessStatusCard, WindowProgress (linear/textual), BlockingReason, ValidationExecutionState, EffectPeekingState, CollectionState (sem fabricar health), NextSafeAction, EvidenceReference e PartialUnknownState; testes de rota, a11y e fronteira; sem dados reais nem ações operacionais.

## 2. Contexto técnico

- I6H assessment MERGED (PR #96): AUTHORIZED_WITH_CONDITIONS / READINESS_SCREEN_ONLY / fixture-backed / read-only.
- I6H post-merge closure MERGED (PR #97). Human task authorizes I6I Readiness implementation only.
- I6B ViewModels MERGED; I6C fixtures MERGED; I5 shell MERGED; I6E Overview MERGED; I6G Runs MERGED.
- Screen mounts inside ApplicationShell outlet; replaces only `/future-collection/readiness` placeholder.
- Optional narrowly-scoped READY synthetic fixture may be added for UI tests only (product route remains illustrative NOT_READY).

## 3. Componentes afetados

| Componente | Impacto |
|------------|---------|
| `web/src/screens/readiness/**` | Nova tela e componentes |
| `web/src/app/AppRoutes.tsx` | Troca placeholder Readiness pela tela real |
| `web/src/shell/navigation.ts` | Label nav "Readiness" → "Prontidão" (chrome PT) |
| `web/src/fixtures/types.ts` / `scenarios.ts` | Fixture READY ilustrativo opcional para testes |
| `web/tests/screens/**`, `web/tests/a11y/**` | Testes de tela / a11y / fronteira |
| `web/tests/screens/runs/runsScreen.test.tsx` | Ajuste mínimo: Readiness deixa de ser placeholder |
| `docs/PROJECT.md` | Estado I6I / flags / NEXT |
| Governance I6I | Impact / spec / review / handoff |
| Backend / R3E / scheduler | Não afetados |
| Overview / Runs screens | Preservados |

## 4. Arquivos previstos

```text
web/src/screens/readiness/**
web/src/app/AppRoutes.tsx
web/src/shell/navigation.ts
web/src/fixtures/types.ts
web/src/fixtures/scenarios.ts
web/tests/screens/readiness/**
web/tests/a11y/readiness.a11y.test.tsx
web/tests/screens/runs/runsScreen.test.tsx
docs/ai-impact/UX-R1-I6I-READINESS-SCREEN-IMPLEMENTATION_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-I6I-READINESS-SCREEN-IMPLEMENTATION_SPEC.md
docs/ai-reviews/UX-R1-I6I-READINESS-SCREEN-IMPLEMENTATION_REVIEW.md
reports/ai-implementation/UX-R1-I6I-READINESS-SCREEN-IMPLEMENTATION_HANDOFF.md
docs/PROJECT.md
```

## 5. Contratos e interfaces

```text
ROUTE = /future-collection/readiness
SCREEN = ReadinessScreen
DATA = buildFixtureViewModels("current_project_state_illustrative").readiness + metadata
VISIBLE_LABELS = "Dados ilustrativos" | "Synthetic fixture" | "Não representa evidência operacional real"
SECTIONS =
  PageHeader
  SyntheticDataNotice
  ReadinessStatusCard
  WindowProgress
  BlockingReason
  ValidationExecutionState
  EffectPeekingState
  CollectionState
  NextSafeAction
  EvidenceReference
  PartialUnknownState
STATUS_SEMANTICS = I2/I3 StatusBadge + I6B presentation mapping
ACTION_HINT = advisory text only; no buttons that execute
PRODUCT_FIXTURE = current_project_state_illustrative
TEST_SCENARIOS = current_project_state_illustrative; partial_unknown_data; readiness_ready_illustrative
COLLECTION_STATE = disclosure only from nextSafeAction / absence of VM fields; no fabricated health
```

## 6. Persistência e dados

Nenhuma persistência. Fonte única: fixture sintético I6C via `buildFixtureViewModels`. Sem fetch, axios, WebSocket, filesystem runtime, localStorage operacional ou env payload.

## 7. Concorrência, locks e idempotência

N/A backend. Montagem determinística do ViewModel a partir do fixture.

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

Sem telemetria. Testes unitários + axe smoke na rota Readiness + architecture boundary scan.

## 10. Operação

Não altera scheduler, host discovery, coleta, validate ou estado científico R3E. `nextSafeAction` é apenas texto consultivo. Janela ilustrativa (ex.: 14 dias) permanece rotulada como sintética vs protocolo ~90.

## 11. Rollback

```text
ROLLBACK = revert PR; restaurar PlaceholderPage em /future-collection/readiness; remover web/src/screens/readiness/**
NEVER via R3E / validate / scheduler
```

## 12. Compatibilidade

- Consome I2 tokens, I3 primitives, I5 shell/outlet, I6B ReadinessViewModel, I6C fixture catalog.
- Overview e Runs permanecem implementados; Host permanece placeholder.
- Nav label PT "Prontidão" alinhado ao chrome da tela.

## 13. Testes necessários

```text
readiness route renders real screen
synthetic notice visible
current illustrative state renders NOT_READY
NOT_READY not fault/red
READY does not imply strategy/profitability approval
observed/required days render; missing not zero-filled
window progress is linear/textual not gauge
unknown distinct from fault
validation not executed distinct from validation failed
effect peeking false distinct from not reported
collection section does not fabricate health metrics
blocking reason / next safe action / evidence text-only
no validation/collection/scheduler controls
Overview and Runs remain implemented
Host remains placeholder
responsive + axe + architecture boundary
no visible fixture selector
```

## 14. Alternativas consideradas

| Alternativa | Decisão |
|-------------|--------|
| Implementar Host no mesmo PR | REJECTED — READINESS_SCREEN_ONLY |
| Seletor visível de fixtures | REJECTED — fixture fixo interno |
| Dados reais / API | REJECTED — not authorized |
| Gauge / casino progress | REJECTED — linear/textual only |
| Fabricar collection health / cutoff / gaps | REJECTED — out of VM scope |
| Botões validate/collect/scheduler | REJECTED — advisory only |
| Dependências novas | REJECTED |

## 15. Riscos

| Risco | Severidade | Mitigação |
|-------|------------|-----------|
| Scope creep to Host/real data | HIGH | Route wiring limited to readiness |
| Confusing synthetic with real | HIGH | Mandatory SyntheticDataNotice |
| NOT_READY rendered as fault/red | HIGH | StatusBadge not_ready/amber + tests |
| READY implies strategy approval | HIGH | Explicit copy + do_not_validate hint |
| Misleading window progress | MEDIUM | Linear bar + illustrative disclosure |
| Fabricated collection health | MEDIUM | Explicit out-of-VM disclosure |

## 16. Questões abertas

```text
NONE_BLOCKING
HOST = remain unauthorized until separate human task
```

## 17. Decisão arquitetural recomendada

Screen module under `web/src/screens/readiness/`; assemble ViewModel via I6C `buildFixtureViewModels("current_project_state_illustrative")`; reuse I3 primitives; token-only CSS; replace `/future-collection/readiness` placeholder only; optional READY test fixture; WCAG 2.2 AA; zero new dependencies.

## 18. Critérios para autorizar implementação

```text
1. This impact IMPACT_ASSESSMENT_STATUS = APPROVED
2. IMPLEMENTATION_AUTHORIZED = true
3. READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED = true (human task)
4. I6H AUTHORIZED_WITH_CONDITIONS assessment MERGED
5. Scope limited to Readiness screen + tests + governance
6. READINESS_SCREEN_MERGE_AUTHORIZED remains false until human merge
```

All criteria satisfied for proceeding with I6I Readiness screen code in this task/PR.
