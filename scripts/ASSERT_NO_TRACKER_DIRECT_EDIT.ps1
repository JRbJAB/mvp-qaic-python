param(
  [string]$RepoRoot = "",
  [switch]$AllowTrackerRenderOnly
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version 2.0

if ([string]::IsNullOrWhiteSpace($RepoRoot)) { $RepoRoot = (Get-Location).Path }
$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
Set-Location -LiteralPath $RepoRoot

$changed = @(git status --porcelain -- "mvp_qaic_reflex_ui/migration_tracker.py")
$allowEnv = $env:QAIC_ALLOW_TRACKER_RENDER_ONLY_EDIT
if ($changed.Count -gt 0 -and -not $AllowTrackerRenderOnly -and $allowEnv -ne "true") {
  Write-Host "STATUS=FAILED_NO_TRACKER_DIRECT_EDIT"
  Write-Host "TRACKER_CHANGED=$($changed -join '; ')"
  Write-Host "POLICY=P12G+ must write migration decisions to JSON/overlay or migration_os.py, not directly to migration_tracker.py."
  throw "migration_tracker.py direct edit is blocked"
}
Write-Host "STATUS=OK_NO_TRACKER_DIRECT_EDIT"
