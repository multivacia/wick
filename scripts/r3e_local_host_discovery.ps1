# Read-only local host discovery for B5-D1 (Windows).
# Does NOT install packages, require Administrator, register schedulers,
# run collection, run validate, print secrets, or transmit results.
$ErrorActionPreference = "Stop"

$Out = if ($env:R3E_DISCOVERY_OUT) { $env:R3E_DISCOVERY_OUT } else { Join-Path (Get-Location) "R3E_LOCAL_HOST_DISCOVERY_RESULT.md" }
$UtcNow = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

# Refuse elevated execution when detectable
try {
  $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
  $principal = New-Object Security.Principal.WindowsPrincipal($identity)
  if ($principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw "refuse to run as Administrator"
  }
} catch {
  if ("$($_.Exception.Message)" -match "refuse to run") { throw }
}

$os = Get-CimInstance Win32_OperatingSystem
$cs = Get-CimInstance Win32_ComputerSystem
$cpuInfo = Get-CimInstance Win32_Processor | Select-Object -First 1

$osName = $os.Caption
$osVer = $os.Version
$hostName = $env:COMPUTERNAME
$userName = $env:USERNAME
$homeDir = $env:USERPROFILE
$shellName = "powershell"
$psVersion = $PSVersionTable.PSVersion.ToString()

$pythonCommand = "missing"
$pythonVersion = "missing"
foreach ($cand in @("python", "py")) {
  $cmd = Get-Command $cand -ErrorAction SilentlyContinue
  if ($cmd) {
    $pythonCommand = $cand
    try { $pythonVersion = (& $cand --version 2>&1 | Out-String).Trim() } catch { $pythonVersion = "unknown" }
    break
  }
}

$gitVersion = "missing"
$gitCmd = Get-Command git -ErrorAction SilentlyContinue
if ($gitCmd) { $gitVersion = (git --version 2>&1 | Out-String).Trim() }

$cpu = if ($cpuInfo) { $cpuInfo.Name } else { "unknown" }
$memoryTotal = if ($os.TotalVisibleMemorySize) { "{0:N0}MB" -f ($os.TotalVisibleMemorySize / 1024) } else { "unknown" }

$drive = Get-PSDrive -Name ($homeDir.Substring(0,1)) -ErrorAction SilentlyContinue
$diskTotal = "unknown"
$diskAvailable = "unknown"
$fsType = "unknown"
if ($drive) {
  $diskTotal = "{0:N1}GB" -f (($drive.Used + $drive.Free) / 1GB)
  $diskAvailable = "{0:N1}GB" -f ($drive.Free / 1GB)
}
try {
  $vol = Get-Volume -DriveLetter $homeDir.Substring(0,1) -ErrorAction SilentlyContinue
  if ($vol) { $fsType = $vol.FileSystemType }
} catch { }

$timezone = [System.TimeZoneInfo]::Local.Id
$networkAvailable = "false"
$outboundHttps = "false"
try {
  $resp = Invoke-WebRequest -Uri "https://example.com" -Method Head -TimeoutSec 5 -UseBasicParsing
  if ($resp.StatusCode -ge 200) {
    $networkAvailable = "true"
    $outboundHttps = "true"
  }
} catch { }

$taskSchedulerAvailable = "false"
try {
  Get-ScheduledTask -ErrorAction Stop | Out-Null
  $taskSchedulerAvailable = "true"
} catch {
  # Get-ScheduledTask may require modules; presence of schtasks.exe is enough as availability signal
  if (Get-Command schtasks.exe -ErrorAction SilentlyContinue) { $taskSchedulerAvailable = "true" }
}
$systemdAvailable = "false"
$cronAvailable = "false"
$schedulerMechanism = if ($taskSchedulerAvailable -eq "true") { "WINDOWS_TASK_SCHEDULER" } else { "MANUAL_ONLY" }

$localRootCandidate = Join-Path $homeDir "wick-r3e"
$localRootExists = Test-Path $localRootCandidate
$localRootWritable = Test-Path $homeDir

$repoPath = (Get-Location).Path
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoCandidate = Resolve-Path (Join-Path $scriptRoot "..") -ErrorAction SilentlyContinue
if ($repoCandidate -and (Test-Path (Join-Path $repoCandidate "pyproject.toml"))) {
  $repoPath = $repoCandidate.Path
}
$repoExists = (Test-Path (Join-Path $repoPath "pyproject.toml")) -or (Test-Path (Join-Path $repoPath ".git"))

$configPath = Join-Path $localRootCandidate "config\r3e-collector.env"
$backupPath = Join-Path $localRootCandidate "backups"

$blockers = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]
$status = "READY_FOR_REVIEW"

if ($pythonCommand -eq "missing") { $blockers.Add("python_missing") | Out-Null; $status = "BLOCKED" }
if ($gitVersion -eq "missing") { $warnings.Add("git_missing") | Out-Null; if ($status -eq "READY_FOR_REVIEW") { $status = "DEGRADED" } }
if ($outboundHttps -ne "true") { $warnings.Add("outbound_https_unconfirmed") | Out-Null; if ($status -eq "READY_FOR_REVIEW") { $status = "DEGRADED" } }
if (-not $localRootExists) { $warnings.Add("local_root_not_created_yet") | Out-Null }
if ($homeDir -match 'Temp') { $blockers.Add("home_looks_temporary") | Out-Null; $status = "BLOCKED" }

$blockerStr = if ($blockers.Count -gt 0) { ($blockers -join ",") } else { "none" }
$warningStr = if ($warnings.Count -gt 0) { ($warnings -join ",") } else { "none" }

$content = @"
# R3E Local Host Discovery Result

``````text
DISCOVERY_EXECUTED_AT_UTC = $UtcNow
OPERATING_SYSTEM = $osName
OPERATING_SYSTEM_VERSION = $osVer
HOSTNAME = $hostName
CURRENT_USERNAME = $userName
HOME_DIRECTORY = $homeDir
SHELL = $shellName
POWERSHELL_VERSION = $psVersion
PYTHON_COMMAND = $pythonCommand
PYTHON_VERSION = $pythonVersion
GIT_VERSION = $gitVersion
CPU = $cpu
MEMORY_TOTAL = $memoryTotal
DISK_TOTAL = $diskTotal
DISK_AVAILABLE = $diskAvailable
FILESYSTEM_TYPE = $fsType
TIMEZONE = $timezone
NETWORK_AVAILABLE = $networkAvailable
OUTBOUND_HTTPS_AVAILABLE = $outboundHttps
SCHEDULER_MECHANISM = $schedulerMechanism
TASK_SCHEDULER_AVAILABLE = $taskSchedulerAvailable
SYSTEMD_AVAILABLE = $systemdAvailable
CRON_AVAILABLE = $cronAvailable
LOCAL_ROOT_CANDIDATE = $localRootCandidate
LOCAL_ROOT_EXISTS = $localRootExists
LOCAL_ROOT_WRITABLE = $localRootWritable
REPOSITORY_PATH = $repoPath
REPOSITORY_PATH_EXISTS = $repoExists
CONFIG_PATH_CANDIDATE = $configPath
BACKUP_PATH_CANDIDATE = $backupPath
HOST_DISCOVERY_STATUS = $status
RECOMMENDED_LOCAL_ROOT = $localRootCandidate
RECOMMENDED_SCHEDULER_MECHANISM = $schedulerMechanism
BLOCKERS = $blockerStr
WARNINGS = $warningStr
NEXT_ACTION = submit this file for readiness review
``````

Notes:

- read-only discovery
- no secrets, public IP, tokens, or env contents collected
"@

# Fix accidental over-escaping of fences in here-string
$content = $content -replace '``````', '```'

Set-Content -Path $Out -Value $content -Encoding UTF8
Write-Host "WROTE $Out"
Write-Host "HOST_DISCOVERY_STATUS=$status"
exit 0
