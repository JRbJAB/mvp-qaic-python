# STOP_REFLEX_LOCAL_SAFE.ps1
# Stop only safe local Reflex-related processes listening on ports 3000/8000 by default.
[CmdletBinding()]
param(
    [int]$FrontendPort = 3000,
    [int]$BackendPort = 8000
)

$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

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
    foreach ($listenerPid in $pids) {
        $proc = Get-Process -Id $listenerPid -ErrorAction SilentlyContinue
        if (-not $proc) { continue }
        $name = $proc.ProcessName
        if ($name -match '^(python|pythonw|node|bun|reflex)$') {
            Write-Host "STOP PID=$listenerPid PROCESS=$name PORT=$Port"
            Stop-Process -Id $listenerPid -Force -ErrorAction SilentlyContinue
        } else {
            Write-Host "SKIP PID=$listenerPid PROCESS=$name PORT=$Port NOT_SAFE_TO_KILL"
        }
    }
}

Stop-PortIfSafe -Port $FrontendPort
Stop-PortIfSafe -Port $BackendPort
Write-Host "STOP_DONE"
