# Local Persistent Host — Environment Discovery (B5)

## Metadados

```text
RELEASE = R3E
BACKLOG_ITEM = B5
TASK_ID = COLLECTION-SCHEDULER-ACTIVATION-001
HOST_STRATEGY = LOCAL_PERSISTENT_HOST
HOST_PROVIDER = LOCAL
HOST_ID = wick-r3e-local-collector-01
DISCOVERY_CONTEXT = cursor_agent_environment_not_operational_host
DISCOVERED_AT = 2026-07-19T00:57:10Z
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
```

## Descoberta (sem mudanças permanentes)

Valores observados no ambiente de preparação do agente (não é o host operacional de Gustavo):

```text
LOCAL_OPERATING_SYSTEM = Linux
LOCAL_OPERATING_SYSTEM_VERSION = 6.12.94+
LOCAL_HOSTNAME = cursor
LOCAL_USERNAME = ubuntu
LOCAL_HOME = /home/ubuntu
PYTHON_VERSION = 3.12.3
GIT_VERSION = 2.43.0
AVAILABLE_DISK = 233G_available_on_overlay_root
DISK_BACKEND = overlay
SCHEDULER_MECHANISM = SYSTEMD
```

## Caminho persistente escolhido (template operacional)

```text
DURABLE_STORE_PATH = $HOME/wick-r3e
DURABLE_STORE_PATH_LINUX_MACOS = $HOME/wick-r3e
DURABLE_STORE_PATH_WINDOWS = %USERPROFILE%\wick-r3e
DURABLE_STORE_PATH_STATUS = PREFERRED_TEMPLATE_PENDING_OPERATOR_CONFIRMATION_ON_REAL_HOST
```

Estrutura alvo:

```text
<LOCAL_ROOT>/app
<LOCAL_ROOT>/data/future_unseen
<LOCAL_ROOT>/reports/r3e_future_unseen
<LOCAL_ROOT>/backups
<LOCAL_ROOT>/logs
<LOCAL_ROOT>/config
```

## Restrições

- não usar `/tmp`, workspace efêmero do Cursor, nem overlay de container como store oficial;
- o operador deve confirmar que `$HOME/wick-r3e` (ou equivalente Windows) está em disco persistente real;
- HostGator permanece `DEFERRED_FUTURE_MIGRATION`.
