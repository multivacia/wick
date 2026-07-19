# UX-R1-I1 — Frontend Scaffold and CI — Handoff

```text
STATUS = IMPLEMENTATION_COMPLETE_AWAITING_HUMAN_REVIEW
RELEASE = UX-R1
BACKLOG_ITEM = UX-B2
TASK_ID = FRONTEND-SCAFFOLD-AND-CI-001
INCREMENT = I1
PHASE = IMPLEMENTATION
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-DESIGN-SYSTEM-IMPLEMENTATION-AUTHORIZATION_IMPACT_ASSESSMENT.md
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
BASE_SHA = 2fbf91c248acc381e940d433934633279338ef3b
BRANCH = feature/ux-r1-i1-frontend-scaffold-and-ci
PR = https://github.com/multivacia/wick/pull/51
NODE_VERSION = 22
PNPM_VERSION = 10.33.3
FRONTEND_FRAMEWORK = React
LANGUAGE = TypeScript
BUILD_TOOL = Vite
FRONTEND_LOCATION = web/
DEPENDENCIES_ADDED = react@19.2.7, react-dom@19.2.7, typescript@5.9.3, vite@8.1.5, vitest@4.1.10, eslint@9.39.5, @testing-library/react@16.3.2, jest-axe@10.0.0, axe-core@4.11.0, and pinned toolchain peers (see package.json / lockfile)
FILES_CREATED = web/** scaffold, docs/ai-specs/UX-R1-I1-FRONTEND-SCAFFOLD-AND-CI_IMPLEMENTATION_SPEC.md, reports/ai-implementation/UX-R1-I1-FRONTEND-SCAFFOLD-AND-CI_IMPLEMENTATION_REPORT.md, docs/ai-reviews/UX-R1-I1-FRONTEND-SCAFFOLD-AND-CI_TECHNICAL-AND-SAFETY_REVIEW.md, reports/ai-implementation/UX-R1-I1-FRONTEND-SCAFFOLD-AND-CI_HANDOFF.md, .github/workflows/dependency-review.yml
CI_FILES_CHANGED = .github/workflows/ci.yml (additive frontend-validate job), .github/workflows/dependency-review.yml (new)
BACKEND_TESTS = PASS
FRONTEND_TYPECHECK = PASS
FRONTEND_LINT = PASS
FRONTEND_TESTS = PASS
FRONTEND_A11Y = PASS
FRONTEND_BUILD = PASS
DEPENDENCY_AUDIT = PASS
GOVERNANCE_VALIDATOR = ERRORS_0_WARNINGS_0
CI_STATUS = GREEN
IMPLEMENTATION_HEAD = 29e05752a1e3f11f0ba560df825c4cc47ca9d8a4
CONTENT_REVIEWED_THROUGH_HEAD = 29e05752a1e3f11f0ba560df825c4cc47ca9d8a4
FINAL_CANDIDATE_HEAD = 29e05752a1e3f11f0ba560df825c4cc47ca9d8a4
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
I1_IMPLEMENTATION_STATUS = READY_FOR_HUMAN_REVIEW
I2_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_SCIENTIFIC_STATE_CHANGE = false
BLOCKERS = none for I1 scaffold; GitHub Dependency graph not enabled so dependency-review job is advisory (continue-on-error); pnpm audit/licenses remain enforceable; I2+ still unauthorized; UI screens unauthorized
FINAL_RECOMMENDATION = Human-review and merge I1 scaffold only; do not authorize I2/tokens/components/screens in this PR; keep scheduler blocked; do not run validate; do not unlock R4/R5
CREATED_AT = 2026-07-19T16:12:00Z
UPDATED_AT = 2026-07-19T16:23:38Z
```

Impact path: `docs/ai-impact/UX-R1-DESIGN-SYSTEM-IMPLEMENTATION-AUTHORIZATION_IMPACT_ASSESSMENT.md`

## Documented exception

```text
DEPENDENCY_REVIEW_EXCEPTION = GitHub Dependency graph is not enabled on multivacia/wick; actions/dependency-review-action cannot run as a hard gate. Workflow kept as advisory (continue-on-error). Enforceable substitutes: pnpm audit + pnpm licenses list + exact lockfile pins.
```
