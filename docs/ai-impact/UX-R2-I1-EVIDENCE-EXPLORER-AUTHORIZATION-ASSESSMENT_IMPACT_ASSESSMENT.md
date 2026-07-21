# UX-R2-I1-EVIDENCE-EXPLORER-AUTHORIZATION-ASSESSMENT — Análise de Impacto

## Metadados

```text
RELEASE = UX-R2
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE R2
INCREMENT = I1
TASK_ID = EVIDENCE-EXPLORER-AUTHORIZATION-ASSESSMENT-001
TITLE = Evidence Explorer Authorization Assessment
PHASE = IMPLEMENTATION_AUTHORIZATION_ASSESSMENT
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
ASSESSMENT_ONLY = true
ASSESSMENT_AUTHORIZED = true
IMPLEMENTATION_SCOPE = AUTHORIZATION_ASSESSMENT_DOCUMENTATION_ONLY
DECISION = AUTHORIZED_WITH_CONDITIONS

IMPLEMENTATION_EXECUTION_AUTHORIZED = false
UX_R2_I1_IMPLEMENTATION_AUTHORIZED = false
EVIDENCE_EXPLORER_IMPLEMENTATION_AUTHORIZED = false
PRODUCT_CODE_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
FIXTURE_IMPLEMENTATION_AUTHORIZED = false
REAL_DATA_INTEGRATION_AUTHORIZED = false
REPOSITORY_FILE_READ_INTEGRATION_AUTHORIZED = false
FUTURE_UNSEEN_RESULTS_ACCESS_AUTHORIZED = false
VALIDATION_EXECUTION_AUTHORIZED = false
EFFECT_PEEKING_AUTHORIZED = false
SCIENTIFIC_INTERPRETATION_CHANGE_AUTHORIZED = false
REAL_HOST_DISCOVERY_AUTHORIZED = false
SCHEDULER_ACTIVATION_AUTHORIZED = false
OPERATIONAL_ACTIONS_AUTHORIZED = false
R4_STATE_CHANGE_AUTHORIZED = false
R5_STATE_CHANGE_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false

RECOMMENDED_ROUTE = /governance/evidence
RECOMMENDED_NAV_LABEL = Evidências
RECOMMENDED_IMPLEMENTATION_POSTURE = A_STATIC_FIXTURE_BACKED_EVIDENCE_CATALOG
RECOMMENDED_IMPLEMENTATION_BOUNDARY = EVIDENCE_EXPLORER_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; CURATED_MANIFEST_ONLY; LIST_AND_DETAIL; NO_VISIBLE_FIXTURE_SELECTOR; NO_RUNTIME_REPOSITORY_ACCESS; NO_RAW_FILESYSTEM_ACCESS; NO_REAL_DATA; NO_FUTURE_UNSEEN_RESULTS; NO_VALIDATION_EXECUTION; NO_EFFECT_PEEKING; NO_OPERATIONAL_ACTIONS; NO_DOWNLOADS; NO_RAW_MARKDOWN_REPO_RENDERING; SUMMARY_AND_METADATA_ONLY; SYNTHETIC_DISCLOSURE_REQUIRED; DEDICATED_VIEWMODEL_REQUIRED; DEDICATED_FIXTURE_REQUIRED

PR112_STATUS = MERGED
PR112_MERGE_COMMIT = 9f25b19d47035e54a0375878f7d452c5a082f802
PR113_STATUS = MERGED
PR113_MERGE_COMMIT = 44758af78c967d3a3c34ca2f7ec9dfb0fc9df0b8
MAIN_TIP = 44758af78c967d3a3c34ca2f7ec9dfb0fc9df0b8

UX_R2_DISCOVERY_AND_SCOPE_STATUS = MERGED
UX_R2_DISCOVERY_AND_SCOPE_DECISION = SCOPE_RECOMMENDED
UX_R2_RECOMMENDED_DIRECTION = D_EVIDENCE_AND_AUDIT_EXPLORER

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

UX_R1_RELEASE_STATUS = CLOSED
UX_R1_RELEASE_ACCEPTANCE_STATUS = ACCEPTED
UX_R1_RELEASE_SCOPE = FIXTURE_BACKED_READ_ONLY

REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 44758af78c967d3a3c34ca2f7ec9dfb0fc9df0b8
ANALYZED_AT = 2026-07-21T15:20:15Z
ANALYZED_BY = cursor-agent
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
NEXT_RECOMMENDED_TASK = UX_R2_I1_EVIDENCE_EXPLORER_IMPLEMENTATION
NEXT_ITEM = UX_R2_I1_EVIDENCE_EXPLORER_SEPARATE_IMPLEMENTATION_TASK
```

G1 note: **AUTHORIZED_WITH_CONDITIONS** authorizes only a **future separate** Evidence Explorer implementation prompt under the boundary below. This assessment does **not** flip any implementation, product-code, fixture, ViewModel, real-data, repository-read, validation, peeking, host, scheduler, R4 or R5 flags to true.

## MANDATORY_CONSTRAINTS

```text
ASSESSMENT_ONLY = true
NO_PRODUCT_CODE_CHANGES = true
NO_NEW_SCREENS = true
NO_RUNTIME_REPOSITORY_ACCESS = true
NO_RAW_FILESYSTEM_ACCESS = true
NO_REAL_DATA = true
NO_FUTURE_UNSEEN_RESULTS = true
NO_VALIDATION_EXECUTION = true
NO_EFFECT_PEEKING = true
NO_OPERATIONAL_ACTIONS = true
NO_SCIENTIFIC_INTERPRETATION_CHANGE = true
NO_R4_OR_R5_STATE_CHANGE = true
PARALLEL_TASKS_ALLOWED = false
```

## SUMMARY

UX-R2 discovery (PR #112/#113) recommended **D_EVIDENCE_AND_AUDIT_EXPLORER**. Planned nav **Evidências** exists inactive under Governança. I1 can safely authorize a **fixture-backed, read-only, curated-manifest Evidence Explorer** with list+detail, dedicated ViewModel+fixture, synthetic disclosure, summary/metadata only — without runtime repo/FS access, downloads, raw Markdown rendering of repository files, scientific numeric result tables, future-unseen payloads, validation, or operational controls.

Preferred prompt candidate route `/evidence` is adjusted to **`/governance/evidence`** to match namespaced routes (`/operations/*`, `/experiments/*`, `/future-collection/*`) and the Governança nav group. Bare `/evidence` is rejected for I1.

## 1. Candidate implementation postures

| ID | Posture | I1 disposition |
|----|---------|----------------|
| A | Static fixture-backed evidence catalog | **RECOMMENDED / AUTHORIZED_WITH_CONDITIONS** |
| B | Build-time catalog from approved docs | Deferred — needs generator gate + allowlist |
| C | Runtime read-only curated manifest | Deferred — `REPOSITORY_FILE_READ` HIGH |
| D | Runtime direct filesystem browsing | **BLOCKED** — path traversal / disclosure |
| E | Governed backend evidence-index API | Deferred — backend out of I1 |
| F | Hybrid fixture + approved-doc metadata | Deferred after A proven |

## 2. Explicit authorization answers

1. **First user journey:** Open Evidências → see curated evidence list (synthetic) → open one detail → read summary/metadata/known/unknown/limitations → leave without any action that changes state.
2. **List vs detail:** **List + detail** required.
3. **Route / nav:** `/governance/evidence` · **Evidências** (activate planned nav item only).
4. **Allowed evidence classes:** `release_record`; `implementation_handoff`; `impact_assessment`; `technical_scientific_review`; `experiment_specification`; `validation_report` (historical/audited illustrative only); `collection_readiness_evidence` (status metadata only); `operational_debt_record`.
5. **Allowed paths / file types (as metadata strings only in I1):** illustrative `sourcePath` under documented prefixes `docs/releases/`, `docs/ai-impact/`, `docs/ai-reviews/`, `docs/ai-specs/`, `docs/audits/`, `reports/ai-implementation/` — **not opened at runtime**. File types as labels only: `.md`, `.json` (metadata). **Forbidden path prefixes in fixture content:** `reports/r3e_future_unseen/` result payloads, `.env`, secrets, credentials, private keys.
6. **Content policy:** **Describe + summarize** via fixture fields. Do **not** render repository file bodies.
7. **Raw Markdown rendering of repo files:** **Not allowed** in I1.
8. **Repository-relative links:** Display as **non-navigating text** (copyable path). No auto-navigation to raw files. No external links in I1 fixture content.
9. **Download:** **Not allowed**.
10. **Search:** Optional client-side over approved metadata only: `title`, `evidenceClass`, `release`, `increment`, `experimentId`, `status`, `dataOrigin`.
11. **Filters:** Allowed exact fields: `evidenceClass`, `release`, `status`, `scientificStage`, `dataOrigin`.
12. **Scientific numeric results:** **Not allowed** in I1 (no tables of metrics/PnL/edge). Status codes and governance flags only.
13. **Stale labeling:** Require `freshnessLabel` ∈ {`CURRENT`, `HISTORICAL`, `STALE`, `UNKNOWN`}; UI must show non-CURRENT conspicuously.
14. **State distinction:** Require `dataOrigin` ∈ {`SYNTHETIC_ILLUSTRATIVE`, `HISTORICAL_AUDITED`, `EXPLORATORY_RECORDED`, `GOVERNANCE_RECORD`} and `scientificStage` ∈ {`NOT_APPLICABLE`, `AUDITED_COMPLETE`, `EXPLORATORY_COMPLETE`, `PENDING_FUTURE_UNSEEN`, `BLOCKED`}. Future-unseen **payloads** forbidden; pending gate may appear only as status text.
15. **R3D vs R3E:** Separate `experimentId` / `scientificStage`; never merge conclusions; preserve `R3D_RESULT=NO_MEASURABLE_EDGE` vs `R3E_GATE=PENDING_FUTURE_UNSEEN_DATA`.
16. **FU / peeking prevention:** No fixture rows sourced from `reports/r3e_future_unseen/*` observation/result bodies; architecture tests forbid imports of future-unseen modules; boundary tests assert absence of FU payload fields.
17. **Path traversal prevention:** No runtime FS/repo access in I1; `sourcePath` is display metadata validated against allowlist prefix regex in fixture tests; reject `..`, absolute paths, URLs.
18. **Unsafe content prevention:** No HTML/Markdown-from-repo rendering; no `dangerouslySetInnerHTML`; no script tags; summaries are plain text/structured fields only.
19. **Dedicated ViewModel:** **Required**.
20. **Dedicated fixture/manifest:** **Required** (synthetic curated catalog).
21. **Backend code:** **Not required** for I1.
22. **Runtime repository/file access:** **Not required / not allowed** for I1.
23. **Data classification:** All I1 rows `SYNTHETIC_ILLUSTRATIVE` (or explicitly labeled historical governance records still synthetic in fixture). Secrets class never present. Allowlist of classes/fields as above.
24. **A11y / responsive / tests:** Screen a11y tests; responsive layout; architecture boundary tests; ViewModel unit tests; fixture contract tests; no fabricated metrics assertions.
25. **Out of scope I1:** real-data adapters; repo/FS reads; downloads; raw MD render; Approvals workflow; host/scheduler; collection/validate; FU results; numeric scientific tables; backend API; other planned nav items; R4/R5.
26. **Later increment for real evidence:** Separate HIGH-risk assessment for posture **B or C** (build-time or runtime curated manifest) with security review, path allowlist, secret scanning, and explicit FU exclusions — not authorized here.

## 3. Security assessment

| Risk | Prevention | Test evidence |
|------|------------|---------------|
| Path traversal | No runtime FS; path metadata allowlist; reject `..` | fixture contract + unit tests |
| Arbitrary file disclosure | No file open/read APIs | architecture boundary tests |
| Secret/credential exposure | Forbidden path/field classes; no env rendering | fixture audit test |
| Unsafe MD/HTML | No repo MD render; no HTML injection | screen tests + lint patterns |
| Script execution | No script embedding; React text nodes only | a11y/screen tests |
| External-link safety | No external hrefs in I1 | fixture link policy test |
| Stale evidence | Mandatory freshness label | ViewModel tests |
| Misclassification | Enum-constrained fields | fixture schema tests |
| Fabricated metadata | Only status codes / known governance facts; no invented metrics | review checklist + tests |
| FU result leakage | Ban FU payload paths/fields | boundary + fixture tests |
| Effect peeking | No validate/collection actions; read-only UI | architecture tests |
| Scientific-context collapse | Separate evidence/interpretation sections; no approval CTA | screen copy tests |
| R3D/R3E conflation | Distinct experiment fields + copy | screen tests |
| False approval / prod-ready | No approve buttons; synthetic disclosure; no readiness claims | screen tests |

## 4. Recommended implementation boundary (for future I1 impl)

```text
ROUTE = /governance/evidence
NAV_LABEL = Evidências
NAV_ACTIVATION = PLANNED_EVIDENCE_ITEM_ONLY

READ_ONLY = true
FIXTURE_BACKED = true
CURATED_MANIFEST_ONLY = true
LIST_AND_DETAIL = true
VISIBLE_FIXTURE_SELECTOR = false
RUNTIME_REPOSITORY_ACCESS = false
RAW_FILESYSTEM_ACCESS = false
REAL_DATA = false
FUTURE_UNSEEN_RESULTS = false
VALIDATION_EXECUTION = false
EFFECT_PEEKING = false
OPERATIONAL_ACTIONS = false
DOWNLOADS = false
RAW_MARKDOWN_REPO_RENDERING = false
SCIENTIFIC_NUMERIC_RESULTS = false
BACKEND_REQUIRED = false
DEDICATED_VIEWMODEL_REQUIRED = true
DEDICATED_FIXTURE_REQUIRED = true
SYNTHETIC_DISCLOSURE_REQUIRED = true
```

### Allowed metadata fields

```text
evidenceId, title, evidenceClass, release, increment, experimentId,
status, dataOrigin, scientificStage, freshnessLabel, createdAtOrUnknown,
sourcePath, summary, supports, limitations, knownState, unknownState,
governanceFlags
```

## 5. Required pre-implementation gates

```text
G0_THIS_AUTH_ASSESSMENT_MERGED
G1_SEPARATE_HUMAN_IMPLEMENTATION_PROMPT
G2_ARCHITECTURE_BOUNDARY_TESTS_EXTENDED
G3_FIXTURE_CONTRACT_AND_A11Y_GATES
G4_NO_REAL_DATA_OR_REPO_READ_FLAGS
```

## 6. Scientific and operational truth (unchanged)

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
SCIENTIFIC_CONCLUSION = UNCHANGED
```

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```

## 7. Decision

```text
DECISION = AUTHORIZED_WITH_CONDITIONS
RECOMMENDED_IMPLEMENTATION_POSTURE = A_STATIC_FIXTURE_BACKED_EVIDENCE_CATALOG
NEXT_RECOMMENDED_TASK = UX_R2_I1_EVIDENCE_EXPLORER_IMPLEMENTATION
UX_R2_I1_IMPLEMENTATION_AUTHORIZED = false
EVIDENCE_EXPLORER_IMPLEMENTATION_AUTHORIZED = false
```
