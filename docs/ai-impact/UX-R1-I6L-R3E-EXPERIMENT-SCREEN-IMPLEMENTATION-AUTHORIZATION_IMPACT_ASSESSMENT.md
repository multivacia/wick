# UX-R1-I6L-R3E-EXPERIMENT-SCREEN-IMPLEMENTATION-AUTHORIZATION — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = I6_R3E_EXPERIMENT_SCREEN_AUTHORIZATION_ASSESSMENT
TASK_ID = R3E-EXPERIMENT-SCREEN-IMPLEMENTATION-AUTHORIZATION-ASSESSMENT-001
TITLE = R3E Experiment Screen Implementation Authorization Assessment
INCREMENT = I6L
PHASE = AUTHORIZATION_ASSESSMENT
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
ASSESSMENT_ONLY = true
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_SCOPE = AUTHORIZATION_ASSESSMENT_DOCUMENTATION_ONLY
IMPLEMENTATION_EXECUTION_AUTHORIZED = false
DECISION = AUTHORIZED_WITH_CONDITIONS
RECOMMENDED_IMPLEMENTATION_BOUNDARY = R3E_EXPERIMENT_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; EXPLANATORY_ONLY; NO_VISIBLE_FIXTURE_SELECTOR; NO_REAL_DATA; NO_FUTURE_UNSEEN_RESULTS; NO_VALIDATION_EXECUTION; NO_EFFECT_PEEKING; NO_TRADING_RECOMMENDATIONS; NO_PROFITABILITY_CLAIMS; NO_SCIENTIFIC_INTERPRETATION_CHANGE; NO_R4_OR_R5_STATE_CHANGE
SCREEN = Experimento R3E
ROUTE = /experiments/r3e
CANDIDATE_ROUTE_REJECTED = /research/r3e
R3E_EXPERIMENT_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
REAL_DATA_INTEGRATION_AUTHORIZED = false
VALIDATION_EXECUTION_AUTHORIZED = false
EFFECT_PEEKING_AUTHORIZED = false
SCIENTIFIC_INTERPRETATION_CHANGE_AUTHORIZED = false
OPERATIONAL_ACTIONS_AUTHORIZED = false
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
ECONOMIC_INTERPRETATION_ALLOWED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
PR102_STATUS = MERGED
PR102_MERGE_COMMIT = b71ed839e4828b7cba801dff17a8150ed1eb4ffb
PR103_STATUS = MERGED
I6_OVERVIEW_SCREEN_IMPLEMENTATION_STATUS = MERGED
I6_RUNS_SCREEN_IMPLEMENTATION_STATUS = MERGED
I6_READINESS_SCREEN_IMPLEMENTATION_STATUS = MERGED
I6_HOST_SCHEDULER_SCREEN_IMPLEMENTATION_STATUS = MERGED
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 3cd31e76e292b3819ae9efe1120a416372296d49
FINAL_CANDIDATE_HEAD = a5e900eb97ce74b2e7a67885d62d721aed882333
CONTENT_REVIEWED_THROUGH_HEAD = a5e900eb97ce74b2e7a67885d62d721aed882333
POST_REVIEW_NORMATIVE_CHANGES = 0
ANALYZED_AT = 2026-07-21T00:47:00Z
ANALYZED_BY = cursor-agent
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
NEXT_RECOMMENDED_TASK = I6_R3E_EXPERIMENT_SCREEN_IMPLEMENTATION
NEXT_ITEM = I6_R3E_EXPERIMENT_SCREEN_SEPARATE_IMPLEMENTATION_TASK
```

G1 note: This assessment may recommend **AUTHORIZED_WITH_CONDITIONS** for a future R3E explanatory screen task. It does **not** flip `R3E_EXPERIMENT_SCREEN_IMPLEMENTATION_AUTHORIZED`, `IMPLEMENTATION_EXECUTION_AUTHORIZED`, `VALIDATION_EXECUTION_AUTHORIZED`, `EFFECT_PEEKING_AUTHORIZED`, or scientific-interpretation flags to true for product execution. Screen implementation requires a separate human-authorized implementation prompt. R3D and R3E conclusions remain distinct and unchanged. No future-unseen results may be inspected.

## SUMMARY

Prerequisites I6E–I6K are merged (Overview, Runs, Readiness, Host e Automação). The project is ready to authorize a **narrow, fixture-backed, read-only, explanatory Experimento R3E screen** at `/experiments/r3e` that explains hypothesis, protocol, M0–M5, `DELTA_CANDLE = M5 − M4`, temporal/leakage protections, and the pending future-unseen gate — without claiming an edge is proven, future validation passed, R4 unlocked, or economic usefulness. There is **no dedicated R3E ViewModel or fixture today**; the implementation task must introduce a minimal explanatory ViewModel + synthetic fixture (definitions and governed status codes only — no fabricated metrics). Candidate route `/research/r3e` is rejected in favor of the reserved IA/I5A path `/experiments/r3e`.

Approved scientific distinctions to preserve:

```text
R3D_RESULT = NO_MEASURABLE_EDGE
R3_GATE = REJECTED_NO_MEASURABLE_EDGE_V1
R3E_STATUS = EXPLORATORY_COMPLETE_PENDING_FUTURE_UNSEEN_DATA
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
EXPLORATORY_COMPLETE != EDGE_PROVEN
AUDIT_COMPLETE != FUTURE_VALIDATION_COMPLETE
NO_MEASURABLE_EDGE_IN_R3D != R3E_REJECTED
```

## 1. Objetivo

Avaliar se o projeto está pronto para autorizar uma tarefa separada de implementação da tela explicativa **Experimento R3E** (`/experiments/r3e`), somente leitura e alimentada por fixtures, sem implementar a tela, sem executar validação futura, sem effect peeking e sem alterar conclusões científicas nesta tarefa.

## 2. Contexto técnico

- I6K Host e Automação MERGED (PR #102 → `b71ed83`); post-merge closure MERGED (PR #103 → `3cd31e7`).
- `NEXT_RECOMMENDED_TASK` em `main` aponta para `I6_R3E_EXPERIMENT_SCREEN_AUTHORIZATION_ASSESSMENT`.
- I6B ViewModels MERGED — Overview/Runs/Readiness/Host only; **sem** `R3eExperimentViewModel`.
- I6C fixtures MERGED — `scientificGate`/`r4Status`/`r5Status` strings on Overview; readiness validation/effect-peeking booleans; **sem** família R3E de fixtures.
- I5 shell: nav group **Experimentos** → item **R3E** (`active: false`, sem path); rota reservada em I5A/IA: `/experiments/r3e`.
- UX-B3 contracts cobrem apenas quatro telas operacionais; R3E explicativo é UX-B9 (PLANNED).
- Spec científica: `docs/experiments/R3E_CONTEXTUAL_EDGE_SPECIFICATION.md`; guardrails: `docs/ux/UX-R1-SCIENTIFIC-AND-ECONOMIC-LANGUAGE-GUARDRAILS.md`.
- Estado oficial: `R3E_GATE=PENDING_FUTURE_UNSEEN_DATA`, `R4_STATUS=BLOCKED`, `R5_STATUS=NOT_STARTED`, `ECONOMIC_INTERPRETATION_ALLOWED=false`.

## 3. Componentes afetados

| Componente | Impacto nesta tarefa |
|------------|----------------------|
| Docs I6L (impact/review/handoff) | Novos artefatos de autorização |
| `docs/PROJECT.md` | Resultado da assessment + NEXT |
| `web/src/screens/**` | Não modificado |
| Overview / Runs / Readiness / Host | Preservados |
| R3E ViewModel / fixtures / route | Não criados nesta assessment |
| R3E engine / validate / future unseen | Não executados / não alterados |

## 4. Arquivos previstos

```text
docs/ai-impact/UX-R1-I6L-R3E-EXPERIMENT-SCREEN-IMPLEMENTATION-AUTHORIZATION_IMPACT_ASSESSMENT.md
docs/ai-reviews/UX-R1-I6L-R3E-EXPERIMENT-SCREEN-IMPLEMENTATION-AUTHORIZATION_REVIEW.md
reports/ai-implementation/UX-R1-I6L-R3E-EXPERIMENT-SCREEN-IMPLEMENTATION-AUTHORIZATION_HANDOFF.md
docs/PROJECT.md
```

Futura implementação (fora desta tarefa), se autorizada por prompt humano separado:

```text
web/src/viewmodels/*R3e* (or equivalent explanatory ViewModel)
web/src/fixtures/** (r3e illustrative scenario)
web/src/screens/r3e-experiment/** (or experiments/r3e)
web/src/app/AppRoutes.tsx
web/src/shell/navigation.ts
web/tests/screens/** + a11y + architectureBoundary
```

## 5. Contratos e interfaces

```text
RECOMMENDED_ROUTE = /experiments/r3e
REJECTED_CANDIDATE_ROUTE = /research/r3e
RECOMMENDED_NAV_LABEL = R3E
RECOMMENDED_PAGE_TITLE = Experimento R3E
NAV_GROUP = Experimentos

SUPPLIED_OR_AUTHORIZABLE_FIELDS =
  experiment id (governed)
  parent / related experiment ids (R3D vs R3E vs R3E-FU)
  hypothesis (plain language from frozen protocol)
  protocol version / freeze notice
  model family labels M0–M5 (definitions only)
  DELTA_CANDLE definition (M5 − M4)
  temporal split / holdout description (qualitative)
  leakage / preprocessing protection summary (qualitative)
  bootstrap / FDR description (qualitative — no fabricated numbers)
  future unseen gate status code
  collection / readiness status (from existing VMs when composed)
  validationCommandExecuted / effectPeekingPerformed (from Readiness VM)
  next safe scientific action (advisory text)
  evidence references (text-only paths to governed docs)

NOT_AUTHORIZE_FABRICATION =
  p-values
  confidence intervals
  effect sizes
  returns / Sharpe / win rate / drawdown / profitability
  future-unseen outcomes
  validation timestamps of unrun validation
  dataset counts / market symbols / cost tables
  approval decisions / strategy recommendations
```

## 6. Persistência e dados

Nenhuma persistência nesta assessment. Fonte futura autorizável: ViewModel/fixture sintético + metadados governados já mergeados (`docs/PROJECT.md`, R3E specification, B4 guardrails). Sem fetch de resultados futuros, sem leitura de audits numéricos como prova na UI, sem localStorage operacional.

## 7. Concorrência, locks e idempotência

N/A backend. Assessment docs-only. Futura montagem de ViewModel deve ser determinística a partir de fixture + constantes governadas.

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

Sem telemetria. Assessment validada por suite UX-R1 + governance validator nos artefatos I6L.

## 10. Operação

Não altera coleta, scheduler, host, validate, R3E gate, R4/R5 nem conclusões. A tela futura, se implementada, permanece explicativa e advisory (`nextSafeScientificAction` texto apenas).

## 11. Rollback

```text
ROLLBACK = revert assessment PR; restaurar NEXT se necessário
NEVER via R3E validate / future unseen / R4 / R5
```

## 12. Compatibilidade

- Consome padrões I2/I3/I5/I6B/I6C e telas I6E–I6K como referência de apresentação.
- Overview/Runs/Readiness/Host permanecem preservados.
- Rota recomendada alinha I5A/IA (`/experiments/r3e`); candidato `/research/r3e` não existe e não deve ser introduzido.
- UX-B9 permanece o backlog de produto; esta assessment autoriza somente o incremento I6L→implementação futura com condições.

## 13. Testes necessários

(Para a futura tarefa de implementação — não nesta assessment.)

```text
/experiments/r3e renders real explanatory screen
synthetic/governed notice visible
R3D NO_MEASURABLE_EDGE remains distinct from R3E pending future unseen
M0–M5 definitions render without metrics
DELTA_CANDLE explained as M5 − M4 without significance/economic claims
temporal/leakage/bootstrap/FDR explained qualitatively without fabricated numbers
future unseen validation clearly not executed
effect peeking false distinct from not reported
validation not executed distinct from failed
no trading recommendations / profitability language
no p-values/Sharpe/returns fabricated
Overview/Runs/Readiness/Host preserved
no visible fixture selector
axe + architecture boundary
```

## 14. Alternativas consideradas

| Alternativa | Decisão |
|-------------|--------|
| BLOCKED até ViewModel R3E existir em PR separado | REJECTED — ViewModel mínimo pode ser criado na tarefa de implementação sob condições |
| Autorizar rota `/research/r3e` | REJECTED — conflita com I5A/IA `/experiments/r3e` |
| Autorizar colar tabelas de `docs/audits/R3E_REAL_DATA_RESULTS.md` | REJECTED — risco de interpretação econômica / métricas |
| Autorizar execução de validate / future unseen | REJECTED — not authorized |
| Autorizar recomendações de trading | REJECTED — guardrails |
| ADJUSTMENT_REQUIRED só por falta de contrato UX-B3 R3E | REJECTED — UX-B9 + conditions suficientes com boundary estreito |
| AUTHORIZED sem ViewModel/fixture dedicado | REJECTED — fixture-backed boundary requires dedicated data surface |

## 15. Riscos

| Risco | Severidade | Mitigação |
|-------|------------|-----------|
| False edge claim | CRITICAL | Copy: EXPLORATORY_COMPLETE ≠ EDGE_PROVEN; no numeric edge tables |
| False approval / strategy claim | CRITICAL | ECONOMIC_INTERPRETATION_ALLOWED=false; no approval language |
| Invented metrics | CRITICAL | Forbid p/CI/Sharpe/returns unless already on approved VM as illustrative |
| Collapsing R3D and R3E conclusions | CRITICAL | Separate sections; R3D NO_MEASURABLE_EDGE ≠ R3E rejected |
| Premature scientific interpretation | HIGH | Explanatory definitions only; evidence vs interpretation vs future decision |
| Effect peeking / future result access | HIGH | No validate execution; no future result inspection |
| Fixture/live confusion | HIGH | Mandatory SyntheticOrGovernedDataNotice |
| Scope creep to R4/R5 unlock | HIGH | NO_R4_OR_R5_STATE_CHANGE |

## 16. Questões abertas

```text
NONE_BLOCKING
R3E_VIEWMODEL_SHAPE = to be defined in implementation task within authorized fields only
OPTIONAL_CONTRACT_NOTE = UX-B9 remains PLANNED; implementation may proceed under I6L conditions without rewriting UX-B3
```

## 17. Decisão arquitetural recomendada

Autorizar (em tarefa futura separada) um módulo de tela explicativa sob `web/src/screens/` (ex.: `r3e-experiment/`) que:

1. introduz um **R3eExperimentViewModel** mínimo (definições + códigos de estado governados; sem métricas fabricadas);
2. introduz fixture sintético dedicado (ex.: `r3e_current_state_illustrative`) e notice obrigatório;
3. registra rota **`/experiments/r3e`** e ativa o item de nav **R3E**;
4. explica hipótese, protocolo, M0–M5, `DELTA_CANDLE`, proteções temporais/leakage, bootstrap/FDR em linguagem simples + termos técnicos;
5. separa R3D (`NO_MEASURABLE_EDGE`) de R3E (`PENDING_FUTURE_UNSEEN_DATA`);
6. permanece read-only / explanatory-only, sem validação, sem effect peeking, sem recomendações, sem mudança científica.

## 18. Critérios para autorizar implementação

```text
1. This impact IMPACT_ASSESSMENT_STATUS = APPROVED
2. IMPLEMENTATION_AUTHORIZED = true (assessment docs)
3. DECISION = AUTHORIZED_WITH_CONDITIONS
4. I6K Host MERGED; NEXT was R3E authorization assessment
5. Separate human prompt must set R3E_EXPERIMENT_SCREEN_IMPLEMENTATION_AUTHORIZED=true
6. R3E_EXPERIMENT_SCREEN_MERGE_AUTHORIZED remains false until human merge
7. VALIDATION_EXECUTION / EFFECT_PEEKING / SCIENTIFIC_INTERPRETATION_CHANGE remain false
8. Dedicated explanatory ViewModel + fixture created in/before screen UI
9. Route is /experiments/r3e (not /research/r3e)
```

## Assessment dimensions

| Dimension | Result | Notes |
|-----------|--------|-------|
| R3E ViewModel readiness | ADJUSTMENT_REQUIRED_THEN_READY | No dedicated VM today; required in implementation |
| Fixture coverage | ADJUSTMENT_REQUIRED_THEN_READY | Overview gate strings insufficient alone |
| Experiment-purpose clarity | READY | Spec + B4 Experimentos language exist |
| R3D/R3E distinction safety | READY_WITH_CONDITIONS | Must keep conclusions separate on screen |
| M0–M5 explanatory readiness | READY | Definitions in R3E specification |
| DELTA_CANDLE semantic safety | READY_WITH_CONDITIONS | Definition only; no significance claim |
| Temporal-validation explanation | READY | Qualitative from protocol docs |
| Leakage-protection explanation | READY | Qualitative from protocol docs |
| Bootstrap/FDR explanation | READY_WITH_CONDITIONS | Qualitative only; no fabricated numbers |
| Future-unseen gate clarity | READY | `PENDING_FUTURE_UNSEEN_DATA` on Overview fixtures + PROJECT |
| Scientific-state safety | READY | Gate/R4/R5 codes available as strings |
| Known-vs-unknown separation | READY_WITH_CONDITIONS | Must disclose unknowns explicitly |
| Effect-peeking semantics | READY | Readiness VM `effectPeekingPerformed=false` |
| Validation-execution semantics | READY | Readiness VM `validationCommandExecuted=false` |
| Evidence-reference safety | READY | Text-only doc paths |
| Responsive / a11y | READY_WITH_CONDITIONS | Follow I6E–I6K patterns |
| Route readiness | READY_WITH_CONDITIONS | Reserved `/experiments/r3e`; nav planned inactive |
| False edge claim risk | HIGH_MITIGATED_BY_COPY_AND_BOUNDARY | |
| False approval claim risk | HIGH_MITIGATED_BY_GUARDRAILS | |
| Invented metric risk | HIGH_MITIGATED_BY_NO_FABRICATION | |
| Premature interpretation risk | HIGH_MITIGATED_BY_EXPLANATORY_ONLY | |
| Increment size / reviewability | READY | Screen-only + VM/fixture in one task is reviewable if narrow |

## Mandatory safety answers

1. **Is there a merged R3E-specific ViewModel, or must the screen compose existing governed ViewModels?** There is **no** dedicated R3E ViewModel. A future screen must **introduce** a minimal R3eExperimentViewModel (preferred) and may compose Overview/Readiness status fields (`scientificGate`, validation/effect-peeking booleans) — not invent metrics.
2. **Are current fixtures sufficient without inventing metrics?** **Not alone.** Current fixtures expose gate/R4/R5 strings and readiness flags only. A dedicated synthetic R3E fixture is required for explanatory sections.
3. **Can R3D’s NO_MEASURABLE_EDGE remain distinct from R3E’s pending future validation?** **Yes** — mandatory separate sections/copy; do not collapse conclusions.
4. **Can M0–M5 be explained accurately and concisely?** **Yes** — from frozen R3E specification definitions.
5. **Can DELTA_CANDLE = M5 − M4 be explained without claiming significance or economic value?** **Yes** — definitional only; `ECONOMIC_INTERPRETATION_ALLOWED=false`.
6. **Can temporal split, holdout and preprocessing leakage protections be explained from merged evidence?** **Yes** — qualitative protocol wording from governed specs; no fabricated holdout scores.
7. **Can bootstrap and FDR be explained without fabricated numerical results?** **Yes** — conceptual explanation only.
8. **Can the screen clearly state future unseen validation has not run?** **Yes** — `R3E_GATE=PENDING_FUTURE_UNSEEN_DATA`; `validationCommandExecuted=false`.
9. **Can the screen avoid effect peeking?** **Yes** — no validate/future-result access; show `effectPeekingPerformed=false` distinctly.
10. **Can the screen avoid trading recommendations and profitability language?** **Yes** — B4 scientific/economic guardrails; prohibited wording list.
11. **Exact implementation boundary?** See recommended boundary.
12. **Which scientific content must remain out of scope?** Fabricated metrics; future-unseen outcomes; economic usefulness claims; strategy approval; R4/R5 unlock; collapsing R3D/R3E; live audit tables as UI proof.
13. **Is a new dedicated R3E ViewModel required before screen implementation?** **Yes** — as a required pre-/in-task adjustment of the implementation increment (must land before or with the screen UI).
14. **Is a dedicated synthetic fixture required?** **Yes**.
15. **What route and navigation label are safest?** Route **`/experiments/r3e`**; nav label **`R3E`** (group **Experimentos**); page title **Experimento R3E**. Do **not** use `/research/r3e`.

## Authorization decision

```text
DECISION = AUTHORIZED_WITH_CONDITIONS
```

### Conditions

1. **R3E experiment screen only** — do not modify Overview/Runs/Readiness/Host.
2. **Fixture-backed** — dedicated synthetic R3E fixture; product posture matches `PENDING_FUTURE_UNSEEN_DATA`.
3. **Read-only / explanatory-only**.
4. **No visible fixture selector**.
5. **No real data / no future-unseen results inspection**.
6. **No validation execution / no effect peeking**.
7. **No trading recommendations / no profitability claims**.
8. **No scientific interpretation change / no R4 or R5 state change**.
9. **Dedicated R3eExperimentViewModel + fixture required** in the implementation task (definitions + governed status codes only).
10. **Route `/experiments/r3e` only** — reject `/research/r3e`.
11. **Keep R3D and R3E conclusions distinct** on screen.
12. **DELTA_CANDLE / M0–M5 / bootstrap / FDR** as definitions/concepts — never fabricated statistics.
13. **Mandatory SyntheticOrGovernedDataNotice** + approved wording / prohibited wording.
14. Separate human prompt must set `R3E_EXPERIMENT_SCREEN_IMPLEMENTATION_AUTHORIZED=true`; this assessment does not flip execution flags.

### Approved scientific wording (examples)

```text
R3D encerrou com NO_MEASURABLE_EDGE (R3_GATE = REJECTED_NO_MEASURABLE_EDGE_V1).
R3E permanece PENDING_FUTURE_UNSEEN_DATA — exploração concluída não prova edge.
DELTA_CANDLE = M5 − M4 descreve a contribuição incremental do padrão de candle (definição).
ECONOMIC_INTERPRETATION_ALLOWED = false.
Validação futura não vista ainda não foi executada.
Effect peeking não foi realizado.
R4 permanece BLOCKED; R5 NOT_STARTED.
```

### Prohibited wording / implications

```text
guaranteed profit / lucro garantido
approved strategy / estratégia aprovada
ready for real money / pronto para dinheiro real
future validation passed / validação futura aprovada
edge confirmed / edge comprovado
R4 unlocked / R5 started
trading recommendation / recomendação de trade
profitability / Sharpe / win rate as live proof
R3D and R3E collapsed into one rejection/approval statement
```

### Explicit out of scope

```text
REAL_DATA_INTEGRATION
FUTURE_UNSEEN_RESULT_INSPECTION
VALIDATION_EXECUTION
EFFECT_PEEKING
FABRICATED_PVALUES_CI_EFFECT_SIZES
FABRICATED_RETURNS_SHARPE_WINRATE_DRAWDOWN
TRADING_RECOMMENDATIONS
PROFITABILITY_CLAIMS
STRATEGY_APPROVAL
R4_UNLOCK
R5_START
SCIENTIFIC_INTERPRETATION_CHANGE
ROUTE_/research/r3e
OVERVIEW_RUNS_READINESS_HOST_CHANGES
AUTHENTICATION
PERMISSIONS
FINANCIAL_EXECUTION
```

### Required pre-implementation adjustments

```text
1. Add minimal R3eExperimentViewModel (explanatory fields only)
2. Add dedicated synthetic R3E fixture scenario
3. Register /experiments/r3e and activate nav item R3E
4. Do not introduce /research/r3e
5. Wire SyntheticOrGovernedDataNotice + R3D/R3E distinction + prohibited-language tests
```

## Decisão

```text
I6L_DECISION = AUTHORIZED_WITH_CONDITIONS
IMPLEMENTATION_EXECUTION_AUTHORIZED = false
R3E_EXPERIMENT_SCREEN_IMPLEMENTATION_AUTHORIZED = false
VALIDATION_EXECUTION_AUTHORIZED = false
EFFECT_PEEKING_AUTHORIZED = false
SCIENTIFIC_INTERPRETATION_CHANGE_AUTHORIZED = false
NEXT_RECOMMENDED_TASK = I6_R3E_EXPERIMENT_SCREEN_IMPLEMENTATION
NEXT_ITEM = I6_R3E_EXPERIMENT_SCREEN_SEPARATE_IMPLEMENTATION_TASK
```
