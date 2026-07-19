# UX-R1-I2-DESIGN-TOKENS-AND-THEMES — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = DESIGN-SYSTEM-FOUNDATION-001
TASK_ID = DESIGN-TOKENS-AND-THEMES-001
TITLE = Design Tokens and Themes Assessment and Specification
INCREMENT = I2
PHASE = AUTHORIZATION_AND_SPECIFICATION
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
I2_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
UX_B2_IMPLEMENTATION_AUTHORIZED = false
NO_TOKEN_IMPLEMENTATION = true
NO_THEME_IMPLEMENTATION = true
NO_COMPONENTS = true
NO_RADIX_INSTALLATION = true
NO_SCREEN_IMPLEMENTATION = true
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE_CHANGE = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 221aacc7141697403e9bbbc9f8690953b683e3a9
ANALYZED_AT = 2026-07-19T16:54:33Z
ANALYZED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTHORIZATION_DECISION = AUTHORIZED_WITH_CONDITIONS
FRONTEND_LOCATION = web/
DESIGN_TOKEN_CONTRACT_VERSION = 1.0.0
```

Nota G1: `IMPLEMENTATION_AUTHORIZED=true` autoriza **somente** este pacote documental (impacto + spec + review + handoff + status `I2_STATUS`). **Não** autoriza CSS de tokens, temas, componentes, Radix, telas ou qualquer código em `web/src`. `I2_IMPLEMENTATION_AUTHORIZED=false` permanece vinculante até flip humano explícito pós-merge.

## MANDATORY_CONSTRAINTS

```text
NO_TOKEN_IMPLEMENTATION
NO_THEME_IMPLEMENTATION
NO_COMPONENTS
NO_RADIX_INSTALLATION
NO_SCREEN_IMPLEMENTATION
I2_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## SUMMARY

Avaliação e especificação do incremento I2 (design tokens e temas) do Design System WICK. **Nenhum arquivo de token CSS, tema, componente ou dependência UI é criado nesta tarefa.**

Predecessor: I1 scaffold MERGED em `web/` (PR #51). Autorização B2 permanece `AUTHORIZED_FOR_INCREMENT_I1_ONLY` para código além do assessment; I2 código exige flip humano de `I2_IMPLEMENTATION_AUTHORIZED` após merge deste pacote.

```text
AUTHORIZATION_DECISION = AUTHORIZED_WITH_CONDITIONS
AUTHORIZED_SCOPE_THIS_PR = docs assessment + specification only
CODE_IMPLEMENTATION = NOT_AUTHORIZED
```

## PREDECESSOR_STATE

```text
I1_IMPLEMENTATION_STATUS = MERGED
I1_PR = 51
I1_MERGE_COMMIT = c283592 (ancestor of main tip)
MAIN_TIP_AT_ASSESSMENT = 221aacc7141697403e9bbbc9f8690953b683e3a9
FRONTEND_LOCATION = web/ (locked by I1; supersedes earlier frontend/ plan for path only)
WEB_SCAFFOLD = present (React+TS+Vite+pnpm+ESLint+Vitest+axe harness)
TOKEN_CSS = absent
RADIX = not installed
I2_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
VISUAL_DIRECTION = docs/ux/WICK_VISUAL_DIRECTION.md ACTIVE
DRAFT_DS_SPEC = docs/ai-specs/UX-R1-DESIGN-SYSTEM-FOUNDATION_DRAFT_SPEC.md
AUTH_IMPACT = docs/ai-impact/UX-R1-DESIGN-SYSTEM-IMPLEMENTATION-AUTHORIZATION_IMPACT_ASSESSMENT.md
```

## 1. Objetivo

Especificar o contrato de design tokens e temas (raw → semantic → component boundary), temas light/dark, semântica de status, tipografia, espaçamento, raios, sombras, motion, breakpoints, z-index, foco e contraste WCAG 2.2 AA — e definir critérios para autorizar a implementação I2 futura — **sem implementar código**.

## 2. Contexto técnico

### CURRENT_STATE

| Dimensão | Estado verificado |
|----------|-------------------|
| Frontend root | `web/` (I1) |
| Stack | React 19 + TypeScript strict + Vite + pnpm 10 + Node 22 |
| CSS atual | `web/src/styles.css` scaffold-only (hardcoded hex; sem `--wick-*`) |
| Tokens `--wick-*` | Ausentes |
| Temas light/dark | Ausentes |
| Radix | Não instalado |
| Componentes DS | Ausentes |
| Python/R3E | Inalterado |
| CI frontend | Job additive em paths `web/**` |

### ALIGNMENT

- `docs/ux/WICK_VISUAL_DIRECTION.md` — paleta semântica, light primary / dark supported, proibições casino/P&L
- `docs/ai-specs/UX-R1-DESIGN-SYSTEM-FOUNDATION_DRAFT_SPEC.md` — TOKEN_LAYER CSS custom properties
- Authorization impact I2 scope — `--wick-*`, light/dark, contrast tests, `DESIGN_TOKEN_CONTRACT_VERSION`
- `FRONTEND_LOCATION = web/` (não `frontend/`)

## 3. Componentes afetados

**Esta PR (docs):** artefatos de impacto/spec/review/handoff + linha `I2_STATUS` em `docs/PROJECT.md`.

**Implementação futura I2 (não nesta PR):** arquivos de tokens/temas sob `web/` (ex.: `web/src/styles/tokens/`, ou pacote `web/packages/wick-ds` se criado na tarefa I2), testes de contraste/versão, política anti-hardcode.

**Não afetados:** `src/wick` científico, Alembic, validate, readiness, scheduler, coleta, Radix installs, componentes, rotas/telas.

## 4. Arquivos previstos

### Nesta tarefa (somente docs)

```text
docs/ai-impact/UX-R1-I2-DESIGN-TOKENS-AND-THEMES_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-I2-DESIGN-TOKENS-AND-THEMES_SPEC.md
docs/ai-reviews/UX-R1-I2-DESIGN-TOKENS-AND-THEMES_REVIEW.md
reports/ai-implementation/UX-R1-I2-DESIGN-TOKENS-AND-THEMES_HANDOFF.md
docs/PROJECT.md  (ADD I2_STATUS = ASSESSMENT_IN_PROGRESS only)
```

### Previstos para implementação I2 futura (após I2_IMPLEMENTATION_AUTHORIZED=true)

```text
web/src/styles/tokens/raw.css
web/src/styles/tokens/semantic.css
web/src/styles/tokens/themes/light.css
web/src/styles/tokens/themes/dark.css
web/src/styles/tokens/motion.css
web/src/styles/tokens/index.css
web/tests/tokens/*.test.ts (version + required keys + contrast)
```

Caminhos exatos podem ajustar layout interno desde que o contrato `--wick-*` e a versão permaneçam estáveis. **Nenhum destes arquivos é criado agora.**

## 5. Contratos e interfaces

### DESIGN_TOKEN_CONTRACT

```text
PREFIX = --wick-
NAMING = category-role-variant (CSS custom properties; kebab after prefix)
DESIGN_TOKEN_CONTRACT_VERSION = 1.0.0
SOURCE_FORMAT = CSS custom properties (hand-authored in I2)
OPTIONAL_JSON_SOURCE = deferred (Style Dictionary non-blocking)
SEMANTIC_OVER_RAW = required for product UI consumption
PROHIBITED_IN_COMPONENTS = raw hex/rgb/hsl product colors (must use tokens)
THEME_SWITCHING = html[data-theme="light"|"dark"] or .wick-theme-light|.wick-theme-dark
NO_SCIENTIFIC_STATE_COUPLING = themes must not read readiness/validate/scheduler state
```

### TOKEN_LAYERS

| Layer | Role | Consumers |
|-------|------|-----------|
| Raw | scales (palette steps, space steps, type sizes) | only semantic/theme files |
| Semantic | background/text/border/status/focus/surface | components (preferred) |
| Component | optional thin slot mapping | foundation components (I3+); not required in I2 |

### STATUS_SEMANTICS (binding)

```text
NORMAL | SUCCESS | ATTENTION | BLOCKED | ERROR | UNAVAILABLE | INFORMATIONAL
```

| Status | Visual direction | Binding rule |
|--------|------------------|--------------|
| NORMAL | neutro / surface default | estado padrão operacional |
| SUCCESS | verde moderado (`complete`/`healthy`) | conclusão operacional; **SUCCESS ≠ lucro / P&L** |
| ATTENTION | âmbar | inclui `NOT_READY`; nunca ERROR por default |
| BLOCKED | roxo discreto ou cinza forte | gate/protocolo; **BLOCKED ≠ crash automático** |
| ERROR | vermelho | **somente falha real** operacional/científica |
| UNAVAILABLE | cinza | ausência / N/A |
| INFORMATIONAL | ciano discreto / accent | informação sem alarme |

Canais obrigatórios (I3+/I4 enforcement; I2 fornece tokens): cor + contraste AA; componentes futuros exigem texto + ícone + SR (não cor-only).

### THEMES

```text
LIGHT_THEME = primary default
DARK_THEME = supported functional parity (not gamer neon)
HIGH_CONTRAST = considerations via stronger border/text/status tokens (not a third brand)
```

### A11Y_CONTRACT

```text
WCAG_TARGET = 2.2 AA
CONTRAST_TEXT = >= 4.5:1 normal text; >= 3:1 large text / UI components per WCAG
FOCUS_VISIBLE = mandatory tokenized focus ring
PREFERS_REDUCED_MOTION = motion tokens collapse to near-zero / none
NON_COLOR_STATUS = enforced at component layer (I3/I4); tokens must remain distinguishable in HC considerations
```

## 6. Persistência e dados

```text
PERSISTENCE = none (CSS tokens are static assets)
NO_DATABASE = true
NO_ALEMBIC = true
THEME_PREFERENCE_STORAGE = deferred to UI shell (I5+); I2 only ships token sets
FIXTURE_POLICY = unchanged; DEMONSTRATION DATA remains B3/I4 concern
NO_OPERATIONAL_METADATA_MUTATION = true
```

## 7. Concorrência, locks e idempotência

```text
RUNTIME_LOCKS = none
TOKEN_BUILD = idempotent static CSS
THEME_TOGGLE = client presentation only; must not mutate scientific stores
CI_RACE = frontend job independent of Python r1-validate scientific paths
IDEMPOTENT_INGEST = unaffected
```

## 8. Segurança

```text
NO_SECRETS_IN_TOKENS = true
NO_ENV_SECRETS_IN_CSS = true
CLIENT_BUNDLE = public visual constants only
MASKING_RULES = inherited from B2/B4 (secrets/env/provider_tokens); tokens do not weaken masking
NO_RADIX_IN_I2 = true (license review remains I3 gate)
```

## 9. Observabilidade

```text
TOKEN_VERSION_SURFACE = DESIGN_TOKEN_CONTRACT_VERSION exposable in about/debug surfaces later
NO_CLIENT_FINANCIAL_CALC = true
NO_TELEMETRY_REQUIRED_IN_I2 = true
THEME_APPLIED_ATTR = data-theme for support diagnostics
```

## 10. Operação

```text
OPS_IMPACT = none in this docs PR
I2_CODE_OPS = replace scaffold hardcoded colors with tokens; keep scaffold copy non-operational
CLI_SOURCE_OF_TRUTH = unchanged until authorized UI
SCHEDULER_ACTIVATION = BLOCKED (unchanged)
HOST_DISCOVERY = DEFERRED (unchanged)
OPERATIONAL_DEBT = OPEN (must remain visible when UI lands; tokens must support ATTENTION/BLOCKED)
```

## 11. Rollback

```text
THIS_DOCS_PR = revert commit / close PR; remove I2_STATUS row or restore prior PROJECT.md
FUTURE_I2_CODE = revert token CSS PR; bump DESIGN_TOKEN_CONTRACT_VERSION major if consumers already shipped
ALWAYS = no Alembic / R3E / validate / scheduler changes in token PRs
```

## 12. Compatibilidade

```text
I1_SCAFFOLD = compatible; I2 replaces hardcoded scaffold colors gradually
DRAFT_FRONTEND_PATH = authorization docs may still say frontend/; execution path is web/
B3_SCREEN_CONTRACTS = consume semantic status tokens later; no screen code now
B4_LANGUAGE = status vocabulary aligns with SUCCESS≠profit / ERROR=real failure
R3E_SCIENTIFIC = unchanged
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
```

## 13. Testes necessários

### Nesta tarefa (docs)

- `uv run ruff check .`
- `uv run pytest -q`
- governance validator on the four I2 artifacts
- `pnpm --dir web` typecheck / lint / test / test:a11y / build (scaffold unchanged)

### Na implementação I2 futura

- unit: required semantic keys present in light and dark
- unit: `DESIGN_TOKEN_CONTRACT_VERSION === 1.0.0` at first ship
- contrast: text/status pairs meet WCAG 2.2 AA thresholds
- policy: forbid new hardcoded product colors outside token files (lint/test)
- theme smoke: light + dark mount without runtime errors
- reduced-motion: motion token values respect media query strategy

## 14. Alternativas consideradas

| Option | Verdict |
|--------|---------|
| Hand-authored CSS `--wick-*` in I2 | **SELECTED** |
| Style Dictionary / JSON source of truth now | DEFERRED (non-blocking) |
| Tailwind theme as sole source | REJECTED (semantic leakage risk) |
| CSS-in-JS runtime theme engine | REJECTED (bundle/complexity) |
| Dark-only product theme | REJECTED (light primary per visual direction) |
| Full component tokens in I2 | REJECTED (I3 boundary; keep I2 thin) |
| Install Radix in I2 | REJECTED (`NO_RADIX_INSTALLATION`) |

## 15. Riscos

| Risk | Severity | Mitigation |
|------|----------|------------|
| Token values fail contrast in dark | HIGH | contrast tests gate I2 code merge |
| SUCCESS green read as profit | HIGH | semantic docs + B4 copy + future StatusBadge multi-channel |
| Hardcoded colors leak in scaffold/components | MEDIUM | lint/test forbid outside token layer |
| Path confusion `frontend/` vs `web/` | MEDIUM | this assessment locks `FRONTEND_LOCATION=web/` |
| Premature I2 code without human flag | HIGH | `I2_IMPLEMENTATION_AUTHORIZED=false` until flip |
| Scope creep into components/screens | HIGH | mandatory constraints + review checklist |

## 16. Questões abertas

```text
1. Exact font family licensing/self-host choice — finalize at I2 code (must avoid Inter/Roboto/Arial as brand default; technical mono for run_id)
2. Whether to introduce web/packages/wick-ds in I2 or keep tokens under web/src/styles — DEFERRED_TO_I2_IMPLEMENTATION (non-blocking for this assessment)
3. High-contrast as separate data-theme vs stronger semantic tokens — prefer stronger tokens first; optional HC set later
4. Style Dictionary adoption timing — DEFERRED_NON_BLOCKING
```

Nenhuma questão aberta bloqueia `AUTHORIZATION_DECISION = AUTHORIZED_WITH_CONDITIONS` para o pacote documental.

## 17. Decisão arquitetural recomendada

```text
RECOMMENDED_ARCHITECTURE = HEADLESS_PRIMITIVES_PLUS_WICK_TOKENS (unchanged)
I2_TOKEN_STRATEGY = CSS_CUSTOM_PROPERTIES_FIRST
TOKEN_PREFIX = --wick-
CONTRACT_VERSION = 1.0.0
THEMES = light primary + dark supported + HC considerations
FRONTEND_LOCATION = web/
COMPONENT_BOUNDARY = I2 ships tokens/themes only; components start I3
RADIX = not in I2
AUTHORIZATION_DECISION = AUTHORIZED_WITH_CONDITIONS
```

Condições: (1) merge humano deste assessment/spec; (2) flip explícito `I2_IMPLEMENTATION_AUTHORIZED=true` em tarefa futura; (3) implementação I2 respeita mandatory constraints e testes de contraste/versão; (4) sem Radix/componentes/telas na PR de tokens.

## 18. Critérios para autorizar implementação

Antes de qualquer PR de código I2, todos devem ser verdadeiros:

1. Este impacto `IMPACT_ASSESSMENT_STATUS=APPROVED` mergeado em `main`
2. Spec I2 mergeada e estável
3. Humano define `I2_IMPLEMENTATION_AUTHORIZED=true` (hoje **false**)
4. `UI_SCREEN_IMPLEMENTATION_AUTHORIZED=false` permanece (sem telas)
5. Escopo limitado a tokens/temas/testes de token — sem componentes, sem Radix, sem screens
6. `DESIGN_TOKEN_CONTRACT_VERSION=1.0.0` e prefixo `--wick-*`
7. Status semantics binding documentado (SUCCESS≠profit; ERROR=real failure only)
8. Contrast/WCAG 2.2 AA test plan included in I2 implementation PR
9. `R3E_SCIENTIFIC_STATE_CHANGE=false` preservado
10. `SCHEDULER_ACTIVATION=BLOCKED`, `HOST_DISCOVERY=DEFERRED`, `OPERATIONAL_DEBT=OPEN` inalterados

```text
AUTHORIZATION_DECISION = AUTHORIZED_WITH_CONDITIONS
I2_CODE_AUTHORIZED_NOW = false
I2_IMPLEMENTATION_AUTHORIZED = false
MERGE_OF_DOCS = AWAITING_HUMAN_AUTHORIZATION
AUTOMATIC_MERGE_AUTHORIZED = false
```

## SCIENTIFIC_AND_OPERATIONAL_SAFETY

| Gate | Result |
|------|--------|
| R3E scientific state unchanged | PASS |
| No validate / readiness / scheduler changes | PASS |
| SUCCESS ≠ profit | PASS (contract) |
| ERROR = real failure only | PASS (contract) |
| NOT_READY → ATTENTION | PASS (contract) |
| Operational debt remains OPEN / visible later | PASS |
| No fake economics in tokens | PASS |
| Effect peeking | false |

## BLOCKERS

```text
BLOCKER_1 = Human merge authorization of this docs package
BLOCKER_2 = Human must set I2_IMPLEMENTATION_AUTHORIZED=true before token CSS lands
BLOCKER_3 = UI_SCREEN_IMPLEMENTATION_AUTHORIZED=false (blocks screens indefinitely for this track)
BLOCKER_4 = Radix/component work remains I3+ (out of I2)
```

## AUTHORIZATION_DECISION

```text
AUTHORIZATION_DECISION = AUTHORIZED_WITH_CONDITIONS
AUTHORIZED_NOW = documentation assessment and specification only
NOT_AUTHORIZED_NOW = token CSS, themes in code, components, Radix, screens
REQUIRES_HUMAN_MERGE = true
REQUIRES_HUMAN_I2_FLAG_FLIP = true
I2_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
```
