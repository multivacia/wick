# Runbook — Local Persistent Host Activation (B5)

> Preparação local persistente. Fail-closed. Sem `validate`.
> `SCHEDULER_ACTIVATION_AUTHORIZED = false` até autorização humana explícita.

```text
OPERATIONAL_OWNER = Gustavo Almeida
HOST_STRATEGY = LOCAL_PERSISTENT_HOST
HOST_PROVIDER = LOCAL
HOST_ID = wick-r3e-local-collector-01
DURABLE_STORE_PATH = $HOME/wick-r3e
SECRET_STORAGE_STRATEGY = LOCAL_PROTECTED_ENV_FILE
FAILURE_ALERT_DESTINATION = LOCAL_LOG_AND_EMAIL_WHEN_AVAILABLE
ALERT_MODE = LOCAL_LOG
EMAIL_TRANSPORT_STATUS = DEFERRED
HOSTGATOR_VPS_STATUS = DEFERRED_FUTURE_MIGRATION
```

## 1. Ambiente detectado (preparação)

Ver `docs/operations/R3E_LOCAL_PERSISTENT_HOST_DISCOVERY.md`.

No host operacional real do operador, confirmar disco **não** efêmero antes de coletar.

## 2. Estrutura local

Linux/macOS:

```bash
export WICK_ROOT="${HOME}/wick-r3e"
mkdir -p \
  "$WICK_ROOT/app" \
  "$WICK_ROOT/data/future_unseen/raw" \
  "$WICK_ROOT/data/future_unseen/validated" \
  "$WICK_ROOT/data/future_unseen/manifests" \
  "$WICK_ROOT/reports/r3e_future_unseen" \
  "$WICK_ROOT/backups" \
  "$WICK_ROOT/logs" \
  "$WICK_ROOT/config"
chmod 700 "$WICK_ROOT/config"
```

Windows: `%USERPROFILE%\wick-r3e\` com as mesmas subpastas.

## 3. Instalação

```bash
git clone https://github.com/multivacia/wick.git "$WICK_ROOT/app"
cd "$WICK_ROOT/app"
python3 -m venv .venv
.venv/bin/pip install -U pip
.venv/bin/pip install -e .
```

Symlinks (código usa paths relativos ao checkout):

```bash
mkdir -p "$WICK_ROOT/app/data" "$WICK_ROOT/app/reports"
ln -sfn "$WICK_ROOT/data/future_unseen" "$WICK_ROOT/app/data/future_unseen"
ln -sfn "$WICK_ROOT/reports/r3e_future_unseen" "$WICK_ROOT/app/reports/r3e_future_unseen"
```

## 4. Configuração

```bash
cp "$WICK_ROOT/app/ops/local/wick-r3e-collector.env.example" \
   "$WICK_ROOT/config/r3e-collector.env"
chmod 600 "$WICK_ROOT/config/r3e-collector.env"
# editar ALERT_EMAIL etc. sem versionar
```

Windows destino: `%USERPROFILE%\wick-r3e\config\r3e-collector.env`.

## 5. Preflight

```bash
export WICK_ROOT="${HOME}/wick-r3e"
bash "$WICK_ROOT/app/scripts/r3e_future_unseen_local_healthcheck.sh"
```

## 6. Dry-run

```bash
cd "$WICK_ROOT/app"
FU_DRY_RUN_ONLY=1 bash scripts/r3e_future_unseen_local_run.sh
```

## 7. Execução manual controlada

Somente se autorizada operacionalmente (ainda sem scheduler):

```bash
bash scripts/r3e_future_unseen_local_run.sh
```

## 8. Backup

```bash
WICK_ROOT="$HOME/wick-r3e" BACKUP_RETENTION_DAYS=14 \
  bash "$WICK_ROOT/app/scripts/r3e_future_unseen_backup.sh"
```

## 9. Health check

Ver seção 5. Estados: `HEALTHY|DEGRADED|BLOCKED|FAILED`.

## 10. Preparação do scheduler

### Linux systemd (user)

```bash
mkdir -p ~/.config/systemd/user
cp "$WICK_ROOT/app/ops/local/systemd/"*.service ~/.config/systemd/user/
cp "$WICK_ROOT/app/ops/local/systemd/"*.timer ~/.config/systemd/user/
systemctl --user daemon-reload
# NÃO enable nesta fase
```

### Linux cron

Ver `ops/local/cron.example` — não instalar nesta fase.

### Windows Task Scheduler

Scripts:

- `ops/windows/register-wick-r3e-collector-task.ps1`
- `ops/windows/unregister-wick-r3e-collector-task.ps1`

Não registrar nesta fase.

## 11. Ativação posterior

Somente após:

```text
SCHEDULER_ACTIVATION_AUTHORIZED = true
```

e confirmação de disco persistente + healthcheck aceitável.

## 12. Desativação

```bash
systemctl --user disable --now wick-r3e-local-collector.timer
# ou remover linha cron / unregister task Windows
```

## 13. Rollback

Desativar scheduler; manter store append-only; restaurar backup se necessário.

## 14. Migração futura para HostGator

Ver `docs/runbooks/R3E_FUTURE_UNSEEN_LOCAL_TO_HOSTGATOR_MIGRATION.md`.

## 15. Lock stale

Mesmo contrato B4: `reports/r3e_future_unseen/automation.lock`, TTL 3300s, recuperação automática.

## 16. Preservação do store

Nunca apagar observações aceitas para “desfazer” um ciclo. Backup antes de migrações.

## Proibições

```bash
# NÃO executar
python -m wick.r3e.future_unseen validate
```
