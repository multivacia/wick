# R3E-B1-PR12-REVIEW-001 — Revisão Técnica e de Segurança Científica

## Metadados

```text
RELEASE = R3E
BACKLOG_ITEM = B1
TASK_ID = R3E-B1-PR12-REVIEW-001
REVIEW_TYPE = TECHNICAL_AND_SCIENTIFIC_SAFETY
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
REVIEWER = Cursor executor com revisão materializada para validação independente por ChatGPT / Sofia
REPOSITORY = multivacia/wick
PULL_REQUEST = 12
BASE_BRANCH = main
HEAD_BRANCH = feature/r3e-future-unseen-incremental-collector
HEAD_COMMIT = 25135e15d2a9339370542d00013dfae00df34a1c
REVIEWED_AT = 2026-07-18T17:28:12Z
ORIGINAL_FEATURE_COMMITS = 1020313a8753f8beb6fa0fe64bb1f674ca01cf41, a44cfec911a04a92938c82dcada4ba7146a0133b
PR_13_STATUS = MERGED
PR_13_MERGE_COMMIT = 0c06d3222b20038785edb5507c0177353f8a649a
PR_13_MERGED_AT = 2026-07-18T17:27:57Z
PR_13_CI = GREEN
```

## 1. Objetivo

Revisar tecnicamente e sob segurança científica o coletor incremental oficial `future_unseen` da PR #12, sem autorizar merge automático e sem executar validação científica.

## 2. Materiais revisados

- `docs/ai-governance/` (framework já mergeado via PR #13);
- `docs/runbooks/R3E_FUTURE_UNSEEN_INCREMENTAL_COLLECTION_RUNBOOK.md`;
- `docs/audits/R3E_FUTURE_UNSEEN_INCREMENTAL_COLLECTOR_AUDIT.md`;
- `reports/r3e_future_unseen/collection_runs/`;
- descrição, commits e diff da PR #12;
- `src/wick/r3e/future_unseen/collector.py`;
- `src/wick/r3e/future_unseen/discovery.py`;
- `src/wick/r3e/future_unseen/cli.py`;
- `tests/test_r3e_future_unseen_collector.py`;
- estado oficial em `data/future_unseen/manifests/collection_state.json` e ops-report.

## 3. Escopo

Coleta incremental operacional pós-cutoff (`collect`, `--dry-run`, persistência append-only, auditoria por run). Fora de escopo: `validate`, gate, interpretação econômica, R4/R5, tuning.

## 4. Evidências

```text
TESTS_DECLARED = 148 PASSED
TECHNICAL_TESTS_THIS_REVIEW = 33 PASSED
  (tests/test_r3e_future_unseen_collector.py + tests/test_r3e_future_unseen.py)
DRY_RUN_CANDIDATES = 70
DRY_RUN_STORE_WRITES = 0
REAL_COLLECTION_ACCEPTED = 70
REAL_COLLECTION_SERIES = 5 crypto 1h
RERUN_NEW_RECORDS = 0
STORE_TOTAL_AFTER_RERUN = 70
YAHOO_ELIGIBLE_CLOSED_BARS = 0
CI_ON_FEATURE_TIP_BEFORE_MAIN_MERGE = SUCCESS (R1 validate)
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```

Branch atualizada com `origin/main` após merge da PR #13 via merge commit não destrutivo (`25135e1`). Sem force-push.

## 5. Análise do diff

O diff da PR #12 adiciona:

- descoberta incremental e coleta (`discovery.py`, `collector.py`);
- comando CLI `collect` com opções permitidas;
- testes de cutoff, candle fechado, dry-run, idempotência, falha parcial e anti-peeking;
- runbook, auditoria e relatórios de collection runs;
- artefatos operacionais do store (`batch_*`, `observation_index`, ops overlays).

Não altera:

- cutoff imutável;
- model freeze / thresholds / grids / custos;
- runner de efeito / gate decision paths como parte de `collect`;
- estados R4/R5.

`validate` permanece comando CLI separado com import lazy; `collector.py` e `discovery.py` não importam `validate`, `gate`, `pipeline` ou `compare`.

## 6. Testes e CI

- Testes técnicos permitidos executados nesta revisão: **33 passed**.
- CI da PR #12 no tip de feature anterior à incorporação da main: **SUCCESS**.
- Após merge de `main` (governança), novo CI será reavaliado no GitHub; confirmação visual antes do merge humano permanece condição operacional.

`python -m wick.r3e.future_unseen validate` **não** foi executado.

## 7. Idempotência

Confirmado por teste (`test_idempotent_second_collect`) e pela evidência de execução real: reexecução imediata produziu 0 candidatos novos e manteve `n_observations = 70`. Persistência via `ingest_batch` rejeita duplicatas idênticas.

## 8. Comportamento do dry-run

`--dry-run` calcula candidatos, gera relatório sob `collection_runs/dry_*`, e **não** escreve raw/validated/manifestos oficiais de lote (`written=false`, `n_observations` inalterado). Teste `test_dry_run_does_not_write` passa.

## 9. Tratamento de barras abertas

Candles abertos são filtrados por `filter_closed_candles` e rejeitados com motivo `CANDLE_NOT_CLOSED`. Timestamps `<= cutoff` rejeitados com `NOT_STRICTLY_AFTER_FUTURE_UNSEEN_CUTOFF`.

## 10. Tratamento de provedores

Falha de uma série isola o erro (`PROVIDER_ERROR` / `PARTIAL`) sem impedir demais séries. Retry limitado (default 3) via `retry_call`. Yahoo sem barras fechadas elegíveis aparece como ausência operacional (`NO_NEW_CLOSED_CANDLES` / sem candidatos), não como resultado científico.

## 11. Persistência e integridade do store

Append-only via `ingest_batch` em `data/future_unseen/{raw,validated,manifests}/`. Hashes SHA-256 por lote. Relatórios de run incluem `hash_manifest.json`. Ops-report mantém `hash_integrity_ok` e `effect_metrics_disclosed=false`.

## 12. Segurança científica

```text
R3E_FUTURE_DATA_COLLECTION = IN_PROGRESS
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```

Relatórios de coleta bloqueiam chaves científicas proibidas (`FORBIDDEN_REPORT_KEYS`). Sem flags `--ignore-cutoff`, `--allow-historical`, `--unlock-r4`, `--overwrite`, `--disable-hashes` no CLI de `collect`.

## 13. Achados

### Críticos

Nenhum.

### Altos

Nenhum.

### Médios

Nenhum.

### Baixos

- Confirmar visualmente no GitHub o CI após o merge de `main` (PR #13) na branch da PR #12 antes da autorização humana de merge.
- Yahoo ainda sem barras fechadas elegíveis pós-cutoff: estado operacional esperado; não bloqueia o coletor.

## 14. Riscos remanescentes

- Cobertura Yahoo só poderá ser exercitada quando houver sessão/barras fechadas posteriores ao cutoff.
- Completude prospectiva (90 dias / 200 barras) permanece pendente e fora desta revisão.

## 15. Decisão

```text
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
```

A aprovação técnica/documental **não** autoriza merge automático da PR #12.

## 16. Condições antes do merge

- CI verde no GitHub no tip atual da PR #12;
- sem alterações fora do escopo do coletor;
- decisão final de merge humana;
- não executar `validate` como parte do merge;
- manter R4/R5 bloqueados e sem interpretação econômica.
