# UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS — Handoff

```text
STATUS = REBASED_SPECIFICATION_READY_FOR_HUMAN_REVIEW
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
PR = 44
OLD_BASE_SHA = 5e438b8ad84d13f0c22c4017d3d3e26ac3c26647
NEW_BASE_SHA = 1bad329e93fbd8d7e8693a593f00ed6d021bb6e9
IMPLEMENTATION_HEAD = 8fa4a103c2b2fde13f00220a980510f02434e212
CONTENT_REVIEWED_THROUGH_HEAD = 8fa4a103c2b2fde13f00220a980510f02434e212
FINAL_CANDIDATE_HEAD = 8fa4a103c2b2fde13f00220a980510f02434e212
PR_TIP = cdc5b2739ac6c647fdc49099a79bf81da5b099cb
FULL_TEST_SUITE = PASS
LINT_STATUS = PASS
GOVERNANCE_VALIDATOR = ERRORS_0_WARNINGS_0
CI_STATUS = GREEN
PR_MERGEABLE = true
UX_B3_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_SCIENTIFIC_STATE_CHANGE = false
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
BLOCKERS = none for specification; UI blocked until explicit authorization; live host discovery still deferred for real ops data; UX-B4 language track parallel (not a B3 blocker)
FINAL_RECOMMENDATION = PR #44 rebased and mergeable candidate after human review. Do not authorize UI implementation. Do not merge automatically. Future UI must consume UX-B2 architecture + UX-B3 contracts + UX-B4 language when authorized. Keep scheduler inactive and validate unauthorized. Data-access recommendation remains architectural only (no index/adapter in this PR).
```

## Summary

UX-B3 screen contracts rebased onto `main` (`1bad329`), reconciled with UX-B2 I1 authorization track and UX-B4 independent language track. Specification-only; no UI code.

## Parallel tracks

```text
UX-B2 = future frontend / design-system architecture (I1 auth merged; execution blocked)
UX-B3 = screen and data contracts (this PR)
UX-B4 = terminology and microcopy (independent track / PR #42)
```

## Data access

```text
RECOMMENDED_DATA_ACCESS = GENERATED_OPERATIONAL_INDEX_PLUS_CLI_READ_ONLY
SCOPE = ARCHITECTURAL_RECOMMENDATION_ONLY
INDEX_GENERATED_IN_THIS_TASK = false
ADAPTER_IMPLEMENTED_IN_THIS_TASK = false
```
