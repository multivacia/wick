# Local persistent host runner (Windows).
# Does NOT invoke validate. Does NOT register Task Scheduler jobs.
$ErrorActionPreference = "Stop"

function Write-UtcLog([string]$Message) {
  $ts = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  $line = "$ts $Message"
  Write-Host $line
  if ($script:LogFile) { Add-Content -Path $script:LogFile -Value $line }
}

$WickRoot = if ($env:WICK_ROOT) { $env:WICK_ROOT } else { Join-Path $env:USERPROFILE "wick-r3e" }
$AppDir = Join-Path $WickRoot "app"
$ConfigEnv = if ($env:WICK_ENV_FILE) { $env:WICK_ENV_FILE } else { Join-Path $WickRoot "config\r3e-collector.env" }
$ReportsDir = Join-Path $WickRoot "reports\r3e_future_unseen"
$DataDir = Join-Path $WickRoot "data\future_unseen"
$LogDir = Join-Path $WickRoot "logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$script:LogFile = Join-Path $LogDir ("local_run_" + (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ") + ".log")

Write-UtcLog "START wick_root=$WickRoot"

if ($WickRoot -match '^(C:\\Windows\\Temp|.*\\AppData\\Local\\Temp)') {
  throw "refusing ephemeral WICK_ROOT=$WickRoot"
}

if (Test-Path $ConfigEnv) {
  Get-Content $ConfigEnv | ForEach-Object {
    if ($_ -match '^\s*#' -or $_ -match '^\s*$') { return }
    $pair = $_.Split("=", 2)
    if ($pair.Count -eq 2) {
      Set-Item -Path "Env:$($pair[0].Trim())" -Value $pair[1].Trim()
    }
  }
  Write-UtcLog "ENV_LOADED path=$ConfigEnv"
} else {
  Write-UtcLog "ENV_MISSING path=$ConfigEnv"
}

foreach ($p in @($AppDir, $DataDir, $ReportsDir)) {
  if (-not (Test-Path $p)) { throw "missing path: $p" }
}

Set-Location $AppDir
$venvPython = Join-Path $AppDir ".venv\Scripts\python.exe"
$python = if (Test-Path $venvPython) { $venvPython } else { "python" }

$argsList = @("-m", "wick.r3e.future_unseen", "run-cycle", "--json")
if ($env:FU_DRY_RUN_ONLY -eq "1") { $argsList += "--dry-run-only" }
if ($env:FU_AS_OF) { $argsList += @("--as-of", $env:FU_AS_OF) }

Write-UtcLog "RUN_CYCLE begin"
& $python @argsList 2>&1 | Tee-Object -FilePath $script:LogFile -Append
$ec = $LASTEXITCODE
Write-UtcLog "END exit=$ec"
exit $ec
