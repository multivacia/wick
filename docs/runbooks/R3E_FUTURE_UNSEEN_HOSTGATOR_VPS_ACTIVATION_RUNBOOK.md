# Runbook — HostGator VPS Activation (B5 preparation)

> Preparação e operação do collector future-unseen em VPS HostGator.
> Fail-closed. Sem peeking. Sem `validate`.
> `SCHEDULER_ACTIVATION_AUTHORIZED = false` até autorização humana explícita.

```text
OPERATIONAL_OWNER = Gustavo Almeida
HOST_STRATEGY = VPS
HOST_PROVIDER = HostGator
HOST_ID = wick-r3e-collector-01
DURABLE_STORE_PATH = /srv/wick
SECRET_STORAGE_STRATEGY = SYSTEMD_ENVIRONMENT_FILE
FAILURE_ALERT_DESTINATION = EMAIL
EMAIL_TRANSPORT_STATUS = PENDING_CONFIGURATION
```

## 0. Proibições

```bash
# NÃO executar
python -m wick.r3e.future_unseen validate
```

Não ativar o timer sem autorização humana de ativação.
Não commitar `/etc/wick/r3e-collector.env`.
Não usar GitHub Actions como dono do store oficial.
Não usar a máquina do agente Cursor como host operacional.

## 1. Pré-requisitos da VPS

- Ubuntu/Debian (ou equivalente systemd)
- Usuário com sudo para bootstrap
- Disco durável montado (não efêmero)
- Rede com egress para provedores públicos (binance / yahoo)
- NTP/chrony sincronizado (UTC)
- Python 3.11+ disponível para criar venv

Registrar após provisionamento (sem credenciais):

```text
HOST_PROVIDER_INSTANCE_ID =
HOST_PUBLIC_IP =
HOSTNAME_CONFIRMED =
```

## 2. Criação do usuário `wick`

```bash
sudo useradd --system --create-home --home-dir /home/wick --shell /usr/sbin/nologin wick || true
sudo mkdir -p /etc/wick
sudo chown root:root /etc/wick
sudo chmod 755 /etc/wick
```

Não executar o serviço como root.

## 3. Estrutura de diretórios

```bash
sudo mkdir -p \
  /srv/wick/app \
  /srv/wick/data/future_unseen/raw \
  /srv/wick/data/future_unseen/validated \
  /srv/wick/data/future_unseen/manifests \
  /srv/wick/reports/r3e_future_unseen \
  /srv/wick/backups \
  /srv/wick/logs

sudo chown -R wick:wick /srv/wick
sudo chmod 750 /srv/wick /srv/wick/data /srv/wick/reports /srv/wick/backups /srv/wick/logs
```

## 4. Clone / update do repositório

```bash
# primeira vez
sudo -u wick git clone https://github.com/multivacia/wick.git /srv/wick/app

# atualização (timer DESABILITADO durante update)
sudo systemctl stop wick-r3e-collector.timer || true
sudo -u wick git -C /srv/wick/app fetch --prune
sudo -u wick git -C /srv/wick/app checkout <approved_sha>
```

Symlinks duráveis (código usa paths relativos ao checkout):

```bash
sudo -u wick mkdir -p /srv/wick/app/data /srv/wick/app/reports
sudo -u wick ln -sfn /srv/wick/data/future_unseen /srv/wick/app/data/future_unseen
sudo -u wick ln -sfn /srv/wick/reports/r3e_future_unseen /srv/wick/app/reports/r3e_future_unseen
```

## 5. Ambiente Python

```bash
sudo -u wick python3 -m venv /srv/wick/app/.venv
sudo -u wick /srv/wick/app/.venv/bin/pip install -U pip
sudo -u wick /srv/wick/app/.venv/bin/pip install -e /srv/wick/app
```

## 6. Dependências

Instalar somente o necessário ao projeto (`pip install -e .` / extras do `pyproject.toml`).
Não instalar serviços científicos adicionais nesta etapa.

## 7. Criação do env file

```bash
sudo cp /srv/wick/app/ops/systemd/wick-r3e-collector.env.example /etc/wick/r3e-collector.env
sudo chown root:root /etc/wick/r3e-collector.env
sudo chmod 0600 /etc/wick/r3e-collector.env
sudo -e /etc/wick/r3e-collector.env   # preencher ALERT_EMAIL etc. sem versionar
```

Variáveis reais usadas pelo wrapper/código:

| Nome | Origem | Obrigatória para run-cycle |
|---|---|---|
| `PATH` | env file | recomendada (venv) |
| `PYTHONUNBUFFERED` | env file | recomendada |
| `FU_AS_OF` | wrapper opcional | não |
| `FU_DRY_RUN_ONLY` | wrapper opcional | não |
| `LOG_LEVEL` | Settings | não |
| `CANDLE_CLOSE_SAFETY_DELAY_SECONDS` | Settings | não |
| `BRAPI_TOKEN` | Settings | não (universo congelado sem brapi) |
| `ALERT_EMAIL` | alert adapter | para alertas |
| `EMAIL_TRANSPORT` | alert adapter | `mail`/`sendmail`/`smtp` |

`DATABASE_URL` **não** é usado por `run-cycle`.

## 8. Instalação das units

```bash
sudo cp /srv/wick/app/ops/systemd/wick-r3e-collector.service /etc/systemd/system/
sudo cp /srv/wick/app/ops/systemd/wick-r3e-collector.timer /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/wick-r3e-collector.service /etc/systemd/system/wick-r3e-collector.timer
```

## 9. daemon-reload

```bash
sudo systemctl daemon-reload
```

**Não** habilitar o timer ainda.

## 10. Preflight manual

```bash
sudo -u wick -E WICK_ROOT=/srv/wick ENV_FILE=/etc/wick/r3e-collector.env \
  /srv/wick/app/scripts/r3e_future_unseen_healthcheck.sh
```

## 11. Dry-run

```bash
sudo -u wick bash -lc 'cd /srv/wick/app && FU_DRY_RUN_ONLY=1 ./scripts/r3e_future_unseen_run_cycle.sh'
```

## 12. Execução manual controlada (somente se autorizada)

```bash
sudo -u wick bash -lc 'cd /srv/wick/app && ./scripts/r3e_future_unseen_run_cycle.sh'
# opcional: capturar exit e alertar
ec=$?
sudo -u wick -E ALERT_EMAIL=... /srv/wick/app/scripts/r3e_future_unseen_alert.sh "$ec" FAILED "manual_cycle"
```

Mapear status textuais: `FAILED`, `BLOCKED`, `SKIPPED_LOCKED_REPEATED`, `READY_TRANSITION`.

## 13. Verificação de logs

```bash
journalctl -u wick-r3e-collector.service -n 200 --no-pager
ls -lt /srv/wick/reports/r3e_future_unseen/automation_runs | head
cat /srv/wick/reports/r3e_future_unseen/automation_state.json
```

## 14. Verificação de store

```bash
ls /srv/wick/data/future_unseen/manifests
sudo -u wick bash -lc 'cd /srv/wick/app && python -m wick.r3e.future_unseen ops-report --json' || true
sudo -u wick bash -lc 'cd /srv/wick/app && python -m wick.r3e.future_unseen readiness --json'
```

## 15. Habilitação do timer

Somente após:

```text
SCHEDULER_ACTIVATION_AUTHORIZED = true
EMAIL_TRANSPORT_STATUS = CONFIGURED
```

```bash
sudo systemctl enable --now wick-r3e-collector.timer
systemctl list-timers wick-r3e-collector.timer --no-pager
```

## 16. Desabilitação

```bash
sudo systemctl disable --now wick-r3e-collector.timer
# permitir ciclo em voo terminar; se necessário aguardar até LOCK_TTL (3300s)
```

## 17. Rollback

```bash
sudo systemctl disable --now wick-r3e-collector.timer
# NÃO apagar observações aceitas
# opcional: voltar checkout para SHA anterior
sudo -u wick git -C /srv/wick/app checkout <previous_sha>
```

## 18. Backup

```bash
sudo -u wick -E WICK_ROOT=/srv/wick BACKUP_RETENTION_DAYS=14 \
  /srv/wick/app/scripts/r3e_future_unseen_backup.sh
```

## 19. Restauração

```bash
sudo systemctl disable --now wick-r3e-collector.timer
# escolher arquivo
ls -lt /srv/wick/backups/fu_backup_*.tar.gz | head
sudo -u wick tar -xzf /srv/wick/backups/fu_backup_<STAMP>.tar.gz -C /srv/wick
# revalidar paths/symlinks + healthcheck + dry-run
```

Não apagar o último backup válido.

## 20. Incidente e lock stale

Sintomas:

- exit `4` / `SKIPPED_LOCKED` repetido
- `automation.lock` presente com pid morto

Procedimento:

1. `systemctl status wick-r3e-collector.service`
2. inspecionar `reports/r3e_future_unseen/automation.lock`
3. se TTL expirado ou pid morto, o próximo ciclo recupera automaticamente
4. remoção manual só se recuperação automática falhar e não houver processo vivo
5. alertar `OPERATIONAL_OWNER` por e-mail (`scripts/r3e_future_unseen_alert.sh`)
6. **nunca** executar `validate` como mitigação

## Contrato de alertas

```text
ALERT_ON = FAILED | BLOCKED | SKIPPED_LOCKED_REPEATED | READY_TRANSITION
ALERT_DESTINATION = EMAIL
EMAIL_TRANSPORT_STATUS = PENDING_CONFIGURATION
```

READY apenas sinaliza autorização humana necessária; não autoriza `validate`.
