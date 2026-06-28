# START_REFLEX_LOCAL_SAFE.ps1
# MVP QAIC Reflex local runtime starter - Windows PowerShell 5.1 safe
# R5K: npm-first frontend repair; no PowerShell stop on npm warnings; rolldown native binding repair.
# Local/private only. No deploy, no broker, no Sheet/BQ write.
[CmdletBinding()]
param(
    [string]$RepoRoot = "",
    [string]$RuntimeRoot = "$env:LOCALAPPDATA\MVP_QAIC_REFLEX_RUNTIME\P_REFLEX_06C_20260625_200632",
    [int]$FrontendPort = 3000,
    [int]$BackendPort = 8000,
    [int]$MaxRestarts = 2,
    [switch]$NoKillPorts,
    [switch]$UseBun,
    [switch]$NoFrontendRepair,
    [switch]$CleanWeb
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
$env:PYTHONUTF8 = "1"
$env:BROWSER = "none"
$env:REFLEX_DIR = Join-Path $env:LOCALAPPDATA "MVP_QAIC_REFLEX_STATE"

# Default to npm. Bun has repeatedly failed on Windows with missing rolldown native bindings.
if ($UseBun) {
    Remove-Item Env:\REFLEX_USE_NPM -ErrorAction SilentlyContinue
} else {
    $env:REFLEX_USE_NPM = "true"
    $env:NPM_CONFIG_INCLUDE = "optional"
}

$LogDir = Join-Path $env:LOCALAPPDATA "MVP_QAIC_REFLEX_LOGS"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
New-Item -ItemType Directory -Force -Path $env:REFLEX_DIR | Out-Null
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = Join-Path $LogDir "reflex_local_$Stamp.log"

function Write-Step([string]$Text) {
    Write-Host "===== $Text ====="
    Add-Content -LiteralPath $LogFile -Encoding UTF8 -Value "===== $Text ====="
}

function Write-Log([string]$Text) {
    Write-Host $Text
    Add-Content -LiteralPath $LogFile -Encoding UTF8 -Value $Text
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
        Write-Log "PORT_$Port=FREE"
        return
    }
    foreach ($listenerPid in $pids) {
        $proc = Get-Process -Id $listenerPid -ErrorAction SilentlyContinue
        if (-not $proc) { continue }
        $name = $proc.ProcessName
        if ($name -match '^(python|pythonw|node|bun|reflex|granian)$') {
            Write-Log "STOP_PORT_$Port PID=$listenerPid PROCESS=$name"
            Stop-Process -Id $listenerPid -Force -ErrorAction SilentlyContinue
            Start-Sleep -Milliseconds 500
        } else {
            throw "Port $Port already used by PID=$listenerPid PROCESS=$name. Stop it manually or run with another port."
        }
    }
}

function Get-NodePlatformArch() {
    try {
        $v = (& node -p "process.platform + '-' + process.arch" 2>$null)
        if ($LASTEXITCODE -eq 0 -and $v) { return $v.Trim() }
    } catch {}
    return "unknown"
}

function Get-RolldownBindingPackage() {
    $arch = Get-NodePlatformArch
    if ($arch -eq "win32-arm64") { return "@rolldown/binding-win32-arm64-msvc" }
    if ($arch -eq "win32-x64") { return "@rolldown/binding-win32-x64-msvc" }
    return ""
}

function Get-RolldownVersion() {
    $pkg = Join-Path $RuntimeRoot ".web\node_modules\rolldown\package.json"
    if (Test-Path -LiteralPath $pkg) {
        try {
            $obj = Get-Content -LiteralPath $pkg -Raw -Encoding UTF8 | ConvertFrom-Json
            if ($obj.version) { return [string]$obj.version }
        } catch {}
    }
    return "1.0.3"
}

function Invoke-NpmInWeb([string[]]$Args) {
    $web = Join-Path $RuntimeRoot ".web"
    if (-not (Test-Path -LiteralPath $web)) { throw ".web not found: $web" }
    Push-Location -LiteralPath $web
    try {
        Write-Log ("NPM_CMD=npm " + ($Args -join " "))
        $old = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        & npm @Args 2>&1 | Tee-Object -FilePath $LogFile -Append
        $code = $LASTEXITCODE
        $ErrorActionPreference = $old
        Write-Log "NPM_EXIT_CODE=$code"
        return $code
    } finally {
        Pop-Location
    }
}

function Repair-FrontendNativeDeps() {
    Write-Step "FRONTEND NATIVE DEPS REPAIR"
    $web = Join-Path $RuntimeRoot ".web"
    $nodeModules = Join-Path $web "node_modules"
    $packageLock = Join-Path $web "package-lock.json"
    $npmShrink = Join-Path $web "npm-shrinkwrap.json"

    Write-Log "NODE_PLATFORM_ARCH=$(Get-NodePlatformArch)"
    Write-Log "PACKAGE_MANAGER_DEFAULT=$(if ($UseBun) { 'bun' } else { 'npm' })"

    if (-not (Test-Path -LiteralPath $web)) {
        Write-Log "WEB_DIR_NOT_FOUND_SKIP_REPAIR=$web"
        return
    }

    if ($CleanWeb -and (Test-Path -LiteralPath $nodeModules)) {
        Write-Log "REMOVE_NODE_MODULES=$nodeModules"
        Remove-Item -LiteralPath $nodeModules -Recurse -Force -ErrorAction SilentlyContinue
    }
    if (Test-Path -LiteralPath $packageLock) {
        Write-Log "REMOVE_PACKAGE_LOCK=$packageLock"
        Remove-Item -LiteralPath $packageLock -Force -ErrorAction SilentlyContinue
    }
    if (Test-Path -LiteralPath $npmShrink) {
        Write-Log "REMOVE_NPM_SHRINKWRAP=$npmShrink"
        Remove-Item -LiteralPath $npmShrink -Force -ErrorAction SilentlyContinue
    }

    if ($UseBun) {
        Write-Log "REPAIR_SKIPPED_FOR_BUN_MODE=True"
        return
    }

    $code = Invoke-NpmInWeb -Args @("install", "--legacy-peer-deps", "--include=optional", "--no-audit", "--prefer-online")
    if ($code -ne 0) { Write-Log "WARN_NPM_INSTALL_FAILED=$code" }

    $binding = Get-RolldownBindingPackage
    if ($binding) {
        $version = Get-RolldownVersion
        $pkgSpec = "$binding@$version"
        Write-Log "ROLldown_BINDING_TARGET=$pkgSpec"
        $code2 = Invoke-NpmInWeb -Args @("install", "--legacy-peer-deps", "--include=optional", "--no-audit", "--prefer-online", $pkgSpec)
        if ($code2 -ne 0) { Write-Log "WARN_ROLLDOWN_BINDING_INSTALL_FAILED=$code2" }

        $bindingDir = Join-Path $web ("node_modules\" + $binding.Replace("/", "\"))
        if (Test-Path -LiteralPath $bindingDir) {
            Write-Log "ROLLDOWN_BINDING_PRESENT=True PATH=$bindingDir"
        } else {
            Write-Log "ROLLDOWN_BINDING_PRESENT=False PATH=$bindingDir"
        }
    } else {
        Write-Log "ROLLDOWN_BINDING_TARGET=UNKNOWN_ARCH"
    }
}

function Test-LastLogLooksLikeRolldownBindingFailure() {
    if (-not (Test-Path -LiteralPath $LogFile)) { return $false }
    $tail = Get-Content -LiteralPath $LogFile -Tail 220 -ErrorAction SilentlyContinue
    $txt = ($tail -join "`n")
    return ($txt -match "Cannot find native binding" -or $txt -match "@rolldown/binding-win32" -or $txt -match "rolldown-binding\.win32")
}

Write-Step "MVP QAIC REFLEX LOCAL START R5J"
Write-Log "NO_PUBLIC_DEPLOY=$env:NO_PUBLIC_DEPLOY"
Write-Log "NO_LIVE_ACTION=$env:NO_LIVE_ACTION"
Write-Log "REFLEX_DIR=$env:REFLEX_DIR"
Write-Log "REFLEX_USE_NPM=$env:REFLEX_USE_NPM"
Write-Log "LOG_FILE=$LogFile"

if (-not (Test-Path -LiteralPath $RuntimeRoot)) {
    throw "RuntimeRoot not found: $RuntimeRoot"
}
if (-not (Test-Path -LiteralPath (Join-Path $RuntimeRoot "rxconfig.py"))) {
    throw "rxconfig.py not found in runtime: $RuntimeRoot"
}

Set-Location -LiteralPath $RuntimeRoot
Write-Log "RUNTIME_ROOT=$RuntimeRoot"

function Invoke-VersionCheck([string]$Label, [scriptblock]$Command) {
    Write-Log "CHECK=$Label"
    $old = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        & $Command 2>&1 | ForEach-Object {
            $line = [string]$_
            Write-Log $line
        }
        Write-Log "CHECK_EXIT_$Label=$LASTEXITCODE"
    } catch {
        Write-Log "CHECK_WARN_$Label=$($_.Exception.Message)"
    } finally {
        $ErrorActionPreference = $old
    }
}

Write-Step "PYTHON NODE REFLEX CHECK"
Invoke-VersionCheck -Label "PYTHON_VERSION" -Command { python --version }
Invoke-VersionCheck -Label "REFLEX_VERSION" -Command { python -c "import importlib.metadata as m; print('REFLEX_VERSION=' + m.version('reflex'))" }
Invoke-VersionCheck -Label "NODE_VERSION" -Command { node --version }
Invoke-VersionCheck -Label "NPM_VERSION" -Command { npm --version }
Write-Log "NODE_PLATFORM_ARCH=$(Get-NodePlatformArch)"

if (-not $NoKillPorts) {
    Write-Step "PORT CLEANUP SAFE"
    Stop-PortIfSafe -Port $FrontendPort
    Stop-PortIfSafe -Port $BackendPort
} else {
    Write-Step "PORT CLEANUP SKIPPED"
}

if ($CleanWeb -and -not $NoFrontendRepair) {
    Repair-FrontendNativeDeps
}

Write-Step "START REFLEX FOREGROUND"
Write-Log "OPEN_URL=http://localhost:$FrontendPort/"
Write-Log "CDC_DEV_TRACKER_URL=http://localhost:$FrontendPort/cdc-dev-tracker"
Write-Log "BACKEND=http://127.0.0.1:$BackendPort"
Write-Log "KEEP THIS POWERSHELL WINDOW OPEN. CTRL+C stops the server."

$attempt = 0
$repaired = $false
while ($attempt -le $MaxRestarts) {
    $attempt++
    Write-Step "REFLEX_ATTEMPT_$attempt"
    $started = Get-Date

    $oldErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & python -u -m reflex run --frontend-port $FrontendPort --backend-port $BackendPort --backend-host 127.0.0.1 --loglevel debug 2>&1 | Tee-Object -FilePath $LogFile -Append
    $exit = $LASTEXITCODE
    $ErrorActionPreference = $oldErrorActionPreference

    $seconds = [int](((Get-Date) - $started).TotalSeconds)
    Write-Log "REFLEX_EXIT_CODE=$exit"
    Write-Log "REFLEX_UPTIME_SEC=$seconds"

    if ($exit -eq 0) { break }

    if ((-not $NoFrontendRepair) -and (-not $UseBun) -and (-not $repaired) -and (Test-LastLogLooksLikeRolldownBindingFailure)) {
        Write-Log "DETECTED_ROLLDOWN_NATIVE_BINDING_FAILURE=True"
        $repaired = $true
        Repair-FrontendNativeDeps
        Write-Log "REFLEX_RESTART_AFTER_REPAIR=True"
        Start-Sleep -Seconds 2
        continue
    }

    if ($attempt -gt $MaxRestarts) { break }
    Write-Log "REFLEX_RESTART_IN_3_SEC attempt=$attempt max=$MaxRestarts"
    Start-Sleep -Seconds 3
}

Write-Step "REFLEX STOPPED"
Write-Log "LOG_FILE=$LogFile"
Write-Log "If this was unexpected, run STATUS_REFLEX_LOCAL_SAFE.ps1 and copy the last error block."
