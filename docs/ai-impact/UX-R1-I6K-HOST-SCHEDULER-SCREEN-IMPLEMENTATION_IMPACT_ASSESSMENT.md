# UX-R1-I6K-HOST-SCHEDULER-SCREEN-IMPLEMENTATION — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = HOST-SCHEDULER-SCREEN-IMPLEMENTATION-AUTHORIZATION-ASSESSMENT-001
TASK_ID = HOST-SCHEDULER-SCREEN-IMPLEMENTATION-001
TITLE = Host and Automation Screen Implementation
INCREMENT = I6K
PHASE = IMPLEMENTATION
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = true
HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED = true
HOST_SCHEDULER_SCREEN_MERGE_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
REAL_HOST_DISCOVERY_AUTHORIZED = false
REAL_DATA_INTEGRATION_AUTHORIZED = false
CREDENTIAL_ACCESS_AUTHORIZED = false
OPERATIONAL_ACTIONS_AUTHORIZED = false
SCHEDULER_ACTIVATION_AUTHORIZED = false
COLLECTION_ACTIONS_AUTHORIZED = false
RUN_NOW_AUTHORIZED = false
REMOTE_COMMANDS_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
COLLECTION = IN_PROGRESS
READINESS = NOT_READY
READINESS_REASON = WINDOW_DAYS_INSUFFICIENT
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE_CHANGE = false
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = e6444111c921094e81353ae09ff4a69a9480995d
FINAL_CANDIDATE_HEAD = 4b338852196f80314875bdf8a994e19cc8ad0f3a
CONTENT_REVIEWED_THROUGH_HEAD = 4b338852196f80314875bdf8a994e19cc8ad0f3a
POST_REVIEW_NORMATIVE_CHANGES = 0
ANALYZED_AT = 2026-07-20T23:57:00Z
ANALYZED_BY = cursor-agent
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTHORIZATION_DECISION = HUMAN_AUTHORIZED_FOR_THIS_TASK
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
FRONTEND_LOCATION = web/
I6J_DECISION = AUTHORIZED_WITH_CONDITIONS
I6J_RECOMMENDED_IMPLEMENTATION_BOUNDARY = HOST_SCHEDULER_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; NO_VISIBLE_FIXTURE_SELECTOR; NO_REAL_HOST_DISCOVERY; NO_REAL_DATA; NO_CREDENTIALS; NO_SCHEDULER_ACTIVATION; NO_COLLECTION_ACTIONS; NO_RUN_NOW; NO_OPERATIONAL_COMMANDS; NO_SCIENTIFIC_STATE_CHANGE
FIXTURE_ID = current_project_state_illustrative
ROUTE = /operations/host-scheduler
SCREEN = Host e Automação
```

G1 note: authorization covers **only** the read-only fixture-backed Host e Automação screen (`/operations/host-scheduler`). It does **not** authorize real host discovery, credentials, scheduler activation, collection/run-now controls, real-data adapters, or scientific state changes. Overview, Runs and Readiness remain preserved.

## MANDATORY_CONSTRAINTS

```text
READ_ONLY = true
FIXTURE_BACKED = true
FIXTURE_ID = current_project_state_illustrative
NO_VISIBLE_FIXTURE_SELECTOR = true
NO_REAL_HOST_DISCOVERY = true
NO_REAL_DATA = true
NO_CREDENTIALS = true
NO_SCHEDULER_ACTIVATION = true
NO_COLLECTION_ACTIONS = true
NO_RUN_NOW = true
NO_OPERATIONAL_COMMANDS = true
NO_NETWORK_CLIENTS = true
NO_BACKEND_API = true
NO_EXTRA_RUNTIME_OR_DEV_DEPENDENCIES = true
TOKEN_ONLY_STYLING = true
REUSE_I3_PRIMITIVES = true
CONSUME_I6B_VIEWMODELS = true
CONSUME_I6C_FIXTURES = true
REPLACE_HOST_SCHEDULER_PLACEHOLDER_ONLY = true
PRESERVE_OVERVIEW_SCREEN = true
PRESERVE_RUNS_SCREEN = true
PRESERVE_READINESS_SCREEN = true
DEFERRED_IS_NOT_COMPLETE = true
DEFERRED_IS_NOT_FAILED = true
BLOCKED_IS_NOT_FAULT = true
UNKNOWN_IS_NOT_OFFLINE = true
NOT_CONFIGURED_IS_NOT_FAILED = true
SCHEDULER_INACTIVE_IS_NOT_FAILED = true
MISSING_IS_NOT_FALSE = true
MISSING_IS_NOT_ZERO = true
ILLUSTRATIVE_IS_NOT_OPERATIONAL = true
RED_ONLY_FOR_CONFIRMED_FAULT = true
NO_FABRICATED_HOSTNAME_IP_PATH_CADENCE_NEXTRUN = true
OFFICIAL_OPERATIONAL_DEBT_WORDING_REQUIRED = true
WCAG_2_2_AA = true
PARALLEL_TASKS_ALLOWED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## SUMMARY

Implement the Wick product screen Host e Automação at `/operations/host-scheduler`, consuming merged `HostSchedulerViewModel` + synthetic fixture catalog + shell/router + tokens + accessible primitives. Read-only. Clearly labeled synthetic. No real host access. No credentials. No scheduler activation. No operational controls. Fields absent from the ViewModel (hostname, cadence, next expected run, paths) must remain explicitly unavailable — never fabricated.

## 1. Objetivo

Entregar a tela Host e Automação com PageHeader, SyntheticDataNotice, HostDiscoveryStatus, OperationalDebtNotice, SchedulerStatus, KnownEnvironmentDetails (somente indisponibilidade explícita quando ausente do VM), CadenceState (indisponível se ausente), LastKnownRun, NextExpectedRun (indisponível se ausente), BlockingReason, NextSafeHumanAction, EvidenceReference e PartialUnknownState; testes de rota, a11y e fronteira; sem descoberta real, credenciais, ativação ou comandos operacionais.

## 2. Contexto técnico

- I6J assessment MERGED (PR #100 → `b284a72`): AUTHORIZED_WITH_CONDITIONS / HOST_SCHEDULER_SCREEN_ONLY / fixture-backed / read-only.
- I6J post-merge closure MERGED (PR #101 → `e644411`).
- Human task authorizes I6K Host/Scheduler screen implementation only.
- I6B ViewModels MERGED; I6C fixtures MERGED; I5 shell MERGED; I6E/I6G/I6I screens MERGED.
- Screen mounts inside ApplicationShell outlet; replaces only `/operations/host-scheduler` placeholder.
- Product constellation preserved: HOST_DISCOVERY=DEFERRED, OPERATIONAL_DEBT=OPEN, SCHEDULER_ACTIVATION=BLOCKED.
- Official debt wording required when debt is open / discovery deferred.

## 3. Componentes afetados

| Componente | Impacto |
|------------|---------|
| `web/src/screens/host-scheduler/**` | Nova tela e componentes |
| `web/src/app/AppRoutes.tsx` | Troca placeholder Host pela tela real |
| `web/src/shell/navigation.ts` | Label nav → "Host e Automação" |
| `web/tests/screens/host-scheduler/**` | Testes de tela / fronteira |
| `web/tests/a11y/hostScheduler.a11y.test.tsx` | axe smoke |
| `web/tests/screens/overview|runs|readiness/**` | Ajuste: Host deixa de ser placeholder |
| `docs/PROJECT.md` | Estado I6K / flags / NEXT |
| Governance I6K | Impact / spec / review / handoff |
| Backend / R3E / scheduler / host | Não afetados |
| Overview / Runs / Readiness screens | Preservados |

## 4. Arquivos previstos

```text
web/src/screens/host-scheduler/**
web/src/app/AppRoutes.tsx
web/src/shell/navigation.ts
web/tests/screens/host-scheduler/**
web/tests/a11y/hostScheduler.a11y.test.tsx
web/tests/screens/overview/overviewScreen.test.tsx
web/tests/screens/runs/runsScreen.test.tsx
web/tests/screens/readiness/readinessScreen.test.tsx
docs/ai-impact/UX-R1-I6K-HOST-SCHEDULER-SCREEN-IMPLEMENTATION_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-I6K-HOST-SCHEDULER-SCREEN-IMPLEMENTATION_SPEC.md
docs/ai-reviews/UX-R1-I6K-HOST-SCHEDULER-SCREEN-IMPLEMENTATION_REVIEW.md
reports/ai-implementation/UX-R1-I6K-HOST-SCHEDULER-SCREEN-IMPLEMENTATION_HANDOFF.md
docs/PROJECT.md
```

## 5. Contratos e interfaces

```text
ROUTE = /operations/host-scheduler
SCREEN = HostSchedulerScreen
DATA = buildFixtureViewModels("current_project_state_illustrative").hostScheduler + metadata
VISIBLE_LABELS = "Dados ilustrativos" | "Synthetic fixture" | "Não representa evidência operacional real"
OFFICIAL_DEBT_WORDING = "Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída."
SECTIONS =
  PageHeader
  SyntheticDataNotice
  HostDiscoveryStatus
  OperationalDebtNotice
  SchedulerStatus
  KnownEnvironmentDetails
  CadenceState
  LastKnownRun
  NextExpectedRun
  BlockingReason
  NextSafeHumanAction
  EvidenceReference
  PartialUnknownState
STATUS_SEMANTICS = I2/I3 StatusBadge + I6B presentation mapping
ACTION_HINT = advisory text only; no operational buttons
PRODUCT_FIXTURE = current_project_state_illustrative
TEST_SCENARIOS = current_project_state_illustrative; host_discovery_deferred; scheduler_blocked_not_authorized; partial_unknown_data
VM_ONLY_FIELDS = true (no hostname/IP/path/cadence/next-run fabrication)
```

## 6. Persistência e dados

Nenhuma persistência. Fonte única: fixture sintético I6C via `buildFixtureViewModels`. Sem fetch, axios, WebSocket, filesystem runtime, localStorage operacional, env de descoberta de infraestrutura ou leitura de credenciais.

## 7. Concorrência, locks e idempotência

N/A backend. Montagem determinística do ViewModel a partir do fixture.

## 8. Segurança

```text
NO_SECRETS = true
NO_CREDENTIALS = true
NO_IPS = true
NO_SENSITIVE_PATHS = true
NO_AUTH = true
NO_OPERATIONAL_COMMANDS = true
NO_REMOTE_COMMANDS = true
pnpm audit --audit-level high required
NEW_RUNTIME_DEPENDENCIES = 0
NEW_DEV_DEPENDENCIES = 0
EVIDENCE_AS_TEXT_ONLY = true
```

## 9. Observabilidade

Sem telemetria. Testes unitários + axe smoke na rota Host/Scheduler + architecture boundary scan.

## 10. Operação

Não altera host discovery, scheduler, coleta, validate ou estado científico R3E. `nextSafeAction` é apenas texto consultivo. Débito operacional permanece OPEN; ativação permanece BLOCKED; descoberta permanece DEFERRED.

## 11. Rollback

```text
ROLLBACK = revert PR; restaurar PlaceholderPage em /operations/host-scheduler; remover web/src/screens/host-scheduler/**
NEVER via R3E / validate / scheduler / host discovery
```

## 12. Compatibilidade

- Consome I2 tokens, I3 primitives, I5 shell/outlet, I6B HostSchedulerViewModel, I6C fixture catalog.
- Overview, Runs e Readiness permanecem implementados.
- Nav label PT "Host e Automação" alinhado ao chrome da tela.

## 13. Testes necessários

```text
host-scheduler route renders real screen
synthetic notice visible
host discovery deferred distinct from complete and failed
scheduler blocked distinct from confirmed fault
operational debt wording visible
missing host identity not invented
missing environment/cadence/timestamps remain unavailable
unknown not rendered as offline
inactive not rendered as failed
no credentials, IPs or sensitive paths exposed
no operational controls / start/stop/retry/run-now/activate/install/configure
next safe human action is text-only
evidence reference does not fabricate a link
Overview / Runs / Readiness remain implemented
responsive + axe + architecture boundary
no visible fixture selector
```

## 14. Alternativas consideradas

| Alternativa | Decisão |
|-------------|--------|
| Descoberta real de host / SSH / IPs | REJECTED — not authorized |
| Credenciais / tokens / chaves | REJECTED — not authorized |
| Ativação / install / configure scheduler | REJECTED — not authorized |
| Controles start/stop/retry/run-now | REJECTED — read-only |
| Fabricar hostname/cadence/next-run | REJECTED — absent from VM |
| Seletor visível de fixtures | REJECTED — fixture fixo interno |
| Dados reais / API | REJECTED — not authorized |
| Implementar em paralelo com outras telas | REJECTED — PARALLEL_TASKS_ALLOWED=false |
| Dependências novas | REJECTED |

## 15. Riscos

| Risco | Severidade | Mitigação |
|-------|------------|-----------|
| Scope creep to real host / activation | HIGH | Route wiring limited; architecture boundary tests |
| Confusing synthetic with operational proof | HIGH | Mandatory SyntheticDataNotice + illustrative labels |
| DEFERRED rendered as COMPLETE/FAILED | HIGH | StatusBadge deferred + semantic copy + tests |
| BLOCKED rendered as FAULT/red | HIGH | purple/gray mapping + tests |
| Fabricated hostname/IP/path/cadence | HIGH | Explicit unavailable sections; no invented fields |
| Operational control buttons | HIGH | No buttons; advisory-only NextSafeHumanAction |
| Official debt wording omitted | MEDIUM | OperationalDebtNotice with canonical copy |

## 16. Questões abertas

```text
NONE_BLOCKING
MERGE = remains unauthorized until separate human merge authorization
ACTIVE_COMPLETE_FIXTURE = not required for product route; optional test-only only if needed
```

## 17. Decisão arquitetural recomendada

Screen module under `web/src/screens/host-scheduler/`; assemble ViewModel via I6C `buildFixtureViewModels("current_project_state_illustrative")`; reuse I3 primitives; token-only CSS; replace `/operations/host-scheduler` placeholder only; disclose absent B3 identity/cadence/next-run fields as unavailable; WCAG 2.2 AA; zero new dependencies.

## 18. Critérios para autorizar implementação

```text
1. This impact IMPACT_ASSESSMENT_STATUS = APPROVED
2. IMPLEMENTATION_AUTHORIZED = true
3. HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED = true (human task)
4. I6J AUTHORIZED_WITH_CONDITIONS assessment MERGED
5. Scope limited to Host/Scheduler screen + tests + governance
6. HOST_SCHEDULER_SCREEN_MERGE_AUTHORIZED remains false until human merge
```

All criteria satisfied for proceeding with I6K Host/Scheduler screen code in this task/PR.
