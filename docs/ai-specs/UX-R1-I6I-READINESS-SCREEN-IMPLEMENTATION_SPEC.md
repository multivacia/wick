# UX-R1-I6I — Readiness Screen Implementation Spec

```text
RELEASE = UX-R1
INCREMENT = I6I
TASK_ID = READINESS-SCREEN-IMPLEMENTATION-001
PHASE = IMPLEMENTATION
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_STATUS = COMPLETE
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
IMPACT = docs/ai-impact/UX-R1-I6I-READINESS-SCREEN-IMPLEMENTATION_IMPACT_ASSESSMENT.md
ROUTE = /future-collection/readiness
SCREEN = Prontidão
FIXTURE_ID = current_project_state_illustrative
READ_ONLY = true
FIXTURE_BACKED = true
NO_VISIBLE_FIXTURE_SELECTOR = true
```

## Objective

Deliver the fixture-backed, read-only **Prontidão** product screen at `/future-collection/readiness`, consuming merged `ReadinessViewModel` fields only.

## Behavior

Answer in plain language first:

1. Can future validation already be considered?
2. How many future days were observed?
3. How many days are required?
4. Which rule blocks readiness?
5. Is collection still advancing (without fabricating health metrics)?
6. Was validation executed?
7. Was effect peeking performed?
8. What is the next safe action?

## Sections

```text
PageHeader
SyntheticDataNotice
ReadinessStatusCard
WindowProgress
BlockingReason
ValidationExecutionState
EffectPeekingState
CollectionState
NextSafeAction
EvidenceReference
PartialUnknownState
```

Visible synthetic labels: `Dados ilustrativos`, `Synthetic fixture`, `Não representa evidência operacional real`.

## Semantics

```text
NOT_READY != FAULT (amber, never red)
READY != STRATEGY_APPROVED / PROFITABILITY_CONFIRMED
UNKNOWN / MISSING != ZERO
VALIDATION_NOT_EXECUTED != VALIDATION_FAILED
EFFECT_PEEKING_FALSE != EFFECT_NOT_REPORTED
COLLECTION_IN_PROGRESS != READY
```

Window progress is linear/textual with illustrative disclosure. No gauge. Collection health fields are disclosed as out of ViewModel scope.

## Architecture

```text
web/src/screens/readiness/**
AppRoutes: replace readiness placeholder only
Nav label: Prontidão
Optional test fixture: readiness_ready_illustrative
Product fixture remains current_project_state_illustrative
```

## Out of scope

Host/Scheduler screen, real data, validation/collection/scheduler controls, fabricated collection health / cutoff / gaps / duplicates, B3 parity, new dependencies, scientific interpretation change.
