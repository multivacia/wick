# UX-R1-I6B-VIEWMODEL-IMPLEMENTATION — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = I6A-OVERVIEW-SCREEN-DATA-AND-FIXTURE-PREPARATION-001
TASK_ID = VIEWMODEL-IMPLEMENTATION-001
TITLE = ViewModel Implementation
INCREMENT = I6B
PHASE = IMPLEMENTATION
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED = true
I6_VIEWMODEL_MERGE_AUTHORIZED = false
I6_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
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
BASE_SHA = 2d281a228f403a58a28cc5ada232ec0d553a0186
ANALYZED_AT = 2026-07-20T12:36:00Z
ANALYZED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = PENDING
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTHORIZATION_DECISION = HUMAN_AUTHORIZED_FOR_THIS_TASK
NEW_RUNTIME_DEPENDENCIES = 0
FRONTEND_LOCATION = web/
I5_IMPLEMENTATION_STATUS = MERGED
I6B_DECISION = AUTHORIZED_WITH_CONDITIONS
```

G1 note: `I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED=true` covers **typed pure ViewModel builders and presentation contracts only**. It does **not** authorize executable fixtures, product screens, shell visuals, real-data adapters, scheduler activation, or scientific validation.

## MANDATORY_CONSTRAINTS

```text
PURE_FUNCTIONS = true
DETERMINISTIC = true
IMMUTABLE_INPUTS = true
SERIALIZABLE_OUTPUTS = true
FRAMEWORK_AGNOSTIC = true
SCREEN_AGNOSTIC = true
DATA_SOURCE_AGNOSTIC = true
NO_REACT_IMPORTS_IN_VIEWMODELS
NO_ROUTER_IMPORTS_IN_VIEWMODELS
NO_NETWORK_CLIENTS_IN_VIEWMODELS
NO_FIXTURE_IMPLEMENTATION
NO_SCREEN_CONTENT_IMPLEMENTATION
NO_OPERATIONAL_DATA_INTEGRATION
NO_EXTRA_RUNTIME_DEPENDENCIES
NOT_READY_IS_NOT_FAULT
BLOCKED_IS_NOT_FAULT
DEFERRED_IS_NOT_FAULT
RED_ONLY_FOR_CONFIRMED_FAULT
NO_FAKE_ZEROES
NO_FAKE_TIMESTAMPS
NO_INVENTED_STATUS
EXPLICIT_NOW_FOR_FRESHNESS
I6_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
HOST_DISCOVERY = DEFERRED
SCHEDULER_ACTIVATION = BLOCKED
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## SUMMARY

Implement a typed, pure, screen-agnostic ViewModel layer under `web/src/viewmodels/` that maps normalized operational-domain inputs into presentation-ready contracts for future Visão Geral, Execuções, Prontidão, and Host/Scheduler screens. No product screens, fixtures, or real-data integration.

## 1. Objetivo

Entregar contratos compartilhados de apresentação e builders `buildOverviewViewModel`, `buildRunsViewModel`, `buildReadinessViewModel`, `buildHostSchedulerViewModel`, com taxonomia de razões, semântica de status (NOT_READY ≠ FAULT), handling de dados parciais, tempo explícito e testes de fronteira arquitetural.

## 2. Contexto técnico

- I5 shell/nav MERGED (PR #77); rotas com placeholders neutros.
- I6A contracts MERGED (docs): Overview ViewModel field groups and fixture scenarios remain documentation; this task does **not** implement TypeScript fixtures.
- StatusBadge / semantic tokens already encode healthy/completed/attention/not_ready/blocked/deferred/unknown/fault/informational.
- ViewModels must remain framework-agnostic and serializable for future screens (I6C+) without importing React or router.

## 3. Componentes afetados

| Componente | Impacto |
|------------|---------|
| `web/src/viewmodels/**` | Novo domínio de apresentação puro |
| `web/tests/viewmodels/**` | Testes unitários e de fronteira |
| `docs/PROJECT.md` | Estado I6B / flags / NEXT |
| Governance artifacts I6B | Impact / spec / review / handoff |

Shell, router, primitives, package.json dependencies: **unchanged** (except optional non-visual typing if strictly necessary — not planned).

## 4. Arquivos previstos

```text
web/src/viewmodels/**
web/tests/viewmodels/**
docs/ai-impact/UX-R1-I6B-VIEWMODEL-IMPLEMENTATION_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-I6B-VIEWMODEL-IMPLEMENTATION_SPEC.md
docs/ai-reviews/UX-R1-I6B-VIEWMODEL-IMPLEMENTATION_REVIEW.md
reports/ai-implementation/UX-R1-I6B-VIEWMODEL-IMPLEMENTATION_HANDOFF.md
docs/PROJECT.md
```

## 5. Contratos e interfaces

Inputs: normalized operational facts (collection run, freshness, readiness, host, scheduler, blockers, evidence) with explicit availability (`unknown` / `not_available` / domain states).

Outputs: `PresentationStatus`, `PresentationSeverity`, messages, evidence links, action hints, timestamp/metric presentation, screen-agnostic ViewModel objects.

Semantic mapping:

```text
READY/COMPLETE → healthy/green
IN_PROGRESS → informational/cyan
NOT_READY → attention/amber
BLOCKED/DEFERRED → blocked_or_neutral/purple_or_gray
UNKNOWN → neutral/gray
FAULT → critical/red
```

## 6. Persistência e dados

Nenhuma persistência. Sem adapter. Sem leitura de arquivos operacionais. Dados de exemplo somente em testes.

## 7. Segurança / operação

Action hints are advisory presentation only — no command execution, scheduler activation, validation, merge, or financial actions.

## 8. Testes necessários

Status semantics, partial data, explicit `now`, deterministic/immutable/serializable outputs, all four builders, reason codes, architecture boundary (no react/router/fetch/fixtures/screens imports).

## 9. Alternativas consideradas

| Alternativa | Decisão |
|-------------|--------|
| Colocar ViewModels em `web/src/domain/presentation/` | Equivalente; escolhido `web/src/viewmodels/` por clareza |
| Incluir fixtures TypeScript (I6A scenarios) | Rejeitado — `I6_FIXTURE_IMPLEMENTATION_AUTHORIZED=false` |
| Hooks React / context | Rejeitado — deve ser framework-agnostic |

## 10. Riscos

| Risco | Mitigação |
|-------|-----------|
| Confundir NOT_READY com FAULT | Testes semânticos obrigatórios |
| Inventar métricas/zeros | `null` + availability explícita |
| Acoplar a telas | Boundary tests + no screen imports |
| Escopo I6B virar fixtures/screens | Flags false; review checklist |

## 11. Critérios para autorizar implementação

Já autorizados por este prompt humano para esta tarefa:

```text
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED = true
```

Merge permanece `I6_VIEWMODEL_MERGE_AUTHORIZED=false` até autorização humana separada.

## Decisão arquitetural recomendada

```text
DECISION = APPROVED_FOR_IMPLEMENTATION
LOCATION = web/src/viewmodels/
NEW_RUNTIME_DEPENDENCIES = 0
IMPLEMENTATION_STATUS = AUTHORIZED
```
