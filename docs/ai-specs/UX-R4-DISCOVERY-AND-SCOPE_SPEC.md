# UX-R4 Discovery and Scope — Spec

```text
RELEASE = UX-R4
DOCUMENT = UX-R4-DISCOVERY-AND-SCOPE_SPEC
TASK_ID = UX-R4-DISCOVERY-AND-SCOPE-ASSESSMENT-001
STATUS = ASSESSMENT_COMPLETE_UNMERGED
DECISION = SCOPE_RECOMMENDED
UX_R4_RECOMMENDATION = MULTIPLE_BOUNDED_INCREMENTS
UX_R4_DIRECTION = F_GOVERNED_DECISION_LEDGER_REFRESH
UX_R4_DELIVERY_MODEL = A_FULL_INCREMENTAL_FLOW
BASE_SHA = 16bf2bd72c26cc804f7e630b504b74878848bed2
UX_R4_STATUS = NOT_STARTED
UX_R4_SCOPE_AUTHORIZED = false
UX_R4_IMPLEMENTATION_AUTHORIZED = false
```

## Objective

Define the recommended UX-R4 direction after closed UX-R3 without authorizing implementation.

## Recommended direction

```text
F_GOVERNED_DECISION_LEDGER_REFRESH
POSTURE = FIXTURE_BACKED_READ_ONLY
PRIMARY_ROUTE = /governance/evidence
NEW_TOP_LEVEL_ROUTE = false
```

### Primary user outcome

Gustavo can open **Evidências** and answer:

1. What is accepted?
2. What is blocked?
3. What is deferred?
4. What trigger would justify reassessment?
5. What must not be inferred?

## Frozen increment sketch (not authorized)

```text
UX_R4_INCREMENT_COUNT = 3
ORDER = I1 → I2 → I3

I1 = UX_R4_I1_DECISION_LEDGER_AUTHORIZATION_ASSESSMENT
     docs-only authorization of exact fixture/VM/UI boundary

I2 = UX_R4_I2_EVIDENCE_DECISION_LEDGER_FIXTURE_REFRESH
     curated evidence catalog refresh + decision-ledger presentation
     on existing Evidence Explorer only

I3 = UX_R4_I3_FIXTURE_ACCEPTANCE_AND_CLOSURE
     fixture-backed acceptance/closure after I2 validation
```

I2–I3 remain **unauthorized** until I1 authorization assessment merges and a separate human execution prompt exists.

## Maximum boundary

```text
EXISTING_ROUTE_ONLY = /governance/evidence
NO_NEW_TOP_LEVEL_ROUTE
NO_BACKLOG_ROUTE_ACTIVATION
NO_APPROVALS_ROUTE_ACTIVATION
FIXTURE_BACKED_ONLY
READ_ONLY
NO_BACKEND
NO_REAL_DATA
NO_RUNTIME_REPOSITORY_ACCESS
NO_RAW_FILESYSTEM_ACCESS
NO_FUTURE_UNSEEN_RESULTS
NO_VALIDATION_EXECUTION
NO_EFFECT_PEEKING
NO_HOST_DISCOVERY
NO_SCHEDULER_ACTIVATION
NO_OPERATIONAL_COMMANDS
NO_SCIENTIFIC_INTERPRETATION_CHANGE
NO_R4_OR_R5_STATE_CHANGE
```

## Out of scope

```text
scientific R4 unlock
R5 start
real-data adapters
future-unseen progress/results
validation execution UI
effect peeking
host/scheduler activation
backups/incidents operational UI
Backlog / Aprovações activation
hypothesis planning workspace
experiment comparison results beyond explanatory R3E
collection-quality charts/dashboards
trading or profitability claims
```

## Delivery model

```text
A_FULL_INCREMENTAL_FLOW
```

Single-execution (B) may be reconsidered only after I1 freezes a tiny reversible fixture-only boundary with mandatory checkpoints and human final validation.

## Explicit naming boundary

```text
UX_R4 != R4 scientific stage
discovery does not unlock R4
discovery does not start R5
fixture-backed evidence != live truth
```

## First next task

```text
FIRST_NEXT_TASK = UX_R4_I1_DECISION_LEDGER_AUTHORIZATION_ASSESSMENT
NEXT_ITEM = UX_R4_I1_AUTHORIZATION_SEPARATE_ASSESSMENT_NOT_STARTED
```

## Scientific and operational truth (immutable)

```text
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
COLLECTION = IN_PROGRESS
READINESS = NOT_READY
READINESS_REASON = WINDOW_DAYS_INSUFFICIENT
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3D_RESULT = NO_MEASURABLE_EDGE
R3E_STATUS = EXPLORATORY_COMPLETE_PENDING_FUTURE_UNSEEN_DATA
SCIENTIFIC_CONCLUSION = UNCHANGED
R3E_SCIENTIFIC_STATE_CHANGE = false
```

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```
