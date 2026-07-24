# UX-R4-DISCOVERY-AND-SCOPE — Análise de Impacto

## Metadados

```text
RELEASE = UX-R4
RELEASE_NAME = WICK GOVERNED DECISION LEDGER REFRESH
TASK_ID = UX-R4-DISCOVERY-AND-SCOPE-ASSESSMENT-001
TITLE = UX-R4 Discovery and Scope Assessment
PHASE = DISCOVERY_AND_SCOPE_ASSESSMENT
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
ASSESSMENT_ONLY = true
ASSESSMENT_AUTHORIZED = true
UX_R4_STATUS = NOT_STARTED
UX_R4_SCOPE_AUTHORIZED = false
UX_R4_IMPLEMENTATION_AUTHORIZED = false
PRODUCT_CODE_AUTHORIZED = false
BACKEND_IMPLEMENTATION_AUTHORIZED = false
NEW_ROUTE_AUTHORIZED = false
NEW_SCREEN_AUTHORIZED = false
NAVIGATION_CHANGE_AUTHORIZED = false
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
DECISION = SCOPE_RECOMMENDED
UX_R4_RECOMMENDATION = MULTIPLE_BOUNDED_INCREMENTS

BASE_SHA = 16bf2bd72c26cc804f7e630b504b74878848bed2
PR134_STATUS = MERGED
PR134_MERGE_COMMIT = 3ad9336af1d6ea2f9be431d7c1e183852fb4bb86
PR135_STATUS = MERGED
PR135_MERGE_COMMIT = 16bf2bd72c26cc804f7e630b504b74878848bed2

UX_R3_RELEASE_STATUS = CLOSED
UX_R3_RELEASE_ACCEPTANCE_STATUS = ACCEPTED
UX_R3_RELEASE_SCOPE =
  FIXTURE_BACKED_COLLECTION_MONITORING_DATA_QUALITY_AND_COHERENCE

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
ANALYZED_AT = 2026-07-23T12:48:33Z
ANALYZED_BY = cursor-agent
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION

UX_R4_RECOMMENDED_DIRECTION = F_GOVERNED_DECISION_LEDGER_REFRESH
UX_R4_FIRST_INCREMENT = UX_R4_I1_DECISION_LEDGER_AUTHORIZATION_ASSESSMENT
UX_R4_DELIVERY_MODEL = A_FULL_INCREMENTAL_FLOW
NEXT_RECOMMENDED_TASK = UX_R4_I1_DECISION_LEDGER_AUTHORIZATION_ASSESSMENT
NEXT_ITEM = UX_R4_I1_AUTHORIZATION_SEPARATE_ASSESSMENT_NOT_STARTED
```

G1 note: **SCOPE_RECOMMENDED** identifies a safe UX-R4 direction and first increment for a **separate** authorization assessment. It does **not** authorize product code, mark UX-R4 started, unlock scientific R4, start R5, integrate real data, peek future-unseen results, activate host/scheduler, or start parallel work. **UX_R4 ≠ R4 scientific stage.**

## MANDATORY_CONSTRAINTS

```text
ASSESSMENT_ONLY = true
NO_PRODUCT_CODE_CHANGES = true
NO_UX_R4_STARTED = true
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

UX-R1–UX-R3 are closed within fixture-backed boundaries. Active screens already cover Overview, Runs, Readiness, Dados Coletados, Host/Scheduler, R3E, and Evidence Explorer, with coherent cross-navigation after UX-R3 I2.

The live scientific/operational constraint remains unchanged: collection in progress, readiness NOT_READY (`WINDOW_DAYS_INSUFFICIENT`), R3E gate pending future-unseen data, host discovery deferred, scheduler blocked, R4 blocked, R5 not started.

Primary remaining **honest** fixture-backed user problem: Gustavo cannot answer, in one governed UX surface, what is **accepted**, **blocked**, **deferred**, what **trigger** would justify reassessment, and what must **not** be inferred — without reading raw docs. The Evidence catalog fixture clock (`EVIDENCE_CATALOG_NOW_ISO = 2026-07-21T12:00:00.000Z`) predates UX-R3 formal closure (`2026-07-23`) and does not yet reflect post-closure / UX-R4-not-authorized state.

Safest high-value UX-R4 direction: **F — Governed Decision Ledger Refresh** inside the existing Evidence Explorer (`/governance/evidence`), fixture-backed and read-only. Do **not** invent scientific, operational, approval, or real-data UX while those capabilities remain blocked.

## 1. Primary question

```text
What is the next real user problem that Wick should solve in the UX,
without pretending that blocked scientific or operational capabilities are available?
```

**Answer:** Make the current governed decision state (accepted / blocked / deferred / reassessment triggers / non-inferences) inspectable in the existing Evidence Explorer, including a curated catalog refresh after UX-R3 closure — without unlocking scientific R4, R5, real data, future-unseen results, validation, peeking, host discovery, or scheduler activation.

## 2. Baseline de capacidade UX (merged)

| Surface | Status | Role after UX-R3 |
|---------|--------|------------------|
| Overview | MERGED | Coarse ops summary + inbound link to Dados Coletados |
| Runs | MERGED | Collection run list + inbound link to Dados Coletados |
| Readiness | MERGED | Gate/window; points quality to Dados Coletados |
| Dados Coletados | MERGED (UX-R3) | Series-level illustrative quality |
| Host/Scheduler | MERGED | Deferred/blocked ops posture + debt visibility |
| R3E Experiment | MERGED | Explanatory; gate pending |
| Evidence Explorer | MERGED (UX-R2) | Curated evidence catalog; catalog clock pre-UX-R3 closure |

### User outcome checklist

| Capability | Status |
|------------|--------|
| understand the current scientific cycle | PARTIAL (R3E explanatory; no future-unseen results) |
| inspect runs | YES |
| understand readiness | YES |
| inspect evidence | YES (catalog stale vs UX-R3 closure) |
| inspect illustrative collection quality | YES |
| distinguish data quality from scientific approval | YES |
| understand operational blockers | YES |
| identify the next safe action | YES (per-screen advisory) |
| navigate coherently | YES (after UX-R3 I2) |
| inspect current accepted/deferred decision ledger in product UI | PARTIAL / NO compact ledger |
| execute validation / peek / host / scheduler / R4 / R5 | NO (correctly blocked) |

## 3. Candidates assessed

| Candidate | Disposition | Rationale |
|-----------|-------------|-----------|
| Governed decision ledger + Evidence catalog refresh | **RECOMMEND_FOR_UX_R4** | Highest remaining fixture-backed value; existing route |
| Evidence catalog refresh alone (no ledger UX) | REJECTED_AS_LOW_VALUE | Refresh without decision framing is incomplete for Gustavo |
| New Governance Timeline screen | REJECTED_AS_REDUNDANT | Duplicates Evidence Explorer |
| Activate Backlog / Aprovações | REJECTED_AS_REDUNDANT | Implies workflow/approval semantics; prior releases deferred |
| Research hypothesis / experiment planning | DEFER_TO_LATER_UX_RELEASE | Risks implying recalibration authorization |
| Experiment comparison workspace | DEFER_TO_LATER_UX_RELEASE / DEFER_UNTIL_REAL_DATA | R3E already explains M0–M5; real comparison needs data/gate |
| Scientific conclusion traceability UI | DEFER_UNTIL_REAL_DATA | Gate pending future-unseen |
| Readiness ↔ evidence reconciliation deep workflow | DEFER_TO_LATER_UX_RELEASE | Partial links exist; deeper workflow low urgency now |
| Collection-quality history / charts | REJECTED_AS_REDUNDANT | Dados Coletados owns quality; charts rejected in UX-R3 |
| Operational-debt visibility center | REJECTED_AS_REDUNDANT | Host/Scheduler already owns this |
| Release/governance timeline as new product | REJECTED_AS_REDUNDANT | Prefer Evidence ledger refresh |
| No new UX until future-unseen data (blanket) | REJECTED_AS_LOW_VALUE as blanket | Correct for scientific/ops UX; too strong for governance refresh |
| Future-unseen result surfaces | BLOCKED_BY_SCIENTIFIC_STATE | Peeking forbidden; validation not executed |
| Host/scheduler activation UX | BLOCKED_BY_OPERATIONAL_STATE | Discovery deferred; scheduler blocked |
| R4/R5 promotion UX | BLOCKED_BY_SCIENTIFIC_STATE | R4 blocked; R5 not started |
| Real-data integration | DEFER_UNTIL_REAL_DATA / BLOCKED | Backend + real data unauthorized |

## 4. Value / feasibility (recommended candidate)

| Dimension | Score |
|-----------|-------|
| PRIMARY_USER_VALUE | HIGH |
| NEED_NOW | HIGH |
| NON_DUPLICATION | HIGH (stay on `/governance/evidence`) |
| FIXTURE_BACKED_FEASIBILITY | HIGH |
| NO_BACKEND_FEASIBILITY | HIGH |
| NO_REAL_DATA_FEASIBILITY | HIGH |
| SCIENTIFIC_SAFETY | HIGH |
| OPERATIONAL_SAFETY | HIGH |
| SECURITY | HIGH |
| ACCESSIBILITY | HIGH |
| TESTABILITY | HIGH |
| REVERSIBILITY | HIGH |
| IMPLEMENTATION_SIZE | MEDIUM (bounded; auth first) |

## 5. Architectural impact (recommended direction)

```text
routes = existing /governance/evidence only (no new top-level route)
navigation = no Backlog/Aprovações activation
fixtures = evidence catalog refresh + decision-ledger fields/entries
ViewModels = Evidence Explorer VM extensions only if authorized later
shared components = reuse RelatedEvidenceLinks / existing explorer chrome
cross-navigation = optional inbound links only if frozen later
state ownership = fixture-backed governance presentation only
terminology = accepted / blocked / deferred / trigger / do-not-infer
security = no fs/fetch/Markdown/raw HTML/downloads/external hrefs
accessibility = semantic structure + axe on touched screen
test architecture = fixture + VM + screen + a11y focused tests
regression surface = Evidence Explorer primarily
governance volume = auth → implementation → closure (incremental)
delivery model = A_FULL_INCREMENTAL_FLOW
```

### Blocked capabilities required?

```text
backend = false
database = false
network = false
real data = false
future-unseen results = false
runtime repository/filesystem = false
host discovery = false
scheduler = false
scientific validation = false
effect peeking = false
R4 scientific authorization = false
R5 start = false
new dependencies = false
```

## 6. Delivery-model assessment

| Model | Disposition |
|-------|-------------|
| A_FULL_INCREMENTAL_FLOW | **RECOMMENDED** — auth assessment first; freeze boundary before product |
| B_SINGLE_BRANCH_SINGLE_PR_SINGLE_FINAL_VALIDATION | Possible only after I1 freezes a tiny reversible boundary |
| C_HYBRID_SINGLE_EXECUTION_WITH_INTERNAL_CHECKPOINTS | Not needed yet |
| D_DEFER_UX_R4 | Rejected — remaining governance gap is real and fixture-feasible |

```text
UX_R4_DELIVERY_MODEL = A_FULL_INCREMENTAL_FLOW
```

## 7. Required decision

```text
DECISION = SCOPE_RECOMMENDED
UX_R4_RECOMMENDATION = MULTIPLE_BOUNDED_INCREMENTS
UX_R4_DIRECTION = F_GOVERNED_DECISION_LEDGER_REFRESH
UX_R4_OBJECTIVE =
  Make accepted/blocked/deferred decisions and reassessment triggers
  inspectable in Evidence Explorer after UX-R3 closure, fixture-backed.
UX_R4_PRIMARY_USER_OUTCOME =
  Gustavo opens Evidências and can answer what is accepted, blocked,
  deferred, which trigger justifies reassessment, and what must not be inferred.
UX_R4_INCREMENT_COUNT = 3
UX_R4_INCREMENT_IDS =
  UX_R4_I1_DECISION_LEDGER_AUTHORIZATION_ASSESSMENT;
  UX_R4_I2_EVIDENCE_DECISION_LEDGER_FIXTURE_REFRESH;
  UX_R4_I3_FIXTURE_ACCEPTANCE_AND_CLOSURE
UX_R4_INCREMENT_ORDER = I1 → I2 → I3
UX_R4_MAXIMUM_BOUNDARY =
  Existing /governance/evidence only; fixture-backed read-only decision
  ledger + catalog refresh; no new top-level route; no Backlog/Aprovações
  activation; no scientific/ops unlock.
UX_R4_OUT_OF_SCOPE =
  scientific R4; R5; real data; future-unseen; validation; peeking;
  host/scheduler activation; backups/incidents; backlog/approvals;
  experiment planning; quality charts; new comparison results.
UX_R4_RISK = MEDIUM
UX_R4_DELIVERY_MODEL = A_FULL_INCREMENTAL_FLOW
FIRST_NEXT_TASK = UX_R4_I1_DECISION_LEDGER_AUTHORIZATION_ASSESSMENT
```

## 8. Product boundaries preserved

```text
UX release numbering != scientific release authorization
UX_R4 != R4 scientific stage
UX_R4 discovery does not unlock R4
UX_R4 discovery does not start R5
fixture-backed evidence does not imply live truth
```

## Official operational wording preserved

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```
