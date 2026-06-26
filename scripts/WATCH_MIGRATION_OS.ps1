param(
  [string]$RepoRoot = "",
  [int]$IntervalSeconds = 5
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version 2.0
chcp 65001 | Out-Null
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

if ([string]::IsNullOrWhiteSpace($RepoRoot)) { $RepoRoot = (Get-Location).Path }
$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
Set-Location -LiteralPath $RepoRoot

$watch = @(
  "docs\MIGRATION_GLOBAL_MATRIX.json",
  "docs\MIGRATION_GLOBAL_MATRIX_SUMMARY.json",
  "docs\MIGRATION_DECISION_OVERLAY.json",
  "docs\MVPQAIC_CLASP_IMPORTS_ALL.csv",
  "docs\MVPQAIC_CLASP_IMPORTS_ALL_HEADERS.csv"
)

function Get-Signature {
  $parts = @()
  foreach ($rel in $watch) {
    $p = Join-Path $RepoRoot $rel
    if (Test-Path -LiteralPath $p) {
      $item = Get-Item -LiteralPath $p
      $parts += ("{0}:{1}:{2}" -f $rel, $item.LastWriteTimeUtc.Ticks, $item.Length)
    } else {
      $parts += ("{0}:MISSING" -f $rel)
    }
  }
  return ($parts -join "|")
}

Write-Host "STATUS=WATCH_MIGRATION_OS_STARTED"
Write-Host "REPO_ROOT=$RepoRoot"
Write-Host "INTERVAL_SECONDS=$IntervalSeconds"
Write-Host "CTRL_C_TO_STOP=true"

$last = ""
while ($true) {
  $sig = Get-Signature
  if ($sig -ne $last) {
    Write-Host "CHANGE_DETECTED=$(Get-Date -Format o)"
    powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $RepoRoot "scripts\REFRESH_MIGRATION_OS.ps1") -RepoRoot $RepoRoot
    if ($LASTEXITCODE -ne 0) { Write-Host "REFRESH_FAILED_EXIT=$LASTEXITCODE" }
    $last = $sig
  }
  Start-Sleep -Seconds $IntervalSeconds
}
