$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
Set-Location -LiteralPath "C:\Users\Julie\AppData\Local\MVP_QAIC_REFLEX_RUNTIME\P_REFLEX_06C_20260625_200632"
Write-Host "P_REFLEX_12B_LOCAL_SERVER_START"
Write-Host "HOME=http://localhost:3000/"
Write-Host "ARCHITECTURE_WEB=http://localhost:3000/architecture-web"
Write-Host "SITEMAP=http://localhost:3000/sitemap"
Write-Host "SVG=http://localhost:3000/mvp_qaic_web_architecture_schema.svg"
if (Get-Command py -ErrorAction SilentlyContinue) {
  py -3 -m reflex run --env dev --backend-host 127.0.0.1 --frontend-port 3000 *>&1 | Tee-Object -FilePath "Q:\MVP_QAIC_PY\05_EXPORTS\P_REFLEX_12B_RUNTIME_VISUAL_SMOKE_ARCHITECTURE_WEB_20260626_012539\P_REFLEX_12B_LOCAL_SERVER.log"
} else {
  python -m reflex run --env dev --backend-host 127.0.0.1 --frontend-port 3000 *>&1 | Tee-Object -FilePath "Q:\MVP_QAIC_PY\05_EXPORTS\P_REFLEX_12B_RUNTIME_VISUAL_SMOKE_ARCHITECTURE_WEB_20260626_012539\P_REFLEX_12B_LOCAL_SERVER.log"
}
