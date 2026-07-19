# UX-R1 — Design System Foundation — Draft Spec

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
TASK_ID = DESIGN-SYSTEM-FOUNDATION-001
PHASE = IMPACT_ASSESSMENT_ONLY
SPEC_STATUS = DRAFT
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
UI_IMPLEMENTATION_AUTHORIZED = false
UX_B2_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-DESIGN-SYSTEM-FOUNDATION-001_IMPACT_ASSESSMENT.md
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
SPEC_VERSION = 0.2.0-draft
CREATED_AT = 2026-07-19T12:31:41Z
RECONCILED_AT = 2026-07-19T12:56:44Z
```

Rascunho. Não autoriza scaffold/install/código UI.

## 1. Arquitetura

```text
RECOMMENDED_ARCHITECTURE = HEADLESS_PRIMITIVES_PLUS_WICK_TOKENS
FRAMEWORK = React + TypeScript
FRONTEND_ROOT = frontend/
DS_PACKAGE = frontend/packages/wick-ds
JS_PACKAGE_MANAGER = pnpm
HEADLESS = Radix UI primitives
TOKEN_LAYER = CSS custom properties (--wick-*)
NO_DEPENDENCY_INSTALL_AUTHORIZED = true
NO_FRONTEND_SCAFFOLD_AUTHORIZED = true
```

## 2. Tokens

Semantic-first categories; `DESIGN_TOKEN_CONTRACT_VERSION` semver; light primary / dark supported; no hardcoded product colors.

## 3. Components

Button, Input, Textarea, Select, Card (interaction-only), Badge/StatusBadge, Alert, Table (+ mobile card), Progress, Tooltip, Modal, Drawer, Navigation, FocusRing/SkipLink, DemoDataLabel, Evidence primitives.

## 4. Semantic statuses

```text
NORMAL | SUCCESS | ATTENTION | BLOCKED | ERROR | UNAVAILABLE | INFORMATIONAL
```

`NOT_READY`→ATTENTION; SUCCESS≠profit; ERROR=real failure only.

## 5. Accessibility

```text
WCAG_TARGET = 2.2 AA
TOOLS = axe-core + Testing Library + Playwright keyboard
```

## 6. Responsive

Desktop sidebar; tablet collapsible; mobile bottom nav per UX-B1.

## 7. Fixtures

`DEMONSTRATION DATA` mandatory; no implied profit/accuracy/readiness/scheduler/validate.

## 8. Security masking

Mask secrets/env/tokens by default; partial admin redaction for hosts/paths; no secrets in client bundles.

## 9. Test matrix

Mandatory: unit, component, a11y, semantic-status, fixture-label, scientific-safety, theme, responsive smoke. Visual regression phase-2 (Playwright).

## 10. Implementation increments (future; requires UX_B2_IMPLEMENTATION_AUTHORIZED)

1. Tokens + themes + StatusBadge + DemoDataLabel  
2. Forms + Alert + Table + Progress  
3. Overlays + navigation primitives  
4. Catalog + a11y report gate  

## 11. Prohibited patterns

Full trading UI kits; neon/ticker/gauges; P&L traffic lights; color-only status; hidden technical state; fake economic results; secrets in client; scaffolding under DS without authorization.
