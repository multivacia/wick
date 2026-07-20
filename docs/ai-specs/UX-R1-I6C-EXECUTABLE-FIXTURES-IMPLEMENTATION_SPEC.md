# UX-R1-I6C — Executable Fixtures Implementation Spec

```text
RELEASE = UX-R1
INCREMENT = I6C
TASK_ID = EXECUTABLE-FIXTURES-IMPLEMENTATION-001
PHASE = IMPLEMENTATION
CHANGE_RISK = MEDIUM
SPEC_STATUS = APPROVED
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-I6C-EXECUTABLE-FIXTURES-IMPLEMENTATION_IMPACT_ASSESSMENT.md
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
IMPLEMENTATION_STATUS = COMPLETE
I6_FIXTURE_IMPLEMENTATION_AUTHORIZED = true
I6_FIXTURE_MERGE_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
CREATED_AT = 2026-07-20T13:03:00Z
```

## Scope

```text
web/src/fixtures/ — metadata, builders, named scenarios, catalog/runner
web/tests/fixtures/ — catalog, semantics, boundary tests
```

Scenarios: healthy_collection_not_ready, collection_in_progress, readiness_window_insufficient, host_discovery_deferred, scheduler_blocked_not_authorized, confirmed_collection_fault, partial_unknown_data, empty_no_runs, mixed_operational_blockers, current_project_state_illustrative.

API: `listFixtureScenarios`, `getFixtureScenario`, `buildFixtureViewModels`.

## Non-scope

```text
OVERVIEW_SCREEN = NOT_IMPLEMENTED
RUNS_SCREEN = NOT_IMPLEMENTED
READINESS_SCREEN = NOT_IMPLEMENTED
HOST_SCHEDULER_SCREEN = NOT_IMPLEMENTED
FIXTURE_UI_SELECTOR = NOT_IMPLEMENTED
REAL_DATA = NOT_INTEGRATED
```
