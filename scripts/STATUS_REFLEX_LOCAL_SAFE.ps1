# STATUS_REFLEX_LOCAL_SAFE.ps1
# MVP QAIC Reflex local runtime status R5L - Windows PowerShell 5.1 safe
[CmdletBinding()]
param(
    [int]$FrontendPort = 3000,
    [int]$BackendPort = 8000,
    [int]$Tail = 120
)

$ErrorActionPreference = "Continue"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

$LogDir = Join-Path $env:LOCALAPPDATA "MVP_QAIC_REFLEX_LOGS"
Write-Host "===== MVP QAIC REFLEX LOCAL STATUS R5L ====="

function Test-PortOpen {
  param([int]$Port)
  try {
    $client = New-Object Net.Sockets.TcpClient
    $iar = $client.BeginConnect("127.0.0.1", $Port, $null, $null)
    $ok = $iar.AsyncWaitHandle.WaitOne(800, $false)
    if ($ok) { $client.EndConnect($iar) }
    $client.Close()
    return [bool]$ok
  } catch { return $false }
}

$front = Test-PortOpen -Port $FrontendPort
$back = Test-PortOpen -Port $BackendPort
Write-Host "FRONTEND_$FrontendPort=$front"
Write-Host "BACKEND_$BackendPort=$back"
Write-Host "URL=http://127.0.0.1:$FrontendPort/cdc-dev-tracker"

Write-Host "===== PORT OWNERS ====="
Get-NetTCPConnection -LocalPort $FrontendPort,$BackendPort -ErrorAction SilentlyContinue |
  Select-Object LocalAddress,LocalPort,State,OwningProcess |
  Format-Table -AutoSize

Write-Host "===== LATEST LOG ====="
$latest = $null
if (Test-Path -LiteralPath $LogDir) {
  $latest = Get-ChildItem -LiteralPath $LogDir -Filter "reflex_local_*.log" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
}
if (-not $latest) {
  Write-Host "NO_LOG_FOUND=$LogDir"
  exit 0
}

Write-Host "LOG_FILE=$($latest.FullName)"
$content = Get-Content -LiteralPath $latest.FullName -Tail $Tail
$content

$s = ($content -join "`n")
if ($s -match "react-router.*n.?est pas reconnu") {
  Write-Host "DETECTED=FRONTEND_REACT_ROUTER_BIN_MISSING"
  Write-Host "ACTION=Run START_REFLEX_LOCAL_SAFE.ps1 -CleanWeb -MaxRestarts 2"
}
if ($s -match "Cannot find native binding" -or $s -match "@rolldown/binding-win32") {
  Write-Host "DETECTED=FRONTEND_ROLLDOWN_NATIVE_BINDING_MISSING"
  Write-Host "ACTION=Run START_REFLEX_LOCAL_SAFE.ps1 -CleanWeb -MaxRestarts 2"
}
