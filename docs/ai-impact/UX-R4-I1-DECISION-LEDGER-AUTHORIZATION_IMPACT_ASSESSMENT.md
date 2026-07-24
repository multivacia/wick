# UX-R4-I1-DECISION-LEDGER-AUTHORIZATION-ASSESSMENT — Análise de Impacto

## Metadados

```text
RELEASE = UX-R4
RELEASE_NAME = WICK GOVERNED DECISION LEDGER REFRESH
INCREMENT = I1
TASK_ID = UX-R4-I1-DECISION-LEDGER-AUTHORIZATION-ASSESSMENT-001
TITLE = Decision Ledger Authorization Assessment
PHASE = AUTHORIZATION_ASSESSMENT
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
ASSESSMENT_ONLY = true
ASSESSMENT_AUTHORIZED = true
IMPLEMENTATION_SCOPE = AUTHORIZATION_ASSESSMENT_DOCUMENTATION_ONLY
DECISION = AUTHORIZED_WITH_CONDITIONS

UX_R4_STATUS = NOT_STARTED
UX_R4_I1_STATUS = NOT_STARTED
UX_R4_I1_IMPLEMENTATION_AUTHORIZED = false
UX_R4_I2_STATUS = NOT_STARTED
UX_R4_I3_STATUS = NOT_STARTED
PRODUCT_CODE_AUTHORIZED = false
NEW_ROUTE_AUTHORIZED = false
NEW_SCREEN_AUTHORIZED = false
NAVIGATION_CHANGE_AUTHORIZED = false
FIXTURE_IMPLEMENTATION_AUTHORIZED = false
VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
TEST_IMPLEMENTATION_AUTHORIZED = false
BACKEND_IMPLEMENTATION_AUTHORIZED = false
REAL_DATA_INTEGRATION_AUTHORIZED = false
RUNTIME_REPOSITORY_ACCESS_AUTHORIZED = false
RAW_FILESYSTEM_ACCESS_AUTHORIZED = false
FUTURE_UNSEEN_RESULTS_ACCESS_AUTHORIZED = false
VALIDATION_EXECUTION_AUTHORIZED = false
EFFECT_PEEKING_AUTHORIZED = false
SCIENTIFIC_INTERPRETATION_CHANGE_AUTHORIZED = false
REAL_HOST_DISCOVERY_AUTHORIZED = false
SCHEDULER_ACTIVATION_AUTHORIZED = false
OPERATIONAL_ACTIONS_AUTHORIZED = false
R4_STATE_CHANGE_AUTHORIZED = false
R5_STATE_CHANGE_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false

AUTHORIZED_ROUTE = /governance/evidence
AUTHORIZED_NAV_ITEM = Evidências
AUTHORIZED_POSTURE = STATIC_FIXTURE_BACKED_READ_ONLY
AUTHORIZED_INTEGRATION_MODE = B_NEW_SECTION_ABOVE_CATALOG
AUTHORIZED_FIXTURE_NAME = governed_decision_ledger_current_state_illustrative
AUTHORIZED_FIXTURE_VERSION = 1
AUTHORIZED_VIEWMODEL_NAME = GovernedDecisionLedgerViewModel

PR136_STATUS = MERGED
PR136_MERGE_COMMIT = 01847508f3275ed71207145324543901ed3d1199
PR137_STATUS = MERGED
PR137_MERGE_COMMIT = 461b8730166bcbaf54dba3fed19895a91880fa44
MAIN_TIP = 461b8730166bcbaf54dba3fed19895a91880fa44

UX_R4_DISCOVERY_STATUS = MERGED
UX_R4_DISCOVERY_DECISION = SCOPE_RECOMMENDED
UX_R4_DIRECTION = F_GOVERNED_DECISION_LEDGER_REFRESH
UX_R4_DELIVERY_MODEL = A_FULL_INCREMENTAL_FLOW

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

REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 461b8730166bcbaf54dba3fed19895a91880fa44
ANALYZED_AT = 2026-07-24T01:05:34Z
ANALYZED_BY = cursor-agent
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
NEXT_RECOMMENDED_TASK = UX_R4_I2_EVIDENCE_DECISION_LEDGER_FIXTURE_REFRESH
NEXT_ITEM = UX_R4_I2_IMPLEMENTATION_SEPARATE_PROMPT_NOT_AUTHORIZED
```

G1 note: **AUTHORIZED_WITH_CONDITIONS** freezes the I2 product boundary for a later separate human-authorized implementation prompt. It does **not** authorize product code now, mark UX-R4 started, unlock scientific R4, start R5, or activate Backlog/Aprovações.

## MANDATORY_CONSTRAINTS

```text
ASSESSMENT_ONLY = true
NO_PRODUCT_CODE_CHANGES = true
NO_UX_R4_STARTED = true
NO_I2_STARTED = true
NO_REAL_DATA = true
NO_RUNTIME_REPOSITORY_ACCESS = true
NO_RAW_FILESYSTEM_ACCESS = true
NO_FUTURE_UNSEEN_RESULTS = true
NO_VALIDATION_EXECUTION = true
NO_EFFECT_PEEKING = true
NO_OPERATIONAL_ACTIONS = true
NO_SCHEDULER_ACTIVATION = true
NO_SCIENTIFIC_INTERPRETATION_CHANGE = true
NO_R4_OR_R5_STATE_CHANGE = true
PARALLEL_TASKS_ALLOWED = false
```

## SUMMARY

UX-R4 discovery MERGED recommended a fixture-backed governed decision ledger inside existing Evidence Explorer. This I1 assessment authorizes that boundary **with conditions**.

Existing `/governance/evidence` remains valid: no new route/nav item. Recommended integration is **B_NEW_SECTION_ABOVE_CATALOG** — a compact ledger section after notices and before catalog search/filters — so Gustavo can answer accepted/blocked/deferred/triggers/do-not-infer without turning the catalog into a backlog or approval workflow.

Implementation remains **unauthorized** until a separate I2 execution prompt. Seed records are limited to already-stamped UX release acceptances and current blocked/deferred scientific/operational truths — no fabricated conclusions.

## 1. Primary user outcome (frozen)

Minimum safe ledger answers:

```text
What decision was made?
What is its current disposition?
Why was it accepted, blocked, deferred or rejected?
What evidence supports it?
What must not be inferred from it?
What condition justifies reassessment?
What is the next governed action?
```

Explicit non-identity:

```text
ledger != backlog
ledger != approval workflow
ledger != task tracker
ledger != commit log
ledger != scientific-result dashboard
```

## 2. Route / integration (frozen)

```text
ROUTE = /governance/evidence
NAV_ITEM = Evidências
POSTURE = STATIC_FIXTURE_BACKED_READ_ONLY
INTEGRATION_MODE = B_NEW_SECTION_ABOVE_CATALOG
```

| Mode | Disposition |
|------|-------------|
| A_NEW_TAB_WITHIN_EXISTING_SCREEN | REJECTED — no tab system exists; adds nav complexity |
| B_NEW_SECTION_ABOVE_CATALOG | **AUTHORIZED** — ledger before catalog workflow |
| C_NEW_SECTION_BELOW_CATALOG | REJECTED — ledger would be easy to miss |
| D_FILTERED_VIEW_MODE | REJECTED — filters ≠ decision answers |
| E_NO_SAFE_INTEGRATION | REJECTED — existing route is architecturally valid |

## 3. Disposition taxonomy (frozen)

| Disposition | Plain language | Severity badge | Completion | Scientific | Operational | Reassessment |
|-------------|----------------|----------------|------------|------------|-------------|--------------|
| ACCEPTED | Escopo/decisão aceita no limite declarado | completed | closed within stated scope | ≠ strategy approval | ≠ ops activation | only if trigger met |
| AUTHORIZED_WITH_CONDITIONS | Autorizado com condições; não implementado | informational | incomplete until conditions consumed | no edge claim | no activation | when conditions change |
| BLOCKED | Bloqueado por dependência/estado | blocked | not complete | ≠ scientific failure | ≠ system crash | when blocking state clears |
| DEFERRED | Adiado conscientemente | deferred | not rejected | no reinterpretation | may wait on host/etc. | explicit trigger |
| REJECTED | Rejeitado neste contexto | attention | closed as rejected | ≠ invalid forever | no ops action | only if boundary changes |
| SUPERSEDED | Substituído por decisão posterior | informational | historical | prior record retained | no delete semantics | none (point to successor) |
| UNKNOWN | Indisponível / não inventado | unknown | unknown ≠ zero | no fill | no fill | when data appears |

Preserved inequalities:

```text
ACCEPTED != SCIENTIFIC_APPROVAL
AUTHORIZED_WITH_CONDITIONS != IMPLEMENTED
BLOCKED != SYSTEM_FAILURE
DEFERRED != REJECTED
REJECTED != INVALID_FOREVER
SUPERSEDED != DELETED
UNKNOWN != ZERO
PENDING != FAULT
RED_FOR_FAULT_ONLY
```

## 4. Domains and decision types (frozen)

Approved domains:

```text
UX_GOVERNANCE
SCIENTIFIC_GOVERNANCE
DATA_QUALITY
OPERATIONAL_GOVERNANCE
RELEASE_GOVERNANCE
ARCHITECTURE
SECURITY
```

Approved decision types:

```text
SCOPE_DECISION
AUTHORIZATION_DECISION
IMPLEMENTATION_DECISION
REVIEW_DECISION
MERGE_DECISION
RELEASE_ACCEPTANCE_DECISION
DEFERRAL_DECISION
BLOCKING_DECISION
REASSESSMENT_DECISION
```

Rejected as project-management creep: assignees, due dates, sprint status, % complete, generic todo states.

## 5. Record schema (frozen)

### Required fields

| Field | Type | Notes |
|-------|------|-------|
| decision_id | string `dec-*` | stable curated id |
| title | string | plain language first |
| summary | string | short why/what |
| domain | enum | approved domains |
| decision_type | enum | approved types |
| disposition | enum | approved dispositions |
| decision_date | ISO date or UNKNOWN | no invented zero |
| scope | string | stated boundary |
| rationale | string | why this disposition |
| evidence_refs | list[{evidenceId,label}] | internal ids only |
| must_not_infer | string[] | mandatory non-inferences |
| reassessment_trigger | string \| null | descriptive only |
| next_governed_action | string | advisory text only |
| is_illustrative | boolean | always true in fixture |
| fixture_authored_at | ISO datetime | when fixture row authored |
| catalog_curated_at | ISO datetime | curated catalog clock |

### Optional fields

```text
effective_date
conditions
related_release
related_increment
scientific_boundary
operational_boundary
supersedes
superseded_by
source_artifact
primary_evidence_ref (if distinct from evidence_refs[0])
```

### Timestamp disambiguation

```text
fixture_authored_at = when the fixture row was written
catalog_curated_at = curated illustrative “as of” for the ledger catalog
decision_effective_at / effective_date = when decision applies (may be UNKNOWN)
source_artifact_created_at = optional metadata of cited artifact (not live mtime)
```

No fake live freshness. Later I2 may refresh `catalog_curated_at` and curated rows reflecting UX-R1–R3 + current blocked/deferred truths.

### Evidence references

```text
model = primary optional + supporting evidence_refs
route = /governance/evidence?evidenceId=<sanitized>
helpers = buildEvidenceExplorerHref / parseEvidenceIdParam
no arbitrary URLs
no filesystem access
no Markdown/downloads
```

### Reassessment triggers (descriptive only)

Approved example phrasing families:

```text
future-unseen window reaches required duration
new independent evidence exists
operational host is identified
scheduler activation is formally authorized
architecture boundary changes
material contradiction is discovered
```

Triggers must **not** auto-authorize, mutate state, execute checks, access live data, schedule monitoring, unlock R4, or start R5.

## 6. Seed records

| Candidate | Disposition |
|-----------|-------------|
| UX-R1 accepted fixture-backed read-only scope | **INCLUDE** |
| UX-R2 accepted evidence/audit exploration scope | **INCLUDE** |
| UX-R3 accepted collection monitoring/data-quality/coherence scope | **INCLUDE** |
| R3D no measurable edge | **INCLUDE** (SCIENTIFIC_GOVERNANCE / BLOCKED or ACCEPTED-as-recorded-result with must_not_infer) |
| R3E pending future-unseen data | **INCLUDE** (BLOCKED / DEFERRAL_DECISION) |
| host discovery deferred | **INCLUDE** (OPERATIONAL_GOVERNANCE / DEFERRED) |
| scheduler activation blocked | **INCLUDE** (OPERATIONAL_GOVERNANCE / BLOCKED) |
| scientific R4 blocked | **INCLUDE** (SCIENTIFIC_GOVERNANCE / BLOCKED) |
| R5 not started | **INCLUDE** (SCIENTIFIC_GOVERNANCE / DEFERRED or BLOCKED wording “not started”) |

Do not fabricate new scientific conclusions. R3D INCLUDE as recorded `NO_MEASURABLE_EDGE` with must_not_infer that it is not a trading-strategy rejection forever and not an ops fault.

## 7. ViewModel architecture (frozen for later I2)

```text
curated fixture governed_decision_ledger_current_state_illustrative
→ validation/builders/selectors
→ GovernedDecisionLedgerViewModel
→ EvidenceExplorerScreenView new section (above catalog)
```

List shape: compact cards/rows with disposition badge, title, domain, related release, next action teaser.  
Filters (optional later): disposition, domain, release, decision_type, reassessment availability.  
Default sort: `decision_date` desc, then `decision_id` asc — **not** severity-first (blocked must not look “more scientific”).  
Counts: preserve UNKNOWN≠ZERO; blocked≠failure; accepted≠approved strategy; trigger≠automatic action.  
States: empty / no-results / unknown / stale-fixture disclosure.  
Detail: expand inline or panel within section; no new route.  
Evidence links: RelatedEvidenceLinks / existing deep-link helper only.

No charts, pies, or gauges.

## 8. Security / accessibility / scientific / operational boundaries

Security prohibit: fs, child_process, network/fetch, process.env, runtime repo browse, raw paths, unsafe HTML/Markdown, downloads, external URLs, secrets, future-unseen payloads. Later I2 must add architecture boundary tests mirroring Evidence Explorer.

Accessibility: semantic headings/lists/links; keyboard; visible focus; SR labels binding decision↔evidence; non-color-only disposition; responsive; axe on Evidence Explorer after change.

Scientific:

```text
ledger record != scientific result
accepted UX scope != accepted trading strategy
evidence link != validated edge
reassessment trigger != permission
blocked scientific R4 != UX failure
```

Operational:

```text
host discovery deferred != host unavailable forever
scheduler blocked != collection failed
```

No R3D/R3E reinterpretation.

## 9. Maximum implementation boundary (for later I2)

```text
existing /governance/evidence only
B_NEW_SECTION_ABOVE_CATALOG
fixture-backed GovernedDecisionLedgerViewModel
curated seed records only
internal evidence deep-links only
no Backlog/Aprovações activation
no backend/real data/FU/validate/peek/host/scheduler
no R4 unlock / R5 start
no new dependencies
```

## 10. Stop conditions (later I2)

```text
new route required
backend required
real data required
runtime repository access required
future-unseen access required
scientific reinterpretation required
automatic transitions requested
approval workflow requested
Backlog/Aprovações activation requested
new dependency required
security failure
accessibility failure
schema ambiguity
ungrounded seed record
material duplication with Evidence catalog
```

## 11. Decision

```text
AUTHORIZATION_DECISION = AUTHORIZED_WITH_CONDITIONS
FINAL_RECOMMENDATION =
  Merge this docs-only assessment; then issue a separate human-authorized
  I2 implementation prompt within the frozen boundary; do not start product now.
```

## Official operational wording preserved

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```
