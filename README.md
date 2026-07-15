# Wick

Sistema de pesquisa quantitativa para avaliar se padrões de candlestick apresentam vantagem preditiva líquida após custos — **antes de qualquer uso de dinheiro real**.

Release atual: **R1 — Setup e Ingestão**.

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Docker + Docker Compose **ou** PostgreSQL 16 local
- Git

## Setup do zero

```bash
# 1) Dependências
uv sync --all-extras

# 2) Variáveis de ambiente
cp .env.example .env

# 3) Banco (recomendado: Docker Compose)
docker compose up -d db
# Aguarde o healthcheck ficar healthy

# Alternativa TimescaleDB (opcional, porta 5433):
# docker compose --profile timescale up -d timescaledb
# Ajuste DATABASE_URL no .env para a porta 5433

# 4) Migrations (Alembic é a fonte oficial do schema — não use create_all)
uv run alembic upgrade head

# 5) Validação
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run wick db-check
```

## Ingestão

Fontes R1:

| Fonte | Provider | Credencial |
|-------|----------|------------|
| Binance (cripto) | `binance` (public klines via `data-api.binance.vision`; ccxt-compatible interface nos testes) | Não necessária |
| Yahoo Finance (ações) | `yahoo` (yfinance) | Não necessária |
| brapi (B3, opcional) | `brapi` | `BRAPI_TOKEN` opcional |

```bash
# Cripto — Binance
uv run wick ingest \
  --source binance \
  --symbols "BTC/USDT,ETH/USDT" \
  --timeframes 1d \
  --start 2024-01-01T00:00:00Z \
  --end 2024-06-01T00:00:00Z \
  --report reports/example_binance.json

# Ações — Yahoo (histórico intraday pode ser parcial)
uv run wick ingest \
  --source yahoo \
  --symbols AAPL \
  --timeframes 1d \
  --start 2023-01-01T00:00:00Z \
  --end 2024-01-01T00:00:00Z \
  --report reports/example_yahoo.json

# Reexecução é idempotente; com --incremental (default) busca só o faltante
uv run wick ingest \
  --source binance \
  --symbols "BTC/USDT" \
  --timeframes 1d \
  --start 2024-01-01T00:00:00Z \
  --end 2024-06-01T00:00:00Z
```

Cada execução grava um `ingestion_run` com `run_id`, cobertura, rejeições, lacunas e um relatório JSON.

## Garantias da R1

- Timestamps UTC com timezone
- Somente candles fechados (`open_time + duration <= now - safety_delay`)
- Upsert idempotente; revisão de OHLCV incrementa `data_revision` e gera auditoria
- Histórico parcial → status `PARTIAL` (nunca disfarçado de sucesso)
- Falha de um ativo não impede os demais
- Testes offline (providers injetados / mockados — sem rede)
- brapi e TimescaleDB são opcionais
- Nenhum segredo no repositório

## Estrutura

```
src/wick/          # código da aplicação
alembic/           # migrations oficiais
docs/              # especificações e arquitetura
prompts/           # prompts de build/auditoria
tests/             # pytest (sem rede)
reports/           # relatórios de qualidade gerados
```

## Documentação

1. `CLAUDE.md` — regras operacionais
2. `docs/PROJECT.md` — visão e roadmap
3. `docs/architecture/` — dados, qualidade, metodologia
4. `docs/releases/R1_SPEC.md` — escopo desta release

## Fora de escopo (R1)

- Detectores de padrões (R2)
- Backtests / dinheiro real
- Ordens em corretora
