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

## Trilha paralela — UX (experiência operacional)

Release **independente** do estado científico de R3E. Não modifica modelos, coleta, `validate`, readiness, scheduler, thresholds nem desbloqueia R4/R5.

| Campo | Valor |
|-------|--------|
| RELEASE_ID | UX-R1 |
| RELEASE_NAME | WICK OPERATIONAL EXPERIENCE |
| UX_R1_STATUS / UX-R1_STATUS | **IMPLEMENTATION_STARTED** |
| UX_B1_STATUS / UX-B1_STATUS | **MERGED** (`UX-RELEASE-FOUNDATION-001`; PR #31 → `5101c65`) |
| UX-B2_IMPACT_STATUS | **MERGED** (`DESIGN-SYSTEM-FOUNDATION-001`; PR #35 → `5bcb088`) |
| UX_B2_AUTHORIZATION_STATUS | **MERGED** (PR #43 → `34ce0e7`) |
| UX_B2_AUTHORIZATION_DECISION | **AUTHORIZED_FOR_INCREMENT_I1_ONLY** |
| UX_B2_STATUS | **I1_MERGED** |
| UX_B2_AUTHORIZED_INCREMENT | **I1** |
| I1_IMPLEMENTATION_STATUS | **MERGED** (PR #51 → `c283592`) |
| I2_STATUS | **ASSESSMENT_MERGED** (PR #55 → `ca24cc4`) |
| I2_AUTHORIZATION_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| I2_IMPLEMENTATION_AUTHORIZED | **false** |
| I5A_STATUS | **ARCHITECTURE_MERGED** (PR #56 → `134c93a`) |
| I5_ARCHITECTURE_DECISION | **AUTHORIZED_WITH_CONDITIONS** |
| I5_IMPLEMENTATION_AUTHORIZED | **false** |
| ROUTER_INSTALLATION_AUTHORIZED | **false** |
| I6A_STATUS | **DATA_PREPARATION_IN_PROGRESS** (draft PR #57) |
| I6_SCREEN_IMPLEMENTATION_AUTHORIZED | **false** |
| PARALLEL_KICKOFF_STATUS | **COMPLETE** (PRs #58–#61) |
| IMPLEMENTATION_EXECUTION_AUTHORIZED | **false** (I1 complete; no further increment authorized) |
| UX_B2_IMPLEMENTATION_AUTHORIZED | **false** (beyond I1) |
| UX_B3_STATUS / UX-B3_STATUS | **MERGED** (`OPERATIONAL-MVP-SCREEN-CONTRACTS-001`; PR #44 → `253bd82`) |
| UX_B3_IMPLEMENTATION_AUTHORIZED | **false** |
| UX_B4_STATUS / UX-B4_STATUS | **MERGED** (`OPERATIONAL-LANGUAGE-MICROCOPY-001`; PR #42 → `92e8320`) |
| UX_B4_IMPLEMENTATION_AUTHORIZED | **false** |
| RELEASE_OWNER | Gustavo Almeida |
| UX_FOUNDATION_MERGE_AUTHORIZED | **true** (fundação documental mergeada; UI não autorizada) |
| UI_IMPLEMENTATION_AUTHORIZED | **false** |
| UI_SCREEN_IMPLEMENTATION_AUTHORIZED | **false** |
| HOST_DISCOVERY | **DEFERRED** |
| OPERATIONAL_DEBT | **OPEN** |
| SCHEDULER_ACTIVATION | **BLOCKED** |
| R3E_SCIENTIFIC_STATE | **UNCHANGED** |
| Spec | `docs/releases/UX-R1_SPEC.md` |
| Backlog UX | `docs/ux/UX-R1_BACKLOG.md` |
| Fundação | `docs/ux/` · `docs/ai-specs/UX-R1-EXPERIENCE-FOUNDATION_SPEC.md` |
| Linguagem operacional B4 | `docs/ux/UX-R1-OPERATIONAL-LANGUAGE-GUIDE.md` (+ catálogos status/empty/failure/guardrails) |
| Contratos MVP B3 | `docs/ai-specs/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS_SPEC.md` |
| Impacto B1 | `docs/ai-impact/UX-RELEASE-FOUNDATION-001_IMPACT_ASSESSMENT.md` (`APPROVED`) |
| Impacto B2 | `docs/ai-impact/UX-R1-DESIGN-SYSTEM-FOUNDATION-001_IMPACT_ASSESSMENT.md` (`APPROVED`; implementação não autorizada) |
| Autorização B2 | `docs/ai-impact/UX-R1-DESIGN-SYSTEM-IMPLEMENTATION-AUTHORIZATION_IMPACT_ASSESSMENT.md` (`AUTHORIZED_FOR_INCREMENT_I1_ONLY`; **MERGED** PR #43) |
| Impacto B3 | `docs/ai-impact/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS-001_IMPACT_ASSESSMENT.md` (`APPROVED`; **MERGED** PR #44) |
| Impacto B4 | `docs/ai-impact/UX-R1-OPERATIONAL-LANGUAGE-MICROCOPY-001_IMPACT_ASSESSMENT.md` (`APPROVED`; **MERGED** PR #42) |
| PR fundação | https://github.com/multivacia/wick/pull/31 (**MERGED**) |
| PR design system (impacto) | https://github.com/multivacia/wick/pull/35 (**MERGED** `5bcb088`) |
| PR autorização I1 | https://github.com/multivacia/wick/pull/43 (**MERGED** `34ce0e7`) |
| PR linguagem B4 | https://github.com/multivacia/wick/pull/42 (**MERGED** `92e8320`) |
| PR contratos MVP B3 | https://github.com/multivacia/wick/pull/44 (**MERGED** `253bd82`) |
| PR I1 scaffold + CI | https://github.com/multivacia/wick/pull/51 (**MERGED** `c283592`) |
| PR kickoff paralelo I2/I5A/I6A | https://github.com/multivacia/wick/pull/58 (**MERGED** `d2a52cc`) |
| PR I2 design tokens assessment | https://github.com/multivacia/wick/pull/55 (**MERGED** `ca24cc4`) |
| PR I5A shell/nav architecture | https://github.com/multivacia/wick/pull/56 (**MERGED** `134c93a`) |

MVP funcional previsto (após autorização de UI): Visão Geral, Execuções da Coleta, Prontidão, Host e Automação, Experimento R3E (explicativo). Contratos de tela (UX-B3) e linguagem operacional (UX-B4) estão **MERGED**. Implementação de telas UI **não** autorizada. UX-B2 I1 (frontend scaffold + CI em `web/`) está **MERGED**; I2 assessment está **MERGED** com `AUTHORIZED_WITH_CONDITIONS` e `I2_IMPLEMENTATION_AUTHORIZED=false`; I5A architecture está **MERGED** com `AUTHORIZED_WITH_CONDITIONS`, `I5_IMPLEMENTATION_AUTHORIZED=false` e `ROUTER_INSTALLATION_AUTHORIZED=false`; I6A permanece draft (PR #57).

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
| R3E_READINESS_GATE | **IMPLEMENTED** (B2 / R3E-READINESS-001; status operacional separado do gate científico) |
| R3E_COLLECTION_AUTOMATION | **IMPLEMENTED** (B4 / COLLECTION-AUTOMATION-001; PR #19 MERGED `f773702`; validate não autorizado) |
| R3E_COLLECTION_SCHEDULER | **AWAITING_OPERATOR_DISCOVERY** (B5-D1; PR #28 MERGED `83308f5`; Gustavo deve rodar discovery no host real; timer não ativado) |
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
| 2026-07-18 | Autorização humana B2 / R3E-READINESS-001 | Ambiguidade pós-PR #12 resolvida | Próximo item = Future-Unseen Readiness Gate; validate/R4/R5 não autorizados |
| 2026-07-18 | Implementação B2 readiness gate | `python -m wick.r3e.future_unseen readiness` | Gate operacional READY/NOT_READY/BLOCKED; validate/R4/R5 inalterados |
| 2026-07-18 | Validação final PR #15 readiness | CI GREEN; 172 pytest; readiness NOT_READY | Merge autorizado por gates; validate/R4/R5 inalterados |
| 2026-07-18 | Merge PR #15 em `main` (`9220a14`) | Readiness gate B2 incorporado | Coleta permanece IN_PROGRESS; validate não autorizado; R4/R5 inalterados |
| 2026-07-18 | B3 coleta incremental continuity | dry-run+collect+idempotency; 70→85 obs | Readiness NOT_READY (window); validate não executado |
| 2026-07-18 | Merge PR #17 em `main` (`d32e027`) | Continuação B3 + reconciliação imutável `bc6a0d0` | Coleta permanece IN_PROGRESS; validate não autorizado; R4/R5 inalterados |
| 2026-07-18 | G1 impact assessment gate | Análise de impacto pré-implementação obrigatória | B4 fica IMPACT_ANALYSIS_REQUIRED até impacto aprovado |
| 2026-07-18 | Merge PR #20 em `main` (`3e839a2`) | Gate G1 vigente | PR #19 B4 bloqueada até impacto aprovado; validate inalterado |
| 2026-07-18 | B4 impacto APPROVE_WITH_CHANGES | Impacto aprovado; implementação autorizada com ajustes | PR #19 draft; merge não autorizado; validate inalterado |
| 2026-07-18 | Merge PR #19 em `main` (`f773702`) | Automação `run-cycle` B4 incorporada | Scheduler não ativado; validate não autorizado; R4/R5 inalterados |
| 2026-07-18 | Próximo item R3E pós-B4 ambíguo | Sem B5/TASK_ID oficial inequívoco | `BLOCKED_BY_AMBIGUOUS_NEXT_ITEM`; sem implementação por inferência |
| 2026-07-18 | Handoff pós-merge B4 (PR #22) | Merge PR #19 + reconciliação próximo item | Sem implementação; scheduler não ativado; validate/R4/R5 inalterados |
| 2026-07-18 | Humano nomeia B5 / COLLECTION-SCHEDULER-ACTIVATION-001 | Próximo item oficial pós-B4 | Impacto HIGH; `IMPACT_ASSESSMENT_STATUS=BLOCKED` até owner/host; sem ativação |
| 2026-07-18 | Impacto B5 scheduler (draft PR) | Comparação de hosts/store/secrets/rollback | Ativação bloqueada; validate/R4/R5 inalterados |
| 2026-07-18 | Merge PR #23 em `main` (`c098fa8`) | Impacto B5 BLOCKED incorporado | Sem ativação; 6 decisões humanas pendentes; validate/R4/R5 inalterados |
| 2026-07-18 | Decisões humanas B5 completas | Owner Gustavo; HostGator VPS; `/srv/wick`; systemd env; email | Impacto APPROVED; preparação autorizada; ativação ainda bloqueada |
| 2026-07-18 | Preparação HostGator B5 (draft PR) | units/runbook/backup/healthcheck | Timer não habilitado; validate/R4/R5 inalterados |
| 2026-07-19 | Merge PR #25 em `main` (`b5bb3f1`) | Preparação B5 HostGator incorporada | Timer não habilitado; host readiness pendente; validate/R4/R5 inalterados |
| 2026-07-19 | Ficha readiness HostGator B5 | Campos reais do VPS deixados vazios | `HOST_READINESS_STATUS=BLOCKED_PENDING_REAL_HOST_DETAILS` |
| 2026-07-19 | B5 troca para LOCAL_PERSISTENT_HOST | HostGator deferred; path `$HOME/wick-r3e` | Preparação local apenas; scheduler não ativado; validate/R4/R5 inalterados |
| 2026-07-19 | Merge PR #27 em `main` (`134f066`) | Preparação local B5 incorporada | Timer não habilitado; discovery no host real ainda pendente |
| 2026-07-19 | B5-D1 discovery preparation | Scripts read-only sh/ps1 + runbook | Resultado gerado só no host operacional; sem ativação |
| 2026-07-19 | Merge PR #28 em `main` (`83308f5`) | Discovery prep B5-D1 incorporada | Pacote operador publicado; discovery no Cursor não executada |
| 2026-07-19 | Pacote de execução operador B5-D1 | Guia copy-paste Windows/Linux | Aguardando `R3E_LOCAL_HOST_DISCOVERY_RESULT.md` do host real |
| 2026-07-19 | Abrir trilha paralela UX-R1 (Operational Experience) | Fundação UX-B1; sem UI; R3E inalterado | `UX-R1_STATUS=PLANNING`; `UI_IMPLEMENTATION_AUTHORIZED=false` |
| 2026-07-19 | Reconciliar impacto UX-B1 e congelar evidência final | Impacto APPROVED; review alinhada; PR #31 draft | `UX-B1_STATUS=READY_FOR_HUMAN_MERGE_REVIEW`; UX-B2 bloqueado; merge humano pendente |
| 2026-07-19 | Merge PR #31 UX-B1 Experience Foundation | Autorização humana; docs-only; R3E inalterado | `UX-B1_STATUS=MERGED`; UX-B2 bloqueado até impacto/autorização separados; UI não autorizada |
| 2026-07-19 | Iniciar impacto UX-B2 Design System Foundation | Fase IMPACT_ASSESSMENT_ONLY; sem UI | `UX-B2_STATUS=IMPACT_ASSESSMENT_IN_PROGRESS`; implementação não autorizada |
| 2026-07-19 | Reconciliar impacto UX-B2 (rebase + APPROVED) | Option B locked; gates definidos; sem código UI | `UX-B2_STATUS=IMPACT_ASSESSMENT_READY_FOR_HUMAN_REVIEW`; `UX_B2_IMPLEMENTATION_AUTHORIZED=false` |
| 2026-07-19 | Congelar evidência final UX-B2 (PR #35) | Revalidação local PASS; backlog alinhado; merge humano pendente | `IMPACT_ASSESSMENT_STATUS=APPROVED`; `UI_IMPLEMENTATION_AUTHORIZED=false` |
| 2026-07-19 | Merge PR #35 UX-B2 Design System impact | Docs-only; Option B locked; sem código UI | `UX_B2_IMPACT_STATUS=MERGED`; `UX_B2_IMPLEMENTATION_STATUS=BLOCKED_PENDING_EXPLICIT_AUTHORIZATION` |
| 2026-07-19 | Post-merge + merge-complete UX-B2 impact | PR #39 handoff; implementação bloqueada | `NEXT_ITEM=IMPLEMENTATION_AUTHORIZATION_ASSESSMENT`; UI não autorizada |
| 2026-07-19 | Avaliação de autorização de implementação UX-B2 | I1-only; stack locked; sem código UI | `UX_B2_AUTHORIZATION_ASSESSMENT_STATUS=IN_PROGRESS`; `AUTHORIZATION_DECISION=AUTHORIZED_FOR_INCREMENT_I1_ONLY` |
| 2026-07-19 | Merge PR #43 autorização I1 UX-B2 | Docs-only; I1 future task only | `UX_B2_AUTHORIZATION_STATUS=MERGED`; `I1_IMPLEMENTATION_STATUS=BLOCKED_PENDING_SEPARATE_TASK_AND_HUMAN_AUTHORIZATION` |
| 2026-07-19 | Post-merge + merge-complete autorização I1 UX-B2 | PR #45 handoff; I1 ainda bloqueado | `NEXT_ITEM=I1 FRONTEND-SCAFFOLD-AND-CI`; UI não autorizada |
| 2026-07-19 | UX-B4 linguagem operacional e microcopy | Catálogos docs-only; trilha independente de B2/B3 | `UX_B4_STATUS=CONTENT_DESIGN_READY_FOR_HUMAN_REVIEW`; `UX_B4_IMPLEMENTATION_AUTHORIZED=false`; UI não autorizada; R3E inalterado |
| 2026-07-19 | Merge PR #42 UX-B4 Operational Language | Autorização humana; docs-only; R3E inalterado | `UX_B4_STATUS=MERGED`; `UX_B4_IMPLEMENTATION_AUTHORIZED=false`; UI não autorizada |
| 2026-07-19 | Merge PR #44 UX-B3 Operational MVP Screen Contracts | Autorização humana; docs-only; consome UX-B4 | `UX_B3_STATUS=MERGED`; `UX_B3_IMPLEMENTATION_AUTHORIZED=false`; UI não autorizada |
| 2026-07-19 | Fechamento coordenado UX-B2/B3/B4 | B2 COMPLETE (I1-only); B3+B4 MERGED | `NEXT_ITEM=I1 FRONTEND-SCAFFOLD-AND-CI` (tarefa separada); scheduler/validate inalterados |
| 2026-07-19 | Merge PR #58 kickoff paralelo I2/I5A/I6A | Coordenação docs-only; PRs #55/#56/#57 permanecem draft | `I2_STATUS=ASSESSMENT_IN_PROGRESS`; `I5A_STATUS=ARCHITECTURE_IN_PROGRESS`; `I6A_STATUS=DATA_PREPARATION_IN_PROGRESS`; implementação não autorizada |
| 2026-07-19 | Merge PR #59 kickoff final-merge handoff | Status I2/I5A/I6A reconciliado em `main`; workstreams ainda draft | `PR58+PR59=MERGED`; PRs #55/#56/#57 `OPEN_DRAFT`; implementação não autorizada |
| 2026-07-19 | Merge PR #60 kickoff merge-complete record | Coordenação I2/I5A/I6A encerrada no track de kickoff | `PR58+PR59+PR60=MERGED`; PRs #55/#56/#57 `OPEN_DRAFT_REBASE_REQUIRED`; sem MAIN_TIP-only follow-up |
| 2026-07-19 | Merge PR #61 kickoff final-closure | Track de kickoff paralelo COMPLETE em `main` | `PARALLEL_KICKOFF_STATUS=COMPLETE`; PRs #55/#56/#57 abertos; implementação não autorizada |
| 2026-07-19 | Merge PR #55 I2 design tokens assessment | Docs-only; condições C1–C8; sem CSS/tokens | `I2_STATUS=ASSESSMENT_MERGED`; `AUTHORIZED_WITH_CONDITIONS`; `I2_IMPLEMENTATION_AUTHORIZED=false`; NEXT=I5A PR56 |
| 2026-07-19 | Merge PR #56 I5A shell/nav architecture | Docs-only; condições C1–C8; sem router/shell | `I5A_STATUS=ARCHITECTURE_MERGED`; `AUTHORIZED_WITH_CONDITIONS`; `I5_IMPLEMENTATION_AUTHORIZED=false`; `ROUTER_INSTALLATION_AUTHORIZED=false`; NEXT=I6A PR57 |
