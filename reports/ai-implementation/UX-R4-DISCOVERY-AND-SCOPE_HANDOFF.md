# UX-R4 Discovery and Scope Assessment — Handoff

```text
STATUS = FINAL_EVIDENCE_READY_FOR_HUMAN_MERGE_AUTHORIZATION
RELEASE = UX-R4
TASK_ID = UX-R4-DISCOVERY-AND-SCOPE-ASSESSMENT-001
PHASE = DISCOVERY_AND_SCOPE_ASSESSMENT
CHANGE_RISK = MEDIUM
ASSESSMENT_AUTHORIZED = true

PR = PENDING
PR_URL = PENDING
BRANCH = cursor/ux-r4-discovery-and-scope-assessment-04f5
BASE_SHA = 16bf2bd72c26cc804f7e630b504b74878848bed2
PR_TIP = 60993f02887b8d4c45bc362cf7847b93a5553b04
FINAL_CANDIDATE_HEAD = 8d1140262082c608b92d9f337b839e33968b76e9
CONTENT_REVIEWED_THROUGH_HEAD = 8d1140262082c608b92d9f337b839e33968b76e9
POST_REVIEW_NORMATIVE_CHANGES = 0

DISCOVERY_STATUS = COMPLETE
IMPACT_ASSESSMENT_STATUS = APPROVED
REVIEW_STATUS = APPROVED
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

CURRENT_UX_BASELINE =
  Overview+Runs+Readiness+Dados Coletados+Host/Scheduler+R3E+Evidence MERGED;
  Backlog/Aprovações/Backups/Incidentes still placeholder.
CURRENT_USER_OUTCOMES =
  Collection quality, readiness, runs, evidence, ops blockers, and coherent
  cross-nav are available fixture-backed; compact decision ledger is not.
CURRENT_GAPS =
  Post-UX-R3 decision state not inspectable as a governed ledger in product UI;
  Evidence catalog NOW_ISO still 2026-07-21 (pre-UX-R3 closure).
DUPLICATION_FINDINGS =
  New governance timeline / Backlog / Aprovações / ops-debt center / quality
  charts would duplicate existing surfaces — rejected.
SCIENTIFIC_BOUNDARY_FINDINGS =
  R3E gate pending future-unseen; R4 blocked; R5 not started; UX_R4 != R4.
OPERATIONAL_BOUNDARY_FINDINGS =
  Host discovery deferred; scheduler blocked; operational debt open and already
  visible on Host/Scheduler.
ARCHITECTURAL_FINDINGS =
  Stay on /governance/evidence; fixture+VM+screen path only; no backend.
SECURITY_FINDINGS =
  No fs/fetch/Markdown/raw HTML/downloads/external hrefs required.
ACCESSIBILITY_FINDINGS =
  Existing Evidence Explorer a11y baseline retained; later I2 must keep axe green.

CANDIDATES_ASSESSED = 14
CANDIDATE_DISPOSITIONS =
  RECOMMEND_FOR_UX_R4=1;
  REJECTED_AS_REDUNDANT=4;
  REJECTED_AS_LOW_VALUE=2;
  DEFER_TO_LATER_UX_RELEASE=3;
  DEFER_UNTIL_REAL_DATA=1;
  BLOCKED_BY_SCIENTIFIC_STATE=2;
  BLOCKED_BY_OPERATIONAL_STATE=1
VALUE_TEST_RESULTS =
  Recommended candidate HIGH primary value / HIGH fixture feasibility /
  HIGH scientific+ops safety / MEDIUM size.
STOP_CONDITIONS = none triggered

UNRESOLVED_BLOCKERS = NONE
ACCEPTED_LIMITATIONS =
  Exact ledger schema deferred to I1 authorization;
  I2–I3 unauthorized until separate prompts;
  no live repository browsing.
REQUIRED_HUMAN_INPUTS =
  Merge authorization for this discovery PR;
  later separate I1 authorization assessment prompt.
REQUIRED_EXTERNAL_DEPENDENCIES = NONE
FINAL_RECOMMENDATION =
  Approve and merge this docs-only discovery PR; then run separate
  UX_R4_I1_DECISION_LEDGER_AUTHORIZATION_ASSESSMENT; do not start product,
  unlock R4, or start R5.
NEXT_RECOMMENDED_TASK = UX_R4_I1_DECISION_LEDGER_AUTHORIZATION_ASSESSMENT
NEXT_ITEM = UX_R4_I1_AUTHORIZATION_SEPARATE_ASSESSMENT_NOT_STARTED

UX_R3_RELEASE_STATUS = CLOSED
UX_R3_RELEASE_ACCEPTANCE_STATUS = ACCEPTED
UX_R4_STATUS = NOT_STARTED
UX_R4_SCOPE_AUTHORIZED = false
UX_R4_IMPLEMENTATION_AUTHORIZED = false
PRODUCT_CODE_AUTHORIZED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED

BACKEND_TESTS = PENDING
BACKEND_RUFF = PENDING
GOVERNANCE_VALIDATOR = PENDING
FRONTEND_INSTALL = PENDING
FRONTEND_TYPECHECK = PENDING
FRONTEND_LINT = PENDING
FRONTEND_TESTS = PENDING
FRONTEND_A11Y = PENDING
FRONTEND_BUILD = PENDING
FRONTEND_AUDIT = PENDING
CI_STATUS = PENDING
PR_MERGEABLE = PENDING
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION

HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
COLLECTION = IN_PROGRESS
READINESS = NOT_READY
READINESS_REASON = WINDOW_DAYS_INSUFFICIENT
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
R3D_RESULT = NO_MEASURABLE_EDGE
R3E_STATUS = EXPLORATORY_COMPLETE_PENDING_FUTURE_UNSEEN_DATA
SCIENTIFIC_CONCLUSION = UNCHANGED
R3E_SCIENTIFIC_STATE_CHANGE = false

REPOSITORY = multivacia/wick
BASE_BRANCH = main
CREATED_AT = 2026-07-23T12:48:33Z
CREATED_BY = cursor-agent
```

## Official operational wording preserved

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```
