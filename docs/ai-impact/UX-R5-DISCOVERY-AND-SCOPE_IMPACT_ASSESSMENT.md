# UX-R5-DISCOVERY-AND-SCOPE — Análise de Impacto

## Metadados

```text
RELEASE = UX-R5
RELEASE_NAME = WICK UX-R5 DISCOVERY (DEFER)
TASK_ID = UX-R5-DISCOVERY-AND-SCOPE-ASSESSMENT-001
TITLE = UX-R5 Discovery and Scope Assessment
PHASE = DISCOVERY_AND_SCOPE_ASSESSMENT
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
ASSESSMENT_ONLY = true
ASSESSMENT_AUTHORIZED = true
UX_R5_STATUS = NOT_STARTED
UX_R5_SCOPE_AUTHORIZED = false
UX_R5_IMPLEMENTATION_AUTHORIZED = false
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
R5_SCIENTIFIC_STATE_CHANGE_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
DECISION = DEFER_RECOMMENDED
UX_R5_RECOMMENDATION = NO_NEW_UX_RELEASE_NOW
UX_R5_DELIVERY_MODEL = D_DEFER_UX_R5

BASE_SHA = 259092ec8b66a809dfb5d23d4ef0ddd65d455d64
PR143_STATUS = MERGED
PR143_MERGE_COMMIT = 28062165e2497457356ae49f914f02d3a716a8e7
PR144_STATUS = MERGED
PR144_MERGE_COMMIT = 1c569b037b29de090359950f8ad69712088126b1
PR145_STATUS = MERGED
PR145_MERGE_COMMIT = 259092ec8b66a809dfb5d23d4ef0ddd65d455d64

UX_R4_RELEASE_STATUS = CLOSED
UX_R4_RELEASE_ACCEPTANCE_STATUS = ACCEPTED
UX_R4_RELEASE_SCOPE =
  FIXTURE_BACKED_GOVERNED_DECISION_LEDGER_AND_EVIDENCE_CATALOG_REFRESH

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
ANALYZED_AT = 2026-07-24T23:31:25Z
ANALYZED_BY = cursor-agent
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION

NEXT_RECOMMENDED_TASK = UX_R5_REASSESSMENT_AFTER_FUTURE_UNSEEN_READINESS_CHANGE
NEXT_ITEM = UX_R5_PRODUCT_SCOPE_NOT_AUTHORIZED
```

G1 note: **DEFER_RECOMMENDED** / **NO_NEW_UX_RELEASE_NOW** means UX-R5 product scope is **not** opened. This assessment does **not** authorize product code, mark UX-R5 started, unlock scientific R4, start scientific R5, integrate real data, peek future-unseen results, activate host/scheduler, or start parallel work. **UX_R5 ≠ scientific R5.**

## MANDATORY_CONSTRAINTS

```text
ASSESSMENT_ONLY = true
NO_PRODUCT_CODE_CHANGES = true
NO_UX_R5_STARTED = true
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

UX-R1–UX-R4 are formally **CLOSED / ACCEPTED** within fixture-backed boundaries. Active screens already cover Overview, Runs, Readiness, Dados Coletados, Host/Scheduler, R3E Experiment, and Evidence Explorer with Governed Decision Ledger (nine grounded seeds, filters, reassessment triggers, semantic safeguards).

The binding constraint is **not** missing UX inspection: collection remains `IN_PROGRESS`, readiness `NOT_READY` (`WINDOW_DAYS_INSUFFICIENT`), R3E gate `PENDING_FUTURE_UNSEEN_DATA`, scientific R4 `BLOCKED`, scientific R5 `NOT_STARTED`, host discovery `DEFERRED`, scheduler `BLOCKED`.

Primary answer to the discovery question: while future-unseen data is still accumulating and scientific R4 remains blocked, **do not open a new UX release**. Gustavo can already understand the scientific cycle (explanatory), inspect runs/readiness/evidence/DQ, inspect governed decisions and reassessment triggers, distinguish UX acceptance from scientific approval, and identify the next safe action (`wait_for_sufficient_future_window` / continue collection / do not validate or activate). Remaining polish (catalog clock lag; optional UX-R4 acceptance seed) does not change that safe action and must not become a release treadmill.

## 1. Primary question

```text
What is the next meaningful user decision or workflow Wick should support,
given that future-unseen data is still accumulating and scientific R4 remains blocked?
```

**Answer:** Support **patience with honesty** — keep the existing fixture-backed inspection surfaces as the governed wait loop. Do **not** invent new research-planning, gate-workflow, promotion, or real-data UX. Reassess UX-R5 only after readiness/future-unseen maturity (or a separately authorized scientific/ops posture change) creates a new user problem that fixtures alone cannot honestly answer.

## 2. Baseline de capacidade UX (merged)

| Surface | Status | Role after UX-R4 |
|---------|--------|------------------|
| Overview | MERGED | Coarse ops summary + next safe action |
| Runs | MERGED | Collection run list |
| Readiness | MERGED | Gate/window; `WINDOW_DAYS_INSUFFICIENT` |
| Dados Coletados | MERGED | Series-level illustrative quality |
| Host/Scheduler | MERGED | Deferred/blocked ops posture + debt |
| R3E Experiment | MERGED | Explanatory; gate pending |
| Evidence Explorer + Decision Ledger | MERGED (UX-R2/R4) | Catalog + governed decisions above catalog |

### User outcome checklist

| Capability | Status |
|------------|--------|
| understand the current scientific cycle | YES (explanatory; no future-unseen results — correct) |
| inspect runs | YES |
| understand readiness | YES |
| inspect evidence | YES |
| inspect illustrative collection quality | YES |
| inspect governed decisions + reassessment triggers | YES (UX-R4) |
| distinguish UX acceptance from scientific approval | YES |
| distinguish data quality from scientific approval | YES |
| understand operational blockers | YES |
| identify the next safe action | YES |
| navigate coherently | YES |
| execute validation / peek / host / scheduler / R4 / R5 | NO (correctly blocked) |

## 3. Candidates assessed

| Candidate | Disposition | Rationale |
|-----------|-------------|-----------|
| No new UX until future-unseen data matures | **RECOMMEND_FOR_UX_R5** (as deferral posture) | Highest honesty; binding constraint is data/gate, not UX |
| Post-closure governance coherence (UX-R4 seed + catalog clock + decisionId deep-link) | DEFER_TO_LATER_UX_RELEASE / REJECTED_AS_LOW_VALUE as release | Polish only; does not change next safe action; avoid refresh treadmill |
| Reassessment queue derived from governed triggers | REJECTED_AS_REDUNDANT | Ledger already lists triggers descriptively; queue risks implying authorization |
| Evidence-to-decision traceability workspace | DEFER_TO_LATER_UX_RELEASE | Partial links exist (`?evidenceId=`); deeper workspace low urgency |
| Future-window progress history | DEFER_UNTIL_REAL_DATA | Readiness already states window insufficiency; history of real progress needs real collection truth |
| Data-quality trend history / charts | REJECTED_AS_REDUNDANT | Dados Coletados owns quality; charts rejected in UX-R3/R4 |
| Research hypothesis registry | DEFER_TO_LATER_UX_RELEASE | Risks implying recalibration authorization while R4 blocked |
| Experiment planning and comparison | DEFER_UNTIL_REAL_DATA / DEFER_TO_LATER_UX_RELEASE | R3E already explains M0–M5; real comparison needs data/gate |
| Scientific decision journal | REJECTED_AS_REDUNDANT | Decision Ledger already covers governed inspection |
| Release/governance timeline screen | REJECTED_AS_REDUNDANT | Duplicates Evidence + Ledger |
| Operational-debt register | REJECTED_AS_REDUNDANT | Host/Scheduler already owns debt visibility |
| Activate Backlog / Aprovações | REJECTED_AS_REDUNDANT | Implies approval workflow; planned-nav inactive |
| Future-unseen result surfaces | BLOCKED_BY_SCIENTIFIC_STATE | Peeking forbidden; validation not executed |
| Host/scheduler activation UX | BLOCKED_BY_OPERATIONAL_STATE | Discovery deferred; scheduler blocked |
| R4/R5 promotion UX | BLOCKED_BY_SCIENTIFIC_STATE | R4 blocked; scientific R5 not started |
| Real-data integration UI | DEFER_UNTIL_REAL_DATA | Unauthorized; needs later gated posture |

## 4. Value / feasibility (recommended deferral)

| Dimension | Score |
|-----------|-------|
| PRIMARY_USER_VALUE | HIGH (avoid false-confidence UX) |
| NEED_NOW | HIGH (stop inventing surfaces while waiting) |
| NON_DUPLICATION | HIGH |
| FIXTURE_BACKED_FEASIBILITY | N/A (no product increment) |
| SCIENTIFIC_SAFETY | HIGH |
| OPERATIONAL_SAFETY | HIGH |
| SECURITY | HIGH |
| ACCESSIBILITY | HIGH (preserve existing baselines) |
| TESTABILITY | HIGH (docs-only) |
| REVERSIBILITY | HIGH |
| SIZE | ZERO product delta |

## 5. Deferral record

```text
DECISION = DEFER_RECOMMENDED
UX_R5_RECOMMENDATION = NO_NEW_UX_RELEASE_NOW
UX_R5_DELIVERY_MODEL = D_DEFER_UX_R5
UX_R5_DIRECTION = NONE
UX_R5_INCREMENT_COUNT = 0

DEFERRAL_REASON =
  After UX-R4 CLOSED/ACCEPTED, the fixture-backed inspection loop Gustavo needs
  while waiting on future-unseen data is already available. Remaining gaps are
  polish/coherence, not a new user workflow. Opening UX-R5 now would invent
  product work without changing the safe next action.

REQUIRED_TRIGGER =
  READINESS changes away from NOT_READY/WINDOW_DAYS_INSUFFICIENT, and/or
  R3E_GATE advances beyond PENDING_FUTURE_UNSEEN_DATA under separate scientific
  authorization; optionally a separately authorized operational posture change
  (host discovery / scheduler) if that creates a new honest UX problem.

WHAT_CAN_PROCEED_INSTEAD =
  Continue scientific collection under existing ops guidance;
  keep using Overview/Runs/Readiness/Dados Coletados/R3E/Evidence+Ledger;
  accept operational debt as registered without activation fiction;
  docs/governance only — no UX-R5 product scope.

REASSESSMENT_CONDITION =
  Re-run UX-R5 discovery when the required trigger fires, or when a human
  authorizes a new discovery prompt with changed scientific/ops truth.
```

## 6. Architecture / boundaries (no recommended product direction)

No routes, navigation, fixtures, ViewModels, shared components, or dependencies are recommended for UX-R5 product work. Any future reassessment must re-prove fixture/no-backend/no-real-data feasibility and must preserve:

```text
UX_R5 != scientific R5
UX release numbering != scientific authorization
fixture-backed evidence != live truth
reassessment trigger != automatic authorization
governed decision != scientific approval
UX-R5 discovery does not unlock R4
UX-R5 discovery does not start scientific R5
```

## 7. Stop conditions

```text
STOP if product code is requested under this discovery
STOP if UX-R5 is marked STARTED without separate authorization
STOP if scientific R4 unlock or scientific R5 start is implied
STOP if real data / future-unseen / validate / peek / host / scheduler UX is proposed as “UX-R5”
```

## 8. Scientific and operational truth (immutable)

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
