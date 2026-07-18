# R3E-B1-PR12-REVIEW-001 — Especificação de Revisão do Coletor Incremental

## Metadados

```text
RELEASE = R3E
BACKLOG_ITEM = B1
TASK_ID = R3E-B1-PR12-REVIEW-001
SPEC_STATUS = APPROVED
REPOSITORY = multivacia/wick
PULL_REQUEST = 12
BASE_BRANCH = main
HEAD_BRANCH = feature/r3e-future-unseen-incremental-collector
ORIGINAL_FEATURE_COMMITS = 1020313, a44cfec
CREATED_AT = 2026-07-18T17:28:12Z
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

## Evidências conhecidas

Evidência declarada da implementação (PR #12 / execução controlada):

```text
TESTS = 148 PASSED
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

## Critérios de aceite

- [ ] CI verde;
- [ ] somente barras fechadas são aceitas;
- [ ] dry-run não escreve no store;
- [ ] reexecução é idempotente;
- [ ] falha parcial não corrompe o store;
- [ ] cutoff permanece inalterado;
- [ ] freeze permanece inalterado;
- [ ] não existem flags inseguras;
- [ ] `validate` não foi executado;
- [ ] nenhuma métrica de efeito foi consultada;
- [ ] runbook existe;
- [ ] auditoria existe;
- [ ] runs são auditáveis;
- [ ] testes relevantes estão presentes e passam.

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
MERGE_STATUS = BLOCKED
```
