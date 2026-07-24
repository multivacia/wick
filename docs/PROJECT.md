# Wick — Visão do Projeto

## Missão

Avaliar, com rigor quantitativo e auditável, se padrões de candlestick apresentam vantagem preditiva líquida após custos — antes de qualquer uso de dinheiro real.

## Princípios

- Detectar padrão não é recomendar compra ou venda.
- Resultados devem ser reproduzíveis (`run_id`, versões, seeds).
- Dados incompletos nunca são tratados como completos.
- Sem look-ahead: confirmação e entrada respeitam disponibilidade temporal.
- Long-only por padrão; short só com decisão explícita.
- Nenhum dinheiro real até R3 e R4 concluídas e auditadas; ordens reais só a partir da R6.

## Roadmap

| Release | Escopo | Status |
|---------|--------|--------|
| R1 | Setup, schema, ingestão OHLCV idempotente e auditável | **MERGED** (`R1_GATE = APPROVED`, tag `v0.1.0-r1`) |
| R2 | Detectores de padrões com contrato matemático versionado | **MERGED** (`R2_GATE = APPROVED`, tag `v0.2.0-r2`) |
| R3A–C | Motor, estatística, relatórios e gates mecânicos | **MERGED** (`R3_IMPLEMENTATION/AUDIT = COMPLETE`, tag `v0.3.0-r3`) |
| R3D | Validação em dados históricos reais (sem recalibrar) | **COMPLETE** (`R3_GATE = REJECTED_NO_MEASURABLE_EDGE_V1`, tag `v0.4.0-r3d-real-validation`) |
| R3E | Motor contextual M0–M5 (nested WF) | **CODE APPROVED** (`v0.5.0-r3e-engine`); real-data run **COMPLETE** (exploratório) |
| R3E-FU | Infra de validação final com dados futuros não vistos | **ENGINE COMPLETE** (coleta `NOT_STARTED`) |
| R4 | Paper trading / simulação temporal sem ordem real | **BLOCKED** |
| R5 | Observabilidade, relatórios e gates de promoção | **NOT_STARTED** |
| R6+ | Integração com corretora (fora do escopo atual) | — |

## Trilha paralela — UX (experiência operacional)

Release **independente** do estado científico de R3E. Não modifica modelos, coleta, `validate`, readiness, scheduler, thresholds nem desbloqueia R4/R5.

| Campo | Valor |
|-------|--------|
| RELEASE_ID | UX-R1 |
| RELEASE_NAME | WICK OPERATIONAL EXPERIENCE |
| UX_R1_STATUS / UX-R1_STATUS | **CLOSED_ACCEPTED_FIXTURE_BACKED_READ_ONLY** |
| UX_R1_FINAL_CLOSURE_ASSESSMENT_STATUS | **MERGED** |
| UX_R1_FINAL_CLOSURE_ASSESSMENT_DECISION | **ACCEPTED_FOR_CLOSURE** |
| UX_R1_RELEASE_STATUS | **CLOSED** |
| UX_R1_RELEASE_ACCEPTANCE_STATUS | **ACCEPTED** |
| UX_R1_RELEASE_SCOPE | **FIXTURE_BACKED_READ_ONLY** |
| UX_R1_RELEASE_CLOSURE_AUTHORIZED | **true** |
| UX_R1_RELEASE_ACCEPTANCE_AUTHORIZED | **true** |
| UX_R1_RELEASE_CLOSED | **true** |
| UX_R1_RELEASE_ACCEPTED | **true** |
| UX_R1_RELEASE_ACCEPTANCE_WORDING | **UX-R1 fixture-backed read-only scope is complete and governed.** |
| Formal closure record | `docs/releases/UX-R1-FORMAL-RELEASE-CLOSURE-AND-ACCEPTANCE.md` |
| UX_R2_STATUS / UX-R2_STATUS | **CLOSED_ACCEPTED_FIXTURE_BACKED_EVIDENCE_AND_AUDIT_EXPLORATION** |
| UX_R2_DISCOVERY_ASSESSMENT_STATUS | **MERGED** |
| UX_R2_DISCOVERY_AND_SCOPE_STATUS | **MERGED** |
| UX_R2_DISCOVERY_DECISION | **SCOPE_RECOMMENDED** |
| UX_R2_DISCOVERY_AND_SCOPE_DECISION | **SCOPE_RECOMMENDED** |
| UX_R2_RECOMMENDED_DIRECTION | **D_EVIDENCE_AND_AUDIT_EXPLORER** |
| UX_R2_RECOMMENDED_FIRST_INCREMENT | **UX_R2_I1_EVIDENCE_EXPLORER_AUTHORIZATION_ASSESSMENT** |
| UX_R2_I1_STATUS | **IMPLEMENTATION_MERGED** |
| UX_R2_I1_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| UX_R2_I1_EVIDENCE_EXPLORER_AUTHORIZATION_ASSESSMENT_STATUS | **MERGED** |
| UX_R2_I1_EVIDENCE_EXPLORER_AUTHORIZATION_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| UX_R2_I1_RECOMMENDED_ROUTE | **/governance/evidence** |
| UX_R2_I1_RECOMMENDED_NAV_LABEL | **Evidências** |
| UX_R2_I1_RECOMMENDED_IMPLEMENTATION_POSTURE | **A_STATIC_FIXTURE_BACKED_EVIDENCE_CATALOG** |
| UX_R2_I1_RECOMMENDED_IMPLEMENTATION_BOUNDARY | **EVIDENCE_EXPLORER_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; CURATED_MANIFEST_ONLY; LIST_AND_DETAIL; NO_RUNTIME_REPOSITORY_ACCESS; NO_REAL_DATA; NO_FUTURE_UNSEEN_RESULTS** |
| UX_R2_I1_EVIDENCE_EXPLORER_IMPLEMENTATION_STATUS | **MERGED** (PR #116 → `d820f05`) |
| UX_R2_I1_EVIDENCE_EXPLORER_REVIEW_STATUS | **APPROVED** |
| UX_R2_I1_EVIDENCE_EXPLORER_ROUTE | **/governance/evidence** |
| UX_R2_I1_EVIDENCE_EXPLORER_POSTURE | **A_STATIC_FIXTURE_BACKED_EVIDENCE_CATALOG** |
| UX_R2_I1_FIXTURE_ID | **evidence_catalog_current_state_illustrative** |
| UX_R2_REMAINING_RELEASE_INTEGRAL_PLAN_STATUS | **MERGED** (PR #118 → `47c31e2`) |
| UX_R2_REMAINING_RELEASE_SINGLE_EXECUTION_STATUS | **MERGED** (PR #120 → `2112e6a`) |
| UX_R2_REMAINING_RELEASE_FINAL_REVIEW_STATUS | **APPROVED** |
| UX_R2_I2_STATUS | **MERGED** |
| UX_R2_I3_STATUS | **MERGED** |
| UX_R2_I4_STATUS | **MERGED** |
| UX_R2_I5_STATUS | **MERGED** |
| UX_R2_FINAL_REVIEW_STATUS | **APPROVED** |
| UX_R2_EXECUTION_MODEL | **SINGLE_BRANCH_SINGLE_PR_SINGLE_FINAL_VALIDATION** |
| UX_R2_RELEASE_STATUS | **CLOSED** |
| UX_R2_RELEASE_ACCEPTANCE_STATUS | **ACCEPTED** |
| UX_R2_RELEASE_SCOPE | **FIXTURE_BACKED_EVIDENCE_AND_AUDIT_EXPLORATION** |
| UX_R2_ACCEPTANCE_WORDING | **UX-R2 fixture-backed evidence and audit exploration scope is complete, accepted, and governed.** |
| UX_R2_RELEASE_CLOSED | **true** |
| UX_R2_RELEASE_ACCEPTED | **true** |
| Formal closure record | `docs/releases/UX-R2-FORMAL-RELEASE-CLOSURE-AND-ACCEPTANCE-STAMP.md` |
| UX_R2_FINAL_CLOSURE_AND_ACCEPTANCE_ASSESSMENT_STATUS | **MERGED** (PR #122 → `dda0667`) |
| UX_R2_FINAL_CLOSURE_AND_ACCEPTANCE_DECISION | **CLOSURE_AND_ACCEPTANCE_RECOMMENDED** |
| UX_R2_FINAL_ASSESSMENT_DECISION | **CLOSURE_AND_ACCEPTANCE_RECOMMENDED** |
| UX_R2_RELEASE_CLOSURE_AUTHORIZED | **true** |
| UX_R2_RELEASE_ACCEPTANCE_AUTHORIZED | **true** |
| UX_R2_RELEASE_STAMP_AUTHORIZED | **true** |
| UX_R3_STATUS | **CLOSED** / **ACCEPTED** |
| UX_R3_DISCOVERY_AND_SCOPE_STATUS | **MERGED** (PR #126 → `e23bfe9`) |
| UX_R3_DISCOVERY_DECISION | **SCOPE_RECOMMENDED** |
| UX_R3_RECOMMENDED_DIRECTION | **E_COLLECTION_MONITORING_AND_DATA_QUALITY** |
| UX_R3_RECOMMENDED_FIRST_INCREMENT | **UX_R3_I1_COLLECTION_DATA_QUALITY_AUTHORIZATION_ASSESSMENT** |
| UX_R3_I1_STATUS | **MERGED** |
| UX_R3_I1_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| UX_R3_I1_COLLECTION_DATA_QUALITY_AUTHORIZATION_STATUS | **MERGED** (PR #128 → `95fd5b8`) |
| UX_R3_I1_COLLECTION_DATA_QUALITY_AUTHORIZATION_ASSESSMENT_STATUS | **MERGED** (PR #128 → `95fd5b8`) |
| UX_R3_I1_AUTHORIZATION_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| UX_R3_I1_COLLECTION_DATA_QUALITY_IMPLEMENTATION_STATUS | **COMPLETE** / **MERGED** (PR #130 → `a611616`) |
| UX_R3_I1_IMPLEMENTATION_STATUS | **COMPLETE** |
| UX_R3_I1_FINAL_REVIEW_STATUS | **APPROVED** |
| UX_R3_I1_IMPLEMENTATION_REVIEW_DECISION | **APPROVED** |
| UX_R3_I1_ROUTE | **/future-collection/collected-data** |
| UX_R3_I1_NAV_LABEL | **Dados Coletados** |
| UX_R3_I1_NAV_STATUS | **ACTIVE** |
| UX_R3_I1_IMPLEMENTATION_POSTURE | **A_STATIC_FIXTURE_BACKED_COLLECTION_DATA_QUALITY** |
| UX_R3_I1_AUTHORIZED_ROUTE | **/future-collection/collected-data** |
| UX_R3_I1_AUTHORIZED_NAV_LABEL | **Dados Coletados** |
| UX_R3_I1_AUTHORIZED_IMPLEMENTATION_POSTURE | **A_STATIC_FIXTURE_BACKED_COLLECTION_DATA_QUALITY** |
| UX_R3_I1_AUTHORIZED_FIXTURE_ID | **collection_data_quality_current_state_illustrative** |
| UX_R3_I1_AUTHORIZED_VIEWMODEL_NAME | **CollectionDataQualityViewModel** |
| UX_R3_I2_STATUS | **MERGED** (PR #134 → `3ad9336`) |
| UX_R3_I3_STATUS | **MERGED** (PR #134 → `3ad9336`) |
| UX_R3_I4_STATUS | **NOT_STARTED** (out of remaining scope) |
| UX_R3_I5_STATUS | **NOT_STARTED** (out of remaining scope) |
| UX_R3_REMAINING_RELEASE_SINGLE_EXECUTION_STATUS | **MERGED** (PR #134 → `3ad9336`) |
| UX_R3_REMAINING_RELEASE_FINAL_REVIEW_STATUS | **APPROVED** |
| UX_R3_HUMAN_FINAL_VALIDATION_RESULT | **APPROVED** |
| UX_R3_RELEASE_STATUS | **CLOSED** |
| UX_R3_RELEASE_ACCEPTANCE_STATUS | **ACCEPTED** |
| UX_R3_RELEASE_SCOPE | **FIXTURE_BACKED_COLLECTION_MONITORING_DATA_QUALITY_AND_COHERENCE** |
| UX_R3_ACCEPTANCE_WORDING | **UX-R3 fixture-backed collection monitoring, data-quality exploration, and workflow coherence scope is complete, accepted, and governed.** |
| UX_R4_STATUS | **NOT_STARTED** |
| UX_R4_DISCOVERY_STATUS | **MERGED** (PR #136 → `0184750`) |
| UX_R4_DISCOVERY_AND_SCOPE_STATUS | **MERGED** (PR #136 → `0184750`) |
| UX_R4_DISCOVERY_DECISION | **SCOPE_RECOMMENDED** |
| UX_R4_RECOMMENDATION | **MULTIPLE_BOUNDED_INCREMENTS** |
| UX_R4_DIRECTION | **F_GOVERNED_DECISION_LEDGER_REFRESH** |
| UX_R4_RECOMMENDED_DIRECTION | **F_GOVERNED_DECISION_LEDGER_REFRESH** |
| UX_R4_PROPOSED_INCREMENT_COUNT | **3** |
| UX_R4_DELIVERY_MODEL | **A_FULL_INCREMENTAL_FLOW** |
| UX_R4_DISCOVERY_AUTHORIZED | **true** (consumed by PR #136 merge) |
| UX_R4_SCOPE_AUTHORIZED | **false** |
| UX_R4_IMPLEMENTATION_AUTHORIZED | **false** |
| UX_R4_I1_STATUS | **AUTHORIZATION_ASSESSMENT_COMPLETE_UNMERGED** |
| UX_R4_I1_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| UX_R4_I1_DECISION_LEDGER_AUTHORIZATION_ASSESSMENT_STATUS | **COMPLETE_UNMERGED** |
| UX_R4_I1_AUTHORIZATION_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| UX_R4_I1_AUTHORIZED_ROUTE | **/governance/evidence** |
| UX_R4_I1_AUTHORIZED_NAV_ITEM | **Evidências** |
| UX_R4_I1_AUTHORIZED_POSTURE | **STATIC_FIXTURE_BACKED_READ_ONLY** |
| UX_R4_I1_AUTHORIZED_INTEGRATION_MODE | **B_NEW_SECTION_ABOVE_CATALOG** |
| UX_R4_I1_AUTHORIZED_FIXTURE_NAME | **governed_decision_ledger_current_state_illustrative** |
| UX_R4_I1_AUTHORIZED_FIXTURE_VERSION | **1** |
| UX_R4_I1_AUTHORIZED_VIEWMODEL_NAME | **GovernedDecisionLedgerViewModel** |
| UX_R4_I1_IMPLEMENTATION_AUTHORIZED | **false** |
| UX_R4_I2_STATUS | **NOT_STARTED** |
| UX_R4_I2_IMPLEMENTATION_AUTHORIZED | **false** |
| UX_R4_I3_STATUS | **NOT_STARTED** |
| UX_R4_I3_IMPLEMENTATION_AUTHORIZED | **false** |
| UX_R3_COMPLETE_RELEASE_ASSESSMENT_STATUS | **MERGED** (PR #132 → `4d00d9b`) |
| UX_R3_COMPLETE_RELEASE_IMPACT_ASSESSMENT_STATUS | **MERGED** (PR #132 → `4d00d9b`) |
| UX_R3_COMPLETE_RELEASE_DECISION | **REMAINING_SCOPE_RECOMMENDED** |
| UX_R3_RELEASE_DECISION | **REMAINING_SCOPE_RECOMMENDED** |
| UX_R3_COMPLETE_RELEASE_DELIVERY_MODEL | **B_SINGLE_BRANCH_SINGLE_PR_SINGLE_FINAL_VALIDATION** |
| UX_R3_DELIVERY_MODEL | **B_SINGLE_BRANCH_SINGLE_PR_SINGLE_FINAL_VALIDATION** |
| UX_R3_SHOULD_CLOSE_AFTER_I1 | **false** |
| UX_R3_REMAINING_SCOPE | **ONE_INCREMENT_PLUS_DOCS_CLOSURE** |
| UX_R3_REMAINING_INCREMENT_COUNT | **2** |
| UX_R3_REMAINING_INCREMENT_IDS | **UX_R3_I2_COLLECTION_QUALITY_CROSS_NAV_AND_COHERENCE; UX_R3_I3_FIXTURE_ACCEPTANCE_AND_CLOSURE** |
| UX_R3_REMAINING_SCOPE_AUTHORIZED | **true** (consumed by PR #134 merge) |
| UX_R3_REMAINING_IMPLEMENTATION_AUTHORIZED | **true** (consumed by PR #134 merge) |
| UX_R3_IMPLEMENTATION_POSTURE | **FIXTURE_BACKED_READ_ONLY** |
| UX_R3_PROCESS_MODEL | **FULL_INCREMENTAL_FLOW** |
| UX_R3_SCOPE_AUTHORIZED | **false** |
| UX_R3_IMPLEMENTATION_AUTHORIZED | **false** (I1+I2+I3 consumed; no further UX-R3 product authorized) |
| UX_R3_I1_IMPLEMENTATION_AUTHORIZED | **true** (consumed by PR #130 merge) |
| UX_R3_I2_IMPLEMENTATION_AUTHORIZED | **true** (consumed by PR #134 merge) |
| UX_R3_I3_CLOSURE_PREPARATION_AUTHORIZED | **true** (consumed by PR #134 merge) |
| UX_R3_START_AUTHORIZED | **false** (UX-R3 CLOSED/ACCEPTED) |
| UX_R2_REMAINING_RELEASE_FROZEN_SCOPE_STATUS | **FROZEN** |
| UX_R2_REMAINING_RELEASE_DECISION | **AUTHORIZED_FOR_SINGLE_EXECUTION_WITH_CONDITIONS** |
| UX_R2_REMAINING_INCREMENT_LIST | **I2 catalog history; I3 provenance UX; I4 cross-navigation; I5 fixture closure** |
| UX_R2_REMAINING_IMPLEMENTATION_AUTHORIZED | **true** (I2–I5 single execution MERGED; no further remaining-release product authorized) |
| UX_R2_SINGLE_BRANCH_EXECUTION_AUTHORIZED | **true** (consumed by PR #120 merge) |
| UX_R2_SINGLE_PR_EXECUTION_AUTHORIZED | **true** (consumed by PR #120 merge) |
| UX_R2_SINGLE_FINAL_VALIDATION_AUTHORIZED | **true** (consumed by PR #120 merge) |
| UX_R2_IMPLEMENTATION_AUTHORIZED | **true** (I1 + I2–I5 Evidence Explorer remaining release MERGED) |
| UX_R2_PRODUCT_CODE_AUTHORIZED | **false** (I1 + I2–I5 MERGED; no further UX-R2 product code; stamp task docs-only) |
| UX_R2_I1_IMPLEMENTATION_AUTHORIZED | **true** |
| EVIDENCE_EXPLORER_IMPLEMENTATION_AUTHORIZED | **true** |
| EVIDENCE_EXPLORER_MERGE_AUTHORIZED | **true** (consumed by PR #116 merge) |
| REPOSITORY_FILE_READ_INTEGRATION_AUTHORIZED | **false** |
| RUNTIME_REPOSITORY_ACCESS_AUTHORIZED | **false** |
| RAW_FILESYSTEM_ACCESS_AUTHORIZED | **false** |
| UX_B1_STATUS / UX-B1_STATUS | **MERGED** (`UX-RELEASE-FOUNDATION-001`; PR #31 → `5101c65`) |
| UX-B2_IMPACT_STATUS | **MERGED** (`DESIGN-SYSTEM-FOUNDATION-001`; PR #35 → `5bcb088`) |
| UX_B2_AUTHORIZATION_STATUS | **MERGED** (PR #43 → `34ce0e7`) |
| UX_B2_AUTHORIZATION_DECISION | **AUTHORIZED_FOR_INCREMENT_I1_ONLY** |
| UX_B2_STATUS | **I1_MERGED** |
| UX_B2_AUTHORIZED_INCREMENT | **I1** |
| I1_IMPLEMENTATION_STATUS | **MERGED** (PR #51 → `c283592`) |
| I2_STATUS | **IMPLEMENTATION_MERGED** (PR #69 → `762b303`; assessment PR #55 → `ca24cc4`) |
| I2_AUTHORIZATION_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| I2_IMPLEMENTATION_AUTHORIZED | **true** (I2 tokens/themes merged; no further I2 work authorized) |
| I2_IMPLEMENTATION_STATUS | **MERGED** |
| I5A_STATUS | **ARCHITECTURE_MERGED** (PR #56 → `134c93a`) |
| I5_ARCHITECTURE_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| I5_STATUS | **IMPLEMENTATION_MERGED** (PR #77 → `855d184`) |
| I5_IMPLEMENTATION_AUTHORIZED | **true** (I5 shell/nav merged; no further I5 work authorized) |
| I5_IMPLEMENTATION_STATUS | **MERGED** |
| I5_MERGE_AUTHORIZED | **true** (consumed by PR #77 merge) |
| ROUTER_INSTALLATION_AUTHORIZED | **true** (react-router-dom installed for I5; no data routers/loaders) |
| I6A_STATUS | **DATA_PREPARATION_MERGED** (PR #57 → `4bf15db`) |
| I6B_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| I6B_STATUS | **IMPLEMENTATION_MERGED** (PR #81 → `b38bcce`) |
| I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED | **true** (I6B ViewModel merged; no further I6B work authorized) |
| I6_VIEWMODEL_IMPLEMENTATION_STATUS | **MERGED** |
| I6_VIEWMODEL_MERGE_AUTHORIZED | **true** (consumed by PR #81 merge) |
| I6C_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| I6C_STATUS | **IMPLEMENTATION_MERGED** (PR #84 → `c44ec3f`) |
| I6_FIXTURE_IMPLEMENTATION_AUTHORIZED | **true** (I6C fixtures merged; no further I6C work authorized) |
| I6_FIXTURE_IMPLEMENTATION_STATUS | **MERGED** |
| I6_FIXTURE_MERGE_AUTHORIZED | **true** (consumed by PR #84 merge) |
| I6_SCREEN_IMPLEMENTATION_AUTHORIZED | **true** (I6E Overview screen merged only; other screens false) |
| VIEWMODEL_IMPLEMENTATION_AUTHORIZED | **true** (I6B ViewModel merged) |
| TYPESCRIPT_FIXTURE_IMPLEMENTATION_AUTHORIZED | **true** (I6C fixtures merged) |
| OPERATIONAL_DATA_INTEGRATION_AUTHORIZED | **false** |
| OPERATIONAL_ACTIONS_AUTHORIZED | **false** |
| PARALLEL_KICKOFF_STATUS | **COMPLETE** (PRs #58–#61) |
| I2_I5_I6_IMPL_AUTH_ASSESSMENT_STATUS | **MERGED** (PR #66 → `5098e83`) |
| I2_I5_I6_IMPL_AUTH_NEXT | **UX_R4_I2_EVIDENCE_DECISION_LEDGER_FIXTURE_REFRESH** (I1 AUTHORIZED_WITH_CONDITIONS; I2 implementation unauthorized) |
| I3_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| I3_STATUS | **IMPLEMENTATION_MERGED** (PR #72 → `897353e`) |
| I3_IMPLEMENTATION_AUTHORIZED | **true** (I3 primitives merged; no further I3 work authorized) |
| I3_IMPLEMENTATION_STATUS | **MERGED** |
| I3_MERGE_AUTHORIZED | **true** (consumed by PR #72 merge) |
| I3_PREREQUISITE_DECISION | **SATISFIED_FOR_I5_AND_I6C** |
| I5_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| I6D_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| I6D_STATUS | **ASSESSMENT_MERGED** (PR #87 → `4aa3861`) |
| I6D_SCREEN_AUTHORIZATION_ASSESSMENT_STATUS | **MERGED** |
| I6D_RECOMMENDED_SCREEN_SEQUENCE | **OVERVIEW_FIRST** |
| I6D_FIRST_AUTHORIZED_SCREEN | **Visão Geral** |
| I6D_SCREEN_SCOPE_RECOMMENDATION | **OVERVIEW_FIRST** |
| I6E_DECISION | **HUMAN_AUTHORIZED_FOR_THIS_TASK** |
| I6E_STATUS | **IMPLEMENTATION_MERGED** (PR #90 → `93b9220`) |
| I6_OVERVIEW_SCREEN_IMPLEMENTATION_AUTHORIZED | **true** |
| I6_OVERVIEW_SCREEN_IMPLEMENTATION_STATUS | **MERGED** |
| I6_OVERVIEW_SCREEN_MERGE_AUTHORIZED | **true** (consumed by PR #90 merge) |
| I6F_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| I6F_STATUS | **ASSESSMENT_MERGED** (PR #92 → `f0e9c29`) |
| I6F_RUNS_SCREEN_AUTHORIZATION_ASSESSMENT_STATUS | **MERGED** |
| I6F_RECOMMENDED_IMPLEMENTATION_BOUNDARY | **RUNS_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; NO_VISIBLE_FIXTURE_SELECTOR; NO_REAL_DATA; NO_OPERATIONAL_ACTIONS** |
| I6G_DECISION | **HUMAN_AUTHORIZED_FOR_THIS_TASK** |
| I6G_STATUS | **IMPLEMENTATION_MERGED** (PR #94 → `37092be`) |
| RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED | **true** (I6G Runs screen merged; no further Runs work authorized) |
| I6_RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED | **true** |
| I6_RUNS_SCREEN_IMPLEMENTATION_STATUS | **MERGED** |
| I6_RUNS_SCREEN_MERGE_AUTHORIZED | **true** (consumed by PR #94 merge) |
| I6H_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| I6H_STATUS | **ASSESSMENT_MERGED** (PR #96 → `2a90787`) |
| I6H_READINESS_SCREEN_AUTHORIZATION_ASSESSMENT_STATUS | **MERGED** |
| I6H_RECOMMENDED_IMPLEMENTATION_BOUNDARY | **READINESS_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; NO_VISIBLE_FIXTURE_SELECTOR; NO_REAL_DATA; NO_VALIDATION_EXECUTION; NO_COLLECTION_ACTIONS; NO_SCHEDULER_ACTIONS; NO_SCIENTIFIC_INTERPRETATION_CHANGE** |
| I6I_DECISION | **HUMAN_AUTHORIZED_FOR_THIS_TASK** |
| I6I_STATUS | **IMPLEMENTATION_MERGED** (PR #98 → `061c388`) |
| READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED | **true** (I6I Readiness screen merged; no further Readiness work authorized) |
| I6_READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED | **true** |
| I6_READINESS_SCREEN_IMPLEMENTATION_STATUS | **MERGED** |
| READINESS_SCREEN_MERGE_AUTHORIZED | **true** (consumed by PR #98 merge) |
| HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED | **true** (I6K Host screen merged; no further Host work authorized) |
| I6J_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| I6J_STATUS | **ASSESSMENT_MERGED** (PR #100 → `b284a72`) |
| I6J_HOST_SCHEDULER_SCREEN_AUTHORIZATION_ASSESSMENT_STATUS | **MERGED** |
| I6J_RECOMMENDED_IMPLEMENTATION_BOUNDARY | **HOST_SCHEDULER_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; NO_VISIBLE_FIXTURE_SELECTOR; NO_REAL_HOST_DISCOVERY; NO_REAL_DATA; NO_CREDENTIALS; NO_SCHEDULER_ACTIVATION; NO_COLLECTION_ACTIONS; NO_RUN_NOW; NO_OPERATIONAL_COMMANDS; NO_SCIENTIFIC_STATE_CHANGE** |
| I6K_DECISION | **HUMAN_AUTHORIZED_FOR_THIS_TASK** |
| I6K_STATUS | **IMPLEMENTATION_MERGED** (PR #102 → `b71ed83`) |
| I6_HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED | **true** |
| I6_HOST_SCHEDULER_SCREEN_IMPLEMENTATION_STATUS | **MERGED** |
| HOST_SCHEDULER_SCREEN_MERGE_AUTHORIZED | **true** (consumed by PR #102 merge) |
| R3E_EXPERIMENT_SCREEN_IMPLEMENTATION_AUTHORIZED | **true** (I6M R3E screen merged; no further R3E screen work authorized) |
| I6L_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| I6L_STATUS | **ASSESSMENT_MERGED** (PR #104 → `458b47b`) |
| I6L_R3E_EXPERIMENT_SCREEN_AUTHORIZATION_ASSESSMENT_STATUS | **MERGED** |
| I6L_RECOMMENDED_IMPLEMENTATION_BOUNDARY | **R3E_EXPERIMENT_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; EXPLANATORY_ONLY; NO_VISIBLE_FIXTURE_SELECTOR; NO_REAL_DATA; NO_FUTURE_UNSEEN_RESULTS; NO_VALIDATION_EXECUTION; NO_EFFECT_PEEKING; NO_TRADING_RECOMMENDATIONS; NO_PROFITABILITY_CLAIMS; NO_SCIENTIFIC_INTERPRETATION_CHANGE; NO_R4_OR_R5_STATE_CHANGE** |
| I6L_RECOMMENDED_ROUTE | **/experiments/r3e** |
| I6L_RECOMMENDED_NAV_LABEL | **Experimento R3E** |
| I6L_DEDICATED_R3E_VIEWMODEL_REQUIRED | **true** |
| I6L_DEDICATED_SYNTHETIC_FIXTURE_REQUIRED | **true** |
| I6M_DECISION | **HUMAN_AUTHORIZED_FOR_THIS_TASK** |
| I6M_STATUS | **IMPLEMENTATION_MERGED** (PR #106 → `764e85f`) |
| I6_R3E_EXPERIMENT_SCREEN_IMPLEMENTATION_AUTHORIZED | **true** |
| I6_R3E_EXPERIMENT_SCREEN_IMPLEMENTATION_STATUS | **MERGED** |
| R3E_EXPERIMENT_SCREEN_MERGE_AUTHORIZED | **true** (consumed by PR #106 merge) |
| IMPLEMENTATION_EXECUTION_AUTHORIZED | **false** (no open authorized implementation task) |
| NEW_IMPLEMENTATION_AUTHORIZED | **false** |
| REAL_DATA_INTEGRATION_AUTHORIZED | **false** |
| REAL_HOST_DISCOVERY_AUTHORIZED | **false** |
| SCHEDULER_ACTIVATION_AUTHORIZED | **false** |
| VALIDATION_EXECUTION_AUTHORIZED | **false** |
| EFFECT_PEEKING_AUTHORIZED | **false** |
| FUTURE_UNSEEN_RESULTS_ACCESS_AUTHORIZED | **false** |
| SCIENTIFIC_INTERPRETATION_CHANGE_AUTHORIZED | **false** |
| R4_STATE_CHANGE_AUTHORIZED | **false** |
| R5_STATE_CHANGE_AUTHORIZED | **false** |
| NEXT_RECOMMENDED_TASK | **UX_R4_I2_EVIDENCE_DECISION_LEDGER_FIXTURE_REFRESH** |
| NEXT_ITEM | **UX_R4_I2_IMPLEMENTATION_SEPARATE_PROMPT_NOT_AUTHORIZED** |
| PARALLEL_TASKS_ALLOWED | **false** |
| UX_B2_IMPLEMENTATION_AUTHORIZED | **false** (beyond authorized increments) |
| UX_B3_STATUS / UX-B3_STATUS | **MERGED** (`OPERATIONAL-MVP-SCREEN-CONTRACTS-001`; PR #44 → `253bd82`) |
| UX_B3_IMPLEMENTATION_AUTHORIZED | **false** |
| UX_B4_STATUS / UX-B4_STATUS | **MERGED** (`OPERATIONAL-LANGUAGE-MICROCOPY-001`; PR #42 → `92e8320`) |
| UX_B4_IMPLEMENTATION_AUTHORIZED | **false** |
| RELEASE_OWNER | Gustavo Almeida |
| UX_FOUNDATION_MERGE_AUTHORIZED | **true** (fundação documental mergeada; UI não autorizada) |
| UI_IMPLEMENTATION_AUTHORIZED | **true** (I6E Overview + I6G Runs + I6I Readiness + I6K Host + I6M R3E + UX-R2 I1 Evidence Explorer merged) |
| UI_SCREEN_IMPLEMENTATION_AUTHORIZED | **true** (I6E Overview + I6G Runs + I6I Readiness + I6K Host + I6M R3E + UX-R2 I1 Evidence Explorer merged) |
| HOST_DISCOVERY | **DEFERRED** |
| OPERATIONAL_DEBT | **OPEN** |
| SCHEDULER_ACTIVATION | **BLOCKED** |
| R3E_SCIENTIFIC_STATE | **UNCHANGED** |
| Spec | `docs/releases/UX-R1_SPEC.md` |
| Backlog UX | `docs/ux/UX-R1_BACKLOG.md` |
| Fundação | `docs/ux/` · `docs/ai-specs/UX-R1-EXPERIENCE-FOUNDATION_SPEC.md` |
| Linguagem operacional B4 | `docs/ux/UX-R1-OPERATIONAL-LANGUAGE-GUIDE.md` (+ catálogos status/empty/failure/guardrails) |
| Contratos MVP B3 | `docs/ai-specs/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS_SPEC.md` |
| Impacto B1 | `docs/ai-impact/UX-RELEASE-FOUNDATION-001_IMPACT_ASSESSMENT.md` (`APPROVED`) |
| Impacto B2 | `docs/ai-impact/UX-R1-DESIGN-SYSTEM-FOUNDATION-001_IMPACT_ASSESSMENT.md` (`APPROVED`; implementação não autorizada) |
| Autorização B2 | `docs/ai-impact/UX-R1-DESIGN-SYSTEM-IMPLEMENTATION-AUTHORIZATION_IMPACT_ASSESSMENT.md` (`AUTHORIZED_FOR_INCREMENT_I1_ONLY`; **MERGED** PR #43) |
| Impacto B3 | `docs/ai-impact/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS-001_IMPACT_ASSESSMENT.md` (`APPROVED`; **MERGED** PR #44) |
| Impacto B4 | `docs/ai-impact/UX-R1-OPERATIONAL-LANGUAGE-MICROCOPY-001_IMPACT_ASSESSMENT.md` (`APPROVED`; **MERGED** PR #42) |
| PR fundação | https://github.com/multivacia/wick/pull/31 (**MERGED**) |
| PR design system (impacto) | https://github.com/multivacia/wick/pull/35 (**MERGED** `5bcb088`) |
| PR autorização I1 | https://github.com/multivacia/wick/pull/43 (**MERGED** `34ce0e7`) |
| PR linguagem B4 | https://github.com/multivacia/wick/pull/42 (**MERGED** `92e8320`) |
| PR contratos MVP B3 | https://github.com/multivacia/wick/pull/44 (**MERGED** `253bd82`) |
| PR I1 scaffold + CI | https://github.com/multivacia/wick/pull/51 (**MERGED** `c283592`) |
| PR kickoff paralelo I2/I5A/I6A | https://github.com/multivacia/wick/pull/58 (**MERGED** `d2a52cc`) |
| PR I2 design tokens assessment | https://github.com/multivacia/wick/pull/55 (**MERGED** `ca24cc4`) |
| PR I5A shell/nav architecture | https://github.com/multivacia/wick/pull/56 (**MERGED** `134c93a`) |
| PR I6A Overview data/fixtures | https://github.com/multivacia/wick/pull/57 (**MERGED** `4bf15db`) |
| Autorização I2/I3/I5/I6 | https://github.com/multivacia/wick/pull/66 (**MERGED** `5098e83`) |
| I2 tokens/themes implementation | https://github.com/multivacia/wick/pull/69 (**MERGED** `762b303`) |
| I3 minimum accessible primitives | https://github.com/multivacia/wick/pull/72 (**MERGED** `897353e`) |
| I5 application shell and navigation | https://github.com/multivacia/wick/pull/77 (**MERGED** `855d184`) |
| I6B ViewModel implementation | https://github.com/multivacia/wick/pull/81 (**MERGED** `b38bcce`) |
| I6C executable fixtures | https://github.com/multivacia/wick/pull/84 (**MERGED** `c44ec3f`) |
| I6D screen authorization assessment | https://github.com/multivacia/wick/pull/87 (**MERGED** `4aa3861`) |
| I6E Overview screen implementation | https://github.com/multivacia/wick/pull/90 (**MERGED** `93b9220`) |
| I6F Runs screen authorization assessment | https://github.com/multivacia/wick/pull/92 (**MERGED** `f0e9c29`) |
| I6G Runs screen implementation | https://github.com/multivacia/wick/pull/94 (**MERGED** `37092be`) |
| I6H Readiness screen authorization assessment | https://github.com/multivacia/wick/pull/96 (**MERGED** `2a90787`) |
| I6I Readiness screen implementation | https://github.com/multivacia/wick/pull/98 (**MERGED** `061c388`) |
| I6J Host/Scheduler screen authorization assessment | https://github.com/multivacia/wick/pull/100 (**MERGED** `b284a72`) |
| I6K Host/Scheduler screen implementation | https://github.com/multivacia/wick/pull/102 (**MERGED** `b71ed83`) |
| I6L R3E experiment screen authorization assessment | https://github.com/multivacia/wick/pull/104 (**MERGED** `458b47b`) |
| I6M R3E experiment screen implementation | https://github.com/multivacia/wick/pull/106 (**MERGED** `764e85f`) |
| UX-R1 final closure and acceptance assessment | https://github.com/multivacia/wick/pull/108 (**MERGED** `708f11a`) |
| UX-R1 formal release closure and acceptance stamp | https://github.com/multivacia/wick/pull/110 (**MERGED** `df5fe40`) |
| UX-R2 discovery and scope assessment | https://github.com/multivacia/wick/pull/112 (**MERGED** `9f25b19`) |
| UX-R2 I1 Evidence Explorer authorization assessment | https://github.com/multivacia/wick/pull/114 (**MERGED** `3be8920`) |
| UX-R2 I1 Evidence Explorer implementation | https://github.com/multivacia/wick/pull/116 (**MERGED** `d820f05`) |
| UX-R2 remaining-release integral plan | https://github.com/multivacia/wick/pull/118 (**MERGED** `47c31e2`) |
| UX-R2 I2–I5 single-execution implementation | https://github.com/multivacia/wick/pull/120 (**MERGED** `2112e6a`) |
| UX-R2 final closure and acceptance assessment | https://github.com/multivacia/wick/pull/122 (**MERGED** `dda0667`) |
| UX-R2 assessment FINAL-MERGE handoff | https://github.com/multivacia/wick/pull/123 (**MERGED** `13337f9`) |
| UX-R2 formal release closure and acceptance stamp | https://github.com/multivacia/wick/pull/124 (**MERGED** `2fe9715`) |
| UX-R3 discovery and scope assessment | https://github.com/multivacia/wick/pull/126 (**MERGED** `e23bfe9`) |
| UX-R3 I1 Collection Data Quality authorization assessment | https://github.com/multivacia/wick/pull/128 (**MERGED** `95fd5b8`) |
| UX-R3 I1 Collection Data Quality implementation | https://github.com/multivacia/wick/pull/130 (**MERGED** `a611616`) |
| UX-R3 complete-release impact assessment | https://github.com/multivacia/wick/pull/132 (**MERGED** `4d00d9b`) |
| UX-R3 complete-release assessment FINAL-MERGE handoff | https://github.com/multivacia/wick/pull/133 (**OPEN**) |
| UX-R3 remaining-release single execution (I2+I3) | https://github.com/multivacia/wick/pull/134 (**MERGED** `3ad9336`) |
| UX-R3 remaining-release FINAL-MERGE + formal stamp | https://github.com/multivacia/wick/pull/135 (**OPEN**) |
| UX-R4 discovery and scope assessment | https://github.com/multivacia/wick/pull/136 (**MERGED** `0184750`) |
| UX-R4 discovery FINAL-MERGE handoff | https://github.com/multivacia/wick/pull/137 (**OPEN**) |
| UX-R4 I1 Decision Ledger authorization assessment | PENDING_DRAFT_PR |

MVP funcional previsto (após autorização de UI): Visão Geral, Execuções da Coleta, Prontidão, Host e Automação, Experimento R3E (explicativo). Contratos de tela (UX-B3) e linguagem operacional (UX-B4) estão **MERGED**. UX-B2 I1 **MERGED**; I2 tokens/temas **MERGED** (PR #69); I3 primitivos **MERGED** (PR #72); I5 shell/nav **MERGED** (PR #77); I6B ViewModel **MERGED** (PR #81); I6C fixtures **MERGED** (PR #84). I6D assessment **MERGED** (PR #87): **AUTHORIZED_WITH_CONDITIONS** / **OVERVIEW_FIRST**. I6E Overview screen **MERGED** (PR #90; fixture-backed `/overview`; `I6_OVERVIEW_SCREEN_IMPLEMENTATION_STATUS=MERGED`). I6F Runs authorization assessment **MERGED** (PR #92). I6G Runs screen **MERGED** (PR #94; fixture-backed `/future-collection/runs`; `I6_RUNS_SCREEN_IMPLEMENTATION_STATUS=MERGED`). I6H Readiness authorization assessment **MERGED** (PR #96 → `2a90787`): **AUTHORIZED_WITH_CONDITIONS**. I6I Readiness screen **MERGED** (PR #98 → `061c388`; fixture-backed `/future-collection/readiness`; `I6_READINESS_SCREEN_IMPLEMENTATION_STATUS=MERGED`). I6J Host/Scheduler authorization assessment **MERGED** (PR #100 → `b284a72`): **AUTHORIZED_WITH_CONDITIONS**. I6K Host e Automação screen **MERGED** (PR #102 → `b71ed83`; fixture-backed `/operations/host-scheduler`; `I6_HOST_SCHEDULER_SCREEN_IMPLEMENTATION_STATUS=MERGED`). I6L R3E experiment screen authorization assessment **MERGED** (PR #104 → `458b47b`): **AUTHORIZED_WITH_CONDITIONS**. I6M R3E experiment screen **MERGED** (PR #106 → `764e85f`; fixture-backed `/experiments/r3e`; dedicated ViewModel+fixture; `I6_R3E_EXPERIMENT_SCREEN_IMPLEMENTATION_STATUS=MERGED`; `R3E_GATE=PENDING_FUTURE_UNSEEN_DATA`; `PARALLEL_TASKS_ALLOWED=false`). UX-R1 final closure assessment **MERGED** (PR #108 → `708f11a`; decision **ACCEPTED_FOR_CLOSURE**). UX-R1 formal release stamp **CLOSED / ACCEPTED** (**MERGED** PR #110 → `df5fe40`; `UX_R1_RELEASE_SCOPE=FIXTURE_BACKED_READ_ONLY`; acceptance wording: *UX-R1 fixture-backed read-only scope is complete and governed.*). UX-R2 discovery assessment **MERGED** (PR #112 → `9f25b19`; **SCOPE_RECOMMENDED**; **D_EVIDENCE_AND_AUDIT_EXPLORER**). UX-R2 I1 Evidence Explorer authorization assessment **MERGED** (PR #114 → `3be8920`; **AUTHORIZED_WITH_CONDITIONS**). UX-R2 I1 Evidence Explorer implementation **MERGED** (PR #116 → `d820f05`; fixture-backed `/governance/evidence`; fixture `evidence_catalog_current_state_illustrative`; review **APPROVED**; `UX_R2_I1_EVIDENCE_EXPLORER_IMPLEMENTATION_STATUS=MERGED`). UX-R2 remaining-release integral plan **MERGED** (PR #118 → `47c31e2`). UX-R2 I2–I5 single execution **MERGED** (PR #120 → `2112e6a`; I2 catalog history + I3 provenance UX + I4 cross-nav + I5 fixture closure; final review **APPROVED**). UX-R2 final closure assessment **MERGED** (PR #122 → `dda0667`; decision **CLOSURE_AND_ACCEPTANCE_RECOMMENDED**). UX-R2 formal release stamp **CLOSED / ACCEPTED** (**MERGED** PR #124 → `2fe9715`; `UX_R2_RELEASE_SCOPE=FIXTURE_BACKED_EVIDENCE_AND_AUDIT_EXPLORATION`; acceptance wording: *UX-R2 fixture-backed evidence and audit exploration scope is complete, accepted, and governed.*; UX-R3 **NOT_STARTED**). UX-R3 discovery assessment **MERGED** (PR #126 → `e23bfe9`; **SCOPE_RECOMMENDED**; direction **E_COLLECTION_MONITORING_AND_DATA_QUALITY**). UX-R3 I1 Collection Data Quality authorization assessment **MERGED** (PR #128 → `95fd5b8`; **AUTHORIZED_WITH_CONDITIONS**). UX-R3 I1 Collection Data Quality implementation **MERGED** (PR #130 → `a611616`; final review **APPROVED**; route **/future-collection/collected-data**; nav **Dados Coletados** **ACTIVE**; posture **A_STATIC_FIXTURE_BACKED_COLLECTION_DATA_QUALITY**; fixture `collection_data_quality_current_state_illustrative`; ViewModel `CollectionDataQualityViewModel`; UX-R3 **IN_PROGRESS**). UX-R3 complete-release impact assessment **MERGED** (PR #132 → `4d00d9b`; decision **REMAINING_SCOPE_RECOMMENDED**; delivery model **B_SINGLE_BRANCH_SINGLE_PR_SINGLE_FINAL_VALIDATION**; remaining increments **UX_R3_I2_COLLECTION_QUALITY_CROSS_NAV_AND_COHERENCE** + **UX_R3_I3_FIXTURE_ACCEPTANCE_AND_CLOSURE**; remaining scope/implementation **unauthorized**; `NEXT_RECOMMENDED_TASK=UX_R3_REMAINING_RELEASE_SINGLE_EXECUTION`). UX-R3 remaining-release single execution **MERGED** (PR #134 → `3ad9336`; human final validation **APPROVED**; I2 cross-nav + I3 closure). UX-R3 formal release stamp **CLOSED / ACCEPTED** (`UX_R3_RELEASE_SCOPE=FIXTURE_BACKED_COLLECTION_MONITORING_DATA_QUALITY_AND_COHERENCE`; acceptance wording: *UX-R3 fixture-backed collection monitoring, data-quality exploration, and workflow coherence scope is complete, accepted, and governed.*; UX-R4 **NOT_STARTED**; `NEXT_RECOMMENDED_TASK=UX_R4_DISCOVERY_AND_SCOPE_ASSESSMENT`). UX-R4 discovery assessment **MERGED** (PR #136 → `0184750`; decision **SCOPE_RECOMMENDED**; direction **F_GOVERNED_DECISION_LEDGER_REFRESH**; delivery **A_FULL_INCREMENTAL_FLOW**; 3 proposed increments; UX-R4 **NOT_STARTED**; implementation **false**; `NEXT_RECOMMENDED_TASK=UX_R4_I1_DECISION_LEDGER_AUTHORIZATION_ASSESSMENT`).

## Estado oficial (pós-R3D / R3E engine)

| Campo | Valor |
|-------|--------|
| R1_GATE | APPROVED |
| R2_GATE | APPROVED |
| R3A_GATE | APPROVED |
| R3_IMPLEMENTATION | COMPLETE |
| R3_AUDIT | COMPLETE |
| R3D_IMPLEMENTATION | COMPLETE |
| R3D_AUDIT | COMPLETE |
| R3_GATE | **REJECTED_NO_MEASURABLE_EDGE_V1** |
| R3E_CODE_GATE | **APPROVED** |
| R3E_IMPLEMENTATION | COMPLETE |
| R3E_AUDIT | COMPLETE |
| R3E_DEVELOPMENT_RUN | **REAL_OHLCV_EXPLORATORY** (sintético prévio: `SYNTHETIC_ONLY`) |
| R3E_REAL_DATA_RUN | **COMPLETE** |
| R3E_REAL_DATA_AUDIT | **COMPLETE** |
| ECONOMIC_INTERPRETATION_ALLOWED | **false** |
| R3E_GATE | **PENDING_FUTURE_UNSEEN_DATA** |
| R3E_FUTURE_VALIDATION_ENGINE | **COMPLETE** |
| R3E_FUTURE_VALIDATION_AUDIT | **COMPLETE** |
| R3E_FUTURE_DATA_COLLECTION | **IN_PROGRESS** |
| R3E_READINESS_GATE | **IMPLEMENTED** (B2 / R3E-READINESS-001; status operacional separado do gate científico) |
| R3E_COLLECTION_AUTOMATION | **IMPLEMENTED** (B4 / COLLECTION-AUTOMATION-001; PR #19 MERGED `f773702`; validate não autorizado) |
| R3E_COLLECTION_SCHEDULER | **AWAITING_OPERATOR_DISCOVERY** (B5-D1; PR #28 MERGED `83308f5`; Gustavo deve rodar discovery no host real; timer não ativado) |
| FUTURE_UNSEEN_CUTOFF | `2026-07-18T01:30:00+00:00` |
| R3E_OPERATIONAL_BACKFILL_RUN | **COMPLETE** (histórico; não científico) |
| R3E_OPERATIONAL_BACKFILL_AUDIT | **COMPLETE** |
| R3E_OPERATIONAL_BACKFILL_SCIENTIFIC_ELIGIBILITY | **false** |
| R4_STATUS | **BLOCKED** |
| R5_STATUS | NOT_STARTED |
| experiment_id (R3D) | `r3d-real-validation-v1` |
| experiment_id (R3E) | `r3e-contextual-edge-v1` |
| experiment_id (R3E-FU) | `r3e-future-unseen-v1` |
| detector_version / parameters_hash | `1.0.0` / `2f202cf99000ec16` |
| cost_model_version | `1.0.0-provisional` (congelado pós-holdout) |
| seed / bootstrap | `42` / `1000` |
| holdout R3D | consumido 1×; **reuso proibido** |
| R3D mecânico | 0 PASSES / 568 FAILS / 3272 INCONCLUSIVE |
| Ações 1d | `PARTIAL_ACCEPTED_FOR_R3D` (~4.988y) |
| Paper trading | **não iniciado** |
| Tags | `v0.1.0-r1` … `v0.4.0-r3d-real-validation`, `v0.5.0-r3e-engine` |

## Encerramento R1

| Campo | Valor |
|-------|--------|
| Status | Concluída — `R1_GATE = APPROVED` |
| PR | https://github.com/multivacia/wick/pull/1 (MERGED) |
| Tag | `v0.1.0-r1` |

## Status R2 / R3 / R3D

| Campo | Valor |
|-------|--------|
| R2 PR | https://github.com/multivacia/wick/pull/2 (MERGED) · tag `v0.2.0-r2` |
| R3A PR | https://github.com/multivacia/wick/pull/3 (MERGED) |
| R3B PR | https://github.com/multivacia/wick/pull/4 (MERGED) · tag `v0.3.0-r3` |
| R3D PR | https://github.com/multivacia/wick/pull/5 · tag `v0.4.0-r3d-real-validation` |
| Custos | `1.0.0-provisional` — não alterar para reavaliar `r3d-real-validation-v1` |
| R3_GATE | `REJECTED_NO_MEASURABLE_EDGE_V1` |
| R3E engine | PR #6 · tag `v0.5.0-r3e-engine` · `experiment_id=r3e-contextual-edge-v1` |
| R3E real-data | PR #7 **MERGED** · `CANDLE_ADDS_NO_VALUE` · 0 `CANDLE_ADDS_VALUE_EXPLORATORY` · sem evidência de valor incremental do candle |
| R3E_GATE | `PENDING_FUTURE_UNSEEN_DATA` (holdout R3D **não** reutilizado; validação final = dados futuros) |
| Interpretação econômica | **não aprovada** |
| R4 / R5 | BLOCKED / NOT_STARTED |

## Gates

- R1 → R2: **aprovado**; merges em `main` concluídos.
- R2 → R3: **aprovado**.
- R3 → R4: **rejeitado na v1** — sem edge mensurável sob metodologia/custos congelados; R4 bloqueada.
- R3E: nested walk-forward; validação final exige dados futuros inéditos; R4 permanece bloqueada.
- R4 → R5: paper signals auditáveis, sem execução real (não iniciado).
- Qualquer uso de dinheiro real exige decisão humana explícita.

## Stack

Python 3.11+, uv, SQLAlchemy 2.x, psycopg 3, Alembic, **PostgreSQL 16** (oficial; mínimo 15 por `NULLS NOT DISTINCT`), TimescaleDB opcional, Polars, NumPy, pydantic-settings, pytest, ruff, Docker Compose, GitHub Actions CI.

## Fontes de dados (R1)

- Binance via endpoints públicos de klines (`data-api.binance.vision`; interface ccxt-compatível nos testes).
- Yahoo Finance via yfinance (sem cadastro); ver `docs/audits/R3D_YAHOO_1H_COVERAGE.md` para limites intraday observados.
- brapi plugável e opcional (token em `.env` quando disponível).

## Log de decisões

| Data | Decisão | Contexto | Impacto |
|------|----------|----------|---------|
| 2026-07-15 | Iniciar R1 em repositório vazio na branch `feature/r1-ingestion` | Pacote de specs como fonte de verdade | Base do projeto Wick |
| 2026-07-15 | Alembic como única fonte de schema em runtime | Evitar `create_all` na aplicação | Reproduzibilidade de schema |
| 2026-07-15 | Binance via `data-api.binance.vision` | `api.binance.com` retornou 451 no ambiente | Market data público sem API key |
| 2026-07-15 | Incremental append-only; lacunas históricas com `--full` | Escopo R1 sem motor de repair | Atualização busca faltantes à frente |
| 2026-07-16 | Upsert `ON CONFLICT DO NOTHING` + `SELECT FOR UPDATE` | Corrida de criação vs serialização de revisão | Idempotência concorrente |
| 2026-07-16 | `NULLS NOT DISTINCT` em `asset(symbol, source, exchange)` | Unique clássico permitia duplicatas com `exchange` NULL | Exige PostgreSQL ≥ 15 |
| 2026-07-16 | PostgreSQL 16 oficial; 15 mínimo; Timescale `2.28.3-pg16` | Homologação e CI | Compose/CI fixados em 16 |
| 2026-07-16 | CI GitHub Actions com PG 16 vazio + Alembic | Gate de hardening | PR bloqueável por checks |
| 2026-07-16 | `R1_GATE = APPROVED` | Hardening + CI verde + 39 testes | R1 encerrada |
| 2026-07-16 | Implementar R2 com `R2_PATTERN_SPECIFICATION.md` | Spec executável fornecida pelo humano | Oito padrões oficiais, sem retorno |
| 2026-07-16 | Custos R3 provisórios (BASE total 0.0024) | Numerics ausentes na metodologia | `1.0.0-provisional`; confirmação humana antes de R4 |
| 2026-07-16 | Merges PR #1–#4 em `main` + tags v0.1/v0.2/v0.3 | Autorização humana explícita | Cadeia R1–R3 em main |
| 2026-07-16 | R3D: universo cripto+ações, 1h/1d, sem recalibrar | Validação honesta em dados reais | Branch `feature/r3d-real-data-validation` |
| 2026-07-16 | R3D: 0 estratégias passaram o gate mecânico | 568 FAILS; 3272 INCONCLUSIVE; 0 promovidas | Resultado negativo aceito como conclusão válida |
| 2026-07-16 | Parâmetros e custos **não** alterados após abertura do holdout | Holdout consumido 1×; reuso proibido | Experimento `r3d-real-validation-v1` congelado |
| 2026-07-16 | Ações 1d ~4.988y → `PARTIAL_ACCEPTED_FOR_R3D` | Sem fill artificial; aceite humano para R3D | Não reclassifica COMPLETE |
| 2026-07-16 | `R3_GATE = REJECTED_NO_MEASURABLE_EDGE_V1` | Autorização humana pós-auditoria R3D | R4/R5 não iniciados; sem paper trading |
| 2026-07-17 | Iniciar R3E como experimento independente | Holdout R3D consumido; não reutilizar | `r3e-contextual-edge-v1`; nested WF |
| 2026-07-17 | R3E: M0–M5, DELTA_CANDLE=M5−M4, grids/thresholds congelados | Spec `R3E_CONTEXTUAL_EDGE_SPECIFICATION` | Sem AutoML/árvores; custos `1.0.0-provisional` |
| 2026-07-17 | `R3E_GATE = PENDING_FUTURE_UNSEEN_DATA` | Mesmo com resultados de desenvolvimento | R4 bloqueada; sem paper trading |
| 2026-07-17 | R3E code gate APPROVED; development run SYNTHETIC_ONLY | Relatórios marcados sem interpretação econômica | Tag `v0.5.0-r3e-engine` |
| 2026-07-17 | Merge PR #6 + tag `v0.5.0-r3e-engine` | Encerramento motor R3E | Real-data run autorizado em seguida |
| 2026-07-18 | R3E real-data exploratory run COMPLETE | Nested WF em OHLCV real; holdout R3D excluído | `CANDLE_ADDS_NO_VALUE`; R4 permanece BLOCKED |
| 2026-07-18 | Ratificação humana: sem evidência de valor incremental do candle | Protocolo R3E congelado; FDR sem Δ(M5−M4) significativo | `ECONOMIC_INTERPRETATION_ALLOWED=false`; `R3E_GATE=PENDING_FUTURE_UNSEEN_DATA`; `R4_STATUS=BLOCKED` |
| 2026-07-18 | Merge PR #7 em `main` | Registro da execução exploratória real + auditoria apenas | Não autoriza interpretação econômica, gate final R3E nem R4 |
| 2026-07-18 | Infra R3E future-unseen | Cutoff `2026-07-18T01:30:00Z`; ingestão append-only; ops sem peeking; gate automático | Coleta `NOT_STARTED`; R4 bloqueada; sem usar histórico como futuro |
| 2026-07-18 | Merge PR #8 em `main` (`2cf41f3`) | Infra de validação futura incorporada | Cutoff/freeze preservados; sem evidência científica |
| 2026-07-18 | Init formal da coleta future-unseen | `python -m wick.r3e.future_unseen init` (PR #9 → `20201e1`) | `R3E_FUTURE_DATA_COLLECTION=IN_PROGRESS`; `validate` não executado |
| 2026-07-18 | Backfill operacional 90d histórico | `python -m wick.r3e.operational_backfill collect` | 20/20 séries; 13725 barras; sandbox isolada; gate inalterado |
| 2026-07-18 | Merge PR #11 em `main` (`132bbb1`) | Backfill operacional incorporado | Scientific eligibility=false; future-unseen intacto |
| 2026-07-18 | Coletor incremental future-unseen | `python -m wick.r3e.future_unseen collect` | 70 obs pós-cutoff (crypto 1h); validate não executado |
| 2026-07-18 | Merge PR #12 em `main` (`a258e71`) | Coletor incremental + governança de revisão incorporados | Coleta permanece `IN_PROGRESS`; `validate` não executado; R4/R5 inalterados |
| 2026-07-18 | Próximo item R3E formalmente ambíguo | Fontes oficiais conflitam (coleta contínua vs readiness vs validate) | `BLOCKED_BY_AMBIGUOUS_NEXT_ITEM`; sem implementação por inferência |
| 2026-07-18 | Autorização humana B2 / R3E-READINESS-001 | Ambiguidade pós-PR #12 resolvida | Próximo item = Future-Unseen Readiness Gate; validate/R4/R5 não autorizados |
| 2026-07-18 | Implementação B2 readiness gate | `python -m wick.r3e.future_unseen readiness` | Gate operacional READY/NOT_READY/BLOCKED; validate/R4/R5 inalterados |
| 2026-07-18 | Validação final PR #15 readiness | CI GREEN; 172 pytest; readiness NOT_READY | Merge autorizado por gates; validate/R4/R5 inalterados |
| 2026-07-18 | Merge PR #15 em `main` (`9220a14`) | Readiness gate B2 incorporado | Coleta permanece IN_PROGRESS; validate não autorizado; R4/R5 inalterados |
| 2026-07-18 | B3 coleta incremental continuity | dry-run+collect+idempotency; 70→85 obs | Readiness NOT_READY (window); validate não executado |
| 2026-07-18 | Merge PR #17 em `main` (`d32e027`) | Continuação B3 + reconciliação imutável `bc6a0d0` | Coleta permanece IN_PROGRESS; validate não autorizado; R4/R5 inalterados |
| 2026-07-18 | G1 impact assessment gate | Análise de impacto pré-implementação obrigatória | B4 fica IMPACT_ANALYSIS_REQUIRED até impacto aprovado |
| 2026-07-18 | Merge PR #20 em `main` (`3e839a2`) | Gate G1 vigente | PR #19 B4 bloqueada até impacto aprovado; validate inalterado |
| 2026-07-18 | B4 impacto APPROVE_WITH_CHANGES | Impacto aprovado; implementação autorizada com ajustes | PR #19 draft; merge não autorizado; validate inalterado |
| 2026-07-18 | Merge PR #19 em `main` (`f773702`) | Automação `run-cycle` B4 incorporada | Scheduler não ativado; validate não autorizado; R4/R5 inalterados |
| 2026-07-18 | Próximo item R3E pós-B4 ambíguo | Sem B5/TASK_ID oficial inequívoco | `BLOCKED_BY_AMBIGUOUS_NEXT_ITEM`; sem implementação por inferência |
| 2026-07-18 | Handoff pós-merge B4 (PR #22) | Merge PR #19 + reconciliação próximo item | Sem implementação; scheduler não ativado; validate/R4/R5 inalterados |
| 2026-07-18 | Humano nomeia B5 / COLLECTION-SCHEDULER-ACTIVATION-001 | Próximo item oficial pós-B4 | Impacto HIGH; `IMPACT_ASSESSMENT_STATUS=BLOCKED` até owner/host; sem ativação |
| 2026-07-18 | Impacto B5 scheduler (draft PR) | Comparação de hosts/store/secrets/rollback | Ativação bloqueada; validate/R4/R5 inalterados |
| 2026-07-18 | Merge PR #23 em `main` (`c098fa8`) | Impacto B5 BLOCKED incorporado | Sem ativação; 6 decisões humanas pendentes; validate/R4/R5 inalterados |
| 2026-07-18 | Decisões humanas B5 completas | Owner Gustavo; HostGator VPS; `/srv/wick`; systemd env; email | Impacto APPROVED; preparação autorizada; ativação ainda bloqueada |
| 2026-07-18 | Preparação HostGator B5 (draft PR) | units/runbook/backup/healthcheck | Timer não habilitado; validate/R4/R5 inalterados |
| 2026-07-19 | Merge PR #25 em `main` (`b5bb3f1`) | Preparação B5 HostGator incorporada | Timer não habilitado; host readiness pendente; validate/R4/R5 inalterados |
| 2026-07-19 | Ficha readiness HostGator B5 | Campos reais do VPS deixados vazios | `HOST_READINESS_STATUS=BLOCKED_PENDING_REAL_HOST_DETAILS` |
| 2026-07-19 | B5 troca para LOCAL_PERSISTENT_HOST | HostGator deferred; path `$HOME/wick-r3e` | Preparação local apenas; scheduler não ativado; validate/R4/R5 inalterados |
| 2026-07-19 | Merge PR #27 em `main` (`134f066`) | Preparação local B5 incorporada | Timer não habilitado; discovery no host real ainda pendente |
| 2026-07-19 | B5-D1 discovery preparation | Scripts read-only sh/ps1 + runbook | Resultado gerado só no host operacional; sem ativação |
| 2026-07-19 | Merge PR #28 em `main` (`83308f5`) | Discovery prep B5-D1 incorporada | Pacote operador publicado; discovery no Cursor não executada |
| 2026-07-19 | Pacote de execução operador B5-D1 | Guia copy-paste Windows/Linux | Aguardando `R3E_LOCAL_HOST_DISCOVERY_RESULT.md` do host real |
| 2026-07-19 | Abrir trilha paralela UX-R1 (Operational Experience) | Fundação UX-B1; sem UI; R3E inalterado | `UX-R1_STATUS=PLANNING`; `UI_IMPLEMENTATION_AUTHORIZED=false` |
| 2026-07-19 | Reconciliar impacto UX-B1 e congelar evidência final | Impacto APPROVED; review alinhada; PR #31 draft | `UX-B1_STATUS=READY_FOR_HUMAN_MERGE_REVIEW`; UX-B2 bloqueado; merge humano pendente |
| 2026-07-19 | Merge PR #31 UX-B1 Experience Foundation | Autorização humana; docs-only; R3E inalterado | `UX-B1_STATUS=MERGED`; UX-B2 bloqueado até impacto/autorização separados; UI não autorizada |
| 2026-07-19 | Iniciar impacto UX-B2 Design System Foundation | Fase IMPACT_ASSESSMENT_ONLY; sem UI | `UX-B2_STATUS=IMPACT_ASSESSMENT_IN_PROGRESS`; implementação não autorizada |
| 2026-07-19 | Reconciliar impacto UX-B2 (rebase + APPROVED) | Option B locked; gates definidos; sem código UI | `UX-B2_STATUS=IMPACT_ASSESSMENT_READY_FOR_HUMAN_REVIEW`; `UX_B2_IMPLEMENTATION_AUTHORIZED=false` |
| 2026-07-19 | Congelar evidência final UX-B2 (PR #35) | Revalidação local PASS; backlog alinhado; merge humano pendente | `IMPACT_ASSESSMENT_STATUS=APPROVED`; `UI_IMPLEMENTATION_AUTHORIZED=false` |
| 2026-07-19 | Merge PR #35 UX-B2 Design System impact | Docs-only; Option B locked; sem código UI | `UX_B2_IMPACT_STATUS=MERGED`; `UX_B2_IMPLEMENTATION_STATUS=BLOCKED_PENDING_EXPLICIT_AUTHORIZATION` |
| 2026-07-19 | Post-merge + merge-complete UX-B2 impact | PR #39 handoff; implementação bloqueada | `NEXT_ITEM=IMPLEMENTATION_AUTHORIZATION_ASSESSMENT`; UI não autorizada |
| 2026-07-19 | Avaliação de autorização de implementação UX-B2 | I1-only; stack locked; sem código UI | `UX_B2_AUTHORIZATION_ASSESSMENT_STATUS=IN_PROGRESS`; `AUTHORIZATION_DECISION=AUTHORIZED_FOR_INCREMENT_I1_ONLY` |
| 2026-07-19 | Merge PR #43 autorização I1 UX-B2 | Docs-only; I1 future task only | `UX_B2_AUTHORIZATION_STATUS=MERGED`; `I1_IMPLEMENTATION_STATUS=BLOCKED_PENDING_SEPARATE_TASK_AND_HUMAN_AUTHORIZATION` |
| 2026-07-19 | Post-merge + merge-complete autorização I1 UX-B2 | PR #45 handoff; I1 ainda bloqueado | `NEXT_ITEM=I1 FRONTEND-SCAFFOLD-AND-CI`; UI não autorizada |
| 2026-07-19 | UX-B4 linguagem operacional e microcopy | Catálogos docs-only; trilha independente de B2/B3 | `UX_B4_STATUS=CONTENT_DESIGN_READY_FOR_HUMAN_REVIEW`; `UX_B4_IMPLEMENTATION_AUTHORIZED=false`; UI não autorizada; R3E inalterado |
| 2026-07-19 | Merge PR #42 UX-B4 Operational Language | Autorização humana; docs-only; R3E inalterado | `UX_B4_STATUS=MERGED`; `UX_B4_IMPLEMENTATION_AUTHORIZED=false`; UI não autorizada |
| 2026-07-19 | Merge PR #44 UX-B3 Operational MVP Screen Contracts | Autorização humana; docs-only; consome UX-B4 | `UX_B3_STATUS=MERGED`; `UX_B3_IMPLEMENTATION_AUTHORIZED=false`; UI não autorizada |
| 2026-07-19 | Fechamento coordenado UX-B2/B3/B4 | B2 COMPLETE (I1-only); B3+B4 MERGED | `NEXT_ITEM=I1 FRONTEND-SCAFFOLD-AND-CI` (tarefa separada); scheduler/validate inalterados |
| 2026-07-19 | Merge PR #58 kickoff paralelo I2/I5A/I6A | Coordenação docs-only; PRs #55/#56/#57 permanecem draft | `I2_STATUS=ASSESSMENT_IN_PROGRESS`; `I5A_STATUS=ARCHITECTURE_IN_PROGRESS`; `I6A_STATUS=DATA_PREPARATION_IN_PROGRESS`; implementação não autorizada |
| 2026-07-19 | Merge PR #59 kickoff final-merge handoff | Status I2/I5A/I6A reconciliado em `main`; workstreams ainda draft | `PR58+PR59=MERGED`; PRs #55/#56/#57 `OPEN_DRAFT`; implementação não autorizada |
| 2026-07-19 | Merge PR #60 kickoff merge-complete record | Coordenação I2/I5A/I6A encerrada no track de kickoff | `PR58+PR59+PR60=MERGED`; PRs #55/#56/#57 `OPEN_DRAFT_REBASE_REQUIRED`; sem MAIN_TIP-only follow-up |
| 2026-07-19 | Merge PR #61 kickoff final-closure | Track de kickoff paralelo COMPLETE em `main` | `PARALLEL_KICKOFF_STATUS=COMPLETE`; PRs #55/#56/#57 abertos; implementação não autorizada |
| 2026-07-19 | Merge PR #55 I2 design tokens assessment | Docs-only; condições C1–C8; sem CSS/tokens | `I2_STATUS=ASSESSMENT_MERGED`; `AUTHORIZED_WITH_CONDITIONS`; `I2_IMPLEMENTATION_AUTHORIZED=false`; NEXT=I5A PR56 |
| 2026-07-19 | Merge PR #56 I5A shell/nav architecture | Docs-only; condições C1–C8; sem router/shell | `I5A_STATUS=ARCHITECTURE_MERGED`; `AUTHORIZED_WITH_CONDITIONS`; `I5_IMPLEMENTATION_AUTHORIZED=false`; `ROUTER_INSTALLATION_AUTHORIZED=false`; NEXT=I6A PR57 |
| 2026-07-19 | Merge PR #57 I6A Overview data/fixtures | Docs-only; condições C1–C8; sem ViewModel/TS/screen | `I6A_STATUS=DATA_PREPARATION_MERGED`; `AUTHORIZED_WITH_CONDITIONS`; `RUNTIME_IMPLEMENTATION_AUTHORIZED=false`; NEXT=I2/I5/I6 implementation authorization assessment |
| 2026-07-19 | Abrir avaliação autorização I2/I3/I5/I6 | Docs-only; decomposição não monolítica; I6D BLOCKED | `NEXT_RECOMMENDED_TASK=I2_DESIGN_TOKENS_AND_THEMES_IMPLEMENTATION`; todas flags de implementação permanecem false |
| 2026-07-19 | I3 minimum accessible primitives (implementação) | Primitivos + Radix Dialog only; draft PR; sem merge | `I3_STATUS=IMPLEMENTATION_IN_PROGRESS`; `I3_MERGE_AUTHORIZED=false`; I5/I6/router/screens false |
| 2026-07-20 | Merge PR #72 I3 minimum accessible primitives | Primitivos MERGED; Radix Dialog only; sem router/shell/telas | `I3_STATUS=IMPLEMENTATION_MERGED`; `I3_PREREQUISITE_DECISION=SATISFIED_FOR_I5_AND_I6C`; NEXT=I5 shell/nav (não autorizado) |
| 2026-07-20 | Post-merge closure I3 (PRs #73/#74) | Handoffs final-merge + merge-complete; PROJECT reconciliado | `I3_IMPLEMENTATION_STATUS=MERGED`; `NEXT_ITEM=I5_APPLICATION_SHELL_AND_NAVIGATION_SEPARATE_IMPLEMENTATION_TASK`; I5 não autorizado |
| 2026-07-20 | I5 application shell and navigation (implementação) | Shell + react-router-dom; placeholders only; draft PR; sem merge | `I5_STATUS=IMPLEMENTATION_IN_PROGRESS`; `I5_MERGE_AUTHORIZED=false`; screens/ViewModel/fixtures false |
| 2026-07-20 | Merge PR #77 I5 application shell and navigation | Shell/nav MERGED; react-router-dom only; placeholders; sem telas/ViewModel | `I5_STATUS=IMPLEMENTATION_MERGED`; `I5_IMPLEMENTATION_STATUS=MERGED`; NEXT=I6B ViewModel (não autorizado) |
| 2026-07-20 | Post-merge closure I5 (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `I6B_DECISION=AUTHORIZED_WITH_CONDITIONS`; `I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED=false`; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-20 | I6B ViewModel implementation | Pure builders + contracts; draft PR; sem fixtures/telas/dados reais | `I6B_STATUS=IMPLEMENTATION_IN_PROGRESS`; `I6_VIEWMODEL_MERGE_AUTHORIZED=false`; screens/fixtures false |
| 2026-07-20 | Merge PR #81 I6B ViewModel | ViewModel MERGED; sem fixtures/telas/dados reais | `I6B_STATUS=IMPLEMENTATION_MERGED`; `I6_VIEWMODEL_IMPLEMENTATION_STATUS=MERGED`; NEXT=I6C fixtures (não autorizado) |
| 2026-07-20 | Post-merge closure I6B (PRs #82/#83) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `I6C_DECISION=AUTHORIZED_WITH_CONDITIONS`; `I6_FIXTURE_IMPLEMENTATION_AUTHORIZED=false`; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-20 | I6C executable fixtures implementation | Fixtures sintéticas + catálogo; draft PR; sem telas/dados reais | `I6C_STATUS=IMPLEMENTATION_IN_PROGRESS`; `I6_FIXTURE_MERGE_AUTHORIZED=false`; screens false |
| 2026-07-20 | Merge PR #84 I6C executable fixtures | Fixtures MERGED; sintéticas; sem telas/seletor/dados reais | `I6C_STATUS=IMPLEMENTATION_MERGED`; `I6_FIXTURE_IMPLEMENTATION_STATUS=MERGED`; NEXT=I6 screen auth assessment |
| 2026-07-20 | Post-merge closure I6C (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `I6_SCREEN_IMPLEMENTATION_AUTHORIZED=false`; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-20 | I6D screen implementation authorization assessment | Docs-only; OVERVIEW_FIRST; AUTHORIZED_WITH_CONDITIONS | `I6D_DECISION=AUTHORIZED_WITH_CONDITIONS`; `I6_SCREEN_IMPLEMENTATION_AUTHORIZED=false`; NEXT=Overview screen (não autorizado) |
| 2026-07-20 | Merge PR #87 I6D screen authorization assessment | Assessment MERGED; Overview-first; execução de telas ainda false | `I6D_SCREEN_AUTHORIZATION_ASSESSMENT_STATUS=MERGED`; `I6_SCREEN_IMPLEMENTATION_AUTHORIZED=false`; NEXT=I6 Overview screen (não autorizado) |
| 2026-07-20 | Post-merge closure I6D assessment (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | flags de execução de tela permanecem false; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-20 | I6E Overview screen implementation | Visão Geral fixture-backed; draft PR; sem merge; outras telas não implementadas | `I6E_STATUS=IMPLEMENTATION_IN_PROGRESS`; `I6_OVERVIEW_SCREEN_MERGE_AUTHORIZED=false`; `OPERATIONAL_ACTIONS=false` |
| 2026-07-20 | Merge PR #90 I6E Overview screen | Visão Geral MERGED; fixture `current_project_state_illustrative`; sem dados reais/ações | `I6E_STATUS=IMPLEMENTATION_MERGED`; `I6_OVERVIEW_SCREEN_IMPLEMENTATION_STATUS=MERGED`; NEXT=Runs auth assessment |
| 2026-07-20 | Post-merge closure I6E (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED=false`; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-20 | I6F Runs screen authorization assessment | Docs-only; Runs-only fixture/read-only; AUTHORIZED_WITH_CONDITIONS | `I6F_DECISION=AUTHORIZED_WITH_CONDITIONS`; `RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED=false`; NEXT=Runs screen (não autorizado) |
| 2026-07-20 | Merge PR #92 I6F Runs authorization assessment | Assessment MERGED; Runs-only boundary; execução ainda false | `I6F_RUNS_SCREEN_AUTHORIZATION_ASSESSMENT_STATUS=MERGED`; `RUNS_SCREEN_IMPLEMENTATION_AUTHORIZED=false`; NEXT=I6 Runs screen (não autorizado) |
| 2026-07-20 | Post-merge closure I6F assessment (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | flags de execução permanecem false; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-20 | I6G Runs screen implementation | Execuções fixture-backed; draft PR; sem merge; Readiness/Host não implementados | `I6G_STATUS=IMPLEMENTATION_IN_PROGRESS`; `I6_RUNS_SCREEN_MERGE_AUTHORIZED=false`; `OPERATIONAL_ACTIONS=false` |
| 2026-07-20 | Merge PR #94 I6G Runs screen | Execuções MERGED; fixture `current_project_state_illustrative`; sem dados reais/ações | `I6G_STATUS=IMPLEMENTATION_MERGED`; `I6_RUNS_SCREEN_IMPLEMENTATION_STATUS=MERGED`; NEXT=Readiness auth assessment |
| 2026-07-20 | Post-merge closure I6G (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED=false`; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-20 | I6H Readiness screen authorization assessment | Docs-only; Readiness-only fixture/read-only; AUTHORIZED_WITH_CONDITIONS | `I6H_DECISION=AUTHORIZED_WITH_CONDITIONS`; `READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED=false`; NEXT=Readiness screen (não autorizado) |
| 2026-07-20 | Merge PR #96 I6H Readiness authorization | Assessment MERGED; boundary Readiness-only fixture/read-only | `I6H_STATUS=ASSESSMENT_MERGED`; `I6H_READINESS_SCREEN_AUTHORIZATION_ASSESSMENT_STATUS=MERGED`; execution flags false |
| 2026-07-20 | Post-merge closure I6H assessment (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `READINESS_SCREEN_IMPLEMENTATION_AUTHORIZED=false`; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-20 | I6I Readiness screen implementation | Prontidão fixture-backed; draft PR; sem merge; Host não implementado | `I6I_STATUS=IMPLEMENTATION_IN_PROGRESS`; `READINESS_SCREEN_MERGE_AUTHORIZED=false`; `OPERATIONAL_ACTIONS=false` |
| 2026-07-20 | Merge PR #98 I6I Readiness screen | Prontidão MERGED; fixture `current_project_state_illustrative`; sem dados reais/ações | `I6I_STATUS=IMPLEMENTATION_MERGED`; `I6_READINESS_SCREEN_IMPLEMENTATION_STATUS=MERGED`; NEXT=Host auth assessment |
| 2026-07-20 | Post-merge closure I6I (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED=false`; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-20 | I6J Host/Scheduler screen authorization assessment | Docs-only; Host-only fixture/read-only; HIGH risk; AUTHORIZED_WITH_CONDITIONS | `I6J_DECISION=AUTHORIZED_WITH_CONDITIONS`; `HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED=false`; NEXT=Host screen (não autorizado) |
| 2026-07-20 | Merge PR #100 I6J Host/Scheduler authorization | Assessment MERGED; boundary Host-only fixture/read-only; sem ativação | `I6J_STATUS=ASSESSMENT_MERGED`; `I6J_HOST_SCHEDULER_SCREEN_AUTHORIZATION_ASSESSMENT_STATUS=MERGED`; execution flags false |
| 2026-07-20 | Post-merge closure I6J assessment (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED=false`; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-20 | I6K Host/Scheduler screen implementation | Host e Automação fixture-backed; draft PR; sem merge; sem discovery/ativação | `I6K_STATUS=IMPLEMENTATION_IN_PROGRESS`; `HOST_SCHEDULER_SCREEN_MERGE_AUTHORIZED=false`; `OPERATIONAL_ACTIONS=false` |
| 2026-07-21 | Merge PR #102 I6K Host/Scheduler screen | Host e Automação MERGED; fixture `current_project_state_illustrative`; sem discovery/ativação | `I6K_STATUS=IMPLEMENTATION_MERGED`; `I6_HOST_SCHEDULER_SCREEN_IMPLEMENTATION_STATUS=MERGED`; NEXT=R3E auth assessment |
| 2026-07-21 | Post-merge closure I6K (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `PARALLEL_TASKS_ALLOWED=false`; `SCHEDULER_ACTIVATION=BLOCKED`; `HOST_DISCOVERY=DEFERRED` |
| 2026-07-21 | I6L R3E experiment screen authorization assessment | Docs-only; HIGH risk; AUTHORIZED_WITH_CONDITIONS; rota `/experiments/r3e` | `I6L_DECISION=AUTHORIZED_WITH_CONDITIONS`; `R3E_EXPERIMENT_SCREEN_IMPLEMENTATION_AUTHORIZED=false`; NEXT=R3E screen (não autorizado) |
| 2026-07-21 | Merge PR #104 I6L R3E authorization | Assessment MERGED; boundary explanatory-only fixture/read-only; ViewModel+fixture required | `I6L_STATUS=ASSESSMENT_MERGED`; `I6L_R3E_EXPERIMENT_SCREEN_AUTHORIZATION_ASSESSMENT_STATUS=MERGED`; execution flags false |
| 2026-07-21 | Post-merge closure I6L assessment (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `R3E_EXPERIMENT_SCREEN_IMPLEMENTATION_AUTHORIZED=false`; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-21 | I6M R3E experiment screen implementation | Experimento R3E fixture-backed; ViewModel+fixture dedicados; draft PR #106 | `I6M_STATUS=IMPLEMENTATION_COMPLETE_AWAITING_MERGE`; merge false até autorização |
| 2026-07-21 | Merge PR #106 I6M R3E experiment screen | `/experiments/r3e` MERGED; fixture `r3e_experiment_current_state_illustrative`; sem dados reais/validate/peeking | `I6M_STATUS=IMPLEMENTATION_MERGED`; `I6_R3E_EXPERIMENT_SCREEN_IMPLEMENTATION_STATUS=MERGED`; NEXT=UX_R1_FINAL_CLOSURE_ASSESSMENT |
| 2026-07-21 | Post-merge closure I6M (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `PARALLEL_TASKS_ALLOWED=false`; `R3E_GATE=PENDING_FUTURE_UNSEEN_DATA`; R4 blocked; R5 not started |
| 2026-07-21 | UX-R1 final closure and acceptance assessment | Docs-only; HIGH risk; ACCEPTED_FOR_CLOSURE (fixture-backed read-only) | `UX_R1_RELEASE_CLOSURE_AUTHORIZED=false`; `UX_R1_RELEASE_ACCEPTANCE_AUTHORIZED=false`; NEXT=release closure stamp |
| 2026-07-21 | Merge PR #108 UX-R1 final closure assessment | Assessment MERGED; ACCEPTED_FOR_CLOSURE; sem stamp formal | `UX_R1_FINAL_CLOSURE_ASSESSMENT_STATUS=MERGED`; closure/acceptance flags false; NEXT=UX_R1_RELEASE_CLOSURE_STAMP |
| 2026-07-21 | Post-merge closure final assessment (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | flags de stamp formal permanecem false; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-21 | UX-R1 formal release closure and acceptance stamp | Docs-only; HIGH; CLOSED/ACCEPTED fixture-backed read-only | `UX_R1_RELEASE_CLOSED=true`; `UX_R1_RELEASE_ACCEPTED=true`; NEXT=UX_R2 discovery (não iniciado) |
| 2026-07-21 | Merge PR #110 UX-R1 formal release stamp | CLOSED/ACCEPTED MERGED; scope FIXTURE_BACKED_READ_ONLY | wording exact; R3E/R4/R5 inalterados; UX-R2 não iniciado |
| 2026-07-21 | Post-merge closure formal stamp (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `PARALLEL_TASKS_ALLOWED=false`; NEXT=UX_R2 discovery (não iniciado) |
| 2026-07-21 | UX-R2 discovery and scope assessment | Docs-only; HIGH; SCOPE_RECOMMENDED → Evidence/Audit Explorer | `UX_R2_IMPLEMENTATION_AUTHORIZED=false`; NEXT=I1 Evidence Explorer auth (não autorizado) |
| 2026-07-21 | Merge PR #112 UX-R2 discovery assessment | Discovery MERGED; SCOPE_RECOMMENDED; sem implementação | `UX_R2_DISCOVERY_AND_SCOPE_STATUS=MERGED`; NEXT=I1 auth assessment (não iniciado) |
| 2026-07-21 | Post-merge closure UX-R2 discovery (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | flags de implementação permanecem false; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-21 | UX-R2 I1 Evidence Explorer authorization assessment | Docs-only; HIGH; AUTHORIZED_WITH_CONDITIONS; `/governance/evidence` | implementation flags false; NEXT=I1 Evidence Explorer implementation (não autorizado) |
| 2026-07-21 | Merge PR #114 UX-R2 I1 Evidence Explorer auth | Auth assessment MERGED; AUTHORIZED_WITH_CONDITIONS; sem implementação | `UX_R2_I1_EVIDENCE_EXPLORER_AUTHORIZATION_ASSESSMENT_STATUS=MERGED`; NEXT=implementation (não iniciado) |
| 2026-07-21 | Post-merge closure I1 Evidence auth (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | flags de implementação permanecem false; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-21 | UX-R2 I1 Evidence Explorer implementation | Evidências fixture-backed; ViewModel+catálogo curado; draft PR; review APPROVED | `UX_R2_I1_STATUS=IMPLEMENTATION_COMPLETE_AWAITING_MERGE`; merge false até autorização humana |
| 2026-07-21 | Merge PR #116 UX-R2 I1 Evidence Explorer | `/governance/evidence` MERGED; fixture `evidence_catalog_current_state_illustrative`; sem dados reais/FS | `UX_R2_I1_EVIDENCE_EXPLORER_IMPLEMENTATION_STATUS=MERGED`; NEXT=post-merge acceptance |
| 2026-07-21 | Post-merge closure I1 Evidence impl (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `PARALLEL_TASKS_ALLOWED=false`; acceptance não iniciado |
| 2026-07-21 | UX-R2 remaining-release integral plan | Docs-only; freeze I2–I5; single-execution model with conditions | flags de execução permanecem false; NEXT=single execution (não autorizado) |
| 2026-07-21 | Merge PR #118 UX-R2 remaining integral plan | Plan MERGED; AUTHORIZED_FOR_SINGLE_EXECUTION_WITH_CONDITIONS | execution flags false until separate prompt |
| 2026-07-21 | Post-merge closure integral plan (#119) | FINAL-MERGE + MERGE-COMPLETE | `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-21 | UX-R2 I2–I5 single-branch execution | Catalog history, provenance, cross-nav, closure; draft PR #120 | final review APPROVED; awaits human validation |
| 2026-07-21 | Merge PR #120 UX-R2 I2–I5 single execution | Remaining Evidence Explorer MERGED; sem backend/rotas/deps | `UX_R2_REMAINING_RELEASE_SINGLE_EXECUTION_STATUS=MERGED`; NEXT=final closure assessment |
| 2026-07-21 | Post-merge closure I2–I5 execution (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | UX-R2 ainda NOT_YET_FORMALLY_CLOSED; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-21 | UX-R2 final closure and acceptance assessment | Docs-only; CLOSURE_AND_ACCEPTANCE_RECOMMENDED; sem stamp | flags closure/acceptance/stamp false; NEXT=UX_R2_RELEASE_CLOSURE_STAMP |
| 2026-07-21 | Merge PR #122 UX-R2 final closure assessment | Assessment MERGED; CLOSURE_AND_ACCEPTANCE_RECOMMENDED | stamp authorized by separate prompt; UX-R3 not started |
| 2026-07-21 | Merge PR #123 assessment FINAL-MERGE handoff | Docs-only merge evidence for PR #122 | `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-21 | UX-R2 formal release closure and acceptance stamp | Docs-only; CLOSED/ACCEPTED fixture-backed evidence/audit | wording exact; R3E/R4/R5 inalterados; UX-R3 NOT_STARTED |
| 2026-07-21 | Merge PR #124 UX-R2 formal release stamp | CLOSED/ACCEPTED MERGED; scope FIXTURE_BACKED_EVIDENCE_AND_AUDIT_EXPLORATION | wording exact; NEXT=UX_R3 discovery (não iniciado) |
| 2026-07-21 | Post-merge closure formal stamp (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `PARALLEL_TASKS_ALLOWED=false`; UX-R3 NOT_STARTED |
| 2026-07-22 | UX-R3 discovery and scope assessment | Docs-only; SCOPE_RECOMMENDED; E collection monitoring/data quality | UX-R3 NOT_STARTED; implementation false; NEXT=I1 authorization assessment |
| 2026-07-22 | Merge PR #126 UX-R3 discovery assessment | Discovery MERGED; SCOPE_RECOMMENDED; sem implementação | `UX_R3_DISCOVERY_AND_SCOPE_STATUS=MERGED`; NEXT=I1 auth assessment (não iniciado) |
| 2026-07-22 | Post-merge closure UX-R3 discovery (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `PARALLEL_TASKS_ALLOWED=false`; UX-R3 NOT_STARTED |
| 2026-07-22 | UX-R3 I1 Collection Data Quality authorization assessment | Docs-only; AUTHORIZED_WITH_CONDITIONS; `/future-collection/collected-data` | implementation flags false; NEXT=I1 implementation (não autorizado) |
| 2026-07-22 | Merge PR #128 UX-R3 I1 Collection Data Quality auth | Auth assessment MERGED; AUTHORIZED_WITH_CONDITIONS; sem implementação | `UX_R3_I1_COLLECTION_DATA_QUALITY_AUTHORIZATION_STATUS=MERGED`; NEXT=implementation (não iniciado) |
| 2026-07-22 | Post-merge closure UX-R3 I1 auth (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | flags de implementação permanecem false; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-22 | UX-R3 I1 Collection Data Quality implementation | Fixture-backed Dados Coletados; review APPROVED; draft PR | UX-R3 IN_PROGRESS; NEXT=human merge; I2–I5 not started |
| 2026-07-22 | Merge PR #130 UX-R3 I1 Collection Data Quality impl | `/future-collection/collected-data` MERGED; fixture-backed; sem backend/deps | `UX_R3_I1_STATUS=MERGED`; NEXT=next-increment auth assessment |
| 2026-07-22 | Post-merge closure UX-R3 I1 impl (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | I2–I5 NOT_STARTED; `PARALLEL_TASKS_ALLOWED=false` |
| 2026-07-22 | UX-R3 complete-release impact assessment | Docs-only; REMAINING_SCOPE_RECOMMENDED; I2 cross-nav + I3 closure | remaining unauthorized; CLOSE_AFTER_I1=false |
| 2026-07-23 | Merge PR #132 UX-R3 complete-release impact assessment | Assessment MERGED; delivery model B; 2 remaining increments | `UX_R3_COMPLETE_RELEASE_ASSESSMENT_STATUS=MERGED`; remaining unauthorized |
| 2026-07-23 | Post-merge closure UX-R3 complete-release assessment (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | NEXT=`UX_R3_REMAINING_RELEASE_SINGLE_EXECUTION`; I2/I3 not started |
| 2026-07-23 | UX-R3 remaining-release single execution (I2+I3) | Cross-nav coherence + closure proposal; draft PR; review APPROVED | formal CLOSED/ACCEPTED not stamped; NEXT=human validation |
| 2026-07-23 | Merge PR #134 UX-R3 remaining-release + human validation | I2+I3 MERGED; human validation APPROVED; fixture-backed closure | `UX_R3_RELEASE_STATUS=CLOSED`; `UX_R3_RELEASE_ACCEPTANCE_STATUS=ACCEPTED` |
| 2026-07-23 | Post-merge closure UX-R3 remaining-release + formal stamp | FINAL-MERGE + formal stamp + MERGE-COMPLETE + PROJECT | NEXT=`UX_R4_DISCOVERY_AND_SCOPE_ASSESSMENT` (not authorized) |
| 2026-07-23 | UX-R4 discovery and scope assessment | Docs-only; SCOPE_RECOMMENDED; F decision ledger refresh | UX-R4 NOT_STARTED; implementation false; NEXT=I1 authorization assessment |
| 2026-07-24 | Merge PR #136 UX-R4 discovery assessment | Discovery MERGED; SCOPE_RECOMMENDED; sem implementação | `UX_R4_DISCOVERY_STATUS=MERGED`; NEXT=I1 auth assessment (não iniciado) |
| 2026-07-24 | Post-merge closure UX-R4 discovery (final-merge + merge-complete) | Handoffs + PROJECT reconciliado; sem MAIN_TIP-only | `PARALLEL_TASKS_ALLOWED=false`; UX-R4 NOT_STARTED |
| 2026-07-24 | UX-R4 I1 Decision Ledger authorization assessment | Docs-only; AUTHORIZED_WITH_CONDITIONS; `/governance/evidence` + B_NEW_SECTION_ABOVE_CATALOG | UX-R4 NOT_STARTED; implementation false; NEXT=I2 fixture refresh (não autorizado) |
