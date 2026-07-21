# UX-R2 Checkpoint — I4 Cross-Navigation

```text
CHECKPOINT = CHECKPOINT_I4
STATUS = PASS
COMMIT_SHA = b3c418c7bcbef983ed9f19841a3e16998f1401d3
SCOPE_REVIEWED =
  evidenceDeepLink helpers (?evidenceId=)
  EvidenceExplorerScreen useSearchParams sync
  RelatedEvidenceLinks on Overview/Runs/Readiness/Host/R3E
  No new routes; no external hrefs; no sourcePath links
TESTS_EXECUTED =
  web/tests/viewmodels/evidenceDeepLink.test.ts
  EvidenceExplorerScreen deep-link tests
  MVP screen tests wrapped with MemoryRouter where needed
RESULTS =
  Deep-link opens detail; invalid ids rejected by parseEvidenceIdParam.
  Related links use react-router Link to /governance/evidence?evidenceId=…
  No https:// links introduced in related evidence blocks.
BOUNDARY_VIOLATIONS = none
KNOWN_LIMITATIONS =
  Related links show curated subset per screen, not auto-discovered graph.
UNRESOLVED_RISKS = none blocking
NEXT_ACTION = proceed to I5 fixture closure checkpoint
```
