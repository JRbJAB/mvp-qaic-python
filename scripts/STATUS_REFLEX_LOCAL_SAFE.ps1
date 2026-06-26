# STATUS_REFLEX_LOCAL_SAFE.ps1
# Show local Reflex port/process status and latest logs.
[CmdletBinding()]
param(
    [int]$FrontendPort = 3000,
    [int]$BackendPort = 8000,
    [int]$Tail = 80
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
        $pid = [int]$Matches[1]
        $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
        if ($proc) {
            Write-Host "PORT_$Port=LISTENING PID=$pid PROCESS=$($proc.ProcessName) PATH=$($proc.Path)"
        } else {
            Write-Host "PORT_$Port=LISTENING PID=$pid PROCESS=UNKNOWN"
        }
    }
}

Show-Port -Port $FrontendPort
Show-Port -Port $BackendPort

$LogDir = Join-Path $env:LOCALAPPDATA "MVP_QAIC_REFLEX_LOGS"
Write-Host "===== LATEST LOG ====="
if (Test-Path -LiteralPath $LogDir) {
    $latest = Get-ChildItem -LiteralPath $LogDir -Filter "reflex_local_*.log" -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latest) {
        Write-Host "LOG_FILE=$($latest.FullName)"
        Get-Content -LiteralPath $latest.FullName -Tail $Tail
    } else {
        Write-Host "NO_LOG_FOUND_IN=$LogDir"
    }
} else {
    Write-Host "LOG_DIR_NOT_FOUND=$LogDir"
}
