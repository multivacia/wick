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
IMPACT_ASSESSMENT_STATUS = PENDING_REVIEW
IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
UX_B2_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = ef678fb92606541d0706ef408a37c0c020abe384
ANALYZED_AT = 2026-07-19T12:31:41Z
ANALYZED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
RECOMMENDED_DECISION = APPROVE_WITH_CHANGES
```

## SUMMARY

Avaliar o impacto de introduzir a fundação de design system do WICK (tokens, semântica de status, componentes base, a11y e responsivo) **sem implementar UI**.

Descoberta: não existe frontend no repositório. Stack atual = Python/uv/pytest/ruff. R5 prevê React+TypeScript+FastAPI no futuro, mas UX-R1 é trilha paralela operacional e ainda não autoriza implementação.

Recomendação: **Option B — headless primitives + WICK tokens/visual layer**, com tokens CSS como contrato primeiro. Decisão humana necessária sobre stack e pasta monorepo antes de autorizar implementação.

## 1. Objetivo

Produzir análise G1 pré-implementação para UX-B2 / `DESIGN-SYSTEM-FOUNDATION-001`, definindo arquitetura, riscos, guardrails científicos/econômicos, a11y, responsivo, testes e fronteira de implementação — sem código de UI.

## 2. Contexto técnico

### CURRENT_STATE

| Dimensão | Estado verificado |
|----------|-------------------|
| Frontend app | **Ausente** (0 `.tsx`/`.jsx`/`.vue`/`.svelte`/`.css`/`.html` de produto) |
| `package.json` | Ausente |
| Framework UI | Nenhum |
| Package manager (JS) | Nenhum; Python usa **uv** |
| Build system UI | Nenhum |
| CSS strategy | Nenhum |
| Test framework | **pytest** (+ pytest-cov opcional) |
| Lint/format | **ruff** |
| A11y tooling | Ausente |
| Static assets / branding | Ausente (só docs UX-R1) |
| API contract HTTP | Ausente para UX; CLI/reports JSON locais |
| Repo shape | **Monorepo Python** (`src/wick`); templates = AI docs, não UI |
| Predecessor UX-B1 | **MERGED** (PR #31 `5101c65`; post-merge #32–#34) |
| R5 vision (futuro) | React + TypeScript + FastAPI PWA (`docs/releases/R5_SPEC.md`) — **não iniciado** |

Fonte de direção visual já mergeada: `docs/ux/WICK_VISUAL_DIRECTION.md`, linguagem, IA e princípios UX-B1.

## 3. Componentes afetados

**Nesta fase (impacto apenas):** documentação em `docs/ai-impact/`, `docs/ai-specs/`, `docs/ai-reviews/`, `docs/PROJECT.md`, backlog UX, handoff.

**Em implementação futura autorizada (não nesta tarefa):**

- pacote/pasta de design system (proposta);
- tokens CSS;
- primitives headless + wrappers WICK;
- tooling a11y/visual tests;
- possivelmente `frontend/` ou `web/` no monorepo.

**Não afetados:** motor R3E, store future-unseen, validate, scheduler, migrations científicas.

## 4. Arquivos previstos

Nesta PR de impacto:

```text
docs/ai-impact/UX-R1-DESIGN-SYSTEM-FOUNDATION-001_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-DESIGN-SYSTEM-FOUNDATION_DRAFT_SPEC.md
docs/ai-reviews/UX-R1-DESIGN-SYSTEM-FOUNDATION_IMPACT_REVIEW.md
reports/ai-implementation/UX-R1-DESIGN-SYSTEM-FOUNDATION_IMPACT_HANDOFF.md
docs/PROJECT.md
docs/ux/UX-R1_BACKLOG.md
```

Futuros (somente após autorização): a definir na implementação (não criar agora).

## 5. Contratos e interfaces

### TOKEN_CONTRACT (proposto, não implementado)

Naming: `category.role.variant` em CSS custom properties com prefixo `--wick-`.

```text
color.background.*
color.text.*
color.border.*
color.status.*
space.*
size.*
radius.*
shadow.*
font.family.*
font.size.*
font.weight.*
line.height.*
breakpoint.*
motion.duration.*
motion.easing.*
z_index.*
```

Regras:

- tokens **semânticos** (ex.: `--wick-color-status-attention`) sobre raw hex na UI;
- raw tokens internos (ex.: `--wick-palette-petroleum-700`) só no tema;
- light default / dark via `[data-theme="dark"]` ou `prefers-color-scheme` + override explícito;
- proibido hardcode de cor em componentes de produto;
- versionar contrato (`DESIGN_TOKEN_CONTRACT_VERSION`);
- breaking change de token = bump de versão + changelog UX.

### SEMANTIC_STATUS_MODEL

```text
NORMAL
SUCCESS
ATTENTION
BLOCKED
ERROR
UNAVAILABLE
INFORMATIONAL
```

Mapeamento obrigatório:

| Status | Texto | Cor | Nota |
|--------|-------|-----|------|
| NORMAL | Neutro / operacional | Brand/petroleum | Estado padrão |
| SUCCESS | Concluído / saudável | Verde moderado | **Não** significa lucro |
| ATTENTION | Atenção / não pronto | Âmbar | Inclui `NOT_READY` |
| BLOCKED | Bloqueado | Roxo/cinza forte | Não é falha por si |
| ERROR | Falha real | Vermelho | Só falha operacional/científica real |
| UNAVAILABLE | Indisponível / N/A | Cinza | |
| INFORMATIONAL | Informativo | Ciano discreto | Ajuda/contexto |

Canais não-cor obrigatórios: texto + ícone + (quando útil) borda/fundo + `aria-label` / tooltip + modo alto contraste.

Códigos técnicos (`READINESS_NOT_READY`, `WINDOW_DAYS_INSUFFICIENT`, etc.) permanecem na camada secundária.

## 6. Persistência e dados

Design system não persiste dados científicos. Política de fixtures para protótipos futuros:

```text
REAL_OPERATIONAL_METADATA = allowed when labeled and non-secret
SAFE_FIXTURES = allowed
DEMONSTRATION_DATA = mandatory visible label on every fixture surface
```

Fixture **não** pode implicar: lucro real, acurácia de modelo, readiness, ativação de scheduler, execução de `validate`.

## 7. Concorrência, locks e idempotência

Sem locks de runtime nesta fundação. Tokens e componentes devem ser idempotentes sob reimport. Temas não devem depender de estado científico global mutável.

## 8. Segurança

### SECURITY_AND_PRIVACY

Riscos futuros de UI:

- renderizar secrets / env vars / tokens de provedor;
- expor hostnames, usernames, paths, stack traces, logs brutos;
- download/clipboard de evidências sensíveis.

Guardrails:

- máscaras default para secrets e tokens;
- paths/hostnames só para persona Admin com redaction parcial;
- logs estruturados sem secrets;
- clipboard com confirmação para IDs longos; nunca copiar env secrets;
- nenhum segredo no cliente (alinhado a R5);
- permissões por persona (A/B/C/D) na camada de app (fora do DS puro, mas tokens de “sensitive chip” podem existir).

## 9. Observabilidade

Componentes de status e evidence panels devem facilitar auditoria (`run_id`, hashes) sem calcular métricas no cliente. Telemetria de UI, se existir no futuro, não deve enviar PII/secrets.

## 10. Operação

Design system não altera coleta/scheduler. Operadores continuam com CLI até protótipos autorizados. Documentação de tokens deve viver em `docs/ux/` + story/catalog futuro.

## 11. Rollback

Reverter PR de implementação futura remove pacote UI sem tocar dados R3E. Tokens versionados permitem rollback parcial. Esta PR de impacto reverte só docs.

## 12. Compatibilidade

- Compatível com UX-B1 (princípios, visual, IA, linguagem).
- Compatível com R5 React+TS **se** Option B for adotada; se stack divergir de R5, registrar decisão explícita.
- Não conflita com B5-D1 / R3E científica.

## REPOSITORY_BOUNDARIES

Proposta (para decisão humana):

```text
REPO = multivacia/wick (monorepo)
PROPOSED_FRONTEND_ROOT = frontend/   # ou web/ — decidir na autorização
PROPOSED_DS_PACKAGE = frontend/packages/wick-ds  # ou frontend/src/design-system
PYTHON_BACKEND = src/wick (inalterado nesta fase)
NO_SEPARATE_FRONTEND_REPO_FOR_UX_R1 = recommended initially
```

API: UX-R1 protótipo pode começar com fixtures + leitura de reports; API HTTP read-only é dependência futura, não bloqueia tokens/componentes.

## 13. Testes necessários

### TEST_STRATEGY (futuro)

| Camada | Obrigatória antes do merge de implementação DS? |
|--------|--------------------------------------------------|
| unit (tokens/helpers) | SIM |
| component tests | SIM |
| accessibility (axe + keyboard) | SIM |
| semantic-status tests | SIM |
| fixture-label tests | SIM |
| scientific-state safety tests | SIM |
| theme light/dark tests | SIM |
| responsive smoke | SIM |
| visual regression | RECOMENDADO (pode ser fase 2) |
| keyboard navigation suites | SIM para shell/nav/modal |

Nesta tarefa: pytest/ruff/governance do repo Python devem permanecer PASS; sem testes UI (código inexistente).

## 14. Alternativas consideradas

### ARCHITECTURE_OPTIONS

#### Option A — Native tokens + lightweight components

```text
CSS custom properties
small internal component layer
no external UI kit
```

| Critério | Avaliação |
|----------|-----------|
| Custo | Médio-alto (a11y reinventada) |
| Acessibilidade | Boa se disciplinada; risco de regressão |
| Manutenção | Alta propriedade |
| Dependência | Baixa |
| Bundle | Baixo |
| Controle visual | Máximo |
| Dark theme | Total |
| Responsivo | Total |
| Testes | Mais suíte própria |
| Migração | Fácil para headless depois |
| Lock-in | Baixo |
| Adequação WICK | Alta (controle semântico) |

#### Option B — Headless primitives + WICK styling (**recomendada**)

```text
accessible headless primitives
WICK tokens and visual layer
```

| Critério | Avaliação |
|----------|-----------|
| Custo | Médio |
| Acessibilidade | Forte (focus trap, dialog, etc.) |
| Manutenção | Boa |
| Dependência | Moderada (primitivos, não tema visual) |
| Bundle | Moderado |
| Controle visual | Alto (WICK tokens) |
| Dark theme | Total |
| Responsivo | Total |
| Testes | Mais fácil em a11y de primitives |
| Migração | Alinha a React/R5 |
| Lock-in | Moderado (API headless) |
| Adequação WICK | **Alta** |

#### Option C — Full external component library

```text
prebuilt component suite
theme overrides
```

| Critério | Avaliação |
|----------|-----------|
| Custo | Baixo inicial |
| Acessibilidade | Variável |
| Manutenção | Theme fights |
| Dependência | Alta |
| Bundle | Alto |
| Controle visual | Limitado |
| Dark theme | Possível, estética genérica |
| Responsivo | Genérico |
| Testes | Menos superfície própria, mais overrides |
| Migração | Cara |
| Lock-in | Alto |
| Adequação WICK | **Baixa** (risco visual trading/casino, semântica P&L) |

### RECOMMENDED_ARCHITECTURE

```text
RECOMMENDED = OPTION_B_HEADLESS_PLUS_WICK_TOKENS
TOKEN_LAYER = CSS_CUSTOM_PROPERTIES_FIRST
STACK_ALIGNMENT = React_TypeScript_preferred_to_align_R5
STACK_DECISION = HUMAN_REQUIRED_BEFORE_IMPLEMENTATION
REJECTED = OPTION_C_FULL_EXTERNAL_KIT
```

## ACCESSIBILITY_IMPACT

```text
WCAG_TARGET = 2.2 AA
```

Obrigatório no DS:

- navegação teclado completa;
- foco visível (`:focus-visible` tokenizado);
- semântica SR (roles/names);
- contraste AA em light/dark/status;
- status nunca só por cor;
- zoom 200% sem perda crítica; 400% onde aplicável (reflow);
- `prefers-reduced-motion` → motion tokens ~0 / fade mínimo;
- touch targets ≥ 44px em mobile;
- tabelas com headers/`scope`/alternativa card;
- modais: focus trap, return focus, Escape;
- erros identificados em texto;
- plain language + expansão técnica (UX-B1).

Gates de aceite a11y bloqueiam merge de implementação.

## RESPONSIVE_IMPACT

| Viewport | Comportamento DS/app |
|----------|----------------------|
| Desktop | Sidebar + content; tabelas densas |
| Tablet | Sidebar colapsável/rail |
| Mobile | Bottom nav (Início/Coleta/Prontidão/Operação/Mais) |

Requisitos: table→card; filtros empilháveis; `run_id`/hash com wrap/`overflow-wrap`; readiness checklist empilhável; drawers/modais full-screen em mobile; touch; não assumir rede estável no host local (estados UNAVAILABLE/ATTENTION).

## SCIENTIFIC_SAFETY / ECONOMIC_INTERPRETATION_SAFETY

Riscos e guardrails:

| Risco | Guardrail |
|-------|-----------|
| `NOT_READY` como falha | Mapear a ATTENTION; proibir ERROR |
| `BLOCKED` como crash | Copy + cor roxo/cinza; princípio 4 |
| Verde/vermelho = lucro/prejuízo | Proibir semântica P&L; SUCCESS ≠ profit |
| Ocultar estado técnico | Camada secundária obrigatória |
| Interpretação econômica precoce | `ECONOMIC_INTERPRETATION_ALLOWED=false` refletido em UI |
| Demo como real | Label `DEMONSTRATION DATA` |
| Minimizar gates bloqueados | Evidence/status first-class |

## 15. Riscos

```text
RISK = adopting_full_ui_kit_with_trading_aesthetics
IMPACT = HIGH
MITIGATION = reject Option C; visual direction 0_percent_casino
RESIDUAL = LOW

RISK = implementing_ui_before_authorization
IMPACT = HIGH
MITIGATION = IMPLEMENTATION_AUTHORIZED=false until human approval
RESIDUAL = LOW

RISK = status_color_only_encoding
IMPACT = HIGH
MITIGATION = mandatory text/icon/SR channels + tests
RESIDUAL = LOW

RISK = stack_divergence_from_R5
IMPACT = MEDIUM
MITIGATION = explicit human stack decision recorded before code
RESIDUAL = MEDIUM
```

## 16. Questões abertas

1. Confirmar stack UX-R1 = React+TypeScript (alinhado R5) vs outra?
2. Pasta monorepo: `frontend/` vs `web/` vs pacote isolado?
3. Qual biblioteca headless (ex.: Radix, React Aria, Base UI)?
4. Storybook/catalog obrigatório no UX-B2 ou só no B3?
5. API read-only antes do primeiro protótipo ou fixtures-only?

Nenhuma questão bloqueia **aprovação do impacto**; todas bloqueiam **autorização de implementação**.

## DEPENDENCIES

Futuras (não instalar agora):

- runtime UI (React etc.) — decisão humana;
- headless primitives;
- test runners UI (Vitest/Playwright/Testing Library) — a definir;
- axe-core ou equivalente.

**Não modificar** `pyproject.toml` / lockfiles nesta tarefa.

## MIGRATION_STRATEGY

1. Aprovar impacto + decidir stack/pasta/headless.
2. Implementar tokens + status semantics + a11y baseline (incremento 1).
3. Primitives + componentes listados (incremento 2).
4. Catalog/docs (incremento 3).
5. Só então UX-B3 shell consome o DS.

## 17. Decisão arquitetural recomendada

```text
RECOMMENDED_DECISION = APPROVE_WITH_CHANGES
RECOMMENDED_ARCHITECTURE = OPTION_B
TOKEN_CONTRACT = CSS_SEMANTIC_FIRST
ACCESSIBILITY_TARGET = WCAG_2_2_AA
SEMANTIC_STATUS_MODEL = NORMAL|SUCCESS|ATTENTION|BLOCKED|ERROR|UNAVAILABLE|INFORMATIONAL
IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
```

### CHANGE_RISK

```text
CHANGE_RISK = MEDIUM
```

Motivo: nova superfície de produto e dependências futuras, sem mudança científica imediata.

## IMPLEMENTATION_BOUNDARY

**Permitido após autorização futura:** tokens, themes, componentes base, testes a11y, catalog.

**Proibido nesta e na implementação B2 até nova autorização explícita de app:**

- application shell completo de produto (salvo smoke do DS);
- routes/pages de domínio;
- API clients / backend endpoints;
- production UI deploy;
- mock screens de trading/P&L;
- qualquer alteração R3E/validate/scheduler.

## BLOCKERS

```text
BLOCKER_1 = Human review of this impact (PENDING_REVIEW)
BLOCKER_2 = Explicit stack and repository-boundary decision
BLOCKER_3 = UX_B2_IMPLEMENTATION_AUTHORIZED remains false until approval
BLOCKER_4 = UI_IMPLEMENTATION_AUTHORIZED remains false
```

## 18. Critérios para autorizar implementação

Para promover:

```text
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
```

exigir:

1. revisão humana com decisão explícita;
2. escolha documentada de Option B (ou waiver);
3. stack + pasta monorepo decididas;
4. headless library escolhida;
5. draft spec promovida a spec de implementação;
6. `UI_IMPLEMENTATION_AUTHORIZED` ainda pode permanecer false para “somente pacote DS” — se app shell for incluído, exigir flag explícita;
7. suite de testes obrigatórios acordada;
8. R3E inalterado.

Estado atual:

```text
IMPACT_ASSESSMENT_STATUS = PENDING_REVIEW
IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
UX_B2_IMPLEMENTATION_AUTHORIZED = false
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
```

## DECISION

```text
DECISION = APPROVE_WITH_CHANGES
IMPACT_ASSESSMENT_STATUS = PENDING_REVIEW
IMPLEMENTATION_AUTHORIZED = false
```

A fundação de design system é viável e recomendável sob Option B, condicionada a decisões humanas de stack/limites antes de qualquer código.
