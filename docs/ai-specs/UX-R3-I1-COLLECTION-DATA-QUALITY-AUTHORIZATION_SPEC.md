# UX-R3 I1 — Collection Data Quality Authorization Spec

```text
RELEASE = UX-R3
INCREMENT = I1
TASK_ID = UX-R3-I1-COLLECTION-DATA-QUALITY-AUTHORIZATION-ASSESSMENT-001
PHASE = AUTHORIZATION_ASSESSMENT
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
ASSESSMENT_ONLY = true
DECISION = AUTHORIZED_WITH_CONDITIONS
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
IMPACT = docs/ai-impact/UX-R3-I1-COLLECTION-DATA-QUALITY-AUTHORIZATION_IMPACT_ASSESSMENT.md
```

## Purpose

Freeze the exact implementation boundary for a fixture-backed, read-only **Dados Coletados** screen. This spec does **not** authorize implementation and does **not** mark UX-R3 or I1 started.

```text
UX_R3_STATUS = NOT_STARTED
UX_R3_I1_IMPLEMENTATION_AUTHORIZED = false
PRODUCT_CODE_AUTHORIZED = false
NEW_ROUTE_AUTHORIZED = false
NAVIGATION_CHANGE_AUTHORIZED = false
```

## Frozen authorization fields

```text
SCREEN_PURPOSE =
  Explain illustrative collection progress and data-quality posture without
  implying scientific approval, validation readiness, or operational activation.

AUTHORIZED_ROUTE = /future-collection/collected-data
AUTHORIZED_NAV_LABEL = Dados Coletados
AUTHORIZED_NAV_PLACEMENT = Coleta Futura; after Runs and Readiness
AUTHORIZED_SCREEN_TITLE = Dados Coletados
AUTHORIZED_IMPLEMENTATION_POSTURE = A_STATIC_FIXTURE_BACKED_COLLECTION_DATA_QUALITY
AUTHORIZED_FIXTURE_ID = collection_data_quality_current_state_illustrative
AUTHORIZED_VIEWMODEL_NAME = CollectionDataQualityViewModel
```

## Architecture contract

```text
DATA_FLOW = fixture -> builders/selectors -> CollectionDataQualityViewModel -> screen
FIXTURE_BACKED_READ_ONLY = true
CURATED_ILLUSTRATIVE_DATA = true
NO_VISIBLE_FIXTURE_SELECTOR = true
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
BACKEND_FILES_CHANGED = 0

FORBIDDEN_FIXTURE_SOURCES =
  database;
  repository files at runtime;
  reports payloads at runtime;
  host filesystem;
  network;
  environment variables;
  future-unseen payloads
```

## Quality status model

```text
SERIES_COMPLETE
SERIES_PARTIAL
GAPS_PRESENT
DUPLICATES_PRESENT
REJECTED_RECORDS_PRESENT
OPEN_CANDLE_EXCLUDED
SOURCE_UNAVAILABLE
STALE_STATE
UNKNOWN_STATE
```

## Severity model

```text
informational | warning | fault
RED_RESERVED_FOR_GENUINE_FAULT_ONLY = true
```

## Semantic distinctions

```text
DATA_QUALITY != SCIENTIFIC_APPROVAL
COVERAGE_COMPLETE != FUTURE_WINDOW_COMPLETE
COLLECTION_HEALTHY != VALIDATION_READY
GAP_PRESENT != COLLECTION_FAILED
OPEN_CANDLE_EXCLUDED != DATA_CORRUPTION
PENDING != FAULT
UNKNOWN != ZERO
```

## Cross-navigation

```text
INTERNAL_ONLY =
  /future-collection/runs
  /future-collection/readiness
  /governance/evidence?evidenceId=<sanitized>
FORBIDDEN =
  downloads;
  external URLs;
  source-file navigation;
  arbitrary URL generation
```

## Acceptance criteria (implementation gate)

```text
1. Screen answers PRIMARY_USER_QUESTIONS with illustrative fixture data
2. Dedicated VM + fixture; screen does not consume raw fixture records
3. Nav Dados Coletados active; route /future-collection/collected-data
4. Synthetic + freshness disclosure present
5. Severity/quality models + inequalities tested
6. No ops/validate/FU/real-data/backend/deps
7. A11y + architecture + responsive coverage PASS
```

## Process

```text
PROCESS_MODEL = FULL_INCREMENTAL_FLOW
NEXT_RECOMMENDED_TASK = UX_R3_I1_COLLECTION_DATA_QUALITY_IMPLEMENTATION
```

Implementation remains unauthorized until a separate human-approved prompt after this assessment merges.

## Scientific and operational truth (immutable)

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
R3D_RESULT = NO_MEASURABLE_EDGE
R3E_STATUS = EXPLORATORY_COMPLETE_PENDING_FUTURE_UNSEEN_DATA
SCIENTIFIC_CONCLUSION = UNCHANGED
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## Official operational wording preserved

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```
