# UX-R1-I6M — R3E Experiment Screen Implementation Spec

```text
RELEASE = UX-R1
INCREMENT = I6M
TASK_ID = R3E-EXPERIMENT-SCREEN-IMPLEMENTATION-001
PHASE = IMPLEMENTATION
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_STATUS = COMPLETE
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
IMPACT = docs/ai-impact/UX-R1-I6M-R3E-EXPERIMENT-SCREEN-IMPLEMENTATION_IMPACT_ASSESSMENT.md
ROUTE = /experiments/r3e
SCREEN = Experimento R3E
NAV_LABEL = Experimento R3E
FIXTURE_ID = r3e_experiment_current_state_illustrative
VIEWMODEL = R3eExperimentViewModel
READ_ONLY = true
FIXTURE_BACKED = true
EXPLANATORY_ONLY = true
NO_VISIBLE_FIXTURE_SELECTOR = true
```

## Objective

Deliver the fixture-backed, read-only explanatory **Experimento R3E** product screen at `/experiments/r3e`, consuming a dedicated `R3eExperimentViewModel` and synthetic fixture. Explain hypothesis, protocol, M0–M5, `DELTA_CANDLE = M5 − M4`, temporal/leakage/bootstrap/FDR concepts, and the pending future-unseen gate — without claiming an edge is proven, future validation passed, R4 unlocked, or economic usefulness.

## Behavior

Answer in plain language first:

1. What is the purpose of R3E?
2. What is the main hypothesis (H2)?
3. How do R3D and R3E conclusions differ?
4. What are M0–M5?
5. What is DELTA_CANDLE?
6. How does temporal validation / holdout / leakage protection work?
7. What are bootstrap and FDR (conceptually)?
8. What is the current scientific state and R3E gate?
9. Was future validation executed? Was effect peeking performed?
10. What is known vs not known?
11. What is the next safe scientific action?

## Sections

```text
PageHeader
SyntheticDataNotice
ExperimentPurpose
HypothesisSummary
R3DAndR3EDistinction
ProtocolSummary
ModelFamilyComparison
M0M5Explanation
DeltaCandleExplanation
TemporalValidationSummary
LeakageProtection
BootstrapAndFDRExplanation
CurrentScientificState
FutureUnseenGate
WhatIsKnown
WhatIsNotKnown
NextSafeScientificAction
EvidenceReferences
PartialUnknownState
```

Visible synthetic labels: `Dados ilustrativos`, `Synthetic fixture`, plus R3E science disclaimer.

## Semantics

```text
EXPLORATORY_COMPLETE != EDGE_PROVEN
AUDIT_COMPLETE != FUTURE_VALIDATION_COMPLETE
PENDING_FUTURE_UNSEEN_DATA != FAILED
NO_MEASURABLE_EDGE_IN_R3D != R3E_REJECTED
R3E_PENDING != STRATEGY_APPROVED
STATISTICAL_SIGNIFICANCE != ECONOMIC_USEFULNESS
MODEL_COMPARISON != TRADING_RECOMMENDATION
VALIDATION_NOT_EXECUTED != VALIDATION_FAILED
EFFECT_PEEKING_FALSE != EFFECT_NOT_REPORTED
```

## Out of scope

```text
real data integration
future unseen results access
validation execution
effect peeking
trading recommendations
profitability claims
fabricated p-values / returns / Sharpe
R4 unlock / R5 start
visible fixture selector
/research/r3e route
```

## Acceptance

See `reports/ai-implementation/UX-R1-I6M-R3E-EXPERIMENT-SCREEN-IMPLEMENTATION_HANDOFF.md`.
