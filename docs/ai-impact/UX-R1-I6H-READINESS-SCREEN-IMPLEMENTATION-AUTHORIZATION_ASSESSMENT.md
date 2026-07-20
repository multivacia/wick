# UX-R1-I6H — Readiness Screen Implementation Authorization Assessment

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
TASK_ID = READINESS-SCREEN-IMPLEMENTATION-AUTHORIZATION-ASSESSMENT-001
TITLE = Readiness Screen Implementation Authorization Assessment
INCREMENT = I6H
PHASE = AUTHORIZATION_ASSESSMENT
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
ASSESSMENT_ONLY = true
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_SCOPE = AUTHORIZATION_ASSESSMENT_DOCUMENTATION_ONLY
IMPLEMENTATION_EXECUTION_AUTHORIZED = false
DECISION = AUTHORIZED_WITH_CONDITIONS
RECOMMENDED_IMPLEMENTATION_BOUNDARY = READINESS_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; NO_VISIBLE_FIXTURE_SELECTOR; NO_REAL_DATA; NO_VALIDATION_EXECUTION; NO_COLLECTION_ACTIONS; NO_SCHEDULER_ACTIONS; NO_SCIENTIFIC_INTERPRETATION_CHANGE
SCREEN = Prontidão
ROUTE = /future-collection/readiness
RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED = true
READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED = false
HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
OPERATIONAL_ACTIONS_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
COLLECTION = IN_PROGRESS
READINESS = NOT_READY
READINESS_REASON = WINDOW_DAYS_INSUFFICIENT
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE_CHANGE = false
PR94_STATUS = MERGED
PR94_MERGE_COMMIT = 37092befdddb12125538d070c223cace58a0f1c7
PR95_STATUS = MERGED
I6_RUNS_SCREEN_IMPLEMENTATION_STATUS = MERGED
I6_OVERVIEW_SCREEN_IMPLEMENTATION_STATUS = MERGED
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 170b562a3bbd1652207b09b1e975e27fec4bbd99
ANALYZED_AT = 2026-07-20T22:25:00Z
ANALYZED_BY = cursor-agent
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
NEXT_RECOMMENDED_TASK = I6_READINESS_SCREEN_IMPLEMENTATION
NEXT_ITEM = I6_READINESS_SCREEN_SEPARATE_IMPLEMENTATION_TASK
```

G1 note: This assessment may recommend **AUTHORIZED_WITH_CONDITIONS** for a future Readiness-only screen task. It does **not** flip `READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED`, `IMPLEMENTATION_EXECUTION_AUTHORIZED`, or `UI_SCREEN_IMPLEMENTATION_AUTHORIZED` to true for product execution. Screen implementation requires a separate human-authorized implementation prompt.

## SUMMARY

Prerequisites I2, I3, I5, I6B, I6C, I6E (Overview), and I6G (Runs) are merged. The project is ready to authorize a **narrow, fixture-backed, read-only Prontidão (Readiness) screen** at `/future-collection/readiness` as the next visual product surface. Full B3 readiness dashboard parity (series completeness, gaps/duplicates, future cutoff, collection health as readiness-owned fields), real-data integration, validation execution, and operational actions are not authorized.

## 1. Objetivo

Avaliar se o projeto está pronto para autorizar uma tarefa separada de implementação da tela **Prontidão** (`/future-collection/readiness`), somente leitura e alimentada por fixtures, sem implementar a tela nesta tarefa.

## 2. Contexto técnico

- I6G Runs MERGED (PR #94 → `37092be`); post-merge closure MERGED (PR #95 → `170b562`).
- `NEXT_RECOMMENDED_TASK` em `main` aponta para `I6_READINESS_SCREEN_AUTHORIZATION_ASSESSMENT`.
- I6B `buildReadinessViewModel` MERGED; I6C fixture catalog MERGED; I5 route placeholder MERGED; Overview + Runs patterns available.
- Estado científico/operacional preservado: host discovery DEFERRED; scheduler BLOCKED; readiness NOT_READY por janela insuficiente; validation/effect-peeking false; R3E pending future unseen data; R4 BLOCKED; R5 NOT_STARTED.

## 3. Componentes afetados

| Componente | Impacto nesta tarefa |
|------------|----------------------|
| Docs I6H (impact/review/handoff) | Novos artefatos de autorização |
| `docs/PROJECT.md` | Resultado da assessment + NEXT |
| `web/src/screens/**` | Não modificado |
| Rotas / fixtures / ViewModels | Não modificados |
| Backend / R3E / scheduler | Não afetados |

## 4. Arquivos previstos

```text
docs/ai-impact/UX-R1-I6H-READINESS-SCREEN-IMPLEMENTATION-AUTHORIZATION_ASSESSMENT.md
docs/ai-reviews/UX-R1-I6H-READINESS-SCREEN-IMPLEMENTATION-AUTHORIZATION_REVIEW.md
reports/ai-implementation/UX-R1-I6H-READINESS-SCREEN-IMPLEMENTATION-AUTHORIZATION_HANDOFF.md
docs/PROJECT.md
```

Futura implementação (fora desta tarefa) tipicamente em:

```text
web/src/screens/readiness/**
web/src/app/AppRoutes.tsx  (somente /future-collection/readiness)
web/tests/screens/readiness/**
web/tests/a11y/readiness.a11y.test.tsx
```

## 5. Contratos e interfaces

```text
ROUTE_CANONICAL = /future-collection/readiness
SCREEN_LABEL = Prontidão
NAV_LABEL_TODAY = Readiness  (shell; future screen should prefer Portuguese Prontidão)
DATA_SOURCE = buildFixtureViewModels(<fixtureId>).readiness + metadata
VIEWMODEL = ReadinessViewModel
SUPPLIED_FIELDS_ONLY =
  state / presentation
  windowDays / requiredWindowDays
  blockingReasonCodes
  validationAuthorized
  validationCommandExecuted
  effectPeekingPerformed
  nextSafeAction
  evidence
NO_FABRICATED =
  future cutoff
  latest observation timestamp
  collection status
  series completeness
  accepted/rejected counts
  gaps / duplicates
  store integrity / hash / manifest
  scientific gate / R4 / R5 as readiness-owned claims
ACTION_HINT = advisory text only (no validate/collect/scheduler buttons)
SEMANTICS =
  NOT_READY != FAULT
  BLOCKED != FAULT
  UNKNOWN != ZERO
  MISSING != ZERO
  COLLECTION_IN_PROGRESS != READY
  VALIDATION_NOT_EXECUTED != VALIDATION_FAILED
  EFFECT_PEEKING_FALSE != EFFECT_NOT_REPORTED
  READY != scientific approval / profitability / validate permission
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
NO_VALIDATION_EXECUTION = true
NO_REAL_DATA = true
NO_VISIBLE_FIXTURE_SELECTOR = true
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
```

## 9. Observabilidade

Sem telemetria. Assessment validado por suite backend/governance/frontend; futura tela exigirá testes unitários + axe smoke.

## 10. Operação

Não altera scheduler, host discovery, coleta, validate ou estado científico R3E. Flags `validationCommandExecuted` / `effectPeekingPerformed` permanecem false e devem ser exibidas como tais se mostradas.

## 11. Rollback

```text
ROLLBACK = revert assessment PR; restaurar PROJECT.md NEXT sem flags de execução true
NEVER via R3E / validate / scheduler
```

## 12. Compatibilidade

- Consome I2 tokens, I3 primitives, I5 shell/outlet, I6B Readiness ViewModel, I6C fixtures, padrão de notice sintético Overview/Runs.
- Não redefine builders/fixtures/tokens.
- Overview e Runs permanecem; Host placeholder intacto.

## 13. Testes necessários

Nesta tarefa: validação de artefatos + suite UX-R1 verde.

Na futura implementação (condição):

```text
readiness route renders real screen
synthetic notice visible
fixture clearly illustrative / not operational evidence
NOT_READY renders amber/attention, never fault/red
READY (if shown) never implies validate/scientific approval
window days missing stay unavailable, never zero-filled
validationCommandExecuted=false distinct from validation failed
effectPeekingPerformed=false explicit
blocking reasons shown from supplied codes only
evidence text-only when supplied
no validate/collect/scheduler buttons
Overview and Runs remain implemented
Host remains placeholder
semantic headings / responsive / axe smoke
architecture boundary: no network/ops/scheduler/scientific imports
```

## 14. Alternativas consideradas

| Alternativa | Decisão |
|-------------|--------|
| Implementar Readiness nesta tarefa | REJECTED — assessment-only |
| Exigir fidelidade B3 completa (series/gaps/duplicates/cutoff) antes de autorizar | REJECTED — ViewModel-bounded increment first; B3 extras deferred |
| Autorizar Host/Scheduler em paralelo | REJECTED — PARALLEL_TASKS_ALLOWED=false |
| Seletor visível de fixtures | REJECTED |
| Dados reais / readiness_report.json | REJECTED |
| Botões de validate/collect/scheduler | REJECTED |
| BLOCKED por ausência de fixture READY | REJECTED — ViewModel mapeia READY; fixture READY opcional como condição da implementação |

## 15. Riscos

| Risco | Severidade | Mitigação |
|-------|------------|-----------|
| Confundir fixture com evidência operacional | HIGH | Mandatory SyntheticDataNotice |
| READY → falsa aprovação científica / “pode validar” | HIGH | Copy do builder + flags false; do_not_validate advisory |
| Fabricar campos B3 ausentes no ViewModel | HIGH | SUPPLIED_FIELDS_ONLY |
| Gauge de progresso enganoso (3/14 vs protocolo 90) | MEDIUM | Texto/métricas supplied; rotular ilustrativo; evitar gauge que sugira protocolo real |
| NOT_READY como fault/red | MEDIUM | StatusBadge not_ready/amber; tests |
| actionHint virar botão operacional | MEDIUM | Advisory text only |
| Fixture sem READY | LOW | Condição: adicionar cenário sintético ou não exigir READY nos acceptance tests |

## 16. Questões abertas

```text
NONE_BLOCKING
READY_FIXTURE = optional synthetic scenario in future implementation task
ILLUSTRATIVE_WINDOW_14_VS_PROTOCOL_90 = disclose via synthetic labeling
HOST_SCHEDULER = remain unauthorized
NAV_LABEL_PT = prefer Prontidão over English Readiness in future screen chrome
```

## 17. Decisão arquitetural recomendada

Autorizar (em tarefa futura separada) um módulo `web/src/screens/readiness/` que substitui apenas o placeholder `/future-collection/readiness`, consome `buildFixtureViewModels(...).readiness`, reutiliza primitivos I3 + tokens I2, exibe notice sintético obrigatório, renderiza somente campos fornecidos pelo ViewModel, permanece read-only, sem seletor de fixture, sem dados reais, sem execução de validate/collect/scheduler e sem mudança de interpretação científica.

## 18. Critérios para autorizar implementação

```text
1. This impact IMPACT_ASSESSMENT_STATUS = APPROVED
2. IMPLEMENTATION_AUTHORIZED = true (assessment docs)
3. DECISION = AUTHORIZED_WITH_CONDITIONS
4. I6G Runs MERGED
5. Separate human prompt must set READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED=true for Readiness only
6. This assessment does NOT flip execution flags
```

## Assessment dimensions

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Readiness ViewModel readiness | READY | Core status/window/reasons/flags/action/evidence present |
| Readiness fixture readiness | READY_WITH_CONDITIONS | NOT_READY / UNKNOWN / WINDOW_DAYS_INSUFFICIENT covered; no READY scenario in I6C yet |
| NOT_READY state safety | READY | maps to amber `not_ready`; never fault |
| READY state safety | READY_WITH_CONDITIONS | builder copy forbids validate; no READY fixture yet |
| Partial/unknown state safety | READY | `partial_unknown_data` null metrics + unknown state |
| Window-progress representation | READY_WITH_CONDITIONS | metrics available; avoid misleading protocol gauge; disclose illustrative 14≠90 |
| Blocking-reason clarity | READY | `blockingReasonCodes` + explainReasonCode |
| Scientific-governance semantics | READY | READY ≠ approval; scientificGate not owned by readiness VM |
| Validation-execution semantics | READY | `validationCommandExecuted` boolean; fixtures false |
| Effect-peeking semantics | READY | `effectPeekingPerformed` boolean; fixtures false |
| Collection-health representation | OUT_OF_SCOPE_ON_VM | collection status lives on Overview; do not fabricate |
| Evidence-reference safety | READY | text-only EvidenceLink[] |
| Responsive presentation | READY | I5 shell; follow Overview/Runs patterns |
| Accessibility readiness | READY_WITH_CONDITIONS | screen a11y required in implementation |
| Route readiness | READY | `/future-collection/readiness` placeholder registered |
| False scientific approval risk | MEDIUM_MITIGATED_BY_COPY_AND_FLAGS | |
| False operational readiness risk | MEDIUM_MITIGATED_BY_SYNTHETIC_LABELS | |
| Fixture/live confusion risk | MEDIUM_MITIGATED_BY_NOTICE | |
| Accidental execution affordance risk | LOW_IF_READ_ONLY | |

## Mandatory safety answers

1. **Can NOT_READY render without appearing as an error?** Yes — presentation `not_ready`/amber; never fault/red.
2. **Can READY render without implying strategy approval or profitability?** Yes — builder plain language explicitly denies validate authorization; still requires careful UI copy and preferably a dedicated synthetic fixture before claiming READY coverage.
3. **Can observed/required days render without a misleading gauge?** Yes — show supplied metrics as text; avoid inventing protocol progress bars; disclose illustrative window.
4. **Do missing values remain unavailable rather than zero?** Yes — `MetricPresentation` null + availability.
5. **Do validation-not-executed and validation-failed remain distinct?** Yes — boolean flag ≠ fault state; no “failed validate” invented from `false`.
6. **Do effect-peeking states remain explicit?** Yes — boolean must be shown when the field is displayed; fixtures are `false`.
7. **Can the screen remain fully read-only?** Yes — advisory `nextSafeAction` only.
8. **Do validation, collection and scheduler actions remain absent?** Yes — out of scope; no buttons.
9. **Do fixtures cover NOT_READY, READY, partial and unknown?** NOT_READY/partial/unknown yes; READY not yet in I6C — condition for implementation.
10. **Can evidence references remain text-only?** Yes — no validated safe href target on EvidenceLink.

## Authorization decision

```text
DECISION = AUTHORIZED_WITH_CONDITIONS
```

### Conditions (C1–C13) for the next implementation task

1. **Readiness only** — do not implement Host/Scheduler; leave Overview/Runs as-is.
2. **Fixture-backed only** — I6C catalog; no real readiness_report adapters/network.
3. **Mandatory synthetic labeling** visible in UI.
4. **Read-only** — no validate/collect/scheduler controls; `nextSafeAction` advisory text only.
5. **Semantic distinctions preserved** — NOT_READY ≠ FAULT; BLOCKED ≠ FAULT; UNKNOWN/MISSING ≠ ZERO; VALIDATION_NOT_EXECUTED ≠ VALIDATION_FAILED; EFFECT_PEEKING_FALSE explicit; READY ≠ scientific approval.
6. **No fake zeroes** — missing window metrics stay unavailable.
7. **Supplied ReadinessViewModel fields only** — do not fabricate cutoff, observation timestamp, collection status, series completeness, accepted/rejected, gaps/duplicates.
8. **No real-data integration** — `OPERATIONAL_DATA_INTEGRATION_AUTHORIZED` remains false.
9. **No validation execution / effect peeking** — flags remain false; do not execute commands.
10. **Host placeholder unchanged**.
11. **Screen a11y tests required** (WCAG 2.2 AA).
12. **No new runtime/dev dependencies** unless separately authorized.
13. **Separate human prompt** must set `READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED=true` for Readiness only; this assessment does not flip execution flags. READY fixture may be added only inside that implementation task if needed.

### Explicit out of scope

```text
REAL_DATA
NETWORK_FETCHING
VALIDATION_EXECUTION
COLLECTION_ACTIONS
SCHEDULER_ACTIONS
SCIENTIFIC_INTERPRETATION_CHANGE
AUTHENTICATION
PERMISSIONS
FINANCIAL_EXECUTION
HOST_SCHEDULER_SCREEN
FIXTURE_UI_PRODUCT_SELECTOR
B3_SERIES_GAPS_DUPLICATES_CUTOFF_PARITY
FABRICATED_COLLECTION_HEALTH_ON_READINESS
I6H_RUNTIME_IMPLEMENTATION_IN_THIS_TASK
```

## Next task boundary

```text
NEXT_RECOMMENDED_TASK = I6_READINESS_SCREEN_IMPLEMENTATION
NEXT_ITEM = I6_READINESS_SCREEN_SEPARATE_IMPLEMENTATION_TASK
IMPLEMENTATION_EXECUTION_AUTHORIZED = false
READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
```

## Decisão

```text
I6H_DECISION = AUTHORIZED_WITH_CONDITIONS
ASSESSMENT_STATUS = COMPLETE
READY_FOR_SEPARATE_READINESS_SCREEN_TASK = true
```
