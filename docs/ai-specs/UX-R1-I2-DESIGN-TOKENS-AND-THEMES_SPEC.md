# UX-R1-I2 — Design Tokens and Themes — Specification

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = DESIGN-SYSTEM-FOUNDATION-001
TASK_ID = DESIGN-TOKENS-AND-THEMES-001
INCREMENT = I2
PHASE = AUTHORIZATION_AND_SPECIFICATION
SPEC_STATUS = ACTIVE_DRAFT
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-I2-DESIGN-TOKENS-AND-THEMES_IMPACT_ASSESSMENT.md
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
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTHORIZATION_DECISION = AUTHORIZED_WITH_CONDITIONS
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
FRONTEND_LOCATION = web/
DESIGN_TOKEN_CONTRACT_VERSION = 1.0.0
SPEC_VERSION = 1.0.0
CREATED_AT = 2026-07-19T16:54:33Z
BASE_SHA = 221aacc7141697403e9bbbc9f8690953b683e3a9
```

G1 note: `IMPLEMENTATION_AUTHORIZED=true` covers **this specification document package** only. It does **not** authorize token CSS, theme files, components, Radix, or screens. `I2_IMPLEMENTATION_AUTHORIZED=false` is binding until an explicit human flip after docs merge.

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

## 1. Purpose and non-goals

### Purpose

Define the authoritative contract for WICK design tokens and themes so a future I2 implementation PR can land CSS custom properties under `web/` without inventing semantics, aesthetics, or scientific meaning.

### Non-goals (this task and I2 code scope)

```text
NO_TOKEN_IMPLEMENTATION in this PR
NO_THEME_IMPLEMENTATION in this PR
NO_COMPONENTS (I3+)
NO_RADIX_INSTALLATION (I3+)
NO_SCREEN_IMPLEMENTATION (requires UI_SCREEN_IMPLEMENTATION_AUTHORIZED)
NO_STORYBOOK
NO_TAILWIND_AS_SOURCE_OF_TRUTH
NO_RUNTIME_JS_THEME_ENGINE
NO_R3E_SCIENTIFIC_CHANGES
```

## 2. Alignment

| Source | Binding input |
|--------|---------------|
| `docs/ux/WICK_VISUAL_DIRECTION.md` | ops-center aesthetic; light primary; dark supported; semantic palette; WCAG AA; reduced motion; no casino/P&L traffic lights |
| `docs/ai-specs/UX-R1-DESIGN-SYSTEM-FOUNDATION_DRAFT_SPEC.md` | `--wick-*`; status model; WCAG 2.2 AA |
| Authorization impact I2 section | tokens, light/dark, contrast tests, `DESIGN_TOKEN_CONTRACT_VERSION` |
| I1 execution | `FRONTEND_LOCATION = web/` (not `frontend/`) |

## 3. Token architecture

```text
ARCHITECTURE = HEADLESS_PRIMITIVES_PLUS_WICK_TOKENS
TOKEN_LAYER = CSS custom properties
PREFIX = --wick-
DESIGN_TOKEN_CONTRACT_VERSION = 1.0.0
SOURCE_FORMAT = CSS (hand-authored)
CODEGEN = optional Style Dictionary later (non-blocking)
```

### 3.1 Layers

```text
RAW  →  SEMANTIC  →  (optional) COMPONENT
```

| Layer | May reference | Consumed by |
|-------|---------------|-------------|
| Raw | literal values only | semantic + theme files |
| Semantic | raw tokens | components and app chrome (preferred public API) |
| Component | semantic tokens only | foundation/operational components (I3/I4); optional in I2 |

**Rule:** Product UI must not consume raw palette steps directly once components exist. I2 may expose raw for internal theme composition only.

### 3.2 Naming

```text
CSS form: --wick-{category}-{role}-{variant?}
Examples:
  --wick-color-brand-petroleum
  --wick-color-status-success
  --wick-space-4
  --wick-font-size-md
  --wick-motion-duration-fast
  --wick-z-index-overlay
```

Logical dotted names in docs (`color.status.success`) map 1:1 to CSS `--wick-color-status-success`.

## 4. Raw tokens

Raw tokens are scales without product meaning.

### 4.1 Color scales (illustrative roles; final hex chosen at I2 code with contrast tests)

```text
--wick-raw-color-neutral-{0..12}
--wick-raw-color-petroleum-{1..9}
--wick-raw-color-cyan-{1..9}
--wick-raw-color-green-{1..9}
--wick-raw-color-amber-{1..9}
--wick-raw-color-purple-{1..9}
--wick-raw-color-red-{1..9}
```

Direction (from visual direction; not casino neon):

| Scale | Direction |
|-------|-----------|
| petroleum | deep institutional blue / brand |
| cyan | discrete accent / focus / informational |
| green | complete / healthy operational — not profit |
| amber | attention / not ready |
| purple / strong gray | blocked protocol |
| red | real failure only |
| neutral | surfaces, text, unavailable |

### 4.2 Typography raw

```text
--wick-raw-font-family-sans
--wick-raw-font-family-mono
--wick-raw-font-size-{xs,sm,md,lg,xl,2xl}
--wick-raw-font-weight-{regular,medium,semibold,bold}
--wick-raw-line-height-{tight,normal,relaxed}
--wick-raw-letter-spacing-{normal,wide}
```

Constraints:

- Primary UI font: readable product/ops face; **do not** use Inter, Roboto, or Arial as brand default.
- Mono: for `run_id`, hashes, status codes, technical IDs.
- Self-host or system stack documented at I2 code; remote font CDN not required for I2.

### 4.3 Spacing raw

```text
--wick-raw-space-{0,1,2,3,4,5,6,8,10,12,16}
```

Base unit recommendation: `4px` step scale (operational medium density).

### 4.4 Radii raw

```text
--wick-raw-radius-{none,sm,md,lg,full}
```

Prefer modest radii; avoid decorative “pill clusters” as product chrome.

### 4.5 Shadows raw

```text
--wick-raw-shadow-{none,sm,md,lg}
```

Subtle elevation only; **no** aggressive multi-layer glow.

### 4.6 Motion raw

```text
--wick-raw-motion-duration-{0,fast,normal,slow}
--wick-raw-motion-easing-{standard,emphasized}
```

### 4.7 Breakpoints raw

```text
--wick-raw-breakpoint-sm: 640px
--wick-raw-breakpoint-md: 768px
--wick-raw-breakpoint-lg: 1024px
--wick-raw-breakpoint-xl: 1280px
```

Note: CSS custom properties are not media-query native; document JS/CSS `@media` mirrors using the same numeric contract. Token file should declare the numeric constants (and optionally duplicate as custom props for JS `getComputedStyle` consumers).

### 4.8 Z-index raw

```text
--wick-raw-z-index-base: 0
--wick-raw-z-index-sticky: 100
--wick-raw-z-index-dropdown: 200
--wick-raw-z-index-overlay: 300
--wick-raw-z-index-modal: 400
--wick-raw-z-index-toast: 500
--wick-raw-z-index-max: 9999
```

## 5. Semantic tokens

Semantic tokens encode product meaning. Components should prefer these.

### 5.1 Surface / text / border

```text
--wick-color-surface-canvas
--wick-color-surface-panel
--wick-color-surface-subtle
--wick-color-text-primary
--wick-color-text-secondary
--wick-color-text-inverse
--wick-color-text-muted
--wick-color-border-subtle
--wick-color-border-strong
--wick-color-brand-petroleum
--wick-color-accent-cyan
--wick-color-focus-ring
```

### 5.2 Status semantics

```text
--wick-color-status-normal
--wick-color-status-success
--wick-color-status-attention
--wick-color-status-blocked
--wick-color-status-error
--wick-color-status-unavailable
--wick-color-status-informational
```

Optional foreground-on-status pairs for badges:

```text
--wick-color-status-*-fg
--wick-color-status-*-bg
--wick-color-status-*-border
```

#### Status binding rules

| Token status | Maps from operational language | Binding |
|--------------|--------------------------------|---------|
| NORMAL | default / idle healthy-neutral | not a celebration |
| SUCCESS | complete / healthy | **SUCCESS ≠ profit, edge, or P&L** |
| ATTENTION | not ready / warning without failure | `NOT_READY` → ATTENTION |
| BLOCKED | protocol/gate blocked | **BLOCKED ≠ automatic ERROR** |
| ERROR | real operational/scientific failure | **ERROR = real failure only** |
| UNAVAILABLE | N/A / missing | gray / muted |
| INFORMATIONAL | neutral info / accent | no alarm |

Visual direction aliases:

```text
color.status.complete → SUCCESS
color.status.attention → ATTENTION
color.status.blocked → BLOCKED
color.status.failure → ERROR
color.status.unavailable → UNAVAILABLE
```

### 5.3 Typography semantic

```text
--wick-font-family-body
--wick-font-family-technical
--wick-font-size-body
--wick-font-size-label
--wick-font-size-title
--wick-font-size-display
--wick-font-weight-body
--wick-font-weight-emphasis
--wick-line-height-body
```

### 5.4 Spacing / radius / shadow semantic

```text
--wick-space-page
--wick-space-section
--wick-space-stack
--wick-space-inline
--wick-radius-control
--wick-radius-panel
--wick-shadow-panel
--wick-shadow-overlay
```

### 5.5 Focus

```text
--wick-focus-ring-color
--wick-focus-ring-width
--wick-focus-ring-offset
```

Focus must remain visible in light and dark; never `outline: none` without replacement ring.

### 5.6 Motion semantic

```text
--wick-motion-duration-fast
--wick-motion-duration-normal
--wick-motion-easing-standard
```

### 5.7 Z-index semantic

```text
--wick-z-index-sticky
--wick-z-index-overlay
--wick-z-index-modal
--wick-z-index-toast
```

## 6. Component-token boundary

```text
I2 = raw + semantic + themes (+ optional empty component token stubs)
I3 = foundation components consume semantic tokens; may add thin --wick-button-* etc.
I4 = StatusBadge/Alert consume status semantic tokens; must not invent new status meanings
```

Rules:

1. Component tokens may only alias semantic tokens (no new hex).
2. Components must not hardcode product colors.
3. Status components must not encode profit/loss via green/red.
4. DemoDataLabel (if added later) uses INFORMATIONAL/ATTENTION tokens — not SUCCESS-as-profit.

## 7. Light theme

```text
DEFAULT_THEME = light
ACTIVATION = :root, html[data-theme="light"], .wick-theme-light
```

Light is the primary product theme (operations center, not dark-gamer).

Required: all semantic color tokens defined; canvas/panel readable; status pairs AA contrast on their intended backgrounds.

## 8. Dark theme

```text
SUPPORTED = true
ACTIVATION = html[data-theme="dark"], .wick-theme-dark
PARITY = functional (same semantic roles), not neon restyle
```

Dark must redefine semantic color tokens (and any component aliases). Raw scales may stay shared. No glow aesthetics; no ticker/casino treatments.

## 9. High-contrast considerations

```text
APPROACH = strengthen border/text/status semantic tokens; optional future data-theme="hc"
NOT_A_THIRD_BRAND = true
REQUIREMENTS =
  - text contrast remains >= WCAG 2.2 AA (prefer stronger)
  - status borders distinguishable without hue-only reliance
  - focus ring thickness/contrast increased if needed
```

I2 implementation must document HC strategy in token README comments; a full HC theme file is optional if semantic tokens already meet stronger targets.

## 10. Typography

Hierarchy (visual direction):

1. Page title
2. Status in plain language
3. Technical detail (mono)

```text
BODY = sans product face
TECHNICAL = mono
PROHIBITED_BRAND_DEFAULTS = Inter | Roboto | Arial as intentional brand stack
```

Zoom: layouts must remain usable at 200% (smoke in later UI increments); tokens use `rem` for font sizes.

## 11. Spacing, radii, shadows

```text
DENSITY = operational medium
SPACING = 4px-based scale via raw; semantic aliases for page/section/stack
RADII = modest; no decorative hero cards
SHADOWS = subtle only; no aggressive glow
```

## 12. Motion and prefers-reduced-motion

```text
@supports / @media (prefers-reduced-motion: reduce) {
  override --wick-motion-duration-* to 0ms (or near-zero)
  disable non-essential transitions
}
```

I2 must ship the reduced-motion overrides alongside motion tokens. Motion is for presence/hierarchy, not noise; no blinking prices.

## 13. Breakpoints

Mirror UX responsive intent (desktop sidebar / tablet collapsible / mobile — from foundation; chrome not built in I2):

| Name | Width |
|------|-------|
| sm | 640px |
| md | 768px |
| lg | 1024px |
| xl | 1280px |

I2 documents the contract; layout components arrive later.

## 14. Z-index

Use the semantic z-index tokens only. Do not scatter magic numbers in future components.

## 15. Focus

```text
KEYBOARD_FOCUS = always visible
FOCUS_TOKEN = --wick-focus-ring-*
SCAFFOLD_TODAY = hardcoded outline in web/src/styles.css (replace in I2 code)
```

## 16. Contrast (WCAG 2.2 AA)

```text
TARGET = WCAG 2.2 Level AA
NORMAL_TEXT = contrast ratio >= 4.5:1
LARGE_TEXT_OR_UI = >= 3:1 where WCAG allows
STATUS_TEXT_ON_STATUS_BG = must pass
TEXT_PRIMARY_ON_CANVAS = must pass
TEXT_PRIMARY_ON_PANEL = must pass
```

I2 code PR must include automated contrast checks for required pairs in light and dark.

## 17. Token source format and versioning

```text
SOURCE = CSS files with custom properties
PREFIX = --wick-
DESIGN_TOKEN_CONTRACT_VERSION = 1.0.0
VERSION_TOKEN = --wick-design-token-contract-version: "1.0.0"
```

Also export version in a tiny TS constant at I2 code time for unit tests (e.g. `DESIGN_TOKEN_CONTRACT_VERSION = '1.0.0'`), without introducing a theme runtime.

### Versioning rules

| Change | Version impact |
|--------|----------------|
| Add optional token | MINOR |
| Change semantic meaning of existing token | MAJOR |
| Rename/remove token | MAJOR |
| Adjust raw hex without semantic rename if contrast still passes | PATCH (still requires contrast tests) |

### Deprecation

```text
DEPRECATION = mark in comments + keep alias for one increment grace
REMOVAL = next MAJOR after grace
FORBIDDEN = silent removal of status semantic keys
```

## 18. CSS output strategy

Recommended layout under `web/` (adjustable at I2 code if equivalent):

```text
web/src/styles/tokens/raw.css
web/src/styles/tokens/semantic.css
web/src/styles/tokens/themes/light.css
web/src/styles/tokens/themes/dark.css
web/src/styles/tokens/motion.css
web/src/styles/tokens/index.css   # imports all
web/src/styles.css               # imports tokens; removes product hardcodes
```

Strategy:

1. Hand-author CSS custom properties.
2. Import token index from app entry styles.
3. Theme via `data-theme` on `html` (default light).
4. No CSS-in-JS theme provider required.
5. No Tailwind required for DS core.
6. Scaffold page may keep minimal structure CSS; colors/focus must move to tokens in I2 code.

## 19. Validation (future I2 code)

Mandatory tests when `I2_IMPLEMENTATION_AUTHORIZED=true` and code lands:

```text
1. DESIGN_TOKEN_CONTRACT_VERSION equals 1.0.0 at first ship
2. Required semantic keys exist in light and dark
3. Required contrast pairs pass WCAG 2.2 AA
4. Reduced-motion overrides exist
5. No new hardcoded product hex in component files (policy test / lint)
6. Existing web typecheck/lint/unit/a11y/build remain green
```

This docs PR does not add those tests.

## 20. Implementation authorization gate

```text
AUTHORIZATION_DECISION = AUTHORIZED_WITH_CONDITIONS
I2_IMPLEMENTATION_AUTHORIZED = false
```

Conditions before code:

1. Docs package merged
2. Human sets `I2_IMPLEMENTATION_AUTHORIZED=true`
3. Scope limited to tokens/themes/tests described here
4. Constraints in MANDATORY_CONSTRAINTS still respected (no components/Radix/screens)
5. Contrast + version tests included in the code PR

## 21. Prohibited patterns

```text
neon / market-ticker / blinking prices
green/red as profit/loss semantics
color-only status communication (component layer)
hardcoded product colors outside token files
Radix install in I2
foundation/operational components in I2
routes / MVP screens
secrets in CSS
coupling theme to readiness/validate/scheduler state
effect peeking or economic interpretation in token names/comments
```

## 22. Scientific and operational invariants

```text
R3E_SCIENTIFIC_STATE_CHANGE = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```
