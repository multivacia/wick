# UX-R1-I6J-HOST-SCHEDULER-SCREEN-IMPLEMENTATION-AUTHORIZATION — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = I6_HOST_SCHEDULER_SCREEN_AUTHORIZATION_ASSESSMENT
TASK_ID = HOST-SCHEDULER-SCREEN-IMPLEMENTATION-AUTHORIZATION-ASSESSMENT-001
TITLE = Host and Automation Screen Implementation Authorization Assessment
INCREMENT = I6J
PHASE = AUTHORIZATION_ASSESSMENT
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
ASSESSMENT_ONLY = true
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_SCOPE = AUTHORIZATION_ASSESSMENT_DOCUMENTATION_ONLY
IMPLEMENTATION_EXECUTION_AUTHORIZED = false
DECISION = AUTHORIZED_WITH_CONDITIONS
RECOMMENDED_IMPLEMENTATION_BOUNDARY = HOST_SCHEDULER_SCREEN_ONLY; FIXTURE_BACKED; READ_ONLY; NO_VISIBLE_FIXTURE_SELECTOR; NO_REAL_HOST_DISCOVERY; NO_REAL_DATA; NO_CREDENTIALS; NO_SCHEDULER_ACTIVATION; NO_COLLECTION_ACTIONS; NO_RUN_NOW; NO_OPERATIONAL_COMMANDS; NO_SCIENTIFIC_STATE_CHANGE
SCREEN = Host e Automação
ROUTE = /operations/host-scheduler
HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
OPERATIONAL_ACTIONS_AUTHORIZED = false
SCHEDULER_ACTIVATION_AUTHORIZED = false
COLLECTION_ACTIONS_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
COLLECTION = IN_PROGRESS
READINESS = NOT_READY
READINESS_REASON = WINDOW_DAYS_INSUFFICIENT
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE_CHANGE = false
PR98_STATUS = MERGED
PR98_MERGE_COMMIT = 061c388950f2b1553a47cfa84e3ab56fd7ee906b
PR99_STATUS = MERGED
I6_READINESS_SCREEN_IMPLEMENTATION_STATUS = MERGED
I6_OVERVIEW_SCREEN_IMPLEMENTATION_STATUS = MERGED
I6_RUNS_SCREEN_IMPLEMENTATION_STATUS = MERGED
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 8a8444925696947dcf215fdc1d1754efcdea1bfd
FINAL_CANDIDATE_HEAD = 02a44530882e5dfaffa7feeeac0ebbab3ac8cfa0
CONTENT_REVIEWED_THROUGH_HEAD = 02a44530882e5dfaffa7feeeac0ebbab3ac8cfa0
POST_REVIEW_NORMATIVE_CHANGES = 0
ANALYZED_AT = 2026-07-20T23:30:00Z
ANALYZED_BY = cursor-agent
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
NEXT_RECOMMENDED_TASK = I6_HOST_SCHEDULER_SCREEN_IMPLEMENTATION
NEXT_ITEM = I6_HOST_SCHEDULER_SCREEN_SEPARATE_IMPLEMENTATION_TASK
```

G1 note: This assessment may recommend **AUTHORIZED_WITH_CONDITIONS** for a future Host/Scheduler-only screen task. It does **not** flip `HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED`, `IMPLEMENTATION_EXECUTION_AUTHORIZED`, `UI_SCREEN_IMPLEMENTATION_AUTHORIZED`, `SCHEDULER_ACTIVATION_AUTHORIZED`, or operational-data/action flags to true for product execution. Screen implementation requires a separate human-authorized implementation prompt. Real-host discovery and scheduler activation remain separately gated.

## SUMMARY

Prerequisites I2–I6I are merged (Overview, Runs, Readiness screens live). The project is ready to authorize a **narrow, fixture-backed, read-only Host e Automação screen** at `/operations/host-scheduler` that explains deferred discovery, blocked scheduler, and open operational debt — without claiming activation, discovering a real host, or exposing credentials/infrastructure secrets. B3 parity fields absent from `HostSchedulerViewModel` (hostname, paths, cadence, next trigger, HostGator, etc.) must not be fabricated.

Official operational wording to preserve:

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```

## 1. Objetivo

Avaliar se o projeto está pronto para autorizar uma tarefa separada de implementação da tela **Host e Automação** (`/operations/host-scheduler`), somente leitura e alimentada por fixtures, sem implementar a tela, sem descobrir host real e sem ativar scheduler nesta tarefa.

## 2. Contexto técnico

- I6I Readiness MERGED (PR #98 → `061c388`); post-merge closure MERGED (PR #99 → `8a84449`).
- `NEXT_RECOMMENDED_TASK` em `main` aponta para `I6_HOST_SCHEDULER_SCREEN_AUTHORIZATION_ASSESSMENT`.
- I6B `buildHostSchedulerViewModel` MERGED; I6C fixtures MERGED; I5 route placeholder `/operations/host-scheduler` MERGED.
- Estado oficial: `HOST_DISCOVERY=DEFERRED`, `OPERATIONAL_DEBT=OPEN`, `SCHEDULER_ACTIVATION=BLOCKED`, `R3E_COLLECTION_SCHEDULER=AWAITING_OPERATOR_DISCOVERY`.
- Runbooks/scripts de discovery existem (`docs/runbooks/R3E_LOCAL_HOST_DISCOVERY_*`, `scripts/r3e_local_host_discovery.*`) — referenciados, **não executados** nesta assessment.

## 3. Componentes afetados

| Componente | Impacto nesta tarefa |
|------------|----------------------|
| Docs I6J (impact/review/handoff) | Novos artefatos de autorização |
| `docs/PROJECT.md` | Resultado da assessment + NEXT |
| `web/src/screens/**` | Não modificado |
| Overview / Runs / Readiness | Preservados |
| Host placeholder | Preservado |
| Scheduler / R3E / discovery scripts | Não executados / não alterados |

## 4. Arquivos previstos

```text
docs/ai-impact/UX-R1-I6J-HOST-SCHEDULER-SCREEN-IMPLEMENTATION-AUTHORIZATION_IMPACT_ASSESSMENT.md
docs/ai-reviews/UX-R1-I6J-HOST-SCHEDULER-SCREEN-IMPLEMENTATION-AUTHORIZATION_REVIEW.md
reports/ai-implementation/UX-R1-I6J-HOST-SCHEDULER-SCREEN-IMPLEMENTATION-AUTHORIZATION_HANDOFF.md
docs/PROJECT.md
```

Futura implementação (fora desta PR): `web/src/screens/host-scheduler/**`, `AppRoutes.tsx` (somente placeholder Host), testes — apenas após prompt humano separado.

## 5. Contratos e interfaces

```text
ROUTE = /operations/host-scheduler
SCREEN = Host e Automação (nav atual: "Host e Scheduler")
DATA = HostSchedulerViewModel via buildFixtureViewModels
SUPPLIED_FIELDS =
  hostDiscoveryState
  hostPresentation
  persistentHostPresent
  schedulerRegistered
  schedulerActive
  schedulerState
  schedulerPresentation
  lastCycleState
  lastCycleAt
  operationalDebt
  activationAuthorized
  blockers
  nextSafeAction
  evidence
NOT_ON_VM_DO_NOT_FABRICATE =
  hostname / host identity label beyond supplied notes
  environment / OS / HostGator status
  durable|log|backup|lock path states
  cadence / schedule interval
  next expected run / scheduler_next_trigger
  scheduler_type / scheduler_health
  credentials / IPs / shell commands
  manual_run_availability as executable control
```

## 6. Persistência e dados

Nenhuma. Assessment docs-only. Futura tela: fixture sintético apenas; sem fetch, filesystem runtime operacional, localStorage como evidência, ou payloads de env com segredos.

## 7. Concorrência, locks e idempotência

N/A nesta assessment. Futura UI não deve emitir comandos de lock/scheduler.

## 8. Segurança

```text
CHANGE_RISK = HIGH (infraestrutura operacional)
NO_CREDENTIALS = true
NO_PRIVATE_IPS = true
NO_SENSITIVE_PATHS = true
NO_REMOTE_ACCESS = true
NO_SHELL_COMMANDS = true
NO_SCHEDULER_INSTALL = true
NO_SCHEDULER_ACTIVATION = true
EVIDENCE_AS_TEXT_ONLY = true
ILLUSTRATIVE != OPERATIONAL = true
REAL_HOST_WORK_REQUIRES_SEPARATE_HUMAN_AUTH = true
REAL_HOST_DETAILS_FROM_OPERATOR = true
REFERENCE_ONLY = docs/runbooks/R3E_LOCAL_HOST_DISCOVERY_RUNBOOK.md
DO_NOT_EXECUTE_DISCOVERY_IN_THIS_TASK = true
```

Hazards: false activation claim; false discovery-complete claim; leaking hostnames/paths/IPs/credentials from fabricated UI; accidental start/stop/run-now/activate affordances; treating synthetic `active=true` (if ever added) as proof of live activation.

## 9. Observabilidade

Sem telemetria. Assessment validada por suite backend/governance/frontend. Futura tela exigirá testes unitários + axe + architecture boundary (sem botões operacionais).

## 10. Operação

Não altera discovery, scheduler, coleta, validate ou estado científico. A tela futura deve exibir débito operacional aberto de forma inequívoca e a wording oficial. `nextSafeAction` permanece advisory (`complete_host_discovery` / `request_separate_activation_authorization`).

## 11. Rollback

```text
ROLLBACK = revert assessment PR; restaurar PROJECT NEXT se necessário
NEVER via scheduler activation / discovery / validate
```

## 12. Compatibilidade

- Consome I6B HostSchedulerViewModel + I6C fixtures + I5 shell placeholder.
- Overview/Runs/Readiness permanecem implementados.
- Nav label pode alinhar para “Host e Automação” na implementação futura se desejado (não bloqueante).

## 13. Testes necessários (futura implementação)

```text
route replaces placeholder only
synthetic notice visible
DEFERRED host not complete/failed
BLOCKED scheduler not fault/red
missing identity/cadence/next-run stay unavailable
operational debt wording visible
no start/stop/run-now/activate/configure controls
no credentials/IPs/paths fabricated
Overview/Runs/Readiness preserved
axe + architecture boundary
optional ACTIVE/COMPLETE fixtures only if narrowly synthetic and labeled
```

## 14. Alternativas consideradas

| Alternativa | Decisão |
|-------------|--------|
| Autorizar ativação/discovery real nesta assessment | REJECTED — separate human + real host |
| Autorizar campos B3 ausentes do VM | REJECTED — fabricate risk |
| Seletor de fixtures visível | REJECTED |
| Botões run-now / activate / install | REJECTED |
| Fixture ACTIVE como prova operacional | REJECTED — illustrative only if ever added |
| BLOCKED / ADJUSTMENT_REQUIRED por falta de ACTIVE fixture | REJECTED — deferred/blocked coverage sufficient with conditions |

## 15. Riscos

| Risco | Severidade | Mitigação |
|-------|------------|-----------|
| False scheduler activation claim | CRITICAL | No activate controls; active only if VM true + synthetic label; copy denies completion |
| False host discovery complete | CRITICAL | DEFERRED presentation; official debt wording |
| Sensitive infrastructure leak | CRITICAL | No hostname/IP/path/credential fabrication |
| Accidental operational affordance | HIGH | Read-only; no buttons; advisory nextSafeAction only |
| Fixture/live confusion | HIGH | Mandatory synthetic notice |
| Scope creep to real discovery scripts | HIGH | Docs reference only; do not execute |

## 16. Questões abertas

```text
NONE_BLOCKING
OPTIONAL_ACTIVE_OR_COMPLETE_FIXTURE = may be added in implementation task for UI tests only, clearly synthetic
REAL_HOST_INTEGRATION = requires separate human authorization + operator-supplied discovery evidence
```

## 17. Decisão arquitetural recomendada

Autorizar (em tarefa futura separada) um módulo `web/src/screens/host-scheduler/` que substitui apenas o placeholder `/operations/host-scheduler`, consome `buildFixtureViewModels(...).hostScheduler`, reutiliza primitivos I3 + tokens I2, exibe notice sintético e a wording de débito operacional, renderiza somente campos do ViewModel, permanece read-only, sem discovery real, sem credenciais, sem ativação/comandos operacionais e sem mudança científica.

## 18. Critérios para autorizar implementação

```text
1. This impact IMPACT_ASSESSMENT_STATUS = APPROVED
2. IMPLEMENTATION_AUTHORIZED = true (assessment docs)
3. DECISION = AUTHORIZED_WITH_CONDITIONS
4. I6I Readiness MERGED; NEXT was Host authorization assessment
5. Separate human prompt must set HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED=true for Host-only
6. HOST_SCHEDULER_SCREEN_MERGE_AUTHORIZED remains false until human merge
7. SCHEDULER_ACTIVATION_AUTHORIZED / OPERATIONAL_ACTIONS remain false
```

## Assessment dimensions

| Dimension | Result | Notes |
|-----------|--------|-------|
| Host/Scheduler ViewModel readiness | READY | deferred/blocked/unknown mapping + nextSafeAction |
| Fixture readiness | READY_WITH_CONDITIONS | deferred/blocked/partial/unknown covered; no ACTIVE/COMPLETE host scenario |
| DEFERRED state safety | READY | deferred → purple_or_gray; never fault |
| BLOCKED state safety | READY | blocked → purple_or_gray; never fault/red |
| Partial/unknown safety | READY | null booleans + unknown debt; no zeros |
| Operational-debt presentation | READY | `open`/`none`/`unknown` on VM; official wording required |
| Scheduler-state semantics | READY | BLOCKED ≠ FAULT; INACTIVE ≠ FAILED |
| Host-identity safety | READY_WITH_CONDITIONS | no identity on VM — must stay unavailable |
| Cadence presentation safety | OUT_OF_SCOPE_ON_VM | do not fabricate |
| Last/next-run presentation | READY_WITH_CONDITIONS | lastCycleAt only; next run not on VM |
| Human-action guidance | READY | advisory nextSafeAction |
| Evidence-reference safety | READY | text-only EvidenceLink |
| Responsive / a11y / route | READY | placeholder registered; patterns from I6E/G/I |

## Mandatory safety answers

1. **Can DEFERRED render without appearing completed or failed?** Yes — presentation `deferred` / purple_or_gray; copy from `HOST_DISCOVERY_DEFERRED`; never complete/fault.
2. **Can BLOCKED render without fault/red?** Yes — `blocked` severity; red reserved for confirmed fault.
3. **Are missing hostname/environment/cadence/run timestamps preserved as unavailable?** Yes if UI only uses VM fields; hostname/env/cadence/next-run are absent and must show unavailable / out-of-scope — never invent.
4. **Can the screen avoid secrets/credentials/private IPs/sensitive paths?** Yes — do not fabricate; evidence text-only; no forms.
5. **Can the screen remain fully read-only?** Yes — advisory `nextSafeAction` only.
6. **Can start/stop/run-now/retry/activate/install/configure remain absent?** Yes — mandatory out of scope.
7. **Are fixtures sufficient for deferred/blocked/partial/unknown?** Yes (`host_discovery_deferred`, `scheduler_blocked_not_authorized`, `partial_unknown_data`, `current_project_state_illustrative`).
8. **Is there a safe basis for a positive/active scheduler fixture?** Not today. Optional narrowly-scoped synthetic ACTIVE/COMPLETE fixture may be added in the implementation task for UI tests only, explicitly labeled illustrative and never treated as operational proof.
9. **Can evidence remain text-only?** Yes — `EvidenceLink` as text; no fabricated navigable operational links.
10. **Can official operational-debt wording remain visible?** Yes — require it on the screen when debt is open / discovery deferred.
11. **Exact implementation boundary?** See recommended boundary below.
12. **Human operational input before real-host integration?** Operator must run real-host discovery on the actual ops host per `docs/runbooks/R3E_LOCAL_HOST_DISCOVERY_*`, supply durable evidence, and obtain a separate human authorization that sets real-data / activation gates — never from this UI alone.
13. **Explicit out of scope?** Real host discovery/access; credentials; remote/shell/scheduler install/activate; collection/validate/run-now; fabricated B3 identity/path/cadence/next-run fields; scientific state change; Overview/Runs/Readiness changes.

## Authorization decision

```text
DECISION = AUTHORIZED_WITH_CONDITIONS
```

### Conditions

1. **Host/Scheduler screen only** — do not modify Overview/Runs/Readiness.
2. **Fixture-backed** — product fixture `current_project_state_illustrative` (or equivalent deferred/blocked posture).
3. **Read-only** — no operational buttons.
4. **No visible fixture selector**.
5. **No real host discovery** — do not execute discovery scripts from the UI or agent task.
6. **No real data / credentials / sensitive infrastructure fields**.
7. **No scheduler activation / install / configure / run-now / collection actions**.
8. **Supplied ViewModel fields only** — do not fabricate hostname, env, paths, cadence, next run, HostGator, etc.
9. **Official operational-debt wording** must appear when debt is open / discovery deferred.
10. **DEFERRED ≠ COMPLETE**; **BLOCKED ≠ FAULT**; **ILLUSTRATIVE ≠ OPERATIONAL**.
11. Optional ACTIVE/COMPLETE fixture only inside the implementation task, synthetic-labeled, not operational proof.
12. Separate human prompt must set `HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED=true` for Host only; this assessment does not flip execution flags.
13. Real-host integration and scheduler activation remain separately unauthorized until further human gates.

### Explicit out of scope

```text
REAL_HOST_DISCOVERY
REAL_HOST_ACCESS
CREDENTIALS
PRIVATE_IPS
SENSITIVE_PATHS
REMOTE_SHELL
SCHEDULER_INSTALL
SCHEDULER_ACTIVATION
RUN_NOW
COLLECTION_ACTIONS
VALIDATION_EXECUTION
FABRICATED_HOST_IDENTITY
FABRICATED_CADENCE_OR_NEXT_RUN
FABRICATED_PATH_STATES
HOSTGATOR_STATUS
OVERVIEW_RUNS_READINESS_CHANGES
SCIENTIFIC_INTERPRETATION_CHANGE
AUTHENTICATION
PERMISSIONS
FINANCIAL_EXECUTION
```

### Required future human input (before real-host integration)

```text
1. Operator executes discovery on the real ops host (not Cursor agent host) per runbooks
2. Durable discovery evidence recorded
3. Separate human authorization for operational data integration and/or scheduler activation
4. Explicit SCHEDULER_ACTIVATION_AUTHORIZED / related gates — UI never self-authorizes
```

## Decisão

```text
I6J_DECISION = AUTHORIZED_WITH_CONDITIONS
IMPLEMENTATION_EXECUTION_AUTHORIZED = false
HOST_SCHEDULER_SCREEN_IMPLEMENTATION_AUTHORIZED = false
SCHEDULER_ACTIVATION_AUTHORIZED = false
NEXT_RECOMMENDED_TASK = I6_HOST_SCHEDULER_SCREEN_IMPLEMENTATION
NEXT_ITEM = I6_HOST_SCHEDULER_SCREEN_SEPARATE_IMPLEMENTATION_TASK
```
