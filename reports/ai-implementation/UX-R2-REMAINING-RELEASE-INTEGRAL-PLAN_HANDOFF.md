# UX-R2 Remaining Release Integral Plan — Handoff

```text
STATUS = FINAL_EVIDENCE_READY_FOR_HUMAN_MERGE_AUTHORIZATION
RELEASE = UX-R2
TASK_ID = UX-R2-REMAINING-RELEASE-INTEGRAL-PLAN-001
PHASE = INTEGRAL_RELEASE_PLANNING_AND_AUTHORIZATION_ASSESSMENT
CHANGE_RISK = HIGH

PR = 118
PR_URL = https://github.com/multivacia/wick/pull/118
BRANCH = cursor/ux-r2-remaining-integral-plan-04f5
BASE_SHA = 309589a0d79be012a932ffcad3668b2695917b10
PR_TIP = b0c14c4fbdf886c052f96536dc1e61d99d4637a3
FINAL_CANDIDATE_HEAD = 8cae0c7832fa35f03b3d7c6c0798db18955bb365
CONTENT_REVIEWED_THROUGH_HEAD = 8cae0c7832fa35f03b3d7c6c0798db18955bb365
POST_REVIEW_NORMATIVE_CHANGES = 0

ASSESSMENT_STATUS = COMPLETE
IMPACT_ASSESSMENT_STATUS = APPROVED
REVIEW_STATUS = APPROVED
DECISION = AUTHORIZED_FOR_SINGLE_EXECUTION_WITH_CONDITIONS

UX_R2_FINAL_PRODUCT_OBJECTIVE = Complete governed fixture-backed Evidence and Audit Explorer for curated metadata inspection without implying scientific approval, real-data readiness, or operational activation
UX_R2_PRIMARY_USER = Wick operator / governance reviewer (read-only)
UX_R2_PRIMARY_USER_JOURNEY = Evidências catalog → detail → optional MVP cross-links → understand R3D≠R3E / pending≠failed → exit without ops/validation
UX_R2_RELEASE_BOUNDARY = Fixture-backed read-only Evidence Explorer completion (I1+I2–I5); no backend/real-data/repo-FS/host-scheduler/gate-workflow/R4/R5
UX_R2_REMAINING_INCREMENT_COUNT = 4
UX_R2_REMAINING_INCREMENT_LIST = UX_R2_I2_EVIDENCE_CATALOG_RELEASE_AND_GATE_HISTORY; UX_R2_I3_EVIDENCE_PROVENANCE_AND_GOVERNANCE_STATE_UX; UX_R2_I4_EVIDENCE_CROSS_NAV_FROM_MVP_SCREENS; UX_R2_I5_EVIDENCE_EXPLORER_FIXTURE_ACCEPTANCE_AND_CLOSURE
UX_R2_INCREMENT_ORDER = I2 → I3 → I4 → I5
UX_R2_DEPENDENCY_GRAPH = I1→I2→I3→I4→I5
UX_R2_ACCEPTANCE_CRITERIA = catalog history; provenance UX; cross-nav; semantic inequalities tested; zero deps; no new routes/screens; UX-R1 preserved; truth unchanged; final review+human validation
UX_R2_CLOSURE_CRITERIA = UX-R2 fixture-backed Evidence and Audit Explorer scope is complete and governed
UX_R2_EXPLICIT_OUT_OF_SCOPE = real-data; runtime repo/FS; MD/HTML; downloads; Approvals/Backlog app; gate decision workflow; validate/peek; host/scheduler activation; R4/R5; experiment registry; FU payloads
UX_R2_DEFERRED_BACKLOG = C registry; F monitoring; G readiness progression beyond existing screen; H real-data read; I host/scheduler workflow; build-time ingest; backend index

SINGLE_BRANCH_MODEL = CONTINUOUS_SINGLE_BRANCH
SINGLE_DRAFT_PR_MODEL = ONE_DRAFT_PR_FOR_ALL_REMAINING_INCREMENT_WORK
INTERNAL_CHECKPOINT_MODEL = MANDATORY_SHA_TIED_RERUNNABLE_PASS_GATES
FINAL_REVIEW_MODEL = ONE_FINAL_INDEPENDENT_REVIEW
FINAL_HUMAN_VALIDATION_MODEL = ONE_FINAL_HUMAN_VALIDATION_BEFORE_MERGE
STOP_CONDITIONS = scope ambiguity; architecture beyond plan; new dependency; unapproved backend; real-data; runtime repo/FS; FU access; validate; peek; host/scheduler activation; secrets; scientific reinterpretation; R4/R5; security failure; unresolvable checkpoint; PR size/risk exceeded
MAXIMUM_PR_BOUNDARY = increments≤4; product_files≤40; net_lines≤2500; new_routes=0; new_screens=0; new_VMs=0; new_fixtures=0; deps=0
SPLIT_TRIGGER = exceed maxima without waiver; EXECUTION_BLOCKED; need backend/real-data/repo-read; human rejects continuous model
REQUIRED_HUMAN_INPUTS = merge authorization for this planning PR; separate execution prompt to set single-execution flags; final human validation before remaining-release merge
REQUIRED_EXTERNAL_DEPENDENCIES = none for frozen fixture-backed scope
FINAL_RECOMMENDATION = Authorize continuous single-branch execution of frozen I2–I5 only after a separate human-approved execution prompt; keep all implementation flags false until then
NEXT_RECOMMENDED_TASK = UX_R2_REMAINING_RELEASE_SINGLE_EXECUTION
NEXT_ITEM = UX_R2_SEPARATE_HUMAN_APPROVED_SINGLE_EXECUTION_PROMPT

FROZEN_SCOPE = docs/releases/UX-R2-REMAINING-RELEASE-FROZEN-SCOPE.md
IMPACT = docs/ai-impact/UX-R2-REMAINING-RELEASE-INTEGRAL-PLAN_IMPACT_ASSESSMENT.md
SPEC = docs/ai-specs/UX-R2-REMAINING-RELEASE-INTEGRAL-PLAN_SPEC.md
REVIEW = docs/ai-reviews/UX-R2-REMAINING-RELEASE-INTEGRAL-PLAN_REVIEW.md

UX_R2_REMAINING_IMPLEMENTATION_AUTHORIZED = false
UX_R2_SINGLE_BRANCH_EXECUTION_AUTHORIZED = false
UX_R2_SINGLE_PR_EXECUTION_AUTHORIZED = false
UX_R2_SINGLE_FINAL_VALIDATION_AUTHORIZED = false
PRODUCT_CODE_AUTHORIZED = false
REAL_DATA_INTEGRATION_AUTHORIZED = false
RUNTIME_REPOSITORY_ACCESS_AUTHORIZED = false
FUTURE_UNSEEN_RESULTS_ACCESS_AUTHORIZED = false
VALIDATION_EXECUTION_AUTHORIZED = false
EFFECT_PEEKING_AUTHORIZED = false
REAL_HOST_DISCOVERY_AUTHORIZED = false
SCHEDULER_ACTIVATION_AUTHORIZED = false
OPERATIONAL_ACTIONS_AUTHORIZED = false
R4_STATE_CHANGE_AUTHORIZED = false
R5_STATE_CHANGE_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false

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

BACKEND_TESTS = PASS
BACKEND_RUFF = PASS
GOVERNANCE_VALIDATOR = ERRORS_0_WARNINGS_0
FRONTEND_INSTALL = PASS
FRONTEND_TYPECHECK = PASS
FRONTEND_LINT = PASS
FRONTEND_TESTS = PASS
FRONTEND_A11Y = PASS
FRONTEND_BUILD = PASS
FRONTEND_AUDIT = PASS
CI_STATUS = GREEN
PR_MERGEABLE = true
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
```

## Official operational wording preserved

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```

## Notes

Docs-only planning PR. Does not implement I2–I5. Does not start the single-branch experiment. Implementation and single-execution authorization flags remain **false** until a separate human-approved execution prompt.
