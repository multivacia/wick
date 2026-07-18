# Auditoria — Backfill operacional histórico R3E (90d)

## Escopo

Validação operacional de aquisição, transformação e ingestão com dados históricos  
**inelegíveis** para o gate future-unseen.

## Classificação

```text
DATA_ORIGIN = HISTORICAL_OPERATIONAL_BACKFILL
SCIENTIFIC_EVIDENCE_ELIGIBLE = false
FUTURE_UNSEEN_ELIGIBLE = false
ECONOMIC_INTERPRETATION_ALLOWED = false
GATE_IMPACT_ALLOWED = false
R3E_OPERATIONAL_BACKFILL_RUN = COMPLETE
R3E_OPERATIONAL_BACKFILL_AUDIT = COMPLETE
R3E_OPERATIONAL_BACKFILL_SCIENTIFIC_ELIGIBILITY = false
```

## Proteções verificadas

| Proteção | Resultado |
|----------|-----------|
| Cutoff oficial imutável | PASS (hash inalterado) |
| Freeze M4/M5 preservado | PASS |
| `collection_state.json` inalterado | PASS |
| `n_observations` oficial = 0 | PASS |
| Séries present/missing oficiais inalteradas | PASS |
| Sem escrita em `data/future_unseen/{raw,validated,manifests}` | PASS |
| Fluxo oficial rejeita histórico por cutoff | PASS |
| Sem flags `--ignore-cutoff` / `--force` / `--allow-historical` | PASS |
| Política histórica separada de `FutureUnseenEligibilityPolicy` | PASS |
| Sem execução de `validate` / M4 / M5 | PASS |
| Sem peeking de efeito | PASS |
| R4 / R5 permanecem BLOCKED / NOT_STARTED | PASS |

## Isolamento de diretórios

| Raiz | Uso |
|------|-----|
| `data/operational_backfill/r3e_90d/` | sandbox histórica |
| `reports/r3e_operational_backfill/` | relatórios operacionais |
| `data/future_unseen/` | somente leitura / prova de igualdade |

## Estado científico oficial (inalterado)

```text
R3E_FUTURE_DATA_COLLECTION = IN_PROGRESS
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```

## Artefatos

- `reports/r3e_operational_backfill/collection_report.json`
- `reports/r3e_operational_backfill/data_quality_report.json`
- `reports/r3e_operational_backfill/series_coverage.json`
- `reports/r3e_operational_backfill/provider_mapping.json`
- `reports/r3e_operational_backfill/readiness_assessment.json`
- `reports/r3e_operational_backfill/schema_compatibility.json`
- `reports/r3e_operational_backfill/official_reject_probe.json`
- `reports/r3e_operational_backfill/official_state_isolation.json`
- `data/operational_backfill/r3e_90d/manifests/run_manifest.json`
- `docs/audits/R3E_OPERATIONAL_BACKFILL_90D_RESULTS.md`

## Comando

```bash
python -m wick.r3e.operational_backfill collect \
  --start 2026-04-19T01:30:00+00:00 \
  --end 2026-07-18T01:30:00+00:00 \
  --output data/operational_backfill/r3e_90d
```
