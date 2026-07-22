# UX-R3 — Complete Release Proposed Plan

```text
RELEASE = UX-R3
DOCUMENT = UX-R3-COMPLETE-RELEASE-PROPOSED-PLAN
STATUS = PROPOSED_NOT_AUTHORIZED
CHANGE_RISK = MEDIUM
DECISION = REMAINING_SCOPE_RECOMMENDED
DELIVERY_MODEL_RECOMMENDATION = B_SINGLE_BRANCH_SINGLE_PR_SINGLE_FINAL_VALIDATION
ASSESSMENT = docs/ai-impact/UX-R3-COMPLETE-RELEASE_IMPACT_ASSESSMENT.md
SPEC = docs/ai-specs/UX-R3-COMPLETE-RELEASE-ASSESSMENT_SPEC.md
BASELINE_MAIN = cfc057646b371528de6da6a037ac03274fe1d489
UX_R3_STATUS = IN_PROGRESS
UX_R3_I1_STATUS = MERGED
UX_R3_SHOULD_CLOSE_AFTER_I1 = false
DATA_POSTURE = FIXTURE_BACKED_READ_ONLY
BACKEND = false
REAL_DATA = false
```

## Why not close after I1

I1 delivered the Dados Coletados quality surface, but Prontidão still directs Gustavo to Visão Geral for completeness/gaps/duplicates/series counts that Overview does not provide. Inbound cross-nav is missing. Formal acceptance/closure is pending.

## Remaining increment list (frozen recommendation)

```text
REMAINING_INCREMENT_COUNT = 2
REMAINING_INCREMENT_ORDER = I2 → I3

1. UX_R3_I2_COLLECTION_QUALITY_CROSS_NAV_AND_COHERENCE
2. UX_R3_I3_FIXTURE_ACCEPTANCE_AND_CLOSURE
```

### I2 — Cross-nav and coherence

```text
user outcome =
  From Prontidão (and related screens), reach Dados Coletados without a false
  Overview pointer for quality fields.
scope =
  Readiness CollectionState copy + Link;
  thin inbound Related links (Readiness required; Runs/Overview recommended);
  tests; no new route/fixture/VM domain
risk = LOW-MEDIUM
```

### I3 — Fixture acceptance and closure

```text
user outcome =
  Formal acceptance that fixture-backed collection monitoring/quality scope is
  complete, accepted, and governed.
scope = docs + PROJECT stamp + acceptance wording
risk = LOW
```

## Delivery model

```text
B_SINGLE_BRANCH_SINGLE_PR_SINGLE_FINAL_VALIDATION
one branch; one draft PR; checkpoints after I2 and before merge; independent review;
human final validation; stop conditions enforced
```

**Not authorized** by this document. Requires separate human execution prompt.

## Closure wording (for I3, later)

```text
UX-R3 fixture-backed collection monitoring and data-quality scope is complete, accepted, and governed.
```

Must **not** claim real-data completeness, validation readiness, scheduler activation, scientific approval, or R4/R5 unlock.

## Explicit out of remaining scope

```text
replay of proposed I2/I3 product foundations;
Overview quality dashboard;
charts/trends;
real data / FU / ops / R4/R5;
activating Backups/Incidentes/Backlog/Aprovações
```

## Next

```text
NEXT_RECOMMENDED_TASK = UX_R3_REMAINING_RELEASE_SINGLE_EXECUTION
UX_R3_REMAINING_SCOPE_AUTHORIZED = false
UX_R3_REMAINING_IMPLEMENTATION_AUTHORIZED = false
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
