# Runbook — Automação de coleta Future-Unseen (B4)

> Orquestração operacional. Fail-closed. Sem peeking. Sem `validate`.

## Comando oficial

```bash
python -m wick.r3e.future_unseen run-cycle
```

Wrapper local:

```bash
./scripts/r3e_future_unseen_run_cycle.sh
```

### Flags suportadas

```text
--as-of
--dry-run-only
--skip-idempotency-check
--output-dir
--json / --human
--strict
--max-retries
--timeout-seconds
```

Não existem flags de bypass científico (`--force-validate`, `--ignore-cutoff`, etc.).

## Ciclo

Ordem fixa:

1. lock atômico
2. preflight (estado + hashes)
3. dry-run collect
4. collect real (salvo `--dry-run-only`)
5. reexecução idempotente (salvo skip)
6. ops-report
7. readiness
8. relatório imutável em `reports/r3e_future_unseen/automation_runs/<run_id>/`
9. estado resumido `reports/r3e_future_unseen/automation_state.json`
10. eventos de transição em `automation_events.jsonl`

## Status e exit codes (`run-cycle`)

Contrato aprovado pela análise de impacto (não misturar com exit codes do comando `readiness`):

```text
0 = COMPLETE
0 = PARTIAL
0 = NO_NEW_DATA
1 = FAILED
3 = BLOCKED
4 = SKIPPED_LOCKED
```

A saída JSON sempre inclui o campo textual `status`.

Exit codes do comando `readiness` permanecem separados (`0=READY`, `2=NOT_READY`, `3=BLOCKED`).

## Timeout (checkpoint model)

```text
PROVIDER_TIMEOUT = delegated_to_provider_retry_layer
CYCLE_TIMEOUT = 3000_seconds_checkpointed
HARD_CANCEL_MID_FLIGHT = false
TIMEOUT_LIMITATION = execution_in_progress_is_checked_at_safe_checkpoints
```

- o timeout **não** interrompe uma chamada de provedor já em execução;
- após expiração, novas etapas do ciclo não iniciam;
- o lock é liberado no encerramento seguro;
- timeout é registrado em `timed_out` / `hard_error` e classifica `FAILED`;
- hard-cancel mid-flight fica como backlog futuro separado (não nesta entrega).

## Lock

Arquivo: `reports/r3e_future_unseen/automation.lock`

```text
LOCK_PATH = reports/r3e_future_unseen/automation.lock
LOCK_MECHANISM = atomic_file_O_CREAT_EXCL
LOCK_TTL = 3300_seconds
```

- aquisição atômica (`O_CREAT|O_EXCL`)
- owner = hostname:pid
- TTL default 55 minutos
- stale lock recuperável (expirado ou pid morto)
- liberação normal ao fim do ciclo / interrupção tratada

## Frequência recomendada

Universo oficial mistura `1h` e `1d`.

- **Cadência base: horário**, no minuto 15 (`15 * * * *`)
  - candles `1h` já fechados com margem para `safety_delay`
  - evita spam de provedor
  - séries `1d` naturalmente retornam `NO_NEW_DATA` na maior parte do dia
- Não executar mais de um ciclo sobreposto (lock impede)

## Scheduler (estratégia)

```text
RUNNER_STRATEGY = local_agnostic_script
SCHEDULER_STRATEGY = cron_or_systemd_hourly_minute_15
STORE_OWNERSHIP = durable_host_volume_not_github_actions
```

### Prioridade 1 — runner local / cron / systemd

GitHub Actions **não** é o store oficial: ephemerality, falta de volume durável e risco de credenciais/provedores tornam CI inadequado para persistir `data/future_unseen/*`.

Use um host controlado com o repositório e o store montados.

**cron:**

```cron
15 * * * * cd /path/to/wick && ./scripts/r3e_future_unseen_run_cycle.sh >> /var/log/wick-fu-auto.log 2>&1
```

**systemd timer** (exemplo):

```ini
# /etc/systemd/system/wick-fu-auto.service
[Unit]
Description=Wick R3E future-unseen automation cycle
After=network-online.target

[Service]
Type=oneshot
WorkingDirectory=/path/to/wick
ExecStart=/path/to/wick/scripts/r3e_future_unseen_run_cycle.sh
Nice=10
```

```ini
# /etc/systemd/system/wick-fu-auto.timer
[Unit]
Description=Hourly Wick future-unseen automation

[Timer]
OnCalendar=*-*-* *:15:00
Persistent=true

[Install]
WantedBy=timers.target
```

### Prioridade 2 — GitHub Actions

Não implementado como persistência do store oficial nesta entrega.

Se no futuro houver runner self-hosted com volume durável + secrets controlados, um workflow `schedule` pode chamar o mesmo `run-cycle`. Até lá, trate Actions apenas como CI de código.

## Transição READY

Quando readiness muda para `READY`:

- evento `READINESS_BECAME_READY` é registrado
- `VALIDATE_AUTHORIZED = false`
- `HUMAN_AUTHORIZATION_REQUIRED = true`
- **não** executa `validate`
- **não** altera `R3E_GATE`

## Proibições

```bash
# NÃO executar neste fluxo
python -m wick.r3e.future_unseen validate
```

Não calcular M4/M5/DELTA_CANDLE/métricas econômicas. Não alterar cutoff/freeze/universo/thresholds.
