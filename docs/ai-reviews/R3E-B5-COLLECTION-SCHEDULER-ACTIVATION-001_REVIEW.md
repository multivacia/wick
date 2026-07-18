# COLLECTION-SCHEDULER-ACTIVATION-001 — Revisão Técnica e de Segurança Científica

## Metadados

```text
RELEASE = R3E
BACKLOG_ITEM = B5
TASK_ID = COLLECTION-SCHEDULER-ACTIVATION-001
REVIEW_TYPE = TECHNICAL_AND_SCIENTIFIC_SAFETY
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_PATH = docs/ai-impact/COLLECTION-SCHEDULER-ACTIVATION-001_IMPACT_ASSESSMENT.md
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
SCHEDULER_ACTIVATION_AUTHORIZED = false
SCHEDULER_ACTIVATED = false
OPERATIONAL_OWNER = Gustavo Almeida
HOST_STRATEGY = VPS
HOST_PROVIDER = HostGator
HOST_ID = wick-r3e-collector-01
DURABLE_STORE_PATH = /srv/wick
SECRET_STORAGE_STRATEGY = SYSTEMD_ENVIRONMENT_FILE
FAILURE_ALERT_DESTINATION = EMAIL
EMAIL_TRANSPORT_STATUS = PENDING_CONFIGURATION
REPOSITORY = multivacia/wick
PULL_REQUEST = 25
BASE_BRANCH = main
BASE_SHA_AT_REVIEW = 1b84b2c2fec33e7e9ebde3c7f8be6a59c0e383bd
HEAD_BRANCH = cursor/r3e-b5-hostgator-vps-activation-preparation-2b14
IMPLEMENTATION_HEAD = 935df86e548c6dd45f2f2ac6b5208831e9466f85
CONTENT_REVIEWED_THROUGH_HEAD = 935df86e548c6dd45f2f2ac6b5208831e9466f85
PREVIOUSLY_REVIEWED_HEAD = 935df86e548c6dd45f2f2ac6b5208831e9466f85
COMMITS_RECONCILED = evidence_freeze_and_pr_number_only
FINAL_CANDIDATE_HEAD = 3264e773e20573bc87a42eaee36bd972ad7ef1d7
CURRENT_PR_HEAD = 3264e773e20573bc87a42eaee36bd972ad7ef1d7
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
REVIEWED_AT = 2026-07-18T21:42:00Z
```

Impact path: `docs/ai-impact/COLLECTION-SCHEDULER-ACTIVATION-001_IMPACT_ASSESSMENT.md`

## Materiais revisados

- impacto B5 atualizado para APPROVED com decisões humanas
- `ops/systemd/wick-r3e-collector.service`
- `ops/systemd/wick-r3e-collector.timer`
- `ops/systemd/wick-r3e-collector.env.example`
- `scripts/r3e_future_unseen_backup.sh`
- `scripts/r3e_future_unseen_healthcheck.sh`
- `scripts/r3e_future_unseen_alert.sh`
- `docs/runbooks/R3E_FUTURE_UNSEEN_HOSTGATOR_VPS_ACTIVATION_RUNBOOK.md`
- `tests/test_r3e_b5_hostgator_ops_preparation.py`

## Avaliação

| Item | Classificação | Notas |
|---|---|---|
| Impacto APPROVED + decisões humanas | ACCEPT | owner/host/path/secrets/alerts definidos |
| Units systemd User=wick / hardening | ACCEPT | ProtectSystem=strict + ReadWritePaths duráveis |
| Timer UTC :15 | ACCEPT | OnCalendar com UTC; Persistent=true |
| Paths /srv/wick + symlinks | ACCEPT | store sobrevive a update de código |
| Env example sem secrets reais | ACCEPT | apenas nomes; destino /etc/wick mode 0600 |
| Backup atômico + retenção | ACCEPT | temp+rename; não remove último válido |
| Healthcheck STATUS contract | ACCEPT | HEALTHY/DEGRADED/BLOCKED/FAILED |
| Alert adapter | ACCEPT | EMAIL_TRANSPORT_STATUS=PENDING_CONFIGURATION até mail real |
| Runbook HostGator | ACCEPT | 20 seções; sem validate |
| Ausência de validate | ACCEPT | scripts/runbook/tests cobrem |
| Ausência de ativação real | ACCEPT | timer não habilitado nesta tarefa |
| Lock B4 compatível | ACCEPT | lock de aplicação permanece proteção final |
| Ciência / R4 / R5 | ACCEPT | estado preservado; activation auth false |

## Achados

1. `EMAIL_TRANSPORT_STATUS = PENDING_CONFIGURATION` bloqueia ativação final, não a preparação.
2. `HOST_PROVIDER_INSTANCE_ID` / IP / hostname ainda `PENDING_PROVISIONING` até VPS real.
3. `ProtectSystem=strict` exige symlinks corretos para `data`/`reports`; documentado no runbook/healthcheck.

## Decisão

```text
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
SCHEDULER_ACTIVATION_AUTHORIZED = false
SCHEDULER_ACTIVATED = false
FINAL_RECOMMENDATION = merge preparation artifacts when CI green; do not enable timer; do not run validate; await separate human activation authorization after VPS provisioning and email transport configuration
```
