# COLLECTION-SCHEDULER-ACTIVATION-001 — Análise de Impacto Arquitetural

## Metadados

```text
RELEASE = R3E
BACKLOG_ITEM = B5
TASK_ID = COLLECTION-SCHEDULER-ACTIVATION-001
TITLE = Safe Operational Activation of the Future-Unseen Collection Scheduler
CHANGE_RISK = HIGH
PHASE = IMPACT_ANALYSIS_ONLY
IMPACT_ASSESSMENT_STATUS = BLOCKED
IMPLEMENTATION_AUTHORIZED = false
SCHEDULER_ACTIVATION_AUTHORIZED = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = c85641dba106fc1273d1f382f136130233a7ac57
ANALYZED_AT = 2026-07-18T20:43:39Z
ANALYZED_BY = cursor-agent
AUTOMATION_COMMAND = python -m wick.r3e.future_unseen run-cycle
SCHEDULER_IMPLEMENTED = documented_local_cron_or_systemd
SCHEDULER_ACTIVATED = false
READINESS_STATUS = NOT_READY
READINESS_REASON = WINDOW_DAYS_INSUFFICIENT
VALIDATE_AUTHORIZED = false
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
MERGE_STATUS = BLOCKED
DECISION = HUMAN_NAMED_NEXT_OFFICIAL_ITEM
RECOMMENDED_DECISION = BLOCKED
```

## 1. Objetivo

Avaliar arquitetura, ambiente, riscos e pré-condições para ativar com segurança o scheduler recorrente que executará `python -m wick.r3e.future_unseen run-cycle`, sem ativar cron/systemd, sem instalar serviço, sem alterar infraestrutura, sem registrar secrets e sem executar `validate`.

Esta fase determina se a ativação operacional pode ser autorizada. Não a executa.

## 2. Contexto técnico

Estado oficial pós-B4 (main `c85641d`):

- `R3E_COLLECTION_AUTOMATION = IMPLEMENTED` (PR #19 merge `f773702`)
- comando: `python -m wick.r3e.future_unseen run-cycle`
- wrapper: `./scripts/r3e_future_unseen_run_cycle.sh`
- lock atômico: `reports/r3e_future_unseen/automation.lock` (TTL 3300s)
- store append-only: `data/future_unseen/{raw,validated,manifests}`
- histórico: `reports/r3e_future_unseen/automation_runs/<run_id>/`
- estado: `automation_state.json` (último ciclo COMPLETE; store 85; readiness NOT_READY / WINDOW_DAYS_INSUFFICIENT)
- scheduler documentado (cron/systemd horário UTC minuto 15); **não ativado**
- GitHub Actions **não** é dono do store oficial
- `validate` não autorizado; R4 BLOCKED; R5 NOT_STARTED

Lacunas operacionais não versionadas:

- nenhum `OPERATIONAL_OWNER` nomeado em `docs/PROJECT.md` / runbooks
- nenhum `HOST_ID` / path absoluto de volume durável designado como store oficial
- nenhum procedimento de alerta on-call publicado

## 3. Componentes afetados

Nesta fase: **nenhum código de produto**. Impacto esperado de uma futura ativação autorizada:

- host operacional (cron ou systemd timer)
- volume durável contendo checkout do repositório + `data/future_unseen/` + `reports/r3e_future_unseen/`
- ambiente Python do host
- logs do scheduler
- opcionalmente: documentação operacional adicional (runbook de ativação), sem mudança do orquestrador B4

Não afetados: cutoff, freeze, universo, thresholds, `validate`, gate científico, R4/R5.

## 4. Arquivos previstos

Nesta fase (impacto apenas):

```text
docs/ai-impact/COLLECTION-SCHEDULER-ACTIVATION-001_IMPACT_ASSESSMENT.md
reports/ai-implementation/R3E-B5-SCHEDULER-ACTIVATION-001_IMPACT_HANDOFF.md
docs/PROJECT.md
```

Futura ativação (somente após desbloqueio humano + autorização explícita; não nesta PR):

```text
host crontab OU unit/timer systemd
logs em destino operacional do host
possível runbook de ativação/incidente (documental)
```

Não previstos: workflow GitHub Actions que persista o store oficial; serviço long-running dedicado; mudanças em `automation.py` como pré-requisito da ativação.

## 5. Contratos e interfaces

Contrato já mergeado (B4), reutilizado sem alteração:

```text
COMMAND = python -m wick.r3e.future_unseen run-cycle
WRAPPER = ./scripts/r3e_future_unseen_run_cycle.sh
EXIT_0 = COMPLETE | PARTIAL | NO_NEW_DATA
EXIT_1 = FAILED
EXIT_3 = BLOCKED
EXIT_4 = SKIPPED_LOCKED
LOCK_PATH = reports/r3e_future_unseen/automation.lock
LOCK_TTL = 3300_seconds
CYCLE_TIMEOUT = 3000_seconds_checkpointed
HARD_CANCEL_MID_FLIGHT = false
READY_SIGNAL = HUMAN_AUTHORIZATION_REQUIRED=true; VALIDATE_AUTHORIZED=false
```

Env opcionais do wrapper: `FU_AS_OF`, `FU_DRY_RUN_ONLY=1`.

Ativação não introduz novo contrato científico.

## 6. Persistência e dados

### Store oficial

```text
STORE_PATH = data/future_unseen/{raw,validated,manifests}
STORE_OWNER = UNDECLARED_IN_VERSIONED_DOCS
VOLUME_STRATEGY = durable_host_volume_colocated_with_repo_checkout
BACKUP_STRATEGY = REQUIRED_BEFORE_RECURRING_ACTIVATION (filesystem snapshot or copy of data/future_unseen + reports/r3e_future_unseen)
RESTORE_STRATEGY = restore volume paths; verify manifests/hashes via ops-report/readiness; do not delete accepted append-only observations
PERMISSIONS = single unix user owns repo+store; no world-writable store; lock file writable by same user
ATOMICITY = ingest_batch append-only + automation lock O_CREAT|O_EXCL
CORRUPTION_DETECTION = readiness/ops hash+manifest checks each cycle; fail-closed to BLOCKED/FAILED
```

Confirmações obrigatórias:

- append-only: sim (B4)
- fora de storage efêmero: **exige host durável nomeado** (ainda ausente)
- protegido contra concorrência: sim (lock + TTL/stale)
- auditável: sim (`automation_runs/`, `automation_events.jsonl`)
- recuperável: sim se backup de volume existir (backup ainda não formalizado)

### 5.1 Ambiente de execução — comparação

```text
OPTION = persistent_local_host
PERSISTENCE = high (local disk under operator control)
SECRET_HANDLING = local .env / user env; not in git
AVAILABILITY = depends on laptop/desktop uptime
COST = low
OBSERVABILITY = local logs + automation_state.json
OPERATIONAL_OWNERSHIP = requires named human operator
RISKS = sleep/shutdown; disk full; single point of failure
RECOMMENDATION = ACCEPTABLE if host stays online hourly and owner is named

OPTION = VPS
PERSISTENCE = high with attached volume
SECRET_HANDLING = host secrets / env file with restricted perms
AVAILABILITY = high if provider SLA adequate
COST = moderate
OBSERVABILITY = journald/syslog + remote log shipping optional
OPERATIONAL_OWNERSHIP = requires named operator with SSH access
RISKS = provider outage; misconfigured volume; duplicate VPS clones
RECOMMENDATION = PREFERRED_WHEN_LOCAL_UPTIME_UNRELIABLE

OPTION = EC2
PERSISTENCE = high with EBS
SECRET_HANDLING = IAM + SSM/Secrets Manager preferred over plaintext
AVAILABILITY = high
COST = moderate-high
OBSERVABILITY = CloudWatch optional
OPERATIONAL_OWNERSHIP = cloud account owner must be named
RISKS = credential sprawl; wrong region/volume detach
RECOMMENDATION = ACCEPTABLE_EQUIVALENT_TO_VPS

OPTION = container_on_durable_host
PERSISTENCE = only if bind-mount/volume maps data/future_unseen and reports/r3e_future_unseen
SECRET_HANDLING = env injected at runtime; image must not bake secrets
AVAILABILITY = follows host
COST = low-moderate
OBSERVABILITY = container logs + mounted reports
OPERATIONAL_OWNERSHIP = same as host owner
RISKS = ephemeral container FS mistaken for store; duplicate schedules
RECOMMENDATION = ACCEPTABLE_IF_VOLUME_BIND_MOUNTS_OFFICIAL_PATHS

OPTION = GitHub_Actions
PERSISTENCE = ephemeral by default; no official store ownership
SECRET_HANDLING = repo secrets (broader exposure surface)
AVAILABILITY = managed
COST = low within minutes quota
OBSERVABILITY = Actions UI
OPERATIONAL_OWNERSHIP = repository admins
RISKS = CRITICAL store loss/ephemerality; concurrent runners; secret leakage
RECOMMENDATION = REJECT_FOR_OFFICIAL_STORE

OPTION = managed_scheduler_service
PERSISTENCE = depends on attached durable storage to job runtime
SECRET_HANDLING = vendor secret store
AVAILABILITY = high
COST = variable
OBSERVABILITY = vendor dashboards
OPERATIONAL_OWNERSHIP = account owner
RISKS = vendor lock-in; unclear volume semantics
RECOMMENDATION = DEFER_UNTIL_HOST_OWNERSHIP_RESOLVED
```

**Estratégia recomendada (condicional):** host durável (VPS/EC2 ou local sempre ligado) + cron ou systemd timer UTC minuto 15 + volume contendo repo e store. **GitHub Actions rejeitado** como dono do store oficial.

**Bloqueio:** nenhuma opção pode ser ativada enquanto `OPERATIONAL_OWNER` e `HOST_ID`/volume não forem declarados por humano.

## 7. Concorrência, locks e idempotência

### Scheduler

```text
SCHEDULER_TYPE = cron_or_systemd_timer
SCHEDULE = 15 * * * * (hourly at minute 15)
TIMEZONE = UTC
MISFIRE_POLICY = systemd Persistent=true runs missed once; cron skips missed ticks
OVERLAP_POLICY = prevented_by_automation.lock (EXIT_4 SKIPPED_LOCKED)
STARTUP_POLICY = oneshot per tick; no lingering daemon required
SHUTDOWN_POLICY = disable timer/cron; allow in-flight cycle to finish or wait LOCK_TTL
RETRY_POLICY = provider retries inside run_collect (default max_retries=3); scheduler itself does not retry failed ticks automatically
```

Cadência horário @ :15 UTC permanece adequada: candles 1h fechados com margem de safety_delay; séries 1d naturalmente `NO_NEW_DATA` na maior parte do dia; lock TTL 3300s < 3600s.

### Processo e lock

```text
PROCESS_OWNER = UNDECLARED_IN_VERSIONED_DOCS
WORKING_DIRECTORY = repository root on durable host
PYTHON_ENVIRONMENT = host venv/conda with project deps installed; same major Python as CI
LOCK_PATH = reports/r3e_future_unseen/automation.lock
LOCK_TTL = 3300_seconds
PID_HANDLING = lock records hostname:pid; stale if TTL expired or pid dead
STALE_LOCK_RECOVERY = automatic on next acquire when stale; manual delete only if recovery fails
MAX_RUNTIME = CYCLE_TIMEOUT 3000s checkpointed (no hard-cancel mid provider call)
```

## 8. Segurança

Provedores do universo congelado R3E future-unseen: **binance** e **yahoo** (público; sem API key obrigatória no fluxo atual).

```text
REQUIRED_ENV_FOR_RUN_CYCLE = none_mandatory_for_frozen_binance_yahoo_universe
OPTIONAL_ENV = BRAPI_TOKEN (not used by frozen 20-series; must not be required)
OPTIONAL_ENV = DATABASE_URL (not used by run-cycle filesystem path)
OPTIONAL_ENV = CANDLE_CLOSE_SAFETY_DELAY_SECONDS, LOG_LEVEL, FU_AS_OF, FU_DRY_RUN_ONLY
SECRET_ORIGIN = host-local .env or process environment; never commit
MIN_PERMISSIONS = network egress to market data endpoints; read/write only repo store+reports paths
ROTATION = rotate any optional tokens out-of-band; no secret values in automation reports
LOG_MASKING = do not echo env; cycle JSON must not embed credentials (B4 contract)
HUMAN_ACCESS = operator SSH/console only; no shared world-readable .env
EXPOSURE_RISK = medium if .env copied into CI or Actions; mitigated by rejecting Actions store ownership
```

Valores de secrets **não** são registrados neste artefato.

## 9. Observabilidade

```text
LOG_DESTINATION = host file or journald (example: /var/log/wick-fu-auto.log)
RUN_REPORT_LOCATION = reports/r3e_future_unseen/automation_runs/<run_id>/
HEALTH_SIGNAL = automation_state.json last_run_status in {COMPLETE,PARTIAL,NO_NEW_DATA} and freshness < 2h
FAILURE_ALERT = EXIT 1 or missing state update after scheduled tick
BLOCKED_ALERT = EXIT 3 or readiness/cycle BLOCKED event in automation_events.jsonl
READY_ALERT = READINESS_BECAME_READY event => notify human only; does not authorize validate
NO_NEW_DATA_HANDLING = EXIT 0; not an alert condition
RETENTION = keep automation_runs indefinitely while experiment active; rotate host text logs separately
```

Transição READY apenas sinaliza `HUMAN_AUTHORIZATION_REQUIRED=true`; **não** executa ciência.

## 10. Operação

```text
ACTIVATE_OWNER = UNDECLARED (blocker)
MONITOR_OWNER = UNDECLARED (blocker)
INCIDENT_OWNER = UNDECLARED (blocker)
OPERATIONAL_WINDOW = continuous hourly UTC; human review of alerts asynchronously
PAUSE_PROCEDURE = disable systemd timer OR comment/remove cron line; confirm no lock held or wait TTL
RESUME_PROCEDURE = re-enable timer/cron after preflight dry-run
INCIDENT_RUNBOOK = extend docs/runbooks/R3E_FUTURE_UNSEEN_AUTOMATION_RUNBOOK.md after unblock (not in this phase)
CYCLE_EVIDENCE = automation_runs/<run_id>/ + automation_state.json + exit code + host log line
```

Sem operador nomeado, ativação recorrente é irresponsável → **BLOCKED**.

## 11. Rollback

```text
STOP_COMMAND = kill only if process hung beyond LOCK_TTL; prefer await cycle exit
DISABLE_SCHEDULER_COMMAND = systemctl disable --now wick-fu-auto.timer  OR  remove cron line
LOCK_RECOVERY = delete automation.lock only if stale recovery failed and no live pid
STATE_RECOVERY = regenerate automation_state.json from latest immutable run directory if alias corrupt
STORE_RECOVERY = restore from backup volume; never delete valid accepted observations to "rollback"
ROLLBACK_VALIDATION = run-cycle --dry-run-only; ops-report; readiness; confirm VALIDATION_COMMAND_EXECUTED=false
```

Rollback **não** apaga dados aceitos validamente.

## 12. Compatibilidade

- Ativação do scheduler é compatível com comandos manuais (`collect`, `readiness`, `run-cycle`) via lock.
- Não altera contratos B2/B4.
- Não desbloqueia R4/R5.
- Não autoriza `validate`.
- G1: HIGH risk exige impacto aprovado + `IMPLEMENTATION_AUTHORIZED=true` antes de qualquer implementação/ativação; estado atual permanece `BLOCKED`.

## 13. Testes necessários

Nesta fase: somente governança (sem testes de produto; sem código alterado).

Antes de ativação recorrente (futuro, pós-autorização):

1. preflight (hashes/manifests/state)
2. dry-run manual (`--dry-run-only` ou `FU_DRY_RUN_ONLY=1`)
3. live run manual controlado (se autorizado)
4. execução agendada única
5. verificação de lock (sobreposição → EXIT 4)
6. verificação de relatório imutável
7. confirmação de store (append-only; contagem)
8. confirmação de readiness (status/reason)
9. confirmação de ausência de `validate`
10. só então ativação recorrente

**Esta sequência não foi executada nesta fase.**

## 14. Alternativas consideradas

1. **Ativar agora em host implícito (Cloud Agent / CI)** — rejeitada (efêmero; sem ownership).
2. **GitHub Actions schedule como store oficial** — rejeitada (persistência/secrets).
3. **Aprovar impacto e preparar prompt de ativação sem nomear host** — rejeitada pela regra: host/operador indeterminados ⇒ preferir BLOCKED.
4. **Esperar READY antes de ativar scheduler** — desnecessária para o objetivo B5 (precisamos do scheduler para acumular janela); mas ativação ainda exige owner/host.
5. **Documentar estratégia e bloquear ativação até declaração humana de owner/host** — **escolhida**.

## 15. Riscos

```text
RISK = host_unavailable
IMPACT = HIGH
LIKELIHOOD = MEDIUM
MITIGATION = prefer VPS/EC2 always-on; health freshness alert <2h
RESIDUAL_RISK = MEDIUM

RISK = ephemeral_storage
IMPACT = CRITICAL
LIKELIHOOD = MEDIUM if Actions/container misused
MITIGATION = forbid Actions store ownership; require durable volume bind
RESIDUAL_RISK = LOW if policy held

RISK = overlapping_execution
IMPACT = HIGH
LIKELIHOOD = LOW
MITIGATION = atomic lock + TTL + EXIT 4
RESIDUAL_RISK = LOW

RISK = stale_lock
IMPACT = MEDIUM
LIKELIHOOD = MEDIUM
MITIGATION = TTL/pid stale recovery; manual delete procedure
RESIDUAL_RISK = LOW

RISK = missing_credential
IMPACT = LOW for frozen binance/yahoo; MEDIUM if universe expands
LIKELIHOOD = LOW
MITIGATION = document required env; fail-closed provider errors as PARTIAL/FAILED
RESIDUAL_RISK = LOW

RISK = exposed_credential
IMPACT = HIGH
LIKELIHOOD = LOW
MITIGATION = no secrets in reports/git; reject Actions store; restrict .env perms
RESIDUAL_RISK = LOW

RISK = provider_timeout
IMPACT = MEDIUM
LIKELIHOOD = MEDIUM
MITIGATION = provider retries; checkpoint cycle timeout; PARTIAL preserves accepted data
RESIDUAL_RISK = MEDIUM (no hard-cancel mid-flight)

RISK = partial_failure
IMPACT = MEDIUM
LIKELIHOOD = MEDIUM
MITIGATION = PARTIAL status + per-series isolation + idempotent rerun
RESIDUAL_RISK = LOW

RISK = disk_full
IMPACT = HIGH
LIKELIHOOD = LOW
MITIGATION = disk monitoring; retain policy for logs; fail-closed writes
RESIDUAL_RISK = MEDIUM without monitoring owner

RISK = wrong_clock_or_timezone
IMPACT = MEDIUM
LIKELIHOOD = MEDIUM
MITIGATION = force UTC timer; NTP on host; as_of recorded in reports
RESIDUAL_RISK = LOW

RISK = duplicate_scheduler
IMPACT = HIGH
LIKELIHOOD = MEDIUM if two hosts enabled
MITIGATION = single HOST_ID declaration; lock is per-filesystem (not cluster-wide)
RESIDUAL_RISK = HIGH until single-host ownership declared

RISK = report_not_written
IMPACT = MEDIUM
LIKELIHOOD = LOW
MITIGATION = treat missing automation_state freshness as failure alert
RESIDUAL_RISK = LOW

RISK = store_corruption
IMPACT = CRITICAL
LIKELIHOOD = LOW
MITIGATION = hash/manifest checks; backups before recurring activation
RESIDUAL_RISK = MEDIUM without backup strategy named

RISK = activation_without_operator
IMPACT = CRITICAL
LIKELIHOOD = HIGH currently
MITIGATION = IMPACT_ASSESSMENT_STATUS=BLOCKED until OPERATIONAL_OWNER named
RESIDUAL_RISK = LOW while blocked

RISK = READY_transition_ignored
IMPACT = HIGH
LIKELIHOOD = MEDIUM
MITIGATION = READY_ALERT to human; VALIDATE_AUTHORIZED remains false
RESIDUAL_RISK = MEDIUM without on-call

RISK = accidental_validate_execution
IMPACT = CRITICAL
LIKELIHOOD = LOW
MITIGATION = automation does not call validate; runbook prohibition; no cron validate line
RESIDUAL_RISK = LOW
```

## 16. Questões abertas

1. Quem é o `OPERATIONAL_OWNER` (ativar, monitorar, responder)?
2. Qual é o `HOST_ID` e o path absoluto do volume durável oficial?
3. Cron ou systemd nesse host?
4. Destino de alertas (e-mail/chat) para FAILED/BLOCKED/READY?
5. Estratégia de backup/restore nomeada e testada?
6. O host local do mantenedor tem uptime horário confiável, ou exige VPS/EC2?
7. Hard-cancel mid-flight de timeout permanece backlog separado (não bloqueia B5 após owner/host)?

## 17. Decisão arquitetural recomendada

```text
RECOMMENDED_HOST_STRATEGY = durable_host_vps_or_always_on_local_with_bind_mounted_store
STORE_OWNERSHIP = durable_host_volume_not_github_actions
SCHEDULER_STRATEGY = cron_or_systemd_hourly_minute_15_UTC
SECRET_STRATEGY = host_env_no_git_no_actions_store
OBSERVABILITY_STRATEGY = host_logs_plus_automation_state_freshness_plus_ready_human_alert
ROLLBACK_STRATEGY = disable_timer_keep_append_only_store_restore_from_backup_if_needed
OPERATIONAL_OWNER = UNDECLARED
HOST_ID = UNDECLARED
RECOMMENDED_DECISION = BLOCKED
IMPACT_ASSESSMENT_STATUS = BLOCKED
IMPLEMENTATION_AUTHORIZED = false
SCHEDULER_ACTIVATION_AUTHORIZED = false
NEXT_ACTION = HUMAN_MUST_NAME_OPERATIONAL_OWNER_AND_HOST_THEN_REOPEN_IMPACT
```

Justificativa: a arquitetura B4 é adequada, mas a regra explícita desta tarefa exige preferir `BLOCKED` quando host ou operador não puderem ser determinados. Ambos permanecem indeterminados nas fontes versionadas.

## 18. Critérios para autorizar implementação

Para sair de BLOCKED e eventualmente permitir preparação/ativação:

1. humano declara em artefato versionado:
   ```text
   OPERATIONAL_OWNER =
   HOST_ID =
   VOLUME_PATH =
   SCHEDULER_TYPE = cron | systemd
   BACKUP_STRATEGY =
   ALERT_CHANNEL =
   ```
2. revisão humana desta análise com decisão explícita não-bloqueada;
3. atualização deste impacto para:
   ```text
   IMPACT_ASSESSMENT_STATUS = APPROVED
   IMPLEMENTATION_AUTHORIZED = true
   SCHEDULER_ACTIVATION_AUTHORIZED = false
   NEXT_ACTION = PREPARE_ACTIVATION_PROMPT
   ```
4. autorização humana **separada** para ativação recorrente (`SCHEDULER_ACTIVATION_AUTHORIZED = true`);
5. sequência de teste de ativação (seção 13) executada e evidenciada;
6. `VALIDATION_COMMAND_EXECUTED = false` preservado;
7. nenhuma mudança de cutoff/freeze/thresholds/validate;
8. GitHub Actions permanece fora do ownership do store oficial.

Estado atual:

```text
IMPACT_ASSESSMENT_STATUS = BLOCKED
IMPLEMENTATION_AUTHORIZED = false
SCHEDULER_ACTIVATION_AUTHORIZED = false
```
