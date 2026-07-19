# Idempotent example to register Windows Task Scheduler job.
# DO NOT run automatically during preparation. Requires explicit human activation auth later.
param(
  [string]$TaskName = "Wick-R3E-Future-Unseen-Collector",
  [string]$WickRoot = $(if ($env:WICK_ROOT) { $env:WICK_ROOT } else { Join-Path $env:USERPROFILE "wick-r3e" })
)

$ErrorActionPreference = "Stop"
$Runner = Join-Path $WickRoot "app\scripts\r3e_future_unseen_local_run.ps1"
if (-not (Test-Path $Runner)) { throw "missing runner: $Runner" }

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$Runner`""
# Hourly at minute 15
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date "00:15") -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration ([TimeSpan]::MaxValue)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew -RunOnlyIfNetworkAvailable
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force | Out-Null
Write-Host "REGISTERED task=$TaskName (not started by this script beyond schedule definition)"
Write-Host "CADENCE=hourly_minute_15 ALLOW_OVERLAP=false RUN_ONLY_IF_NETWORK_AVAILABLE=true START_WHEN_AVAILABLE=true"
