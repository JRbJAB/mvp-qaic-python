# START_REFLEX_LOCAL_SAFE.ps1
# MVP QAIC Reflex local runtime starter - Windows PowerShell 5.1 safe
# Local/private only. No deploy, no broker, no Sheet/BQ write.
[CmdletBinding()]
param(
    [string]$RepoRoot = "",
    [string]$RuntimeRoot = "$env:LOCALAPPDATA\MVP_QAIC_REFLEX_RUNTIME\P_REFLEX_06C_20260625_200632",
    [int]$FrontendPort = 3000,
    [int]$BackendPort = 8000,
    [int]$MaxRestarts = 3,
    [switch]$NoKillPorts
)

$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

$env:NO_PUBLIC_DEPLOY = "true"
$env:NO_LIVE_ACTION = "true"
$env:NO_BROKER_ORDER_SIZING = "true"
$env:NO_SHEET_WRITE = "true"
$env:NO_BIGQUERY_WRITE = "true"
$env:HUMAN_REVIEW_ONLY = "true"
$env:REFLEX_DIR = Join-Path $env:LOCALAPPDATA "MVP_QAIC_REFLEX_STATE"

# P_REFLEX_12H1D_R2_BEGIN_RUNTIME_SYNC
if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
    $RepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
}
$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
$env:QAIC_REPO_ROOT = $RepoRoot
if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot "mvp_qaic_reflex_ui"))) {
    throw "RepoRoot missing mvp_qaic_reflex_ui: $RepoRoot"
}
# P_REFLEX_12H1D_R2_END_RUNTIME_SYNC

$LogDir = Join-Path $env:LOCALAPPDATA "MVP_QAIC_REFLEX_LOGS"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
New-Item -ItemType Directory -Force -Path $env:REFLEX_DIR | Out-Null
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = Join-Path $LogDir "reflex_local_$Stamp.log"

function Write-Step([string]$Text) {
    Write-Host "===== $Text ====="
    Add-Content -LiteralPath $LogFile -Encoding UTF8 -Value "===== $Text ====="
}

function Get-ListenerPids([int]$Port) {
    $rows = netstat -ano -p tcp 2>$null
    $pids = @()
    foreach ($line in $rows) {
        if ($line -match "^\s*TCP\s+\S+:$Port\s+\S+\s+LISTENING\s+(\d+)\s*$") {
            $pids += [int]$Matches[1]
        }
    }
    $pids | Sort-Object -Unique
}

function Stop-PortIfSafe([int]$Port) {
    $pids = @(Get-ListenerPids -Port $Port)
    if ($pids.Count -eq 0) {
        Write-Host "PORT_$Port=FREE"
        return
    }
    foreach ($pid in $pids) {
        $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
        if (-not $proc) { continue }
        $name = $proc.ProcessName
        if ($name -match '^(python|pythonw|node|bun|reflex)$') {
            Write-Host "STOP_PORT_$Port PID=$pid PROCESS=$name"
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            Start-Sleep -Milliseconds 500
        } else {
            throw "Port $Port already used by PID=$pid PROCESS=$name. Stop it manually or run with another port."
        }
    }
}

Write-Step "MVP QAIC REFLEX LOCAL START"
Write-Host "NO_PUBLIC_DEPLOY=$env:NO_PUBLIC_DEPLOY"
Write-Host "NO_LIVE_ACTION=$env:NO_LIVE_ACTION"
Write-Host "REFLEX_DIR=$env:REFLEX_DIR"
Write-Host "LOG_FILE=$LogFile"

if (-not (Test-Path -LiteralPath $RuntimeRoot)) {
    throw "RuntimeRoot not found: $RuntimeRoot"
}
if (-not (Test-Path -LiteralPath (Join-Path $RuntimeRoot "rxconfig.py"))) {
    throw "rxconfig.py not found in runtime: $RuntimeRoot"
}


Write-Step "SYNC REPO SOURCE TO RUNTIME"
Write-Host "REPO_ROOT=$RepoRoot"
Write-Host "RUNTIME_ROOT=$RuntimeRoot"

$syncDirs = @("mvp_qaic_reflex_ui", "docs")
foreach ($dir in $syncDirs) {
    $src = Join-Path $RepoRoot $dir
    $dst = Join-Path $RuntimeRoot $dir
    if (-not (Test-Path -LiteralPath $src)) {
        throw "SYNC_SOURCE_MISSING=$src"
    }
    Remove-Item -LiteralPath $dst -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
    Write-Host "SYNCED_DIR=$dir"
}

$syncFiles = @("rxconfig.py", "pyproject.toml")
foreach ($file in $syncFiles) {
    $src = Join-Path $RepoRoot $file
    $dst = Join-Path $RuntimeRoot $file
    if (Test-Path -LiteralPath $src) {
        Copy-Item -LiteralPath $src -Destination $dst -Force
        Write-Host "SYNCED_FILE=$file"
    }
}

Set-Location -LiteralPath $RuntimeRoot
Write-Host "RUNTIME_ROOT=$RuntimeRoot"

Write-Step "PYTHON AND REFLEX CHECK"
python --version
python -c "import reflex; print('REFLEX_VERSION=' + getattr(reflex, '__version__', 'unknown'))"

if (-not $NoKillPorts) {
    Write-Step "PORT CLEANUP SAFE"
    Stop-PortIfSafe -Port $FrontendPort
    Stop-PortIfSafe -Port $BackendPort
} else {
    Write-Step "PORT CLEANUP SKIPPED"
}

Write-Step "START REFLEX FOREGROUND"
Write-Host "OPEN_URL=http://localhost:$FrontendPort/"
Write-Host "BACKEND=http://127.0.0.1:$BackendPort"
Write-Host "KEEP THIS POWERSHELL WINDOW OPEN. CTRL+C stops the server."

$attempt = 0
while ($attempt -le $MaxRestarts) {
    $attempt++
    Write-Step "REFLEX_ATTEMPT_$attempt"
    $started = Get-Date
    & python -u -m reflex run --frontend-port $FrontendPort --backend-port $BackendPort --backend-host 127.0.0.1 --loglevel debug 2>&1 | Tee-Object -FilePath $LogFile -Append
    $exit = $LASTEXITCODE
    $seconds = [int](((Get-Date) - $started).TotalSeconds)
    Write-Host "REFLEX_EXIT_CODE=$exit"
    Write-Host "REFLEX_UPTIME_SEC=$seconds"
    Add-Content -LiteralPath $LogFile -Encoding UTF8 -Value "REFLEX_EXIT_CODE=$exit"
    Add-Content -LiteralPath $LogFile -Encoding UTF8 -Value "REFLEX_UPTIME_SEC=$seconds"
    if ($exit -eq 0) { break }
    if ($attempt -gt $MaxRestarts) { break }
    Write-Host "REFLEX_RESTART_IN_3_SEC attempt=$attempt max=$MaxRestarts"
    Start-Sleep -Seconds 3
}

Write-Step "REFLEX STOPPED"
Write-Host "LOG_FILE=$LogFile"
Write-Host "If this was unexpected, copy the last error block from the log."
