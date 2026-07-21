# UX-R2-I1-EVIDENCE-EXPLORER-IMPLEMENTATION — Análise de Impacto

## Metadados

```text
RELEASE = UX-R2
RELEASE_NAME = WICK EVIDENCE AND AUDIT EXPLORER (direction)
BACKLOG_ITEM = UX-R2-I1
PARENT_TASK = EVIDENCE-EXPLORER-AUTHORIZATION-ASSESSMENT-001
TASK_ID = EVIDENCE-EXPLORER-IMPLEMENTATION-001
TITLE = Evidence Explorer Implementation
INCREMENT = I1
PHASE = IMPLEMENTATION
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
UX_R2_I1_IMPLEMENTATION_AUTHORIZED = true
EVIDENCE_EXPLORER_IMPLEMENTATION_AUTHORIZED = true
PRODUCT_CODE_AUTHORIZED = true
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = true
VIEWMODEL_IMPLEMENTATION_AUTHORIZED = true
FIXTURE_IMPLEMENTATION_AUTHORIZED = true
EVIDENCE_EXPLORER_MERGE_AUTHORIZED = false
REAL_DATA_INTEGRATION_AUTHORIZED = false
REPOSITORY_FILE_READ_INTEGRATION_AUTHORIZED = false
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
SCIENTIFIC_CONCLUSION = UNCHANGED
R3D_RESULT = NO_MEASURABLE_EDGE
R3E_STATUS = EXPLORATORY_COMPLETE_PENDING_FUTURE_UNSEEN_DATA
R3E_SCIENTIFIC_STATE_CHANGE = false
ECONOMIC_INTERPRETATION_ALLOWED = false
PR114_STATUS = MERGED
PR114_MERGE_COMMIT = 3be8920ff914df7215c5175047025a1e77ba7879
PR115_STATUS = MERGED
PR115_MERGE_COMMIT = 7cc6d54e0e4debe672167bea18cf6410cff2f25d
I1_AUTH_DECISION = AUTHORIZED_WITH_CONDITIONS
I1_RECOMMENDED_IMPLEMENTATION_POSTURE = A_STATIC_FIXTURE_BACKED_EVIDENCE_CATALOG
I1_RECOMMENDED_IMPLEMENTATION_BOUNDARY = EVIDENCE_EXPLORER_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; CURATED_MANIFEST_ONLY; LIST_AND_DETAIL; NO_RUNTIME_REPOSITORY_ACCESS; NO_REAL_DATA; NO_FUTURE_UNSEEN_RESULTS
FIXTURE_ID = evidence_catalog_current_state_illustrative
ROUTE = /governance/evidence
SCREEN = Evidências
NAV_LABEL = Evidências
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 7cc6d54e0e4debe672167bea18cf6410cff2f25d
FINAL_CANDIDATE_HEAD = PENDING_COMMIT
CONTENT_REVIEWED_THROUGH_HEAD = PENDING_COMMIT
POST_REVIEW_NORMATIVE_CHANGES = 0
ANALYZED_AT = 2026-07-21T16:00:00Z
ANALYZED_BY = cursor-agent
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTHORIZATION_DECISION = HUMAN_AUTHORIZED_FOR_THIS_TASK
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
FRONTEND_LOCATION = web/
```

G1 note: authorization covers **only** the read-only fixture-backed Evidence Explorer screen (`/governance/evidence`) with a dedicated ViewModel and curated static catalog fixture. It does **not** authorize runtime repository/filesystem access, real data, future-unseen result payloads, validation execution, effect peeking, downloads, Markdown/HTML rendering, host discovery, scheduler activation, or R4/R5 state changes. Existing UX-R1 screens remain preserved. Merge remains blocked until separate human authorization.

## MANDATORY_CONSTRAINTS

```text
READ_ONLY = true
FIXTURE_BACKED = true
CURATED_MANIFEST_ONLY = true
LIST_AND_DETAIL = true
FIXTURE_ID = evidence_catalog_current_state_illustrative
NO_VISIBLE_FIXTURE_SELECTOR = true
NO_RUNTIME_REPOSITORY_ACCESS = true
NO_RAW_FILESYSTEM_ACCESS = true
NO_REAL_DATA = true
NO_FUTURE_UNSEEN_RESULTS = true
NO_VALIDATION_EXECUTION = true
NO_EFFECT_PEEKING = true
NO_FILE_DOWNLOAD = true
NO_MARKDOWN_RENDERING = true
NO_HTML_RENDERING = true
NO_DANGEROUSLY_SET_INNER_HTML = true
NO_EXTERNAL_LINKS = true
SOURCE_PATH_DISPLAY_ONLY = true
NO_NETWORK_CLIENTS = true
NO_BACKEND_API = true
NO_EXTRA_RUNTIME_OR_DEV_DEPENDENCIES = true
TOKEN_ONLY_STYLING = true
REUSE_I3_PRIMITIVES = true
DEDICATED_EVIDENCE_VIEWMODEL_REQUIRED = true
DEDICATED_CURATED_FIXTURE_REQUIRED = true
PRESERVE_OVERVIEW_SCREEN = true
PRESERVE_RUNS_SCREEN = true
PRESERVE_READINESS_SCREEN = true
PRESERVE_HOST_SCHEDULER_SCREEN = true
PRESERVE_R3E_EXPERIMENT_SCREEN = true
EVIDENCE_PRESENT_NEQ_SCIENTIFIC_APPROVAL = true
AUDITED_NEQ_FUTURE_VALIDATED = true
SOURCE_PATH_DISPLAY_NEQ_FILE_ACCESS = true
NO_MEASURABLE_EDGE_R3D_NEQ_R3E_REJECTED = true
PENDING_NEQ_FAILED = true
WCAG_2_2_AA = true
PARALLEL_TASKS_ALLOWED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## SUMMARY

Implement the Wick product screen **Evidências** at `/governance/evidence`, introducing a dedicated Evidence Explorer ViewModel and standalone curated fixture `evidence_catalog_current_state_illustrative`. The screen provides list + detail inspection of governance evidence metadata with approved-field search/filters, without opening repository files, rendering Markdown/HTML, downloading content, or accessing real/future-unseen data. Read-only. Clearly labeled synthetic/illustrative catalog. No scientific state change.

## 1. Objetivo

Entregar a tela Evidence Explorer com PageHeader, SyntheticDataNotice, catálogo curado, busca/filtros, lista, detalhe, estados vazios/sem-resultado/seleção-inválida; testes de rota, semântica, a11y e fronteira; sem backend, FS/runtime repo, downloads, Markdown/HTML, dados reais ou future-unseen.

## 2. Contexto técnico

- UX-R2 I1 authorization assessment MERGED (PR #114 → `3be8920`); post-merge closure MERGED (PR #115 → `7cc6d54`).
- I1 auth decision: `AUTHORIZED_WITH_CONDITIONS`; posture `A_STATIC_FIXTURE_BACKED_EVIDENCE_CATALOG`.
- Route `/governance/evidence`; nav **Evidências** under Governança.
- Catalog is standalone (not grafted onto every `FixtureScenario`) to avoid cross-screen churn while remaining fixture-backed and synthetic-disclosed via `fixtureMetadata()`.
- Official scientific posture unchanged: `R3E_GATE=PENDING_FUTURE_UNSEEN_DATA`, `R3D_RESULT=NO_MEASURABLE_EDGE`, `R4=BLOCKED`, `R5=NOT_STARTED`.

## 3. Componentes afetados

| Componente | Impacto |
|------------|---------|
| `web/src/viewmodels/**` | Novo Evidence Explorer ViewModel + enums/types/filter/sourcePath |
| `web/src/fixtures/evidenceCatalog.ts` | Novo catálogo curado standalone |
| `web/src/screens/evidence-explorer/**` | Nova tela list+detail |
| `web/src/app/AppRoutes.tsx` | Rota `/governance/evidence` |
| `web/src/shell/navigation.ts` | Ativar nav **Evidências** |
| `web/tests/**` | Screen / a11y / architecture / ViewModel / fixture tests |
| Overview / Runs / Readiness / Host / R3E | Preservados |
| Backend / validate / future unseen / host ops | Não executados / não alterados |
| Docs I1 impl (impact/spec/review/handoff) + PROJECT | Atualizados |

## 4. Não afetados

- Conclusões científicas R3D/R3E
- Coleta, readiness gates, scheduler activation
- R4/R5
- APIs backend de evidência
- Ingestão dinâmica de documentos do repositório

## 5. Riscos e mitigações

| Risco | Mitigação |
|-------|-----------|
| Falsa confiança científica | Notices explícitos; testes de distinção R3D/R3E |
| sourcePath como acesso a arquivo | Display-only `<code>`; disclaimer; architecture tests |
| Escape para Markdown/HTML | Sem renderers; forbid `dangerouslySetInnerHTML` |
| Runtime FS/repo | Fixture estática; tests de fronteira |
| Dependências novas | Zero novas runtime/dev deps |

## 6. Decisão de impacto

```text
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
EVIDENCE_EXPLORER_MERGE_AUTHORIZED = false
```
