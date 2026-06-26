
# ============================================================
# P_REFLEX_12E-R2 — Permanent private local Reflex server + runtime sync
# Run manually only. Not called by the batch.
# ============================================================

param(
  [string]$RuntimeRoot = "C:\Users\Julie\AppData\Local\MVP_QAIC_REFLEX_RUNTIME\P_REFLEX_06C_20260625_200632",
  [int]$SyncEverySeconds = 4,
  [switch]$NoServerStart
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
$env:NO_BROWSER_OPEN = "true"

function Write-Step($Message) {
  Write-Host ""
  Write-Host "===== $Message ====="
}

function Add-RepoCandidate([string]$Candidate, [string]$Reason) {
  if ([string]::IsNullOrWhiteSpace($Candidate)) { return }
  $gitDir = "$Candidate\.git"
  if (Test-Path -LiteralPath $gitDir) {
    $script:RepoCandidates += [pscustomobject]@{ Path = $Candidate; Reason = $Reason }
  }
}

Write-Step "RESOLVE REPO WITHOUT Q DRIVE ASSUMPTION"
$script:RepoCandidates = @()
if ($env:MVP_QAIC_REPO -and (Test-Path -LiteralPath $env:MVP_QAIC_REPO)) {
  Add-RepoCandidate $env:MVP_QAIC_REPO "env:MVP_QAIC_REPO"
}
if (Test-Path -LiteralPath "Q:\") {
  Add-RepoCandidate "Q:\MVP_QAIC_PY" "Q drive shortcut"
} else {
  Write-Host "Q_DRIVE_AVAILABLE=False"
}
if (Test-Path -LiteralPath "G:\") {
  Add-RepoCandidate "G:\Mon Drive\👥 JULIEN [Perso]\📈 Trading JRb\Solutions & Dev (Trading JRb)\MVP_QAIC_PY" "durable G drive path"
}

$REPO = $null
foreach ($candidate in $script:RepoCandidates) {
  if (-not $REPO) { $REPO = $candidate.Path }
}
if (-not $REPO) { throw "STOP: repo MVP_QAIC_PY introuvable" }
Write-Host "REPO_ROOT=$REPO"
Write-Host "RUNTIME_ROOT=$RuntimeRoot"

function Sync-OneDir([string]$RelPath) {
  $src = "$REPO\$RelPath"
  $dst = "$RuntimeRoot\$RelPath"
  if (Test-Path -LiteralPath $src) {
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    robocopy $src $dst /MIR /NFL /NDL /NJH /NJS /NP | Out-Null
    if ($LASTEXITCODE -le 7) { $global:LASTEXITCODE = 0 } else { throw "ROBOCOPY_FAILED $RelPath code=$LASTEXITCODE" }
    Write-Host "SYNC_DIR_OK=$RelPath"
  } else {
    Write-Host "SYNC_DIR_SKIP_MISSING=$RelPath"
  }
}

function Sync-OneFile([string]$RelPath) {
  $src = "$REPO\$RelPath"
  $dst = "$RuntimeRoot\$RelPath"
  if (Test-Path -LiteralPath $src) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dst) | Out-Null
    Copy-Item -LiteralPath $src -Destination $dst -Force
    Write-Host "SYNC_FILE_OK=$RelPath"
  } else {
    Write-Host "SYNC_FILE_SKIP_MISSING=$RelPath"
  }
}

function Sync-RepoToRuntime() {
  New-Item -ItemType Directory -Force -Path $RuntimeRoot | Out-Null
  Sync-OneDir "mvp_qaic_reflex_ui"
  Sync-OneDir "assets"
  Sync-OneDir "docs"
  Sync-OneDir "05_EXPORTS"
  Sync-OneFile "rxconfig.py"
  Sync-OneFile "requirements.txt"
  Sync-OneFile "pyproject.toml"
}

Write-Step "INITIAL SYNC"
Sync-RepoToRuntime

$serverProcId = $null
if (-not $NoServerStart) {
  Write-Step "START PRIVATE REFLEX SERVER"
  Set-Location -LiteralPath $RuntimeRoot
  $cmd = "python -m reflex run --frontend-port 3000 --backend-port 8000"
  $serverProcess = Start-Process -FilePath "powershell" -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", $cmd) -PassThru -WindowStyle Minimized
  $serverProcId = $serverProcess.Id
  Write-Host "SERVER_PROCESS_ID=$serverProcId"
  Write-Host "FRONTEND=http://localhost:3000/"
  Write-Host "BACKEND=http://127.0.0.1:8000"
} else {
  Write-Host "SERVER_START_SKIPPED_BY_PARAM=True"
}

Write-Step "WATCHER LOOP"
Write-Host "Press Ctrl+C to stop."
while ($true) {
  Sync-RepoToRuntime
  Start-Sleep -Seconds $SyncEverySeconds
}
