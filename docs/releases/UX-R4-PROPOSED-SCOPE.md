# UX-R4 — Proposed Scope

```text
RELEASE = UX-R4
DOCUMENT = UX-R4-PROPOSED-SCOPE
STATUS = PROPOSED_NOT_AUTHORIZED
CHANGE_RISK = MEDIUM
DECISION = SCOPE_RECOMMENDED
UX_R4_RECOMMENDATION = MULTIPLE_BOUNDED_INCREMENTS
UX_R4_DIRECTION = F_GOVERNED_DECISION_LEDGER_REFRESH
UX_R4_DELIVERY_MODEL = A_FULL_INCREMENTAL_FLOW
ASSESSMENT = docs/ai-impact/UX-R4-DISCOVERY-AND-SCOPE_IMPACT_ASSESSMENT.md
SPEC = docs/ai-specs/UX-R4-DISCOVERY-AND-SCOPE_SPEC.md
BASELINE_MAIN = 16bf2bd72c26cc804f7e630b504b74878848bed2
UX_R4_STATUS = NOT_STARTED
UX_R4_SCOPE_AUTHORIZED = false
UX_R4_IMPLEMENTATION_AUTHORIZED = false
DATA_POSTURE = FIXTURE_BACKED_READ_ONLY
BACKEND = false
REAL_DATA = false
```

## Why UX-R4 is recommended now

UX-R3 closed the collection-quality and coherence gap. Remaining honest fixture-backed value is governance clarity: accepted / blocked / deferred decisions, reassessment triggers, and non-inferences — especially after UX-R3 closure, while the Evidence catalog fixture clock still reads `2026-07-21`.

Scientific and operational capabilities remain blocked; inventing R4/R5, real-data, or activation UX would be dishonest.

## Proposed increments (frozen sketch; unauthorized)

```text
UX_R4_INCREMENT_COUNT = 3
UX_R4_INCREMENT_ORDER = I1 → I2 → I3

1. UX_R4_I1_DECISION_LEDGER_AUTHORIZATION_ASSESSMENT
2. UX_R4_I2_EVIDENCE_DECISION_LEDGER_FIXTURE_REFRESH
3. UX_R4_I3_FIXTURE_ACCEPTANCE_AND_CLOSURE
```

### I1 — Authorization assessment (first next task)

```text
user outcome = freeze exact Evidence Explorer boundary before any product work
scope = docs-only authorization assessment
risk = LOW
```

### I2 — Fixture refresh + decision ledger presentation

```text
user outcome =
  On /governance/evidence, inspect accepted/blocked/deferred decisions and
  reassessment triggers with curated post-UX-R3 catalog freshness.
scope =
  existing Evidence Explorer only; fixture + presentation; no new route
risk = MEDIUM
```

### I3 — Fixture acceptance and closure

```text
user outcome = formal fixture-backed acceptance after I2 validation
scope = docs + acceptance stamp preparation
risk = LOW
```

## Maximum boundary

```text
/governance/evidence only
fixture-backed read-only
no Backlog/Aprovações activation
no scientific R4 unlock
no R5 start
no real data / future-unseen / validate / peek / host / scheduler
```

## Explicit out of scope

```text
new governance timeline screen
quality charts
experiment planning/comparison workspaces
operational activation
real-data adapters
R4/R5 promotion UX
```

## Delivery model

```text
A_FULL_INCREMENTAL_FLOW
authorization assessment first; no product until separately authorized
```

**Not authorized** by this document. Requires separate human authorization for I1.

## Next

```text
NEXT_RECOMMENDED_TASK = UX_R4_I1_DECISION_LEDGER_AUTHORIZATION_ASSESSMENT
UX_R4_SCOPE_AUTHORIZED = false
UX_R4_IMPLEMENTATION_AUTHORIZED = false
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
