# UX-R2 Checkpoint — Architecture

```text
CHECKPOINT = CHECKPOINT_ARCHITECTURE
STATUS = PASS
COMMIT_SHA = 2d733dcea1890fbcd9e60727e43a6c5d056c0b18
SCOPE_REVIEWED =
  fixtures -> builder/selectors -> ViewModel -> screen components
  Evidence Explorer at /governance/evidence only
  frozen I2-I5 boundaries from UX-R2-REMAINING-RELEASE-FROZEN-SCOPE.md
  MAX_NEW_ROUTES = 0; BACKEND = false; deps = 0
TESTS_EXECUTED = none (architecture declaration; product tests begin at I2)
RESULTS =
  Architecture confirmed: continue Evidence Explorer VM + curated fixture pattern.
  Deep-link via ?evidenceId= query only (no new routes).
  Cross-nav via react-router Link to internal paths only.
  catalogStanding enum for I2 history standing (current/pending/historical/superseded).
BOUNDARY_VIOLATIONS = none
KNOWN_LIMITATIONS =
  I1 post-merge acceptance stamp is docs-only precondition on this branch.
  Single draft PR will carry all increments without intermediate merges.
UNRESOLVED_RISKS = none blocking
NEXT_ACTION = proceed to I2 catalog history
```

## Architecture decisions

1. Keep single route `/governance/evidence`.
2. Enrich `evidence_catalog_current_state_illustrative` only (no second fixture).
3. Add `catalogStanding` closed enum for history standing distinct from `staleness`.
4. Selection deep-link: `?evidenceId=` via `useSearchParams`.
5. Shared `RelatedEvidenceLinks` + `evidenceDeepLink` helpers for I4.
6. No backend, no new dependencies, no runtime FS/repo access.
