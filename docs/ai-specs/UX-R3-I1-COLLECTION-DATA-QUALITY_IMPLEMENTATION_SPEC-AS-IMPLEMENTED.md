# UX-R3 I1 — Collection Data Quality Implementation — Spec As Implemented

```text
RELEASE = UX-R3
INCREMENT = I1
TASK_ID = UX-R3-I1-COLLECTION-DATA-QUALITY-IMPLEMENTATION-001
PHASE = IMPLEMENTATION
SPEC_STATUS = AS_IMPLEMENTED
DECISION = IMPLEMENTATION_AUTHORIZED
```

## Frozen boundary (implemented)

```text
ROUTE = /future-collection/collected-data
NAV_LABEL = Dados Coletados
SCREEN_TITLE = Dados Coletados
IMPLEMENTATION_POSTURE = A_STATIC_FIXTURE_BACKED_COLLECTION_DATA_QUALITY
FIXTURE_ID = collection_data_quality_current_state_illustrative
VIEWMODEL_NAME = CollectionDataQualityViewModel
```

## Data flow

```text
getCollectionDataQualityFixture()
  -> loadCollectedDataScreenData()
  -> buildCollectionDataQualityViewModel(domain, criteria, clock)
  -> CollectedDataScreenView
```

## Quality statuses implemented

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

## Severity

```text
informational | warning | fault
RED_FOR_FAULT_ONLY = true  (SOURCE_UNAVAILABLE only)
SORT = severity asc (fault>warning>informational) then lastUpdate desc
```

## Semantic safeguards (tested)

```text
DATA_QUALITY != SCIENTIFIC_APPROVAL
COVERAGE_COMPLETE != FUTURE_WINDOW_COMPLETE
COLLECTION_HEALTHY != VALIDATION_READY
GAP_PRESENT != COLLECTION_FAILED
OPEN_CANDLE_EXCLUDED != DATA_CORRUPTION
PENDING != FAULT
UNKNOWN != ZERO
```

## Screen behaviors

```text
SUMMARY_METRICS = implemented
FILTERS = seriesId, market, interval, qualityStatus, severity
EMPTY_STATE = implemented (EMPTY != FAULT)
NO_RESULTS_STATE = implemented + clear filters
UNKNOWN_STATE = Desconhecido display (not 0)
STALE_STATE = freshness disclosure
CROSS_NAV = /future-collection/runs | /future-collection/readiness | /governance/evidence?evidenceId=
RESPONSIVE = phone/tablet/desktop CSS
A11Y = landmarks, labels, StatusBadge text, axe smoke
```

## Key files

```text
web/src/fixtures/collectionDataQuality.ts
web/src/viewmodels/collectionDataQualityEnums.ts
web/src/viewmodels/collectionDataQualityTypes.ts
web/src/viewmodels/filterCollectionDataQuality.ts
web/src/viewmodels/buildCollectionDataQualityViewModel.ts
web/src/screens/collected-data/*
web/src/shell/navigation.ts
web/src/app/AppRoutes.tsx
```

## Prohibited capabilities (architecture-tested)

```text
fs / child_process / fetch / process.env / dangerouslySetInnerHTML /
markdown renderers / downloads / external hrefs / fixture selector /
Date.now / Math.random in fixture / ops activate/validate controls
```
