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

| Release | Escopo | Status |
|---------|--------|--------|
| R1 | Setup, schema, ingestão OHLCV idempotente e auditável | **Concluída** (`R1_GATE = APPROVED`) |
| R2 | Detectores de padrões com contrato matemático versionado | **Implementada + auditada** (`R2_GATE = APPROVED` técnico; PR aberta) |
| R3 | Backtests, custos, baselines, significância estatística | **Implementação completa** (`R3_GATE = PENDING_HUMAN_DECISION`) |
| R4 | Paper trading / simulação temporal sem ordem real | **NOT_STARTED** |
| R5 | Observabilidade, relatórios e gates de promoção | **NOT_STARTED** |
| R6+ | Integração com corretora (fora do escopo atual) | — |

## Encerramento R1

| Campo | Valor |
|-------|--------|
| Status | Concluída — `R1_GATE = APPROVED` |
| Data | 2026-07-16 |
| Commit final | `6482496c021ab6736313b6af96c929e2f9271eda` |
| Testes | 39 passed |
| CI | Verde (PostgreSQL 16, GitHub Actions) |
| PostgreSQL | 16 oficial / homologada; 15 mínima (NULLS NOT DISTINCT) |
| PR | https://github.com/multivacia/wick/pull/1 |
| Merge | Pendente de autorização humana |
| R2 | Não iniciada |

## Status R2 / R3 (2026-07-16)

| Campo | Valor |
|-------|--------|
| R2 PR | https://github.com/multivacia/wick/pull/2 (`feature/r2-detection`) |
| R3A PR | https://github.com/multivacia/wick/pull/3 (`feature/r3a-backtest-core`) |
| R3B branch | `feature/r3b-quant-validation` |
| Testes (tip R3B) | 76 passed |
| Custos OPTIMISTIC/BASE/STRESSED | **provisórios v1** (`cost_model_version=1.0.0-provisional`) — exigem confirmação humana antes de R4 |
| R3_GATE | `PENDING_HUMAN_DECISION` |
| R4 / R5 | NOT_STARTED |

## Gates

- R1 → R2: **aprovado** tecnicamente; merge da R1 ainda aguarda autorização humana.
- R2 → R3: **aprovado** tecnicamente (detectores versionados, golden, zero look-ahead evidenciado nas suítes).
- R3 → R4: metodologia implementada; holdout/FDR/custos documentados; **gate humano obrigatório** (custos provisórios + seleção de estratégias).
- R4 → R5: paper signals auditáveis, sem execução real.
- Qualquer uso de dinheiro real exige decisão humana explícita.

## Stack

Python 3.11+, uv, SQLAlchemy 2.x, psycopg 3, Alembic, **PostgreSQL 16** (oficial; mínimo 15 por `NULLS NOT DISTINCT`), TimescaleDB opcional, Polars, NumPy, pydantic-settings, pytest, ruff, Docker Compose, GitHub Actions CI.

## Fontes de dados (R1)

- Binance via endpoints públicos de klines (`data-api.binance.vision`; interface ccxt-compatível nos testes).
- Yahoo Finance via yfinance (sem cadastro).
- brapi plugável e opcional (token em `.env` quando disponível).

## Log de decisões

| Data | Decisão | Contexto | Impacto |
|------|----------|----------|---------|
| 2026-07-15 | Iniciar R1 em repositório vazio na branch `feature/r1-ingestion` | Pacote de specs como fonte de verdade | Base do projeto Wick |
| 2026-07-15 | Alembic como única fonte de schema em runtime | Evitar `create_all` na aplicação | Reproduzibilidade de schema |
| 2026-07-15 | Binance via `data-api.binance.vision` | `api.binance.com` retornou 451 no ambiente | Market data público sem API key |
| 2026-07-15 | Incremental append-only; lacunas históricas com `--full` | Escopo R1 sem motor de repair | Atualização busca faltantes à frente |
| 2026-07-16 | Upsert `ON CONFLICT DO NOTHING` + `SELECT FOR UPDATE` | Corrida de criação vs serialização de revisão | Idempotência concorrente |
| 2026-07-16 | `NULLS NOT DISTINCT` em `asset(symbol, source, exchange)` | Unique clássico permitia duplicatas com `exchange` NULL | Exige PostgreSQL ≥ 15 |
| 2026-07-16 | PostgreSQL 16 oficial; 15 mínimo; Timescale `2.28.3-pg16` | Homologação e CI | Compose/CI fixados em 16 |
| 2026-07-16 | CI GitHub Actions com PG 16 vazio + Alembic | Gate de hardening | PR bloqueável por checks |
| 2026-07-16 | `R1_GATE = APPROVED` | Hardening + CI verde + 39 testes | R1 encerrada; merge e R2 só com autorização humana |
| 2026-07-16 | Implementar R2 com `R2_PATTERN_SPECIFICATION.md` | Spec executável fornecida pelo humano | Oito padrões oficiais, sem retorno |
| 2026-07-16 | Custos R3 provisórios (BASE total 0.0024) | Numerics ausentes na metodologia | `1.0.0-provisional`; confirmação humana antes de R4 |
| 2026-07-16 | `R3_GATE = PENDING_HUMAN_DECISION` | R3A/R3B/R3C implementados; R4 bloqueada | Seleção de estratégias é humana |
