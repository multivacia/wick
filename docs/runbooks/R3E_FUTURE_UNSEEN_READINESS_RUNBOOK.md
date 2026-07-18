# Runbook — Future-Unseen Readiness Gate (B2 / R3E-READINESS-001)

## Objetivo

Avaliar se o store oficial `future_unseen` está operacionalmente pronto para uma futura validação científica.

O comando **não** executa `validate` e **não** altera o gate científico R3E.

## Comando

```bash
python -m wick.r3e.future_unseen readiness
python -m wick.r3e.future_unseen readiness --as-of 2026-10-20T00:00:00+00:00
python -m wick.r3e.future_unseen readiness --output-report reports/r3e_future_unseen/readiness_report.json
python -m wick.r3e.future_unseen readiness --strict
python -m wick.r3e.future_unseen readiness --human
```

## Exit codes

| Code | Status |
|------|--------|
| 0 | `READY` |
| 2 | `NOT_READY` |
| 3 | `BLOCKED` |

## Thresholds oficiais (não inventar)

Fonte: `src/wick/r3e/future_unseen/config.py` e `docs/specs/R3E_FUTURE_UNSEEN_VALIDATION_SPEC.md`

```text
MIN_CALENDAR_DAYS_AFTER_CUTOFF = 90
MIN_SERIES_COMPLETE = 16
MIN_BARS_PER_SERIES = 200
```

## Propriedades

- read-only no store (raw/validated/manifests);
- determinístico com `--as-of`;
- reexecução idempotente;
- sem métricas de efeito;
- `VALIDATE_AUTHORIZED = false` mesmo se `READY`.

## Interpretação

- `READY`: critérios operacionais satisfeitos; ainda exige autorização humana para `validate`.
- `NOT_READY`: coleta/cobertura incompleta sem falha estrutural.
- `BLOCKED`: integridade/segurança/governança comprometidas.
