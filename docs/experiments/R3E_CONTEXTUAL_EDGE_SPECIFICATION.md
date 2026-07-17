# Wick — R3E Contextual Edge Validation

> **Arquivo sugerido:** `docs/experiments/R3E_CONTEXTUAL_EDGE_SPECIFICATION.md`  
> **Natureza:** novo experimento independente da R3D/V1  
> **Regra central:** o holdout consumido da R3D não pode ser reutilizado como validação final da R3E.

## 1. Objetivo

Avaliar separadamente:

1. se tendência, volume, volatilidade e posição no range possuem vantagem mensurável;
2. se padrões de candle acrescentam valor incremental além desse contexto.

Pergunta principal:

> Adicionar o padrão de candle ao melhor modelo contextual melhora de forma consistente a expectativa líquida fora da amostra?

## 2. Relação com a R3D

A R3D está encerrada:

```text
EXPERIMENT_V1 = CLOSED
EXPERIMENT_V1_RESULT = NO_MEASURABLE_EDGE
R3_GATE = REJECTED_NO_MEASURABLE_EDGE_V1
```

É proibido:

- reabrir o holdout da R3D;
- recalibrar a V1;
- alterar custos retroativamente;
- reclassificar variantes reprovadas;
- usar o holdout consumido como validação final nova.

A R3D pode ser usada apenas como contexto exploratório.

## 3. Hipóteses

### H0

Contexto e padrões não melhoram a expectativa líquida de forma estável fora da amostra.

### H1

Um ou mais modelos contextuais superam os baselines.

### H2

O modelo contextual acrescido de candle supera o mesmo modelo sem candle.

H2 é a hipótese principal.

## 4. Modelos oficiais

```text
M0 = baseline aleatório pareado
M1 = tendência
M2 = tendência + volume
M3 = tendência + volume + volatilidade
M4 = tendência + volume + volatilidade + posição no range
M5 = M4 + padrão de candle
```

A comparação principal é:

```text
DELTA_CANDLE = performance(M5) - performance(M4)
```

## 5. Modelagem

Métodos permitidos na v1:

- estratificação por regras;
- regressão logística L2 para acerto direcional;
- Ridge regression para retorno líquido;
- scikit-learn, statsmodels, NumPy, Polars e SciPy.

Não usar:

- árvores;
- boosting;
- redes neurais;
- deep learning;
- seleção ilimitada de features;
- AutoML.

## 6. Features permitidas

```text
trend_direction
trend_strength
sma_20_slope
distance_from_sma_20
return_5
return_20
volume_ratio_20
volume_regime
atr_14
normalized_atr
volatility_regime
range_position_20
range_position_bucket
pattern_type
signal
confirmation_variant
asset_id
timeframe
```

Features futuras, resultados da operação, máximas/mínimas futuras e identificadores de operação são proibidos.

## 7. Universo

Ativos e timeframes da R3D, sem remoção seletiva:

- BTC/USDT
- ETH/USDT
- SOL/USDT
- BNB/USDT
- XRP/USDT
- PETR4.SA
- VALE3.SA
- ITUB4.SA
- AAPL
- MSFT
- 1h
- 1d

## 8. Validação temporal

A R3E usa nested walk-forward para desenvolvimento.

```text
R3E_DEVELOPMENT = NESTED_WALK_FORWARD
R3E_FINAL_VALIDATION = PENDING_FUTURE_UNSEEN_DATA
```

Regras:

- nenhuma divisão aleatória;
- scaler apenas no treino;
- imputação apenas no treino;
- encoder apenas no treino;
- hiperparâmetros apenas no treino interno;
- teste externo tocado uma única vez por janela.

Mesmo com resultado positivo:

```text
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
```

## 9. Dados ausentes

- `UNKNOWN` é categoria explícita;
- imputação numérica usa apenas estatística do treino;
- não remover linhas silenciosamente;
- relatar cobertura por feature;
- criar indicador de ausência quando necessário.

## 10. Variáveis-alvo

Separar:

```text
directional_hit
net_return
```

Horizontes:

```text
N ∈ {1,3,5,10}
```

Custos:

```text
OPTIMISTIC
BASE
STRESSED
```

Bearish continua sendo métrica direcional, não short executável.

## 11. Comparações obrigatórias

```text
M1 vs M0
M2 vs M1
M3 vs M2
M4 vs M3
M5 vs M4
```

Avaliar:

- diferença de expectativa líquida;
- diferença de acerto;
- intervalo de confiança;
- estabilidade por janela;
- estabilidade por ativo;
- estabilidade por timeframe;
- FDR ajustado;
- sensibilidade a custos.

## 12. Hiperparâmetros congelados

Logística L2:

```yaml
C: [0.01, 0.1, 1.0, 10.0]
class_weight: [null, balanced]
```

Ridge:

```yaml
alpha: [0.01, 0.1, 1.0, 10.0, 100.0]
```

Não ampliar o grid após observar resultados.

## 13. Thresholds congelados

```yaml
score_policy:
  - TOP_10_PERCENT
  - TOP_20_PERCENT
  - PROBABILITY_055
  - PROBABILITY_060
```

Selecionar apenas no treino interno.

## 14. Pré-processamento

Usar pipeline único contendo:

- imputação;
- one-hot encoding;
- StandardScaler;
- modelo.

Categorias desconhecidas no teste devem ser ignoradas de forma explícita e auditada.

## 15. Sobreposição

Produzir:

```text
ALL_SIGNALS
NON_OVERLAPPING_LONG_ONLY
```

M4 e M5 devem usar exatamente a mesma política e o mesmo universo elegível.

## 16. Custos

Manter:

```text
COST_MODEL_VERSION = 1.0.0-provisional
```

Qualquer mudança exige novo `cost_model_version` e novo `experiment_id`.

## 17. Estatística

- block bootstrap temporal;
- 1.000 amostras;
- seed 42;
- IC 95%;
- FDR Benjamini–Hochberg por família;
- p-value bruto e ajustado;
- tamanho do efeito;
- concentração temporal e por ativo.

## 18. Métricas

Classificação:

- balanced accuracy;
- ROC-AUC;
- precision;
- recall;
- Brier score;
- calibração.

Regressão:

- MAE;
- RMSE;
- correlação;
- estabilidade por janela.

Econômicas:

- expectativa líquida;
- taxa de acerto;
- retorno acumulado;
- drawdown;
- exposição;
- operações;
- sensibilidade a custos.

ROC-AUC isoladamente nunca aprova estratégia.

## 19. Gates

Estados:

```text
CONTEXT_PROMISING
CANDLE_ADDS_VALUE
CANDLE_ADDS_NO_VALUE
INCONCLUSIVE
NEGATIVE
REQUIRES_FUTURE_VALIDATION
```

M5 só pode receber `CANDLE_ADDS_VALUE` quando superar M4 fora da amostra, com efeito estável, custos BASE, comparação pareada, FDR reportado e auditoria aprovada.

Mesmo assim, R4 permanece bloqueada até dados futuros realmente inéditos.

## 20. Persistência

Manifesto obrigatório:

```text
experiment_id
parent_experiment_id
model_version
feature_set_version
cost_model_version
detector_version
parameters_hash
data_snapshot_hash
train_windows
test_windows
random_seed
hyperparameter_grid
selected_hyperparameters
score_policy
holdout_policy
created_at
frozen_at
```

## 21. Golden tests

Cobrir:

- scaler sem leakage;
- encoder sem leakage;
- imputação sem leakage;
- nested walk-forward;
- M4 e M5 com mesmo universo;
- threshold escolhido no treino;
- FDR por família;
- bootstrap temporal;
- reprodutibilidade;
- bearish sem short;
- holdout R3D não reutilizado.

## 22. Auditoria adversarial

Procurar:

- reutilização do holdout;
- leakage;
- divisão aleatória;
- threshold escolhido no teste;
- grid ampliado depois;
- ativo removido seletivamente;
- M4/M5 em universos diferentes;
- custos diferentes;
- bootstrap não temporal;
- FDR incorreto;
- resultados negativos escondidos;
- concentração excessiva;
- interpretação de AUC como lucro.

## 23. Critérios de aceite

- manifesto congelado;
- nested walk-forward;
- M0–M5;
- comparação M5 vs M4;
- preprocessing sem leakage;
- thresholds e grids congelados;
- custos preservados;
- FDR e bootstrap;
- auditoria sem CRITICAL/HIGH;
- relatórios;
- CI verde;
- R4 não iniciada.

## 24. Estado máximo

```text
R3E_IMPLEMENTATION = COMPLETE
R3E_AUDIT = COMPLETE
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
```

A R3E deve aceitar honestamente qualquer conclusão, inclusive ausência de vantagem contextual ou ausência de valor incremental do candle.
