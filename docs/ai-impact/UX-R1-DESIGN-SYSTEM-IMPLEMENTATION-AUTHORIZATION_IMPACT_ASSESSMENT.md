# UX-R1-DESIGN-SYSTEM-IMPLEMENTATION-AUTHORIZATION — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
TASK_ID = DESIGN-SYSTEM-FOUNDATION-001
TITLE = Design System Implementation Authorization Assessment
PHASE = IMPLEMENTATION_AUTHORIZATION_ASSESSMENT
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = false
UX_B2_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 5e438b8ad84d13f0c22c4017d3d3e26ac3c26647
ANALYZED_AT = 2026-07-19T13:31:35Z
ANALYZED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTHORIZATION_DECISION = AUTHORIZED_FOR_INCREMENT_I1_ONLY
AUTHORIZED_INCREMENT = I1
RECOMMENDED_ARCHITECTURE = HEADLESS_PRIMITIVES_PLUS_WICK_TOKENS
```

## SUMMARY

Avaliação de autorização para implementação futura do Design System WICK. **Nenhum código UI, scaffold, dependência JS ou workflow é criado nesta tarefa.**

Predecessor (impacto PR #35) permanece válido: `HEADLESS_PRIMITIVES_PLUS_WICK_TOKENS`, React+TypeScript, `frontend/`, pnpm, Radix, WCAG 2.2 AA.

Decisão de autorização proposta (após merge humano deste pacote):

```text
AUTHORIZATION_DECISION = AUTHORIZED_FOR_INCREMENT_I1_ONLY
AUTHORIZED_INCREMENT = I1 = frontend scaffold and CI only
```

`UX_B2_IMPLEMENTATION_AUTHORIZED` e `UI_IMPLEMENTATION_AUTHORIZED` permanecem **false** até tarefa futura explícita pós-merge desta avaliação. I1 só pode começar em PR separada após autorização humana de merge deste assessment **e** flag explícita de autorização de implementação I1.

## PREDECESSOR_STATE

```text
UX_B2_IMPACT_STATUS = MERGED
PR35_MERGE_COMMIT = 5bcb088ba9d0a07e8f4c9ae56ad5851ba445f9a6
POST_MERGE_PR39_MERGED = true
MERGE_COMPLETE_PR40_MERGED = true
FINAL_MAIN_TIP_PR41_MERGED = true
MAIN_TIP_AT_ASSESSMENT = 5e438b8ad84d13f0c22c4017d3d3e26ac3c26647
IMPACT_DOC = docs/ai-impact/UX-R1-DESIGN-SYSTEM-FOUNDATION-001_IMPACT_ASSESSMENT.md
RECOMMENDED_ARCHITECTURE = HEADLESS_PRIMITIVES_PLUS_WICK_TOKENS
UX_B2_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
NO_FRONTEND_DIRECTORY = true
NO_PACKAGE_JSON = true
PYTHON = 3.12 (.python-version); requires-python >=3.11
PYTHON_TOOLING = uv + ruff + pytest + alembic
CI = .github/workflows/ci.yml (Python-only R1 validate)
R5_VISION = React + TypeScript + FastAPI (NOT_STARTED)
```

## MANDATORY_DECISIONS

Cada decisão abaixo: DECISION / RATIONALE / ALTERNATIVES_REJECTED / RISKS / OWNER / EVIDENCE / REVERSIBILITY.

### FRONTEND_LOCATION

```text
DECISION = frontend/ inside multivacia/wick (monorepo)
RATIONALE = aligns impact REPOSITORY_BOUNDARIES; single governance/CI history; R5 path compatible
ALTERNATIVES_REJECTED = separate wick-ui repo (split review/CI); SSR-only templates (weak a11y/component reuse); reports-only (fails UX-R1 MVP interactive ops)
RISKS = polyglot repo complexity; mitigated by isolated frontend/ and separate CI job
OWNER = Gustavo Almeida
EVIDENCE = UX-R1-DESIGN-SYSTEM-FOUNDATION-001 impact §REPOSITORY_BOUNDARIES; R5_SPEC React path
REVERSIBILITY = HIGH before I2; MEDIUM after tokens land (extract package possible)
```

### FRONTEND_FRAMEWORK

```text
DECISION = React
RATIONALE = R5 already specifies React+TS; largest a11y/headless ecosystem; Testing Library maturity
ALTERNATIVES_REJECTED = Vue (extra learning, weaker R5 alignment); Svelte (smaller headless ecosystem); Python SSR templates (poor interactive a11y/component DS path)
RISKS = bundle size; mitigated by Vite + tree-shaking + no full UI kit
OWNER = Gustavo Almeida
EVIDENCE = docs/releases/R5_SPEC.md; predecessor impact FRAMEWORK_DECIDED
REVERSIBILITY = LOW after I3 components; HIGH at I1 scaffold
```

### LANGUAGE

```text
DECISION = TypeScript (strict)
RATIONALE = type-safe props/tokens; matches R5; safer refactors for status semantics
ALTERNATIVES_REJECTED = plain JavaScript
RISKS = toolchain overhead; mitigated by shared tsconfig in monorepo
OWNER = Gustavo Almeida
EVIDENCE = R5_SPEC; predecessor draft spec
REVERSIBILITY = LOW after components exist
```

### PACKAGE_MANAGER

```text
DECISION = pnpm (JS/TS workspace); uv remains Python
RATIONALE = strict node_modules; workspace packages for wick-ds; no conflict with uv.lock
ALTERNATIVES_REJECTED = npm (weaker workspace defaults); yarn classic; bun (less CI maturity for this repo)
RISKS = dual toolchain; document clearly in I1 README
OWNER = Gustavo Almeida
EVIDENCE = predecessor PACKAGE_MANAGER_DECIDED
REVERSIBILITY = MEDIUM at I1; LOW after lockfile + CI
```

### BUILD_TOOL

```text
DECISION = Vite
RATIONALE = fast local DX; first-class React+TS; simple library mode for wick-ds
ALTERNATIVES_REJECTED = Webpack (heavier); Parcel; Next.js (premature app framework for DS package)
RISKS = config drift; pin Vite major in I1
OWNER = Gustavo Almeida
EVIDENCE = industry default for Vite+React DS packages
REVERSIBILITY = MEDIUM at I1
```

### CSS_STRATEGY

```text
DECISION = CSS custom properties (--wick-*) first; no Tailwind required for DS core
RATIONALE = semantic token contract already locked; avoids utility-class leakage into status semantics
ALTERNATIVES_REJECTED = Tailwind-as-source-of-truth; CSS-in-JS runtime (bundle/SSR cost); Sass-only without semantic layer
RISKS = authoring verbosity; mitigated by token codegen later if needed
OWNER = Gustavo Almeida
EVIDENCE = predecessor TOKEN_LAYER = CSS_CUSTOM_PROPERTIES_FIRST
REVERSIBILITY = MEDIUM before wide component adoption
```

### HEADLESS_PRIMITIVE_STRATEGY

```text
DECISION = SELECTED = Radix UI primitives (@radix-ui/react-*)
RATIONALE = accessibility-first primitives; MIT; styling control retained by WICK tokens; matches Option B
ALTERNATIVES_REJECTED = full UI kits (casino/P&L aesthetics); React Aria only (viable alt but higher DIY styling); headlessui (weaker a11y guarantees vs Radix for our matrix); NO_EXTERNAL_PRIMITIVES (a11y cost too high for WCAG 2.2 AA gate)
RISKS = dependency surface; mitigated by subset installs + license review at first add
OWNER = Gustavo Almeida
EVIDENCE = predecessor HEADLESS_LIBRARY_DECIDED; MIT license known
REVERSIBILITY = LOW after I3 overlays; HIGH during I1 (no Radix install in I1)
```

Note: **I1 does not install Radix.** First `pnpm add @radix-ui/*` occurs in I3+ after DEPENDENCY_LICENSE_REVIEWED.

### TEST_FRAMEWORK / COMPONENT_TEST_TOOL / ACCESSIBILITY_TEST_TOOL / VISUAL_REGRESSION_TOOL / E2E_TOOL

```text
TEST_FRAMEWORK = Vitest
COMPONENT_TEST_TOOL = Testing Library (@testing-library/react)
ACCESSIBILITY_TEST_TOOL = axe-core (+ jest-axe or vitest-axe) + Playwright keyboard flows
VISUAL_REGRESSION_TOOL = Playwright screenshots (phase-2; not required for I1 authorization)
E2E_TOOL = Playwright
RATIONALE = aligned with predecessor a11y matrix; Vitest pairs with Vite
ALTERNATIVES_REJECTED = Jest-only (heavier with Vite); Cypress (overlap with Playwright)
RISKS = visual flake; keep visual regression out of I1–I3 merge gates
OWNER = Gustavo Almeida
EVIDENCE = predecessor ACCESSIBILITY_TEST_TOOL_DECIDED; VISUAL_REGRESSION DEFERRED_PHASE_2
REVERSIBILITY = MEDIUM at I1 tooling pin
```

### STORYBOOK_OR_EQUIVALENT

```text
DECISION = Storybook for React (catalog), shipping late in DS track (I3/I4 boundary or pre-UX-B3 consume)
RATIONALE = component catalog required before UX-B3 consumes DS; may ship late per predecessor DEFERRED_WITH_BLOCKER
ALTERNATIVES_REJECTED = Ladle-only; no catalog (blocks B3 safely)
RISKS = Storybook dep weight; isolate as optional workspace package
OWNER = Gustavo Almeida
EVIDENCE = predecessor Storybook timing deferral
REVERSIBILITY = HIGH until catalog is a merge gate for B3
```

### TOKEN_FORMAT / TOKEN_BUILD_STRATEGY

```text
TOKEN_FORMAT = CSS custom properties with DESIGN_TOKEN_CONTRACT_VERSION semver; optional JSON/YAML source later
TOKEN_BUILD_STRATEGY = hand-authored CSS tokens in I2; optional Style Dictionary codegen deferred (non-blocking)
RATIONALE = ship semantic contract without blocking on codegen toolchain
ALTERNATIVES_REJECTED = Tailwind theme as sole source; unversioned ad-hoc colors
RISKS = manual drift; validate naming with lint/tests in I2
OWNER = Gustavo Almeida
EVIDENCE = predecessor TOKEN_CONTRACT
REVERSIBILITY = HIGH in I2
```

### THEME_STRATEGY

```text
DECISION = light primary + dark supported + high-contrast considerations via token sets
RATIONALE = predecessor LIGHT_PRIMARY / DARK_SUPPORTED; ops hosts vary
ALTERNATIVES_REJECTED = dark-only; system-only without explicit tokens
RISKS = contrast failures; gate with axe + contrast checks
OWNER = Gustavo Almeida
EVIDENCE = predecessor §TOKEN_CONTRACT; WICK_VISUAL_DIRECTION
REVERSIBILITY = MEDIUM
```

### ICON_STRATEGY

```text
DECISION = SVG icons with accessible titles; no icon font; status icons mandatory alongside color
RATIONALE = non-color status cues required for WCAG / scientific safety
ALTERNATIVES_REJECTED = emoji-as-status; color-only badges
RISKS = inconsistent metaphor; publish icon usage guide in I4
OWNER = Gustavo Almeida
EVIDENCE = predecessor SEMANTIC_STATUS_MODEL multi-channel
REVERSIBILITY = HIGH before I4
```

### INTERNATIONALIZATION_STRATEGY

```text
DECISION = Portuguese (pt-BR) primary copy for UX-R1; i18n framework deferred
RATIONALE = product language is Portuguese; avoid i18n complexity before MVP screens
ALTERNATIVES_REJECTED = full i18n in I1; English-only UI
RISKS = later string extraction; keep copy in dedicated message modules from I4+
OWNER = Gustavo Almeida
EVIDENCE = docs/ux language guide; PROJECT owner locale
REVERSIBILITY = HIGH
```

### SUPPORTED_BROWSERS / NODE_VERSION

```text
SUPPORTED_BROWSERS = last 2 Chrome/Edge/Firefox/Safari; no IE
NODE_VERSION = 22 LTS (pin in .nvmrc / engines at I1)
RATIONALE = modern baselines; Vite/React support; CI ubuntu-latest compatible
ALTERNATIVES_REJECTED = IE11; unpinned Node
RISKS = operator older browsers; document minimum versions
OWNER = Gustavo Almeida
EVIDENCE = Vite/React current support matrices
REVERSIBILITY = MEDIUM
```

### DEPENDENCY_UPDATE_POLICY

```text
DECISION = Renovate/Dependabot PRs allowed for patch/minor with CI green; majors require human review; no auto-merge of majors
RATIONALE = reduce abandoned-package risk without silent breaking upgrades
ALTERNATIVES_REJECTED = fully automatic merges; frozen deps forever
RISKS = review burden; owner approves frontend dependency PRs
OWNER = Gustavo Almeida
EVIDENCE = dependency governance section below
REVERSIBILITY = HIGH
```

## REPOSITORY_STRATEGY

### Options compared

| Option | Verdict |
|--------|---------|
| A. frontend inside Wick repo | **SELECTED** |
| B. separate wick-ui repo | Rejected for UX-R1 (split governance) |
| C. static SSR operational interface | Rejected as primary DS strategy |
| D. generated read-only reports only | Rejected (fails interactive MVP) |

```text
REPOSITORY_STRATEGY = A_FRONTEND_INSIDE_WICK
FRONTEND_ROOT = frontend/
DS_PACKAGE = frontend/packages/wick-ds
APP_PACKAGE = frontend/apps/ops (created only when UI_IMPLEMENTATION_AUTHORIZED / I5+)
PYTHON_BACKEND = src/wick (unchanged)
```

Monorepo is acceptable: Python CI remains authoritative for scientific code; frontend CI is additive and must not gate R3E scientific paths incorrectly.

## FRONTEND_FRAMEWORK_DECISION

```text
SELECTED = React + TypeScript + Vite + pnpm
ALIGNMENT = R5_SPEC
NOT_INSTALLED_IN_THIS_TASK = true
```

Assessment dimensions (summary): team familiarity via R5 path; strong a11y/headless/testing ecosystem; good maintenance/LTS; acceptable offline/local-host via static build; mobile/tablet/desktop via responsive tokens; security via no secrets in client + dependency audit.

## HEADLESS_PRIMITIVE_DECISION

```text
STATUS = SELECTED
LIBRARY = Radix UI primitives
LICENSE = MIT (re-verify at first install)
INSTALL_IN_I1 = false
INSTALL_FROM_INCREMENT = I3
```

Material architecture is locked; deferral of *install* to I3 does **not** block authorization of I1 scaffold.

## DEPENDENCY_GOVERNANCE

```text
LICENSE_ALLOWLIST = MIT | Apache-2.0 | BSD-2-Clause | BSD-3-Clause | ISC (others need human exception)
SECURITY_SCANNING = pnpm audit + GitHub dependency review on frontend PRs
LOCKFILE_REQUIRED = pnpm-lock.yaml committed
EXACT_VERSION_POLICY = lockfile authoritative; ranges allowed in package.json within allowlist majors
AUTOMATED_UPDATE_POLICY = patch/minor PRs OK; majors human-only; no auto-merge majors
DEPENDENCY_REVIEW = required on PRs touching frontend/**
SBOM_GENERATION = CycloneDX or SPDX artifact on release/CI (from I1 CI plan; may warn-only until stable)
TRANSITIVE_DEPENDENCY_LIMITS = avoid mega-kits; prefer direct radix primitives subset
ABANDONED_PACKAGE_CRITERIA = no commits >18 months OR unresolved critical CVEs → replace/remove
BROWSER_SUPPORT_POLICY = last 2 evergreen
NEW_DEPENDENCY_APPROVER = Gustavo Almeida (human)
FIRST_PNPM_ADD_GATE = DEPENDENCY_LICENSE_REVIEWED = pass
```

## TOKEN_IMPLEMENTATION_CONTRACT

```text
PREFIX = --wick-
NAMING = category.role.variant
DESIGN_TOKEN_CONTRACT_VERSION = 1.0.0 at first token PR (I2)
SOURCE_FORMAT = CSS (I2); optional JSON source later
GENERATED_OUTPUTS = CSS variables consumed by components; no runtime JS theme engine required
RAW_TOKENS = color scales, space scale, font sizes
SEMANTIC_TOKENS = background/text/border/status/*
COMPONENT_TOKENS = optional thin layer mapping semantics → component slots
LIGHT_THEME = primary default
DARK_THEME = supported token set
HIGH_CONTRAST = considerations via status/border/text tokens (not a third product brand)
STATUS_TOKENS = NORMAL SUCCESS ATTENTION BLOCKED ERROR UNAVAILABLE INFORMATIONAL
MOTION_TOKENS = duration/easing; respect prefers-reduced-motion
RESPONSIVE_TOKENS = breakpoints
Z_INDEX_TOKENS = overlay scale
VERSIONING = semver; breaking = major
DEPRECATION = mark + one increment grace
VALIDATION = unit tests for required semantic keys; forbid hardcoded product colors in components
PROHIBITED_DIRECT_VALUES = raw hex/rgb in components (use tokens)
THEME_SWITCHING_BOUNDARY = document/html data-theme or class; no scientific state coupling
```

No token files in this task.

## COMPONENT_BOUNDARY

### FOUNDATION_COMPONENTS (I3)

```text
Button | IconButton | Link | Text | Heading | Badge | Card | Input | Select | Checkbox | Radio | Tooltip | Skeleton | FocusRing/SkipLink
```

### OPERATIONAL_COMPONENTS (I4)

```text
StatusBadge | Alert | EmptyState | TechnicalDetail | EvidenceLink | DemoDataLabel | Table primitives | Dialog | Drawer
```

### DEFERRED_COMPONENTS

```text
Navigation chrome | App shell layout | Charts | Domain dashboards | Storybook full catalog automation
```

### PROHIBITED_IN_FIRST_INCREMENT (I1)

```text
All components | tokens | themes | routes | pages | API clients | Radix installs | mock P&L | scheduler toggles | validate triggers
```

I1 scope = scaffold + CI only (see increments).

## UX_B3_B4_INTEGRATION

```text
UX_B3_STATUS = INDEPENDENT_TRACK (documentation may proceed)
UX_B4_STATUS = INDEPENDENT_TRACK
```

Rules:

1. UX-B3/B4 **docs** (screen contracts, terminology, microcopy) may progress without DS code.
2. UX-B3/B4 **UI implementation** must consume approved DS tokens/components; must not invent missing contracts.
3. Missing UX-B3 screen contracts / UX-B4 copy → UI work uses placeholders labeled incomplete; no invented readiness/profit semantics.
4. Merge-order: DS I2–I4 before B3/B4 UI code merges; B3/B4 docs PRs unrestricted by DS code.
5. Provenance/state matrix from B3 and terminology from B4 are inputs to I4 StatusBadge/EmptyState — not invented in DS.

## SCIENTIFIC_SAFETY_GATES

| Gate | Result |
|------|--------|
| NOT_READY semantics (= ATTENTION, not ERROR) | PASS (locked in impact) |
| READY semantics (no economic implication) | PASS |
| BLOCKED semantics (protocol ≠ crash) | PASS |
| ERROR semantics (real failure only) | PASS |
| operational debt display | PASS (must remain visible; not hidden) |
| fixture labeling | PASS (DEMONSTRATION DATA mandatory) |
| no fake economic results | PASS |
| no inferred scheduler activation | PASS |
| no hidden scientific blockers | PASS |
| timezone visibility | PASS (UTC+tz policy inherited) |
| data freshness visibility | PASS (must surface when data shown) |
| secret masking | PASS |

All scientific gates PASS at policy level. Enforcement tests land in I2–I4, not I1.

## ACCESSIBILITY_GATES

```text
WCAG_TARGET = 2.2 AA
```

| Gate | Result |
|------|--------|
| keyboard test strategy | PASS (Playwright + Testing Library) |
| screen-reader test strategy | PASS (roles/names + SR checklist) |
| contrast validation | PASS (token contrast tests in I2+) |
| focus management | PASS (Radix + FocusRing) |
| reduced motion | PASS (motion tokens) |
| zoom behavior | PASS (200%/400% smoke) |
| touch target policy | PASS (44px) |
| non-color status cues | PASS |
| accessible table strategy | PASS (table→card responsive) |

Critical tooling policy is decided. Tooling **install** deferred to I1 (Vitest/Playwright scaffolding) and I3 (axe in component CI). Missing install does **not** block authorization of I1 plan; missing policy would. Policy is present → authorization of I1 allowed.

## SECURITY_GATES

```text
NO_SECRETS_IN_CLIENT = required
MASK_DEFAULTS = secrets | env | provider_tokens
ADMIN_PARTIAL = hostnames | usernames | paths
ENV_EXAMPLE_ONLY = no real secrets in repo
FRONTEND_ENV = VITE_ public vars only; no DATABASE_URL in client
```

| Gate | Result |
|------|--------|
| secret masking rules | PASS |
| dependency license review at first add | DEFERRED_BLOCKING for I3+ installs; non-blocking for I1 scaffold without new UI libs |
| SBOM | DEFERRED_NON_BLOCKING for I1 (plan required; warn-only OK initially) |

## CI_CD_PLAN

Future frontend CI job (additive; **not modified in this task**):

```text
install (pnpm)
typecheck
lint (eslint/biome — choose at I1)
unit tests (vitest)
component tests
accessibility tests (from I3+)
build
visual regression (phase-2)
dependency audit
SBOM (warn-only → required)
artifact retention = build reports + a11y reports
```

Integration with Python CI:

```text
KEEP = existing r1-validate job unchanged for scientific paths
ADD = frontend-validate job on paths: frontend/**
FAIL_FRONTEND ≠ FAIL_SCIENTIFIC unless monorepo policy later says otherwise
```

No workflow file changes in this assessment PR.

## LOCAL_DEVELOPMENT_PLAN

```text
REQUIRED_RUNTIMES = Python 3.12 + uv; Node 22 + pnpm (from I1)
SETUP_COMMAND = documented in frontend/README (I1): pnpm install; pnpm dev
DEV_SERVER = Vite
BACKEND_INTEGRATION = fixtures-first; no live API required for DS; optional read-only API later under separate auth
FIXTURE_MODE = default for DS/story/prototype
ENV_VARS = .env.example only; no secrets
SECRET_HANDLING = never commit; never bundle
CROSS_PLATFORM = Linux primary CI; Windows operator docs for pnpm parity
```

No scripts created in this task.

## IMPLEMENTATION_INCREMENTS

### I1 — frontend scaffold and CI only

```text
SCOPE = frontend/ workspace skeleton; pnpm; Vite; TS strict; empty wick-ds package; frontend CI job; README; engines pin
NON_GOALS = tokens; components; Radix; routes; pages; Storybook; API
RISK = MEDIUM (polyglot CI)
TESTS = typecheck + lint + empty package build; Python suite unchanged green
ROLLBACK = delete frontend/ + revert CI job
REVIEW_BOUNDARY = docs/auth flags + scaffold only
MERGE_GATE = human auth of this assessment + explicit I1 implementation authorization task; CI green; no UI components
```

### I2 — tokens and themes

```text
SCOPE = --wick-* tokens; light/dark; contrast tests; DESIGN_TOKEN_CONTRACT_VERSION
NON_GOALS = components beyond DemoDataLabel optional; app shell
RISK = MEDIUM
TESTS = token unit + contrast
ROLLBACK = revert token package version major/minor
REVIEW_BOUNDARY = token contract only
MERGE_GATE = token tests pass; no hardcoded colors policy enforced
```

### I3 — foundation components

```text
SCOPE = FOUNDATION_COMPONENTS + Radix subset + axe tests
NON_GOALS = operational status suite; app routes
RISK = HIGH (first external UI deps)
TESTS = component + a11y
ROLLBACK = remove components package version; keep tokens
REVIEW_BOUNDARY = dependency license review required
MERGE_GATE = DEPENDENCY_LICENSE_REVIEWED; a11y CI pass
```

### I4 — operational status components

```text
SCOPE = OPERATIONAL_COMPONENTS; semantic status tests; fixture label tests; scientific-safety tests
NON_GOALS = domain pages
RISK = HIGH (semantics)
TESTS = semantic-status + fixture-label + scientific-safety
ROLLBACK = revert operational package
REVIEW_BOUNDARY = status model freeze
MERGE_GATE = scientific safety tests pass
```

### I5 — MVP application shell

```text
SCOPE = shell layout only under UI_IMPLEMENTATION_AUTHORIZED
NON_GOALS = live data; validate; scheduler controls
RISK = HIGH
TESTS = responsive smoke + a11y shell
ROLLBACK = remove apps/ops
REVIEW_BOUNDARY = requires UI_IMPLEMENTATION_AUTHORIZED=true
MERGE_GATE = explicit UI auth
```

### I6 — first read-only screen

```text
SCOPE = one read-only overview using fixtures; consumes B3 contracts if present
NON_GOALS = writes; economic charts; scheduler activation
RISK = HIGH
TESTS = fixture label + no fake economics
ROLLBACK = remove screen route
REVIEW_BOUNDARY = UX-B3 contract presence or explicit gaps labeled
MERGE_GATE = UI auth + screen contract review
```

No big-bang implementation.

## ROLLBACK_STRATEGY

```text
I1 = revert PR / delete frontend/
I2 = revert token files; bump major if needed
I3+ = versioned packages; remove components without touching Python/R3E
ALWAYS = no Alembic/R3E/scheduler/validate changes in DS PRs
```

## OPEN_DECISIONS

```text
1. ESLint vs Biome for frontend lint — choose at I1 implementation (non-blocking for this authorization)
2. Storybook exact timing (late I3 vs pre-B3) — DEFERRED_NON_BLOCKING for I1
3. Style Dictionary codegen — DEFERRED_NON_BLOCKING
4. Exact Radix package subset list — finalize at I3 dependency review
```

None block `AUTHORIZED_FOR_INCREMENT_I1_ONLY`.

## BLOCKERS

```text
BLOCKER_1 = Human merge authorization of this assessment PR
BLOCKER_2 = Separate future task must set explicit I1 implementation authorization before code
BLOCKER_3 = UX_B2_IMPLEMENTATION_AUTHORIZED remains false in this task
BLOCKER_4 = UI_IMPLEMENTATION_AUTHORIZED remains false (blocks I5–I6)
BLOCKER_5 = DEPENDENCY_LICENSE_REVIEWED pending at first Radix/install (blocks I3, not I1)
```

## AUTHORIZATION_DECISION

```text
AUTHORIZATION_DECISION = AUTHORIZED_FOR_INCREMENT_I1_ONLY
AUTHORIZED_INCREMENT = I1
AUTHORIZATION_APPLIES_TO_THIS_TASK = false
REQUIRES_HUMAN_MERGE_OF_THIS_ASSESSMENT = true
REQUIRES_SEPARATE_I1_IMPLEMENTATION_TASK = true
UX_B2_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
BEYOND_I1 = NOT_AUTHORIZED
```

Interpretation: after human merges this docs package, a **future** implementation task may be authorized to execute **I1 only**. Increments I2+ require their own authorization gates. This task implements nothing.
