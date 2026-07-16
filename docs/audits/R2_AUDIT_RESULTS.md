# Auditoria R2 — Resultados (2026-07-16)

Checklist adversarial conforme `docs/audits/R2_AUDIT.md` e `prompts/PROMPT_AUDIT_R2.md`.

## Escopo auditado

- `src/wick/patterns/` (geometry, detectors, confirmation, params)
- `src/wick/features/context.py`
- `src/wick/detection/service.py`
- migration `20260716_0003_r2_pattern_tables.py`
- golden `tests/golden/r2/` + suítes adversarial/metamórficas

## Tentativas de reprovação

| Vetor | Resultado | Severidade |
|-------|-----------|------------|
| Look-ahead em features (slice > t) | Reprovado pelo código: contexto corta em `t`; testes adversarial cobrem | — |
| Confirmação antecipada (usa open[t+1] / close futuro) | Confirmação só após candle `t+1` fechado | — |
| Candle aberto aceito | Rejeitado por fórmula de fechamento temporal | — |
| Divisão por zero / candle degenerado | Epsilon + guards; negativos golden | — |
| Âncora multi-candle errada (engulfing/star) | Âncora no candle de conclusão; golden positivos/negativos | — |
| Parâmetros sem versão / hash | `detector_version` + `parameters_hash` persistidos | — |
| Rerun duplicando | Idempotência no service (reprocess/dry-run) | — |
| Retorno / backtest vazando na R2 | Ausente por desenho | — |
| Normalização global | Volatilidade exige janela local; senão UNKNOWN | — |
| Escala/translação | Testes metamórficos | — |

## Achados

### CRITICAL
Nenhum.

### HIGH
Nenhum após hardening (ruff/static scan fix `eaea1f8`).

### MEDIUM
1. **TA-Lib não usado como oráculo complementar** — deliberado (spec proíbe TA-Lib como fonte de verdade). Aceitável.
2. **Cobertura de concorrência em confirmação** — menos intensa que R1 upsert; risco residual baixo (unique keys).

### LOW
1. CLI `wick detect` dry-run não persiste (esperado).
2. Documentação de parâmetros espelha spec; qualquer mudança exige nova versão.

## Gate

- CI verde (PR #2)
- Golden + adversarial passam
- Zero look-ahead evidenciado
- R2 não calcula retorno

**R2_GATE = APPROVED** (técnico; merge humano pendente)
