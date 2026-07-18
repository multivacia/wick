# R3E-B1-PR12-REVIEW-001 — Especificação de Revisão do Coletor Incremental

## Metadados

```text
RELEASE = R3E
BACKLOG_ITEM = B1
TASK_ID = R3E-B1-PR12-REVIEW-001
SPEC_STATUS = APPROVED
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
REPOSITORY = multivacia/wick
PULL_REQUEST = 12
BASE_BRANCH = main
HEAD_BRANCH = feature/r3e-future-unseen-incremental-collector
ORIGINAL_IMPLEMENTATION_COMMITS = 1020313a8753f8beb6fa0fe64bb1f674ca01cf41, a44cfec911a04a92938c82dcada4ba7146a0133b
PREVIOUSLY_REVIEWED_HEAD = 25135e15d2a9339370542d00013dfae00df34a1c
CURRENT_PR_HEAD = b4eb335cb4ab45173acb3d21b51156c7a1a826cc
HEAD_SHA_AT_REVIEW = a769ba6254079ea7fe8f8771edf8b79ab3b7eecc
CREATED_AT = 2026-07-18T17:28:12Z
RECONCILED_AT = 2026-07-18T17:41:14Z
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```

## Objetivo

Revisar e validar o coletor incremental oficial de `future_unseen` antes de qualquer autorização de merge.

## Escopo

- comando:

```text
python -m wick.r3e.future_unseen collect
```

- suporte a `--dry-run`;
- coleta incremental;
- somente barras fechadas;
- idempotência;
- auditoria por execução;
- tratamento de crypto e Yahoo;
- preservação do store;
- preservação de cutoff e freeze;
- documentação, runbook e auditoria.

## Não escopo

- validação científica;
- interpretação econômica;
- readiness gate;
- tuning;
- alteração de modelo;
- alteração de thresholds;
- R4;
- R5.

## Evidências conhecidas (implementação original — declaradas)

Não confundir com testes reexecutados nesta revisão:

```text
DECLARED_PREVIOUS_TESTS = 148 PASSED
DRY_RUN_CANDIDATES = 70
DRY_RUN_STORE_WRITES = 0
REAL_COLLECTION_ACCEPTED = 70
REAL_COLLECTION_SERIES = 5 crypto 1h
RERUN_NEW_RECORDS = 0
STORE_TOTAL_AFTER_RERUN = 70
YAHOO_ELIGIBLE_CLOSED_BARS = 0
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```

## Reconciliação de HEAD

```text
PREVIOUSLY_REVIEWED_HEAD = 25135e15d2a9339370542d00013dfae00df34a1c
CURRENT_PR_HEAD = b4eb335cb4ab45173acb3d21b51156c7a1a826cc
COMMITS_RECONCILED = f86d1ae2b16f5a72970f89f595a3887f96d875a0, 7b1646d3d32d18166636b10f9dca97c60bb220ab, 69636de475c1985d50281245a8279605c6b37d5a, 8be78410ca67c0cefa001a2a75a1db1a6ffdbec7, a769ba6254079ea7fe8f8771edf8b79ab3b7eecc
CHANGE_CLASSIFICATION = DOCUMENTATION_AND_GOVERNANCE_WITH_OFFLINE_VALIDATOR
COLLECTOR_CODE_UNCHANGED_SINCE = 25135e15d2a9339370542d00013dfae00df34a1c
SCIENTIFIC_CODE_CHANGED = false
TECHNICAL_REVIEW_REMAINS_VALID = true
SCIENTIFIC_SAFETY_REVIEW_REMAINS_VALID = true
```

Justificativa: `25135e1..69636de` é só documentação PR12; `69636de..a769ba6` adiciona governança + validador offline. Código científico do coletor (`collector`/`discovery`/store/cutoff) permanece inalterado desde `25135e1`.

Regra: uma revisão só é válida para `HEAD_SHA_AT_REVIEW`. Se `CURRENT_PR_HEAD != HEAD_SHA_AT_REVIEW`, reconciliar formalmente, revisar complementarmente, ou voltar para `CHANGES_REQUIRED`.

## Critérios de aceite

Estado verificado em `2026-07-18T17:41:14Z` sobre tip `a769ba6`:

- [x] CI verde no tip atual (`R1 validate` SUCCESS no head `a769ba6`);
- [x] somente barras fechadas são aceitas (testes técnicos + inspeção do coletor);
- [x] dry-run não escreve no store;
- [x] reexecução é idempotente;
- [x] falha parcial não corrompe o store;
- [x] cutoff permanece inalterado;
- [x] freeze permanece inalterado;
- [x] não existem flags inseguras equivalentes a ignore-cutoff / unlock-r4 / overwrite;
- [x] `validate` não foi executado nesta revisão;
- [x] nenhuma métrica de efeito foi consultada;
- [x] runbook existe;
- [x] auditoria existe;
- [x] runs são auditáveis;
- [x] testes relevantes estão presentes e passam (`38 passed` nesta revisão: 33 collector/store + 5 validator).

## Pré-condições de revisão

```text
PR_13_STATUS = MERGED
PR_13_MERGE_COMMIT = 0c06d3222b20038785edb5507c0177353f8a649a
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
CURRENT_MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
```

## Proibições

- Não considerar revisão válida após mudanças materiais não revisadas.
- Não preencher SHA/CI/testes apenas a partir de texto de prompt — consultar Git/GitHub/pytest.
- Não autorizar merge automático.
