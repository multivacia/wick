# Auditoria R3E — Resultados

## Premissa

Assumir leakage até prova em contrário. Experimento independente da R3D.

```text
experiment_id = r3e-contextual-edge-v1
parent_experiment_id = r3d-real-validation-v1
```

## Checks (checklist)

| Item | Resultado |
|------|-----------|
| Holdout R3D não reutilizado | PASS — `filter_development` exclui últimos 30%; manifesto `r3d_holdout_reuse=false` |
| Splits estritamente temporais | PASS — nested expanding WF; testes `assert_no_future_in_train` |
| Scaler/encoder/impute só no treino | PASS — `fit_preprocess` no train; testes golden |
| Threshold/hiperparâmetros só no treino interno | PASS — seleção no inner fold |
| M4 e M5 mesmas observações | PASS — mesmo `dev` row set; features candle só em M5 |
| Custos idênticos / horizonte idêntico | PASS — pareados por configuração |
| UNKNOWN preservado | PASS — categoria explícita; unseen → UNKNOWN auditado |
| Block bootstrap + FDR família | PASS — `paired_delta` + `apply_family_fdr` |
| Long-only; bearish ≠ short | PASS — net_return via long simulation; signal bearish só feature |
| Grid não ampliado | PASS — `LOGISTIC_GRID` / `RIDGE_GRID` / `SCORE_POLICIES` congelados |
| R4 não iniciado | PASS |
| Dados futuros ainda exigidos | PASS — `R3E_GATE=PENDING_FUTURE_UNSEEN_DATA` |

## Achados

### CRITICAL
Nenhum.

### HIGH
Nenhum.

### MEDIUM
1. Relatório inicial em `reports/r3e/` gerado com **painel sintético estrutural** para CI/reprodutibilidade offline (DB local vazia neste ambiente). Reexecução em OHLCV real re-ingerido é necessária antes de interpretação econômica definitiva — ainda assim o gate máximo permanece `PENDING_FUTURE_UNSEEN_DATA`.
2. Pares M5−M4 usam truncamento ao menor número de trades OOS quando contagens diferem após política de score (documentado); universo de **observações elegíveis** permanece idêntico antes da seleção.

### LOW
1. Logistic com fold single-class faz fallback para Ridge (evita crash; reportado no hyperparams kind).

## Estado

```text
R3E_IMPLEMENTATION = COMPLETE
R3E_AUDIT = COMPLETE
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
```
