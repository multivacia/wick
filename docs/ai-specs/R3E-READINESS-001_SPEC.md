# R3E-READINESS-001 — Future-Unseen Readiness Gate

## Metadados

```text
RELEASE = R3E
BACKLOG_ITEM = B2
TASK_ID = R3E-READINESS-001
TITLE = Future-Unseen Readiness Gate
SPEC_STATUS = APPROVED
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
REPOSITORY = multivacia/wick
BASE_BRANCH = main
HEAD_BRANCH = feature/r3e-future-unseen-readiness-gate
SEQUENCE_AFTER = R3E-B1 / PR #12
VALIDATE_EXECUTION_AUTHORIZED = false
R4_AUTHORIZED = false
R5_AUTHORIZED = false
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
CREATED_AT = 2026-07-18T18:40:00Z
```

## Objetivo

Implementar gate operacional auditável que responde apenas `READY | NOT_READY | BLOCKED` sobre o store oficial `future_unseen`, sem executar validação científica.

## Escopo

- comando `python -m wick.r3e.future_unseen readiness`
- janela ≥ 90 dias pós-cutoff (`market_ts`)
- cobertura ≥ 16/20 séries com ≥ 200 barras
- integridade de hashes/manifestos
- classificação de gaps
- estado do coletor
- anti-peeking / anti-validate
- testes e runbook

## Não escopo

- `validate`
- M4/M5/`DELTA_CANDLE`/FDR/bootstrap/métricas econômicas
- alteração de cutoff/freeze/universo/thresholds científicos
- R4/R5

## Critérios de aceite

- [x] interface CLI `readiness` com `--as-of`, `--output-report`, `--strict`, `--json/--human`
- [x] exit codes 0/2/3
- [x] read-only / idempotente
- [x] testes obrigatórios do prompt
- [x] estado científico inalterado
- [x] `VALIDATE_AUTHORIZED = false` mesmo em `READY`
