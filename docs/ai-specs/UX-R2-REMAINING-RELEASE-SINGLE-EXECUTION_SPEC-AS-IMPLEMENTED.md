# UX-R2 Remaining Release Single Execution — Spec As Implemented

```text
RELEASE = UX-R2
TASK_ID = UX-R2-REMAINING-RELEASE-SINGLE-EXECUTION-001
IMPLEMENTATION_STATUS = COMPLETE
ROUTE = /governance/evidence
FIXTURE_ID = evidence_catalog_current_state_illustrative
DEEP_LINK = /governance/evidence?evidenceId=<id>
```

## Delivered

### I2 Catalog history
- `catalogStanding`: current | pending | historical | superseded
- Enriched curated catalog (+4 entries; 11 total)
- Deterministic sort/filter; standing UI in list/detail/filters

### I3 Provenance UX
- List provenance line; detail standing + pending≠fault note
- Strengthened safety notices (evidence≠approval; R3D≠R3E; audited≠future; sourcePath≠access; pending≠fault)

### I4 Cross-navigation
- `buildEvidenceExplorerHref` / `parseEvidenceIdParam`
- `EvidenceExplorerScreen` syncs selection with search params
- `RelatedEvidenceLinks` on Overview, Runs, Readiness, Host, R3E

### I5 Fixture closure
- Fixture metadata + disclosure aligned to fixture-backed acceptance wording
- No fixture selector / live-data switch

## Out of scope (preserved)
Backend, new routes, real data, runtime repo/FS, FU payloads, validate/peek, host/scheduler activation, R4/R5.
