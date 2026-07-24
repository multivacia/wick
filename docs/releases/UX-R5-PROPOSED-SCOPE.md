# UX-R5 — Proposed Scope (Deferral)

```text
RELEASE = UX-R5
DOCUMENT = UX-R5-PROPOSED-SCOPE
STATUS = DEFER_RECOMMENDED_NOT_AUTHORIZED
CHANGE_RISK = MEDIUM
DECISION = DEFER_RECOMMENDED
UX_R5_RECOMMENDATION = NO_NEW_UX_RELEASE_NOW
UX_R5_DIRECTION = NONE
UX_R5_DELIVERY_MODEL = D_DEFER_UX_R5
ASSESSMENT = docs/ai-impact/UX-R5-DISCOVERY-AND-SCOPE_IMPACT_ASSESSMENT.md
SPEC = docs/ai-specs/UX-R5-DISCOVERY-AND-SCOPE_SPEC.md
BASELINE_MAIN = 259092ec8b66a809dfb5d23d4ef0ddd65d455d64
UX_R5_STATUS = NOT_STARTED
UX_R5_SCOPE_AUTHORIZED = false
UX_R5_IMPLEMENTATION_AUTHORIZED = false
DATA_POSTURE = N/A_NO_PRODUCT_INCREMENT
BACKEND = false
REAL_DATA = false
```

## Why UX-R5 is deferred now

UX-R4 closed the governed Decision Ledger + evidence-catalog refresh gap. The remaining honest constraint is scientific/ops: future-unseen window still insufficient, R3E gate pending, scientific R4 blocked, scientific R5 not started, host deferred, scheduler blocked.

Opening a new UX release would invent product work without changing Gustavo’s safe next action (wait for sufficient future window / continue collection / do not validate or activate).

## Proposed product increments

```text
UX_R5_INCREMENT_COUNT = 0
UX_R5_INCREMENT_IDS = NONE
UX_R5_INCREMENT_ORDER = NONE
UX_R5_OBJECTIVE = NONE
UX_R5_PRIMARY_USER_OUTCOME = NONE
UX_R5_MAXIMUM_BOUNDARY = NO_PRODUCT_SCOPE
```

## Deferral

```text
DEFERRAL_REASON =
  Fixture-backed inspection loop already covers the wait state after UX-R4;
  binding constraint is future-unseen readiness, not missing UX.

REQUIRED_TRIGGER =
  READINESS leaves NOT_READY/WINDOW_DAYS_INSUFFICIENT and/or R3E_GATE advances
  beyond PENDING_FUTURE_UNSEEN_DATA under separate scientific authorization;
  or a human-authorized ops posture change that creates a new honest UX problem.

WHAT_CAN_PROCEED_INSTEAD =
  Existing screens; scientific collection; accepted operational debt without
  activation fiction; docs/governance only.

REASSESSMENT_CONDITION =
  New UX-R5 discovery prompt after required trigger; no silent scope reopen.
```

## Explicit out of scope (now)

```text
new UX-R5 product increments
new routes / nav items / screens
Backlog / Aprovações activation
hypothesis registry / experiment planning workspaces
reassessment authorization queues
future-unseen result surfaces
R4/R5 promotion UX
host/scheduler activation UX
real-data adapters
quality charts / governance timeline duplicates
```

## Delivery model

```text
D_DEFER_UX_R5
```

**Not authorized** as a product release. Discovery may merge as docs-only; UX-R5 remains **NOT_STARTED**.

## Next

```text
NEXT_RECOMMENDED_TASK = UX_R5_REASSESSMENT_AFTER_FUTURE_UNSEEN_READINESS_CHANGE
NEXT_ITEM = UX_R5_PRODUCT_SCOPE_NOT_AUTHORIZED
UX_R5_SCOPE_AUTHORIZED = false
UX_R5_IMPLEMENTATION_AUTHORIZED = false
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
SCIENTIFIC_CONCLUSION = UNCHANGED
```

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```
