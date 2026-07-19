# UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS — Handoff

```text
STATUS = SPECIFICATION_COMPLETE_AWAITING_HUMAN_MERGE
RELEASE = UX-R1
BACKLOG_ITEM = UX-B3
TASK_ID = OPERATIONAL-MVP-SCREEN-CONTRACTS-001
PHASE = SPECIFICATION_AND_IMPACT_ASSESSMENT
SCREENS = Visão Geral | Execuções | Readiness | Host e Scheduler
CURRENT_DATA_SOURCES = docs/PROJECT.md; data/future_unseen/manifests/*; reports/r3e_future_unseen/readiness_report.json; ops_report.json; automation_state.json; automation_runs/*/cycle_report.json; collection_runs/*; docs/operations/*; docs/checklists/*; ops/local/systemd/*; failure taxonomy; CLI history/lock-status
DATA_GAPS = host discovery result missing; automation.lock absent; automation_events.jsonl absent; backups absent; raw/validated gitignored; no unified execution index; no OPERATIONAL_DEBT field (derived); no canonical NEXT_ACTION field (derived)
RECOMMENDED_DATA_ACCESS = GENERATED_OPERATIONAL_INDEX_PLUS_CLI_READ_ONLY
SCREEN_CONTRACT_SPEC = docs/ai-specs/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS_SPEC.md
DATA_CONTRACT_CATALOG = docs/ux/UX-R1-OPERATIONAL-MVP_DATA-CONTRACT-CATALOG.md
STATE_MATRIX = docs/ux/UX-R1-OPERATIONAL-MVP_STATE-MATRIX.md
SAFE_FIXTURE_CATALOG = docs/ux/UX-R1-OPERATIONAL-MVP_SAFE-FIXTURE-CATALOG.md
IMPACT_ASSESSMENT = docs/ai-impact/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS-001_IMPACT_ASSESSMENT.md
IMPACT_ASSESSMENT_STATUS = APPROVED
REVIEW = docs/ai-reviews/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS_REVIEW.md
REVIEW_STATUS = APPROVED
BRANCH = cursor/ux-r1-b3-operational-mvp-screen-contracts-123e
PR = https://github.com/multivacia/wick/pull/44
BASE_SHA = 5e438b8ad84d13f0c22c4017d3d3e26ac3c26647
BRANCH_TIP = 325663b89790b955a8e72d2262211ad0f6159efd
IMPLEMENTATION_HEAD = e946c385c25fbea406f69b1516091d5dc672e6d0
CONTENT_REVIEWED_THROUGH_HEAD = e946c385c25fbea406f69b1516091d5dc672e6d0
FINAL_CANDIDATE_HEAD = e946c385c25fbea406f69b1516091d5dc672e6d0
FULL_TEST_SUITE = PASS
LINT_STATUS = PASS
GOVERNANCE_VALIDATOR = ERRORS_0_WARNINGS_0
CI_STATUS = PENDING_ON_PR
UX_B3_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_SCIENTIFIC_STATE_CHANGE = false
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
BLOCKERS = none for specification; UI blocked until explicit authorization; live host discovery still deferred for real ops data
FINAL_RECOMMENDATION = Merge documentation contracts after human review. Do not authorize UI implementation yet. Next UI work requires UX_B3_IMPLEMENTATION_AUTHORIZED=true and preferably UX-B2 implementation authorization or explicit fixtures-only exception. Keep scheduler inactive and validate unauthorized.
```

## Summary

UX-B3 delivers **specification-only** contracts for the four MVP operational screens, grounded in existing R3E future-unseen artifacts and ops docs. No UI code, no backend mutation, no scientific state change.

## Decision notes

- `IMPLEMENTATION_AUTHORIZED=true` satisfies G1 for MEDIUM APPROVED impact and authorizes only these docs.
- `UX_B3_IMPLEMENTATION_AUTHORIZED=false` and `UI_IMPLEMENTATION_AUTHORIZED=false` remain mandatory.
- Recommended future data access: generated operational index + CLI read-only fallbacks.
