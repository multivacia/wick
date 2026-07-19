# UX-R1-I2 — Design Tokens and Themes — Implementation Specification

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = DESIGN-TOKENS-AND-THEMES-001
TASK_ID = DESIGN-TOKENS-AND-THEMES-IMPLEMENTATION-001
INCREMENT = I2
PHASE = IMPLEMENTATION
CHANGE_RISK = MEDIUM
SPEC_STATUS = IMPLEMENTED
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-I2-DESIGN-TOKENS-AND-THEMES-IMPLEMENTATION_IMPACT_ASSESSMENT.md
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_STATUS = COMPLETE
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
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE_CHANGE = false
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
DESIGN_TOKEN_CONTRACT_VERSION = 1.0.0
FRONTEND_LOCATION = web/
NEW_RUNTIME_DEPENDENCIES = 0
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
CREATED_AT = 2026-07-19T20:20:00Z
```

## 1. Purpose

Document the I2 code delivery: `--wick-*` raw/semantic tokens, light/dark themes, system preference bootstrap, focus/motion/reduced-motion baselines, and automated tests.

## 2. Mapping to merged assessment contract

Follows `docs/ai-specs/UX-R1-I2-DESIGN-TOKENS-AND-THEMES_SPEC.md` with these documented extensions from the human implementation prompt:

| Extension | Rationale |
|-----------|-----------|
| Prompt status set (`healthy`, `completed`, `not_ready`, `deferred`, `unknown`, `fault`, …) | Required by implementation authorization prompt |
| Merged-spec aliases (`success`→`completed`, `error`→`fault`, …) | Preserve assessment contract compatibility |
| Prompt surface aliases (`background`, `surface`, `surface_elevated`, `surface_muted`, `border`, `interactive*`) | Required semantic inventory |
| Minimal `theme.ts` bootstrap | Prompt requires theme resolution/tests; not a CSS-in-JS engine |

## 3. File layout

```text
web/src/styles/tokens/raw.css
web/src/styles/tokens/semantic.css
web/src/styles/tokens/themes/light.css
web/src/styles/tokens/themes/dark.css
web/src/styles/tokens/motion.css
web/src/styles/tokens/index.css
web/src/styles.css
web/src/theme/contract.ts
web/src/theme/contrast.ts
web/src/theme/theme.ts
web/src/main.tsx
web/index.html  (FOUC guard)
web/tests/theme/theme.test.ts
web/tests/tokens/tokens.test.ts
web/tests/tokens/contrast.test.ts
web/tests/a11y/theme.a11y.test.tsx
```

## 4. Theme bootstrap

```text
DEFAULT = light when preference invalid
SYSTEM = matchMedia('(prefers-color-scheme: dark)')
ATTR = html[data-theme="light"|"dark"]
CLASS = .wick-theme-light | .wick-theme-dark
PREFERENCE_ATTR = data-theme-preference (optional: light|dark|system)
PERSISTENCE = none required
```

`bootstrapTheme()` runs before React render. Inline `index.html` script reduces FOUC.

## 5. Accessibility

```text
WCAG = 2.2 AA
FOCUS = --wick-focus-ring-* via :focus-visible
REDUCED_MOTION = @media (prefers-reduced-motion: reduce) zeros durations
COLOR_NOT_SOLE_STATUS = documented; component layer later must add text/icon
HC_FULL_THEME = deferred; dark/light semantic tokens strengthened first
```

Automated contrast tests cover text-on-canvas/panel and status badge fg/bg pairs for light and dark.

## 6. Non-goals (enforced)

```text
NO_COMPONENTS
NO_RADIX
NO_ROUTER
NO_SHELL
NO_SCREENS
NO_VIEWMODEL
NO_FIXTURES
NO_OPERATIONAL_DATA
NO_COMPONENT_TOKENS
NEW_RUNTIME_DEPENDENCIES = 0
```

## 7. Validation commands

```text
pytest
ruff check .
python scripts/validate_ai_governance_artifacts.py <impact>
pnpm --dir web typecheck
pnpm --dir web lint
pnpm --dir web test
pnpm --dir web test:a11y
pnpm --dir web build
pnpm --dir web audit --audit-level high
```
