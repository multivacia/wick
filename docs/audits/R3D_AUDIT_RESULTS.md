# Auditoria R3D — Resultados (2026-07-16)

## Escopo

Validação da metodologia congelada (R2/R3A/R3B/R3C) sobre OHLCV real do universo
autorizado, sem recalibrar parâmetros nem reabrir holdout.

**experiment_id:** `r3d-real-validation-v1`

## Artefatos versionados

| Artefato | Caminho |
|----------|---------|
| Manifesto congelado | `reports/r3d/experiment_manifest.json` |
| Cobertura | `reports/r3d/coverage_report.json` |
| Relatório técnico | `reports/r3d/technical_report.json` |
| Relatório executivo | `reports/r3d/executive_report.json` |
| Yahoo 1h | `docs/audits/R3D_YAHOO_1H_COVERAGE.md` |

### Identidade do experimento

| Campo | Valor |
|-------|--------|
| experiment_id | `r3d-real-validation-v1` |
| detector_version | `1.0.0` |
| parameters_hash | `2f202cf99000ec16` |
| cost_model_version | `1.0.0-provisional` |
| seed | `42` |
| n_bootstrap | `1000` |
| holdout_opened | `true` |
| holdout_opened_at | `2026-07-16T18:27:55.890963+00:00` |
| holdout_consumed | `true` |
| holdout_reuse_forbidden | `true` |

## Dados

| Classe | Séries | COMPLETE | PARTIAL | Aceite |
|--------|--------|----------|---------|--------|
| Cripto 1h/1d | 10 | 10 | 0 | — |
| Ações 1h | 5 | 5 | 0 | — |
| Ações 1d | 5 | 0 | 5 | **PARTIAL_ACCEPTED_FOR_R3D** (~4.988y) |

Ações 1d: span ≈ 4.988 anos (< alvo 5.0), sem preenchimento artificial;
aceitas para interpretação da R3D por autorização humana (2026-07-16).

Padrões detectados (detector 1.0.0): **39.997** ocorrências.

## Vectorbt complementar

Comparação por série (HAMMER, N=5, BASE, raw): **20/20 OK**
(contagens/índices/timestamps exatos; retornos dentro de 1e-10 / agregados 1e-8).

## Achados

### CRITICAL
Nenhum.

### HIGH
Nenhum.

### MEDIUM
1. `COST_MODEL_VERSION=1.0.0-provisional` permanece.
2. Ações 1d `PARTIAL_ACCEPTED_FOR_R3D`.
3. Variantes DOJI com filtro `bullish` → 0 sinais executáveis (esperado).

### LOW
1. Oráculo complementar usa fórmula independente em `vectorbt_compare`
   (tolerâncias oficiais); pacote `vectorbt` não é dependência runtime.

## Gates mecânicos

| Gate | Contagem |
|------|----------|
| PASSES_ALL_MECHANICAL_CRITERIA | **0** |
| FAILS_CRITERIA | 568 |
| INCONCLUSIVE | 3272 |
| REQUIRES_HUMAN_REVIEW | 0 |

Nenhuma estratégia promovida. Resultado negativo aceito como conclusão válida.

## Estado

- R3D_IMPLEMENTATION = COMPLETE
- R3D_AUDIT = COMPLETE
- R3_GATE = REJECTED_NO_MEASURABLE_EDGE_V1
- R4_STATUS = BLOCKED_NO_REAL_STRATEGY_APPROVED
- R5_STATUS = NOT_STARTED
- Paper trading: **não iniciado**
