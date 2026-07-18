# R3E — Resultados da execução exploratória em OHLCV real

> Relatório completo. Não autoriza R4. Holdout R3D excluído de alegações confirmatórias.

## Identidade

| Campo | Valor |
|-------|--------|
| experiment_id | `r3e-contextual-edge-v1` |
| parent | `r3d-real-validation-v1` |
| DATA_ORIGIN | `REAL_OHLCV_HISTORICAL` |
| data_snapshot_id | `r3e-real-20260717T235615Z` |
| aggregate_hash_sha256 | `c4c7c157a845b2a88c3f18b35b196c51d72e29204c1a62d2ea883da4edbf6dc7` |
| providers | binance `data-api.binance.vision`; yfinance `1.5.1`; ccxt `4.5.65` |
| detector / params | `1.0.0` / `2f202cf99000ec16` |
| cost_model | `1.0.0-provisional` (congelado) |
| seed / bootstrap | `42` / `1000` |
| n_series / n_result_rows | 20 / 200 |

## Procedimento

1. Reingestão do universo oficial (cripto Binance + ações Yahoo; 1h+1d).
2. Snapshot auditável + identificação dos intervalos de holdout R3D (últimos 30% por série).
3. Detecção R2 (`detector_version=1.0.0`).
4. Manifesto congelado **antes** da avaliação OOS.
5. Nested walk-forward apenas no desenvolvimento; M0–M5; ALL_SIGNALS e NON_OVERLAPPING_LONG_ONLY; FDR na família de pares.
6. Sem alteração de grids/custos/seed/features após ver resultados.

Artefatos JSON: `reports/r3e_real/` (ver `results_summary.json` para tabela compacta; `technical_report.json` para detalhe).

## Classificações (200 configs)

| Label | Contagem |
|-------|----------|
| CONTEXT_HAS_NO_EDGE | 115 |
| INCONCLUSIVE | 69 |
| CANDLE_ADDS_NO_VALUE | 16 |
| CONTEXT_PROMISING | 0 |
| CANDLE_ADDS_VALUE_EXPLORATORY | 0 |

**Agregado oficial:** `CANDLE_ADDS_NO_VALUE` (há casos de contexto promising em que o candle não adiciona valor; zero casos em que o candle adiciona valor exploratório com FDR).

## Slice primário — BASE / N=5 / NON_OVERLAPPING_LONG_ONLY

### Escada de pares (média entre 20 séries)

| Comparação | mean Δ expectativa líquida | mediana Δ | fração p_adj ≤ 0.05 |
|------------|----------------------------|-----------|---------------------|
| M1 vs M0 | −0.00435 | −0.00099 | 0.0 |
| M2 vs M1 | +0.00390 | +0.00156 | 0.0 |
| M3 vs M2 | +0.00167 | +0.00096 | 0.0 |
| M4 vs M3 | +0.00130 | −0.00088 | 0.0 |
| **M5 vs M4** | **−0.00243** | **−0.00099** | **0.0** |

Nenhuma diferença da escada sobrevive FDR a 5% neste slice.

### Por série (M4 / M5 / Δ candle / DD / exposição)

| Ativo | TF | class | mean_net M4 | mean_net M5 | Δ net | Δ hit | IC95 Δ | p_raw | p_adj | n M4 | n M5 | DD M4 | DD M5 | exp M4 | exp M5 |
|-------|----|-------|-------------|-------------|-------|-------|--------|-------|-------|------|------|-------|-------|--------|--------|
| BTC/USDT | 1h | CONTEXT_HAS_NO_EDGE | -0.00155 | -0.00242 | -0.00103 | -0.022 | [-0.00295, 0.00102] | 0.855 | 0.855 | 224 | 488 | -0.336 | -0.714 | 0.019 | 0.040 |
| BTC/USDT | 1d | INCONCLUSIVE | 0.01235 | 0.00203 | -0.01307 | -0.099 | [-0.04659, 0.01939] | 0.781 | 0.781 | 81 | 104 | -0.499 | -0.602 | 0.041 | 0.052 |
| ETH/USDT | 1h | CONTEXT_HAS_NO_EDGE | -0.00244 | -0.00265 | 0.00020 | 0.019 | [-0.00176, 0.00215] | 0.394 | 0.614 | 575 | 656 | -0.783 | -0.852 | 0.048 | 0.054 |
| ETH/USDT | 1d | INCONCLUSIVE | 0.00430 | -0.00181 | -0.00675 | -0.031 | [-0.03045, 0.01607] | 0.745 | 0.798 | 96 | 107 | -0.622 | -0.825 | 0.048 | 0.054 |
| SOL/USDT | 1h | INCONCLUSIVE | -0.00137 | 0.00095 | 0.00027 | 0.029 | [-0.00342, 0.00455] | 0.401 | 0.785 | 174 | 300 | -0.441 | -0.361 | 0.014 | 0.025 |
| SOL/USDT | 1d | CANDLE_ADDS_NO_VALUE | 0.02948 | 0.02442 | -0.00800 | -0.071 | [-0.04659, 0.04000] | 0.596 | 0.859 | 88 | 85 | -0.585 | -0.747 | 0.066 | 0.064 |
| BNB/USDT | 1h | CONTEXT_HAS_NO_EDGE | -0.00098 | -0.00143 | -0.00095 | -0.055 | [-0.00416, 0.00246] | 0.700 | 0.771 | 237 | 298 | -0.432 | -0.443 | 0.020 | 0.025 |
| BNB/USDT | 1d | INCONCLUSIVE | 0.01250 | 0.01598 | 0.00401 | -0.010 | [-0.01849, 0.02257] | 0.372 | 0.620 | 97 | 98 | -0.532 | -0.537 | 0.049 | 0.049 |
| XRP/USDT | 1h | INCONCLUSIVE | 0.00133 | 0.00027 | -0.00094 | -0.026 | [-0.00388, 0.00215] | 0.723 | 0.723 | 427 | 511 | -0.266 | -0.326 | 0.035 | 0.042 |
| XRP/USDT | 1d | CANDLE_ADDS_NO_VALUE | 0.04047 | 0.01742 | -0.01768 | -0.076 | [-0.04802, 0.01581] | 0.822 | 0.822 | 79 | 98 | -0.456 | -0.349 | 0.041 | 0.051 |
| PETR4.SA | 1d | INCONCLUSIVE | 0.00670 | 0.00863 | 0.00158 | -0.041 | [-0.01811, 0.01620] | 0.537 | 0.794 | 49 | 54 | -0.186 | -0.239 | 0.071 | 0.078 |
| PETR4.SA | 1h | CONTEXT_HAS_NO_EDGE | -0.00394 | -0.00193 | 0.00211 | 0.070 | [-0.00097, 0.00516] | 0.081 | 0.405 | 100 | 108 | -0.317 | -0.214 | 0.044 | 0.048 |
| VALE3.SA | 1d | CONTEXT_HAS_NO_EDGE | -0.00819 | -0.00397 | 0.00428 | 0.000 | [-0.00817, 0.01802] | 0.312 | 0.758 | 54 | 47 | -0.380 | -0.196 | 0.078 | 0.068 |
| VALE3.SA | 1h | CONTEXT_HAS_NO_EDGE | -0.00088 | -0.00135 | -0.00042 | 0.000 | [-0.00277, 0.00225] | 0.585 | 0.679 | 151 | 158 | -0.271 | -0.273 | 0.067 | 0.070 |
| ITUB4.SA | 1d | INCONCLUSIVE | 0.00439 | -0.00172 | -0.00414 | 0.059 | [-0.01696, 0.01313] | 0.617 | 0.771 | 34 | 62 | -0.131 | -0.176 | 0.049 | 0.090 |
| ITUB4.SA | 1h | CONTEXT_HAS_NO_EDGE | -0.00156 | -0.00347 | -0.00169 | -0.095 | [-0.00400, 0.00074] | 0.909 | 0.909 | 105 | 141 | -0.189 | -0.399 | 0.047 | 0.063 |
| AAPL | 1d | CONTEXT_HAS_NO_EDGE | -0.00026 | -0.00421 | -0.00330 | -0.025 | [-0.02212, 0.01040] | 0.727 | 0.950 | 40 | 51 | -0.186 | -0.291 | 0.058 | 0.074 |
| AAPL | 1h | INCONCLUSIVE | 0.00126 | 0.00047 | -0.00124 | -0.038 | [-0.00631, 0.00349] | 0.691 | 0.780 | 118 | 106 | -0.159 | -0.153 | 0.053 | 0.047 |
| MSFT | 1d | INCONCLUSIVE | 0.00123 | -0.00089 | -0.00266 | 0.000 | [-0.00972, 0.00563] | 0.736 | 0.920 | 59 | 53 | -0.179 | -0.166 | 0.086 | 0.077 |
| MSFT | 1h | CONTEXT_HAS_NO_EDGE | -0.00263 | -0.00147 | 0.00090 | 0.041 | [-0.00156, 0.00372] | 0.220 | 0.550 | 123 | 130 | -0.290 | -0.210 | 0.055 | 0.058 |

Estabilidade por janela e métricas adicionais por custo/overlap: `reports/r3e_real/results_summary.json` e `technical_report.json`.

## Por custo (h=5, NON_OVERLAPPING)

Para cada ativo/TF, OPTIMISTIC / BASE / STRESSED foram avaliados sem recalibrar. Em geral STRESSED desloca mean_net negativamente ~custo adicional; classificações `CONTEXT_HAS_NO_EDGE` permanecem dominantes em 1h. Detalhe: chave `cost_sensitivity_h5_nonoverlap` em `results_summary.json`.

## ALL_SIGNALS vs NON_OVERLAPPING

Ambas as políticas foram produzidas para BASE (h∈{1,5}) e demais horizontes conforme pipeline. NON_OVERLAPPING reduz operações e é o slice primário econômico; ALL_SIGNALS documentado no technical report.

## Concentração

- Por ativo: 20 linhas cada (uniforme).
- Por timeframe: 1h=100, 1d=100.
- Sem concentração seletiva de universo.

## Estabilidade por janela

Cada modelo reporta `window_stability` (folds outer com `test_n`). Não há promoção baseada em janela única; gate permanece pendente de dados futuros.

## Conclusões (exploratórias)

1. **H0 / contexto:** na maior parte das configs, M4 não entrega edge líquido estável (`CONTEXT_HAS_NO_EDGE` ou `INCONCLUSIVE`).
2. **H2 / candle:** Δ(M5−M4) médio negativo no slice primário; **0** séries com p_adj≤0.05; **0** `CANDLE_ADDS_VALUE_EXPLORATORY`.
3. Casos `CANDLE_ADDS_NO_VALUE` (ex. SOL/XRP 1d no primário) indicam contexto promising sem incremento do candle.
4. **R3E_GATE = PENDING_FUTURE_UNSEEN_DATA**; **R4_STATUS = BLOCKED**; **R5_STATUS = NOT_STARTED**.

## Estado

```text
R3E_REAL_DATA_RUN = COMPLETE
R3E_REAL_DATA_AUDIT = COMPLETE
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
```
