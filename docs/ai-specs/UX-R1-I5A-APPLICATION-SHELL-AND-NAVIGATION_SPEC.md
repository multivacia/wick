# UX-R1-I5A — Application Shell and Navigation Architecture — Specification

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
WORKSTREAM = I5A
TASK_ID = APPLICATION-SHELL-AND-NAVIGATION-ARCHITECTURE-001
TITLE = Application Shell and Navigation Architecture
PHASE = ARCHITECTURE_AND_SPECIFICATION
SPEC_STATUS = ACTIVE
SPEC_VERSION = 1.0.0
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_IMPACT_ASSESSMENT.md
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
UI_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
I5_IMPLEMENTATION_AUTHORIZED = false
NO_ROUTER_INSTALLATION = true
NO_SHELL_IMPLEMENTATION = true
NO_NAVIGATION_COMPONENTS = true
NO_SCREEN_IMPLEMENTATION = true
NO_REAL_DATA = true
R3E_SCIENTIFIC_STATE_CHANGE = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTOMATIC_MERGE_AUTHORIZED = false
CREATED_AT = 2026-07-19T16:55:00Z
IA_SOURCE = docs/ux/WICK_INFORMATION_ARCHITECTURE.md
SCREEN_CONTRACTS = docs/ai-specs/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS_SPEC.md
EXPERIENCE_FOUNDATION = docs/ai-specs/UX-R1-EXPERIENCE-FOUNDATION_SPEC.md
FRONTEND_HOST = web/ (I1 scaffold; no router)
OLD_BASE_SHA = 221aacc7141697403e9bbbc9f8690953b683e3a9
NEW_BASE_SHA = 29674068119e9bd95d6dd497619b6bf2898d458e
BASE_SHA = 29674068119e9bd95d6dd497619b6bf2898d458e
RECONCILED_AT = 2026-07-19T17:52:00Z
ARCHITECTURE_DECISION = AUTHORIZED_WITH_CONDITIONS
ROUTER_INSTALLATION_AUTHORIZED = false
ROUTER_RECOMMENDATION = react-router
PARALLEL_KICKOFF_STATUS = COMPLETE
I2_IMPLEMENTATION_AUTHORIZED = false
```

## 0. Natureza desta especificação

Documento de **arquitetura**. Não instala dependências, não cria componentes, não altera `web/`.

`IMPLEMENTATION_AUTHORIZED=true` autoriza apenas o pacote documental (G1). Código de shell/navegação exige autorização I5 futura separada.

## 1. Objetivo

Definir o contrato estável de application shell e navegação para UX-R1, alinhado à IA aprovada e aos route keys dos contratos MVP, de forma que a implementação futura (I5) possa instalar router e chrome sem reabrir decisões de hierarquia, URL, landmarks ou a11y de navegação.

## 2. Princípios

1. Uma hierarquia de navegação = IA canônica; labels em português (B4); paths estáveis em inglês kebab-case.
2. Cada rota MVP mapeia a exatamente uma tela com um objetivo (IA regra 1).
3. Chrome global nunca inventa estado científico ou econômico.
4. Bloqueado ≠ falha no chrome (semântica B3/B4).
5. Mobile é navegação de primeira classe (bottom nav), não sidebar comprimida.
6. Deep links preservam filtros em query string.
7. Foco e landmarks são parte do contrato, não “polish posterior”.
8. Auth e multi-tenant são fronteiras futuras; MVP assume operador local confiável até autorização explícita.

## 3. Navigation hierarchy

Fonte: `docs/ux/WICK_INFORMATION_ARCHITECTURE.md`.

### 3.1 Desktop (IA completa)

```text
WICK
├── Visão Geral
├── Coleta Futura
│   ├── Execuções
│   ├── Dados Coletados          (post-MVP; reserved)
│   └── Prontidão
├── Operação
│   ├── Host e Automação
│   ├── Backups                  (post-MVP; reserved)
│   └── Incidentes               (post-MVP; reserved)
├── Experimentos
│   └── R3E                      (explanatory; after UX-B9 authorization)
└── Governança
    ├── Backlog                  (post-MVP; reserved)
    ├── Aprovações               (post-MVP; reserved)
    └── Evidências               (post-MVP; reserved)
```

### 3.2 MVP chrome (primeira implementação I5 autorizada)

Itens **visíveis** no sidebar / primary nav:

| Ordem | Label (PT) | Section | Route |
|------:|------------|---------|-------|
| 1 | Visão Geral | root | `/overview` (canonical; `/` redirects) |
| 2 | Execuções | Coleta Futura | `/collection/runs` |
| 3 | Prontidão | Coleta Futura | `/collection/readiness` |
| 4 | Host e Automação | Operação | `/ops/host` |

Seções IA sem tela autorizada: **omitidas** do chrome MVP ou listadas como `disabled` com tooltip “ainda não disponível nesta versão” — preferência: **omitir** para reduzir clutter (IA princípio de um objetivo).

### 3.3 Mobile hierarchy

```text
Início → Coleta → Prontidão → Operação → Mais
```

| Aba | Destino canônico | Notas |
|-----|------------------|-------|
| Início | `/overview` | Visão Geral |
| Coleta | `/collection/runs` | Dados Coletados via subnav futura |
| Prontidão | `/collection/readiness` | |
| Operação | `/ops/host` | Backups/Incidentes em Mais quando existirem |
| Mais | sheet/menu | Experimentos, Governança, tema, ajuda — itens sem rota: hidden |

## 4. Route map

### 4.1 MVP routes (prepare for Visão Geral, Execuções, Readiness, Host e Scheduler)

| Route key | Canonical path | Screen | Nav |
|-----------|----------------|--------|-----|
| overview | `/overview` | Visão Geral | primary |
| overview-alias | `/` | redirect → `/overview` | — |
| collection-runs | `/collection/runs` | Execuções (lista) | primary |
| collection-run-detail | `/collection/runs/:run_id` | Execuções (detalhe) | child |
| collection-readiness | `/collection/readiness` | Prontidão / Readiness | primary |
| ops-host | `/ops/host` | Host e Automação / Host e Scheduler | primary |

Aligned with B3 route keys (`/` or `/overview`, `/collection/runs`, `/collection/readiness`, `/ops/host`).

### 4.2 Reserved future routes (IA; not in MVP chrome)

| Path | IA destination | Status |
|------|----------------|--------|
| `/collection/data` | Dados Coletados | RESERVED |
| `/ops/backups` | Backups | RESERVED |
| `/ops/incidents` | Incidentes | RESERVED |
| `/experiments/r3e` | Experimento R3E | RESERVED until UX-B9 UI auth |
| `/governance/backlog` | Backlog | RESERVED |
| `/governance/approvals` | Aprovações | RESERVED |
| `/governance/evidence` | Evidências | RESERVED |

Hitting a RESERVED path before authorization → **Not Found** (ou página “não disponível”) — ver §12. Não fabricar telas.

### 4.3 Screen-to-screen links (B3)

| From | To | Trigger |
|------|----|---------|
| Visão Geral | Execuções | última execução / timeline |
| Visão Geral | Readiness | readiness summary |
| Visão Geral | Host | host/scheduler pills |
| Execuções detail | Readiness | readiness before/after |
| Execuções detail | artifact viewer | open evidence (read-only) |
| Readiness | Execuções | last evaluation run |
| Host | Visão Geral | back / next safe action |

## 5. URL conventions

```text
SCHEME = path absolute from app basename (default basename = "/")
CASE = lowercase kebab-case segments
LOCALE_IN_PATH = false (UI language PT; paths language-neutral EN)
TRAILING_SLASH = false (normalize away)
ID_SEGMENT = opaque string (run_id); URL-encode
QUERY = filter/pagination state only; never secrets
HASH = optional focus target id within page (a11y); not primary nav state
```

### 5.1 Query contracts (MVP)

```text
/collection/runs?status=FAILED&from=<ISO-8601>&to=<ISO-8601>&trigger=MANUAL&page=1
```

- Unknown query keys: ignore (forward-compatible), do not error.
- Invalid enum values: coerce to empty filter + inline warning (não 404).
- Detail → list “back” must restore prior query (history stack or explicit `return_to` only if history missing; prefer history).

### 5.2 Canonicalization

| Input | Behavior |
|-------|----------|
| `/` | 302/client redirect to `/overview` |
| `/overview/` | normalize to `/overview` |
| `/collection/Runs` | case-normalize or 404; prefer normalize |
| Unknown path | Not Found boundary |

## 6. Recommended future router (NOT installed now)

```text
RECOMMENDED_ROUTER = react-router
RECOMMENDED_MAJOR = 7.x (current stable line at implementation time; pin exact version then)
HOST = Vite SPA (I1)
MODE = BrowserRouter or createBrowserRouter (data APIs preferred)
INSTALL_NOW = false
NO_ROUTER_INSTALLATION = true
ROUTER_INSTALLATION_AUTHORIZED = false
```

Rationale: matches React 19 + Vite SPA; nested layouts for shell; loaders deferred until data layer authorized; community a11y patterns; lower migration cost than TanStack Router or meta-framework switch.

Alternatives rejected for MVP: TanStack Router (extra complexity), Next/Remix (host change), manual History API (fragile nested layouts).

**I5 implementation must:** pin version, run license/audit, add only after `I5_IMPLEMENTATION_AUTHORIZED=true`.

## 7. Application frame

### 7.1 Layout slots

```text
┌──────────────────────────────────────────────────────────┐
│ header (banner)                                          │
├──────────────┬───────────────────────────────────────────┤
│ sidebar      │ main                                      │
│ (desktop)    │  breadcrumbs                              │
│              │  page title                               │
│              │  route outlet                             │
│              │                                           │
├──────────────┴───────────────────────────────────────────┤
│ bottom nav (mobile only)                                 │
└──────────────────────────────────────────────────────────┘
```

Tablet: sidebar colapsa para rail ou drawer (Experience Foundation §10).

### 7.2 Shell responsibilities

- Brand WICK + release/experiment context label
- Global operational status (plain language + technical code) — consumes B4 catalogs when wired
- Automation indicator: ativa / não ativa (`SCHEDULER_ACTIVATION` reflected; never offers activate in MVP)
- Theme toggle (claro/escuro) — placement in header desktop / Mais mobile
- Skip link to `#main-content`
- Demo-data banner slot when fixtures active (`DADOS_DEMONSTRATIVOS`)

Shell **does not**: run collect/validate, activate scheduler, invent metrics, show P&L.

## 8. Header

| Element | Required | Notes |
|---------|----------|-------|
| Skip to content | yes | first focusable |
| Brand mark + “WICK” | yes | links to `/overview` |
| Context chip (UX-R1 / R3E) | yes | non-economic |
| Global status summary | yes | ATTENTION vs ERROR semantics |
| Automation indicator | yes | blocked/inactive until authorized |
| Theme control | yes | |
| Help / glossary entry | optional MVP | may live under Mais |

Header landmark: `role="banner"` / `<header>`.

## 9. Sidebar

| Property | Contract |
|----------|----------|
| Landmark | `<nav aria-label="Principal">` |
| Structure | Section group labels matching IA (Coleta Futura, Operação, …) only when ≥1 child visible |
| Active state | `aria-current="page"` on active link |
| Collapse | desktop expandable; tablet rail; hidden on mobile (bottom nav replaces) |
| Order | §3.2 |
| Disabled reserved items | omit in MVP |

Keyboard: Tab into nav; Arrow keys optional enhancement within nav list (recommended).

## 10. Mobile navigation

- Fixed bottom bar; five tabs per IA.
- Landmark: `<nav aria-label="Principal móvel">`.
- Active tab: `aria-current="page"`.
- “Mais” opens dialog/sheet with secondary destinations + theme; focus trap while open; Esc closes; restore focus to “Mais” button.
- Safe-area insets respected; does not cover primary CTA of page content (content padding-bottom).

## 11. Breadcrumbs

| Route | Breadcrumb |
|-------|------------|
| `/overview` | WICK / Visão Geral |
| `/collection/runs` | WICK / Coleta Futura / Execuções |
| `/collection/runs/:run_id` | WICK / Coleta Futura / Execuções / `{run_id}` |
| `/collection/readiness` | WICK / Coleta Futura / Prontidão |
| `/ops/host` | WICK / Operação / Host e Automação |

- Landmark: `<nav aria-label="Trilha de navegação">` with ordered list.
- Last crumb: plain text (not link).
- Mobile: may collapse to parent link + current title if width constrained; full trail available to SR via nav.

## 12. Page title contract

```text
DOCUMENT_TITLE = "{PageLabel} · WICK"
H1 = PageLabel (exactly one h1 per route)
PageLabel examples = Visão Geral | Execuções | Prontidão | Host e Automação
Detail = "Execução {run_id}" (truncate visually; full id in mono + copy control)
```

- Route change updates `document.title` and H1.
- Status codes (NOT_READY, BLOCKED) belong in content/status regions — not in H1 alone without plain language.

## 13. Loading boundary

| Layer | Behavior |
|-------|----------|
| App bootstrap | minimal shell chrome + “Carregando experiência operacional…” |
| Route transition | keep chrome; replace outlet with skeleton or plain loading text per B3 |
| Data refresh | manual refresh default; if auto-refresh later ≥60s + stale banner (B3) |

- Loading UI must not flash error styles.
- Announce via `aria-live="polite"` on status region (debounce).
- Prefer route-level Suspense boundary around outlet only; header/nav remain interactive when safe.

## 14. Error boundary

| Class | User presentation | Technical |
|-------|-------------------|-----------|
| Recoverable route error | plain language + retry + link Visão Geral | log `SHELL_ROUTE_ERROR` |
| Unexpected render error | full-page safe fallback inside main; chrome may remain | log stack locally; no PII |
| Data unavailable | EMPTY/UNAVAILABLE per B3/B4 — not error boundary | |

Forbidden: stack traces to non-technical users as primary copy; economic interpretation of failures.

## 15. Not-found behavior

```text
UNKNOWN_PATH → Not Found view
RESERVED_UNAUTHORIZED_PATH → same Not Found or “Rota ainda não disponível” (prefer distinct copy if detectable as reserved)
MISSING_RUN_ID → Not Found within Execuções context + link back to list
```

Not Found content:

- H1: “Página não encontrada”
- Plain explanation + links: Visão Geral, Execuções
- HTTP semantics for static host: SPA fallback to `index.html` then client Not Found (I5 deploy note)

## 16. Deep links

- All MVP routes must be bookmarkable and reload-safe (URL → same view).
- Filters in query; detail ids in path.
- External deep link into detail with unknown `run_id`: Not Found (§15), not empty fabricated run.
- Opening evidence artifacts: read-only; prefer in-app panel or new tab to static file viewer — never execute.
- Deep links must not include filesystem secrets or credentials.

## 17. Keyboard navigation

| Requirement | Contract |
|-------------|----------|
| Full path | All nav and primary controls reachable via Tab |
| Skip link | First tab stop → `#main-content` |
| Focus visible | WCAG 2.2 AA visible indicator |
| Escape | Closes Mais sheet / drawers |
| Enter/Space | Activates links/buttons |
| Arrow keys | Recommended within nav lists and tablists |
| No keyboard trap | Except modal/sheet with documented exit |

## 18. Responsive behavior

| Breakpoint | Shell |
|------------|-------|
| Desktop (≥1100px guideline) | Sidebar expanded + header |
| Tablet (768–1099) | Rail or collapsible sidebar + header |
| Mobile (<768) | Header compact + bottom nav; sidebar hidden |

Content breakpoints for tables/cards remain owned by screen contracts / design system; shell only guarantees chrome swap.

Zoom 200%: chrome remains usable; bottom nav may scroll or compact labels with accessible names retained.

`prefers-reduced-motion`: disable non-essential nav transitions.

## 19. Screen-reader landmarks

Recommended structure matching IA:

```text
header[banner]
  - brand, global status
nav[aria-label=Principal]          (desktop sidebar)
nav[aria-label=Trilha de navegação] (breadcrumbs)
main#main-content
  - h1 page title
  - route content regions
nav[aria-label=Principal móvel]    (mobile bottom; hidden desktop)
complementary (optional)           (help/glossary panel when open)
```

Rules:

- Exactly one `main` landmark visible.
- Nav labels distinct (Principal vs Trilha vs Principal móvel).
- Status banners use `role="status"` or `aria-live` appropriately; assertive only for real errors.
- Decorative icons: `aria-hidden="true"`; text alternatives on controls.

## 20. Focus restoration

| Event | Focus target |
|-------|--------------|
| Client-side route change | `h1` of new page (tabIndex=-1) or `#main-content` |
| Back from detail to list | Previously focused row/link if still present; else list h1 |
| Close Mais sheet | “Mais” tab button |
| Open error retry success | restored route h1 |
| Not Found | Not Found h1 |

Do not leave focus on detached DOM nodes after outlet unmount.

## 21. Route-level access boundary

MVP policy (until auth authorized):

```text
ACCESS_MODE = SINGLE_OPERATOR_LOCAL_TRUSTED
DEFAULT_ROUTE_ACCESS = ALLOW_ALL_MVP_ROUTES
RESERVED_ROUTES = NOT_FOUND_UNTIL_AUTHORIZED
MUTATING_ACTIONS = DENY (collect / validate / activate / delete)
```

Future extension points (interfaces only):

```text
canActivate(routeKey, context) → boolean
canView(resource, context) → boolean
```

Shell checks `canActivate` before rendering outlet; denial → dedicated “Acesso indisponível” view (not silent redirect), with link to Visão Geral.

Scientific gates (`R3E_GATE`, `VALIDATE_AUTHORIZED=false`) are **content** constraints, not HTTP auth — displayed in page body/status, not used as silent nav hide unless product later decides otherwise (default: show Readiness even when NOT_READY).

## 22. Future authentication boundary

```text
AUTH_STATUS = NOT_IN_MVP
AUTH_PROVIDER = UNDECIDED
SESSION = NONE
```

When later authorized, shell must support:

- Unauthenticated → redirect to future `/login` (path reserved conceptually; not implemented)
- Authenticated operator context in header (name/role non-PII excess)
- Logout control
- No secrets in localStorage without explicit security review
- CSRF/session rules owned by backend task — UI only consumes session state

I5A does **not** choose IdP, passwords, or API tokens.

## 23. Telemetry boundary

```text
TELEMETRY_IN_SHELL = OPTIONAL_FUTURE
ALLOWED_EVENTS = SHELL_ROUTE_VIEW | SHELL_NAV_CLICK | SHELL_ROUTE_ERROR | SHELL_NOT_FOUND
FORBIDDEN_PAYLOADS = secrets | raw host paths | provider credentials | PII beyond operator id already authorized
NO_SCIENCE_METRICS = true
NO_ECONOMIC_METRICS = true
```

Shell may emit navigational telemetry only after a future observability authorization. I5A does not add analytics SDKs.

## 24. Feature-flag boundary

```text
FEATURE_FLAGS = FUTURE_OPTIONAL
SHELL_CONSUMES = boolean visibility for reserved IA destinations only
FLAGS_MUST_NOT = unlock validate | activate scheduler | imply READY economic claims
DEFAULT = all reserved destinations hidden in MVP
```

Flag evaluation belongs to a future config service; shell only reads a typed allow-list.

## 25. Layer separation (mandatory)

```text
INFORMATION_ARCHITECTURE = IA doc (what exists)
ROUTE_STRUCTURE = this spec route map (URL keys)
NAVIGATION_PRESENTATION = sidebar/bottom nav chrome
ACCESS_CONTROL = canActivate / future auth
DATA_LOADING = future loaders/adapters (I6+)
SCREEN_CONTENT = page bodies (I6+; NOT embedded in shell architecture)
```

No screen content (cards, tables, ViewModels) may be defined inside shell components beyond outlet placeholders.

## 26. Operational language safeguards

```text
READY != VALIDATION_AUTHORIZED
COMPLETE != SCIENTIFIC_SUCCESS
SUCCESS != PROFIT
NOT_READY != ERROR
BLOCKED != FAILED
```

Dual-layer language in chrome:

```text
plain language first
technical term second
```

Nav labels use B4 catalogs; status chips never use green/red as profit/loss.

## 27. URL and route safety (summary)

```text
STABLE_SLUGS = kebab-case MVP paths in §4
404 = Not Found boundary (§15)
UNKNOWN_NESTED = Not Found (no silent parent fallthrough that invents content)
DEEP_LINK_REFRESH = same route rehydrate; missing resource → Not Found
BASENAME = support future Vite base / deploy prefix via router basename
QUERY_STRING_OWNERSHIP = filters owned by destination screen contracts (B3); shell does not rewrite arbitrary queries
ROUTE_STATE_OWNERSHIP = location + optional ephemeral UI state; no secrets in history state
BACK_FORWARD = browser history; focus restoration per §20
DOCUMENT_TITLE = page title contract §12
SKIP_LINK_DESTINATION = #main-content
```

## 28. Integration with existing artifacts

| Artifact | Consumption |
|----------|-------------|
| `WICK_INFORMATION_ARCHITECTURE.md` | Hierarchy + mobile map |
| UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS_SPEC | Route keys, filters, loading copy |
| UX-R1-EXPERIENCE-FOUNDATION_SPEC | Journeys, a11y, responsive |
| UX-B4 language catalogs | Nav labels, status phrasing |
| `web/` I1 scaffold | Future mount point; App remains scaffold until I5 |

## 29. Future file layout (informative; not created now)

```text
web/src/
  app/
    router.tsx              # React Router config (future I5)
    routes.tsx
  shell/
    ApplicationFrame.tsx
    AppHeader.tsx
    AppSidebar.tsx
    MobileBottomNav.tsx
    Breadcrumbs.tsx
    PageTitle.tsx
    landmarks.ts
  boundaries/
    RouteErrorBoundary.tsx
    RouteLoading.tsx
    NotFoundPage.tsx
  pages/                    # I6+ screens only when authorized
```

Creating these files now is **forbidden**.

## 30. Acceptance criteria (architecture package)

1. Hierarchy matches IA top-level sections.
2. MVP route map covers Visão Geral, Execuções, Readiness, Host e Scheduler.
3. URL conventions and deep-link rules specified.
4. Frame, header, sidebar, mobile nav, breadcrumbs, page title specified.
5. Loading, error, not-found, focus restoration specified.
6. Landmarks and keyboard/responsive behavior specified.
7. Access + auth + telemetry + feature-flag boundaries specified as future-safe.
8. Router recommendation recorded; `ROUTER_INSTALLATION_AUTHORIZED=false`.
9. No `web/` code changes in this task.
10. Flags remain: `I5_IMPLEMENTATION_AUTHORIZED=false`, `UI_SCREEN_IMPLEMENTATION_AUTHORIZED=false`.
11. `ARCHITECTURE_DECISION = AUTHORIZED_WITH_CONDITIONS` with C1–C8 enumerated in impact.

## 31. Explicit non-goals

```text
NO_ROUTER_INSTALLATION
NO_SHELL_IMPLEMENTATION
NO_NAVIGATION_COMPONENTS
NO_SCREEN_IMPLEMENTATION
NO_REAL_DATA
NO_SCHEDULER_ACTIVATION
NO_HOST_DISCOVERY_EXECUTION
NO_R3E_SCIENTIFIC_STATE_CHANGE
NO_R4_R5_UNLOCK
NO_AUTOMATIC_MERGE
ROUTER_INSTALLATION_AUTHORIZED = false
ARCHITECTURE_DECISION = AUTHORIZED_WITH_CONDITIONS
```
