# Runbook — Coleta incremental oficial Future-Unseen

> Coleta operacional prospectiva. Sem peeking. Sem `validate` antecipado.

## Arquitetura

```text
provedor R1 → candles fechados → cutoff (market_ts > FUTURE_UNSEEN_CUTOFF)
→ ingest_batch append-only → manifests/hashes → ops-report
```

Componentes:

- `wick.r3e.future_unseen.discovery` — janela incremental
- `wick.r3e.future_unseen.collector` — orquestração
- `wick.r3e.future_unseen.ingest` — store oficial
- Reuso: providers R1, `filter_closed_candles`, `validate_ohlcv`, gaps, mapping operacional

Cutoff imutável:

```text
FUTURE_UNSEEN_CUTOFF = 2026-07-18T01:30:00+00:00
```

## Comandos

Dry-run (não grava store):

```bash
python -m wick.r3e.future_unseen collect --dry-run
```

Coleta real:

```bash
python -m wick.r3e.future_unseen collect
```

Ops-report:

```bash
python -m wick.r3e.future_unseen ops-report
```

Opções permitidas: `--series`, `--provider`, `--as-of`, `--output-report`, `--max-retries`.

Proibidas: `--force`, `--ignore-cutoff`, `--allow-historical`, `--overwrite`, `--unlock-r4`.

## Periodicidade sugerida

- Horária: alguns minutos após o fechamento do candle 1h; ou
- Diária: todas as barras fechadas desde a última execução.

Ambas são suportadas. Não há automação externa nesta entrega.

## Diretórios

| Caminho | Uso |
|---------|-----|
| `data/future_unseen/raw/` | lotes raw append-only |
| `data/future_unseen/validated/` | lotes validados |
| `data/future_unseen/manifests/` | batch manifests + state |
| `reports/r3e_future_unseen/collection_runs/` | relatórios por execução |
| `reports/r3e_future_unseen/ops_report.json` | visão operacional agregada |

Sandbox histórica (não misturar):

`data/operational_backfill/r3e_90d/`

## Tratamento de erros

- Falha de uma série → demais continuam (`PARTIAL`)
- Retry limitado (default 3) só para erros transitórios
- Sem substituição silenciosa de símbolo/provedor
- Gaps elegíveis podem ser recuperados em execuções futuras (nunca antes do cutoff)

## Revisões / duplicidades

- Idêntico → `duplicate observation` (não crítico)
- Mesma revisão com payload diferente → conflito, sem overwrite
- Correção → exige `revision` incrementada + auditoria

## Rollback operacional

- Não apagar lotes aceitos
- Não reescrever hashes/manifestos anteriores
- Corrigir apenas com novo lote / revisão auditada

## Proibições

```bash
# NÃO executar antes da completude congelada:
python -m wick.r3e.future_unseen validate
```

Não calcular Δ(M5−M4), p-values, FDR, métricas econômicas.
Não abrir R4/R5.
Não marcar `ECONOMIC_INTERPRETATION_ALLOWED=true`.

## Estados esperados

```text
formal_status = IN_PROGRESS
data_driven_status = NOT_STARTED | IN_PROGRESS | COMPLETE
validation_status = NOT_RUN
validate_executed = false
effect_peeking_performed = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
```
