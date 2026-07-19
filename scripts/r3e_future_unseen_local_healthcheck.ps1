# Local persistent host healthcheck (Windows). No secrets printed. No validate.
$ErrorActionPreference = "Continue"
$Status = "HEALTHY"
$Reasons = New-Object System.Collections.Generic.List[string]

function Set-Status([string]$Next) {
  $order = @{ HEALTHY = 0; DEGRADED = 1; BLOCKED = 2; FAILED = 3 }
  if ($order[$Next] -gt $order[$script:Status]) { $script:Status = $Next }
}
function Note([string]$R) { $Reasons.Add($R) | Out-Null }

$WickRoot = if ($env:WICK_ROOT) { $env:WICK_ROOT } else { Join-Path $env:USERPROFILE "wick-r3e" }
$AppDir = Join-Path $WickRoot "app"
$DataDir = Join-Path $WickRoot "data\future_unseen"
$ReportsDir = Join-Path $WickRoot "reports\r3e_future_unseen"
$LogDir = Join-Path $WickRoot "logs"
$BackupDir = Join-Path $WickRoot "backups"
$ConfigDir = Join-Path $WickRoot "config"
$EnvFile = if ($env:ENV_FILE) { $env:ENV_FILE } else { Join-Path $ConfigDir "r3e-collector.env" }

foreach ($p in @($AppDir, $DataDir, $ReportsDir, $LogDir, $BackupDir, $ConfigDir)) {
  if (-not (Test-Path $p)) { Note "MISSING_DIR:$p"; Set-Status "FAILED" }
}
if (-not (Test-Path $EnvFile)) { Note "ENV_FILE_MISSING"; Set-Status "BLOCKED" }

$Runner = Join-Path $AppDir "scripts\r3e_future_unseen_local_run.ps1"
$Cycle = Join-Path $AppDir "scripts\r3e_future_unseen_run_cycle.sh"
if (-not (Test-Path $Runner)) { Note "RUNNER_MISSING"; Set-Status "FAILED" }
if ((Test-Path $Runner) -and (Select-String -Path $Runner -Pattern "wick.r3e.future_unseen validate" -Quiet)) {
  Note "VALIDATE_INVOCATION"; Set-Status "BLOCKED"
}

$Lock = Join-Path $ReportsDir "automation.lock"
if (Test-Path $Lock) { Note "LOCK_PRESENT"; Set-Status "DEGRADED" }

$TaskName = "Wick-R3E-Future-Unseen-Collector"
$SchedPrepared = Test-Path (Join-Path $AppDir "ops\windows\register-wick-r3e-collector-task.ps1")
$SchedActivated = $false
try {
  $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
  if ($task -and $task.State -ne "Disabled") { $SchedActivated = $true }
} catch { }

if ($SchedActivated) { Note "SCHEDULER_ACTIVATED"; Set-Status "DEGRADED" }
if (-not $SchedPrepared) { Note "SCHEDULER_TEMPLATES_MISSING"; Set-Status "DEGRADED" }

Write-Output "STATUS=$Status"
Write-Output "SCHEDULER_PREPARED=$SchedPrepared"
Write-Output "SCHEDULER_ACTIVATED=$SchedActivated"
if ($Reasons.Count -gt 0) { Write-Output ("REASONS=" + ($Reasons -join ",")) } else { Write-Output "REASONS=none" }

switch ($Status) {
  "HEALTHY" { exit 0 }
  "DEGRADED" { exit 10 }
  "BLOCKED" { exit 20 }
  default { exit 30 }
}
