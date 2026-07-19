# Local Host Discovery — Operator Execution (Gustavo)

Short copy-paste guide. Run this on your **real local machine**, not in Cursor.

```text
TASK_ID = LOCAL-HOST-DISCOVERY-PREPARATION-001
SCHEDULER_ACTIVATION_AUTHORIZED = false
SCHEDULER_ACTIVATED = false
```

## Expected output

```text
R3E_LOCAL_HOST_DISCOVERY_RESULT.md
```

Send that file back for readiness review.

No admin/root required.

## Windows PowerShell

```powershell
git checkout main
git pull
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\r3e_local_host_discovery.ps1
```

## Linux / macOS

```bash
git checkout main
git pull
chmod +x scripts/r3e_local_host_discovery.sh
./scripts/r3e_local_host_discovery.sh
```

## Optional: choose output path

Windows:

```powershell
$env:R3E_DISCOVERY_OUT = "$env:USERPROFILE\wick-r3e\R3E_LOCAL_HOST_DISCOVERY_RESULT.md"
.\scripts\r3e_local_host_discovery.ps1
```

Linux/macOS:

```bash
export R3E_DISCOVERY_OUT="$HOME/wick-r3e/R3E_LOCAL_HOST_DISCOVERY_RESULT.md"
./scripts/r3e_local_host_discovery.sh
```

## Do not run

```text
# no package install
# no scheduler registration
# no scheduler activation
# no collection
# no validate
# no firewall changes
# no timezone changes
# no external data upload commands
```

```bash
# NÃO executar
python -m wick.r3e.future_unseen validate
python -m wick.r3e.future_unseen run-cycle
```

## After the file is created

1. Open `R3E_LOCAL_HOST_DISCOVERY_RESULT.md`
2. Confirm it has `HOST_DISCOVERY_STATUS` and `NEXT_ACTION = submit this file for readiness review`
3. Send the file for readiness review
