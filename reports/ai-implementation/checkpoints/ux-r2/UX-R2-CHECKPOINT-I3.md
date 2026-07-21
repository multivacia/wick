# UX-R2 Checkpoint — I3 Provenance UX

```text
CHECKPOINT = CHECKPOINT_I3
STATUS = PASS
COMMIT_SHA = b3c418c7bcbef983ed9f19841a3e16998f1401d3
SCOPE_REVIEWED =
  EvidenceList provenance line (origin · stage · staleness)
  EvidenceDetail standing + pending≠fault note
  EVIDENCE_SAFETY_NOTICES strengthened (R3D≠R3E, pending≠fault, evidence≠approval, sourcePath≠access)
  CSS token-based provenance/standing styles
TESTS_EXECUTED =
  pnpm --dir web test (EvidenceExplorerScreen + ViewModel notice assertions)
  pnpm --dir web test:a11y
RESULTS =
  Safety notices assert R3D≠R3E and pending≠fault.
  sourcePath remains non-clickable <code>.
  StatusBadge + text labels avoid color-only status.
BOUNDARY_VIOLATIONS = none
KNOWN_LIMITATIONS =
  Provenance is fixture metadata only — not live repository lookup.
UNRESOLVED_RISKS = none blocking
NEXT_ACTION = proceed to I4 cross-navigation checkpoint
```
