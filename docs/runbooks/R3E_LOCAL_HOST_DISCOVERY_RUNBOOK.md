# Runbook — Local Host Discovery (B5-D1)

> Read-only discovery on the **real** operational host.
> The Cursor agent environment is **not** the operational host.
> Do not install packages, elevate privileges, register schedulers, run collection, or run `validate`.

```text
TASK_ID = LOCAL-HOST-DISCOVERY-PREPARATION-001
SUBTASK = B5-D1
SCHEDULER_ACTIVATION_AUTHORIZED = false
SCHEDULER_ACTIVATED = false
```

## Output

Scripts write:

```text
R3E_LOCAL_HOST_DISCOVERY_RESULT.md
```

in the current working directory (override with `R3E_DISCOVERY_OUT`).

Submit that file for readiness review. Do not commit secrets.

## Windows

From a clone of the repository on the local machine:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\r3e_local_host_discovery.ps1
```

Optional output path:

```powershell
$env:R3E_DISCOVERY_OUT = "$env:USERPROFILE\wick-r3e\R3E_LOCAL_HOST_DISCOVERY_RESULT.md"
.\scripts\r3e_local_host_discovery.ps1
```

## Linux / macOS

```bash
chmod +x scripts/r3e_local_host_discovery.sh
./scripts/r3e_local_host_discovery.sh
```

Optional output path:

```bash
export R3E_DISCOVERY_OUT="$HOME/wick-r3e/R3E_LOCAL_HOST_DISCOVERY_RESULT.md"
./scripts/r3e_local_host_discovery.sh
```

## What is collected

Inventory only: OS, hostname, username, home, shell, Python/Git versions, CPU/memory/disk summary, filesystem type, timezone, basic HTTPS reachability, scheduler availability, candidate paths.

## What is never collected

- public IP
- passwords / tokens / private keys
- contents of `.env` / `r3e-collector.env`
- shell history
- secrets of any kind

## Prohibitions

```bash
# NÃO executar
python -m wick.r3e.future_unseen validate
python -m wick.r3e.future_unseen run-cycle   # not part of discovery
systemctl enable --now ...                  # not part of discovery
```

## Next action

```text
NEXT_ACTION = submit this file for readiness review
```
