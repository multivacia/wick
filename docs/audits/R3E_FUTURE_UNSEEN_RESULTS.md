# R3E Future-Unseen — Resultados da infraestrutura (pré-coleta)

> Este documento registra a **entrega da engine**, não uma decisão confirmatória.
> Nenhum dado histórico foi usado como evidência futura não vista.

## Identidade

| Campo | Valor |
|-------|--------|
| experiment_id | `r3e-future-unseen-v1` |
| parent | `r3e-contextual-edge-v1` |
| FUTURE_UNSEEN_CUTOFF | `2026-07-18T01:30:00+00:00` |
| Spec | `docs/specs/R3E_FUTURE_UNSEEN_VALIDATION_SPEC.md` |

## Entregas

1. Spec congelada com cutoff, universo, M4/M5, bootstrap/FDR, slice primário e regras de gate.
2. Árvore isolada `data/future_unseen/{raw,validated,manifests}` + `reports/r3e_future_unseen/`.
3. Ingestão append-only com rejeição pré-cutoff, anti-duplicata, revisões auditáveis, hashes.
4. Relatório operacional sem métricas de efeito (`ops_collection_report.json`).
5. Freeze de protocolo/modelos (`model_freeze.json`).
6. Runner `python -m wick.r3e.future_unseen validate`.
7. Gate automático APPROVED / REJECTED / INCONCLUSIVE + bloqueio de R4.
8. Testes de proteções e decisões.

## Decisão de gate

**Não executada** — coleta ainda não iniciada (`NOT_STARTED`).  
Não há `gate_decision.json` de decisão final; isso é intencional.

## Estado oficial

```text
R3E_FUTURE_VALIDATION_ENGINE = COMPLETE
R3E_FUTURE_VALIDATION_AUDIT = COMPLETE
R3E_FUTURE_DATA_COLLECTION = NOT_STARTED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
```

## Próximo passo operacional (fora desta PR)

Ingerir OHLCV com `market_ts > cutoff` via `ingest-json` / rotina append-only, monitorar só ops reports, e somente após completude chamar `validate`.
