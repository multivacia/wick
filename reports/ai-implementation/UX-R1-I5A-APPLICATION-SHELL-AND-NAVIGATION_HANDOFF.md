# UX-R1-I5A — Application Shell and Navigation — Handoff

```text
STATUS = ARCHITECTURE_SPECIFICATION_READY_FOR_HUMAN_REVIEW
RELEASE = UX-R1
WORKSTREAM = I5A
TASK_ID = APPLICATION-SHELL-AND-NAVIGATION-ARCHITECTURE-001
PHASE = ARCHITECTURE_AND_SPECIFICATION
TITLE = Application Shell and Navigation Architecture

IMPACT_ASSESSMENT = docs/ai-impact/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_IMPACT_ASSESSMENT.md
IMPACT_ASSESSMENT_STATUS = APPROVED
SPEC = docs/ai-specs/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_SPEC.md
REVIEW = docs/ai-reviews/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_REVIEW.md
REVIEW_STATUS = APPROVED

BRANCH = cursor/ux-r1-i5a-application-shell-architecture-1b6b
BASE_BRANCH = main
BASE_SHA = 221aacc7141697403e9bbbc9f8690953b683e3a9
IMPLEMENTATION_HEAD = 98a52e229cbd872466c6815635d707a398bb0324
CONTENT_REVIEWED_THROUGH_HEAD = 98a52e229cbd872466c6815635d707a398bb0324
FINAL_CANDIDATE_HEAD = 98a52e229cbd872466c6815635d707a398bb0324
PUSHED = true

CHANGE_RISK = MEDIUM
IMPLEMENTATION_AUTHORIZED = true
AUTHORIZATION_SCOPE = DOCS_PACKAGE_MERGE_CANDIDACY_ONLY
UI_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
I5_IMPLEMENTATION_AUTHORIZED = false
I5A_STATUS = ARCHITECTURE_IN_PROGRESS

NO_ROUTER_INSTALLATION = true
NO_SHELL_IMPLEMENTATION = true
NO_NAVIGATION_COMPONENTS = true
NO_SCREEN_IMPLEMENTATION = true
NO_REAL_DATA = true

HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE_CHANGE = false
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false

MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTOMATIC_MERGE_AUTHORIZED = false
COORDINATED_MERGE_AUTHORIZED = false

RECOMMENDED_FUTURE_ROUTER = react-router (install only after I5 authorization)
MVP_ROUTES = /overview | /collection/runs | /collection/readiness | /ops/host
IA_SECTIONS = Visão Geral | Coleta Futura | Operação | Experimentos | Governança

FULL_TEST_SUITE = PASS (226 passed, 23 skipped)
LINT_STATUS = PASS (ruff check)
GOVERNANCE_VALIDATOR = ERRORS_0_WARNINGS_0 (checked=4)
WEB_TYPECHECK = PASS
WEB_LINT = PASS
WEB_TEST = PASS (2 passed)
WEB_A11Y = PASS (1 passed)
WEB_BUILD = PASS

FINAL_RECOMMENDATION = Approve human merge of docs-only architecture package. Do not install router. Do not implement shell/nav/screens. Do not set I5_IMPLEMENTATION_AUTHORIZED or UI_SCREEN_IMPLEMENTATION_AUTHORIZED. Do not create PR from this agent unless a human requests it. Keep R3E gates and scheduler blocked.
```

## Summary

I5A delivers architecture and specification for the WICK application shell and navigation: IA-aligned hierarchy, MVP route map, URL conventions, frame/header/sidebar/mobile nav, breadcrumbs, page titles, loading/error/not-found boundaries, deep links, keyboard/responsive/landmark/focus contracts, and future access/auth boundaries. React Router is recommended for a **future** I5 task only.

## Files in this package

1. `docs/ai-impact/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_IMPACT_ASSESSMENT.md`
2. `docs/ai-specs/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_SPEC.md`
3. `docs/ai-reviews/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_REVIEW.md`
4. `reports/ai-implementation/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_HANDOFF.md`
5. `docs/PROJECT.md` — additive `| I5A_STATUS | **ARCHITECTURE_IN_PROGRESS** |` only

## Explicit non-changes

```text
web/** unchanged
no React Router dependency
no navigation components
no MVP screens
no I2_STATUS / I6A_STATUS writes
UI_SCREEN_IMPLEMENTATION_AUTHORIZED remains false
no host discovery
no scheduler activation
no validate / collect execution
no PR created by this handoff
```

## Next steps (human)

1. Review and merge this docs package when ready.
2. Open a **separate** authorization/implementation task for I5 before any router install or shell code.
3. Keep parallel I2/I6A tracks independent; do not treat I5A docs merge as UI screen authorization.

## Validation results

```text
uv sync --extra dev = PASS
uv run ruff check . = PASS
uv run pytest -q = PASS (226 passed, 23 skipped)
uv run python scripts/validate_ai_governance_artifacts.py <4 artifacts> = PASS (errors=0 warnings=0)
pnpm --dir web install = PASS
pnpm --dir web typecheck = PASS
pnpm --dir web lint = PASS
pnpm --dir web test = PASS (2 passed)
pnpm --dir web test:a11y = PASS (1 passed)
pnpm --dir web build = PASS
web/** code diff = NONE
```

SHAs recorded after commit:

```text
BASE_SHA = 221aacc7141697403e9bbbc9f8690953b683e3a9
CONTENT_REVIEWED_THROUGH_HEAD = 98a52e229cbd872466c6815635d707a398bb0324
FINAL_CANDIDATE_HEAD = 98a52e229cbd872466c6815635d707a398bb0324
IMPLEMENTATION_HEAD = 98a52e229cbd872466c6815635d707a398bb0324
BRANCH = cursor/ux-r1-i5a-application-shell-architecture-1b6b
PUSHED = true
```
