# Auditoria Quantitativa R3 — Resultados (2026-07-16)

Checklist conforme `docs/audits/R3_QUANT_AUDIT.md` e `prompts/PROMPT_AUDIT_R3.md`.

## Premissa

Assumir backtest enviesado até prova em contrário.

## R3A — Motor

| Vetor | Resultado |
|-------|-----------|
| entry t+1 / confirmado t+2 | Correto; teste prova que open[t+1] não é usado com confirmação |
| exit = entry+N-1 | Correto para N∈{1,3,5,10} |
| custos dois lados | fee+slippage entrada e saída |
| bearish como short | Não; apenas métrica direcional |
| exemplo manual 100→103, cost 0.0024 → 0.0276 | Bate |
| dados futuros insuficientes | `NOT_EVALUABLE_INSUFFICIENT_FUTURE_DATA` |
| idempotência de cálculo | Determinístico por inputs versionados |

### Achados R3A
- CRITICAL: nenhum
- HIGH: nenhum
- MEDIUM: `COST_MODEL_VERSION=1.0.0-provisional` — numerics não estavam na metodologia; exigem confirmação humana antes de R4
- LOW: vectorbt complementar não integrado (tolerância não definida na spec)

**R3A_GATE = APPROVED**

## R3B/R3C — Estatística e gate

### Achados corrigidos nesta auditoria (HIGH)

1. **Baseline “pareado” era shuffle de retornos** — inválido como null de timing.
   - Correção: `paired_random_entry_returns` com âncoras aleatórias e mesmas regras de entrada/custo.
2. **Baselines de tendência / ativo / buy-and-hold ausentes**
   - Correção: `trend_only_returns`, `same_window_asset_returns`, `buy_and_hold_return`.
3. **Walk-forward só contava folds, sem OOS**
   - Correção: `walk_forward_mean_oos` calculado dentro dos 70%.
4. **FDR não batelado entre estratégias**
   - Correção: `apply_fdr_across_reports`.

### Achados remanescentes

#### CRITICAL
Nenhum.

#### HIGH
Nenhum após hardening acima.

#### MEDIUM
1. **Custos provisórios** — bloqueiam promoção metodológica a R4 até humano confirmar bps.
2. **vectorbt complementar** — não adicionado; motor próprio + exemplos manuais são a fonte auditável; tolerância de concordância não está definida (não improvisar).
3. **Relatórios sintéticos** — demonstram pipeline; não são evidência de edge em ativos reais ingestados.
4. **Baseline de tendência usa close>SMA20** — interpretação mínima da “estratégia somente com tendência”; se o humano quiser regra diferente, é decisão metodológica.

#### LOW
1. Shuffle helper legado marcado deprecated em `stats.paired_random_baseline`.
2. Amostra sintética frequentemente EXPLORATORY/INSUFFICIENT → gate INCONCLUSIVE (honesto).

## Resultados mecânicos (sintéticos em `reports/r3/`)

Nenhuma estratégia sintética atingiu `PASSES_ALL_MECHANICAL_CRITERIA`.
Predominam `INCONCLUSIVE` e `FAILS_CRITERIA` / `NEGATIVE` sob BASE/STRESSED.

## Gate final permitido

- R3_IMPLEMENTATION = COMPLETE
- R3_AUDIT = COMPLETE
- R3_GATE = PENDING_HUMAN_DECISION
- R4_STATUS = NOT_STARTED
