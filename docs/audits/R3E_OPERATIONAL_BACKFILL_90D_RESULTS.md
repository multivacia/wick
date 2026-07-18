# Resultados — Backfill operacional histórico R3E (90d)

> `DATA_ORIGIN = HISTORICAL_OPERATIONAL_BACKFILL`  
> `SCIENTIFIC_EVIDENCE_ELIGIBLE = false`  
> `FUTURE_UNSEEN_ELIGIBLE = false`  
> `GATE_IMPACT_ALLOWED = false`

## Janela

| Campo | Valor |
|-------|--------|
| Solicitado início | `2026-04-19T01:30:00+00:00` |
| Solicitado fim | `2026-07-18T01:30:00+00:00` |
| Cutoff imutável | `2026-07-18T01:30:00+00:00` |
| Inclusão | `market_ts` ∈ [start, end] e `<= cutoff` |

Alinhamento efetivo (exemplos): crypto 1h inicia em `2026-04-19T02:00:00+00:00` (próximo open horário); daily crypto rejeita o candle `2026-07-18T00:00:00+00:00` por ainda não fechado no momento da coleta.

## Resumo da carga

| Métrica | Valor |
|---------|--------|
| `R3E_OPERATIONAL_BACKFILL_RUN` | **COMPLETE** |
| Séries esperadas | 20 |
| Completas | 20 |
| Parciais | 0 |
| Ausentes | 0 |
| Barras aceitas (store) | 13725 |
| Rejeições store | 0 |
| Rejeições coleta (abertos) | 5 |
| Gaps detectados | 9 (stocks 1h, severity=info) |
| Duplicidades | 0 |
| Integridade hashes | **ok** |
| Compatibilidade estrutural | **true** |
| Elegibilidade temporal future-unseen | **false** |

## Séries

Ver `reports/r3e_operational_backfill/series_coverage.json` para first/last `market_ts` e contagens por série.

## Prova de rejeição oficial

Probe em diretórios temporários (não persistentes):

- `OFFICIAL_FUTURE_INGEST_REJECTED_HISTORICAL_DATA = true`
- `OFFICIAL_COLLECTION_STATE_UNCHANGED = true`

## Isolamento future-unseen

Antes/depois iguais para cutoff, freeze, collection_state, `n_observations=0`, séries ausentes oficiais e status de gate.

## Não executado

- M4 / M5
- `python -m wick.r3e.future_unseen validate`
- decisão de gate
- interpretação econômica
- abertura de R4/R5

## Aviso

Esta carga **não** satisfaz a janela prospectiva de 90 dias após o cutoff.  
Estas barras **não** contam para o mínimo de 200 barras oficiais.
