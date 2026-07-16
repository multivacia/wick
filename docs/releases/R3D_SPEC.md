# R3D — Validação em Dados Históricos Reais

## Objetivo

Aplicar a metodologia R2/R3A/R3B/R3C **congelada** sobre OHLCV real, sem alterar
parâmetros para melhorar resultados.

## Universo inicial

### Cripto (Binance)
BTC/USDT, ETH/USDT, SOL/USDT, BNB/USDT, XRP/USDT

### Ações (Yahoo)
PETR4.SA, VALE3.SA, ITUB4.SA, AAPL, MSFT

### Timeframes
1h, 1d

### Cobertura alvo
- cripto 1h: 2 anos;
- cripto 1d: máximo disponível, mínimo 4 anos;
- ações 1d: 5 anos;
- ações 1h: máximo efetivo da fonte (Yahoo ~730d).

Séries abaixo do alvo → `PARTIAL` (não completar artificialmente).

## Versões congeladas

- `detector_version` / `parameters_hash` aprovados na R2
- `COST_MODEL_VERSION=1.0.0-provisional`
- `TREND_BASELINE_V1 = close > SMA20`
- Manifesto de experimentos congelado **antes** de abrir o holdout

## Comparação vectorbt (complementar)

- contagens, índices, timestamps: igualdade exata
- retorno por operação: tolerância absoluta `1e-10`
- métricas agregadas: tolerância absoluta `1e-8`

## Gates (estado final autorizado)

- `R3D_IMPLEMENTATION = COMPLETE`
- `R3D_AUDIT = COMPLETE`
- `R3_GATE = REJECTED_NO_MEASURABLE_EDGE_V1`
- `R4_STATUS = BLOCKED_NO_REAL_STRATEGY_APPROVED`
- `R5_STATUS = NOT_STARTED`

`experiment_id = r3d-real-validation-v1` — holdout consumido; reuso proibido;
custos/parâmetros congelados pós-holdout.

Não iniciar R4/R5.
