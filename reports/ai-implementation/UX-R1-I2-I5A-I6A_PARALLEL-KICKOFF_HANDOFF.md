# UX-R1 — I2 / I5A / I6A Parallel Kickoff Handoff

```text
STATUS = PARALLEL_WORKSTREAMS_OPEN
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
ACTION = PARALLEL_WORKSTREAM_KICKOFF
REPOSITORY = multivacia/wick
BASE_BRANCH = main
MAIN_BASE_SHA = 221aacc7141697403e9bbbc9f8690953b683e3a9
COORDINATION_BRANCH = cursor/ux-r1-i2-i5a-i6a-parallel-kickoff-1b6b
CREATED_AT = 2026-07-19T17:01:22Z
CREATED_BY = cursor-agent
AUTOMATIC_MERGE_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## Verified predecessor state

```text
PR51_STATUS = MERGED
PR51_MERGE_COMMIT = c2835921aa15fc1ed2fe8864872bfb1358be02df
PR52_STATUS = MERGED
PR53_STATUS = MERGED
PR54_STATUS = MERGED
I1_IMPLEMENTATION_STATUS = MERGED
FRONTEND_LOCATION = web/
FRONTEND_FRAMEWORK = React
LANGUAGE = TypeScript
BUILD_TOOL = Vite
PACKAGE_MANAGER = pnpm
NODE_VERSION = 22
UX_B3_STATUS = MERGED
UX_B4_STATUS = MERGED
```

## Parallel workstreams

```text
I2_BRANCH = cursor/ux-r1-i2-design-tokens-assessment-1b6b
I2_PR = https://github.com/multivacia/wick/pull/55
I2_HEAD_SHA = ee01c3ce64010b72b06715cc2dbab85b0e32e6b6
I2_STATUS = ASSESSMENT_IN_PROGRESS
I2_TASK_ID = DESIGN-TOKENS-AND-THEMES-001
I2_PHASE = AUTHORIZATION_AND_SPECIFICATION
I2_AUTHORIZATION_DECISION = AUTHORIZED_WITH_CONDITIONS
I2_HANDOFF = reports/ai-implementation/UX-R1-I2-DESIGN-TOKENS-AND-THEMES_HANDOFF.md

I5A_BRANCH = cursor/ux-r1-i5a-application-shell-architecture-1b6b
I5A_PR = https://github.com/multivacia/wick/pull/56
I5A_HEAD_SHA = b8b1c923d3de4673aca7a7249a84422c9662ea0a
I5A_STATUS = ARCHITECTURE_IN_PROGRESS
I5A_TASK_ID = APPLICATION-SHELL-AND-NAVIGATION-ARCHITECTURE-001
I5A_PHASE = ARCHITECTURE_AND_SPECIFICATION
I5A_HANDOFF = reports/ai-implementation/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_HANDOFF.md

I6A_BRANCH = cursor/ux-r1-i6a-overview-data-fixtures-1b6b
I6A_PR = https://github.com/multivacia/wick/pull/57
I6A_HEAD_SHA = 09abaaababe6d0e471deaa10711a248ac7119f0e
I6A_STATUS = DATA_PREPARATION_IN_PROGRESS
I6A_TASK_ID = OVERVIEW-SCREEN-DATA-AND-FIXTURE-PREPARATION-001
I6A_PHASE = DATA_CONTRACT_AND_FIXTURE_PREPARATION
I6A_HANDOFF = reports/ai-implementation/UX-R1-I6A-OVERVIEW-DATA-AND-FIXTURES_HANDOFF.md
```

## Authorization flags (unchanged)

```text
I2_IMPLEMENTATION_AUTHORIZED = false
I5_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## Shared governance invariants preserved

```text
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE = UNCHANGED
```

## PROJECT.md coordination rules

Each workstream branch updates only its own status block:

```text
I2_STATUS = ASSESSMENT_IN_PROGRESS
I5A_STATUS = ARCHITECTURE_IN_PROGRESS
I6A_STATUS = DATA_PREPARATION_IN_PROGRESS
```

Expect rebase before merge. Do not mark another parallel workstream as merged from a sibling branch.

## Validation per workstream

All three independent branches reported:

```text
BACKEND_TESTS = PASS
FRONTEND_TYPECHECK = PASS
FRONTEND_LINT = PASS
FRONTEND_TESTS = PASS
FRONTEND_A11Y = PASS
FRONTEND_BUILD = PASS
GOVERNANCE_VALIDATOR = ERRORS_0_WARNINGS_0
```

## Draft PR policy

```text
ALL_PRS = DRAFT
AUTO_MERGE = false
IMPLEMENTATION_IN_KICKOFF = false
```

## Next human actions

1. Review draft PR #55 (I2 assessment) — decide whether to merge docs and later flip `I2_IMPLEMENTATION_AUTHORIZED`.
2. Review draft PR #56 (I5A architecture) — docs-only; shell implementation remains unauthorized.
3. Review draft PR #57 (I6A data/fixtures) — docs-only; no TypeScript fixtures or adapters yet.
4. Rebase colliding `docs/PROJECT.md` status rows before merge.
5. Keep this coordination PR draft; do not auto-merge.

## Final recommendation

```text
FINAL_RECOMMENDATION = Keep the three workstream PRs independent and draft until human review; do not authorize I2/I5/I6 screen or token code from this coordination package.
```
