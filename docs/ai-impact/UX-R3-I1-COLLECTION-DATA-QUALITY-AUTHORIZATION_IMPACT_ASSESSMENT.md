# UX-R3-I1-COLLECTION-DATA-QUALITY-AUTHORIZATION-ASSESSMENT — Análise de Impacto

## Metadados

```text
RELEASE = UX-R3
RELEASE_NAME = WICK RESEARCH OPERATIONS R3
INCREMENT = I1
TASK_ID = UX-R3-I1-COLLECTION-DATA-QUALITY-AUTHORIZATION-ASSESSMENT-001
TITLE = Collection Data Quality Authorization Assessment
PHASE = AUTHORIZATION_ASSESSMENT
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
ASSESSMENT_ONLY = true
ASSESSMENT_AUTHORIZED = true
IMPLEMENTATION_SCOPE = AUTHORIZATION_ASSESSMENT_DOCUMENTATION_ONLY
DECISION = AUTHORIZED_WITH_CONDITIONS

UX_R3_STATUS = NOT_STARTED
UX_R3_I1_IMPLEMENTATION_AUTHORIZED = false
PRODUCT_CODE_AUTHORIZED = false
NEW_ROUTE_AUTHORIZED = false
NAVIGATION_CHANGE_AUTHORIZED = false
BACKEND_IMPLEMENTATION_AUTHORIZED = false
REAL_DATA_INTEGRATION_AUTHORIZED = false
RUNTIME_REPOSITORY_ACCESS_AUTHORIZED = false
RAW_FILESYSTEM_ACCESS_AUTHORIZED = false
FUTURE_UNSEEN_RESULTS_ACCESS_AUTHORIZED = false
VALIDATION_EXECUTION_AUTHORIZED = false
EFFECT_PEEKING_AUTHORIZED = false
REAL_HOST_DISCOVERY_AUTHORIZED = false
SCHEDULER_ACTIVATION_AUTHORIZED = false
OPERATIONAL_ACTIONS_AUTHORIZED = false
R4_STATE_CHANGE_AUTHORIZED = false
R5_STATE_CHANGE_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false

AUTHORIZED_ROUTE = /future-collection/collected-data
AUTHORIZED_NAV_LABEL = Dados Coletados
AUTHORIZED_NAV_PLACEMENT = Coleta Futura group; after Runs and Readiness
AUTHORIZED_SCREEN_TITLE = Dados Coletados
AUTHORIZED_IMPLEMENTATION_POSTURE = A_STATIC_FIXTURE_BACKED_COLLECTION_DATA_QUALITY
AUTHORIZED_FIXTURE_ID = collection_data_quality_current_state_illustrative
AUTHORIZED_VIEWMODEL_NAME = CollectionDataQualityViewModel

PR126_STATUS = MERGED
PR126_MERGE_COMMIT = e23bfe921c22b8c147ded4546e07f03ba9e0a024
PR127_STATUS = MERGED
PR127_MERGE_COMMIT = e602ef398234c6c8469df4fbbd8a99c1a41b081c
MAIN_TIP = e602ef398234c6c8469df4fbbd8a99c1a41b081c

UX_R3_DISCOVERY_AND_SCOPE_STATUS = MERGED
UX_R3_DISCOVERY_DECISION = SCOPE_RECOMMENDED
UX_R3_RECOMMENDED_DIRECTION = E_COLLECTION_MONITORING_AND_DATA_QUALITY
UX_R3_PROCESS_MODEL = FULL_INCREMENTAL_FLOW

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
R3E_STATUS = EXPLORATORY_COMPLETE_PENDING_FUTURE_UNSEEN_DATA
SCIENTIFIC_CONCLUSION = UNCHANGED
R3E_SCIENTIFIC_STATE_CHANGE = false

REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = e602ef398234c6c8469df4fbbd8a99c1a41b081c
ANALYZED_AT = 2026-07-22T16:45:00Z
ANALYZED_BY = cursor-agent
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
NEXT_RECOMMENDED_TASK = UX_R3_I1_COLLECTION_DATA_QUALITY_IMPLEMENTATION
NEXT_ITEM = UX_R3_I1_COLLECTION_DATA_QUALITY_SEPARATE_IMPLEMENTATION_TASK
```

G1 note: **AUTHORIZED_WITH_CONDITIONS** authorizes only a **future separate** implementation prompt under the frozen boundary below. This assessment does **not** flip implementation, product-code, route, navigation, fixture, ViewModel, real-data, validation, peeking, host, scheduler, R4 or R5 flags to true, and does **not** mark UX-R3 or I1 started.

## MANDATORY_CONSTRAINTS

```text
ASSESSMENT_ONLY = true
NO_PRODUCT_CODE_CHANGES = true
NO_NEW_SCREENS_NOW = true
NO_NAV_ACTIVATION_NOW = true
NO_REAL_DATA = true
NO_RUNTIME_REPOSITORY_ACCESS = true
NO_RAW_FILESYSTEM_ACCESS = true
NO_FUTURE_UNSEEN_RESULTS = true
NO_VALIDATION_EXECUTION = true
NO_EFFECT_PEEKING = true
NO_OPERATIONAL_ACTIONS = true
NO_SCIENTIFIC_INTERPRETATION_CHANGE = true
NO_R4_OR_R5_STATE_CHANGE = true
PARALLEL_TASKS_ALLOWED = false
```

## SUMMARY

UX-R3 discovery recommended **E_COLLECTION_MONITORING_AND_DATA_QUALITY**. Planned nav **Dados Coletados** is inactive under Coleta Futura; Readiness explicitly discloses that collection-health metrics are absent from its ViewModel. I1 can safely authorize a **fixture-backed, read-only Dados Coletados** screen with dedicated ViewModel+fixture, quality dimensions answering the required user questions, severity model with red reserved for genuine fault, synthetic/freshness disclosure, and internal cross-links — without real series payloads, future-unseen results, collection controls, host/scheduler actions, or scientific approval implication.

Authorized route: **`/future-collection/collected-data`** (matches `/future-collection/runs` and `/future-collection/readiness`; planned nav id `collected-data`). Bare `/collected-data` rejected.

## 1. Screen purpose and user questions

```text
SCREEN_PURPOSE =
  Explain illustrative collection progress and data-quality posture for the
  future-collection window so Gustavo can distinguish informational gaps from
  true faults and understand impact on scientific readiness without executing
  collection or validation.

PRIMARY_USER_QUESTIONS =
  what is being collected;
  market / asset / interval / source;
  represented collection window;
  coverage;
  gaps;
  duplicates;
  rejected records;
  open-candle exclusions;
  source state;
  last illustrative update;
  informational vs warning vs true fault;
  impact on scientific readiness;
  next safe action
```

## 2. Frozen authorization boundary

```text
AUTHORIZED_ROUTE = /future-collection/collected-data
AUTHORIZED_NAV_LABEL = Dados Coletados
AUTHORIZED_NAV_PLACEMENT = NAV_GROUPS.future-collection; order Runs → Readiness → Dados Coletados
AUTHORIZED_SCREEN_TITLE = Dados Coletados
AUTHORIZED_IMPLEMENTATION_POSTURE = A_STATIC_FIXTURE_BACKED_COLLECTION_DATA_QUALITY
AUTHORIZED_FIXTURE_ID = collection_data_quality_current_state_illustrative
AUTHORIZED_VIEWMODEL_NAME = CollectionDataQualityViewModel

AUTHORIZED_SCREEN_BOUNDARY =
  COLLECTION_DATA_QUALITY_SCREEN_ONLY;
  FIXTURE_BACKED;
  READ_ONLY;
  NO_VISIBLE_FIXTURE_SELECTOR;
  NO_COLLECTION_START_STOP_RETRY;
  NO_VALIDATE;
  NO_REAL_SERIES_PAYLOADS;
  NO_CHARTS_PNL;
  NO_DOWNLOADS;
  NO_EXTERNAL_LINKS;
  SYNTHETIC_DISCLOSURE_REQUIRED;
  DEDICATED_VIEWMODEL_REQUIRED;
  DEDICATED_FIXTURE_REQUIRED

AUTHORIZED_FIXTURE_CONTRACT =
  curated static TypeScript fixture only;
  never built at runtime from DB/repo/FS/network/env/FU payloads;
  answers PRIMARY_USER_QUESTIONS illustratively;
  includes series entries + aggregate quality summary + nextSafeAction + known/unknown

AUTHORIZED_VIEWMODEL_BOUNDARY =
  fixture -> builders/selectors -> CollectionDataQualityViewModel -> screen;
  screen must not interpret raw fixture records;
  map domain quality states to presentation severity;
  preserve semantic inequalities in labels/notices

AUTHORIZED_SECURITY_BOUNDARY =
  NO_RUNTIME_FS;
  NO_REPO_BROWSE;
  NO_NETWORK_FETCH;
  NO_HTML_MD_RENDER;
  NO_EXTERNAL_HREF;
  NO_FU_PAYLOADS;
  NO_SECRETS;
  sourcePath display-only if present (allowlisted metadata text only)

AUTHORIZED_ACCESSIBILITY_BOUNDARY =
  plain language first;
  semantic headings/landmarks;
  keyboard nav + visible focus;
  accessible lists/tables;
  no color-only meaning;
  responsive layouts;
  illustrative + freshness disclosure required

AUTHORIZED_CROSS_NAVIGATION =
  internal RelatedEvidenceLinks / router Links only to:
    /future-collection/runs;
    /future-collection/readiness;
    /governance/evidence?evidenceId=… (existing sanitize rules);
  optional Overview deep-link later; not required for I1 foundation
```

## 3. Quality / severity / UI models

```text
QUALITY_STATUS_MODEL =
  SERIES_COMPLETE;
  SERIES_PARTIAL;
  GAPS_PRESENT;
  DUPLICATES_PRESENT;
  REJECTED_RECORDS_PRESENT;
  OPEN_CANDLE_EXCLUDED;
  SOURCE_UNAVAILABLE;
  STALE_STATE;
  UNKNOWN_STATE

SEVERITY_MODEL =
  informational | warning | fault;
  RED_RESERVED_FOR_GENUINE_FAULT_ONLY;
  GAP_PRESENT != COLLECTION_FAILED;
  PENDING != FAULT;
  UNKNOWN != ZERO

FILTER_MODEL =
  optional client-side: seriesId; market/asset; interval; qualityStatus; severity
SORT_MODEL =
  default: severity fault>warning>info, then lastUpdate desc; optional seriesId
EMPTY_STATE_MODEL =
  no series in fixture → explicit empty copy; not success
NO_RESULTS_STATE_MODEL =
  filters yield zero → no-results copy; clear-filters affordance
UNKNOWN_STATE_MODEL =
  unknown fields shown as Unknown / Indeterminado; never coerced to 0
STALE_STATE_MODEL =
  freshnessLabel + illustrative disclosure required
ILLUSTRATIVE_DISCLOSURE =
  mandatory SyntheticDataNotice-equivalent; fixture id visible; not live
```

## 4. Semantic distinctions (required)

```text
DATA_QUALITY != SCIENTIFIC_APPROVAL
COVERAGE_COMPLETE != FUTURE_WINDOW_COMPLETE
COLLECTION_HEALTHY != VALIDATION_READY
GAP_PRESENT != COLLECTION_FAILED
OPEN_CANDLE_EXCLUDED != DATA_CORRUPTION
PENDING != FAULT
UNKNOWN != ZERO
COLLECTION_IN_PROGRESS != READY
WINDOW_DAYS_INSUFFICIENT != OPERATIONAL_FAULT
```

## 5. Architecture impact

| Area | I1 impact (when later implemented) |
|------|-------------------------------------|
| Route | Add `/future-collection/collected-data` |
| Nav | Activate planned Dados Coletados |
| ViewModel | New `buildCollectionDataQualityViewModel` |
| Fixture | New dedicated fixture id (not overload Runs/Readiness fixtures) |
| Backend/deps | Zero |
| Tests | VM, fixture contract, architecture boundary, screen, a11y, responsive, semantic inequalities |

```text
NEW_ROUTES_PROPOSED = 1
BACKEND_FILES_PROPOSED = 0
NEW_RUNTIME_DEPENDENCIES_PROPOSED = 0
NEW_DEV_DEPENDENCIES_PROPOSED = 0
```

## 6. Security and trust

| Risk | Mitigation in authorized boundary |
|------|-----------------------------------|
| Path traversal / FS / repo browse | No runtime FS/repo; path text non-navigating |
| Secret exposure | No secrets in fixture |
| Network access | No fetch/axios/WS |
| Unsafe HTML/MD / external links | Forbidden |
| Future-unseen leakage / effect peeking | No FU payloads; no validate |
| Fabricated quality / stale misunderstanding | Illustrative + freshness disclosure |
| False scientific / operational readiness | Explicit inequalities + notices |
| Unsafe ops action | No start/stop/retry/collect/activate |

## 7. Acceptance criteria (for later implementation)

```text
AUTHORIZED_ACCEPTANCE_CRITERIA =
  1. Route /future-collection/collected-data renders fixture-backed screen
  2. Nav Dados Coletados active under Coleta Futura
  3. Dedicated ViewModel+fixture; no raw fixture in screen
  4. Answers PRIMARY_USER_QUESTIONS illustratively
  5. Quality/severity models implemented; red only for fault
  6. Semantic inequalities asserted in tests
  7. Synthetic + freshness disclosure present
  8. No visible fixture selector
  9. No ops/validate/download/external controls
  10. Internal cross-links to Runs/Readiness/Evidence only
  11. Architecture + a11y + responsive tests PASS
  12. Zero new deps; zero backend files
  13. Scientific/operational truth unchanged
```

## 8. Process model

```text
FULL_INCREMENTAL_FLOW preserved:
  authorization assessment (this PR)
  → human merge authorization
  → assessment merge and closure
  → separate implementation authorization prompt
  → implementation
  → independent review
  → human merge authorization
  → post-merge acceptance
```

## 9. Alternatives considered

| Alternative | Decision |
|-------------|----------|
| Overload Readiness with collection-health fields | REJECTED — Readiness VM explicitly excludes them; dedicated screen safer |
| Route `/dados-coletados` or `/collected-data` | REJECTED — breaks `/future-collection/*` convention |
| Real series from DB/backend | REJECTED / deferred — not least-risk |
| Single-execution of I1–I5 now | REJECTED — process is FULL_INCREMENTAL_FLOW; I1 is auth only |
| BLOCKED until FU window complete | REJECTED — fixture value exists during IN_PROGRESS |

## 10. Decisão

```text
DECISION = AUTHORIZED_WITH_CONDITIONS
IMPACT_ASSESSMENT_STATUS = APPROVED
UX_R3_STATUS = NOT_STARTED
UX_R3_I1_IMPLEMENTATION_AUTHORIZED = false
PRODUCT_CODE_AUTHORIZED = false
NEW_ROUTE_AUTHORIZED = false
NAVIGATION_CHANGE_AUTHORIZED = false
NEXT_RECOMMENDED_TASK = UX_R3_I1_COLLECTION_DATA_QUALITY_IMPLEMENTATION
```

## Official operational wording preserved

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```
