# MVP_QAIC_R6H_PID_VARIABLE_FIX
# Lower/mixed-case $pid local variables are renamed to $listenerPid.
# The automatic readonly $PID variable remains preserved when explicitly uppercase.
# START_REFLEX_LOCAL_SAFE.ps1
# MVP QAIC Reflex local runtime starter R5L - Windows PowerShell 5.1 safe
# Local/private only. No deploy, no broker, no Sheet/BQ write.
[CmdletBinding()]
param(
    [string]$RepoRoot = "",
    [string]$RuntimeRoot = "$env:LOCALAPPDATA\MVP_QAIC_REFLEX_RUNTIME\P_REFLEX_06C_20260625_200632",
    [int]$FrontendPort = 3000,
    [int]$BackendPort = 8000,
    [int]$MaxRestarts = 2,
    [switch]$NoKillPorts,
    [switch]$CleanWeb,
    [switch]$NoFrontendPreinstall
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
$env:BROWSER = "none"
$env:PYTHONUTF8 = "1"
$env:GIT_TERMINAL_PROMPT = "0"
$env:REFLEX_USE_NPM = "true"
$env:NPM_CONFIG_INCLUDE = "optional"
$env:NPM_CONFIG_AUDIT = "false"
$env:NPM_CONFIG_FUND = "false"
Remove-Item Env:\NPM_CONFIG_OPTIONAL -ErrorAction SilentlyContinue
Remove-Item Env:\PYTHONNOUSERSITE -ErrorAction SilentlyContinue

$env:REFLEX_DIR = Join-Path $env:LOCALAPPDATA "MVP_QAIC_REFLEX_STATE"

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

function Invoke-NativeSafe {
    param(
        [Parameter(Mandatory=$true)][string]$File,
        [Parameter(ValueFromRemainingArguments=$true)][string[]]$Args
    )
    $old = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        & $File @Args 2>&1 | Tee-Object -FilePath $LogFile -Append
        return $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $old
    }
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
        if ($name -match '^(python|pythonw|node|bun|reflex)$') {
            Write-Log "STOP_PORT_$Port PID=$listenerPid PROCESS=$name"
            Stop-Process -Id $listenerPid -Force -ErrorAction SilentlyContinue
            Start-Sleep -Milliseconds 500
        } else {
            throw "Port $Port already used by PID=$listenerPid PROCESS=$name. Stop it manually or run with another port."
        }
    }
}

function Get-NodeArch {
    try {
        $arch = & "C:\Program Files\nodejs\node.exe" -p "process.arch" 2>$null
        if ($arch) { return [string]($arch | Select-Object -First 1).Trim() }
    } catch {}
    return "unknown"
}

function Repair-FrontendDeps {
    param([switch]$ForceClean)

    $web = Join-Path $RuntimeRoot ".web"
    $pkg = Join-Path $web "package.json"
    $npm = "C:\Program Files\nodejs\npm.CMD"

    if (-not (Test-Path -LiteralPath $pkg)) {
        Write-Log "FRONTEND_REPAIR_SKIPPED=.web/package.json missing; Reflex will initialize it first"
        return
    }

    Write-Step "FRONTEND DEPS REPAIR R5L"

    if ($ForceClean) {
        $nodeModules = Join-Path $web "node_modules"
        $packageLock = Join-Path $web "package-lock.json"
        $viteCache = Join-Path $web ".vite"
        if (Test-Path -LiteralPath $nodeModules) {
            Write-Log "REMOVE=.web/node_modules"
            Remove-Item -LiteralPath $nodeModules -Recurse -Force -ErrorAction SilentlyContinue
        }
        if (Test-Path -LiteralPath $packageLock) {
            Write-Log "REMOVE=.web/package-lock.json"
            Remove-Item -LiteralPath $packageLock -Force -ErrorAction SilentlyContinue
        }
        if (Test-Path -LiteralPath $viteCache) {
            Write-Log "REMOVE=.web/.vite"
            Remove-Item -LiteralPath $viteCache -Recurse -Force -ErrorAction SilentlyContinue
        }
    }

    Push-Location -LiteralPath $web
    try {
        Write-Log "NPM_INSTALL_BASE=true"
        $code = Invoke-NativeSafe -File $npm -Args @("install","--legacy-peer-deps","--include=optional","--no-audit","--fund=false")
        Write-Log "NPM_INSTALL_BASE_EXIT=$code"

        $reactRouterCmd = Join-Path $web "node_modules\.bin\react-router.cmd"
        if (-not (Test-Path -LiteralPath $reactRouterCmd)) {
            Write-Log "REACT_ROUTER_BIN_MISSING=True"
            $devPkgs = @(
                "@react-router/dev@7.15.0",
                "@react-router/fs-routes@7.15.0",
                "vite@8.0.16",
                "autoprefixer@10.5.0",
                "postcss@8.5.14",
                "postcss-import@16.1.1",
                "@emotion/react@11.14.0"
            )
            $args = @("install","--legacy-peer-deps","--include=optional","--no-audit","--fund=false","--save-dev") + $devPkgs
            $code = Invoke-NativeSafe -File $npm -Args $args
            Write-Log "NPM_INSTALL_DEV_EXIT=$code"
        }

        $basePkgs = @(
            "react-router-dom@7.15.0",
            "react-router@7.15.0",
            "react@19.2.6",
            "react-dom@19.2.6",
            "@react-router/node@7.15.0",
            "@radix-ui/themes@3.3.0",
            "lucide-react@1.14.0",
            "react-error-boundary@6.1.1",
            "universal-cookie@7.2.2",
            "isbot@5.1.40",
            "sonner@2.0.7",
            "react-helmet@6.1.0",
            "socket.io-client@4.8.3"
        )
        $args = @("install","--legacy-peer-deps","--include=optional","--no-audit","--fund=false") + $basePkgs
        $code = Invoke-NativeSafe -File $npm -Args $args
        Write-Log "NPM_INSTALL_RUNTIME_EXIT=$code"

        $arch = Get-NodeArch
        Write-Log "NODE_ARCH=$arch"
        if ($arch -eq "arm64" -or $arch -eq "x64") {
            $bindingPkg = "@rolldown/binding-win32-$arch-msvc@1.0.3"
            Write-Log "ENSURE_ROLLDOWN_BINDING=$bindingPkg"
            $code = Invoke-NativeSafe -File $npm -Args @("install","--legacy-peer-deps","--include=optional","--no-audit","--fund=false",$bindingPkg)
            Write-Log "NPM_INSTALL_ROLLDOWN_BINDING_EXIT=$code"
        }

        if (Test-Path -LiteralPath $reactRouterCmd) {
            Write-Log "REACT_ROUTER_BIN_OK=True"
        } else {
            Write-Log "REACT_ROUTER_BIN_OK=False"
        }
    } finally {
        Pop-Location
    }
}

function Has-FrontendMissingDepsError {
    if (-not (Test-Path -LiteralPath $LogFile)) { return $false }
    $tail = Get-Content -LiteralPath $LogFile -Tail 240 -ErrorAction SilentlyContinue
    $s = ($tail -join "`n")
    return ($s -match "react-router.*n.?est pas reconnu" -or $s -match "Cannot find native binding" -or $s -match "@rolldown/binding-win32")
}

Write-Step "MVP QAIC REFLEX LOCAL START R5L"
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

Write-Step "PYTHON NODE REFLEX CHECK"
Invoke-NativeSafe -File "C:\Python314\python.exe" -Args @("--version") | Out-Null
Invoke-NativeSafe -File "C:\Python314\python.exe" -Args @("-c","import importlib.metadata as m; print('REFLEX_VERSION=' + m.version('reflex'))") | Out-Null
Invoke-NativeSafe -File "C:\Program Files\nodejs\node.exe" -Args @("--version") | Out-Null
Invoke-NativeSafe -File "C:\Program Files\nodejs\npm.CMD" -Args @("--version","--loglevel","error") | Out-Null

if (-not $NoKillPorts) {
    Write-Step "PORT CLEANUP SAFE"
    Stop-PortIfSafe -Port $FrontendPort
    Stop-PortIfSafe -Port $BackendPort
} else {
    Write-Step "PORT CLEANUP SKIPPED"
}

if ($CleanWeb -and -not $NoFrontendPreinstall) {
    Repair-FrontendDeps -ForceClean
} elseif (-not $NoFrontendPreinstall) {
    Repair-FrontendDeps
}

Write-Step "START REFLEX FOREGROUND"
Write-Log "OPEN_URL=http://localhost:$FrontendPort/"
Write-Log "CDC_DEV_TRACKER_URL=http://localhost:$FrontendPort/cdc-dev-tracker"
Write-Log "BACKEND=http://127.0.0.1:$BackendPort"
Write-Log "KEEP THIS POWERSHELL WINDOW OPEN. CTRL+C stops the server."

$attempt = 0
while ($attempt -le $MaxRestarts) {
    $attempt++
    Write-Step "REFLEX_ATTEMPT_$attempt"
    $started = Get-Date

    $old = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        & "C:\Python314\python.exe" -u -m reflex run --frontend-port $FrontendPort --backend-port $BackendPort --backend-host 127.0.0.1 --loglevel debug 2>&1 | Tee-Object -FilePath $LogFile -Append
        $exit = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $old
    }

    $seconds = [int](((Get-Date) - $started).TotalSeconds)
    Write-Log "REFLEX_EXIT_CODE=$exit"
    Write-Log "REFLEX_UPTIME_SEC=$seconds"

    if ($exit -eq 0) { break }

    if (Has-FrontendMissingDepsError) {
        Write-Step "DETECTED_FRONTEND_DEPS_ERROR_REPAIR_AND_RETRY"
        Repair-FrontendDeps -ForceClean
    }

    if ($attempt -gt $MaxRestarts) { break }
    Write-Log "REFLEX_RESTART_IN_3_SEC attempt=$attempt max=$MaxRestarts"
    Start-Sleep -Seconds 3
}

Write-Step "REFLEX STOPPED"
Write-Log "LOG_FILE=$LogFile"
Write-Log "If this was unexpected, run STATUS_REFLEX_LOCAL_SAFE.ps1 or copy the last error block from the log."
