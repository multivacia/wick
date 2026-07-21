# UX-R2-I1 — Evidence Explorer Implementation Spec

```text
RELEASE = UX-R2
INCREMENT = I1
TASK_ID = EVIDENCE-EXPLORER-IMPLEMENTATION-001
PHASE = IMPLEMENTATION
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_STATUS = COMPLETE
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
IMPACT = docs/ai-impact/UX-R2-I1-EVIDENCE-EXPLORER-IMPLEMENTATION_IMPACT_ASSESSMENT.md
ROUTE = /governance/evidence
SCREEN = Evidências
NAV_LABEL = Evidências
FIXTURE_ID = evidence_catalog_current_state_illustrative
VIEWMODEL = EvidenceExplorerViewModel
IMPLEMENTATION_POSTURE = A_STATIC_FIXTURE_BACKED_EVIDENCE_CATALOG
READ_ONLY = true
FIXTURE_BACKED = true
CURATED_MANIFEST_ONLY = true
LIST_AND_DETAIL = true
NO_VISIBLE_FIXTURE_SELECTOR = true
BACKEND_REQUIRED = false
```

## Objective

Deliver the fixture-backed, read-only **Evidências** product screen at `/governance/evidence`, consuming a dedicated Evidence Explorer ViewModel and curated catalog fixture. Allow operators to inspect what evidence exists, which release/increment/experiment it supports, known vs unknown state, and limitations — without accessing repository files, real data, or future-unseen results at runtime.

## Behavior

Answer in plain language first:

1. What evidence exists in the curated catalog?
2. Which release, increment, experiment or governance decision does an entry support?
3. What is known, unknown, pending or blocked?
4. What are the limitations of each entry?
5. Is the catalog complete of all repository evidence? (No — curated/illustrative only.)
6. Does sourcePath grant file access? (No — display metadata only.)
7. Does evidence presence equal scientific approval? (No.)

## Sections / composition

```text
PageHeader
SyntheticDataNotice
CatalogDisclosure
SafetyNotices
EvidenceSearch
EvidenceFilters
EvidenceList
EvidenceDetail (summary, supports, limitations, known/unknown, governanceFlags, sourcePath)
Empty / no-results / invalid-selection states
```

## Evidence model

```text
evidenceId, title, evidenceClass, release, increment, experimentId,
status, dataOrigin, scientificStage, createdAtOrUnknown, sourcePath,
summary, supports, limitations, knownState, unknownState,
governanceFlags, staleness
```

Allowed classes (closed enum):

```text
release_record
implementation_handoff
impact_assessment
technical_scientific_review
experiment_specification
validation_report
collection_readiness_evidence
operational_debt_record
```

Initial catalog covers: UX-R1 formal closure; UX-R2 discovery; UX-R2 I1 auth; R3D NO_MEASURABLE_EDGE; R3E PENDING_FUTURE_UNSEEN_DATA; FU collection/readiness NOT_READY; host/scheduler operational debt.

## Search and filters

Search (client-side, case-insensitive, trim, no regex): title, evidenceClass, release, increment, experimentId, status, dataOrigin, scientificStage, summary.

Filters (closed lists from catalog): evidenceClass, release, status, dataOrigin, scientificStage, staleness.

## Semantics

```text
EVIDENCE_PRESENT != SCIENTIFIC_APPROVAL
AUDITED != FUTURE_VALIDATED
HISTORICAL != FUTURE_UNSEEN
EXPLORATORY != CONFIRMATORY
PENDING != FAILED
NO_MEASURABLE_EDGE_R3D != R3E_REJECTED
EVIDENCE_CATALOG != RUNTIME_REPOSITORY_BROWSER
SOURCE_PATH_DISPLAY != FILE_ACCESS
```

## Out of scope

```text
runtime repository / filesystem access
backend evidence APIs
Markdown / HTML rendering
file download / open-in-repo
external links
real data / future-unseen result payloads
validation execution / effect peeking
host discovery / scheduler activation
R4 unlock / R5 start
visible fixture selector
scientific interpretation change
```

## Dependencies

```text
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
```
