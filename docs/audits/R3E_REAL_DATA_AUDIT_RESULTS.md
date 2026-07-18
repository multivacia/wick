# Auditoria R3E — Execução em OHLCV real (desenvolvimento)

## Premissa

Assumir leakage até prova em contrário. Experimento independente da R3D; holdout consumido **não** é validação final.

```text
experiment_id = r3e-contextual-edge-v1
parent_experiment_id = r3d-real-validation-v1
run_kind = R3E_REAL_DATA_DEVELOPMENT
DATA_ORIGIN = REAL_OHLCV_HISTORICAL
data_snapshot_id = r3e-real-20260717T235615Z
```

Artefatos: `reports/r3e_real/` (`data_snapshot.json`, `r3d_holdout_intervals.json`, `experiment_manifest.json`, `executive_report.json`, `technical_report.json`, `results_summary.json`).

## Checks

| Item | Resultado |
|------|-----------|
| Universo oficial reingerido (20 séries) | PASS — 125 848 candles; 0 falhas duras |
| Snapshot auditável (hash, providers, cobertura, revisões) | PASS — `data_snapshot.json` |
| Intervalo holdout R3D identificado | PASS — 20/20 `IDENTIFIED` em `r3d_holdout_intervals.json` |
| Holdout excluído de alegação confirmatória | PASS — `filter_development`; manifesto `confirmatory_use_of_r3d_holdout=false` |
| Holdout **não** usado como novo teste final | PASS — nested WF só no desenvolvimento |
| Manifesto congelado antes da avaliação | PASS — `frozen_at` anterior aos resultados |
| Nested WF M0–M5 | PASS — expanding + inner val; ~15 outer folds em painéis longos |
| Grids / thresholds / custos / seed / features | PASS — `1.0.0-provisional`, seed 42, grids congelados; sem alteração pós-resultado |
| Universo pareado M4 vs M5 (observações elegíveis) | PASS — mesmo `dev` row set; features candle só em M5 |
| ALL_SIGNALS + NON_OVERLAPPING_LONG_ONLY | PASS |
| Bootstrap temporal + FDR | PASS — 1000 resamples; FDR na família de pares |
| Leakage / preprocess / threshold | PASS — scaler/encoder/impute e hiperparâmetros só no treino |
| Concentração | PASS — 10 configs × 20 séries; 1h/1d equilibrados (100/100) |
| Parâmetros não alterados diante dos resultados | PASS |
| R4 / R5 não iniciados | PASS |

## Cobertura / reconstrução

- Cripto 1h/1d: COMPLETE (mesma política R3D).
- Ações 1d: `PARTIAL_ACCEPTED` (~4.991y; mesma classe de aceite R3D ~4.988y).
- Ações 1h Yahoo: COMPLETE sob `min_years=1.5` (lookback intraday limitado documentado).
- Sem divergência material que exija STOP; sem CRITICAL/HIGH.

## Holdout R3D (exemplo BTC/USDT)

| TF | development | holdout | holdout_first → last |
|----|-------------|---------|----------------------|
| 1h | 12 280 | 5 264 | 2025-12-09T16:00Z → 2026-07-16T23:00Z |
| 1d | 2 183 | 936 | 2023-12-24 → 2026-07-16 |

`r3e_confirmatory_claim_allowed_on_holdout = false` em todas as séries.

## Achados

### CRITICAL
Nenhum.

### HIGH
Nenhum.

### MEDIUM
1. Pares M5−M4 truncam ao menor nº de trades OOS quando as políticas de score selecionam contagens diferentes (mesmo universo elegível antes da seleção) — já documentado na auditoria sintética.
2. Em painéis longos, o passo do outer test cresce para ~15 folds (ainda expanding, teste único por janela); grids/custos/seed inalterados.

### LOW
1. Logistic single-class em fold interno faz fallback Ridge (inalterado).

## Resultado executivo (exploratório)

```text
classification (agregado) = CANDLE_ADDS_NO_VALUE
classification_counts:
  CONTEXT_HAS_NO_EDGE = 115
  INCONCLUSIVE = 69
  CANDLE_ADDS_NO_VALUE = 16
  CANDLE_ADDS_VALUE_EXPLORATORY = 0
  CONTEXT_PROMISING = 0  (rótulo puro; casos promising com candle sem valor → CANDLE_ADDS_NO_VALUE)

Slice primário BASE / h=5 / NON_OVERLAPPING (20 séries):
  mean Δ(M5−M4) ≈ -0.00243  (mediana ≈ -0.00099)
  frac p_adj ≤ 0.05 para M5−M4 = 0.0
  mean Δ(M1−M0) ≈ -0.00435 ; nenhuma comparação da escada com frac p_adj≤0.05 > 0
```

Interpretação exploratória: contexto ocasionalmente positivo em alguns 1d (ex. SOL/XRP classificados `CANDLE_ADDS_NO_VALUE`), mas o candle **não** acrescenta valor incremental estável após FDR. Predominam `CONTEXT_HAS_NO_EDGE` / `INCONCLUSIVE`.

## Estado máximo (atingido)

```text
R3E_REAL_DATA_RUN = COMPLETE
R3E_REAL_DATA_AUDIT = COMPLETE
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
```

Validação confirmatória final permanece exigindo dados futuros inéditos. Paper trading não iniciado.
