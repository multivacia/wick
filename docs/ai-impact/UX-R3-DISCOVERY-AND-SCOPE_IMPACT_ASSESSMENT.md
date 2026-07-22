# UX-R3-DISCOVERY-AND-SCOPE — Análise de Impacto

## Metadados

```text
RELEASE = UX-R3
RELEASE_NAME = WICK RESEARCH OPERATIONS R3
TASK_ID = UX-R3-DISCOVERY-AND-SCOPE-ASSESSMENT-001
TITLE = UX-R3 Discovery and Scope Assessment
PHASE = DISCOVERY_AND_SCOPE_ASSESSMENT
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
ASSESSMENT_ONLY = true
ASSESSMENT_AUTHORIZED = true
UX_R3_STATUS = NOT_STARTED
UX_R3_SCOPE_AUTHORIZED = false
UX_R3_IMPLEMENTATION_AUTHORIZED = false
PRODUCT_CODE_AUTHORIZED = false
BACKEND_IMPLEMENTATION_AUTHORIZED = false
NEW_ROUTE_AUTHORIZED = false
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
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false

PR122_STATUS = MERGED
PR124_STATUS = MERGED
PR125_STATUS = MERGED
PR125_MERGE_COMMIT = 2fb2bb9da35f70083972bd7c6da64c72055c9a0e
MAIN_TIP = 2fb2bb9da35f70083972bd7c6da64c72055c9a0e

UX_R2_RELEASE_STATUS = CLOSED
UX_R2_RELEASE_ACCEPTANCE_STATUS = ACCEPTED
UX_R2_RELEASE_SCOPE = FIXTURE_BACKED_EVIDENCE_AND_AUDIT_EXPLORATION

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

REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 2fb2bb9da35f70083972bd7c6da64c72055c9a0e
ANALYZED_AT = 2026-07-22T00:12:00Z
ANALYZED_BY = cursor-agent
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION

UX_R3_RECOMMENDED_DIRECTION = E_COLLECTION_MONITORING_AND_DATA_QUALITY
UX_R3_FIRST_INCREMENT = UX_R3_I1_COLLECTION_DATA_QUALITY_AUTHORIZATION_ASSESSMENT
NEXT_RECOMMENDED_TASK = UX_R3_FIRST_INCREMENT_AUTHORIZATION_ASSESSMENT
NEXT_ITEM = UX_R3_I1_COLLECTION_DATA_QUALITY_AUTHORIZATION_SEPARATE_ASSESSMENT
```

G1 note: **SCOPE_RECOMMENDED** means only that a safe UX-R3 direction and first increment are identified for a **separate** authorization assessment. It does **not** authorize UX-R3 product code, mark UX-R3 started, real data, host/scheduler actions, validation, effect peeking, scientific reinterpretation, R4/R5, or parallel work.

## MANDATORY_CONSTRAINTS

```text
ASSESSMENT_ONLY = true
NO_PRODUCT_CODE_CHANGES = true
NO_UX_R3_STARTED = true
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

UX-R1 and UX-R2 are closed within fixture-backed boundaries. Active screens cover Overview, Runs, Readiness, Host/Scheduler, R3E, and Evidence Explorer. The live scientific/operational constraint is still **collection in progress / readiness NOT_READY (`WINDOW_DAYS_INSUFFICIENT`)**, with R3E gate pending future-unseen data. Readiness explicitly discloses that collection-health metrics are **not** on its ViewModel, and planned nav item **Dados Coletados** remains inactive.

Safest high-value UX-R3 direction: **E — Collection Monitoring and Data Quality**, starting with a **separate authorization assessment** for a fixture-backed, read-only collection data-quality surface (activate planned Dados Coletados). Remain fixture-backed. Do not integrate real data, peek future-unseen results, activate host/scheduler, or unlock R4/R5.

## 1. Objetivo

Determinar o próximo release UX coerente após UX-R2 **sem implementar**, respondendo às perguntas de descoberta e escolhendo exatamente uma direção e um primeiro incremento.

## 2. Baseline de capacidade UX (merged)

| Surface | Status | Notes |
|---------|--------|-------|
| Overview | MERGED | Operational state + evidence links |
| Runs | MERGED | Collection run list (fixture) |
| Readiness | MERGED | Gate readiness; collection-health **absent by design** |
| Host/Scheduler | MERGED | Deferred/blocked semantics |
| R3E Experiment | MERGED | Explanatory; gate pending |
| Evidence Explorer | MERGED | Catalog history, provenance, cross-nav, fixture closure |

**Strengths:** coherent fixture architecture; strong semantic inequalities; evidence↔screen cross-nav; governed acceptance wording.

**Gaps:** no dedicated collection-quality surface; Dados Coletados inactive; hypothesis→experiment registry incomplete; gate decision workflow absent; research planning thin; duplicated status fragments across Overview/Runs/Readiness/R3E.

**Must not expand yet:** real-data adapters; future-unseen result surfaces; host activation; approvals that imply scientific unlock; strategy promotion.

## 3. Candidate evaluation

Disposition legend: recommended / defer / blocked / rejected.

| ID | Candidate | User | Sci | Gov | Data dep | Host dep | Real data | Backend | Security | Peek risk | False confidence | Vision fit | Maturity | Size | Disposition |
|----|-----------|------|-----|-----|----------|----------|-----------|---------|----------|-----------|------------------|------------|----------|------|-------------|
| A | EXPERIMENT_REGISTRY_AND_COMPARISON | H | M | M | L | L | No | Optional later | M | M | M | H | OK | M | DEFER_TO_LATER_UX_RELEASE |
| B | SCIENTIFIC_GATE_AND_DECISION_WORKFLOW | H | H | H | M | L | No | Optional | H | H | H | H | RISKY | M | DEFER_TO_LATER_UX_RELEASE |
| C | RESEARCH_HYPOTHESIS_AND_EXPERIMENT_PLANNING | H | M | L | L | L | No | No | L | L | M | H | OK | M | DEFER_TO_LATER_UX_RELEASE |
| D | RELEASE_AND_GOVERNANCE_CENTER | M | L | H | L | L | No | No | M | L | M | M | OK | S | REJECTED_AS_REDUNDANT |
| E | COLLECTION_MONITORING_AND_DATA_QUALITY | H | M | M | Aligns IN_PROGRESS | L | No for I1 | No for I1 | M | L if no FU | M | H | OK | M | **RECOMMENDED_FOR_UX_R3** |
| F | CONTROLLED_REAL_DATA_READ_INTEGRATION | H | H | H | H | L | Yes | Yes | H | H | H | H | EARLY | L | DEFER_TO_LATER_UX_RELEASE |
| G | R3E_FUTURE_UNSEEN_PROGRESS_AND_EVENTUAL_RESULT_SURFACES | H | H | M | H | L | Maybe | Maybe | H | H | H | H | BLOCKED | M | BLOCKED_BY_FUTURE_UNSEEN_GATE |
| H | HOST_AND_SCHEDULER_OPERATIONAL_WORKFLOW | M | L | M | L | H | Maybe | Maybe | H | L | H | M | BLOCKED | M | BLOCKED_BY_OPERATIONAL_DEPENDENCY |
| I | STRATEGY_READINESS_AND_CONTROLLED_PROMOTION | H | H | H | H | M | Yes | Yes | H | H | H | H | BLOCKED | L | BLOCKED_BY_FUTURE_UNSEEN_GATE |
| J | NO_NEW_UX_RELEASE_UNTIL_R3E_DATA_GATE_CHANGES | L | L | L | H | L | No | No | L | L | L | L | N/A | — | REJECTED_AS_LOW_VALUE |

### Disposition notes

- **E recommended:** current blocker is window/collection progress; Readiness already admits collection-health gap; planned nav exists; fixture-backed surface can teach quality dimensions without validate/peek.
- **D rejected redundant:** Evidence Explorer already covers release/gate/evidence governance for UX-R2 scope.
- **G/I blocked:** require future-unseen results or R4-class promotion semantics.
- **H blocked:** host discovery deferred; scheduler blocked; operational debt open.
- **F deferred:** valuable later; not least-risk posture for UX-R3 start.
- **A/B/C deferred:** strong later themes after collection-quality coherence; B especially high false-confidence risk if framed as unlock workflow.
- **J rejected:** waiting idle forgoes safe fixture value during `COLLECTION=IN_PROGRESS`.

## 4. Strategic decision

```text
UX_R3_RECOMMENDED_DIRECTION = E_COLLECTION_MONITORING_AND_DATA_QUALITY

UX_R3_FINAL_PRODUCT_OBJECTIVE =
  Give Gustavo a governed, fixture-backed view of future-collection progress and
  data-quality posture so he can understand what is known/unknown about the
  collection window without implying readiness approval, validation complete,
  or operational activation.

UX_R3_PRIMARY_USER_OUTCOME =
  Open Dados Coletados → inspect illustrative completeness/gaps/duplicates/cutoff/
  series counts and quality notices → relate to Runs/Readiness/Evidence safely →
  leave knowing COLLECTION_IN_PROGRESS ≠ READY and quality ≠ scientific approval.

UX_R3_RELEASE_BOUNDARY =
  Fixture-backed read-only collection monitoring and data-quality exploration;
  activate planned Dados Coletados; no backend; no real series payloads; no
  future-unseen result tables; no collection start/stop; no host/scheduler actions;
  no R4/R5.

UX_R3_EXPLICIT_OUT_OF_SCOPE =
  real-data adapters; runtime repo/FS; validate execution; effect peeking;
  future-unseen result inspection; host discovery; scheduler activation;
  approvals unlock; experiment registry; strategy promotion; trading claims.

UX_R3_DEFERRED_BACKLOG =
  A experiment registry/comparison;
  B scientific gate decision workflow;
  C hypothesis/experiment planning;
  F controlled real-data read integration;
  G future-unseen progress/result surfaces (blocked until gate changes);
  H host/scheduler operational workflow;
  I strategy readiness/promotion.

UX_R3_FIRST_INCREMENT =
  UX_R3_I1_COLLECTION_DATA_QUALITY_AUTHORIZATION_ASSESSMENT

UX_R3_FIRST_INCREMENT_RISK = MEDIUM
UX_R3_FIRST_INCREMENT_AUTHORIZATION_PREREQUISITE =
  Separate human-authorized authorization assessment PR after this discovery merges;
  implementation remains unauthorized until a further implementation prompt.
```

## 5. Real-data boundary assessment

| Posture | Benefit | Arch | Security | Freshness | Sci semantics | Peek | Ops coupling | Test burden | Reversibility | Human inputs | Rec |
|---------|---------|------|----------|-----------|---------------|------|--------------|-------------|---------------|--------------|-----|
| FIXTURE_BACKED_READ_ONLY | Safe meaningful UX now | Low | Low | Illustrative | Controllable | Low | None | Low | High | None | **DEFAULT for UX-R3** |
| CURATED_BUILD_TIME_MANIFEST | Fresher curated snapshot | Med | Med path/allowlist | Build-time lag | Needs careful labels | Med | Low | Med | Med | Manifest curation rules | Later assessment only |
| CONTROLLED_READ_ONLY_BACKEND_ADAPTER | Live ops status | High | High | Live | High misread risk | High | Med | High | Med | API contract + authz | Later assessment only |
| CONTROLLED_REAL_DATA_READ_INTEGRATION | True series/quality | Very high | Very high | Live | Very high | Very high | High | Very high | Low | Data contract + privacy | Deferred; not UX-R3 |

```text
REAL_DATA_POSTURE_RECOMMENDATION = FIXTURE_BACKED_READ_ONLY
BACKEND_POSTURE_RECOMMENDATION = NO_BACKEND_FOR_UX_R3
FUTURE_UNSEEN_POSTURE_RECOMMENDATION = NO_FUTURE_UNSEEN_RESULTS_SURFACES
OPERATIONAL_POSTURE_RECOMMENDATION = NO_HOST_SCHEDULER_ACTIONS
```

None of the non-fixture postures are authorized by this assessment.

## 6. Scientific / operational constraints preserved

```text
EVIDENCE != SCIENTIFIC_APPROVAL
HISTORICAL != FUTURE_UNSEEN
EXPLORATORY != CONFIRMATORY
PENDING != FAILED
NO_MEASURABLE_EDGE_R3D != R3E_REJECTED
COLLECTION_IN_PROGRESS != VALIDATION_READY
READINESS_NOT_READY != OPERATIONAL_FAULT
QUALITY_METRICS != STRATEGY_APPROVAL
WINDOW_DAYS_INSUFFICIENT != COLLECTION_FAULT
```

Operational assumptions not made: real host discovered; scheduler active; credentials; automatic collection proven; R4 unlocked; R5 started.

## 7. Process model (UX-R2 lessons)

UX-R2 single-execution succeeded **with conditions** for a **frozen remaining** bounded product slice. That does **not** make single-execution default for discovery-shaped releases.

```text
PROCESS_MODEL_RECOMMENDATION = FULL_INCREMENTAL_FLOW
UX_R3_PROCESS_MODEL = FULL_INCREMENTAL_FLOW

WHEN_SINGLE_EXECUTION_IS_ALLOWED =
  Only after a later integral plan freezes a remaining multi-increment list with
  mandatory checkpoints + one final independent review + one final human validation,
  and scope excludes backend/scientific/operational mutation.

WHEN_INCREMENTAL_FLOW_IS_REQUIRED =
  Discovery → first-increment authorization → implementation → review → merge
  for each increment while scope is still being proved; any new route/ViewModel/
  fixture family; any security-sensitive surface.

MANDATORY_CHECKPOINTS =
  architecture; increment acceptance; integration; regression; security;
  accessibility; governance; final independent review before merge of product PRs.

MAXIMUM_RELEASE_BOUNDARY =
  Fixture-backed collection monitoring/data-quality only; no real data; no FU
  results; no ops actions; no R4/R5.

STOP_CONDITIONS =
  request for real-data/backend/FU results/ops actions; scientific reinterpretation;
  R4 unlock implication; scope expansion beyond frozen list; failed checkpoint;
  unresolved security finding.
```

## 8. Proposed release shape (indicative; not frozen)

```text
I1 = UX_R3_I1_COLLECTION_DATA_QUALITY_AUTHORIZATION_ASSESSMENT (docs)
I2 = fixture-backed Dados Coletados screen foundation (after I1 auth+impl prompts)
I3 = quality dimensions + notices (completeness/gaps/duplicates/cutoff) fixture-only
I4 = cross-links from Runs/Readiness/Overview/Evidence
I5 = fixture acceptance / UX-R3 closure stamp
```

Order I1→I2→I3→I4→I5. Data posture all fixture-backed until a separate later assessment. Exact freeze requires a later integral plan if continuous execution is desired.

## 9. Architecture impact (assessment-level)

| Area | Impact |
|------|--------|
| Routes | Candidate activate `/future-collection/collected-data` or equivalent (I1 decides) |
| Navigation | Activate planned Dados Coletados |
| ViewModels | New collection-quality VM; do not overload Readiness VM |
| Fixtures | New curated fixture family |
| Backend/DB | None for UX-R3 |
| Security | Path allowlists if sourcePath display; no downloads/MD/HTML |
| Tests | Architecture boundaries + semantic inequalities + a11y |
| Governance | Standard impact/spec/review/handoff per increment |

## 10. Security and trust

| Risk | Assessment for recommended direction |
|------|--------------------------------------|
| Path traversal / repo disclosure | Keep sourcePath display-only; no FS reads |
| Secret exposure | None expected in fixtures |
| Unsafe rendering / external links | Forbid MD/HTML/external href |
| Real-data / FU leakage | Fixture-only; no FU payloads |
| Effect peeking | Forbidden; no validate |
| Fabricated completeness | Disclose illustrative; no completeness-as-approval |
| Stale-data misunderstanding | Explicit fixture/staleness notices |
| R3D/R3E conflation | Preserve distinctions in copy/tests |
| False strategy / production readiness | Explicit inequalities |
| Unsafe ops action | No start/stop/collect/activate controls |

## 11. Discovery questions answered

1. **User problem?** Understand collection progress/quality while waiting for sufficient future window, without mistaking progress for scientific approval.
2. **Why next safest/highest value?** Aligns with live `COLLECTION=IN_PROGRESS` / `WINDOW_DAYS_INSUFFICIENT`; closes documented Readiness gap; activates planned nav; avoids blocked scientific/ops gates.
3. **Deliverable without violating gates?** Fixture-backed Dados Coletados quality exploration.
4. **Must remain deferred?** Real data, FU results, host/scheduler workflows, approvals unlock, experiment registry, strategy promotion.
5. **Single-branch model?** Not by default — full incremental flow; single-execution only if later frozen with conditions.
6. **Smallest coherent first increment?** Separate authorization assessment for collection data-quality surface.

## 12. Decisão

```text
DECISION = SCOPE_RECOMMENDED
IMPACT_ASSESSMENT_STATUS = APPROVED
UX_R3_RECOMMENDED_DIRECTION = E_COLLECTION_MONITORING_AND_DATA_QUALITY
UX_R3_FIRST_INCREMENT = UX_R3_I1_COLLECTION_DATA_QUALITY_AUTHORIZATION_ASSESSMENT
UX_R3_IMPLEMENTATION_POSTURE = FIXTURE_BACKED_READ_ONLY
UX_R3_PROCESS_MODEL = FULL_INCREMENTAL_FLOW
UX_R3_STATUS = NOT_STARTED
UX_R3_SCOPE_AUTHORIZED = false
UX_R3_IMPLEMENTATION_AUTHORIZED = false
PRODUCT_CODE_AUTHORIZED = false
NEXT_RECOMMENDED_TASK = UX_R3_FIRST_INCREMENT_AUTHORIZATION_ASSESSMENT
```

## Official operational wording preserved

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```
