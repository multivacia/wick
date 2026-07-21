# UX-R2-DISCOVERY-AND-SCOPE — Análise de Impacto

## Metadados

```text
RELEASE = UX-R2
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE R2
TASK_ID = UX-R2-DISCOVERY-AND-SCOPE-ASSESSMENT-001
TITLE = UX-R2 Discovery and Scope Assessment
PHASE = DISCOVERY_AND_SCOPE_ASSESSMENT
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
ASSESSMENT_ONLY = true
ASSESSMENT_AUTHORIZED = true
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
DECISION = SCOPE_RECOMMENDED
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false

PR110_STATUS = MERGED
PR110_MERGE_COMMIT = df5fe40dff47269811279f5010df1253696078d8
PR111_STATUS = MERGED
PR111_MERGE_COMMIT = 441c076365ae63f2c827328efb77f10aa54b1a3f
MAIN_TIP = 441c076365ae63f2c827328efb77f10aa54b1a3f

UX_R1_RELEASE_STATUS = CLOSED
UX_R1_RELEASE_ACCEPTANCE_STATUS = ACCEPTED
UX_R1_RELEASE_SCOPE = FIXTURE_BACKED_READ_ONLY
UX_R1_RELEASE_ACCEPTANCE_WORDING = UX-R1 fixture-backed read-only scope is complete and governed.

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
BASE_SHA = 441c076365ae63f2c827328efb77f10aa54b1a3f
ANALYZED_AT = 2026-07-21T13:05:33Z
ANALYZED_BY = cursor-agent
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION

RECOMMENDED_DIRECTION = D_EVIDENCE_AND_AUDIT_EXPLORER
RECOMMENDED_FIRST_INCREMENT = UX_R2_I1_EVIDENCE_EXPLORER_AUTHORIZATION_ASSESSMENT
NEXT_RECOMMENDED_TASK = UX_R2_I1_EVIDENCE_EXPLORER_AUTHORIZATION_ASSESSMENT
NEXT_ITEM = UX_R2_I1_EVIDENCE_EXPLORER_AUTHORIZATION_SEPARATE_ASSESSMENT
```

G1 note: **SCOPE_RECOMMENDED** means only that a safe UX-R2 direction and first increment are identified for a **separate** authorization assessment. It does **not** authorize UX-R2 product code, screens, adapters, real data, host discovery, scheduler activation, validation, effect peeking, scientific reinterpretation, R4/R5, or parallel work.

## MANDATORY_CONSTRAINTS

```text
ASSESSMENT_ONLY = true
NO_PRODUCT_CODE_CHANGES = true
NO_NEW_SCREENS = true
NO_REAL_DATA = true
NO_REAL_HOST_DISCOVERY = true
NO_CREDENTIALS = true
NO_OPERATIONAL_COMMANDS = true
NO_SCHEDULER_ACTIVATION = true
NO_COLLECTION_ACTIONS = true
NO_VALIDATION_EXECUTION = true
NO_EFFECT_PEEKING = true
NO_FUTURE_UNSEEN_RESULTS = true
NO_TRADING_RECOMMENDATIONS = true
NO_PROFITABILITY_CLAIMS = true
NO_SCIENTIFIC_INTERPRETATION_CHANGE = true
NO_R4_OR_R5_STATE_CHANGE = true
NO_UX_R2_IMPLEMENTATION = true
PARALLEL_TASKS_ALLOWED = false
```

## SUMMARY

UX-R1 is **CLOSED / ACCEPTED** as fixture-backed read-only (`df5fe40` stamp; post-merge `441c076`). Five illustrative screens exist; planned nav still includes inactive **Evidências**. Operational truth remains host deferred, scheduler blocked, collection in progress, readiness NOT_READY (`WINDOW_DAYS_INSUFFICIENT`), R3E gate pending future-unseen, R4 blocked. No `ops_ui_index` adapter exists; architecture tests forbid network/ops imports in screens.

Safest high-value UX-R2 direction: **D — Evidence and Audit Explorer**, starting with a **separate authorization assessment** for a fixture-backed, read-only Evidence Explorer (activate planned Evidências nav). Defer governed real-data reads, host/scheduler workflows, gate-approval workflows, and future-unseen readiness progression until later gated increments.

## 1. Objetivo

Definir o escopo mais seguro e valioso para UX-R2 **sem implementar**, respondendo explicitamente às perguntas de descoberta e escolhendo exatamente um primeiro incremento recomendado.

## 2. Contexto técnico

- UX-R1 closed: routes `/overview`, `/future-collection/runs`, `/future-collection/readiness`, `/operations/host-scheduler`, `/experiments/r3e` — all fixture-backed.
- Planned inactive nav: Dados Coletados, Backups, Incidentes, Backlog, Aprovações, **Evidências**.
- R3E evidence exists under `docs/audits/`, `reports/r3e*`, `reports/r3e_future_unseen/*` — UI must not peek future-unseen result payloads.
- Adapter path `ops_ui_index_v1.json` recommended historically in B3 but never built; prior “I6D adapter” remained BLOCKED (label collision with later Overview I6D).
- Open non-UX drafts #37/#38 (R3E B5-P1) do not block UX-R2 discovery.

## 3. Candidate evaluation matrix

Scoring legend: H/M/L = high/medium/low relative value or risk. Compatibility: OK / RISKY / BLOCKED.

| ID | Candidate | Product | Scientific | Ops | Dep ready | Data avail | Arch ready | Cred risk | Peek/false-conf | Activation | Complexity | Testable | Auditable | Reversible | Increment | Human input | Ext deps | R3E gate compat | Host deferred compat |
|----|-----------|---------|------------|-----|-----------|------------|------------|-----------|-----------------|------------|------------|----------|-----------|------------|-----------|-------------|---------|-----------------|----------------------|
| A | Governed real-data read | H | M | H | L | M | L | H | H | M | H | M | H | M | L | H | M | RISKY | OK if local reports only |
| B | Collection monitoring | H | L | H | L | M | L | M | H | M | M | M | M | M | M | M | M | RISKY | OK if no host cmds |
| C | Experiment registry | M | H | L | H | H (fixtures) | H | L | M | L | M | H | H | H | M | L | L | OK | OK |
| D | Evidence/audit explorer | H | H | M | H | H (fixtures first) | H | L | L | L | M | H | H | H | H | L | L | OK | OK |
| E | Scientific gate workflow | M | H | L | L | L | M | L | H | L | H | M | H | L | L | H | L | BLOCKED | OK |
| F | Host/scheduler workflow | H | L | H | L | L | L | H | M | H | H | M | M | L | L | H | H | OK | BLOCKED |
| G | FU readiness progression | M | H | M | L | L (window) | M | L | H | M | M | M | M | M | M | M | L | BLOCKED | OK |
| H | Release/governance center | M | M | L | H | H | H | L | L | L | L | H | H | H | H | L | L | OK | OK |

## 4. Explicit discovery answers

1. **Primary user problem:** After UX-R1, operators can view illustrative status screens but cannot browse a governed **evidence surface** that separates recorded evidence, interpretation language, and operational controls — without jumping into host activation, live ops adapters, validation, or future-unseen peeking.
2. **Highest safe value:** **D — Evidence and Audit Explorer** (with light optional overlap of H for release/gate history as evidence records).
3. **Require real host details:** **F** primarily; parts of **A/B** if they bind to host paths/credentials.
4. **Blocked by insufficient future-unseen data:** **G** (window insufficient); **E** for final gate decisions; truthful end-to-end **B** completeness claims.
5. **Require real-data adapters:** **A**, **B**, and later phases of **D/H** if reading live report trees (not first fixture-backed increment).
6. **Effect-peeking / false-approval risk:** **E**, **G**, careless **A/B** consuming `reports/r3e_future_unseen` result payloads or implying validate/gate advancement.
7. **Best separates evidence / interpretation / operation:** **D** (and **H**).
8. **Human inputs / external dependencies for recommended path:** Human authorization of I1 assessment then implementation tasks; no external host/provider dependency for fixture-backed Evidence Explorer. Later governed static-audit read may need human approval of allowlisted artifact classes.
9. **Must host discovery happen now?** **No.** Preserve `HOST_DISCOVERY = DEFERRED`.
10. **Data posture for UX-R2 start:** Remain **fixture-backed** for first increment; optional later **hybrid** via allowlisted governed read of static audit/governance artifacts (not live host ops; not future-unseen result payloads). Full operational real-data (**A**) is a later gated direction, not I1.
11. **Exact first increment:** `UX_R2_I1_EVIDENCE_EXPLORER_AUTHORIZATION_ASSESSMENT` — docs-only authorization assessment for a fixture-backed, read-only Evidence Explorer screen (planned nav **Evidências**), with dedicated ViewModel+fixture, synthetic disclosure, no adapters, no real data, no ops controls. Implementation remains unauthorized until that assessment and a later human implementation prompt.
12. **Explicit out of scope (UX-R2 discovery and recommended I1):** product code now; real-data adapters; host discovery; scheduler activation; collection/validate commands; future-unseen result inspection; trading recommendations; R4 unlock; R5 start; Approvals workflow; Host activation UI; live collection control plane.
13. **Required pre-implementation gates:** (a) this discovery assessment MERGED; (b) I1 Evidence Explorer authorization impact+review APPROVED; (c) separate human implementation authorization; (d) any later real-data/static-audit adapter requires its own HIGH-risk impact assessment and security review; (e) host/scheduler remain separately gated.
14. **Eventual UX-R2 closure criteria (provisional):** Evidence Explorer (and any authorized follow-on increments) delivered within declared boundary; no unauthorized real-data/ops/scientific state change; architecture boundary tests green; acceptance wording scoped (not production/trading ready); R3E/R4/R5 posture unchanged unless separately authorized outside UX-R2.

## 5. Recommended release boundary (I1 target, not authorized yet)

```text
EVIDENCE_EXPLORER_SCREEN_ONLY
FIXTURE_BACKED
READ_ONLY
NO_VISIBLE_FIXTURE_SELECTOR
NO_REAL_DATA
NO_REAL_HOST_DISCOVERY
NO_CREDENTIALS
NO_OPERATIONAL_COMMANDS
NO_SCHEDULER_ACTIVATION
NO_COLLECTION_ACTIONS
NO_VALIDATION_EXECUTION
NO_EFFECT_PEEKING
NO_FUTURE_UNSEEN_RESULT_PAYLOADS
NO_TRADING_RECOMMENDATIONS
NO_PROFITABILITY_CLAIMS
NO_SCIENTIFIC_INTERPRETATION_CHANGE
NO_R4_OR_R5_STATE_CHANGE
NO_APPROVALS_WORKFLOW
NO_HOST_ACTIVATION_UI
```

Suggested route (to confirm in I1 auth): `/governance/evidence` (or IA-aligned Evidências path). Nav: activate planned **Evidências** only.

## 6. Accepted risks

```text
ACCEPTED_RISKS =
  FIXTURE_ILLUSTRATIVE_ONLY_AGAIN_FOR_I1;
  OPERATORS_MAY_WANT_LIVE_DATA_SOONER;
  PLANNED_NAV_ITEMS_REMAIN_INACTIVE;
  STALE_UX_R1_SPEC_BACKLOG_STRINGS_UNRELATED
```

## 7. Blocking risks (for other candidates / later increments)

```text
BLOCKING_RISKS =
  HOST_DISCOVERY_STILL_DEFERRED_BLOCKS_F;
  WINDOW_DAYS_INSUFFICIENT_BLOCKS_G_AND_FINAL_GATE_UI;
  FUTURE_UNSEEN_PEEKING_BLOCKS_CARELESS_A_B_E;
  FALSE_APPROVAL_UI_BLOCKS_E;
  NO_OPS_UI_INDEX_ADAPTER_BLOCKS_FULL_A_B_NOW
```

## 8. Scientific and operational truth (unchanged)

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

Official wording preserved:

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```

## 9. Arquivos desta tarefa

```text
docs/ai-impact/UX-R2-DISCOVERY-AND-SCOPE_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R2-DISCOVERY-AND-SCOPE_SPEC.md
docs/ai-reviews/UX-R2-DISCOVERY-AND-SCOPE_REVIEW.md
reports/ai-implementation/UX-R2-DISCOVERY-AND-SCOPE_HANDOFF.md
docs/PROJECT.md
```

## 10. Decisão

```text
DECISION = SCOPE_RECOMMENDED
RECOMMENDED_DIRECTION = D_EVIDENCE_AND_AUDIT_EXPLORER
RECOMMENDED_FIRST_INCREMENT = UX_R2_I1_EVIDENCE_EXPLORER_AUTHORIZATION_ASSESSMENT
UX_R2_IMPLEMENTATION_AUTHORIZED = false
```
