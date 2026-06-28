# STATUS_REFLEX_LOCAL_SAFE.ps1
# Show local Reflex port/process status, latest logs and known frontend dependency failures.
# R5J: detects rolldown native binding failures.
[CmdletBinding()]
param(
    [int]$FrontendPort = 3000,
    [int]$BackendPort = 8000,
    [int]$Tail = 120
)

$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

function Show-Port([int]$Port) {
    Write-Host "===== PORT $Port ====="
    $rows = netstat -ano -p tcp 2>$null | Where-Object { $_ -match "^\s*TCP\s+\S+:$Port\s+\S+\s+LISTENING\s+(\d+)\s*$" }
    if (-not $rows) {
        Write-Host "PORT_$Port=NOT_LISTENING"
        return
    }
    foreach ($line in $rows) {
        $null = $line -match "LISTENING\s+(\d+)\s*$"
        $listenerPid = [int]$Matches[1]
        $proc = Get-Process -Id $listenerPid -ErrorAction SilentlyContinue
        if ($proc) {
            $path = ""
            try { $path = $proc.Path } catch {}
            Write-Host "PORT_$Port=LISTENING PID=$listenerPid PROCESS=$($proc.ProcessName) PATH=$path"
        } else {
            Write-Host "PORT_$Port=LISTENING PID=$listenerPid PROCESS=UNKNOWN"
        }
    }
}

function Show-LatestLog([string]$LogDir) {
    Write-Host "===== LATEST REFLEX LOG ====="
    if (Test-Path -LiteralPath $LogDir) {
        $latest = Get-ChildItem -LiteralPath $LogDir -Filter "reflex_local_*.log" -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($latest) {
            Write-Host "LOG_FILE=$($latest.FullName)"
            $tailLines = Get-Content -LiteralPath $latest.FullName -Tail $Tail
            $tailLines
            $txt = ($tailLines -join "`n")
            Write-Host "===== DIAG ====="
            if ($txt -match "Cannot find native binding" -or $txt -match "@rolldown/binding-win32" -or $txt -match "rolldown-binding\.win32") {
                Write-Host "DIAG=ROLLDOWN_NATIVE_BINDING_MISSING"
                Write-Host "ACTION=Run START_REFLEX_LOCAL_SAFE.ps1 without -UseBun, preferably with -CleanWeb once."
            } elseif ($txt -match "App Running" -or $txt -match "Listening at: http://127.0.0.1") {
                Write-Host "DIAG=BACKEND_OR_APP_STARTED"
            } else {
                Write-Host "DIAG=CHECK_LOG_MANUALLY"
            }
        } else {
            Write-Host "NO_LOG_FOUND_IN=$LogDir"
        }
    } else {
        Write-Host "LOG_DIR_NOT_FOUND=$LogDir"
    }
}

Show-Port -Port $FrontendPort
Show-Port -Port $BackendPort

$LogDir = Join-Path $env:LOCALAPPDATA "MVP_QAIC_REFLEX_LOGS"
Show-LatestLog -LogDir $LogDir

Write-Host "===== TOOLCHAIN ====="
try { python --version } catch {}
try { python -c "import importlib.metadata as m; print('REFLEX_VERSION=' + m.version('reflex'))" } catch {}
try { node --version } catch {}
try { npm --version } catch {}
try { node -p "'NODE_PLATFORM_ARCH=' + process.platform + '-' + process.arch" } catch {}
