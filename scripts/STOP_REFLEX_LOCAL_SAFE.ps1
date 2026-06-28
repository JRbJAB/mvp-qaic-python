# STOP_REFLEX_LOCAL_SAFE.ps1
# Stop only safe local Reflex-related processes listening on ports 3000/8000 by default.
# R5J: also cleans known local Reflex child processes if explicitly requested.
[CmdletBinding()]
param(
    [int]$FrontendPort = 3000,
    [int]$BackendPort = 8000,
    [switch]$KillKnownChildren
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

function Stop-PidIfSafe([int]$PidToStop, [string]$Reason) {
    $proc = Get-Process -Id $PidToStop -ErrorAction SilentlyContinue
    if (-not $proc) { return }
    $name = $proc.ProcessName
    if ($name -match '^(python|pythonw|node|bun|reflex|granian)$') {
        Write-Host "STOP PID=$PidToStop PROCESS=$name REASON=$Reason"
        Stop-Process -Id $PidToStop -Force -ErrorAction SilentlyContinue
    } else {
        Write-Host "SKIP PID=$PidToStop PROCESS=$name REASON=$Reason NOT_SAFE_TO_KILL"
    }
}

function Stop-PortIfSafe([int]$Port) {
    $pids = @(Get-ListenerPids -Port $Port)
    if ($pids.Count -eq 0) {
        Write-Host "PORT_$Port=FREE"
        return
    }
    foreach ($listenerPid in $pids) {
        Stop-PidIfSafe -PidToStop $listenerPid -Reason "PORT_$Port"
    }
}

Stop-PortIfSafe -Port $FrontendPort
Stop-PortIfSafe -Port $BackendPort

if ($KillKnownChildren) {
    Write-Host "===== KILL_KNOWN_CHILDREN ====="
    Get-Process -ErrorAction SilentlyContinue |
        Where-Object { $_.ProcessName -match '^(python|pythonw|node|bun|granian)$' } |
        ForEach-Object {
            $path = ""
            try { $path = $_.Path } catch {}
            if ($path -match 'MVP_QAIC_REFLEX_RUNTIME|MVP_QAIC_REFLEX_STATE|AppData\\Local\\reflex') {
                Stop-PidIfSafe -PidToStop $_.Id -Reason "KNOWN_MVP_QAIC_REFLEX_PATH"
            }
        }
}

Write-Host "STOP_DONE"
