# UX-R4 I2 — Evidence Decision Ledger Fixture Refresh — Spec As Implemented

```text
RELEASE = UX-R4
INCREMENT = I2
DOCUMENT = UX-R4-I2-EVIDENCE-DECISION-LEDGER-FIXTURE-REFRESH_SPEC-AS-IMPLEMENTED
TASK_ID = UX-R4-I2-EVIDENCE-DECISION-LEDGER-FIXTURE-REFRESH-001
STATUS = IMPLEMENTATION_COMPLETE_UNMERGED
BASE_SHA = 60e3460bf297458315c539cf050da34774ab1923
```

## Frozen product boundary (as shipped)

```text
ROUTE = /governance/evidence
NAV_ITEM = Evidências
POSTURE = STATIC_FIXTURE_BACKED_READ_ONLY
INTEGRATION_MODE = B_NEW_SECTION_ABOVE_CATALOG
FIXTURE_NAME = governed_decision_ledger_current_state_illustrative
FIXTURE_VERSION = 1
VIEWMODEL_NAME = GovernedDecisionLedgerViewModel
```

## Module map

```text
web/src/fixtures/governedDecisionLedger.ts
web/src/viewmodels/governedDecisionLedgerEnums.ts
web/src/viewmodels/governedDecisionLedgerTypes.ts
web/src/viewmodels/filterGovernedDecisionLedger.ts
web/src/viewmodels/buildGovernedDecisionLedgerViewModel.ts
web/src/screens/evidence-explorer/GovernedDecisionLedgerSection.tsx
web/src/screens/evidence-explorer/LedgerFilters.tsx
web/src/screens/evidence-explorer/LedgerList.tsx
```

## Seed records (9)

```text
dec-ux-r1-fixture-backed-read-only-acceptance
dec-ux-r2-evidence-audit-exploration-acceptance
dec-ux-r3-collection-quality-coherence-acceptance
dec-r3d-no-measurable-edge
dec-r3e-pending-future-unseen
dec-host-discovery-deferred
dec-scheduler-activation-blocked
dec-scientific-r4-blocked
dec-r5-not-started
```

## Filters / sort / states

```text
FILTERS = disposition; domain; release; decision_type; reassessment_availability
DEFAULT_SORT = decision_date DESC, decision_id ASC
EMPTY / NO_RESULTS / UNKNOWN / STALE = implemented
DETAIL = inline panel within section
EVIDENCE_LINKS = buildEvidenceExplorerHref / RelatedEvidenceLinks only
```

## Badge mapping

```text
ACCEPTED → completed
AUTHORIZED_WITH_CONDITIONS → informational
BLOCKED → blocked
DEFERRED → deferred
REJECTED → attention
SUPERSEDED → informational
UNKNOWN → unknown
fault/red → never for process dispositions
```

## Next

```text
NEXT_RECOMMENDED_TASK = UX_R4_I3_FIXTURE_ACCEPTANCE_AND_CLOSURE
NEXT_ITEM = UX_R4_I3_SEPARATE_PROMPT_NOT_AUTHORIZED
```
