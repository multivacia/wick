# HostGator VPS Readiness Decisions — B5

## Metadados

```text
RELEASE = R3E
BACKLOG_ITEM = B5
TASK_ID = COLLECTION-SCHEDULER-ACTIVATION-001
HOST_PROVIDER = HostGator
HOST_ID = wick-r3e-collector-01
DURABLE_STORE_PATH = /srv/wick
OPERATIONAL_OWNER = Gustavo Almeida
HOST_READINESS_STATUS = BLOCKED_PENDING_REAL_HOST_DETAILS
SCHEDULER_ACTIVATION_AUTHORIZED = false
SCHEDULER_ACTIVATED = false
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
CREATED_AT = 2026-07-19T00:25:25Z
```

## Decisões humanas já aprovadas (não inferidas nesta ficha)

```text
OPERATIONAL_OWNER = Gustavo Almeida
HOST_STRATEGY = VPS
HOST_PROVIDER = HostGator
HOST_ID = wick-r3e-collector-01
DURABLE_STORE_PATH = /srv/wick
SECRET_STORAGE_STRATEGY = SYSTEMD_ENVIRONMENT_FILE
FAILURE_ALERT_DESTINATION = EMAIL
```

## Campos reais ainda necessários

Valores abaixo permanecem vazios até fornecimento explícito pelo proprietário da VPS.
Não preencher por inferência. Não registrar senha, chave privada, token ou segredo.

```text
HOST_PROVIDER_INSTANCE_ID =
HOST_PUBLIC_IP =
HOSTNAME_CONFIRMED =
SSH_ACCESS_CONFIRMED =
OPERATING_SYSTEM =
OPERATING_SYSTEM_VERSION =
CPU =
MEMORY =
DISK_TOTAL =
DISK_AVAILABLE =
PYTHON_VERSION =
GIT_VERSION =
SYSTEMD_AVAILABLE =
TIMEZONE =
FIREWALL_STATUS =
BACKUP_DESTINATION_CONFIRMED =
ALERT_EMAIL_ADDRESS =
EMAIL_TRANSPORT =
EMAIL_TRANSPORT_CONFIGURED =
```

## Critérios para HOST_READINESS_STATUS = READY

Todos devem ser verdadeiros/preenchidos:

```text
HOST_PROVIDER = HostGator
HOST_PROVIDER_INSTANCE_ID != empty
HOST_PUBLIC_IP != empty
HOSTNAME_CONFIRMED = wick-r3e-collector-01
SSH_ACCESS_CONFIRMED = true
OPERATING_SYSTEM is supported Linux
SYSTEMD_AVAILABLE = true
TIMEZONE = UTC
DISK_AVAILABLE is sufficient
BACKUP_DESTINATION_CONFIRMED = true
ALERT_EMAIL_ADDRESS != empty
EMAIL_TRANSPORT_CONFIGURED = true
```

Também:

- usuário `wick` existe;
- `/srv/wick` em storage persistente;
- `/etc/wick/r3e-collector.env` existe com modo 0600;
- secrets não estão no Git;
- timer permanece desabilitado até gate final de ativação.

## Estados intermediários

```text
HOST_READINESS_STATUS = BLOCKED_PENDING_REAL_HOST_DETAILS
```

Quando detalhes do host existirem mas e-mail ainda não:

```text
HOST_READINESS_STATUS = BLOCKED_PENDING_EMAIL_TRANSPORT
```

## Próxima decisão humana

Fornecer:

```text
HOST_PROVIDER_INSTANCE_ID
HOST_PUBLIC_IP
OPERATING_SYSTEM
OPERATING_SYSTEM_VERSION
CPU
MEMORY
DISK_TOTAL
ALERT_EMAIL_ADDRESS
EMAIL_TRANSPORT
```

E confirmar:

```text
SSH_ACCESS_CONFIRMED = true
SYSTEMD_AVAILABLE = true
BACKUP_DESTINATION_CONFIRMED = true
EMAIL_TRANSPORT_CONFIGURED = true | false
```

## Proibições

```text
SCHEDULER_ACTIVATION_AUTHORIZED = false
SCHEDULER_ACTIVATED = false
```

Não executar SSH, instalação de units, criação de env real, enable do timer, live run ou `validate` até autorização explícita posterior.
