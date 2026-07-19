# Unregister Windows Task Scheduler job. Safe if missing.
param(
  [string]$TaskName = "Wick-R3E-Future-Unseen-Collector"
)
$ErrorActionPreference = "SilentlyContinue"
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
Write-Host "UNREGISTERED_OR_ABSENT task=$TaskName"
