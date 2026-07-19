# UX-R1-I1 — Frontend Scaffold and CI — Implementation Spec

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = DESIGN-SYSTEM-FOUNDATION-001
TASK_ID = FRONTEND-SCAFFOLD-AND-CI-001
INCREMENT = I1
PHASE = IMPLEMENTATION
SPEC_STATUS = ACTIVE
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-DESIGN-SYSTEM-IMPLEMENTATION-AUTHORIZATION_IMPACT_ASSESSMENT.md
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
I1_IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_STATUS = COMPLETE
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
DESIGN_TOKEN_IMPLEMENTATION_AUTHORIZED = false
COMPONENT_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
I2_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
SPEC_VERSION = 0.1.0
CREATED_AT = 2026-07-19T16:12:00Z
```

Predecessor authorization impact (APPROVED, MERGED PR #43) authorizes I1 scaffold/CI only.
See `docs/ai-impact/UX-R1-DESIGN-SYSTEM-IMPLEMENTATION-AUTHORIZATION_IMPACT_ASSESSMENT.md`.

## 1. Scope

Create the minimum frontend scaffold and CI foundation for future WICK UX work.

In scope:

```text
frontend project skeleton under web/
toolchain configuration (Node 22, pnpm, Vite, TypeScript strict, ESLint)
package management with committed lockfile
type checking, linting, unit-test harness, accessibility smoke harness
production build
CI integration (additive frontend job + dependency review on web paths)
dependency governance baseline
developer setup documentation (Windows + Linux)
```

Out of scope / non-goals:

```text
design tokens and themes (I2)
foundation or operational components (I3+)
Radix installs
router, app shell, MVP screens
API clients / operational data integration
charts, auth, analytics, remote fonts, CSS frameworks
Storybook
SBOM generation (deferred non-blocking per authorization)
any R3E scientific / collection / validate / scheduler change
```

## 2. Architecture

```text
REPOSITORY_STRATEGY = MONOREPO_INSIDE_WICK
FRONTEND_LOCATION = web/
FRONTEND_FRAMEWORK = React
LANGUAGE = TypeScript (strict)
BUILD_TOOL = Vite
PACKAGE_MANAGER = pnpm@10.33.3
NODE_VERSION = 22 LTS
LINTER = ESLint flat config (chosen at I1; Biome not selected)
TEST_FRAMEWORK = Vitest
COMPONENT_TEST_TOOL = Testing Library
ACCESSIBILITY_TEST_TOOL = axe-core + jest-axe
HEADLESS_PRIMITIVE_STRATEGY = RADIX_FROM_I3_ONLY
ACCESSIBILITY_TARGET = WCAG_2_2_AA
```

### Divergence note (location)

Merged authorization assessment documents used `frontend/` as the planned root.
This I1 execution task locks `FRONTEND_LOCATION = web/` per the authorized I1 implementation prompt.
No `frontend/packages/wick-ds` package is created in I1; an empty DS package remains deferred until a later authorized increment that needs it.

## 3. File structure

```text
web/
  public/
  src/
    App.tsx                 # non-product placeholder only
    main.tsx
    scaffoldCopy.ts
    styles.css              # minimal readable/focus CSS only
    vite-env.d.ts
  tests/
    setup.ts
    App.test.tsx
    a11y/scaffold.a11y.test.tsx
  index.html
  package.json
  pnpm-lock.yaml
  tsconfig.json
  tsconfig.app.json
  tsconfig.node.json
  tsconfig.vitest.json
  vite.config.ts
  vitest.config.ts
  eslint.config.js
  .nvmrc
  .npmrc
  README.md
.github/workflows/ci.yml                    # additive frontend-validate job
.github/workflows/dependency-review.yml     # PRs touching web/**
```

Placeholder visible copy (required):

```text
WICK UX foundation
No operational screens implemented
Demonstration scaffold only
```

## 4. Dependencies

Exact pins (lockfile authoritative):

| Package | Role | Version |
|---------|------|---------|
| react / react-dom | runtime | 19.2.7 |
| typescript | language | 5.9.3 |
| vite | build | 8.1.5 |
| @vitejs/plugin-react | React plugin | 6.0.3 |
| eslint + typescript-eslint | lint | 9.39.5 / 8.64.0 |
| vitest | unit tests | 4.1.10 |
| @testing-library/react | DOM tests | 16.3.2 |
| jest-axe + axe-core | a11y smoke | 10.0.0 / 4.11.0 |
| jsdom | test DOM | 27.4.0 |

Prohibited in I1: Radix, router, state managers, data-fetching libs, chart libs, CSS frameworks, design-token libs, icon libs, analytics, auth, API clients.

Governance:

```text
lockfile required
ignore-scripts=true
exact versions in package.json
pnpm audit in CI
pnpm licenses list for allowlist review
GitHub dependency-review on web/** PRs
license allowlist = MIT | Apache-2.0 | BSD-2-Clause | BSD-3-Clause | ISC
```

## 5. Commands

```bash
pnpm --dir web install --frozen-lockfile
pnpm --dir web typecheck
pnpm --dir web lint
pnpm --dir web test
pnpm --dir web test:a11y
pnpm --dir web build
pnpm --dir web audit
pnpm --dir web licenses
pnpm --dir web dev
```

## 6. CI

Additive job `frontend-validate` in `.github/workflows/ci.yml`:

```text
pnpm install --frozen-lockfile
typecheck
lint
unit tests
accessibility smoke tests
production build
dependency audit
```

Python `r1-validate` job is preserved unchanged in behavior.

`dependency-review` workflow runs on PRs touching `web/**` or related workflow files.

## 7. Testing

Scaffold-only proofs:

1. root application renders
2. scaffold labels present
3. no basic axe violations in placeholder
4. production build succeeds
5. deterministic jsdom test environment

Do not test UX-B3 screens (not implemented).

## 8. Security

```text
no secrets committed
no credentials / production endpoints
no analytics / remote fonts / third-party runtime calls
VITE_ prefix only for client env; documented in web/README.md
production sourcemaps disabled
no operational host/scheduler/filesystem discovery data in UI
```

## 9. Accessibility

WCAG 2.2 AA is the product target. I1 ships the smoke harness only.
Merge-blocking a11y for components starts from later increments (I3+).

## 10. Cross-platform support

Documented for Windows and Linux in `web/README.md`.
Docker is not required for frontend development.

## 11. Rollback

```text
revert the I1 PR / delete web/ and frontend CI additions
Python scientific paths remain untouched
```

## 12. Acceptance criteria

```text
BACKEND_TESTS = PASS
FRONTEND_TYPECHECK = PASS
FRONTEND_LINT = PASS
FRONTEND_TESTS = PASS
FRONTEND_A11Y = PASS
FRONTEND_BUILD = PASS
DEPENDENCY_AUDIT = PASS_OR_DOCUMENTED_APPROVED_EXCEPTION
GOVERNANCE_VALIDATOR = ERRORS_0_WARNINGS_0
CI additive frontend job present
placeholder is non-product and contains required scaffold text
no Radix / screens / tokens / operational metrics
I2_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
```
