# UX-R3 — Proposed Scope

```text
RELEASE = UX-R3
DOCUMENT = UX-R3-PROPOSED-SCOPE
STATUS = PROPOSED_NOT_FROZEN
CHANGE_RISK = HIGH
DECISION = SCOPE_RECOMMENDED
ASSESSMENT = docs/ai-impact/UX-R3-DISCOVERY-AND-SCOPE_IMPACT_ASSESSMENT.md
SPEC = docs/ai-specs/UX-R3-DISCOVERY-AND-SCOPE_SPEC.md
BASELINE_MAIN = 2fb2bb9da35f70083972bd7c6da64c72055c9a0e
UX_R3_STATUS = NOT_STARTED
DATA_POSTURE = FIXTURE_BACKED_READ_ONLY
BACKEND = false
REAL_DATA = false
RUNTIME_REPOSITORY_ACCESS = false
FUTURE_UNSEEN_RESULTS = false
OPERATIONAL_COMMANDS = false
```

## Direction

```text
UX_R3_RECOMMENDED_DIRECTION = E_COLLECTION_MONITORING_AND_DATA_QUALITY
PLANNED_NAV_TARGET = Dados Coletados (currently inactive)
CANDIDATE_ROUTE_FAMILY = /future-collection/* (exact path decided in I1 authorization)
```

## Indicative increment list (not frozen for single-execution)

```text
PROPOSED_INCREMENT_LIST =
  UX_R3_I1_COLLECTION_DATA_QUALITY_AUTHORIZATION_ASSESSMENT
  UX_R3_I2_COLLECTION_DATA_QUALITY_SCREEN_FOUNDATION
  UX_R3_I3_COLLECTION_QUALITY_DIMENSIONS_AND_NOTICES
  UX_R3_I4_COLLECTION_QUALITY_CROSS_NAV
  UX_R3_I5_COLLECTION_QUALITY_FIXTURE_ACCEPTANCE_AND_CLOSURE

UX_R3_INCREMENT_ORDER = I1 → I2 → I3 → I4 → I5
PROCESS_MODEL = FULL_INCREMENTAL_FLOW
```

This list is **proposed**, not frozen. Single-branch continuous execution is **not** authorized by default.

---

## I1 — Authorization assessment (docs-only)

```text
increment id = UX_R3_I1
title = Collection data-quality authorization assessment
user outcome = Decide route, fixture posture, ViewModel boundary, and security conditions
dependencies = UX-R3 discovery MERGED
risk = MEDIUM
data posture = N/A (docs)
architecture posture = docs-only
acceptance criteria =
  AUTHORIZED_WITH_CONDITIONS or clearer deny/adjust decision;
  route candidate explicit;
  FIXTURE_BACKED_READ_ONLY confirmed;
  no implementation flags flipped true beyond assessment outcome.
```

---

## I2 — Screen foundation (illustrative; unauthorized now)

```text
increment id = UX_R3_I2
title = Fixture-backed Dados Coletados screen foundation
user outcome = Open Dados Coletados and see governed fixture-backed collection quality shell
dependencies = I1 AUTHORIZED + separate implementation prompt
risk = MEDIUM
data posture = FIXTURE_BACKED
architecture posture = new screen + VM + fixture; activate planned nav
acceptance criteria =
  route renders; synthetic disclosure; no fixture selector; no ops controls;
  architecture tests pass.
```

---

## I3 — Quality dimensions and notices

```text
increment id = UX_R3_I3
title = Collection quality dimensions and safety notices
user outcome = Inspect completeness/gaps/duplicates/cutoff/series-count style fields as illustrative
dependencies = I2
risk = MEDIUM
data posture = FIXTURE_BACKED curated static
architecture posture = extend collection-quality VM only
acceptance criteria =
  quality ≠ approval inequalities tested;
  COLLECTION_IN_PROGRESS ≠ READY;
  WINDOW_DAYS_INSUFFICIENT ≠ fault;
  pending ≠ failed styling rules held.
```

---

## I4 — Cross-navigation

```text
increment id = UX_R3_I4
title = Cross-navigation from Runs/Readiness/Overview/Evidence
user outcome = Reach collection-quality entries via internal read-only links
dependencies = I2 (stable ids); I3 recommended
risk = MEDIUM
data posture = FIXTURE_BACKED ids only
architecture posture = Related links pattern (as UX-R2 I4)
acceptance criteria =
  internal router links only; no external href; no sourcePath navigation;
  deep-link sanitize if used.
```

---

## I5 — Fixture acceptance and closure

```text
increment id = UX_R3_I5
title = Fixture acceptance and UX-R3 closure
user outcome = Formal acceptance that fixture-backed collection monitoring/quality scope is complete and governed
dependencies = I2–I4
risk = LOW
data posture = FIXTURE_BACKED acceptance wording
architecture posture = docs + minor copy
acceptance criteria =
  final review APPROVED; checkpoints PASS; exact acceptance wording;
  scientific/operational truth unchanged.
```

## Closure criteria (release-level, when later stamped)

```text
UX-R3 fixture-backed collection monitoring and data-quality scope is complete, accepted, and governed.
```

Must **not** claim real-data completeness, validation readiness, scheduler activation, scientific approval, or R4/R5 unlock.

## Explicit deferred / blocked

```text
DEFERRED = A, B, C, F
BLOCKED = G, H, I
REJECTED = D (redundant with UX-R2 Evidence Explorer), J (idle wait)
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

Official wording:

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```
