# P_REFLEX_12F - Refresh Global Migration Matrix + runtime hot refresh
# Mode: LOCAL_REFRESH_ONLY_NO_DRIVE_SCAN_NO_SERVER_RESTART
# Purpose: regenerate docs/MIGRATION_GLOBAL_MATRIX.* and sync docs to LocalAppData runtime.
# Safe: local repo/runtime files only; no public deploy, no live action, no broker/order/sizing, no Sheets/BQ write.
param(
  [string]$RepoRoot = "",
  [string]$RuntimeRoot = "C:\Users\Julie\AppData\Local\MVP_QAIC_REFLEX_RUNTIME\P_REFLEX_06C_20260625_200632",
  [switch]$NoRuntimeSync,
  [switch]$NoHotReloadTouch
)

$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

$env:NO_PUBLIC_DEPLOY = "true"
$env:NO_LIVE_ACTION = "true"
$env:NO_BROKER_ORDER_SIZING = "true"
$env:NO_SHEET_WRITE = "true"
$env:NO_BIGQUERY_WRITE = "true"
$env:HUMAN_REVIEW_ONLY = "true"

function Write-Step([string]$Message) {
  Write-Host ""
  Write-Host "===== $Message ====="
}

function Resolve-RepoNoScan([string]$Candidate) {
  if (-not [string]::IsNullOrWhiteSpace($Candidate)) {
    if ((Test-Path -LiteralPath $Candidate) -and (Test-Path -LiteralPath (Join-Path $Candidate ".git"))) {
      return (Resolve-Path -LiteralPath $Candidate).Path
    }
    throw "STOP: RepoRoot invalid or not a git repo: $Candidate"
  }
  if ($env:MVP_QAIC_REPO -and (Test-Path -LiteralPath $env:MVP_QAIC_REPO) -and (Test-Path -LiteralPath (Join-Path $env:MVP_QAIC_REPO ".git"))) {
    return (Resolve-Path -LiteralPath $env:MVP_QAIC_REPO).Path
  }
  $cwd = (Get-Location).Path
  if ((Test-Path -LiteralPath (Join-Path $cwd ".git"))) { return $cwd }
  throw "STOP: RepoRoot required. Pass -RepoRoot or set env:MVP_QAIC_REPO. No drive scan is performed."
}

function Select-Python() {
  if (Get-Command py -ErrorAction SilentlyContinue) { return @("py", "-3") }
  if (Get-Command python -ErrorAction SilentlyContinue) { return @("python") }
  throw "STOP: python not found"
}

function Copy-OneFile([string]$SrcRoot, [string]$DstRoot, [string]$RelPath) {
  $src = Join-Path $SrcRoot $RelPath
  $dst = Join-Path $DstRoot $RelPath
  if (-not (Test-Path -LiteralPath $src)) { throw "STOP: source missing for runtime sync: $RelPath" }
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dst) | Out-Null
  Copy-Item -LiteralPath $src -Destination $dst -Force
  Write-Host "RUNTIME_SYNC_FILE_OK=$RelPath"
}

function Touch-HotReload([string]$RuntimeRoot) {
  $touchTargets = @(
    "mvp_qaic_reflex_ui\mission_control_auto_update_panel.py",
    "mvp_qaic_reflex_ui\global_migration_page.py"
  )
  foreach ($rel in $touchTargets) {
    $target = Join-Path $RuntimeRoot $rel
    if (Test-Path -LiteralPath $target) {
      (Get-Item -LiteralPath $target).LastWriteTime = Get-Date
      Write-Host "HOT_RELOAD_TOUCH_OK=$rel"
    } else {
      Write-Host "HOT_RELOAD_TOUCH_SKIP_MISSING=$rel"
    }
  }
}

try {
  Write-Step "SAFE FLAGS"
  Write-Host "NO_PUBLIC_DEPLOY=$env:NO_PUBLIC_DEPLOY"
  Write-Host "NO_LIVE_ACTION=$env:NO_LIVE_ACTION"
  Write-Host "NO_BROKER_ORDER_SIZING=$env:NO_BROKER_ORDER_SIZING"
  Write-Host "NO_SHEET_WRITE=$env:NO_SHEET_WRITE"
  Write-Host "NO_BIGQUERY_WRITE=$env:NO_BIGQUERY_WRITE"
  Write-Host "HUMAN_REVIEW_ONLY=$env:HUMAN_REVIEW_ONLY"
  Write-Host "MODE=LOCAL_REFRESH_ONLY_NO_DRIVE_SCAN_NO_SERVER_RESTART"

  Write-Step "RESOLVE REPO NO SCAN"
  $RepoRoot = Resolve-RepoNoScan $RepoRoot
  Set-Location -LiteralPath $RepoRoot
  Write-Host "REPO_ROOT=$RepoRoot"
  Write-Host "RUNTIME_ROOT=$RuntimeRoot"

  Write-Step "VERIFY INPUTS"
  $requiredInputs = @(
    "docs\MVPQAIC_CLASP_IMPORTS_ALL.csv",
    "mvp_qaic_reflex_ui\migration_global_matrix.py"
  )
  foreach ($rel in $requiredInputs) {
    $full = Join-Path $RepoRoot $rel
    if (-not (Test-Path -LiteralPath $full)) { throw "STOP: missing input: $rel" }
    Write-Host "INPUT_OK=$rel"
  }

  Write-Step "PYTHON SELECTOR"
  $pyParts = Select-Python
  $PythonExe = $pyParts[0]
  $PythonArgs = @()
  if ($pyParts.Count -gt 1) { $PythonArgs = $pyParts[1..($pyParts.Count - 1)] }
  & $PythonExe @PythonArgs --version
  if ($LASTEXITCODE -ne 0) { throw "STOP: python --version failed" }

  Write-Step "REFRESH GLOBAL MIGRATION MATRIX"
  $env:PYTHONPATH = "$RepoRoot;$env:PYTHONPATH"
  & $PythonExe @PythonArgs -m mvp_qaic_reflex_ui.migration_global_matrix --repo-root $RepoRoot --write
  if ($LASTEXITCODE -ne 0) { throw "FAILED: migration global matrix refresh" }

  Write-Step "VERIFY OUTPUTS"
  $requiredOutputs = @(
    "docs\MIGRATION_GLOBAL_MATRIX.csv",
    "docs\MIGRATION_GLOBAL_MATRIX.json",
    "docs\MIGRATION_GLOBAL_MATRIX.md",
    "docs\MIGRATION_GLOBAL_MATRIX_SUMMARY.json",
    "docs\MIGRATION_STATUS_LEGEND.json"
  )
  foreach ($rel in $requiredOutputs) {
    $full = Join-Path $RepoRoot $rel
    if (-not (Test-Path -LiteralPath $full)) { throw "STOP: missing output after refresh: $rel" }
    Write-Host "OUTPUT_OK=$rel"
  }

  Write-Step "SUMMARY"
  $summaryPath = Join-Path $RepoRoot "docs\MIGRATION_GLOBAL_MATRIX_SUMMARY.json"
  & $PythonExe @PythonArgs -c "import json, pathlib; p=pathlib.Path(r'$summaryPath'); s=json.loads(p.read_text(encoding='utf-8')); print('TOTAL_ROWS='+str(s.get('total_rows'))); print('SOURCE_CSV_ROWS='+str(s.get('source_csv_rows'))); print('SCRIPT_INVENTORY_COUNT='+str(s.get('script_inventory_count'))); print('FUNCTION_INDEX_COUNT='+str(s.get('function_index_count'))); print('BY_SCOPE='+json.dumps(s.get('by_scope',{}), ensure_ascii=False)); print('BY_STATUS='+json.dumps(s.get('by_status',{}), ensure_ascii=False))"
  if ($LASTEXITCODE -ne 0) { throw "FAILED: print summary" }

  if (-not $NoRuntimeSync) {
    Write-Step "SYNC RUNTIME DOCS FOR PAGE REFRESH"
    if (-not (Test-Path -LiteralPath $RuntimeRoot)) { throw "STOP: RuntimeRoot missing: $RuntimeRoot" }
    $runtimeFiles = @(
      "docs\MIGRATION_GLOBAL_MATRIX.csv",
      "docs\MIGRATION_GLOBAL_MATRIX.json",
      "docs\MIGRATION_GLOBAL_MATRIX.md",
      "docs\MIGRATION_GLOBAL_MATRIX_SUMMARY.json",
      "docs\MIGRATION_STATUS_LEGEND.json",
      "docs\MVPQAIC_CLASP_IMPORTS_ALL.csv",
      "docs\MVPQAIC_CLASP_IMPORTS_ALL_HEADERS.csv",
      "mvp_qaic_reflex_ui\mission_control_auto_update_panel.py",
      "mvp_qaic_reflex_ui\global_migration_page.py",
      "mvp_qaic_reflex_ui\migration_global_matrix.py"
    )
    foreach ($rel in $runtimeFiles) { Copy-OneFile $RepoRoot $RuntimeRoot $rel }
    if (-not $NoHotReloadTouch) { Touch-HotReload $RuntimeRoot }
    Write-Host "RUNTIME_SYNC_OK=True"
    Write-Host "HOT_REFRESH_POLICY=NO_SERVER_RESTART_BROWSER_REFRESH_AFTER_HOT_RELOAD"
  } else {
    Write-Host "RUNTIME_SYNC_SKIPPED_BY_PARAM=True"
  }

  Write-Step "FINAL STATUS"
  Write-Host "STATUS=OK_P_REFLEX_12F_REFRESH_GLOBAL_MIGRATION_MATRIX_HOT_RUNTIME"
  Write-Host "NEXT=REFRESH_BROWSER_MISSION_CONTROL"
}
catch {
  Write-Host ""
  Write-Host "===== FINAL STATUS ====="
  Write-Host "STATUS=FAILED_P_REFLEX_12F_REFRESH_GLOBAL_MIGRATION_MATRIX_HOT_RUNTIME"
  Write-Host "ERROR=$($_.Exception.Message)"
  exit 1
}
