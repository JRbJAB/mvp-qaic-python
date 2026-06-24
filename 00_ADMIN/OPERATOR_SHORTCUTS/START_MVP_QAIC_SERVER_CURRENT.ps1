param(
  [switch]$Pull
)

$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$repo = "C:\Users\Julie\Documents\JRb-Dev\MVP_QAIC_PY_WORK_20260623_192901"
Set-Location -LiteralPath $repo

Write-Host "============================================================"
Write-Host "MVP_QAIC_SERVER_START_CURRENT"
Write-Host "============================================================"
Write-Host "REPO=$repo"
Write-Host "HEAD_BEFORE=$(git rev-parse --short HEAD)"

if ($Pull) {
  $dirty = git status --short --untracked-files=all
  if ($dirty) {
    Write-Host "REPO_DIRTY_NO_PULL:"
    Write-Host $dirty
    throw "Repo dirty: refusing automatic pull"
  }
  git fetch origin master
  git pull --ff-only origin master
  Write-Host "HEAD_AFTER_PULL=$(git rev-parse --short HEAD)"
}

Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue | ForEach-Object {
  if ($_.OwningProcess -and $_.OwningProcess -ne $PID) {
    Write-Host "STOP_OLD_8080_PID=$($_.OwningProcess)"
    Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
  }
}

Write-Host "OPEN=http://127.0.0.1:8080/"
Write-Host "OPEN=http://127.0.0.1:8080/sheets-cockpit-plan"
Write-Host "OPEN=http://127.0.0.1:8080/migration-control"
Write-Host "OPEN=http://127.0.0.1:8080/docs"
Write-Host "OPEN=http://127.0.0.1:8080/notice"

python -m mvp_qaic_py.p173_nicegui_private_local_runner `
  --project-root $repo `
  --host 127.0.0.1 `
  --port 8080 `
  --serve-private
