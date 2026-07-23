# UX-R3 Remaining Release — Spec As Implemented

```text
RELEASE = UX-R3
DOCUMENT = UX-R3-REMAINING-RELEASE_SPEC-AS-IMPLEMENTED
TASK_ID = UX-R3-REMAINING-RELEASE-SINGLE-EXECUTION-001
DELIVERY_MODEL = B_SINGLE_BRANCH_SINGLE_PR_SINGLE_FINAL_VALIDATION
STATUS = IMPLEMENTED_UNMERGED
BASE_SHA = 200f2767af82e027ffe32eeaca485c6236ad595a
```

## Frozen increments executed

### I2 — Collection quality cross-navigation and coherence

```text
increment = UX_R3_I2_COLLECTION_QUALITY_CROSS_NAV_AND_COHERENCE
product surfaces =
  web/src/screens/readiness/CollectionState.tsx
  web/src/screens/readiness/ReadinessScreenView.tsx
  web/src/screens/runs/RunsScreenView.tsx
  web/src/screens/overview/OverviewScreen.tsx
  web/src/screens/shared/RelatedProductLinks.tsx
route = existing /future-collection/collected-data only
navigation = react-router Link only
semantics preserved =
  DATA_QUALITY != SCIENTIFIC_APPROVAL
  COLLECTION_HEALTHY != VALIDATION_READY
  COLLECTION_IN_PROGRESS != READY
  navigation does not change readiness/scientific/ops state
checkpoint = PASS (reports/ai-implementation/UX-R3-I2-COLLECTION-QUALITY-CROSS-NAV-AND-COHERENCE_CHECKPOINT.md)
```

### I3 — Fixture acceptance and closure preparation

```text
increment = UX_R3_I3_FIXTURE_ACCEPTANCE_AND_CLOSURE
scope = docs + PROJECT proposed state + acceptance wording proposal
formal stamp on main = NOT APPLIED (awaits human merge authorization)
proposed wording =
  UX-R3 fixture-backed collection monitoring, data-quality exploration, and workflow coherence scope is complete, accepted, and governed.
proposed release scope =
  FIXTURE_BACKED_COLLECTION_MONITORING_DATA_QUALITY_AND_COHERENCE
```

## Architecture

```text
fixtures → ViewModels (unchanged I1 domain) → screens
shared RelatedProductLinks helper for thin inbound product links
RelatedEvidenceLinks unchanged for evidence deep-links
no new ViewModel domain fields required for I2
```

## Security / a11y

```text
no fetch/fs/child_process/process.env
no dangerouslySetInnerHTML / Markdown rendering
no external hrefs
semantic Link elements with visible focus
axe coverage retained on touched screens
```

## Out of scope (enforced)

```text
new routes/screens/dashboards/charts/metrics
backend / database / network
real data / future-unseen / validation / peeking
host / scheduler / R4 / R5
new dependencies
```
