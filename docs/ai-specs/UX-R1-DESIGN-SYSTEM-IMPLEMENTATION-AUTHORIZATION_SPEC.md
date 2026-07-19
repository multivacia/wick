# UX-R1 — Design System Implementation Authorization Spec

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
TASK_ID = DESIGN-SYSTEM-FOUNDATION-001
PHASE = IMPLEMENTATION_AUTHORIZATION_ASSESSMENT
SPEC_STATUS = ACTIVE_DRAFT
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-DESIGN-SYSTEM-IMPLEMENTATION-AUTHORIZATION_IMPACT_ASSESSMENT.md
AUTHORIZATION_DECISION = AUTHORIZED_FOR_INCREMENT_I1_ONLY
AUTHORIZED_INCREMENT = I1
IMPLEMENTATION_AUTHORIZED = false
UX_B2_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
SPEC_VERSION = 0.1.0
CREATED_AT = 2026-07-19T13:31:35Z
```

This specification defines authorization boundaries. It does **not** authorize code changes inside the assessment PR.

## 1. Locked stack (from predecessor + this assessment)

```text
REPOSITORY_STRATEGY = frontend/ inside multivacia/wick
FRAMEWORK = React
LANGUAGE = TypeScript (strict)
PACKAGE_MANAGER = pnpm
BUILD_TOOL = Vite
CSS_STRATEGY = CSS custom properties (--wick-*)
HEADLESS = Radix UI primitives (install from I3)
ARCHITECTURE = HEADLESS_PRIMITIVES_PLUS_WICK_TOKENS
WCAG_TARGET = 2.2 AA
NODE_VERSION = 22 LTS
```

## 2. Authorized increment — I1 ONLY

After human merge of the authorization assessment **and** an explicit future I1 implementation authorization, the only allowed implementation scope is:

### Allowed in I1

```text
- create frontend/ pnpm workspace
- create frontend/packages/wick-ds empty package (package.json, tsconfig, vite lib stub)
- pin Node engines / .nvmrc
- add frontend README with setup commands
- add frontend CI job (install, typecheck, lint, unit stub, build)
- add lockfile pnpm-lock.yaml
- choose ESLint or Biome at implementation time
- add .gitignore entries for node_modules / dist
```

### Prohibited in I1

```text
- design tokens / themes
- any React components (including Button, StatusBadge)
- Radix or other UI library installs
- Storybook
- routes / pages / app shell
- API clients
- changes to src/wick scientific code
- Alembic / validate / readiness / scheduler
- setting UX_B2_IMPLEMENTATION_AUTHORIZED for increments beyond I1
- setting UI_IMPLEMENTATION_AUTHORIZED=true
```

## 3. Later increments (NOT authorized by this spec)

```text
I2 = tokens and themes
I3 = foundation components + Radix subset
I4 = operational status components
I5 = MVP application shell (requires UI_IMPLEMENTATION_AUTHORIZED)
I6 = first read-only screen (requires UI_IMPLEMENTATION_AUTHORIZED)
```

Each requires a separate authorization or explicit gate satisfaction recorded before coding.

## 4. Scientific / operational safety (binding)

```text
NOT_READY = ATTENTION (never ERROR by default)
SUCCESS ≠ profit
BLOCKED ≠ automatic crash
ERROR = real failure only
DEMONSTRATION DATA label mandatory on fixtures
no fake economic results
no inferred scheduler activation
no hidden scientific blockers
UTC+timezone visibility when timestamps shown
secret masking mandatory
```

## 5. Accessibility (binding)

```text
WCAG_TARGET = 2.2 AA
keyboard + SR + contrast + focus + reduced motion + zoom + 44px touch + non-color status
a11y failure blocks merge from I3 onward
```

## 6. Dependency governance (binding)

```text
license allowlist + lockfile + audit + human approval for new deps
first Radix install requires DEPENDENCY_LICENSE_REVIEWED
```

## 7. UX-B3 / UX-B4

Documentation tracks remain independent. UI consumption of DS requires I2–I4 merged; missing contracts must not be invented.

## 8. Exit criteria for this authorization package

```text
impact APPROVED
review APPROVED
human merge of assessment PR
then separate I1 implementation task may proceed if explicitly authorized
```
