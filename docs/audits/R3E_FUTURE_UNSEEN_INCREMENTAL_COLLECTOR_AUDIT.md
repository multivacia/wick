# Auditoria — Coletor incremental Future-Unseen

## Escopo

Implementação e primeira execução controlada do coletor incremental oficial.  
Não inclui decisão de gate nem interpretação econômica.

## Pré-condição — PR #11

| Campo | Valor |
|-------|--------|
| PR | #11 MERGED |
| MERGE_COMMIT | `132bbb147289c65d6b1d02643a9ee998ec63d7b3` |
| mergedAt (UTC) | `2026-07-18T16:19:05Z` |
| Classificação backfill | `HISTORICAL_OPERATIONAL_BACKFILL` / scientific=false |
| Contaminação future-unseen | nenhuma |

## Proteções

| Item | Status |
|------|--------|
| Cutoff preservado | PASS |
| Freeze M4/M5 preservado | PASS |
| Universo 20 séries preservado | PASS |
| Store append-only | PASS |
| Hashes SHA-256 | PASS |
| Idempotência (2ª coleta sem novos candles) | PASS (testes) |
| Candles abertos rejeitados | PASS |
| Históricos rejeitados (`NOT_STRICTLY_AFTER_FUTURE_UNSEEN_CUTOFF`) | PASS |
| Incrementalidade (não rebaixa histórico pré-cutoff) | PASS |
| Isolamento do backfill operacional | PASS |
| Sem import de validate/gate/pipeline no coletor | PASS |
| Sem peeking / sem métricas de efeito nos relatórios | PASS |
| R4 BLOCKED / R5 NOT_STARTED | PASS |
| Sem flags inseguras no CLI | PASS |

## Comandos auditados

```bash
python -m wick.r3e.future_unseen collect --dry-run
python -m wick.r3e.future_unseen collect
python -m wick.r3e.future_unseen ops-report
```

`validate` **não** executado.

## Execução controlada (UTC ~2026-07-18T16:22Z)

| Campo | Antes | Depois |
|-------|--------|--------|
| n_observations | 0 | 70 |
| data_driven_status | NOT_STARTED | IN_PROGRESS |
| séries presentes | 0 | 5 (crypto 1h) |
| séries ausentes | 20 | 15 |
| cutoff hash | inalterado | inalterado |
| freeze hash | inalterado | inalterado |

Notas operacionais:

- Dry-run: 70 candidatos, store não escrito.
- Coleta real: batch `fu_collect_20260718T162252Z_56bc9f23`, 70 aceitos, 0 rejeições store.
- Reexecução imediata: 0 candidatos novos; `n_observations` permanece 70 (idempotente).
- Séries Yahoo ainda sem candles fechados elegíveis (mercado fechado / sem barra pós-cutoff).
- Todos os `market_ts` aceitos são estritamente posteriores ao cutoff.
- Relatórios em `reports/r3e_future_unseen/collection_runs/`.

## Estado científico após coleta

```text
R3E_FUTURE_DATA_COLLECTION = IN_PROGRESS
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```

Única mudança ocorrida: crescimento operacional da coleta (`n_observations`, séries presentes, data-driven status).
