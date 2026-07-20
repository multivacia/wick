# UX-R1-I6F — Runs Screen Implementation Authorization Assessment

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
TASK_ID = RUNS-SCREEN-IMPLEMENTATION-AUTHORIZATION-ASSESSMENT-001
TITLE = Runs Screen Implementation Authorization Assessment
INCREMENT = I6F
PHASE = AUTHORIZATION_ASSESSMENT
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
ASSESSMENT_ONLY = true
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_SCOPE = AUTHORIZATION_ASSESSMENT_DOCUMENTATION_ONLY
IMPLEMENTATION_EXECUTION_AUTHORIZED = false
DECISION = AUTHORIZED_WITH_CONDITIONS
RECOMMENDED_IMPLEMENTATION_BOUNDARY = RUNS_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; NO_VISIBLE_FIXTURE_SELECTOR; NO_REAL_DATA; NO_OPERATIONAL_ACTIONS
SCREEN = Execuções
ROUTE = /future-collection/runs
RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED = false
READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED = false
HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
OPERATIONAL_ACTIONS_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE_CHANGE = false
PR90_STATUS = MERGED
PR90_MERGE_COMMIT = 93b92206b4ae46abe47fe465654964806a2bdb2d
PR91_STATUS = MERGED
I6_OVERVIEW_SCREEN_IMPLEMENTATION_STATUS = MERGED
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = a9365f929693a7cec20b212fba6a3f4b7d6dddeb
ANALYZED_AT = 2026-07-20T16:48:08Z
ANALYZED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
NEXT_RECOMMENDED_TASK = I6_RUNS_SCREEN_IMPLEMENTATION
NEXT_ITEM = I6_RUNS_SCREEN_SEPARATE_IMPLEMENTATION_TASK
```

G1 note: This assessment may recommend **AUTHORIZED_WITH_CONDITIONS** for a future Runs-only screen task. It does **not** flip `RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED`, `IMPLEMENTATION_EXECUTION_AUTHORIZED`, or `UI_SCREEN_IMPLEMENTATION_AUTHORIZED` to true for product execution. Screen implementation requires a separate human-authorized implementation prompt.

## SUMMARY

Prerequisites I2, I3, I5, I6B, I6C, and I6E (Overview) are merged. The project is ready to authorize a **narrow, fixture-backed, read-only Execuções (Runs) screen** at `/future-collection/runs` as the next visual product surface. Full B3 list/detail/filters/pagination parity, real-data integration, and operational actions are not authorized.

## 1. Objetivo

Avaliar se o projeto está pronto para autorizar uma tarefa separada de implementação da tela **Execuções** (`/future-collection/runs`), somente leitura e alimentada por fixtures, sem implementar a tela nesta tarefa.

## 2. Contexto técnico

- I6E Overview MERGED (PR #90 → `93b9220`); post-merge closure MERGED (PR #91 → `a9365f9`).
- `NEXT_RECOMMENDED_TASK` em `main` já aponta para `I6_RUNS_SCREEN_AUTHORIZATION_ASSESSMENT`.
- I6B `buildRunsViewModel` / `buildRunViewModel` MERGED; I6C fixture catalog MERGED; I5 route placeholder MERGED.
- I6D sequenciava Overview → Readiness → Runs; após Overview MERGED, o próximo item humano recomendado é Runs (esta avaliação). Readiness/Host permanecem não autorizados.
- Estado científico/operacional preservado: host discovery DEFERRED; scheduler BLOCKED; readiness NOT_READY por janela insuficiente; R3E pending future unseen data; R4 BLOCKED; R5 NOT_STARTED.

## 3. Componentes afetados

| Componente | Impacto nesta tarefa |
|------------|----------------------|
| Docs I6F (impact/review/handoff) | Novos artefatos de autorização |
| `docs/PROJECT.md` | Resultado da assessment + NEXT |
| `web/src/screens/**` | Não modificado |
| Rotas / fixtures / ViewModels | Não modificados |
| Backend / R3E / scheduler | Não afetados |

## 4. Arquivos previstos

```text
docs/ai-impact/UX-R1-I6F-RUNS-SCREEN-IMPLEMENTATION-AUTHORIZATION_ASSESSMENT.md
docs/ai-reviews/UX-R1-I6F-RUNS-SCREEN-IMPLEMENTATION-AUTHORIZATION_REVIEW.md
reports/ai-implementation/UX-R1-I6F-RUNS-SCREEN-IMPLEMENTATION-AUTHORIZATION_HANDOFF.md
docs/PROJECT.md
```

Futura implementação (fora desta tarefa) ficaria tipicamente em:

```text
web/src/screens/runs/**
web/src/app/AppRoutes.tsx  (somente /future-collection/runs)
web/tests/screens/runs/**
web/tests/a11y/runs.a11y.test.tsx
```

## 5. Contratos e interfaces

```text
ROUTE_CANONICAL = /future-collection/runs
ROUTE_B3_DOC_ALIAS = /collection/runs  (docs B3; código I5 usa /future-collection/runs)
SCREEN_LABEL = Execuções
DATA_SOURCE = buildFixtureViewModels(<fixtureId>).runs + metadata
VIEWMODEL = RunsViewModel + RunViewModel[]
SUPPLIED_FIELDS_ONLY =
  runId
  startedAt / finishedAt
  state / presentation / resultLabel
  acceptedCount / rejectedCount
  storeBeforeCount / storeAfterCount
  idempotencyResult
  failureReason
  evidence
  empty list (NO_RUNS) / partial metrics via availability
NO_FABRICATED = links; timestamps; metrics; statuses; duration/trigger/host unless already in ViewModel
ACTION_HINT = advisory text only (no execute buttons)
```

## 6. Persistência e dados

Nenhuma. Assessment docs-only. Futura tela: fixture I6C apenas; sem adapters, network, filesystem runtime ou localStorage operacional.

## 7. Concorrência, locks e idempotência

N/A nesta tarefa. Futura montagem determinística via `buildFixtureViewModels`; sem clock implícito além do `nowIso` do cenário.

## 8. Segurança

```text
NO_SECRETS = true
NO_AUTH = true
NO_OPERATIONAL_COMMANDS = true
NO_REAL_DATA = true
NO_VISIBLE_FIXTURE_SELECTOR = true
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
```

## 9. Observabilidade

Sem telemetria. Assessment validado por suite backend/governance/frontend; futura tela exigirá testes unitários + axe smoke.

## 10. Operação

Não altera scheduler, host discovery, coleta, validate ou estado científico R3E. `actionHint` do ViewModel permanece consultivo.

## 11. Rollback

```text
ROLLBACK = revert assessment PR; restaurar PROJECT.md NEXT sem flags de execução true
NEVER via R3E / validate / scheduler
```

## 12. Compatibilidade

- Consome I2 tokens, I3 primitives, I5 shell/outlet, I6B Runs ViewModels, I6C fixtures, padrão de notice sintético da I6E Overview.
- Não redefine builders/fixtures/tokens.
- Overview permanece; Readiness/Host placeholders intactos.

## 13. Testes necessários

Nesta tarefa: validação de artefatos + suite UX-R1 verde.

Na futura implementação (condição):

```text
runs route renders real screen
synthetic notice visible
fixture clearly illustrative / not operational evidence
list rows for complete / fault / empty
IN_PROGRESS / UNKNOWN / EMPTY distinct from FAULT
missing counts/timestamps not zero-filled
evidence references only when supplied
no operational buttons
other routes remain placeholders (incl. Overview intact)
semantic headings / responsive / axe smoke
architecture boundary: no network/ops/scheduler/scientific imports
```

## 14. Alternativas consideradas

| Alternativa | Decisão |
|-------------|--------|
| Implementar Runs nesta tarefa | REJECTED — assessment-only |
| Exigir fidelidade B3 completa (filtros/paginação/detail) antes de autorizar | REJECTED — OVERVIEW-like increment first; B3 extras deferred |
| Autorizar Readiness antes de Runs | DEFERRED — PROJECT NEXT aponta Runs pós-Overview |
| Seletor visível de fixtures | REJECTED |
| Dados reais / API | REJECTED |
| Botões operacionais | REJECTED |
| BLOCKED por falta de fixture `in_progress` run | REJECTED — ViewModel já mapeia; fixture opcional como condição da implementação |

## 15. Riscos

| Risco | Severidade | Mitigação |
|-------|------------|-----------|
| Confundir fixture com evidência operacional | HIGH | Mandatory SyntheticDataNotice (padrão I6E) |
| Fabricar campos B3 ausentes no ViewModel | HIGH | SUPPLIED_FIELDS_ONLY; omitir duration/trigger/host |
| FAULT vs EMPTY/UNKNOWN confusão visual | HIGH | StatusBadge + presentation mapping; empty = NO_RUNS |
| Scope creep para detail/filters/pagination | MEDIUM | RUNS_SCREEN_ONLY list; B3 extras out of scope |
| actionHint virar botão operacional | MEDIUM | Advisory text only; no Button execute |
| Fixture sem run `in_progress` | LOW | Condição: implementação pode adicionar cenário sintético ou cobrir com estados existentes |

## 16. Questões abertas

```text
NONE_BLOCKING
B3_PATH_ALIAS = document /future-collection/runs as canonical code path
B3_EXTRA_FIELDS = deferred to later authorized increment
READINESS_AND_HOST = remain unauthorized
```

## 17. Decisão arquitetural recomendada

Autorizar (em tarefa futura separada) um módulo `web/src/screens/runs/` que substitui apenas o placeholder `/future-collection/runs`, consome `buildFixtureViewModels(...).runs`, reutiliza primitivos I3 + tokens I2, exibe notice sintético obrigatório, renderiza somente campos fornecidos pelo ViewModel, permanece read-only, sem seletor de fixture, sem dados reais e sem ações operacionais.

## 18. Critérios para autorizar implementação

```text
1. This impact IMPACT_ASSESSMENT_STATUS = APPROVED
2. IMPLEMENTATION_AUTHORIZED = true (assessment docs)
3. DECISION = AUTHORIZED_WITH_CONDITIONS
4. I6E Overview MERGED
5. Separate human prompt must set RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED=true for Runs only
6. This assessment does NOT flip execution flags
```

## Assessment dimensions

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Runs ViewModel readiness | READY | `RunViewModel` + `RunsViewModel` cover required supplied fields |
| Runs fixture readiness | READY_WITH_CONDITIONS | complete / fault / empty covered; no dedicated in-progress run scenario yet |
| Empty-state readiness | READY | `empty_no_runs` → `runs: []` + `NO_RUNS` |
| Partial-data readiness | READY | `OptionalMetric` / `OptionalIsoTimestamp` + `metricPresentation` keep null ≠ 0 |
| Status semantic safety | READY | complete / in_progress / fault / unknown mapped; empty distinct; NOT_READY/BLOCKED/DEFERRED ≠ FAULT |
| Responsive presentation | READY | I5 shell responsive; list layout must not break |
| Accessibility readiness | READY_WITH_CONDITIONS | I3 + shell a11y exist; Runs screen a11y required in implementation |
| Route readiness | READY | `/future-collection/runs` placeholder registered |
| Fixture/live confusion risk | MEDIUM | Mitigate with mandatory illustrative notice |
| False operational meaning risk | MEDIUM | Mitigate with synthetic labels + no fabricated fields |
| Operational action risk | LOW_IF_READ_ONLY | actionHint advisory only |

## Mandatory safety answers

1. **Can Runs render without inventing facts?** Yes — consume ViewModel fields only; missing stay null/not_supplied/absent.
2. **Are synthetic fixtures unmistakably labeled?** Yes at fixture metadata; UI must surface notice like Overview.
3. **Can COMPLETE / IN_PROGRESS / FAULT / UNKNOWN / EMPTY stay distinct?** Yes via domain+presentation mapping and empty-list `NO_RUNS`.
4. **Can missing counts/timestamps avoid fake zeroes?** Yes — null + availability; tests already assert null ≠ 0.
5. **Can evidence references stay safe?** Yes — only `toEvidenceLinks` of supplied refs; no invented links.
6. **Can the screen remain read-only?** Yes — no execute controls.
7. **Can real-data integration stay blocked?** Yes — fixtures only.
8. **Is the shell ready without architecture expansion?** Yes — replace Runs placeholder only.
9. **Are ViewModels sufficient for the bounded screen?** Yes for supplied-fields list; B3 extras deferred.
10. **What remains out of scope?** Real data, network, scheduler/collection/validate actions, auth, fixture UI selector, Readiness/Host screens, B3 filters/pagination/detail parity, fabricated B3 fields.

## Authorization decision

```text
DECISION = AUTHORIZED_WITH_CONDITIONS
```

### Conditions (C1–C12) for the next implementation task

1. **Runs only** — do not implement Readiness/Host screens in the same task; Overview remains as-is.
2. **Fixture-backed only** — wire through I6C catalog/runner; no adapters/network.
3. **Mandatory synthetic labeling** visible in UI (“Dados ilustrativos” / not operational evidence).
4. **Read-only** — no operational action buttons, forms that mutate, or command triggers; `actionHint` is advisory text only.
5. **Semantic distinctions preserved** — COMPLETE / IN_PROGRESS / FAULT / UNKNOWN / EMPTY remain distinct; NOT_READY / BLOCKED / DEFERRED never render as fault/red.
6. **No fake zeroes** — missing metrics/timestamps stay null/absent; never coerce to `0` or invented ISO times.
7. **Supplied fields only** — do not fabricate duration, trigger, host, command, filters, or evidence links.
8. **No real-data integration** — `OPERATIONAL_DATA_INTEGRATION_AUTHORIZED` remains false.
9. **Shell placeholders for other non-Runs product routes unchanged** (Readiness/Host stay placeholders).
10. **Screen a11y tests required** (WCAG 2.2 AA for Runs content).
11. **No new runtime/dev dependencies** unless separately authorized.
12. **Separate human prompt** must set `RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED=true` for Runs only; this assessment does not flip execution flags.

### Explicit out of scope

```text
REAL_DATA
NETWORK_FETCHING
SCHEDULER_ACTIONS
COLLECTION_ACTIONS
VALIDATION_ACTIONS
AUTHENTICATION
PERMISSIONS
FINANCIAL_EXECUTION
READINESS_SCREEN
HOST_SCHEDULER_SCREEN
FIXTURE_UI_PRODUCT_SELECTOR
B3_FILTERS_PAGINATION_DETAIL_PARITY
FABRICATED_B3_EXTRA_FIELDS
I6F_RUNTIME_IMPLEMENTATION_IN_THIS_TASK
```

## Next task boundary

```text
NEXT_RECOMMENDED_TASK = I6_RUNS_SCREEN_IMPLEMENTATION
NEXT_ITEM = I6_RUNS_SCREEN_SEPARATE_IMPLEMENTATION_TASK
IMPLEMENTATION_EXECUTION_AUTHORIZED = false
RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
```

## Decisão

```text
I6F_DECISION = AUTHORIZED_WITH_CONDITIONS
ASSESSMENT_STATUS = COMPLETE
READY_FOR_SEPARATE_RUNS_SCREEN_TASK = true
```
