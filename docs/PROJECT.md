# Wick — Visão do Projeto

## Missão

Avaliar, com rigor quantitativo e auditável, se padrões de candlestick apresentam vantagem preditiva líquida após custos — antes de qualquer uso de dinheiro real.

## Princípios

- Detectar padrão não é recomendar compra ou venda.
- Resultados devem ser reproduzíveis (`run_id`, versões, seeds).
- Dados incompletos nunca são tratados como completos.
- Sem look-ahead: confirmação e entrada respeitam disponibilidade temporal.
- Long-only por padrão; short só com decisão explícita.
- Nenhum dinheiro real até R3 e R4 concluídas e auditadas; ordens reais só a partir da R6.

## Roadmap

| Release | Escopo |
|---------|--------|
| R1 | Setup, schema, ingestão OHLCV idempotente e auditável |
| R2 | Detectores de padrões com contrato matemático versionado |
| R3 | Backtests, custos, baselines, significância estatística |
| R4 | Paper trading / simulação temporal sem ordem real |
| R5 | Observabilidade, relatórios e gates de promoção |
| R6+ | Integração com corretora (fora do escopo atual) |

## Gates

- R1 → R2: ingestão confiável, migrations oficiais, testes offline verdes, README reproduzível.
- R2 → R3: detectores versionados, exemplos manuais, sem uso de informação futura.
- R3 → R4: metodologia congelada, holdout intocado até o gate, custos e FDR documentados.
- R4 → R5: paper signals auditáveis, sem execução real.
- Qualquer uso de dinheiro real exige decisão humana explícita.

## Stack

Python 3.11+, uv, SQLAlchemy 2.x, psycopg 3, Alembic, PostgreSQL (TimescaleDB opcional), Polars, NumPy, pydantic-settings, pytest, ruff, Docker Compose.

## Fontes de dados (R1)

- Binance via ccxt (público, sem API key).
- Yahoo Finance via yfinance (sem cadastro).
- brapi plugável e opcional (token em `.env` quando disponível).
