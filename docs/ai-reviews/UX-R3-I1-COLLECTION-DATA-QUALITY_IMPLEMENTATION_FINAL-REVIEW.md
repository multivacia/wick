# UX-R3 I1 — Collection Data Quality Implementation — Final Review

```text
RELEASE = UX-R3
INCREMENT = I1
TASK_ID = UX-R3-I1-COLLECTION-DATA-QUALITY-IMPLEMENTATION-001
PHASE = INDEPENDENT_FINAL_REVIEW
CHANGE_RISK = MEDIUM
FINAL_REVIEW_STATUS = COMPLETE
FINAL_REVIEW_DECISION = APPROVED
```

## Scope verification

- Route `/future-collection/collected-data` registered and rendered
- Nav **Dados Coletados** active under Coleta Futura after Runs/Readiness
- Fixture id `collection_data_quality_current_state_illustrative` only
- Dedicated `CollectionDataQualityViewModel` — screen does not consume raw fixture rows as UI model
- All nine quality statuses present in curated fixture
- Severity model with red reserved for `SOURCE_UNAVAILABLE` only
- Semantic inequalities disclosed and unit-tested
- Filters + deterministic sort implemented
- Empty / no-results / unknown / stale handled
- Cross-nav allowlist only
- Zero backend files; zero new dependencies
- No real data, FU payloads, validation, effect peeking, host/scheduler actions
- R3E / R4 / R5 scientific truth unchanged

## Security / architecture

Architecture boundary tests pass for screen + ViewModel + fixture trees. No `fetch`, `fs`, `process.env`, unsafe HTML, markdown renderers, downloads, or external href generation.

## Accessibility / responsive

Axe smoke PASS on the route. Semantic headings/landmarks present. Status meaning is not color-only (StatusBadge labels + severity text). Responsive CSS covers narrow / tablet / desktop.

## Decision

```text
FINAL_REVIEW_DECISION = APPROVED
UNRESOLVED_BLOCKERS = NONE
POST_REVIEW_NORMATIVE_CHANGES = 0
```

## Recommendation

Await human merge authorization. Do not start I2–I5 or parallel work. Do not merge without green CI and explicit human authorization.
