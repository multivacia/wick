# UX-R1-I6G-RUNS-SCREEN-IMPLEMENTATION — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = RUNS-SCREEN-IMPLEMENTATION-AUTHORIZATION-ASSESSMENT-001
TASK_ID = RUNS-SCREEN-IMPLEMENTATION-001
TITLE = Runs Screen Implementation
INCREMENT = I6G
PHASE = IMPLEMENTATION
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = true
RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED = true
RUNS_SCREEN_MERGE_AUTHORIZED = false
READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED = false
HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
REAL_DATA_INTEGRATION_AUTHORIZED = false
OPERATIONAL_ACTIONS_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE_CHANGE = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 26dfee723dbca8eb7625b711aa505ca2b10a5e11
ANALYZED_AT = 2026-07-20T17:56:00Z
ANALYZED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = PENDING
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTHORIZATION_DECISION = HUMAN_AUTHORIZED_FOR_THIS_TASK
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
FRONTEND_LOCATION = web/
I6F_DECISION = AUTHORIZED_WITH_CONDITIONS
I6F_RECOMMENDED_IMPLEMENTATION_BOUNDARY = RUNS_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; NO_VISIBLE_FIXTURE_SELECTOR; NO_REAL_DATA; NO_OPERATIONAL_ACTIONS
FIXTURE_ID = current_project_state_illustrative
ROUTE = /future-collection/runs
SCREEN = Execuções
```

G1 note: authorization covers **only** the read-only fixture-backed Execuções (`/future-collection/runs`) screen. It does **not** authorize Readiness/Host-Scheduler screens, fixture UI selectors, real-data adapters, operational buttons, scheduler activation, or scientific validation. Overview remains preserved.

## MANDATORY_CONSTRAINTS

```text
READ_ONLY = true
FIXTURE_BACKED = true
FIXTURE_ID = current_project_state_illustrative
NO_VISIBLE_FIXTURE_SELECTOR = true
NO_REAL_DATA = true
NO_OPERATIONAL_ACTIONS = true
NO_NETWORK_CLIENTS = true
NO_BACKEND_API = true
NO_EXTRA_RUNTIME_OR_DEV_DEPENDENCIES = true
TOKEN_ONLY_STYLING = true
REUSE_I3_PRIMITIVES = true
CONSUME_I6B_VIEWMODELS = true
CONSUME_I6C_FIXTURES = true
REPLACE_RUNS_PLACEHOLDER_ONLY = true
PRESERVE_OVERVIEW_SCREEN = true
PRESERVE_OTHER_ROUTE_PLACEHOLDERS = true
IN_PROGRESS_IS_NOT_FAULT = true
UNKNOWN_IS_NOT_FAULT = true
EMPTY_IS_NOT_FAULT = true
RED_ONLY_FOR_CONFIRMED_FAULT = true
NO_FAKE_ZEROES = true
NO_FABRICATED_LINKS_OR_METRICS = true
NO_B3_FILTERS_PAGINATION_DETAIL_PARITY = true
NO_FABRICATED_B3_EXTRA_FIELDS = true
```

## Objective

Implement the Wick product screen **Execuções** at `/future-collection/runs`, fixture-backed via I6C catalog and I6B Runs ViewModels, answering which runs exist, their status, timing, counts, store delta, idempotency, failure reason, and evidence — plain language first, technical evidence second.

## Scope in

```text
web/src/screens/runs/**
web/src/app/AppRoutes.tsx (Runs route only)
web/src/fixtures/scenarios.ts (optional synthetic in_progress run for collection_in_progress — Runs list only)
web/tests/screens/runs/**
web/tests/a11y/runs.a11y.test.tsx
docs/ai-impact|ai-specs|ai-reviews + reports handoff for I6G
docs/PROJECT.md status fields for I6G in-progress (if required)
```

## Scope out

```text
READINESS_SCREEN
HOST_SCHEDULER_SCREEN
OVERVIEW_BEHAVIOR_CHANGE
FIXTURE_UI_PRODUCT_SELECTOR
REAL_DATA
NETWORK_FETCHING
OPERATIONAL_ACTIONS
B3_FILTERS_PAGINATION_DETAIL_PARITY
FABRICATED_B3_EXTRA_FIELDS
NEW_DEPENDENCIES
SCHEDULER_ACTIVATION
SCIENTIFIC_VALIDATION
```

## Product fixture selection

```text
PRODUCT_ROUTE_FIXTURE = current_project_state_illustrative
VISIBLE_FIXTURE_SELECTOR = false
TEST_SCENARIO_COVERAGE = collection_in_progress; confirmed_collection_fault; partial_unknown_data; empty_no_runs; current_project_state_illustrative
```

Internal loader may accept a fixture id **for tests only**; the product `RunsScreen` always uses `RUNS_FIXTURE_ID`.

## Risk

| Risk | Mitigation |
|------|------------|
| Fixture/live confusion | Mandatory SyntheticDataNotice labels |
| Fake zeroes / invented fields | Render only supplied ViewModel fields; missing → indisponível |
| IN_PROGRESS painted as fault | StatusBadge informational/cyan; never fault/red |
| EMPTY/UNKNOWN as fault | Distinct empty copy + unknown badge |
| Operational action creep | No buttons; actionHint advisory text only |
| Overview regression | Do not change Overview visuals/behavior |

## Decision

```text
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
AUTHORIZATION_DECISION = HUMAN_AUTHORIZED_FOR_THIS_TASK
READY_FOR_IMPLEMENTATION = true
```
