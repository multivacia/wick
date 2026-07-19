# UX-R1-I2-DESIGN-TOKENS-AND-THEMES-IMPLEMENTATION — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = DESIGN-TOKENS-AND-THEMES-001
TASK_ID = DESIGN-TOKENS-AND-THEMES-IMPLEMENTATION-001
TITLE = Design Tokens and Themes Implementation
INCREMENT = I2
PHASE = IMPLEMENTATION
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
I2_IMPLEMENTATION_AUTHORIZED = true
I2_MERGE_AUTHORIZED = false
I3_IMPLEMENTATION_AUTHORIZED = false
I5_IMPLEMENTATION_AUTHORIZED = false
ROUTER_INSTALLATION_AUTHORIZED = false
I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
I6_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
NO_COMPONENTS = true
NO_RADIX_INSTALLATION = true
NO_SCREEN_IMPLEMENTATION = true
NO_ROUTER_INSTALLATION = true
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE_CHANGE = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
OLD_BASE_SHA = 176586469bd22a08b5d432c42ec0d097402e0ec8
NEW_BASE_SHA = 40b073471005675d2fc7784534c039d273a2ac31
BASE_SHA = 40b073471005675d2fc7784534c039d273a2ac31
ANALYZED_AT = 2026-07-19T20:14:00Z
REBASED_AT = 2026-07-19T20:31:49Z
ANALYZED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTHORIZATION_DECISION = HUMAN_AUTHORIZED_FOR_THIS_TASK
DESIGN_TOKEN_CONTRACT_VERSION = 1.0.0
FRONTEND_LOCATION = web/
NEW_RUNTIME_DEPENDENCIES = 0
PR68_STATUS = MERGED
PR68_MERGE_COMMIT = 40b073471005675d2fc7784534c039d273a2ac31
```

G1 note: `IMPLEMENTATION_AUTHORIZED=true` and `I2_IMPLEMENTATION_AUTHORIZED=true` cover **I2 token/theme CSS + minimal theme bootstrap + tests** only. They do **not** authorize I3 components, Radix, router, shell, screens, ViewModel, fixtures, or operational data.

## MANDATORY_CONSTRAINTS

```text
NO_COMPONENTS
NO_RADIX_INSTALLATION
NO_ROUTER_INSTALLATION
NO_SCREEN_IMPLEMENTATION
NO_SHELL_IMPLEMENTATION
NO_VIEWMODEL_IMPLEMENTATION
NO_FIXTURE_IMPLEMENTATION
NO_OPERATIONAL_DATA_INTEGRATION
I3_IMPLEMENTATION_AUTHORIZED = false
I5_IMPLEMENTATION_AUTHORIZED = false
ROUTER_INSTALLATION_AUTHORIZED = false
I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
I6_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
I6D_DECISION = BLOCKED
I3_PREREQUISITE_DECISION = I3_REQUIRED_BEFORE_I5_AND_I6C
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## SUMMARY

Implement the approved I2 design-token and theme foundation under `web/`: raw CSS custom properties, semantic tokens (including operational status semantics), light/dark themes, system preference resolution via a minimal bootstrap (not a CSS-in-JS theme engine), focus/motion/reduced-motion baselines, and automated token/contrast/theme tests.

Predecessor assessments (I2 contract PR #55; cross-increment auth PR #66/#67) remain binding. This task executes the human-authorized I2 code increment only.

```text
AUTHORIZED_SCOPE = raw + semantic tokens + light/dark/system themes + focus + motion + tests + docs
PROHIBITED_SCOPE = components, Radix, router, shell, screens, ViewModel, fixtures, real data
```

## 1. Objetivo

Entregar a fundação `--wick-*` v1.0.0 em `web/` com temas light/dark, resolução system, semântica de status operacional (NOT_READY ≠ ERROR; BLOCKED ≠ FAILED; SUCCESS ≠ PROFIT), contraste WCAG 2.2 AA verificável, e `prefers-reduced-motion` — sem componentes, telas ou integração de dados.

## 2. Contexto técnico

- I1 scaffold MERGED (`web/` React+TS+Vite+pnpm+Vitest+axe).
- I2 assessment MERGED (contrato `--wick-*`, `DESIGN_TOKEN_CONTRACT_VERSION=1.0.0`).
- Cross-increment auth MERGED; human task authorizes `I2_IMPLEMENTATION_AUTHORIZED=true` for this PR only.
- Scaffold hoje usa cores hardcoded em `web/src/styles.css`; I2 substitui por tokens.
- Spec assessment rejeitou CSS-in-JS theme engine; este impacto autoriza bootstrap mínimo TypeScript que apenas resolve/aplica `data-theme` no `html` (sem provider, sem store persistente obrigatória).

## 3. Componentes afetados

| Componente | Impacto |
|------------|---------|
| `web/src/styles.css` | Importa tokens; remove hardcodes de cor/foco |
| `web/src/styles/tokens/**` | Novo — raw/semantic/themes/motion |
| `web/src/theme/**` | Novo — bootstrap mínimo + contrato TS |
| `web/src/main.tsx` | Chama bootstrap de tema antes do render |
| `web/index.html` | Script mínimo anti-FOUC opcional |
| `web/tests/**` | Novos testes de tokens/tema/contraste/a11y |
| Backend / R3E / scheduler / validate | **Não afetados** |
| Governance validator source | **Não afetado** |

## 4. Arquivos previstos

```text
web/src/styles/tokens/raw.css
web/src/styles/tokens/semantic.css
web/src/styles/tokens/themes/light.css
web/src/styles/tokens/themes/dark.css
web/src/styles/tokens/motion.css
web/src/styles/tokens/index.css
web/src/styles.css (update)
web/src/theme/theme.ts
web/src/theme/contract.ts
web/src/theme/contrast.ts
web/src/main.tsx (update)
web/index.html (minimal FOUC guard)
web/tests/theme/theme.test.ts
web/tests/tokens/tokens.test.ts
web/tests/tokens/contrast.test.ts
web/tests/a11y/theme.a11y.test.tsx
docs/ai-impact/UX-R1-I2-DESIGN-TOKENS-AND-THEMES-IMPLEMENTATION_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-I2-DESIGN-TOKENS-AND-THEMES-IMPLEMENTATION_SPEC.md
docs/ai-reviews/UX-R1-I2-DESIGN-TOKENS-AND-THEMES-IMPLEMENTATION_REVIEW.md
reports/ai-implementation/UX-R1-I2-DESIGN-TOKENS-AND-THEMES-IMPLEMENTATION_HANDOFF.md
docs/PROJECT.md (status reconciliation)
```

## 5. Contratos e interfaces

```text
PREFIX = --wick-
DESIGN_TOKEN_CONTRACT_VERSION = 1.0.0
VERSION_TOKEN = --wick-design-token-contract-version
THEME_ATTR = html[data-theme="light"|"dark"]
THEME_CLASS = .wick-theme-light | .wick-theme-dark
THEME_PREFERENCE = light | dark | system
DEFAULT_THEME = light
SYSTEM_FALLBACK = matchMedia prefers-color-scheme
INVALID_THEME_FALLBACK = light
STATUS_SEMANTICS = healthy|completed|attention|not_ready|blocked|deferred|unknown|fault|informational
MERGED_SPEC_STATUS_ALIASES = normal|success|error|unavailable (aliased to prompt set)
COMPONENT_TOKENS = NOT_AUTHORIZED
```

Bootstrap API (minimal):

```text
resolveThemePreference(input) -> light|dark
applyResolvedTheme(theme) -> sets data-theme + wick-theme-* class
bootstrapTheme() -> system-aware apply before React render
```

No CSS-in-JS theme provider. No required persistence beyond optional session/local read if already present; default is system-or-light without forced storage.

## 6. Persistência e dados

Nenhuma persistência de domínio. Nenhuma tabela, migration, fixture operacional ou integração com coleta/validate. Preferência de tema: sem storage obrigatório; se lida, apenas chave de UI local não sensível.

## 7. Concorrência, locks e idempotência

N/A no backend. Bootstrap de tema é idempotente (reaplicar o mesmo `data-theme` é seguro). Testes determinísticos via preferência explícita.

## 8. Segurança

```text
NO_SECRETS_IN_CSS = true
NO_NETWORK_FONT_CDN_REQUIRED = true
CLIENT_BUNDLE = public visual constants only
NO_OPERATIONAL_DATA_IN_TOKENS = true
NO_FINANCIAL_TRADING_TOKEN_NAMES = true
```

## 9. Observabilidade

Sem telemetria nova. Versão do contrato exportada em CSS (`--wick-design-token-contract-version`) e TS (`DESIGN_TOKEN_CONTRACT_VERSION`) para testes.

## 10. Operação

Não altera scheduler, host discovery, coleta ou validate. Não ativa R4/R5. Operadores veem apenas scaffold com cores tokenizadas.

## 11. Rollback

```text
ROLLBACK =
  - revert this PR
  - restore scaffold hardcoded colors if needed
  - never roll back via R3E / validate / scheduler changes
  - token renames require MAJOR contract bump (not expected in this PR)
```

## 12. Compatibilidade

- Compatível com I1 scaffold; App placeholder permanece.
- Não quebra backend.
- I3+ deve consumir semantic tokens; raw é composição de tema.
- Desvio documentado vs assessment: bootstrap TS mínimo permitido pelo prompt de implementação humano (assessment proibia theme engine CSS-in-JS, não um setter de `data-theme`).

## 13. Testes necessários

```text
1. DESIGN_TOKEN_CONTRACT_VERSION == 1.0.0
2. Required semantic + status + focus tokens present in light and dark
3. Contrast pairs WCAG 2.2 AA (text on canvas/panel; status fg/bg)
4. Theme resolution: light, dark, system, invalid fallback
5. Reduced-motion overrides present
6. No forbidden financial/trading token names
7. Existing typecheck/lint/unit/a11y/build remain green
8. Theme a11y smoke (axe on scaffold under light and dark)
```

## 14. Alternativas consideradas

| Alternativa | Decisão |
|-------------|--------|
| Style Dictionary codegen now | REJECTED — hand-authored CSS sufficient for I2 |
| Tailwind as source of truth | REJECTED — assessment |
| Full CSS-in-JS theme engine / provider | REJECTED — assessment; minimal bootstrap only |
| Dark-only product | REJECTED — light primary |
| Component tokens in I2 | REJECTED — not authorized |
| Install color contrast npm lib | REJECTED — tiny internal relative-luminance helper |

## 15. Riscos

| Risco | Severidade | Mitigação |
|-------|------------|-----------|
| Contrast failure light/dark | MEDIUM | Automated contrast tests gate PR |
| FOUC on first paint | LOW | Tiny pre-React bootstrap + optional inline guard |
| Status color misread as P&L | MEDIUM | Naming + forbidden-token tests + docs |
| Scope creep into components | HIGH | Hard file/scope constraints; review checklist |

## 16. Questões abertas

```text
NONE_BLOCKING
HC_FULL_THEME_FILE = deferred (stronger semantic tokens first; optional later)
TOKEN_CODEGEN = deferred
```

## 17. Decisão arquitetural recomendada

Hand-authored `--wick-*` CSS layers (raw → semantic → themes + motion), light default, dark via `html[data-theme]`, system via minimal TS bootstrap, WCAG 2.2 AA contrast tests, zero new runtime dependencies, no components/Radix/router/screens.

## 18. Critérios para autorizar implementação

```text
1. This impact assessment IMPACT_ASSESSMENT_STATUS = APPROVED
2. IMPLEMENTATION_AUTHORIZED = true (this package)
3. I2_IMPLEMENTATION_AUTHORIZED = true (human task flag)
4. Scope limited to tokens/themes/bootstrap/tests/docs listed above
5. Contrast + version + status semantics tests included
6. I2_MERGE_AUTHORIZED remains false until human merge authorization
```

All criteria above are satisfied for proceeding with I2 code in this task/PR. Merge remains awaiting human authorization.
