# Prompt — Implementar e Auditar R3E

O experimento V1/R3D está encerrado.

```text
EXPERIMENT_V1 = CLOSED
EXPERIMENT_V1_RESULT = NO_MEASURABLE_EDGE
R3_GATE = REJECTED_NO_MEASURABLE_EDGE_V1
R3E_STATUS = PENDING_IMPLEMENTATION
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
```

Leia:

1. `CLAUDE.md`
2. `docs/PROJECT.md`
3. `docs/architecture/DATA_MODEL.md`
4. `docs/architecture/DATA_QUALITY.md`
5. `docs/architecture/QUANT_METHODOLOGY.md`
6. `docs/experiments/R3E_CONTEXTUAL_EDGE_SPECIFICATION.md`
7. código, manifestos, relatórios e auditorias da R3D

Crie:

```text
feature/r3e-contextual-edge
```

Não faça merge. Não inicie R4/R5. Não conecte corretora.

## Objetivo

Implementar e auditar:

```text
M0 = aleatório pareado
M1 = tendência
M2 = tendência + volume
M3 = tendência + volume + volatilidade
M4 = contexto completo
M5 = M4 + candle
```

A comparação principal é M5 vs M4.

## Restrições

- não reutilizar o holdout da R3D como holdout novo;
- não reabrir a V1;
- não alterar custos;
- não ampliar grids;
- não remover ativos;
- não selecionar períodos depois;
- não usar divisão aleatória;
- não usar features futuras;
- não iniciar R4 mesmo com resultado positivo.

## Implementação

- novo experiment_id;
- lineage para R3D;
- snapshot hash;
- manifesto congelado;
- nested walk-forward;
- preprocessing dentro do pipeline;
- regressão logística L2;
- Ridge;
- grids congelados;
- thresholds congelados;
- M0–M5;
- M5 vs M4 pareado;
- OPTIMISTIC/BASE/STRESSED;
- ALL_SIGNALS;
- NON_OVERLAPPING_LONG_ONLY;
- block bootstrap;
- FDR por família;
- golden tests;
- auditoria;
- relatórios;
- CI.

## Auditoria

Assuma que existe leakage. Tente reprovar:

- splits;
- scaler;
- encoder;
- imputação;
- threshold;
- hiperparâmetros;
- universos M4/M5;
- custos;
- bootstrap;
- FDR;
- holdout;
- concentração;
- interpretação.

Classifique CRITICAL/HIGH/MEDIUM/LOW e corrija CRITICAL/HIGH que não alterem metodologia.

## Resultado

Classifique:

```text
CONTEXT_PROMISING
CANDLE_ADDS_VALUE
CANDLE_ADDS_NO_VALUE
INCONCLUSIVE
NEGATIVE
REQUIRES_FUTURE_VALIDATION
```

Estado máximo:

```text
R3E_IMPLEMENTATION = COMPLETE
R3E_AUDIT = COMPLETE
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
```

Entregue PR, commits, manifesto, janelas, hiperparâmetros, testes, CI, auditoria, M0–M5, delta M5-M4, custos, bootstrap, FDR, estabilidade, concentração, limitações e recomendação.
