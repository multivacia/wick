# Auditoria R3D — Resultados (2026-07-16)

## Escopo

Validação da metodologia congelada (R2/R3A/R3B/R3C) sobre OHLCV real do universo
autorizado, sem recalibrar parâmetros nem reabrir holdout.

## Dados

| Classe | Séries | COMPLETE | PARTIAL | MISSING |
|--------|--------|----------|---------|---------|
| Cripto 1h/1d | 10 | 10 | 0 | 0 |
| Ações 1h | 5 | 5 | 0 | 0 |
| Ações 1d | 5 | 0 | 5 | 0 |

Ações 1d ficaram **PARTIAL** por span ≈ 4.988 anos (< alvo 5.0), sem preenchimento
artificial. Yahoo 1h exigiu margem de lookback (729d) e skip de NaN (ITUB4).

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
1. `COST_MODEL_VERSION=1.0.0-provisional` permanece; interpretações de edge líquido
   dependem de confirmação humana dos bps.
2. Ações 1d PARTIAL (~2 dias úteis abaixo de 5 anos calendário).
3. Variantes DOJI com filtro `bullish` → 0 sinais executáveis (esperado; DOJI não é
   long signal na R2).

### LOW
1. Pacote `vectorbt` não adicionado; oráculo complementar usa a mesma fórmula
   independente no módulo `vectorbt_compare` (tolerâncias oficiais aplicadas).

## Gates mecânicos (todas as variantes × séries)

| Gate | Contagem |
|------|----------|
| PASSES_ALL_MECHANICAL_CRITERIA | **0** |
| FAILS_CRITERIA | 568 |
| INCONCLUSIVE | 3272 |
| REQUIRES_HUMAN_REVIEW | 0 |

Nenhuma estratégia real aprovada para R4.

## Estado

- R3D_IMPLEMENTATION = COMPLETE
- R3D_AUDIT = COMPLETE
- R3_GATE = PENDING_HUMAN_DECISION
- R4_STATUS = BLOCKED_NO_REAL_STRATEGY_APPROVED
- R5_STATUS = NOT_STARTED
