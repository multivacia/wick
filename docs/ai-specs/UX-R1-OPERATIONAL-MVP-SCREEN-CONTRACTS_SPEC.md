# UX-R1 — Operational MVP Screen Contracts Spec

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B3
TASK_ID = OPERATIONAL-MVP-SCREEN-CONTRACTS-001
DOCUMENT = UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS_SPEC
DOCUMENT_VERSION = 1.0.0
PHASE = SPECIFICATION_AND_IMPACT_ASSESSMENT
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS-001_IMPACT_ASSESSMENT.md
IMPLEMENTATION_STATUS = SPECIFICATION_COMPLETE
IMPLEMENTATION_AUTHORIZED = true
UI_IMPLEMENTATION_AUTHORIZED = false
UX_B3_IMPLEMENTATION_AUTHORIZED = false
DESIGN_SYSTEM_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
EFFECTIVE_AT = 2026-07-19T13:45:00Z
```

## 1. Purpose

Define read-only screen contracts for the four approved MVP operational screens so a future UI can render accurate operational state without inventing scientific or economic meaning.

```text
IMPLEMENTATION_AUTHORIZED=true authorizes only these specification artifacts.
UI code remains prohibited until UX_B3_IMPLEMENTATION_AUTHORIZED and UI_IMPLEMENTATION_AUTHORIZED are explicitly true.
```

## 2. Information architecture

Aligns with `docs/ux/WICK_INFORMATION_ARCHITECTURE.md`.

### Primary navigation (MVP)

| Nav item | Route key (contract) | Screen |
|----------|----------------------|--------|
| Visão Geral | `/` or `/overview` | Visão Geral |
| Execuções | `/collection/runs` | Execuções |
| Prontidão | `/collection/readiness` | Readiness |
| Host e Automação | `/ops/host` | Host e Scheduler |

Mobile bottom nav: Início → Coleta → Prontidão → Operação → Mais.

### Screen-to-screen links

| From | To | Trigger |
|------|----|---------|
| Visão Geral | Execuções | “Última execução” / timeline item |
| Visão Geral | Readiness | readiness summary card |
| Visão Geral | Host | host/scheduler pills |
| Execuções detail | Readiness | readiness before/after |
| Execuções detail | raw artifact | open evidence |
| Readiness | Execuções | last evaluation run |
| Host | Visão Geral | back / next safe action |

Deep links must preserve filters in URL query (see Navigation).

## 3. Cross-cutting safety rules

Terminology and microcopy for status labels, empty states, failures/warnings, and scientific/economic guardrails are owned by **UX-B4** (authoritative after PR #42 merge):

```text
docs/ux/UX-R1-OPERATIONAL-LANGUAGE-GUIDE.md
docs/ux/UX-R1-STATUS-MESSAGE-CATALOG.md
docs/ux/UX-R1-EMPTY-STATE-CATALOG.md
docs/ux/UX-R1-FAILURE-AND-WARNING-MICROCOPY.md
docs/ux/UX-R1-SCIENTIFIC-AND-ECONOMIC-LANGUAGE-GUARDRAILS.md
```

UX-B3 screen contracts must **consume** UX-B4 wording. Do not duplicate or overwrite UX-B4 catalogs.

1. `NOT_READY` must not appear as system failure (visual semantic ATTENTION, not ERROR).
2. Green / SUCCESS must not imply profit or edge.
3. Blocked scientific state (`R3E_GATE`, `R4_STATUS`, `VALIDATE_AUTHORIZED=false`) must remain visible.
4. Activation debt must appear as deferred/open/blocked — never completed.
5. All timestamps include timezone (prefer ISO-8601 with offset).
6. Unavailable data must be explicit (`UNAVAILABLE` / `EMPTY` / `PARTIAL`), never fabricated.
7. No destructive or mutating actions in MVP contract.
8. Fixtures always labeled `DADOS_DEMONSTRATIVOS` / `DEMONSTRATION DATA`.
9. Economic metrics prohibited (return, accuracy, risk-adjusted return ratios, P&amp;L).

### Readiness language (mandatory)

```text
NOT_READY = ainda não há dados suficientes ou critérios atendidos
BLOCKED   = uma condição impede prosseguir
ERROR     = falha real de execução ou integridade
READY     = critérios formais atendidos, sem autorizar validate automaticamente
```

## 4. Screen contract — Visão Geral

### Purpose

Answer:

```text
O sistema está coletando?
A coleta está saudável?
Os dados estão prontos?
Existe algum bloqueio?
Qual é a próxima ação segura?
```

### Information blocks

| Block | Required | Notes |
|-------|----------|-------|
| overall operational state | yes | composed collection + readiness + host + scheduler |
| last completed execution | yes | from automation_state / cycle reports |
| last failed execution | yes | null → EMPTY, not fabricated |
| future-unseen store summary | yes | observation counts + cutoff |
| readiness summary | yes | status + primary reason |
| host state | yes | known / unknown / DEFERRED |
| scheduler state | yes | must show not activated |
| open incidents | yes | EMPTY if no incident store; do not invent |
| open operational debt | yes | fixed OPEN constellation |
| scientific gate state | yes | R3E_GATE + VALIDATE_AUTHORIZED |
| next safe action | yes | DERIVED_READ_ONLY |

### Overall state composition (deterministic)

Priority (highest first):

1. ERROR if last cycle `FAILED` or critical integrity blocker present
2. BLOCKED if scientific/ops blocker (`blockers[]` non-empty with hard codes, or scheduler forbidden action requested)
3. ATTENTION / NOT_READY if readiness `NOT_READY`
4. DEGRADED if collection warnings / provider_failures without hard fail
5. HEALTHY_COLLECTION only if recent cycle COMPLETE/PARTIAL/NO_NEW_DATA and no hard errors — still show NOT_READY separately
6. UNKNOWN if core artifacts missing

Never map NOT_READY → ERROR.

### Next safe action rules (derived)

| Condition | Next safe action (plain language) |
|-----------|-----------------------------------|
| HOST_DISCOVERY missing | Executar discovery no host persistente (runbook) |
| Scheduler prepared but not authorized | Manter scheduler inativo; completar checklist |
| readiness NOT_READY window/series | Continuar coleta; aguardar critérios |
| last cycle FAILED | Investigar execução falha (abrir Execuções) |
| readiness READY and VALIDATE_AUTHORIZED=false | Não executar validate; aguardar autorização humana |
| All quiet + collecting | Nenhuma ação urgente; monitorar próxima coleta |

### Prohibited on this screen

- profit / edge claims
- “sistema pronto para operar capital”
- auto-start validate CTA
- showing scheduler as active

## 5. Screen contract — Execuções

### Purpose

List and inspect collection / automation executions with evidence links.

### List fields

| Field | User label | Technical |
|-------|------------|-----------|
| run_id | ID da execução | `run_id` / `collection_run_id` |
| status | Status | `status` / `run_status` |
| started_at | Início | `started_at` |
| finished_at | Fim | `finished_at` |
| duration | Duração | derived |
| trigger_type | Origem | MANUAL / SCHEDULER / DRY_RUN / UNKNOWN |
| host_identity | Host | from lock/discovery (masked) |
| command_type | Comando | run-cycle / collect / dry-run |
| observations_accepted | Barras aceitas | `observations_accepted` / persist accepted |
| observations_rejected | Barras rejeitadas | `observations_rejected` |
| readiness_transition | Prontidão | `readiness_transition` |
| failure_category | Categoria de falha | taxonomy code |

### Detail fields (additional)

```text
store_before / store_after
idempotency_status / idempotency_run_id
readiness_status before/after (from cycle + nested readiness_report)
warnings (provider_failures soft, gap informational)
failures (hard_error, timed_out, rejections)
lock result (lock object / SKIPPED_LOCKED)
backup evidence (link if present; else UNAVAILABLE)
artifact links (run_dir, cycle_report, collection_run, series_status, rejections, hash_manifest, readiness_report)
```

### Filtering / sorting

| Filter | Values |
|--------|--------|
| date range | on `started_at` (UTC) |
| status | COMPLETE, PARTIAL, NO_NEW_DATA, BLOCKED, FAILED, SKIPPED_LOCKED, … |
| trigger | MANUAL, SCHEDULER, DRY_RUN, UNKNOWN |
| host | masked host id / UNKNOWN |
| command | run-cycle, collect, dry-run |
| failure category | taxonomy codes |
| readiness transition | e.g. `NOT_READY->NOT_READY` |

Default sort: `started_at` descending.

### Pagination and retention

```text
page_size_default = 25
page_size_max = 100
offset/cursor = offset OK for MVP contract
retention = do not invent runs; only evidence present under reports/r3e_future_unseen/
retention_policy_reference = ops retention scripts (display note only)
```

Do not invent historical executions not present in evidence.

### Trigger type derivation

| Evidence | trigger_type |
|----------|--------------|
| `dry_run_only=true` or dry_run artifacts | DRY_RUN |
| systemd timer / scheduler metadata says activated trigger | SCHEDULER (only if real evidence) |
| manual CLI / no scheduler evidence | MANUAL |
| insufficient metadata | UNKNOWN |

While `SCHEDULER_ACTIVATION=BLOCKED`, do not label runs as SCHEDULER unless artifact explicitly proves timer firing (currently none should).

## 6. Screen contract — Readiness

### Purpose

Explain formal readiness criteria and scientific gate consequences without implying validation success.

### Required fields

```text
current readiness_status
blocking reasons (blockers[])
not_ready_reasons[]
window_days / required_window_days
minimum required days (= required_window_days)
series completeness (series_complete / required_series / series_partial / series_missing / series_blocked)
coverage (series_counts, eligible_series, n_observations_total)
freshness (as_of, generated_at)
gaps (gap_status)
duplicates (duplicates_flagged)
store integrity (hash_status, manifest_status)
last readiness evaluation (generated_at + derived_from_run)
historical readiness evaluations (per automation_runs/*/readiness_report.json when present)
READY transition evidence (only if status became READY with run evidence)
scientific gate consequence (scientific_safety block)
```

### Scientific gate consequence copy (mandatory when READY or not)

```text
READY does not authorize validate.
VALIDATE_AUTHORIZED remains false until explicit human authorization.
R3E_GATE remains PENDING_FUTURE_UNSEEN_DATA until future validation completes under protocol.
ECONOMIC_INTERPRETATION_ALLOWED remains false.
R4_STATUS remains BLOCKED.
```

### Progress presentation

- Window progress: `window_days / required_window_days` (cap display at 100% only when ≥ required).
- Series progress: `len(series_complete) / required_series` and `series_with_min_bars`.
- Bars threshold: `required_min_bars` (200) as technical detail.

## 7. Screen contract — Host e Scheduler

### Purpose

Show host strategy and scheduler preparation without representing the scheduler as active.

### Required fields

```text
host_strategy
host_identity
host_discovery_status
operational_debt_status
durable_store_path_state
log_path_state
backup_path_state
lock_path_state
scheduler_type
scheduler_registered
scheduler_enabled
scheduler_last_trigger
scheduler_next_trigger
scheduler_health
manual_run_availability
activation_authorization_state
```

### Current debt representation (mandatory defaults until evidence changes)

```text
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
scheduler_enabled = false
scheduler_registered = false (templates prepared ≠ registered/enabled on host)
activation_authorization_state = NOT_AUTHORIZED
```

### Path states

| Path kind | Source | Empty behavior |
|-----------|--------|----------------|
| durable store | discovery result / docs template `$HOME/wick-r3e` | UNAVAILABLE if discovery missing |
| logs | `$WICK_ROOT/logs` pattern | UNAVAILABLE |
| backups | `backups/` or configured backup root | UNAVAILABLE (not FAIL) |
| lock | `reports/.../automation.lock` via lock-status | ABSENT is normal idle |

### Manual run availability

Informational only: contract may state that CLI manual `run-cycle` exists on ops host. UI must **not** enable an execute button in this MVP.

## 8. Data provenance contract

Every field in the catalog declares:

```text
FIELD_NAME
USER_LABEL
TECHNICAL_LABEL
SOURCE_TYPE
SOURCE_PATH
SOURCE_FIELD
TRANSFORM
FRESHNESS
NULL_BEHAVIOR
EMPTY_STATE
ERROR_STATE
SECURITY_CLASSIFICATION
SCIENTIFIC_SAFETY_NOTE
```

Allowed SOURCE_TYPE values:

```text
REPOSITORY_DOCUMENT
RUN_ARTIFACT
STORE_METADATA
READINESS_REPORT
SCHEDULER_METADATA
HOST_DISCOVERY_RESULT
DERIVED_READ_ONLY
DEMONSTRATION_FIXTURE
```

Canonical catalog: `docs/ux/UX-R1-OPERATIONAL-MVP_DATA-CONTRACT-CATALOG.md`.

## 9. State matrix

Canonical matrix: `docs/ux/UX-R1-OPERATIONAL-MVP_STATE-MATRIX.md`.

Per-screen states to support:

```text
LOADING
EMPTY
PARTIAL
STALE
UNAVAILABLE
ERROR
BLOCKED
NOT_READY
READY
```

Each state includes: plain-language message, technical detail, visual semantic, allowed actions, prohibited implications.

## 10. Fixture scenarios

Canonical catalog: `docs/ux/UX-R1-OPERATIONAL-MVP_SAFE-FIXTURE-CATALOG.md`.

Required scenarios:

```text
healthy_collection_not_ready
collection_warning
collection_failure
host_discovery_deferred
scheduler_not_activated
readiness_ready_but_validation_not_authorized
no_execution_history
partial_metadata
```

Every fixture:

```text
fixture_id
fixture_label = DADOS_DEMONSTRATIVOS
scenario
source = SYNTHETIC
scientific_interpretation_allowed = false
economic_interpretation_allowed = false
```

No executable fixture files in this task.

## 11. Navigation and interaction contract

### URL / filters

```text
/collection/runs?status=FAILED&from=...&to=...&trigger=MANUAL&page=1
/collection/runs/:run_id
/collection/readiness
/ops/host
```

### Behaviors

| Behavior | Contract |
|----------|----------|
| back | browser history; detail → list preserves filters |
| refresh | manual refresh control on all screens |
| auto-refresh | default OFF; if enabled later ≥ 60s + stale banner |
| loading | skeleton/plain “Carregando estado operacional…” |
| stale-data warning | if artifact `generated_at`/`updated_at` older than threshold (default 6h for overview) |
| copy technical ID | allowed (run_id, batch_id) |
| download evidence | read-only download of existing artifact |
| open raw artifact | opens/local viewer of JSON evidence |
| destructive actions | none enabled |
| run collect / validate / activate | prohibited |

## 12. Accessibility and responsive behavior

Target: WCAG 2.2 AA.

| Concern | Contract |
|---------|----------|
| desktop layout | sidebar nav + main landmark; overview cards as summary list regions |
| tablet layout | collapsible nav; tables scroll horizontally or stack |
| mobile layout | bottom nav; stacked sections; tables → definition lists |
| keyboard order | skip link → nav → status → main → complementary |
| landmarks | `banner`, `navigation`, `main`, `complementary`, `contentinfo` |
| heading hierarchy | one `h1` per screen; sections `h2`; cards `h3` |
| table alternative | mobile stacked list with same data |
| status non-color cue | icon + text label (ex.: “Não pronto”) |
| long SHA/path wrapping | `overflow-wrap: anywhere`; copy button |
| touch targets | ≥ 44×44 CSS px |
| zoom | usable at 200% |
| reduced motion | no essential info only in motion; respect `prefers-reduced-motion` |

## 13. Security and privacy

### Classification

| Class | Examples | Render rule |
|-------|----------|-------------|
| PUBLIC_OPERATIONAL | readiness_status, run status, window_days | visible |
| INTERNAL_OPERATIONAL | run_id, batch_id, masked paths | visible |
| SENSITIVE | hostname, username, full filesystem paths | mask by default |
| SECRET | tokens, provider credentials, env values | never render |

### Masking rules

| Data | Mask |
|------|------|
| usernames | `u***` or `REDACTED_USER` |
| hostnames | `host-***` |
| filesystem paths | show basename + `…/` prefix mask |
| environment variable values | never |
| tokens / credentials | never |
| stack traces | collapsed “detalhe técnico disponível no artefato” |
| internal identifiers | run_id OK; secrets in logs redacted |
| downloadable evidence | strip secret files; verification must assert `secret_files_absent` |

## 14. Read-only adapter recommendation

See impact assessment. Spec locks:

```text
RECOMMENDED_DATA_ACCESS = GENERATED_OPERATIONAL_INDEX_PLUS_CLI_READ_ONLY
SCOPE = ARCHITECTURAL_RECOMMENDATION_ONLY
INDEX_ARTIFACT_NAME = ops_ui_index_v1.json (future; not created in this task)
INDEX_GENERATED_IN_THIS_TASK = false
ADAPTER_IMPLEMENTED_IN_THIS_TASK = false
API_IMPLEMENTED_IN_THIS_TASK = false
CLI_FALLBACKS = history, lock-status, backup-verify (read-only)
FUTURE_REQUIREMENT = separate impact assessment + authorization before building index/adapter/API
```

Proposed index sections (future DTO, not implemented):

```text
overview
executions[]
execution_details[run_id]
readiness
host_scheduler
provenance
generated_at
source_heads[]
```

## 14.1 Parallel-track integration boundaries

```text
UX-B2 = future frontend / design-system architecture (I1 auth MERGED; execution blocked)
UX-B3 = screen and data contracts (this document)
UX-B4 = terminology and microcopy (authoritative; PR #42 MERGED)
```

UX-B3 consumes UX-B4 catalogs for user-facing wording and does not duplicate them. UX-B3 does not require UX-B2 I1 execution to remain valid as a specification. Future UI implementation must consume approved B2+B3+B4 outputs.

## 15. Acceptance criteria

1. Four screen contracts defined with purpose, blocks, safety rules.
2. Field provenance catalog complete for required fields.
3. State matrix covers collection/readiness/scheduler/host/freshness/incident combinations.
4. Safe fixture catalog covers eight required scenarios without economic metrics.
5. Navigation/interaction is read-only only.
6. Accessibility and responsive contracts documented per screen family.
7. Security classification and masking defined.
8. Adapter options assessed; D+B recommended.
9. Impact assessment APPROVED; UI implementation still false.
10. PROJECT/backlog status updated; R3E scientific state unchanged.
11. Governance validator / pytest / ruff pass.

## 16. Non-goals (reaffirmed)

No frontend code, routes, components, CSS, tokens, JS deps, API clients, backend behavior changes, collect/run-cycle/validate execution, scheduler activation, inferred missing ops data, fabricated metrics, R4/R5 unblock.
