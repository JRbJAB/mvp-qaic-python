# STOP_REFLEX_LOCAL_SAFE.ps1
# MVP QAIC Reflex local runtime stop R5L - Windows PowerShell 5.1 safe
[CmdletBinding()]
param(
    [int[]]$Ports = @(3000,8000),
    [switch]$KillLocalRuntimeChildren
)

$ErrorActionPreference = "Continue"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

Write-Host "===== MVP QAIC REFLEX LOCAL STOP R5L ====="

foreach ($port in $Ports) {
  try {
    $owners = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue |
      Select-Object -ExpandProperty OwningProcess -Unique
    if (-not $owners) {
      Write-Host "PORT_$port=FREE"
      continue
    }
    foreach ($owner in $owners) {
      $p = Get-Process -Id $owner -ErrorAction SilentlyContinue
      if (-not $p) { continue }
      if ($p.ProcessName -match '^(python|pythonw|node|bun|reflex)$') {
        Stop-Process -Id $owner -Force -ErrorAction SilentlyContinue
        Write-Host "STOPPED_PORT_$port PID=$owner PROCESS=$($p.ProcessName)"
      } else {
        Write-Host "SKIPPED_PORT_$port PID=$owner PROCESS=$($p.ProcessName)"
      }
    }
  } catch {
    Write-Host "PORT_STOP_ERROR_$port=$($_.Exception.Message)"
  }
}

if ($KillLocalRuntimeChildren) {
  $runtime = Join-Path $env:LOCALAPPDATA "MVP_QAIC_REFLEX_RUNTIME"
  Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
    Where-Object {
      $_.CommandLine -and
      ($_.CommandLine -like "*MVP_QAIC_REFLEX_RUNTIME*" -or $_.CommandLine -like "*reflex run*")
    } |
    ForEach-Object {
      try {
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
        Write-Host "STOPPED_RUNTIME_CHILD PID=$($_.ProcessId)"
      } catch {}
    }
}

Write-Host "DONE"
