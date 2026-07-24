# UX-R4 I1 Decision Ledger Authorization — Spec

```text
RELEASE = UX-R4
INCREMENT = I1
DOCUMENT = UX-R4-I1-DECISION-LEDGER-AUTHORIZATION_SPEC
TASK_ID = UX-R4-I1-DECISION-LEDGER-AUTHORIZATION-ASSESSMENT-001
STATUS = ASSESSMENT_COMPLETE_UNMERGED
AUTHORIZATION_DECISION = AUTHORIZED_WITH_CONDITIONS
BASE_SHA = 461b8730166bcbaf54dba3fed19895a91880fa44
UX_R4_STATUS = NOT_STARTED
UX_R4_I1_IMPLEMENTATION_AUTHORIZED = false
PRODUCT_CODE_AUTHORIZED = false
```

## Frozen product boundary

```text
ROUTE = /governance/evidence
NAV_ITEM = Evidências
POSTURE = STATIC_FIXTURE_BACKED_READ_ONLY
INTEGRATION_MODE = B_NEW_SECTION_ABOVE_CATALOG
FIXTURE_NAME = governed_decision_ledger_current_state_illustrative
FIXTURE_VERSION = 1
VIEWMODEL_NAME = GovernedDecisionLedgerViewModel
```

## Architecture for later I2

```text
fixture → validators/builders/selectors → GovernedDecisionLedgerViewModel
→ EvidenceExplorerScreenView section above catalog
```

Catalog list/detail/search/filters remain unchanged except optional deep-links into ledger evidence refs.

## Dispositions

```text
ACCEPTED
AUTHORIZED_WITH_CONDITIONS
BLOCKED
DEFERRED
REJECTED
SUPERSEDED
UNKNOWN
```

Badge mapping guidance:

```text
ACCEPTED → completed
AUTHORIZED_WITH_CONDITIONS → informational
BLOCKED → blocked
DEFERRED → deferred
REJECTED → attention
SUPERSEDED → informational
UNKNOWN → unknown
fault/red → only for true fault semantics (not used for process dispositions)
```

## Domains / decision types

```text
DOMAINS =
  UX_GOVERNANCE; SCIENTIFIC_GOVERNANCE; DATA_QUALITY;
  OPERATIONAL_GOVERNANCE; RELEASE_GOVERNANCE; ARCHITECTURE; SECURITY

DECISION_TYPES =
  SCOPE_DECISION; AUTHORIZATION_DECISION; IMPLEMENTATION_DECISION;
  REVIEW_DECISION; MERGE_DECISION; RELEASE_ACCEPTANCE_DECISION;
  DEFERRAL_DECISION; BLOCKING_DECISION; REASSESSMENT_DECISION
```

## Required schema fields

```text
decision_id, title, summary, domain, decision_type, disposition,
decision_date, scope, rationale, evidence_refs, must_not_infer,
reassessment_trigger, next_governed_action, is_illustrative,
fixture_authored_at, catalog_curated_at
```

Optional: effective_date, conditions, related_release, related_increment, scientific_boundary, operational_boundary, supersedes, superseded_by, source_artifact, primary_evidence_ref.

## Evidence links

```text
internal evidenceId only
href = /governance/evidence?evidenceId=<sanitized>
reuse buildEvidenceExplorerHref / parseEvidenceIdParam
no external URLs / fs / Markdown / downloads
```

## Filters / sort / summary (I2)

```text
APPROVED_FILTERS = disposition; domain; release; decision_type; reassessment_availability
DEFAULT_SORT = decision_date DESC, decision_id ASC
SUMMARY_SEMANTICS =
  UNKNOWN != ZERO;
  blocked count != failure count;
  accepted count != approved strategy count;
  trigger count != automatic action count
EMPTY_STATE / NO_RESULTS_STATE / UNKNOWN_STATE / STALE_FIXTURE_STATE = required
NO_CHARTS
```

## Seed records authorized for later curated fixture

INCLUDE:

```text
UX-R1 fixture-backed read-only acceptance
UX-R2 evidence/audit exploration acceptance
UX-R3 collection monitoring/data-quality/coherence acceptance
R3D NO_MEASURABLE_EDGE (recorded; must_not_infer carefully)
R3E PENDING_FUTURE_UNSEEN_DATA
host discovery DEFERRED
scheduler activation BLOCKED
scientific R4 BLOCKED
R5 NOT_STARTED
```

## Catalog freshness (I2 may update)

```text
catalog_curated_at
fixture version bump
decision rows for UX-R1..R3 + current blocked/deferred truths
reassessment trigger text
```

Disallowed: fake live freshness, runtime mtime, repository polling.

## Security / a11y / stop conditions

As frozen in the impact assessment. Architecture boundary tests required in I2 for Evidence Explorer + new ledger module.

## Explicit non-authorization

```text
This spec does not authorize I2 product work.
This spec does not start UX-R4 implementation.
This spec does not unlock scientific R4 or start R5.
```

## Next

```text
NEXT_RECOMMENDED_TASK = UX_R4_I2_EVIDENCE_DECISION_LEDGER_FIXTURE_REFRESH
NEXT_ITEM = UX_R4_I2_IMPLEMENTATION_SEPARATE_PROMPT_NOT_AUTHORIZED
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
