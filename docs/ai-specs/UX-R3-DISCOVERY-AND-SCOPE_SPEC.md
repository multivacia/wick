# UX-R3 Discovery and Scope — Spec

```text
RELEASE = UX-R3
TASK_ID = UX-R3-DISCOVERY-AND-SCOPE-ASSESSMENT-001
PHASE = DISCOVERY_AND_SCOPE_ASSESSMENT
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
ASSESSMENT_ONLY = true
DECISION = SCOPE_RECOMMENDED
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
IMPACT = docs/ai-impact/UX-R3-DISCOVERY-AND-SCOPE_IMPACT_ASSESSMENT.md
PROPOSED_SCOPE = docs/releases/UX-R3-PROPOSED-SCOPE.md
```

## Discovery outcome

This specification records the **discovery outcome** for UX-R3: primary user problem, evaluated candidates, recommended direction, first increment, release boundary, process model, and explicit non-goals. It does **not** authorize implementation and does **not** mark UX-R3 started.

```text
UX_R3_STATUS = NOT_STARTED
UX_R3_SCOPE_AUTHORIZED = false
UX_R3_IMPLEMENTATION_AUTHORIZED = false
PRODUCT_CODE_AUTHORIZED = false
```

## Primary user problem

```text
While future-collection is IN_PROGRESS and readiness is NOT_READY due to
WINDOW_DAYS_INSUFFICIENT, Gustavo needs a governed place to understand
collection progress and data-quality posture without treating quality metrics
as scientific approval, validation readiness, or operational activation.
```

## Recommended direction

```text
UX_R3_RECOMMENDED_DIRECTION = E_COLLECTION_MONITORING_AND_DATA_QUALITY
UX_R3_FINAL_PRODUCT_OBJECTIVE =
  Fixture-backed collection monitoring and data-quality exploration via Dados Coletados.
UX_R3_PRIMARY_USER_OUTCOME =
  Inspect illustrative collection quality dimensions and relate them safely to
  Runs/Readiness/Evidence without executing collection or validation.
UX_R3_RELEASE_BOUNDARY =
  FIXTURE_BACKED_READ_ONLY; planned Dados Coletados activation; no backend;
  no real series; no future-unseen results; no ops controls; no R4/R5.
UX_R3_IMPLEMENTATION_POSTURE = FIXTURE_BACKED_READ_ONLY
UX_R3_PROCESS_MODEL = FULL_INCREMENTAL_FLOW
```

## First increment

```text
UX_R3_FIRST_INCREMENT = UX_R3_I1_COLLECTION_DATA_QUALITY_AUTHORIZATION_ASSESSMENT
UX_R3_FIRST_INCREMENT_RISK = MEDIUM
UX_R3_FIRST_INCREMENT_AUTHORIZATION_PREREQUISITE =
  This discovery PR merged + separate human-authorized authorization assessment prompt.
NEXT_RECOMMENDED_TASK = UX_R3_FIRST_INCREMENT_AUTHORIZATION_ASSESSMENT
```

## Candidate dispositions (summary)

```text
A EXPERIMENT_REGISTRY_AND_COMPARISON = DEFER_TO_LATER_UX_RELEASE
B SCIENTIFIC_GATE_AND_DECISION_WORKFLOW = DEFER_TO_LATER_UX_RELEASE
C RESEARCH_HYPOTHESIS_AND_EXPERIMENT_PLANNING = DEFER_TO_LATER_UX_RELEASE
D RELEASE_AND_GOVERNANCE_CENTER = REJECTED_AS_REDUNDANT
E COLLECTION_MONITORING_AND_DATA_QUALITY = RECOMMENDED_FOR_UX_R3
F CONTROLLED_REAL_DATA_READ_INTEGRATION = DEFER_TO_LATER_UX_RELEASE
G R3E_FUTURE_UNSEEN_PROGRESS_AND_EVENTUAL_RESULT_SURFACES = BLOCKED_BY_FUTURE_UNSEEN_GATE
H HOST_AND_SCHEDULER_OPERATIONAL_WORKFLOW = BLOCKED_BY_OPERATIONAL_DEPENDENCY
I STRATEGY_READINESS_AND_CONTROLLED_PROMOTION = BLOCKED_BY_FUTURE_UNSEEN_GATE
J NO_NEW_UX_RELEASE_UNTIL_R3E_DATA_GATE_CHANGES = REJECTED_AS_LOW_VALUE
```

## Posture recommendations

```text
REAL_DATA_POSTURE_RECOMMENDATION = FIXTURE_BACKED_READ_ONLY
BACKEND_POSTURE_RECOMMENDATION = NO_BACKEND_FOR_UX_R3
FUTURE_UNSEEN_POSTURE_RECOMMENDATION = NO_FUTURE_UNSEEN_RESULTS_SURFACES
OPERATIONAL_POSTURE_RECOMMENDATION = NO_HOST_SCHEDULER_ACTIONS
```

## Process model

```text
PROCESS_MODEL_RECOMMENDATION = FULL_INCREMENTAL_FLOW
WHEN_SINGLE_EXECUTION_IS_ALLOWED =
  Later frozen remaining multi-increment list + mandatory checkpoints +
  final independent review + final human validation + no backend/sci/ops mutation.
WHEN_INCREMENTAL_FLOW_IS_REQUIRED =
  Default for UX-R3 until such a freeze exists; any new route/VM/fixture family.
MANDATORY_CHECKPOINTS =
  architecture; increment; integration; regression; security; a11y; governance;
  final independent review.
MAXIMUM_RELEASE_BOUNDARY =
  Fixture-backed collection monitoring/data-quality only.
STOP_CONDITIONS =
  real-data/backend/FU/ops/scientific-reinterpretation/R4-implication requests;
  failed checkpoint; unresolved security finding; unauthorized scope expansion.
```

## Explicit out of scope

```text
UX_R3_EXPLICIT_OUT_OF_SCOPE =
  product code in this discovery;
  marking UX-R3 started;
  real-data / backend adapters;
  runtime repository or filesystem access;
  future-unseen result inspection;
  validation execution / effect peeking;
  host discovery / scheduler activation;
  approvals unlock workflow;
  experiment registry implementation;
  strategy promotion / R4 unlock / R5 start.
```

## Deferred backlog

```text
UX_R3_DEFERRED_BACKLOG =
  A experiment registry and comparison;
  B scientific gate and decision workflow;
  C research hypothesis and experiment planning;
  F controlled real-data read integration;
  G future-unseen progress/result surfaces;
  H host and scheduler operational workflow;
  I strategy readiness and controlled promotion.
```

## Scientific and operational truth (immutable)

```text
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_IMPLEMENTATION = COMPLETE
R3E_AUDIT = COMPLETE
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

## Official operational wording preserved

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```
