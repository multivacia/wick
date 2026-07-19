# UX-R1-DESIGN-SYSTEM-FOUNDATION-001 — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
TASK_ID = DESIGN-SYSTEM-FOUNDATION-001
TITLE = Design System Foundation Impact Assessment
CHANGE_RISK = MEDIUM
PHASE = IMPACT_ASSESSMENT_ONLY
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
UI_IMPLEMENTATION_AUTHORIZED = false
UX_B2_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
OLD_BASE_SHA = ef678fb92606541d0706ef408a37c0c020abe384
BASE_SHA = 223ba0c39a0b4975284d87668e2816c7f8684062
NEW_BASE_SHA = 223ba0c39a0b4975284d87668e2816c7f8684062
REBASING_STATUS = COMPLETE
CONFLICTS_RESOLVED = none
ANALYZED_AT = 2026-07-19T12:31:41Z
RECONCILED_AT = 2026-07-19T12:56:44Z
ANALYZED_BY = cursor-agent
APPROVED_BY = cursor-agent-reconciliation
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
RECOMMENDED_DECISION = APPROVED
RECOMMENDED_ARCHITECTURE = HEADLESS_PRIMITIVES_PLUS_WICK_TOKENS
```

## SUMMARY

Impacto da fundação de design system WICK, reconciliado após rebase em `main` (inclui PR #30 / B5-P1).

```text
RECOMMENDED_ARCHITECTURE = HEADLESS_PRIMITIVES_PLUS_WICK_TOKENS
ARCHITECTURE_NOTE = architectural recommendation only; no dependency install; no frontend scaffold
```

`IMPLEMENTATION_AUTHORIZED=true` (G1) significa que o **desenho** está aprovado para uma tarefa futura de implementação. **Código UI permanece proibido** até `UX_B2_IMPLEMENTATION_AUTHORIZED=true` explícito.

## CHANGES_RECONCILIATION

| Required change | Disposition | Resolution |
|-----------------|-------------|------------|
| Exact frontend repository boundary | RESOLVED | `frontend/` monorepo root; DS at `frontend/packages/wick-ds` |
| Framework strategy (no frontend today) | RESOLVED | React + TypeScript (align R5) |
| Dependency policy for headless primitives | RESOLVED | Radix UI primitives only; no full visual kit; license MIT review at install time |
| Token versioning | RESOLVED | `DESIGN_TOKEN_CONTRACT_VERSION` semver; breaking = major |
| WCAG 2.2 AA gates | RESOLVED | Mandatory merge gate for DS implementation |
| Semantic status rules | RESOLVED | Model locked below; `NOT_READY`→ATTENTION; SUCCESS≠profit |
| Fixture labeling | RESOLVED | `DEMONSTRATION DATA` mandatory |
| Sensitive data masking | RESOLVED | Default masks for secrets/env/tokens; admin-only partial paths |
| Test matrix | RESOLVED | Mandatory layers locked; visual regression phase-2 |
| Implementation increments | RESOLVED | Four increments locked in draft spec |
| Rollback and migration strategy | RESOLVED | Sections 11 + MIGRATION_STRATEGY |
| Storybook in B2 vs B3 | DEFERRED_WITH_BLOCKER | Catalog required before UX-B3 consumes DS; may ship late in B2 |
| API read-only vs fixtures-only | DEFERRED_WITH_BLOCKER | Fixtures-only for first DS/prototype; API not a B2 DS blocker |
| Option C full kit | REJECTED_WITH_RATIONALE | Trading aesthetics / P&L semantics / lock-in |

## 1. Objetivo

Produzir e reconciliar análise G1 pré-implementação para UX-B2 / `DESIGN-SYSTEM-FOUNDATION-001`, fechando condicionantes do pacote de impacto — sem código de UI.

## 2. Contexto técnico

### CURRENT_STATE

| Dimensão | Estado verificado |
|----------|-------------------|
| Frontend app | **Ausente** |
| `package.json` | Ausente |
| Framework UI | Nenhum |
| Package manager (JS) | Nenhum; Python usa **uv** |
| Build system UI | Nenhum |
| CSS strategy | Nenhum |
| Test framework | **pytest** |
| Lint/format | **ruff** |
| A11y tooling | Ausente |
| Repo shape | Monorepo Python `src/wick` |
| UX-B1 | MERGED (PR #31) |
| Main pós-rebase | Inclui PR #30 B5-P1 + post-merge handoffs |
| R5 vision | React+TS+FastAPI (não iniciado) |

```text
OLD_BASE_SHA = ef678fb92606541d0706ef408a37c0c020abe384
NEW_BASE_SHA = 223ba0c39a0b4975284d87668e2816c7f8684062
REBASING_STATUS = COMPLETE
CONFLICTS_RESOLVED = none
```

## 3. Componentes afetados

**Impacto (esta PR):** docs de impacto/spec/review/handoff + `docs/PROJECT.md` + backlog UX.

**Implementação futura (não autorizada agora):** `frontend/`, `frontend/packages/wick-ds`, tooling a11y/UI tests.

**Não afetados:** R3E científico, store, validate, scheduler, migrations.

## 4. Arquivos previstos

```text
docs/ai-impact/UX-R1-DESIGN-SYSTEM-FOUNDATION-001_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-DESIGN-SYSTEM-FOUNDATION_DRAFT_SPEC.md
docs/ai-reviews/UX-R1-DESIGN-SYSTEM-FOUNDATION_IMPACT_REVIEW.md
reports/ai-implementation/UX-R1-DESIGN-SYSTEM-FOUNDATION_IMPACT_HANDOFF.md
reports/ai-implementation/UX-R1-DESIGN-SYSTEM-FOUNDATION_FINAL-EVIDENCE_HANDOFF.md
docs/PROJECT.md
docs/ux/UX-R1_BACKLOG.md
```

## 5. Contratos e interfaces

### TOKEN_CONTRACT

```text
PREFIX = --wick-
NAMING = category.role.variant
DESIGN_TOKEN_CONTRACT_VERSION = 1.0.0 (ao criar implementação)
SEMANTIC_OVER_RAW = required
LIGHT_PRIMARY = true
DARK_SUPPORTED = true
HARDCODED_PRODUCT_COLORS = prohibited
```

Categorias: `color.background|text|border|status.*`, `space.*`, `size.*`, `radius.*`, `shadow.*`, `font.*`, `breakpoint.*`, `motion.*`, `z_index.*`.

### SEMANTIC_STATUS_MODEL

```text
NORMAL | SUCCESS | ATTENTION | BLOCKED | ERROR | UNAVAILABLE | INFORMATIONAL
```

| Status | Uso |
|--------|-----|
| ATTENTION | inclui `NOT_READY` |
| BLOCKED | gate/protocolo; não é falha automática |
| ERROR | somente falha real |
| SUCCESS | operacional completo; **não** lucro |

Canais obrigatórios: texto + ícone + SR + tooltip + contraste HC.

### REPOSITORY_BOUNDARIES (RESOLVED)

```text
REPO = multivacia/wick
FRONTEND_ROOT = frontend/
DS_PACKAGE = frontend/packages/wick-ds
JS_PACKAGE_MANAGER = pnpm
PYTHON_BACKEND = src/wick
SEPARATE_FRONTEND_REPO = false for UX-R1
```

## 6. Persistência e dados

```text
FIXTURE_POLICY = REAL_OPERATIONAL_METADATA | SAFE_FIXTURES | DEMONSTRATION_DATA
DEMONSTRATION_DATA_LABEL = mandatory on every fixture surface
PROHIBITED_IMPLICATIONS = profit | model_accuracy | readiness | scheduler_on | validate_executed
```

## 7. Concorrência, locks e idempotência

Sem locks de runtime no DS. Tokens/componentes idempotentes. Temas independentes de estado científico mutável.

## 8. Segurança

### SECURITY_AND_PRIVACY

```text
MASK_DEFAULTS = secrets | env | provider_tokens
ADMIN_PARTIAL = hostnames | usernames | filesystem_paths
LOGS = structured_no_secrets
CLIPBOARD = confirm_long_ids | never_secrets
CLIENT_BUNDLES = no_secrets
```

## 9. Observabilidade

Status/evidence first-class; sem cálculo financeiro no cliente; telemetria futura sem PII/secrets.

## 10. Operação

DS não altera coleta/scheduler. CLI permanece fonte operacional até protótipos autorizados.

## 11. Rollback

Reverter PR de implementação UI remove `frontend/` sem tocar R3E. Tokens versionados permitem rollback parcial. Rollback desta PR = reverter docs.

## 12. Compatibilidade

UX-B1, R5 React path, B5-P1/R3E científica preservados. Rebase confirmou preservação de UX-B1 MERGED e PR #30.

## IMPLEMENTATION_GATES

| Gate | STATUS | OWNER | EVIDENCE | BLOCKING_EFFECT |
|------|--------|-------|----------|-----------------|
| FRONTEND_LOCATION_DECIDED | DECIDED_IN_IMPACT | Gustavo / impact | `frontend/` | Blocks scaffold until auth |
| FRAMEWORK_DECIDED | DECIDED_IN_IMPACT | Gustavo / impact | React+TypeScript | Blocks scaffold until auth |
| PACKAGE_MANAGER_DECIDED | DECIDED_IN_IMPACT | Gustavo / impact | pnpm (JS); uv (Python) | Blocks scaffold until auth |
| HEADLESS_LIBRARY_DECIDED | DECIDED_IN_IMPACT | Gustavo / impact | Radix UI primitives | Blocks deps until auth |
| DEPENDENCY_LICENSE_REVIEWED | PENDING_AT_INSTALL | Implementer | MIT check at install | Blocks first `pnpm add` |
| ACCESSIBILITY_TEST_TOOL_DECIDED | DECIDED_IN_IMPACT | Gustavo / impact | axe-core + Testing Library + Playwright | Blocks DS merge without a11y tests |
| VISUAL_REGRESSION_TOOL_DECIDED | DEFERRED_PHASE_2 | Gustavo | Playwright screenshots later | Does not block impact; blocks “visual complete” claim |
| TOKEN_CONTRACT_APPROVED | DECIDED_IN_IMPACT | Gustavo / impact | this document §5 | Blocks token code drift |
| SEMANTIC_STATUS_MODEL_APPROVED | DECIDED_IN_IMPACT | Gustavo / impact | this document §5 | Blocks status components |
| FIXTURE_POLICY_APPROVED | DECIDED_IN_IMPACT | Gustavo / impact | §6 | Blocks unlabeled fixtures |
| SECURITY_MASKING_RULES_APPROVED | DECIDED_IN_IMPACT | Gustavo / impact | §8 | Blocks unmasked secrets in UI |
| UX_B2_IMPLEMENTATION_AUTHORIZED | false | Human | explicit auth | **Blocks all DS code** |
| UI_IMPLEMENTATION_AUTHORIZED | false | Human | explicit auth | Blocks app shell/routes/pages |

## 13. Testes necessários

### TEST_STRATEGY

Obrigatório antes do merge de implementação DS:

- unit tokens
- component tests
- a11y (axe + keyboard)
- semantic-status
- fixture-label
- scientific-state safety
- theme light/dark
- responsive smoke

Visual regression: phase-2 (Playwright).

Nesta tarefa: pytest/ruff/governance Python PASS; sem UI code.

## 14. Alternativas consideradas

### ARCHITECTURE_OPTIONS

- **A** Native tokens + lightweight — alta propriedade, a11y mais cara
- **B** Headless + WICK tokens — **recomendada**
- **C** Full external kit — **REJECTED** (casino/P&L/lock-in)

### RECOMMENDED_ARCHITECTURE

```text
RECOMMENDED_ARCHITECTURE = HEADLESS_PRIMITIVES_PLUS_WICK_TOKENS
TOKEN_LAYER = CSS_CUSTOM_PROPERTIES_FIRST
FRAMEWORK = React_TypeScript
HEADLESS = Radix_UI_primitives
REJECTED = OPTION_C_FULL_EXTERNAL_KIT
NO_DEPENDENCY_INSTALL_AUTHORIZED = true
NO_FRONTEND_SCAFFOLD_AUTHORIZED = true
```

## ACCESSIBILITY_IMPACT

```text
WCAG_TARGET = 2.2 AA
```

Keyboard, focus-visible, SR, contrast, non-color status, 200%/400% zoom, reduced motion, 44px touch, table a11y, modal focus trap, plain-language + technical expansion. Falha a11y bloqueia merge de implementação.

## RESPONSIVE_IMPACT

Desktop sidebar; tablet collapsible; mobile bottom nav (UX-B1). Table→card; wrap IDs; stacked filters/checklists; offline/local host → UNAVAILABLE/ATTENTION.

## SCIENTIFIC_SAFETY / ECONOMIC_INTERPRETATION_SAFETY

Guardrails: `NOT_READY`≠ERROR; `BLOCKED`≠crash; SUCCESS≠profit; technical layer mandatory; no fabricated economic results; demo labeled; gates visible.

## 15. Riscos

```text
RISK = implementing_ui_before_UX_B2_auth
IMPACT = HIGH
MITIGATION = UX_B2_IMPLEMENTATION_AUTHORIZED=false
RESIDUAL = LOW

RISK = status_color_only
IMPACT = HIGH
MITIGATION = mandatory multi-channel status + tests
RESIDUAL = LOW

RISK = full_ui_kit_aesthetics
IMPACT = HIGH
MITIGATION = Option C rejected
RESIDUAL = LOW
```

## 16. Questões abertas

Nenhuma questão aberta bloqueia aprovação do impacto.

Itens deferred (não bloqueiam impacto APPROVED):

1. Storybook timing (B2 late vs pré-B3) — DEFERRED_WITH_BLOCKER para consumo B3
2. API read-only timing — DEFERRED; fixtures-only suficiente para DS

## DEPENDENCIES

Futuras (install **não** autorizado nesta fase):

- react, react-dom, typescript
- @radix-ui/react-* (subset needed)
- vitest, @testing-library/react, playwright, axe-core
- pnpm workspace

Não modificar `pyproject.toml` / lockfiles Python nesta tarefa.

## MIGRATION_STRATEGY

1. Human merge of this impact PR (docs only)
2. Separate task: set `UX_B2_IMPLEMENTATION_AUTHORIZED=true`
3. Increment 1: tokens + themes + StatusBadge + DemoDataLabel
4. Increment 2: forms + Alert + Table + Progress
5. Increment 3: overlays + navigation primitives
6. Increment 4: catalog + a11y report gate
7. UX-B3 shell consumes DS

## 17. Decisão arquitetural recomendada

```text
DECISION = APPROVED
RECOMMENDED_ARCHITECTURE = HEADLESS_PRIMITIVES_PLUS_WICK_TOKENS
TOKEN_CONTRACT = CSS_SEMANTIC_FIRST
ACCESSIBILITY_TARGET = WCAG_2_2_AA
SEMANTIC_STATUS_MODEL = NORMAL|SUCCESS|ATTENTION|BLOCKED|ERROR|UNAVAILABLE|INFORMATIONAL
IMPLEMENTATION_AUTHORIZED = true
UX_B2_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
```

### CHANGE_RISK

```text
CHANGE_RISK = MEDIUM
```

## IMPLEMENTATION_BOUNDARY

**Após `UX_B2_IMPLEMENTATION_AUTHORIZED=true`:** tokens, themes, componentes DS, testes a11y, catalog.

**Ainda proibido sem flags adicionais:** app shell de domínio, routes/pages, API clients, production deploy, P&L mocks, R3E/validate/scheduler changes.

**Nesta PR:** somente documentação.

## BLOCKERS

```text
BLOCKER_1 = Human authorization to merge PR #35 (docs)
BLOCKER_2 = UX_B2_IMPLEMENTATION_AUTHORIZED=false (blocks all DS code)
BLOCKER_3 = UI_IMPLEMENTATION_AUTHORIZED=false (blocks product UI)
BLOCKER_4 = DEPENDENCY_LICENSE_REVIEWED pending at first install
```

## 18. Critérios para autorizar implementação

Código DS só após:

```text
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
UX_B2_IMPLEMENTATION_AUTHORIZED = true   # human explicit
```

Estado atual pós-reconciliação:

```text
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
UX_B2_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
```

## DECISION

```text
DECISION = APPROVED
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
UX_B2_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
```

Impacto documental aprovado com arquitetura `HEADLESS_PRIMITIVES_PLUS_WICK_TOKENS`. Implementação de código permanece não autorizada.
