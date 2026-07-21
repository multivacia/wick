# UX-R2 Checkpoint — I2 Catalog History

```text
CHECKPOINT = CHECKPOINT_I2
STATUS = PASS
COMMIT_SHA = b3c418c7bcbef983ed9f19841a3e16998f1401d3
SCOPE_REVIEWED =
  catalogStanding enum (current/pending/historical/superseded)
  evidence_catalog_current_state_illustrative enrichment (+4 entries)
  deterministic sort/filter; EvidenceFilters/List/Detail standing UI
  fixture integrity + ViewModel standing tests
TESTS_EXECUTED =
  pnpm --dir web test (includes fixture + ViewModel standing/sort/filter)
RESULTS =
  11 catalog entries with closed standings; missing classes covered
  (implementation_handoff, technical_scientific_review, superseded draft).
  Sort rank current→pending→historical→superseded verified in tests.
  R3D≠R3E preserved in fixture content.
BOUNDARY_VIOLATIONS = none
KNOWN_LIMITATIONS =
  Catalog remains curated/illustrative; not complete repository history.
UNRESOLVED_RISKS = none blocking
NEXT_ACTION = proceed to I3 provenance UX (already in same impl commit; verify I3 checkpoint)
```
