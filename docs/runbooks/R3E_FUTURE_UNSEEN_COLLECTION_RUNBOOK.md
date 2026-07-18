# Runbook — Coleta R3E Future-Unseen

> Coleta operacional apenas. Sem peeking de efeito. Sem `validate` antecipado.

## Estado permitido durante a coleta

```text
R3E_FUTURE_DATA_COLLECTION = IN_PROGRESS
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
```

## Cutoff (imutável)

```text
FUTURE_UNSEEN_CUTOFF = 2026-07-18T01:30:00+00:00
```

Somente observações com **market_ts** estritamente posterior ao cutoff são elegíveis.  
O horário de ingestão **não** torna um dado elegível.

## Inicialização (já executada em main após merge da PR #8)

```bash
python -m wick.r3e.future_unseen init
```

Idempotente: preserva cutoff/freeze; não ingere dados; não executa validate; marca coleta formal como `IN_PROGRESS`.

## Ingestão

Comando oficial:

```bash
python -m wick.r3e.future_unseen ingest-json --input <arquivo.json>
```

Formato do arquivo: lista JSON de registros com campos

`symbol`, `timeframe`, `source`, `market_ts`, `open`, `high`, `low`, `close`, `volume`, opcionalmente `revision`.

Exemplo de origem rotulada:

```bash
python -m wick.r3e.future_unseen ingest-json --input batch.json --origin provider-export
```

### Regras de elegibilidade

- `market_ts` > `2026-07-18T01:30:00+00:00` (estritamente);
- timestamp **igual** ao cutoff → rejeitado;
- timestamp **anterior** → rejeitado;
- ingest time não substitui market timestamp;
- duplicidade idêntica → rejeitada;
- correção do provedor → exige `revision` incrementada + trilha de auditoria;
- overwrite silencioso → proibido;
- séries fora do universo oficial → rejeitadas;
- origem apontando para datasets proibidos (`reports/r3e_real`, `reports/r3d`, etc.) → rejeitada.

## Verificação após ingestão

```bash
python -m wick.r3e.future_unseen ops-report
```

Campos permitidos: estado da coleta, contagens, séries presentes/ausentes, primeiro/último `market_ts`, gaps, duplicidades, rejeições (via batch manifests), integridade de hashes, cobertura temporal, completude operacional.

### Proibido no ops-report

- Δ(M5−M4), p-values, métricas econômicas, rankings, decisões de gate.

## Proibição de validação antecipada

**Não executar** antes da condição mínima congelada estar integralmente satisfeita:

```bash
python -m wick.r3e.future_unseen validate
```

Não abrir relatórios intermediários de efeito.  
Não alterar critérios com base nos dados coletados.  
Não encerrar a coleta porque um resultado aparente parece positivo ou negativo (optional stopping proibido).

## Completude (relembrar da spec)

A coleta só fica pronta para `validate` quando:

1. ≥ 90 dias corridos após o cutoff;
2. ≥ 16 de 20 séries com ≥ 200 barras fechadas pós-cutoff;
3. integridade de hashes OK.

Até lá: `R3E_GATE = PENDING_FUTURE_UNSEEN_DATA`.

## Artefatos

| Path | Função |
|------|--------|
| `data/future_unseen/manifests/cutoff_manifest.json` | cutoff imutável |
| `data/future_unseen/manifests/model_freeze.json` | freeze M4/M5 |
| `data/future_unseen/manifests/initialization_manifest.json` | init formal |
| `data/future_unseen/manifests/collection_state.json` | estado oficial |
| `data/future_unseen/raw/` | lotes brutos append-only |
| `data/future_unseen/validated/` | lotes validados |
| `reports/r3e_future_unseen/ops_collection_report.json` | ops sem peeking |
