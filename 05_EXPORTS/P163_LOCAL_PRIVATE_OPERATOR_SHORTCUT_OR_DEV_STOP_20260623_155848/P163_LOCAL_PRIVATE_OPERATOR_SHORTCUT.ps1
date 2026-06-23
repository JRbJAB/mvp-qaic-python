$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "============================================================"
Write-Host "MVP QAIC - LOCAL PRIVATE OPERATOR SHORTCUT"
Write-Host "============================================================"

$repo = $env:MVP_QAIC_PY_REPO

if (-not $repo) {
  try {
    $gitRoot = git rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -eq 0 -and $gitRoot) {
      $repo = $gitRoot.Trim()
    }
  } catch {
    $repo = $null
  }
}

if (-not $repo) {
  $repo = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\..\..")).Path
}

Set-Location -LiteralPath $repo

$p163Dir = $PSScriptRoot
$p162DirObj = Get-ChildItem -LiteralPath (Join-Path $repo "05_EXPORTS") -Directory |
  Where-Object { $_.Name -like "P162_LOCAL_PRIVATE_OPERATOR_HANDOFF_OR_DEV_STOP_*" } |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1

if (-not $p162DirObj) {
  throw "P162 operator handoff directory not found."
}

$p162Dir = $p162DirObj.FullName

Write-Host "REPO=$repo"
Write-Host "MODE=LOCAL_PRIVATE"
Write-Host "PROMPT_SOURCE_ID=P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"
Write-Host "LOCAL_PRIVATE_RELEASE_SEALED=True"
Write-Host "OPERATOR_SHORTCUT_READY=True"
Write-Host "OPERATOR_HANDOFF_READY=True"
Write-Host "DEV_STOP_RECOMMENDED=True"
Write-Host "FINAL_CLOSE_READY=True"
Write-Host "PUBLIC_DEPLOY_READY=False"
Write-Host "NO_GOOGLE_SHEETS_WRITE=True"
Write-Host "NO_APPS_SCRIPT_EXECUTION=True"
Write-Host "NO_CLASP_PUSH=True"
Write-Host "NO_BROKER=True"
Write-Host "NO_ORDER=True"
Write-Host "NO_SIZING=True"

$files = @(
  (Join-Path $p163Dir "P163_OPERATOR_SHORTCUT.md"),
  (Join-Path $p163Dir "P163_FINAL_CLOSE_DECISION.md"),
  (Join-Path $p163Dir "P163_SUMMARY.json"),
  (Join-Path $p162Dir "P162_OPERATOR_HANDOFF.md"),
  (Join-Path $p162Dir "P162_DEV_STOP_DECISION.md")
)

Write-Host ""
Write-Host "OPERATOR FILES:"
foreach ($file in $files) {
  if (Test-Path -LiteralPath $file) {
    Write-Host "OK  $file"
  } else {
    Write-Host "MISS $file"
  }
}

Write-Host ""
Write-Host "FINAL_STATUS=MVP_QAIC_LOCAL_PRIVATE_RELEASE_CLOSED_DEV_STOP"
Write-Host "NEXT=USE_LOCAL_PRIVATE_OPERATOR_FLOW_ONLY"
Write-Host "============================================================"
