# UX-R1-I5A — Application Shell and Navigation Architecture — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2 / UX-B5-prep
WORKSTREAM = I5A
TASK_ID = APPLICATION-SHELL-AND-NAVIGATION-ARCHITECTURE-001
TITLE = Application Shell and Navigation Architecture
CHANGE_RISK = MEDIUM
PHASE = ARCHITECTURE_AND_SPECIFICATION
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
UI_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
I5_IMPLEMENTATION_AUTHORIZED = false
I5A_STATUS = ARCHITECTURE_IN_PROGRESS
NO_ROUTER_INSTALLATION = true
NO_SHELL_IMPLEMENTATION = true
NO_NAVIGATION_COMPONENTS = true
NO_SCREEN_IMPLEMENTATION = true
NO_REAL_DATA = true
R3E_SCIENTIFIC_STATE_CHANGE = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 221aacc7141697403e9bbbc9f8690953b683e3a9
ANALYZED_AT = 2026-07-19T16:55:00Z
ANALYZED_BY = cursor-agent
APPROVED_AT = 2026-07-19T17:05:00Z
APPROVED_BY = cursor-agent-independent-review
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
RECOMMENDED_DECISION = APPROVED
DECISION = APPROVED
AUTOMATIC_MERGE_AUTHORIZED = false
```

## SUMMARY

Esta tarefa define a **arquitetura e especificação** do application shell e da navegação UX-R1 (hierarquia IA, mapa de rotas, frame, landmarks, a11y de navegação, deep links, boundaries de loading/erro/404, fronteiras futuras de acesso/autenticação).

`IMPLEMENTATION_AUTHORIZED=true` (gate G1) autoriza **apenas** o pacote documental e candidatura a merge destes artefatos. **Não** autoriza instalação de router, componentes de shell/nav, telas, dados reais ou qualquer código em `web/`.

```text
ARTIFACTS = impact | spec | review | handoff | PROJECT.md status line
UI_CODE = NONE
ROUTER_INSTALL = NONE
SHELL_CODE = NONE
R3E_SCIENTIFIC_STATE = UNCHANGED
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
I5_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
```

## SCOPE

### In scope (docs only)

- Navigation hierarchy aligned to `docs/ux/WICK_INFORMATION_ARCHITECTURE.md`
- Route map and URL conventions for MVP + reserved future IA routes
- Application frame: header, sidebar, mobile nav, breadcrumbs, page title contract
- Loading boundary, error boundary, not-found behavior
- Deep links, keyboard navigation, responsive behavior
- Screen-reader landmarks, focus restoration
- Route-level access boundary and future authentication boundary (contracts only)
- Recommended future router choice (React Router) without installation

### Out of scope

```text
NO_ROUTER_INSTALLATION
NO_SHELL_IMPLEMENTATION
NO_NAVIGATION_COMPONENTS
NO_SCREEN_IMPLEMENTATION
NO_REAL_DATA
I2 design tokens implementation
I3+ component library implementation
I6A screen/data fixture implementation
Host discovery execution
Scheduler activation
Validate / collect / run-cycle execution
R3E scientific state change
R4 / R5 unlock
```

## DEPENDENCIES

| Dependency | Status | Role |
|------------|--------|------|
| UX-B1 Experience Foundation | MERGED | Personas, journeys, a11y baseline |
| UX IA `WICK_INFORMATION_ARCHITECTURE.md` | ACTIVE | Canonical nav hierarchy |
| UX-B3 Screen contracts | MERGED | MVP route keys and screen contracts |
| UX-B4 Operational language | MERGED | Microcopy for nav labels / status |
| UX-B2 I1 scaffold (`web/`) | MERGED | Vite + React 19 host; no router yet |
| UX-B2 I2+ | NOT AUTHORIZED | Tokens/components remain blocked |
| I5 shell implementation | NOT AUTHORIZED | This package is architecture only |

## IMPLEMENTATION_BOUNDARY

```text
G1_AUTHORIZATION_SCOPE = DOCS_PACKAGE_MERGE_CANDIDACY_ONLY
I5_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
ALLOWED_REPO_TOUCHES = docs/ai-impact | docs/ai-specs | docs/ai-reviews | reports/ai-implementation | docs/PROJECT.md (I5A_STATUS line only)
FORBIDDEN_REPO_TOUCHES = web/** | package.json router deps | src/wick/** | data/** | alembic/** | ops activation
```

## SCIENTIFIC_SAFETY

- Nenhuma alteração de coleta, readiness, validate, thresholds, manifests ou reports científicos.
- Shell futuro deve expor estado científico existente (ex.: `R3E_GATE`, readiness) sem reinterpretar economicamente.
- `SCHEDULER_ACTIVATION=BLOCKED` e `HOST_DISCOVERY=DEFERRED` permanecem; nav não implica conclusão operacional.

## SECURITY_IMPACT

- Sem secrets, sem rede nova, sem auth runtime nesta fase.
- Contrato futuro: route-level access boundary + authentication boundary documentados; implementação de auth permanece fora de I5A e fora de UX-R1 MVP até autorização explícita.

## ACCESSIBILITY_IMPACT

- Spec define landmarks, focus restoration, keyboard nav e contraste herdado de WCAG 2.2 AA (UX-B1/B10).
- Sem implementação a11y de shell nesta tarefa; harness I1 permanece scaffold-only.

## ROLLBACK_STRATEGY

- Docs-only: revert do commit/PR remove arquitetura sem efeito em runtime.
- `I5A_STATUS` em `PROJECT.md` reverte junto com o PR se necessário.
- Nenhum migration, schema, dependency ou store alterado.

## BLOCKERS

Nenhum blocker para **arquitetura documental**.

Blockers para **implementação I5 futura**:

```text
I5_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
Separate human authorization task required before router install or shell code
```

## DECISION

```text
DECISION = APPROVED
RECOMMENDED_DECISION = APPROVED
IMPLEMENTATION_AUTHORIZED = true
SCOPE_OF_AUTHORIZATION = DOCS_ONLY
UI_IMPLEMENTATION_AUTHORIZED = false
I5_IMPLEMENTATION_AUTHORIZED = false
AUTOMATIC_MERGE_AUTHORIZED = false
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
```

---

## 1. Objetivo

Definir a arquitetura de application shell e navegação do WICK UX-R1 — hierarquia, rotas, frame, landmarks, deep links, boundaries de carregamento/erro/404, teclado/responsivo/a11y e fronteiras futuras de acesso — sem instalar router, sem componentes e sem telas.

## 2. Contexto técnico

- Frontend scaffold I1 em `web/` (Vite, React 19, TypeScript strict, Vitest, axe): página scaffold única em `<main>`, **sem** React Router.
- IA aprovada: Visão Geral, Coleta Futura, Operação, Experimentos, Governança (`docs/ux/WICK_INFORMATION_ARCHITECTURE.md`).
- Contratos MVP B3 fixam route keys: `/` ou `/overview`, `/collection/runs`, `/collection/readiness`, `/ops/host`.
- Trilha paralela UX: `R3E_SCIENTIFIC_STATE=UNCHANGED`; host discovery deferred; scheduler blocked; R4 blocked; R5 not started.
- I5A é preparação arquitetural; execução de shell (I5) permanece não autorizada.

## 3. Componentes afetados

**Afetados (docs):** `docs/ai-impact/`, `docs/ai-specs/`, `docs/ai-reviews/`, `reports/ai-implementation/`, `docs/PROJECT.md` (somente `I5A_STATUS`).

**Não afetados:** `web/src/**`, `web/package.json`, backend `src/wick/**`, pipelines R3E, dados operacionais, CI além de validação local de regressão.

**Afetados no futuro (após autorização I5):** router dependency, layout shell, nav components, route modules — **fora desta tarefa**.

## 4. Arquivos previstos

| Arquivo | Ação nesta tarefa |
|---------|-------------------|
| `docs/ai-impact/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_IMPACT_ASSESSMENT.md` | Criar |
| `docs/ai-specs/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_SPEC.md` | Criar |
| `docs/ai-reviews/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_REVIEW.md` | Criar |
| `reports/ai-implementation/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_HANDOFF.md` | Criar |
| `docs/PROJECT.md` | Adicionar `I5A_STATUS = ARCHITECTURE_IN_PROGRESS` |

Nenhum arquivo sob `web/` nesta tarefa.

## 5. Contratos e interfaces

- **Navigation contract:** hierarquia desktop/mobile e labels alinhados à IA e à linguagem B4.
- **Route map contract:** paths MVP + rotas reservadas futuras; query filters preservados (B3).
- **Shell frame contract:** header, sidebar, bottom nav, breadcrumbs, page title.
- **Boundary contracts:** loading, error, not-found, focus restoration.
- **Access contracts (future):** route-level gate + auth boundary sem implementação.
- **Router recommendation:** React Router v7 (data APIs / Vite SPA) na implementação futura I5 — **não** instalar agora.

Consumidores futuros: I5 implementation task, I6A+ screens, UX-B10 a11y audit.

## 6. Persistência e dados

- Sem persistência nova.
- Sem leitura de artefatos operacionais nesta tarefa (`NO_REAL_DATA`).
- Shell futuro consome apenas dados já autorizados por contratos B3/adapters futuros; I5A não define adapter.

## 7. Concorrência, locks e idempotência

- Documentação: merge idempotente; reaplicação dos mesmos artefatos não altera runtime.
- Shell futuro não deve adquirir locks de automação; navegação é read-only em relação a `automation.lock`.
- Deep-link + refresh: estado de URL é fonte de navegação (idempotente sob mesmos query params).

## 8. Segurança

- Sem secrets no repositório; sem endpoints novos.
- Deep links futuros não devem embutir tokens ou paths sensíveis de filesystem no URL público.
- Route-level access boundary: por padrão, MVP local assume single-operator trusted host; multi-user auth é fronteira futura explícita.
- Proibido: ações destrutivas, activate scheduler, validate, collect a partir do shell.

## 9. Observabilidade

- Spec recomenda `run_id` / route name em telemetria futura de UI (quando autorizada); I5A não instrumenta.
- Erros de boundary devem mapear a códigos estáveis (`SHELL_ROUTE_ERROR`, `SHELL_NOT_FOUND`) sem métricas econômicas.

## 10. Operação

- Operação científica/ops inalterada.
- Status operacional (`HOST_DISCOVERY`, `OPERATIONAL_DEBT`, `SCHEDULER_ACTIVATION`) permanece DEFERRED/OPEN/BLOCKED.
- Shell futuro deve refletir esses estados no chrome global sem permitir ativação.

## 11. Rollback

Revert docs + linha `I5A_STATUS`. Sem rollback de schema, deps ou dados. Se I5 já tivesse código (não é o caso), rollback seria remoção do router/shell em PR separado — **não aplicável agora**.

## 12. Compatibilidade

- Compatível com scaffold I1 (sem router).
- Compatível com route keys B3; paths canônicos documentados na spec.
- Não conflita com I2/I6A assessments paralelos desde que não se altere `I2_*` / `I6A_*` / `UI_SCREEN_IMPLEMENTATION_AUTHORIZED`.
- Mobile bottom-nav mapping permanece o da IA.

## 13. Testes necessários

**Nesta tarefa (docs):**

- `uv run ruff check .`
- `uv run pytest -q`
- `uv run python scripts/validate_ai_governance_artifacts.py` nos 4 artefatos novos
- `pnpm --dir web typecheck && lint && test && test:a11y && build` (regressão; sem mudança em `web/`)

**Na implementação I5 futura (não autorizada):**

- Route unit tests; landmark a11y tests; focus restoration; 404/error boundary; deep-link query preservation; keyboard nav.

## 14. Alternativas consideradas

| Opção | Descrição | Decisão |
|-------|-----------|---------|
| A. React Router (SPA, Vite) | Biblioteca madura; data routers; a11y-friendly | **Recomendada para I5 futuro** |
| B. TanStack Router | Type-safe; mais setup | Descartada para MVP (custo vs benefício) |
| C. File-based (Remix/Next) | Exige mudança de host | Incompatível com I1 Vite SPA locked |
| D. Manual history API | Sem dep | Descartada (manutenção, a11y, nested routes) |
| E. Implementar shell agora | Código UI | **Rejeitada** — `I5_IMPLEMENTATION_AUTHORIZED=false` |

## 15. Riscos

| Risco | Severidade | Mitigação |
|-------|------------|-----------|
| Confundir G1 docs auth com auth de código UI | Médio | Flags explícitas `I5_*=false`, `UI_*=false` em todos artefatos |
| Drift entre IA e route map | Médio | Spec referencia IA + B3; review checklist |
| Prefixo EN de rotas vs labels PT | Baixo | Labels PT na UI; paths estáveis em EN kebab |
| Implementação prematura de auth | Médio | Auth boundary documentada como FUTURE_ONLY |
| Parallel track I2/I6A status pollution | Médio | PROJECT.md altera só `I5A_STATUS` |

## 16. Questões abertas

1. Momento exato da autorização I5 (task humana separada) — **fora do escopo I5A**; permanece bloqueado.
2. Se Experimento R3E entra no MVP shell nav na primeira I5 ou só após UX-B9 — **recomendação:** reservar rota `/experiments/r3e` na IA; não incluir no MVP chrome até tela autorizada.
3. Provider de auth futuro (local single-user vs IdP) — **deferred**; boundary apenas.
4. Base path de deploy (`/` vs subpath) — **recomendação:** `basename=/` até ops de hosting UI definir; Vite `base` permanece default.

Nenhuma questão aberta bloqueia a aprovação documental I5A.

## 17. Decisão arquitetural recomendada

1. Congelar arquitetura de shell/nav em spec I5A; merge humano docs-only.
2. Adotar React Router na **futura** I5 (não agora).
3. Landmarks e hierarquia alinhados à IA; MVP routes = Visão Geral, Execuções, Readiness, Host e Scheduler.
4. Manter `I5_IMPLEMENTATION_AUTHORIZED=false` e `UI_SCREEN_IMPLEMENTATION_AUTHORIZED=false` até task explícita.
5. Não alterar estado científico R3E nem gates operacionais.

## 18. Critérios para autorizar implementação

Autorizar implementação I5 (código) **somente** quando **todos** forem verdadeiros:

```text
I5A architecture artifacts MERGED
Separate impact/authorization for I5 implementation APPROVED
I5_IMPLEMENTATION_AUTHORIZED = true
UI_IMPLEMENTATION_AUTHORIZED = true (or scoped shell-only flag equivalent)
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false still allowed if shell-only (screens remain I6+)
NO scientific unlock implied
Human merge authorization recorded
Router pin + license review completed in that future task
```

Até lá:

```text
NO_ROUTER_INSTALLATION
NO_SHELL_IMPLEMENTATION
NO_NAVIGATION_COMPONENTS
NO_SCREEN_IMPLEMENTATION
NO_REAL_DATA
AUTOMATIC_MERGE_AUTHORIZED = false
```
