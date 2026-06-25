$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Set-Location -LiteralPath "Q:\MVP_QAIC_PY"

Write-Host "============================================================"
Write-Host "MANUAL PRIVATE REFLEX PREVIEW - RXCONFIG READY"
Write-Host "============================================================"
Write-Host "LOCAL_ONLY=TRUE"
Write-Host "HOST=127.0.0.1"
Write-Host "PORT=3000"
Write-Host "PUBLIC_DEPLOY=FALSE"
Write-Host "BROKER_ORDER_SIZING=FALSE"
Write-Host ""

python -m reflex run --env dev --backend-host 127.0.0.1 --frontend-port 3000
