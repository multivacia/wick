# UX-R1-I5-APPLICATION-SHELL-AND-NAVIGATION-IMPLEMENTATION — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = I5A-APPLICATION-SHELL-AND-NAVIGATION-ARCHITECTURE-001
TASK_ID = APPLICATION-SHELL-AND-NAVIGATION-IMPLEMENTATION-001
TITLE = Application Shell and Navigation Implementation
INCREMENT = I5
PHASE = IMPLEMENTATION
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
I5_IMPLEMENTATION_AUTHORIZED = true
ROUTER_INSTALLATION_AUTHORIZED = true
I5_MERGE_AUTHORIZED = false
I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
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
BASE_SHA = 8bd36372caf8519ee0f021347033f5f5267f58ff
ANALYZED_AT = 2026-07-20T12:00:00Z
ANALYZED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = PENDING
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTHORIZATION_DECISION = HUMAN_AUTHORIZED_FOR_THIS_TASK
ROUTER_PACKAGE = react-router-dom
NEW_RUNTIME_DEPENDENCIES = 1
FRONTEND_LOCATION = web/
I2_TOKEN_CONTRACT_VERSION = 1.0.0
I3_PREREQUISITE_DECISION = SATISFIED_FOR_I5_AND_I6C
```

G1 note: `IMPLEMENTATION_AUTHORIZED=true`, `I5_IMPLEMENTATION_AUTHORIZED=true`, and `ROUTER_INSTALLATION_AUTHORIZED=true` cover **I5 application shell, navigation, and react-router-dom only**. They do **not** authorize product screens, ViewModel, fixtures, or operational data.

## MANDATORY_CONSTRAINTS

```text
NO_SCREEN_CONTENT_IMPLEMENTATION
NO_VIEWMODEL_IMPLEMENTATION
NO_FIXTURE_IMPLEMENTATION
NO_OPERATIONAL_DATA_INTEGRATION
NO_AUTHENTICATION
NO_PERMISSIONS
NO_EXTRA_RUNTIME_DEPENDENCIES_BEYOND_REACT_ROUTER_DOM
TOKEN_ONLY_STYLING = true
I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
I6_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
I6D_DECISION = BLOCKED
HOST_DISCOVERY = DEFERRED
SCHEDULER_ACTIVATION = BLOCKED
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## SUMMARY

Implement the first Wick operational application shell and responsive navigation under `web/src/shell/` and route wiring under `web/src/app/`, consuming merged I2 tokens/themes and I3 primitives. Install only `react-router-dom`. Active MVP routes render neutral placeholders only — no product screens.

## 1. Objetivo

Entregar ApplicationShell, sidebar desktop, drawer mobile, TopBar, região principal, SkipLink, ThemeControl e rotas MVP com placeholders neutros, WCAG 2.2 AA, sem telas de produto, ViewModel ou dados reais.

## 2. Contexto técnico

- I3 primitives MERGED (PR #72); I3 prerequisite SATISFIED_FOR_I5_AND_I6C.
- I5A architecture MERGED (docs-only); human task flips I5 + router flags true.
- Theme API is imperative (`bootstrapTheme` / `applyResolvedTheme`); no ThemeProvider.
- Drawer primitive (Radix Dialog presentation) reused for mobile navigation.
- Divergence from I5A path names: this authorized task uses human-prompt routes (`/future-collection/*`, `/operations/host-scheduler`) instead of I5A `/collection/*` and `/ops/host`. Documented and stable for this release increment.

## 3. Componentes afetados

| Componente | Impacto |
|------------|---------|
| `web/src/App.tsx` | Substitui scaffold por router + shell |
| `web/src/app/**` | Novas rotas |
| `web/src/shell/**` | Novo chrome |
| `web/package.json` / lockfile | +`react-router-dom` |
| `web/tests/shell/**`, `web/tests/a11y/**` | Novos testes |
| Backend / R3E / scheduler | Não afetados |

## 4. Arquivos previstos

```text
web/src/app/routes.tsx
web/src/app/AppRouter.tsx
web/src/shell/**
web/src/App.tsx
web/tests/shell/**
web/tests/a11y/shell.a11y.test.tsx
docs/ai-impact/UX-R1-I5-APPLICATION-SHELL-AND-NAVIGATION-IMPLEMENTATION_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-I5-APPLICATION-SHELL-AND-NAVIGATION-IMPLEMENTATION_SPEC.md
docs/ai-reviews/UX-R1-I5-APPLICATION-SHELL-AND-NAVIGATION-IMPLEMENTATION_REVIEW.md
reports/ai-implementation/UX-R1-I5-APPLICATION-SHELL-AND-NAVIGATION-IMPLEMENTATION_HANDOFF.md
docs/PROJECT.md
```

## 5. Contratos e interfaces

```text
ROUTER_PACKAGE = react-router-dom
ACTIVE_ROUTES =
  / → /overview
  /overview
  /future-collection/runs
  /future-collection/readiness
  /operations/host-scheduler
  * → not-found
PLACEHOLDER_STATUS = planned_or_not_implemented
SIDEBAR_COLLAPSE_BEHAVIOR = hide persistent sidebar below 1024px; use mobile Drawer
MOBILE_NAV = TopBar menu + Drawer primitive
THEME = system|light|dark via existing I2 theme API
STYLING = --wick-* tokens only
```

## 6. Persistência e dados

Nenhuma. Sem adapters, fixtures, loaders, actions ou integração operacional.

## 7. Concorrência, locks e idempotência

N/A backend. Estado de menu mobile é React local; tema via atributos DOM existentes.

## 8. Segurança

```text
NO_SECRETS = true
NO_AUTH = true
LICENSE_REVIEW = MIT react-router-dom (acceptable)
pnpm audit --audit-level high required
```

## 9. Observabilidade

Sem telemetria. Testes unitários + axe smoke.

## 10. Operação

Não altera scheduler, host discovery, coleta ou validate.

## 11. Rollback

```text
ROLLBACK = revert PR; remove shell/app routes + react-router-dom; restore scaffold App
NEVER via R3E / validate / scheduler
```

## 12. Compatibilidade

- Consome I2 themes e I3 primitives; não redefine tokens nem primitivos.
- I6C Overview deve montar no outlet do shell; I5 não antecipa conteúdo de tela.

## 13. Testes necessários

```text
default redirect /
active navigation
desktop nav landmark
mobile drawer open/close/escape/close-after-nav
skip link
main landmark
theme control
not-found
keyboard + axe smoke
```

## 14. Alternativas consideradas

| Alternativa | Decisão |
|-------------|--------|
| Bottom mobile tabs (I5A sketch) | DEFERRED — human prompt requires Drawer |
| I5A path names `/collection/*` | REJECTED for this task — follow authorized prompt routes |
| Extra icon library | REJECTED |
| Data router / loaders | REJECTED |

## 15. Riscos

| Risco | Severidade | Mitigação |
|-------|------------|-----------|
| Path divergence from I5A | LOW | Documented; stable within I5 |
| Scope creep to screens | HIGH | Placeholders only + review |
| a11y drawer focus | MEDIUM | Reuse I3 Drawer/Radix |

## 16. Questões abertas

```text
NONE_BLOCKING
I5A_PATH_ALIASES = deferred; may add redirects later if product locks I5A names
```

## 17. Decisão arquitetural recomendada

`react-router-dom` nested layout; shell chrome with I3 primitives; mobile nav via Drawer; placeholders only; WCAG 2.2 AA tests; no screens/data.

## 18. Critérios para autorizar implementação

```text
1. This impact IMPACT_ASSESSMENT_STATUS = APPROVED
2. IMPLEMENTATION_AUTHORIZED = true
3. I5_IMPLEMENTATION_AUTHORIZED = true (human task)
4. ROUTER_INSTALLATION_AUTHORIZED = true (human task)
5. Scope limited to shell/nav/placeholders
6. I5_MERGE_AUTHORIZED remains false until human merge
```

All criteria satisfied for proceeding with I5 code in this task/PR.
