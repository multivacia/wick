# Runbook — Local Persistent Host → HostGator VPS Migration

```text
SOURCE_HOST_STRATEGY = LOCAL_PERSISTENT_HOST
TARGET_HOST_STRATEGY = VPS
TARGET_HOST_PROVIDER = HostGator
TARGET_HOST_ID = wick-r3e-collector-01
TARGET_DURABLE_STORE_PATH = /srv/wick
SCHEDULER_ACTIVATION_AUTHORIZED = false
```

## Objetivo

Migrar store/relatórios de `$HOME/wick-r3e` (local) para `/srv/wick` (HostGator) sem coleta simultânea e sem `validate`.

## Sequência

1. **Congelar scheduler local**
   ```bash
   systemctl --user disable --now wick-r3e-local-collector.timer || true
   # Windows: ops/windows/unregister-wick-r3e-collector-task.ps1
   ```
2. **Backup local**
   ```bash
   WICK_ROOT="$HOME/wick-r3e" bash "$HOME/wick-r3e/app/scripts/r3e_future_unseen_backup.sh"
   ```
3. **Validar checksums**
   ```bash
   sha256sum "$HOME/wick-r3e/backups"/fu_backup_*.tar.gz | tee /tmp/fu_backup_checksums.txt
   ```
4. **Copiar store e relatórios** para staging na VPS (sem ativar timer VPS):
   - `data/future_unseen`
   - `reports/r3e_future_unseen`
   - manter `automation.lock` ausente no destino
5. **Restaurar na VPS** sob `/srv/wick` conforme runbook HostGator.
6. **Preflight VPS** (`r3e_future_unseen_healthcheck.sh` com `WICK_ROOT=/srv/wick`).
7. **Dry-run VPS** (`FU_DRY_RUN_ONLY=1` + `run-cycle`).
8. **Evitar coleta simultânea**: confirmar scheduler local desabilitado antes de qualquer live VPS.
9. **Trocar ownership do store**: declarar HostGator como store oficial em `docs/operations` / PROJECT após sucesso.
10. **Ativar VPS** somente com `SCHEDULER_ACTIVATION_AUTHORIZED = true`.
11. **Rollback local**: se VPS falhar, manter local como dono; não apagar backups locais.

## Proibições

- não executar `validate` em nenhum lado;
- não habilitar dois schedulers ao mesmo tempo;
- não commitar secrets/`r3e-collector.env`.
