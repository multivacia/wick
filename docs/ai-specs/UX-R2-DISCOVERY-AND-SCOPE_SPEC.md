# UX-R2 — Discovery and Scope Specification

```text
RELEASE = UX-R2
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE R2
TASK_ID = UX-R2-DISCOVERY-AND-SCOPE-ASSESSMENT-001
PHASE = DISCOVERY_AND_SCOPE_ASSESSMENT
CHANGE_RISK = HIGH
SPEC_STATUS = DRAFT_FOR_ASSESSMENT
DECISION = SCOPE_RECOMMENDED
ASSESSMENT_ONLY = true

UX_R2_IMPLEMENTATION_AUTHORIZED = false
UX_R2_PRODUCT_CODE_AUTHORIZED = false
REAL_DATA_INTEGRATION_AUTHORIZED = false
REAL_HOST_DISCOVERY_AUTHORIZED = false
SCHEDULER_ACTIVATION_AUTHORIZED = false
OPERATIONAL_ACTIONS_AUTHORIZED = false
VALIDATION_EXECUTION_AUTHORIZED = false
EFFECT_PEEKING_AUTHORIZED = false
FUTURE_UNSEEN_RESULTS_ACCESS_AUTHORIZED = false
SCIENTIFIC_INTERPRETATION_CHANGE_AUTHORIZED = false
R4_STATE_CHANGE_AUTHORIZED = false
R5_STATE_CHANGE_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
```

## 1. Purpose

This specification records the **discovery outcome** for UX-R2: the primary user problem, evaluated candidate directions, recommended direction, recommended first increment, release boundary, and explicit non-goals. It does **not** authorize implementation.

## 2. Prerequisite (UX-R1)

```text
UX_R1_RELEASE_STATUS = CLOSED
UX_R1_RELEASE_ACCEPTANCE_STATUS = ACCEPTED
UX_R1_RELEASE_SCOPE = FIXTURE_BACKED_READ_ONLY
UX_R1_RELEASE_ACCEPTANCE_WORDING = UX-R1 fixture-backed read-only scope is complete and governed.
```

Accepted UX-R1 routes remain the operational MVP status surfaces. UX-R2 must not reopen UX-R1 as incomplete; it extends with a new governed evidence surface.

## 3. Primary user problem

Operators need a governed place to **browse evidence and audit records** (what exists, what was decided, what is known vs unknown) without:

- treating fixtures as live truth without disclosure;
- activating host/scheduler controls;
- executing collection/validate;
- inspecting future-unseen result payloads;
- conflating evidence with scientific approval or trading readiness.

## 4. Candidates evaluated

```text
CANDIDATES_EVALUATED =
  A_GOVERNED_REAL_DATA_READ_INTEGRATION;
  B_COLLECTION_MONITORING_AND_OPERATIONAL_EVIDENCE;
  C_EXPERIMENT_REGISTRY_AND_COMPARISON;
  D_EVIDENCE_AND_AUDIT_EXPLORER;
  E_SCIENTIFIC_DECISION_GATE_WORKFLOW;
  F_HOST_DISCOVERY_AND_SCHEDULER_ACTIVATION_WORKFLOW;
  G_R3E_FUTURE_UNSEEN_READINESS_PROGRESSION;
  H_RELEASE_HISTORY_AND_GOVERNANCE_CENTER
```

### Disposition

| Candidate | Disposition for UX-R2 start |
|-----------|-----------------------------|
| A | Deferred — high value, needs adapter + security gates; not I1 |
| B | Deferred — ops value high; peeking/false-confidence risk until allowlists exist |
| C | Optional later — valuable; lower urgency than evidence surface |
| D | **Recommended direction** |
| E | Out of scope until R3E gate data ready and separate HIGH auth |
| F | Out of scope while `HOST_DISCOVERY=DEFERRED` |
| G | Blocked by `WINDOW_DAYS_INSUFFICIENT` / false-progress risk |
| H | Compatible companion; fold release/gate history **as evidence records** into D rather than a separate first increment |

## 5. Recommended direction

```text
RECOMMENDED_DIRECTION = D_EVIDENCE_AND_AUDIT_EXPLORER
RECOMMENDED_DATA_POSTURE = FIXTURE_BACKED_FIRST
RECOMMENDED_OPERATIONAL_POSTURE = READ_ONLY_NO_CONTROLS
RECOMMENDED_SCIENTIFIC_POSTURE = EVIDENCE_DISPLAY_ONLY_NO_INTERPRETATION_CHANGE
RECOMMENDED_RELEASE_BOUNDARY = EVIDENCE_EXPLORER_ONLY_FIXTURE_BACKED_READ_ONLY
```

### Recommended first increment (authorization only)

```text
RECOMMENDED_FIRST_INCREMENT = UX_R2_I1_EVIDENCE_EXPLORER_AUTHORIZATION_ASSESSMENT
INCREMENT_GOAL = Authorize (later) a fixture-backed read-only Evidence Explorer screen
PROPOSED_NAV = Evidências (currently planned/inactive)
PROPOSED_ROUTE_CANDIDATE = /governance/evidence
REQUIRED_PATTERN = dedicated ViewModel + synthetic fixture + synthetic disclosure
ADAPTERS = NOT_IN_I1
REAL_DATA = NOT_IN_I1
```

I1 in this discovery means the **next assessment task**, not product implementation.

## 6. Required human inputs

```text
REQUIRED_HUMAN_INPUTS =
  MERGE_THIS_DISCOVERY_ASSESSMENT;
  AUTHORIZE_SEPARATE_I1_AUTHORIZATION_ASSESSMENT;
  LATER_AUTHORIZE_I1_IMPLEMENTATION_IF_APPROVED;
  SEPARATE_AUTH_FOR_ANY_REAL_DATA_OR_STATIC_AUDIT_ADAPTER;
  SEPARATE_AUTH_FOR_HOST_OR_SCHEDULER_WORK
```

## 7. Required external dependencies

```text
REQUIRED_EXTERNAL_DEPENDENCIES =
  NONE_FOR_FIXTURE_BACKED_I1;
  REAL_HOST_NOT_REQUIRED_NOW;
  PROVIDER_CREDENTIALS_NOT_REQUIRED_NOW;
  FUTURE_UNSEEN_WINDOW_NOT_REQUIRED_FOR_I1
```

## 8. Required pre-implementation gates

```text
REQUIRED_PRE_IMPLEMENTATION_GATES =
  G0_DISCOVERY_ASSESSMENT_MERGED;
  G1_I1_AUTHORIZATION_IMPACT_APPROVED;
  G2_I1_HUMAN_IMPLEMENTATION_AUTHORIZATION;
  G3_ARCHITECTURE_BOUNDARY_TESTS_REMAIN_ENFORCED;
  G4_ANY_ADAPTER_REQUIRES_OWN_HIGH_IMPACT_AND_SECURITY_REVIEW;
  G5_HOST_SCHEDULER_REMAIN_SEPARATELY_GATED
```

## 9. Explicit out of scope

```text
EXPLICIT_OUT_OF_SCOPE =
  PRODUCT_CODE_IN_THIS_TASK;
  UX_R2_IMPLEMENTATION_NOW;
  REAL_DATA_ADAPTERS;
  OPS_UI_INDEX;
  HOST_DISCOVERY_UI_OR_EXECUTION;
  SCHEDULER_ACTIVATION;
  COLLECTION_OR_VALIDATE_COMMANDS;
  FUTURE_UNSEEN_RESULT_PAYLOAD_INSPECTION;
  APPROVALS_WORKFLOW;
  SCIENTIFIC_GATE_DECISION_UI;
  R4_UNLOCK;
  R5_START;
  TRADING_OR_PRODUCTION_READINESS_CLAIMS;
  PARALLEL_TASKS
```

## 10. Provisional UX-R2 closure criteria

UX-R2 may later be closed when authorized increments within its declared boundary are complete and governed, with acceptance wording that does **not** claim production/trading readiness, real-data completeness (unless separately accepted), scheduler activation, strategy approval, edge proof, future validation complete, R4 unlocked, or R5 started.

## 11. Scientific and operational invariants

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
SCIENTIFIC_CONCLUSION = UNCHANGED
```

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```

## 12. Next task

```text
NEXT_RECOMMENDED_TASK = UX_R2_I1_EVIDENCE_EXPLORER_AUTHORIZATION_ASSESSMENT
NEXT_ITEM = UX_R2_I1_EVIDENCE_EXPLORER_AUTHORIZATION_SEPARATE_ASSESSMENT
```
