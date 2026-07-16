# R3D — Cobertura Yahoo 1h (auditável)

Documento de cobertura da fonte **Yahoo Finance** para timeframe `1h` no
experimento `experiment_id = r3d-real-validation-v1`.

## Ressalva da fonte

Yahoo Finance **não é uma fonte oficial de market data** para pesquisa
institucional. A documentação pública sobre limites de histórico intraday é
**inconsistente** entre canais (FAQ, mensagens de erro da API e comportamento
observado via `yfinance`). Os valores abaixo descrevem o **comportamento
efetivamente observado** nesta execução R3D, não uma garantia do provedor.

## Biblioteca e método

| Campo | Valor |
|-------|--------|
| Biblioteca | `yfinance` |
| Versão | `1.5.1` |
| Provider Wick | `src/wick/ingestion/providers/yahoo.py` (`YahooProvider`) |
| Método | `yfinance.Ticker(symbol).history(...)` |
| Intervalo solicitado | `1h` |
| `auto_adjust` | `False` |
| Série usada | OHLCV bruto; `Adj Close` quando disponível (`series_used=adjusted_close_when_available`) |
| Lookback efetivo no código | `_INTRADAY_MAX_LOOKBACK["1h"] = timedelta(days=729)` |
| Motivo da margem | Pedido em exatamente 730 dias foi rejeitado pela API (“must be within the last 730 days”); margem de 1 dia |

### Parâmetros de chamada (código)

```text
ticker.history(
    start=start.strftime("%Y-%m-%d"),
    end=(end + timedelta(days=1)).strftime("%Y-%m-%d"),  # buffer: yfinance end exclusive
    interval="1h",
    auto_adjust=False,
)
```

Clamp de início (quando necessário):

```text
earliest = now_utc - timedelta(days=729)
effective_start = max(requested_start, earliest)
```

Tratamento de qualidade: linhas com NaN/Inf em OHLCV são **ignoradas** (não
preenchidas). Lacunas de calendário acionário **não são preenchidas**.

## Runs de ingestão versionados

| Arquivo | `run_id` | Status |
|---------|----------|--------|
| `reports/r3d/ingestion_yahoo_1h.json` | `ing_a1436cb06dc64241` | FAILED (primeiro attempt @ ~730d exatos) |
| `reports/r3d/ingestion_yahoo_1h_retry.json` | `ing_c7e4701b3a164137` | PARTIAL (sucesso 4/5; ITUB4 NaN crash → retry) |
| `reports/r3d/ingestion_yahoo_itub4_1h.json` | `ing_a1531c6f329a47c2` | SUCCESS |

## Datas e contagens reais (run efetivo)

Janela solicitada no retry: `2024-07-17T23:59:59+00:00` → `2026-07-16T23:59:59+00:00`
(~729 dias).

| Símbolo | status | actual_start | actual_end | received | inserted | rejected | gaps reportados |
|---------|--------|--------------|------------|----------|----------|----------|-----------------|
| PETR4.SA | SUCCESS | 2024-07-18T13:00:00Z | 2026-07-16T18:00:00Z | 3472 | 3471 | 1 | 6 |
| VALE3.SA | SUCCESS | 2024-07-18T13:00:00Z | 2026-07-16T18:00:00Z | 3471 | 3470 | 1 | 6 |
| ITUB4.SA | SUCCESS (2º run) | 2024-07-18T13:00:00Z | 2026-07-16T18:00:00Z | 3472 | 3471 | 1 | 6 |
| AAPL | SUCCESS | 2024-07-18T13:30:00Z | 2026-07-16T16:30:00Z | 3469 | 3468 | 1 | 13 |
| MSFT | SUCCESS | 2024-07-18T13:30:00Z | 2026-07-16T16:30:00Z | 3469 | 3468 | 1 | 13 |

Span observado em `coverage_report.json`: ≈ **1.993–1.994 anos** (~729 dias
úteis de calendário de sessão, não 730 dias corridos cheios).

## Lacunas

Gaps listados nos JSON de ingestão são checagens heurísticas **sem calendário
de pregão** (`severity=info`). Fins de semana / feriados geram “gaps” esperados;
**nenhuma barra foi sintetizada**.

## Comportamento observado (~729 dias)

1. Pedido com início em ~730 dias → erro Yahoo / série vazia.
2. Pedido com início em **729 dias** → dados retornados.
3. Cobertura R3D para ações 1h: `COMPLETE` vs `min_years=1.5` do universo R3D
   (alvo “máximo efetivo da fonte”).

## Implicações

- Reprodutibilidade depende da disponibilidade futura do Yahoo/`yfinance`.
- Esta documentação congela o que foi obtido em 2026-07-16 para
  `r3d-real-validation-v1`.
- Não reutilizar o holdout nem alterar custos/parâmetros para reavaliar este
  experimento.
