# UX-R1-I6G — Runs Screen Implementation Spec

```text
RELEASE = UX-R1
INCREMENT = I6G
TASK_ID = RUNS-SCREEN-IMPLEMENTATION-001
PHASE = IMPLEMENTATION
CHANGE_RISK = MEDIUM
SPEC_STATUS = APPROVED
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-I6G-RUNS-SCREEN-IMPLEMENTATION_IMPACT_ASSESSMENT.md
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED = true
RUNS_SCREEN_MERGE_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = true
READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED = false
HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
OPERATIONAL_ACTIONS_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = PENDING
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
CREATED_AT = 2026-07-20T17:56:00Z
```

## Scope

```text
ROUTE = /future-collection/runs
SCREEN = web/src/screens/runs/**
ROUTE_WIRING = web/src/app/AppRoutes.tsx (Runs only)
FIXTURE_ID = current_project_state_illustrative
TESTS = web/tests/screens/runs/** + web/tests/a11y/runs.a11y.test.tsx
```

Required sections: PageHeader, SyntheticDataNotice, RunsSummary, RunsCollection, RunStatus, RunTiming, RunCounts, RunStoreDelta, RunIdempotency, RunFailureReason, RunEvidenceReference, EmptyState, PartialUnknownState.

Visible labels: `Dados ilustrativos`, `Synthetic fixture`, `Não representa evidência operacional real`.

## Product data assembly

```text
RUNS_FIXTURE_ID = current_project_state_illustrative
loadRunsScreenData() → buildFixtureViewModels(RUNS_FIXTURE_ID).runs + metadata
NO_VISIBLE_FIXTURE_SELECTOR = true
```

Tests may call `loadRunsScreenData(fixtureId)` or `buildFixtureViewModels(fixtureId)` to cover:

```text
collection_in_progress
confirmed_collection_fault
partial_unknown_data
empty_no_runs
current_project_state_illustrative
```

Optional fixture enrichment (Runs list only): `collection_in_progress` may include a synthetic `in_progress` run row so IN_PROGRESS ≠ FAULT can be exercised without a visible selector.

## Rendering rules

- Plain language first; technical codes second.
- Missing metrics/timestamps → `indisponível` / omit invented values; never coerce to `0`.
- Evidence references as text/`<code>` only (no fabricated links).
- Status via `StatusBadge` + visible Portuguese label; red only for `fault`.
- Empty runs → empty state “Ainda não há execuções registradas.” with technical `NO_RUNS`; not fault.
- Desktop: semantic table; small screens: card/list presentation (responsive CSS) without horizontal overflow.
- No operational buttons.

## Non-scope

```text
READINESS_SCREEN = NOT_IMPLEMENTED
HOST_SCHEDULER_SCREEN = NOT_IMPLEMENTED
FIXTURE_UI_SELECTOR = NOT_IMPLEMENTED
REAL_DATA = NOT_INTEGRATED
OPERATIONAL_ACTIONS = NOT_IMPLEMENTED
B3_FILTERS_PAGINATION_DETAIL = NOT_IMPLEMENTED
```

## Architecture

- Consume I6B `RunsViewModel` / `RunViewModel`.
- Consume I6C `buildFixtureViewModels`.
- Reuse I3 primitives (`PageHeader`, `Section`, `Card`, `Alert`, `StatusBadge`, `Stack`, `Inline`).
- Token-only CSS (`--wick-*`).
- Replace only `/future-collection/runs` placeholder; preserve Overview and other placeholders.

## Acceptance

```text
RUNS_SCREEN = IMPLEMENTED
RUNS_ROUTE = IMPLEMENTED
SYNTHETIC_DATA_NOTICE = IMPLEMENTED
IN_PROGRESS != FAULT
EMPTY != FAULT
NO_OPERATIONAL_BUTTONS = true
ARCHITECTURE_BOUNDARY_TESTS = IMPLEMENTED
ACCESSIBILITY_TESTS = IMPLEMENTED
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
```
