$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# P163 local private operator shortcut.
# Safe by construction: no Sheet write/read, no public deploy, no Apps Script/CLASP,
# no broker, no order, no sizing.

$repo = $env:MVP_QAIC_PY_REPO
if (-not $repo) { $repo = "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY" }
if (-not (Test-Path -LiteralPath (Join-Path $repo "pyproject.toml"))) {
  throw "MVP_QAIC_PY repo introuvable. Set `$env:MVP_QAIC_PY_REPO puis relance."
}
Set-Location -LiteralPath $repo

Write-Host "============================================================"
Write-Host "MVP_QAIC_PY LOCAL PRIVATE OPERATOR SHORTCUT"
Write-Host "============================================================"
Write-Host "MODE=LOCAL_PRIVATE"
Write-Host "PROMPT_SOURCE_ID=P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"
Write-Host "NO_SHEETS_WRITE=true"
Write-Host "NO_PUBLIC_DEPLOY=true"
Write-Host "NO_APPS_SCRIPT=true"
Write-Host "NO_CLASP=true"
Write-Host "NO_BROKER_ORDER_SIZING=true"
Write-Host ""

$p162 = Get-ChildItem -LiteralPath ".\05_EXPORTS" -Directory |
  Where-Object { $_.Name -like "P162_LOCAL_PRIVATE_OPERATOR_HANDOFF_OR_DEV_STOP*" } |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1
if (-not $p162) { throw "P162 handoff introuvable." }

$handoff = Join-Path $p162.FullName "P162_OPERATOR_HANDOFF.md"
$decision = Join-Path $p162.FullName "P162_DEV_STOP_DECISION.md"
$promptFile = Join-Path (Get-Location).Path "mvp_qaic_py\multimodal_gem_image_prompt_usd_contract.py"

Write-Host "P162_HANDOFF=$handoff"
Write-Host "P162_DEV_STOP_DECISION=$decision"
Write-Host "PROMPT_SOURCE_FILE=$promptFile"
Write-Host ""
Write-Host "OPERATOR_ACTION=Use the sealed local private prompt workflow."
Write-Host "DEV_STATUS=STOP_RECOMMENDED_AFTER_THIS_SHORTCUT"
Write-Host "============================================================"
