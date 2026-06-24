$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "============================================================"
Write-Host "MVP QAIC - PRIVATE LOCAL COCKPIT"
Write-Host "URL: http://127.0.0.1:8088"
Write-Host "PRIVATE ONLY / NO PUBLIC SERVE / NO SHEET WRITE / NO BROKER"
Write-Host "============================================================"

Set-Location -LiteralPath "C:\Users\Julie\Documents\JRb-Dev\MVP_QAIC_PY_WORK_20260623_192901"

python -m mvp_qaic_py.p173_nicegui_private_local_runner --project-root . --host 127.0.0.1 --port 8088 --serve-private
