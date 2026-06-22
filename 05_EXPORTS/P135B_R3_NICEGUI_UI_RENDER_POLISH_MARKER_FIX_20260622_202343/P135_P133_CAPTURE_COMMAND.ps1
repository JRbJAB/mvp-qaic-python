$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$responseText = "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P135B_R3_NICEGUI_UI_RENDER_POLISH_MARKER_FIX_20260622_202343\P135_GEM_RESPONSE_INPUT.md"
$outputDir = "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY\05_EXPORTS\P135B_R3_NICEGUI_UI_RENDER_POLISH_MARKER_FIX_20260622_202343\P133_FROM_P135_OPERATOR_POLISH"
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

python -m mvp_qaic_py.gem_multimodal_response_capture_gate `
  --response-text $responseText `
  --output-dir $outputDir `
  --run-id "P135B-R3-NICEGUI-UI-RENDER-POLISH-MARKER-FIX-20260622-P133-GATE" `
  --generated-at-utc "2026-06-22T00:00:00Z"

Write-Host "P133_OUTPUT_DIR=$outputDir"
Write-Host "OPEN_FIRST=$(Join-Path $outputDir 'P133_GEM_RESPONSE_HUMAN_REVIEW.md')"
Write-Host "OPEN_JSON=$(Join-Path $outputDir 'P133_GEM_RESPONSE_PRETTY.json')"
