# UX-R1 — I2 / I3 / I5 / I6 Implementation Authorization — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
TASK_ID = I2-I5-I6-IMPLEMENTATION-AUTHORIZATION-ASSESSMENT-001
TITLE = Cross-increment Implementation Authorization Assessment
PHASE = IMPLEMENTATION_AUTHORIZATION_ASSESSMENT
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_SCOPE = AUTHORIZATION_ASSESSMENT_DOCUMENTATION_ONLY
ASSESSMENT_ONLY = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = false
DECISION_REQUIRED = true
MERGE_AUTHORIZED = false
I2_IMPLEMENTATION_AUTHORIZED = false
I3_IMPLEMENTATION_AUTHORIZED = false
I5_IMPLEMENTATION_AUTHORIZED = false
ROUTER_INSTALLATION_AUTHORIZED = false
I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
I6_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = f4e43a6a96fe13d27566c9beded7a442428bd3b1
ANALYZED_AT = 2026-07-19T19:18:37Z
ANALYZED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTOMATIC_MERGE_AUTHORIZED = false
REVIEW_STATUS = APPROVED
I2_DECISION = AUTHORIZED_WITH_CONDITIONS
I3_DECISION = AUTHORIZED_WITH_CONDITIONS
I3_PREREQUISITE_DECISION = I3_REQUIRED_BEFORE_I5_AND_I6C
I5_DECISION = AUTHORIZED_WITH_CONDITIONS
I6B_DECISION = AUTHORIZED_WITH_CONDITIONS
I6C_DECISION = AUTHORIZED_WITH_CONDITIONS
I6D_DECISION = BLOCKED
NEXT_RECOMMENDED_TASK = I2_DESIGN_TOKENS_AND_THEMES_IMPLEMENTATION
```

## Objetivo

Avaliar, de forma independente e cross-increment, quais incrementos executáveis UX-R1 podem ser autorizados a seguir, sem implementar nenhum deles nesta tarefa.

Incrementos avaliados separadamente:

```text
I2  = design tokens and themes implementation
I3  = minimum accessible primitives required by shell/screen
I5  = router installation plus application shell/navigation
I6B = typed ViewModel plus executable demonstration fixtures
I6C = Visão Geral screen using demonstration fixtures only
I6D = operational/real-data integration
```

Esta avaliação **não** autoriza execução de código. Flags de implementação permanecem `false` até tarefas humanas separadas.

## Contexto técnico

Pré-requisitos já mergeados em `main`:

```text
I1_IMPLEMENTATION_STATUS = MERGED
I2_STATUS = ASSESSMENT_MERGED
I2_AUTHORIZATION_DECISION = AUTHORIZED_WITH_CONDITIONS
I2_SOURCE_PR = 55
I5A_STATUS = ARCHITECTURE_MERGED
I5_ARCHITECTURE_DECISION = AUTHORIZED_WITH_CONDITIONS
I5_SOURCE_PR = 56
I6A_STATUS = DATA_PREPARATION_MERGED
I6_DATA_CONTRACT_DECISION = AUTHORIZED_WITH_CONDITIONS
I6_SOURCE_PR = 57
PR57_MERGE_COMMIT = 4bf15db0fe7be32228cfd585561a0f49ece10c3b
MAIN_TIP_AT_ASSESSMENT = f4e43a6a96fe13d27566c9beded7a442428bd3b1
```

Documentação mergeada **não** implica autorização de execução. Sequência proposta avaliada:

```text
STEP_1 = I2 tokens/themes
STEP_2 = I3 minimum accessible primitives
STEP_3 = I5 router + shell/navigation
STEP_4 = I6B typed ViewModel + demonstration fixtures
STEP_5 = I6C Visão Geral with demonstration fixtures
STEP_6 = I6D read-only operational-data adapter/integration
```

## Componentes afetados

```text
AFFECTED_NOW = documentation only (impact, spec, review, handoff, PROJECT.md)
AFFECTED_FUTURE_I2 = web/src/styles/tokens/*, web/src/styles/themes/*, token tests
AFFECTED_FUTURE_I3 = web component primitives (+ optional Radix subset)
AFFECTED_FUTURE_I5 = react-router, shell, navigation, landmarks, boundaries
AFFECTED_FUTURE_I6B = Overview ViewModel types + synthetic fixtures
AFFECTED_FUTURE_I6C = Overview screen (fixtures only)
AFFECTED_FUTURE_I6D = operational index adapter (blocked)
UNAFFECTED = src/wick scientific pipeline, Alembic, scheduler, validate, collection
```

## Arquivos previstos

Nesta tarefa (somente documentação):

```text
docs/ai-impact/UX-R1-I2-I3-I5-I6_IMPLEMENTATION-AUTHORIZATION_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-I2-I3-I5-I6_IMPLEMENTATION-AUTHORIZATION_SPEC.md
docs/ai-reviews/UX-R1-I2-I3-I5-I6_IMPLEMENTATION-AUTHORIZATION_REVIEW.md
reports/ai-implementation/UX-R1-I2-I3-I5-I6_IMPLEMENTATION-AUTHORIZATION_HANDOFF.md
docs/PROJECT.md
```

Nenhum arquivo Python, TypeScript, CSS, JSON runtime, dependência ou CI nesta PR.

## Contratos e interfaces

Contratos já mergeados consumidos por esta avaliação:

```text
I2_TOKEN_CONTRACT = docs/ai-specs/UX-R1-I2-DESIGN-TOKENS-AND-THEMES_SPEC.md
I5A_SHELL_CONTRACT = docs/ai-specs/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_SPEC.md
I6A_VIEWMODEL = docs/ux/UX-R1-I6A-OVERVIEW-VIEWMODEL-CONTRACT.md
I6A_FIXTURES = docs/ux/UX-R1-I6A-OVERVIEW-FIXTURE-SCENARIOS.md
B3_SCREEN_CONTRACTS = docs/ai-specs/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS_SPEC.md
B4_LANGUAGE = docs/ux/UX-R1-OPERATIONAL-LANGUAGE-GUIDE.md
```

Interfaces futuras (não implementadas aqui): token CSS `--wick-*`, React Router route registry, OverviewViewModel TypeScript, fixture modules, read-only operational adapter.

## Persistência e dados

```text
PERSISTENCE_CHANGE = none
DATABASE_MIGRATION = none
OPERATIONAL_INDEX = not built
REAL_DATA_READ = not authorized
FIXTURE_DATA = synthetic documentation only until I6B
HOST_DISCOVERY = DEFERRED
```

## Concorrência, locks e idempotência

```text
CONCURRENCY_IMPACT = none in this assessment
IMPLEMENTATION_LOCK = one executable increment at a time until I2 lands
PARALLEL_DOCS_OK = true
PARALLEL_CODE_TASKS_ALLOWED = false until NEXT_RECOMMENDED_TASK merges
IDEMPOTENT_ASSESSMENT = true (docs-only re-run safe)
```

## Segurança

```text
NO_SECRETS_IN_CLIENT = required for all future increments
NO_WRITE_OPERATIONS_FROM_UI = required through I6C
I6D_FILESYSTEM_SAFETY = required before any real-data adapter
MASK_HOST_PATHS = required if paths ever surface in UI
NO_CREDENTIAL_LEAK_IN_FIXTURES = true
```

## Observabilidade

Futuros incrementos devem preservar evidência operacional sem interpretação científica:

```text
FRESHNESS_VISIBLE = required for I6B/I6C/I6D
PROVENANCE_VISIBLE = required for I6B/I6C/I6D
DADOS_DEMONSTRATIVOS_LABEL = required for fixtures and fixture-backed UI
RUN_ID_SURFACING = when execution metadata exists
```

## Operação

```text
SCHEDULER_ACTIVATION = BLOCKED
COLLECTION_COMMAND = not invoked by UI
VALIDATE_COMMAND = not invoked by UI
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
R3E_SCIENTIFIC_STATE = UNCHANGED
```

## Rollback

```text
THIS_ASSESSMENT_ROLLBACK = revert docs PR
I2_ROLLBACK = remove token/theme CSS + tests
I3_ROLLBACK = remove primitives package slice
I5_ROLLBACK = remove router dependency + shell routes
I6B_ROLLBACK = remove ViewModel/fixture modules
I6C_ROLLBACK = remove Overview screen route/component
I6D_ROLLBACK = N/A while BLOCKED
```

## Compatibilidade

```text
I1_SCAFFOLD = compatible (web/ exists)
I2_ASSESSMENT = compatible (C1-C8 preserved)
I5A_ARCHITECTURE = compatible (react-router recommendation preserved)
I6A_DATA_CONTRACT = compatible (17 field groups + 8 scenarios preserved)
B3_B4 = consumed, not rewritten
PYTHON_CI = unchanged by this assessment
```

## Testes necessários

Nesta tarefa: suites existentes devem permanecer verdes (pytest, ruff, governance validator, web typecheck/lint/test/a11y/build).

Futuros incrementos exigem testes próprios (token contrast/semantics; primitive a11y; router landmarks; fixture schema; screen states; adapter read-only). Detalhe na spec.

## Alternativas consideradas

```text
ALT_1 = authorize monolithic I2+I3+I5+I6C PR
REJECTED = blast radius, review failure, governance ambiguity

ALT_2 = start with I6C screen first
REJECTED = missing tokens, primitives, shell, ViewModel; premature UI

ALT_3 = start with I5 router before I2/I3
REJECTED = shell without tokens/primitives increases redesign and a11y debt

ALT_4 = authorize I6D now
REJECTED = no host discovery result; no operational index; B3 data access still recommendation-only

ALT_5 = authorize I2 implementation task next
SELECTED = lowest dependency risk, smallest reviewable scope, foundational value
```

## Riscos

| RISK_ID | SEVERITY | TRIGGER | MITIGATION | OWNER | BLOCKING |
|---------|----------|---------|------------|-------|----------|
| R01_DESIGN_SYSTEM_DRIFT | HIGH | implement screens before tokens | I2 before I5/I6C | RELEASE_OWNER | true for I5/I6C |
| R02_PREMATURE_COMPONENT_COUPLING | HIGH | ad-hoc DOM in shell/screen | require I3 minimum primitives | RELEASE_OWNER | true for I5/I6C |
| R03_ROUTER_LOCKIN | MEDIUM | install router without pin/audit | I5 C3 pin+license before install | RELEASE_OWNER | true for I5 |
| R04_A11Y_REGRESSION | HIGH | color-only status / missing landmarks | WCAG 2.2 AA gates on I2/I3/I5/I6C | RELEASE_OWNER | true |
| R05_SEMANTIC_STATUS_DRIFT | HIGH | READY=validate / SUCCESS=profit | B4 guardrails + I2 C5 + I6A C5 | RELEASE_OWNER | true |
| R06_FIXTURE_REAL_DIVERGENCE | MEDIUM | fixtures diverge from future adapter | versioned ViewModel; I6D separate | RELEASE_OWNER | false now |
| R07_STALE_DATA_MISREP | HIGH | stale shown as healthy | freshness/provenance required | RELEASE_OWNER | true for I6C/I6D |
| R08_SCIENTIFIC_OVERCLAIM | CRITICAL | UI implies gate/economic success | SCIENTIFIC_INTERPRETATION_ALLOWED=false | RELEASE_OWNER | true |
| R09_ECONOMIC_OVERCLAIM | CRITICAL | financial return claims in UI | ECONOMIC_INTERPRETATION_ALLOWED=false | RELEASE_OWNER | true |
| R10_GOVERNANCE_FLAG_AMBIGUITY | HIGH | docs auth confused with runtime auth | scoped IMPLEMENTATION_AUTHORIZED + runtime flags false | RELEASE_OWNER | true |
| R11_LARGE_PR_BLAST_RADIUS | HIGH | multi-increment PR | one increment per implementation task | RELEASE_OWNER | true |
| R12_PARALLEL_IMPL_CONFLICTS | MEDIUM | parallel code streams on web/ | PARALLEL_TASKS_ALLOWED=false until I2 merges | RELEASE_OWNER | true now |

## Questões abertas

```text
Q1 = Exact I3 minimum primitive set freeze for I5 (Dialog vs Drawer timing) — non-blocking for I2
Q2 = Whether I6B may start immediately after I2 merges in parallel with I3 — deferred to post-I2 reassessment
Q3 = Operational index schema version for I6D — blocked until host discovery path exists
Q4 = ESLint vs Biome already chosen in I1 — no open decision for this assessment
```

## Decisão arquitetural recomendada

```text
DECOMPOSITION = non-monolithic stepped authorization
ROUTER_BELONGS_TO = I5_IMPLEMENTATION
I3_PREREQUISITE_DECISION = I3_REQUIRED_BEFORE_I5_AND_I6C
NEXT_RECOMMENDED_TASK = I2_DESIGN_TOKENS_AND_THEMES_IMPLEMENTATION
I6D_DECISION = BLOCKED
ALL_RUNTIME_FLAGS_REMAIN_FALSE = true
```

## Critérios para autorizar implementação

Nenhuma implementação de código é autorizada por este documento sozinho. Para cada incremento futuro:

```text
1. Human merges this authorization assessment (docs)
2. Separate implementation task is opened for exactly one increment
3. Explicit PROJECT flag flip for that increment (human)
4. Conditions from predecessor C1-C8 plus this matrix OPEN_CONDITIONS satisfied
5. CI green on the implementation PR
6. No scientific/economic overclaim; no scheduler/validate/collection activation
```

Até lá:

```text
I2_IMPLEMENTATION_AUTHORIZED = false
I3_IMPLEMENTATION_AUTHORIZED = false
I5_IMPLEMENTATION_AUTHORIZED = false
ROUTER_INSTALLATION_AUTHORIZED = false
I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
I6_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
```

## Dependency graph

```text
I2 -> I3
I2 -> I5
I3 -> I5
I2 -> I6C
I3 -> I6C
I5 -> I6C
I6B -> I6C
I6C -> I6D
B3_DATA_ACCESS -> I6D
B4_SEMANTIC_LANGUAGE -> I6B / I6C / I6D
```

```text
ROUTER_INSTALLATION = belongs to I5_IMPLEMENTATION only (not I2, not I6)
I3_MANDATORY_BEFORE_SHELL_OR_SCREEN = true (minimum accessible primitives)
I6B_CAN_BE_PURE_TS = true (no router required), but status token snapshots prefer I2 first
```

## Authorization matrix

| INCREMENT | SCOPE | PREREQUISITES | DECISION | OPEN_CONDITIONS | SEPARATE_TASK_REQUIRED | HUMAN_AUTHORIZATION_REQUIRED | IMPLEMENTATION_FLAG_REMAINS_FALSE |
|-----------|-------|---------------|----------|-----------------|------------------------|------------------------------|-----------------------------------|
| I2 | tokens/themes/CSS vars/tests | I1 merged; I2 assessment merged | AUTHORIZED_WITH_CONDITIONS | I2 C2-C8; no components/router/screens | true | true | true |
| I3 | minimum primitives listed below | I2 implementation merged | AUTHORIZED_WITH_CONDITIONS | I3 scope freeze; Radix license for needed primitives | true | true | true |
| I5 | react-router + shell/nav/a11y chrome | I2+I3 merged; I5A architecture merged | AUTHORIZED_WITH_CONDITIONS | I5A C2-C8; router pin/audit | true | true | true |
| I6B | typed ViewModel + 8 synthetic fixtures | I6A merged; prefer I2 for status tokens | AUTHORIZED_WITH_CONDITIONS | I6A C3-C5; DADOS_DEMONSTRATIVOS | true | true | true |
| I6C | Visão Geral fixtures-only screen | I2+I3+I5+I6B | AUTHORIZED_WITH_CONDITIONS | I6A C2/C6; no real data | true | true | true |
| I6D | read-only operational adapter | I6C + B3 index + host path | BLOCKED | host discovery; index schema; security review | true | true | true |

## Per-increment assessment summaries

### I2

```text
I2_DECISION = AUTHORIZED_WITH_CONDITIONS
ALLOWED_LABEL = AUTHORIZED_FOR_I2_IMPLEMENTATION_TASK
COVERAGE = token source format, raw/semantic tokens, light/dark themes, status semantics, focus tokens, contrast, motion/reduced-motion, CSS output strategy, versioning/deprecation, test strategy, rollback
SAFEGUARDS = NOT_READY!=ERROR; BLOCKED!=FAILED; READY!=VALIDATION_AUTHORIZED; GREEN=healthy/completed only; AMBER=attention/not-ready; PURPLE_OR_GRAY=blocked/deferred/unknown; RED=confirmed fault only; COLOR_IS_NOT_SOLE_MEANING=true
I2_IMPLEMENTATION_AUTHORIZED = false until separate human-authorized I2 implementation task
```

### I3

```text
I3_PREREQUISITE_DECISION = I3_REQUIRED_BEFORE_I5_AND_I6C
I3_DECISION = AUTHORIZED_WITH_CONDITIONS
MINIMUM_SET = Button, Link, StatusBadge, Card, Stack, Inline, PageHeader, Section, Alert, Skeleton, Dialog_or_Drawer_Primitive, FocusTrap_Primitive, VisuallyHidden
RADIX_NOW = partial — only for Dialog/FocusTrap/VisuallyHidden as needed; defer full Radix suite
NO_RADIX_INSTALL_IN_THIS_ASSESSMENT = true
I3_IMPLEMENTATION_AUTHORIZED = false
```

### I5

```text
I5_DECISION = AUTHORIZED_WITH_CONDITIONS
ROUTER_RECOMMENDATION = react-router
ASSESS = ROUTER_INSTALLATION, ROUTE_REGISTRY, APPLICATION_SHELL, DESKTOP_NAVIGATION, MOBILE_NAVIGATION, SKIP_LINK, LANDMARKS, FOCUS_RESTORATION, DOCUMENT_TITLE, NOT_FOUND, ERROR_BOUNDARY, LOADING_BOUNDARY
I5_IMPLEMENTATION_AUTHORIZED = false
ROUTER_INSTALLATION_AUTHORIZED = false
```

### I6B

```text
I6B_DECISION = AUTHORIZED_WITH_CONDITIONS
SCOPE = typed Overview ViewModel + eight synthetic fixtures + validation + freshness/provenance + unknown/partial/stale + safe next-action codes
FIXTURES = healthy_collection_not_ready, collection_warning, collection_failure, host_discovery_deferred, scheduler_not_activated, readiness_ready_but_validation_not_authorized, no_execution_history, partial_metadata
REQUIRED_LABELS = DADOS_DEMONSTRATIVOS=true; SOURCE=SYNTHETIC; SCIENTIFIC_INTERPRETATION_ALLOWED=false; ECONOMIC_INTERPRETATION_ALLOWED=false
I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
I6_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
```

### I6C

```text
I6C_DECISION = AUTHORIZED_WITH_CONDITIONS
BOUNDARIES = no real-data adapter; no collection; no validate; no scheduler; no scientific conclusion; no financial claims; no editable operational actions
UX_STATES = loading, empty, partial, stale, healthy, attention, blocked, error
A11Y = WCAG_2_2_AA, keyboard, SR status, status_not_color_only, heading hierarchy, reduced motion, responsive
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
```

### I6D

```text
I6D_DECISION = BLOCKED
REASON = no real host discovery result; operational index not built; B3 data access remains recommendation-only; security/privacy/filesystem review incomplete
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
HOST_DISCOVERY = DEFERRED
SCHEDULER_ACTIVATION = BLOCKED
```

## Next recommended task

```text
NEXT_RECOMMENDED_TASK = I2_DESIGN_TOKENS_AND_THEMES_IMPLEMENTATION
NEXT_TASK_SCOPE = web token/theme CSS (--wick-*), light/dark themes, status/focus/motion tokens, token unit tests; no components, no Radix, no router, no screens
NEXT_TASK_RISK = MEDIUM
NEXT_TASK_PREREQUISITES = human merge of this assessment; explicit I2_IMPLEMENTATION_AUTHORIZED=true on separate I2 implementation task; preserve I2 C3-C8
NEXT_TASK_PROHIBITED_ACTIONS = components; Radix; router; shell; screens; fixtures TS; real data; scheduler; validate; collection; scientific/economic claims
PARALLEL_TASKS_ALLOWED = false
```

## Summary decision

```text
ASSESSMENT_DECISION = APPROVED_FOR_HUMAN_MERGE_OF_DOCUMENTATION
IMPLEMENTATION_EXECUTION_AUTHORIZED = false
MONOLITHIC_IMPLEMENTATION = NOT_AUTHORIZED
NEXT = I2 only (separate future task)
```
