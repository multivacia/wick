# UX-R1-I6D — Screen Implementation Authorization Assessment

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
TASK_ID = SCREEN-IMPLEMENTATION-AUTHORIZATION-ASSESSMENT-001
TITLE = Screen Implementation Authorization Assessment
INCREMENT = I6D
PHASE = AUTHORIZATION_ASSESSMENT
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
ASSESSMENT_ONLY = true
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_SCOPE = AUTHORIZATION_ASSESSMENT_DOCUMENTATION_ONLY
IMPLEMENTATION_EXECUTION_AUTHORIZED = false
DECISION = AUTHORIZED_WITH_CONDITIONS
SCREEN_SCOPE_RECOMMENDATION = OVERVIEW_FIRST
RECOMMENDED_SCREEN_SEQUENCE = OVERVIEW → READINESS → RUNS → HOST_SCHEDULER
FIRST_AUTHORIZED_SCREEN = Visão Geral
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
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
BASE_SHA = bedb02a11213bb327d96b16a7f2171fd93d3ac79
ANALYZED_AT = 2026-07-20T13:35:00Z
ANALYZED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
NEXT_RECOMMENDED_TASK = I6_OVERVIEW_SCREEN_IMPLEMENTATION
NEXT_ITEM = I6_OVERVIEW_SCREEN_SEPARATE_IMPLEMENTATION_TASK
```

G1 note: This assessment may recommend **AUTHORIZED_WITH_CONDITIONS** for a future Overview-first screen task. It does **not** flip `I6_SCREEN_IMPLEMENTATION_AUTHORIZED` or `IMPLEMENTATION_EXECUTION_AUTHORIZED` to true. Screen implementation requires a separate human-authorized implementation prompt.

## SUMMARY

Prerequisites I2, I3, I5, I6B, and I6C are merged. The project is ready to authorize a **narrow, fixture-backed, read-only Overview screen** as the first visual product surface. Combined MVP screens or real-data integration are not authorized.

## 1. Prerequisite inventory

| Increment | Status | Role for screens |
|-----------|--------|------------------|
| I2 tokens/themes | MERGED | Status colors + semantic tokens |
| I3 primitives | MERGED | PageHeader, Section, StatusBadge, Alert, Card, Stack, etc. |
| I5 shell/router | MERGED | Routes + placeholders for `/overview` and siblings |
| I6B ViewModels | MERGED | Pure builders for Overview/Runs/Readiness/HostScheduler |
| I6C fixtures | MERGED | Synthetic catalog + `buildFixtureViewModels` |

## 2. Assessment dimensions

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Architectural readiness | READY | Shell + routes + primitives + ViewModels + fixtures stacked |
| ViewModel completeness | READY_FOR_OVERVIEW | Overview aggregation present; deeper screen-specific UX copy can refine later |
| Fixture completeness | READY | Includes `current_project_state_illustrative` and fault/non-fault coverage |
| Semantic-status safety | READY | NOT_READY/BLOCKED/DEFERRED ≠ FAULT; StatusBadge tokens exist |
| Accessibility readiness | READY_WITH_CONDITIONS | I3 primitives + shell a11y tests; screen-level a11y still required in implementation |
| Responsive readiness | READY | I5 shell responsive; screen content must not break layout |
| Route readiness | READY | `/overview` placeholder exists; no architectural expansion needed |
| Test readiness | READY_WITH_CONDITIONS | VM/fixture tests exist; screen unit/a11y tests required next |
| Visual-system readiness | READY | Tokens + primitives sufficient for read-only operational UI |
| False operational meaning risk | MEDIUM | Mitigate with synthetic labels and plain-language first |
| Fixture/live-data confusion risk | MEDIUM | Mitigate with mandatory “Dados ilustrativos” chrome |
| Accidental operational action risk | LOW_IF_READ_ONLY | No buttons that activate scheduler/collection/validate |
| Reviewability | HIGH for Overview-first | Small increment |
| Increment size | SMALL if Overview-only | Combined MVP would be too large |

## 3. Mandatory safety answers

1. **Can every proposed screen render without inventing facts?** Yes, if fed only by ViewModels/fixtures and missing fields stay null/unknown.
2. **Are synthetic fixtures unmistakably labeled?** Yes (`synthetic`, `illustrative`, `notOperationalEvidence`, EXAMPLE_LABEL).
3. **Can NOT_READY / BLOCKED / DEFERRED / UNKNOWN / FAULT remain visually distinct?** Yes via I2/I3 status semantics.
4. **Can screens remain read-only?** Yes — no action controls in first increment.
5. **Can operational actions remain absent?** Yes — out of scope.
6. **Can real-data integration remain fully blocked?** Yes — fixtures only.
7. **Can the current shell support screens without architectural expansion?** Yes — replace Overview placeholder content only.
8. **Are ViewModels sufficient, or are contract gaps present?** Sufficient for Overview first; Runs/Readiness/Host can follow after visual validation.
9. **Which screen provides the best first demonstrable value?** Visão Geral.
10. **What must remain out of scope?** Real data, network fetch, scheduler/collection/validation actions, auth/permissions, financial execution, fixture UI selectors as product controls, combined four-screen MVP in one task.

## 4. Screen sequence recommendation

```text
SCREEN_SCOPE_RECOMMENDATION = OVERVIEW_FIRST
RECOMMENDED_SCREEN_SEQUENCE = OVERVIEW → READINESS → RUNS → HOST_SCHEDULER
FIRST_AUTHORIZED_SCREEN = Visão Geral
```

Rationale: Overview exercises end-to-end composition (collection + readiness + host/scheduler summaries + blockers + next safe action) with the earliest visual validation, while remaining read-only and fixture-backed. Combined MVP increases review/a11y risk. Host/Scheduler first would over-emphasize deferred/blocked debt before the operational summary is visible.

## 5. Authorization decision

```text
DECISION = AUTHORIZED_WITH_CONDITIONS
```

### Conditions (C1–C10) for the next implementation task

1. **Overview only** — do not implement Runs/Readiness/Host screens in the same task.
2. **Fixture-backed only** — wire through I6C catalog/runner; no adapters/network.
3. **Mandatory synthetic labeling** visible in UI (“Dados ilustrativos” / Synthetic fixture).
4. **Read-only** — no operational action buttons, forms that mutate, or command triggers.
5. **Semantic inequalities preserved** — NOT_READY/BLOCKED/DEFERRED never render as fault/red.
6. **No real-data integration** — `OPERATIONAL_DATA_INTEGRATION_AUTHORIZED` remains false.
7. **Shell placeholders for other routes unchanged**.
8. **Screen a11y tests required** (WCAG 2.2 AA for Overview content).
9. **No new runtime/dev dependencies** unless separately authorized.
10. **Separate human prompt** must set `I6_SCREEN_IMPLEMENTATION_AUTHORIZED=true` for Overview only; this assessment does not flip execution flags.

### Explicit out of scope

```text
REAL_DATA
NETWORK_FETCHING
SCHEDULER_ACTIONS
COLLECTION_ACTIONS
VALIDATION_ACTIONS
AUTHENTICATION
PERMISSIONS
FINANCIAL_EXECUTION
COMBINED_MVP_SCREENS
FIXTURE_UI_PRODUCT_SELECTOR
I6D_RUNTIME_IMPLEMENTATION_IN_THIS_TASK
```

## 6. Next task boundary

```text
NEXT_RECOMMENDED_TASK = I6_OVERVIEW_SCREEN_IMPLEMENTATION
NEXT_ITEM = I6_OVERVIEW_SCREEN_SEPARATE_IMPLEMENTATION_TASK
IMPLEMENTATION_EXECUTION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
```

## Decisão

```text
I6D_DECISION = AUTHORIZED_WITH_CONDITIONS
ASSESSMENT_STATUS = COMPLETE
READY_FOR_SEPARATE_OVERVIEW_SCREEN_TASK = true
```
