$ErrorActionPreference = "Stop"
Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue | ForEach-Object {
  if ($_.OwningProcess -and $_.OwningProcess -ne $PID) {
    Write-Host "STOP_8080_PID=$($_.OwningProcess)"
    Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
  }
}
Write-Host "MVP_QAIC_SERVER_8080_STOPPED"
