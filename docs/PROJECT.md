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
| R1 | Setup, schema, ingestão OHLCV idempotente e auditável | **MERGED** (`R1_GATE = APPROVED`, tag `v0.1.0-r1`) |
| R2 | Detectores de padrões com contrato matemático versionado | **MERGED** (`R2_GATE = APPROVED`, tag `v0.2.0-r2`) |
| R3A–C | Motor, estatística, relatórios e gates mecânicos | **MERGED** (`R3_IMPLEMENTATION/AUDIT = COMPLETE`, tag `v0.3.0-r3`) |
| R3D | Validação em dados históricos reais (sem recalibrar) | **COMPLETE** (`R3_GATE = REJECTED_NO_MEASURABLE_EDGE_V1`, tag `v0.4.0-r3d-real-validation`) |
| R3E | Motor contextual M0–M5 (nested WF) | **CODE APPROVED** (`v0.5.0-r3e-engine`); real-data run **COMPLETE** (exploratório) |
| R3E-FU | Infra de validação final com dados futuros não vistos | **ENGINE COMPLETE** (coleta `NOT_STARTED`) |
| R4 | Paper trading / simulação temporal sem ordem real | **BLOCKED** |
| R5 | Observabilidade, relatórios e gates de promoção | **NOT_STARTED** |
| R6+ | Integração com corretora (fora do escopo atual) | — |

## Estado oficial (pós-R3D / R3E engine)

| Campo | Valor |
|-------|--------|
| R1_GATE | APPROVED |
| R2_GATE | APPROVED |
| R3A_GATE | APPROVED |
| R3_IMPLEMENTATION | COMPLETE |
| R3_AUDIT | COMPLETE |
| R3D_IMPLEMENTATION | COMPLETE |
| R3D_AUDIT | COMPLETE |
| R3_GATE | **REJECTED_NO_MEASURABLE_EDGE_V1** |
| R3E_CODE_GATE | **APPROVED** |
| R3E_IMPLEMENTATION | COMPLETE |
| R3E_AUDIT | COMPLETE |
| R3E_DEVELOPMENT_RUN | **REAL_OHLCV_EXPLORATORY** (sintético prévio: `SYNTHETIC_ONLY`) |
| R3E_REAL_DATA_RUN | **COMPLETE** |
| R3E_REAL_DATA_AUDIT | **COMPLETE** |
| ECONOMIC_INTERPRETATION_ALLOWED | **false** |
| R3E_GATE | **PENDING_FUTURE_UNSEEN_DATA** |
| R3E_FUTURE_VALIDATION_ENGINE | **COMPLETE** |
| R3E_FUTURE_VALIDATION_AUDIT | **COMPLETE** |
| R3E_FUTURE_DATA_COLLECTION | **IN_PROGRESS** |
| FUTURE_UNSEEN_CUTOFF | `2026-07-18T01:30:00+00:00` |
| R3E_OPERATIONAL_BACKFILL_RUN | **COMPLETE** (histórico; não científico) |
| R3E_OPERATIONAL_BACKFILL_AUDIT | **COMPLETE** |
| R3E_OPERATIONAL_BACKFILL_SCIENTIFIC_ELIGIBILITY | **false** |
| R4_STATUS | **BLOCKED** |
| R5_STATUS | NOT_STARTED |
| experiment_id (R3D) | `r3d-real-validation-v1` |
| experiment_id (R3E) | `r3e-contextual-edge-v1` |
| experiment_id (R3E-FU) | `r3e-future-unseen-v1` |
| detector_version / parameters_hash | `1.0.0` / `2f202cf99000ec16` |
| cost_model_version | `1.0.0-provisional` (congelado pós-holdout) |
| seed / bootstrap | `42` / `1000` |
| holdout R3D | consumido 1×; **reuso proibido** |
| R3D mecânico | 0 PASSES / 568 FAILS / 3272 INCONCLUSIVE |
| Ações 1d | `PARTIAL_ACCEPTED_FOR_R3D` (~4.988y) |
| Paper trading | **não iniciado** |
| Tags | `v0.1.0-r1` … `v0.4.0-r3d-real-validation`, `v0.5.0-r3e-engine` |

## Encerramento R1

| Campo | Valor |
|-------|--------|
| Status | Concluída — `R1_GATE = APPROVED` |
| PR | https://github.com/multivacia/wick/pull/1 (MERGED) |
| Tag | `v0.1.0-r1` |

## Status R2 / R3 / R3D

| Campo | Valor |
|-------|--------|
| R2 PR | https://github.com/multivacia/wick/pull/2 (MERGED) · tag `v0.2.0-r2` |
| R3A PR | https://github.com/multivacia/wick/pull/3 (MERGED) |
| R3B PR | https://github.com/multivacia/wick/pull/4 (MERGED) · tag `v0.3.0-r3` |
| R3D PR | https://github.com/multivacia/wick/pull/5 · tag `v0.4.0-r3d-real-validation` |
| Custos | `1.0.0-provisional` — não alterar para reavaliar `r3d-real-validation-v1` |
| R3_GATE | `REJECTED_NO_MEASURABLE_EDGE_V1` |
| R3E engine | PR #6 · tag `v0.5.0-r3e-engine` · `experiment_id=r3e-contextual-edge-v1` |
| R3E real-data | PR #7 **MERGED** · `CANDLE_ADDS_NO_VALUE` · 0 `CANDLE_ADDS_VALUE_EXPLORATORY` · sem evidência de valor incremental do candle |
| R3E_GATE | `PENDING_FUTURE_UNSEEN_DATA` (holdout R3D **não** reutilizado; validação final = dados futuros) |
| Interpretação econômica | **não aprovada** |
| R4 / R5 | BLOCKED / NOT_STARTED |

## Gates

- R1 → R2: **aprovado**; merges em `main` concluídos.
- R2 → R3: **aprovado**.
- R3 → R4: **rejeitado na v1** — sem edge mensurável sob metodologia/custos congelados; R4 bloqueada.
- R3E: nested walk-forward; validação final exige dados futuros inéditos; R4 permanece bloqueada.
- R4 → R5: paper signals auditáveis, sem execução real (não iniciado).
- Qualquer uso de dinheiro real exige decisão humana explícita.

## Stack

Python 3.11+, uv, SQLAlchemy 2.x, psycopg 3, Alembic, **PostgreSQL 16** (oficial; mínimo 15 por `NULLS NOT DISTINCT`), TimescaleDB opcional, Polars, NumPy, pydantic-settings, pytest, ruff, Docker Compose, GitHub Actions CI.

## Fontes de dados (R1)

- Binance via endpoints públicos de klines (`data-api.binance.vision`; interface ccxt-compatível nos testes).
- Yahoo Finance via yfinance (sem cadastro); ver `docs/audits/R3D_YAHOO_1H_COVERAGE.md` para limites intraday observados.
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
| 2026-07-16 | `R1_GATE = APPROVED` | Hardening + CI verde + 39 testes | R1 encerrada |
| 2026-07-16 | Implementar R2 com `R2_PATTERN_SPECIFICATION.md` | Spec executável fornecida pelo humano | Oito padrões oficiais, sem retorno |
| 2026-07-16 | Custos R3 provisórios (BASE total 0.0024) | Numerics ausentes na metodologia | `1.0.0-provisional`; confirmação humana antes de R4 |
| 2026-07-16 | Merges PR #1–#4 em `main` + tags v0.1/v0.2/v0.3 | Autorização humana explícita | Cadeia R1–R3 em main |
| 2026-07-16 | R3D: universo cripto+ações, 1h/1d, sem recalibrar | Validação honesta em dados reais | Branch `feature/r3d-real-data-validation` |
| 2026-07-16 | R3D: 0 estratégias passaram o gate mecânico | 568 FAILS; 3272 INCONCLUSIVE; 0 promovidas | Resultado negativo aceito como conclusão válida |
| 2026-07-16 | Parâmetros e custos **não** alterados após abertura do holdout | Holdout consumido 1×; reuso proibido | Experimento `r3d-real-validation-v1` congelado |
| 2026-07-16 | Ações 1d ~4.988y → `PARTIAL_ACCEPTED_FOR_R3D` | Sem fill artificial; aceite humano para R3D | Não reclassifica COMPLETE |
| 2026-07-16 | `R3_GATE = REJECTED_NO_MEASURABLE_EDGE_V1` | Autorização humana pós-auditoria R3D | R4/R5 não iniciados; sem paper trading |
| 2026-07-17 | Iniciar R3E como experimento independente | Holdout R3D consumido; não reutilizar | `r3e-contextual-edge-v1`; nested WF |
| 2026-07-17 | R3E: M0–M5, DELTA_CANDLE=M5−M4, grids/thresholds congelados | Spec `R3E_CONTEXTUAL_EDGE_SPECIFICATION` | Sem AutoML/árvores; custos `1.0.0-provisional` |
| 2026-07-17 | `R3E_GATE = PENDING_FUTURE_UNSEEN_DATA` | Mesmo com resultados de desenvolvimento | R4 bloqueada; sem paper trading |
| 2026-07-17 | R3E code gate APPROVED; development run SYNTHETIC_ONLY | Relatórios marcados sem interpretação econômica | Tag `v0.5.0-r3e-engine` |
| 2026-07-17 | Merge PR #6 + tag `v0.5.0-r3e-engine` | Encerramento motor R3E | Real-data run autorizado em seguida |
| 2026-07-18 | R3E real-data exploratory run COMPLETE | Nested WF em OHLCV real; holdout R3D excluído | `CANDLE_ADDS_NO_VALUE`; R4 permanece BLOCKED |
| 2026-07-18 | Ratificação humana: sem evidência de valor incremental do candle | Protocolo R3E congelado; FDR sem Δ(M5−M4) significativo | `ECONOMIC_INTERPRETATION_ALLOWED=false`; `R3E_GATE=PENDING_FUTURE_UNSEEN_DATA`; `R4_STATUS=BLOCKED` |
| 2026-07-18 | Merge PR #7 em `main` | Registro da execução exploratória real + auditoria apenas | Não autoriza interpretação econômica, gate final R3E nem R4 |
| 2026-07-18 | Infra R3E future-unseen | Cutoff `2026-07-18T01:30:00Z`; ingestão append-only; ops sem peeking; gate automático | Coleta `NOT_STARTED`; R4 bloqueada; sem usar histórico como futuro |
| 2026-07-18 | Merge PR #8 em `main` (`2cf41f3`) | Infra de validação futura incorporada | Cutoff/freeze preservados; sem evidência científica |
| 2026-07-18 | Init formal da coleta future-unseen | `python -m wick.r3e.future_unseen init` (PR #9 → `20201e1`) | `R3E_FUTURE_DATA_COLLECTION=IN_PROGRESS`; `validate` não executado |
| 2026-07-18 | Backfill operacional 90d histórico | `python -m wick.r3e.operational_backfill collect` | 20/20 séries; 13725 barras; sandbox isolada; gate inalterado |
| 2026-07-18 | Merge PR #11 em `main` (`132bbb1`) | Backfill operacional incorporado | Scientific eligibility=false; future-unseen intacto |
| 2026-07-18 | Coletor incremental future-unseen | `python -m wick.r3e.future_unseen collect` | 70 obs pós-cutoff (crypto 1h); validate não executado |
| 2026-07-18 | Merge PR #12 em `main` (`a258e71`) | Coletor incremental + governança de revisão incorporados | Coleta permanece `IN_PROGRESS`; `validate` não executado; R4/R5 inalterados |
| 2026-07-18 | Próximo item R3E formalmente ambíguo | Fontes oficiais conflitam (coleta contínua vs readiness vs validate) | `BLOCKED_BY_AMBIGUOUS_NEXT_ITEM`; sem implementação por inferência |
