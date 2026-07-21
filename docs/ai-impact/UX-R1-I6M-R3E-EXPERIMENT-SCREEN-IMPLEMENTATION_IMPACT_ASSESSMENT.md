# UX-R1-I6M-R3E-EXPERIMENT-SCREEN-IMPLEMENTATION — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B9
PARENT_TASK = R3E-EXPERIMENT-SCREEN-IMPLEMENTATION-AUTHORIZATION-ASSESSMENT-001
TASK_ID = R3E-EXPERIMENT-SCREEN-IMPLEMENTATION-001
TITLE = R3E Experiment Screen Implementation
INCREMENT = I6M
PHASE = IMPLEMENTATION
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = true
R3E_EXPERIMENT_SCREEN_IMPLEMENTATION_AUTHORIZED = true
R3E_EXPERIMENT_SCREEN_MERGE_AUTHORIZED = false
R3E_VIEWMODEL_IMPLEMENTATION_AUTHORIZED = true
R3E_SYNTHETIC_FIXTURE_IMPLEMENTATION_AUTHORIZED = true
REAL_DATA_INTEGRATION_AUTHORIZED = false
FUTURE_UNSEEN_RESULTS_ACCESS_AUTHORIZED = false
VALIDATION_EXECUTION_AUTHORIZED = false
EFFECT_PEEKING_AUTHORIZED = false
SCIENTIFIC_INTERPRETATION_CHANGE_AUTHORIZED = false
OPERATIONAL_ACTIONS_AUTHORIZED = false
R4_STATE_CHANGE_AUTHORIZED = false
R5_STATE_CHANGE_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
R3E_IMPLEMENTATION = COMPLETE
R3E_AUDIT = COMPLETE
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R3E_FUTURE_VALIDATION = PENDING
COLLECTION = IN_PROGRESS
READINESS = NOT_READY
READINESS_REASON = WINDOW_DAYS_INSUFFICIENT
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
SCIENTIFIC_CONCLUSION = UNCHANGED
R3D_RESULT = NO_MEASURABLE_EDGE
R3E_STATUS = EXPLORATORY_COMPLETE_PENDING_FUTURE_UNSEEN_DATA
R3E_SCIENTIFIC_STATE_CHANGE = false
ECONOMIC_INTERPRETATION_ALLOWED = false
PR104_STATUS = MERGED
PR104_MERGE_COMMIT = 458b47b4fc260ac89fe8f9e3a396cdf8265a8f68
PR105_STATUS = MERGED
I6L_DECISION = AUTHORIZED_WITH_CONDITIONS
I6L_RECOMMENDED_IMPLEMENTATION_BOUNDARY = R3E_EXPERIMENT_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; EXPLANATORY_ONLY; NO_VISIBLE_FIXTURE_SELECTOR; NO_REAL_DATA; NO_FUTURE_UNSEEN_RESULTS; NO_VALIDATION_EXECUTION; NO_EFFECT_PEEKING; NO_TRADING_RECOMMENDATIONS; NO_PROFITABILITY_CLAIMS; NO_SCIENTIFIC_INTERPRETATION_CHANGE; NO_R4_OR_R5_STATE_CHANGE
FIXTURE_ID = r3e_experiment_current_state_illustrative
ROUTE = /experiments/r3e
SCREEN = Experimento R3E
NAV_LABEL = Experimento R3E
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 04e3bfe0adc6b373a81ba080cf49ded5ca03b324
FINAL_CANDIDATE_HEAD = PENDING_IMPLEMENTATION
CONTENT_REVIEWED_THROUGH_HEAD = PENDING_IMPLEMENTATION
POST_REVIEW_NORMATIVE_CHANGES = 0
ANALYZED_AT = 2026-07-21T01:12:00Z
ANALYZED_BY = cursor-agent
REVIEW_STATUS = PENDING_POST_IMPLEMENTATION
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTHORIZATION_DECISION = HUMAN_AUTHORIZED_FOR_THIS_TASK
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
FRONTEND_LOCATION = web/
```

G1 note: authorization covers **only** the read-only fixture-backed explanatory Experimento R3E screen (`/experiments/r3e`) with a dedicated ViewModel and synthetic fixture. It does **not** authorize real data, future-unseen result access, validation execution, effect peeking, trading recommendations, profitability claims, scientific interpretation changes, or R4/R5 state changes. Overview, Runs, Readiness and Host/Scheduler remain preserved. Merge remains blocked until separate human authorization.

## MANDATORY_CONSTRAINTS

```text
READ_ONLY = true
FIXTURE_BACKED = true
EXPLANATORY_ONLY = true
FIXTURE_ID = r3e_experiment_current_state_illustrative
NO_VISIBLE_FIXTURE_SELECTOR = true
NO_REAL_DATA = true
NO_FUTURE_UNSEEN_RESULTS = true
NO_VALIDATION_EXECUTION = true
NO_EFFECT_PEEKING = true
NO_TRADING_RECOMMENDATIONS = true
NO_PROFITABILITY_CLAIMS = true
NO_SCIENTIFIC_INTERPRETATION_CHANGE = true
NO_R4_OR_R5_STATE_CHANGE = true
NO_NETWORK_CLIENTS = true
NO_BACKEND_API = true
NO_EXTRA_RUNTIME_OR_DEV_DEPENDENCIES = true
TOKEN_ONLY_STYLING = true
REUSE_I3_PRIMITIVES = true
DEDICATED_R3E_VIEWMODEL_REQUIRED = true
DEDICATED_SYNTHETIC_FIXTURE_REQUIRED = true
PRESERVE_OVERVIEW_SCREEN = true
PRESERVE_RUNS_SCREEN = true
PRESERVE_READINESS_SCREEN = true
PRESERVE_HOST_SCHEDULER_SCREEN = true
EXPLORATORY_COMPLETE_IS_NOT_EDGE_PROVEN = true
AUDIT_COMPLETE_IS_NOT_FUTURE_VALIDATION_COMPLETE = true
PENDING_FUTURE_UNSEEN_IS_NOT_FAILED = true
R3D_NO_MEASURABLE_EDGE_IS_NOT_R3E_REJECTED = true
R3E_PENDING_IS_NOT_STRATEGY_APPROVED = true
STATISTICAL_SIGNIFICANCE_IS_NOT_ECONOMIC_USEFULNESS = true
MODEL_COMPARISON_IS_NOT_TRADING_RECOMMENDATION = true
VALIDATION_NOT_EXECUTED_IS_NOT_VALIDATION_FAILED = true
EFFECT_PEEKING_FALSE_IS_NOT_EFFECT_NOT_REPORTED = true
NO_FABRICATED_PVALUES_CI_EFFECT_SIZES = true
NO_FABRICATED_RETURNS_SHARPE_WINRATE_DRAWDOWN = true
ILLUSTRATIVE_IS_NOT_SCIENTIFIC_PROOF = true
WCAG_2_2_AA = true
PARALLEL_TASKS_ALLOWED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## SUMMARY

Implement the Wick product screen **Experimento R3E** at `/experiments/r3e`, introducing a dedicated `R3eExperimentViewModel` and synthetic fixture `r3e_experiment_current_state_illustrative`. The screen explains hypothesis, protocol, M0–M5, `DELTA_CANDLE = M5 − M4`, temporal/leakage/bootstrap/FDR concepts, and the pending future-unseen gate — without claiming an edge is proven, future validation passed, R4 unlocked, or economic usefulness. Read-only. Clearly labeled synthetic. No fabricated metrics.

## 1. Objetivo

Entregar a tela explicativa Experimento R3E com PageHeader, SyntheticDataNotice e seções obrigatórias (propósito, hipótese, distinção R3D/R3E, protocolo, famílias M0–M5, DELTA_CANDLE, validação temporal, leakage, bootstrap/FDR, estado científico, gate futuro, conhecido/desconhecido, próxima ação segura, evidências, estado parcial); testes de rota, semântica científica, a11y e fronteira; sem dados reais, validação, effect peeking ou recomendações de trading.

## 2. Contexto técnico

- I6L authorization assessment MERGED (PR #104 → `458b47b`); post-merge closure MERGED (PR #105 → `04e3bfe`).
- I6L decision: `AUTHORIZED_WITH_CONDITIONS`; dedicated ViewModel + fixture required.
- No R3E screen/ViewModel/fixture exists on `main` yet; nav item `r3e` is planned (`active: false`).
- Closest UI template: Host/Scheduler (I6K). Scientific semantics from `docs/experiments/R3E_CONTEXTUAL_EDGE_SPECIFICATION.md` and UX scientific/economic guardrails.
- Official posture: `R3E_GATE=PENDING_FUTURE_UNSEEN_DATA`, `R3D_RESULT=NO_MEASURABLE_EDGE`, `R4=BLOCKED`, `R5=NOT_STARTED`.

## 3. Componentes afetados

| Componente | Impacto |
|------------|---------|
| `web/src/viewmodels/**` | Novo `R3eExperimentViewModel` + builder |
| `web/src/fixtures/**` | Novo scenario id + catalog wiring |
| `web/src/screens/r3e-experiment/**` | Nova tela e seções |
| `web/src/app/AppRoutes.tsx` | Rota `/experiments/r3e` |
| `web/src/shell/navigation.ts` | Ativar nav **Experimento R3E** |
| `web/tests/**` | Screen / a11y / architecture tests |
| Overview / Runs / Readiness / Host | Preservados |
| R3E engine / validate / future unseen | Não executados / não alterados |
| Docs I6M (impact/spec/review/handoff) + PROJECT | Atualizados |

## 4. Arquivos previstos

```text
docs/ai-impact/UX-R1-I6M-R3E-EXPERIMENT-SCREEN-IMPLEMENTATION_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-I6M-R3E-EXPERIMENT-SCREEN-IMPLEMENTATION_SPEC.md
docs/ai-reviews/UX-R1-I6M-R3E-EXPERIMENT-SCREEN-IMPLEMENTATION_REVIEW.md
reports/ai-implementation/UX-R1-I6M-R3E-EXPERIMENT-SCREEN-IMPLEMENTATION_HANDOFF.md
docs/PROJECT.md
web/src/viewmodels/inputs.ts
web/src/viewmodels/outputs.ts
web/src/viewmodels/buildR3eExperimentViewModel.ts
web/src/viewmodels/presentation.ts
web/src/viewmodels/index.ts
web/src/fixtures/types.ts
web/src/fixtures/scenarios.ts
web/src/fixtures/catalog.ts
web/src/fixtures/builders.ts (se necessário)
web/src/screens/r3e-experiment/**
web/src/app/AppRoutes.tsx
web/src/shell/navigation.ts
web/tests/screens/r3e-experiment/**
web/tests/a11y/r3eExperiment.a11y.test.tsx
web/tests/viewmodels/** (se necessário)
```

## 5. Contratos e interfaces

```text
ROUTE = /experiments/r3e
NAV_LABEL = Experimento R3E
PAGE_TITLE = Experimento R3E
NAV_GROUP = Experimentos
FIXTURE_ID = r3e_experiment_current_state_illustrative

VIEWMODEL = R3eExperimentViewModel
ALLOWED_FIELDS =
  experimentId, parentExperimentId, title, purpose, hypothesis,
  protocolVersion, modelFamilies, modelStages M0–M5,
  deltaCandleDefinition, temporalValidationSummary, holdoutSummary,
  leakageProtectionSummary, bootstrapSummary, fdrSummary,
  currentScientificState, r3dResult, r3eGate, collectionState,
  readinessState, validationExecutionState, effectPeekingState,
  knownStatements, unknownStatements, nextSafeScientificAction,
  evidenceReferences

FORBIDDEN_FABRICATION =
  p-values, confidence intervals, effect sizes,
  returns / Sharpe / win rate / drawdown / profitability,
  future-unseen outcomes, validation timestamps of unrun validation,
  dataset counts / market symbols / cost tables as proof,
  trading recommendations / strategy approval
```

## 6. Persistência e dados

Sem persistência backend. Fonte: ViewModel sintético + fixture dedicada. Sem fetch de resultados futuros, sem leitura de audits numéricos como prova na UI, sem localStorage operacional.

## 7. Concorrência, locks e idempotência

N/A backend. Montagem determinística a partir do fixture id fixo da rota de produto.

## 8. Segurança

```text
NO_SECRETS = true
NO_REAL_DATA = true
NO_FUTURE_UNSEEN_RESULTS = true
NO_VALIDATION_EXECUTION = true
NO_EFFECT_PEEKING = true
NO_TRADING_RECOMMENDATIONS = true
NO_PROFITABILITY_CLAIMS = true
NO_SCIENTIFIC_INTERPRETATION_CHANGE = true
NO_R4_OR_R5_STATE_CHANGE = true
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
EVIDENCE_AS_TEXT_ONLY = true
```

## 9. Observabilidade

Sem telemetria. Validação por suite UX-R1 + governance validator + CI.

## 10. Operação

Não altera coleta, scheduler, host, validate, R3E gate, R4/R5 nem conclusões. A tela permanece explicativa e advisory (`nextSafeScientificAction` texto apenas).

## 11. Rollback

```text
ROLLBACK = revert implementation PR
NEVER via R3E validate / future unseen / R4 / R5
```

## 12. Compatibilidade

- Consome I2/I3/I5/I6B/I6C e padrões I6E–I6K.
- Overview/Runs/Readiness/Host preservados.
- Rota alinha I5A/IA (`/experiments/r3e`); `/research/r3e` não introduzido.
- UX-B9 backlog item entregue como incremento I6M sob condições I6L.

## 13. Testes necessários

```text
/experiments/r3e renders real explanatory screen
synthetic notice visible; dedicated fixture used
R3D NO_MEASURABLE_EDGE distinct from R3E pending
M0–M5 + DELTA_CANDLE without significance/profit claims
temporal/holdout/leakage/bootstrap/FDR qualitative only
future unseen gate pending; validation not executed ≠ failed
effect peeking false ≠ not reported
no future unseen results / trading recommendations / profitability
R4 blocked; R5 not started
Overview/Runs/Readiness/Host preserved
no visible fixture selector
responsive + axe + architecture boundary
```

## 14. Alternativas consideradas

| Alternativa | Decisão |
|-------------|--------|
| Reusar Overview ViewModel sem VM R3E | REJECTED — I6L exige ViewModel dedicado |
| Reusar `current_project_state_illustrative` como único fixture | REJECTED — I6L exige fixture R3E dedicado |
| Incluir tabelas de `R3E_REAL_DATA_RESULTS.md` | REJECTED — risco de interpretação econômica |
| Autorizar validate / effect peeking | REJECTED — fora do boundary |
| Rota `/research/r3e` | REJECTED — I6L |

## 15. Decisão

```text
IMPACT_ASSESSMENT_STATUS = APPROVED
AUTHORIZATION_DECISION = HUMAN_AUTHORIZED_FOR_THIS_TASK
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
R3E_EXPERIMENT_SCREEN_IMPLEMENTATION_AUTHORIZED = true
R3E_EXPERIMENT_SCREEN_MERGE_AUTHORIZED = false
```

Proceed with implementation under the mandatory constraints above. Fresh independent review required after implementation. Do not merge without separate human merge authorization.
