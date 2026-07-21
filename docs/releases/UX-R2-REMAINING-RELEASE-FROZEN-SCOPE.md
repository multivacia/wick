# UX-R2 Remaining Release — Frozen Scope

```text
RELEASE = UX-R2
DOCUMENT = UX-R2-REMAINING-RELEASE-FROZEN-SCOPE
STATUS = FROZEN
CHANGE_RISK = HIGH
DECISION = AUTHORIZED_FOR_SINGLE_EXECUTION_WITH_CONDITIONS
ASSESSMENT = docs/ai-impact/UX-R2-REMAINING-RELEASE-INTEGRAL-PLAN_IMPACT_ASSESSMENT.md
SPEC = docs/ai-specs/UX-R2-REMAINING-RELEASE-INTEGRAL-PLAN_SPEC.md
BASELINE_MAIN = 309589a0d79be012a932ffcad3668b2695917b10
I1_STATUS = MERGED
I1_ROUTE = /governance/evidence
I1_FIXTURE_ID = evidence_catalog_current_state_illustrative
DATA_POSTURE = FIXTURE_BACKED_CURATED_STATIC
BACKEND = false
REAL_DATA = false
RUNTIME_REPOSITORY_ACCESS = false
FUTURE_UNSEEN_RESULTS = false
OPERATIONAL_COMMANDS = false
```

## Frozen remaining increment list

```text
FROZEN_REMAINING_INCREMENT_LIST =
  UX_R2_I2_EVIDENCE_CATALOG_RELEASE_AND_GATE_HISTORY
  UX_R2_I3_EVIDENCE_PROVENANCE_AND_GOVERNANCE_STATE_UX
  UX_R2_I4_EVIDENCE_CROSS_NAV_FROM_MVP_SCREENS
  UX_R2_I5_EVIDENCE_EXPLORER_FIXTURE_ACCEPTANCE_AND_CLOSURE

UX_R2_INCREMENT_ORDER = I2 → I3 → I4 → I5
```

Precondition (docs-only, before I2 product commits in the single-execution branch):

```text
PRECONDITION = UX_R2_I1_EVIDENCE_EXPLORER_POST_MERGE_ACCEPTANCE_STAMP
```

May be the first docs-only commit on the single-execution branch.

---

## I2 — Evidence catalog release and gate history

```text
increment id = UX_R2_I2
business/user outcome =
  Catalog includes representative release/gate/handoff/ops-debt evidence records
  so governance history is inspectable without a separate governance-center app.
route or affected screen = /governance/evidence (fixture enrichment only)
implementation boundary =
  Enrich evidence_catalog_current_state_illustrative only; no new routes/screens;
  no runtime repo read; no full document bodies; no FU payloads.
data posture = FIXTURE_BACKED curated static
scientific posture = UNCHANGED; R3D≠R3E preserved in entries
operational posture = DEBT records illustrative only; no activation
security risks = fabricated completeness; path allowlist violations
architecture impact = fixture + ViewModel filter options only
tests = fixture integrity; class enum; R3D/R3E distinction; path allowlist
checkpoint criteria = CHECKPOINT_INCREMENT_I2 PASS
rollback/reversibility = revert I2 commits on same draft PR
dependencies = I1 MERGED
```

---

## I3 — Provenance and governance-state UX

```text
increment id = UX_R2_I3
business/user outcome =
  Operators clearly see dataOrigin, scientificStage, staleness, known/unknown,
  and safety notices without inferring approval or future validation.
route or affected screen = /governance/evidence
implementation boundary =
  Presentation/UX on Evidence Explorer only; extend existing ViewModel;
  no new screens; no charts/PnL; pending/blocked ≠ fault styling.
data posture = FIXTURE_BACKED
scientific posture = UNCHANGED; strengthen inequalities in UI/tests
operational posture = unchanged
security risks = false confidence; color-only status
architecture impact = Evidence Explorer components + ViewModel labels
tests = semantic notices; status mapping; a11y non-color-only
checkpoint criteria = CHECKPOINT_INCREMENT_I3 PASS
rollback/reversibility = revert I3 commits
dependencies = I2
```

---

## I4 — Cross-navigation from MVP screens

```text
increment id = UX_R2_I4
business/user outcome =
  From Overview/Runs/Readiness/Host/R3E, reach related evidence entries via
  internal read-only links without leaving the governed evidence model.
route or affected screen =
  Existing MVP screens + /governance/evidence (query or path state for selection)
implementation boundary =
  Internal React Router links only; no external URLs; no sourcePath links;
  no new top-level routes; no downloads; deep-link to evidenceId only.
data posture = FIXTURE_BACKED evidenceIds must exist in catalog
scientific posture = UNCHANGED
operational posture = UNCHANGED; no ops buttons
security risks = open-redirect; fabricating evidenceIds; external href injection
architecture impact = small link affordances on existing screens; evidence selection via URL state if already patterned
tests = link targets; no https href; evidenceId resolution; a11y
checkpoint criteria = CHECKPOINT_INCREMENT_I4 PASS
rollback/reversibility = revert I4 commits
dependencies = I2 (stable evidenceIds); I3 recommended
```

---

## I5 — Fixture acceptance and UX-R2 closure

```text
increment id = UX_R2_I5
business/user outcome =
  Formal acceptance that UX-R2 fixture-backed Evidence/Audit Explorer scope is
  complete and governed; freeze deferred backlog.
route or affected screen = docs primarily; optional copy polish on Evidence screen only
implementation boundary =
  Docs/governance stamp + minor non-behavioral copy if needed;
  no new routes; no new fixtures; no real-data language.
data posture = FIXTURE_BACKED acceptance wording
scientific posture = UNCHANGED
operational posture = UNCHANGED; preserve operational-debt wording
security risks = overclaiming readiness
architecture impact = docs + PROJECT
tests = governance validator; wording assertions if UI copy touched
checkpoint criteria = CHECKPOINT_INCREMENT_I5 + GOVERNANCE + FINAL_INDEPENDENT_REVIEW PASS
rollback/reversibility = revert I5 commits before final merge
dependencies = I2, I3, I4
```

---

## Single execution boundary

```text
SINGLE_EXECUTION_BOUNDARY =
  ONE_BRANCH + ONE_DRAFT_PR + I2..I5 + mandatory checkpoints +
  ONE_FINAL_INDEPENDENT_REVIEW + ONE_FINAL_HUMAN_VALIDATION +
  FINAL_MERGE_ONLY;
  NO product work outside FROZEN_REMAINING_INCREMENT_LIST;
  NO intermediate merges;
  NO implementation until separate human execution prompt sets
  UX_R2_SINGLE_BRANCH_EXECUTION_AUTHORIZED = true (and related flags).
```

## Scientific and operational truth (immutable for this release)

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

Official wording preserved:

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```
