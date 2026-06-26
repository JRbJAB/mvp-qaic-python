param(
  [string]$RepoRoot = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version 2.0
chcp 65001 | Out-Null
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

function Fail([string]$Message) {
  Write-Host "STATUS=FAILED_MIGRATION_OS_REFRESH"
  Write-Host "ERROR=$Message"
  throw $Message
}

Write-Host "===== QAIC MIGRATION OS REFRESH ====="
Write-Host "NO_PUBLIC_DEPLOY=true"
Write-Host "NO_LIVE_ACTION=true"
Write-Host "NO_BROKER_ORDER_SIZING=true"
Write-Host "NO_SHEET_WRITE=true"
Write-Host "NO_BIGQUERY_WRITE=true"
Write-Host "HUMAN_REVIEW_ONLY=true"

if ([string]::IsNullOrWhiteSpace($RepoRoot)) { $RepoRoot = (Get-Location).Path }
$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
Set-Location -LiteralPath $RepoRoot

$required = @(
  "docs\MIGRATION_GLOBAL_MATRIX.json",
  "docs\MIGRATION_GLOBAL_MATRIX_SUMMARY.json",
  "docs\MIGRATION_DECISION_OVERLAY.json",
  "mvp_qaic_reflex_ui\migration_os.py"
)
foreach ($rel in $required) {
  if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot $rel) -PathType Leaf)) { Fail "INPUT_MISSING=$rel" }
  Write-Host "INPUT_OK=$rel"
}

$env:QAIC_REPO_ROOT = $RepoRoot
if ([string]::IsNullOrWhiteSpace($env:PYTHONPATH)) {
  $env:PYTHONPATH = $RepoRoot
} elseif ($env:PYTHONPATH -notlike "*$RepoRoot*") {
  $env:PYTHONPATH = "$RepoRoot;$env:PYTHONPATH"
}

$tmp = Join-Path $env:TEMP ("qaic_refresh_migration_os_" + [Guid]::NewGuid().ToString("N") + ".py")
$python = @'
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

repo = Path(os.environ["QAIC_REPO_ROOT"]).resolve()
sys.path.insert(0, str(repo))
os.chdir(repo)

from mvp_qaic_reflex_ui.migration_os import build_migration_tracker_payload

payload = build_migration_tracker_payload()
body_for_hash = json.dumps(payload, ensure_ascii=False, sort_keys=True)
payload["live_meta"] = {
    "schema_version": "MIGRATION_OS_LIVE_PAYLOAD_1.0.0",
    "updated_at_utc": datetime.now(timezone.utc).isoformat(),
    "data_hash": hashlib.sha256(body_for_hash.encode("utf-8")).hexdigest()[:16],
    "source": "scripts/REFRESH_MIGRATION_OS.ps1",
}

docs = repo / "docs"
docs.mkdir(parents=True, exist_ok=True)
out = docs / "MIGRATION_OS_LIVE_PAYLOAD.json"
tmp_out = out.with_suffix(".json.tmp")
tmp_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
tmp_out.replace(out)

signal = docs / "MIGRATION_OS_REFRESH_SIGNAL.txt"
signal.write_text(
    "updated_at_utc=" + payload["live_meta"]["updated_at_utc"] + "\n"
    + "data_hash=" + payload["live_meta"]["data_hash"] + "\n",
    encoding="utf-8",
)

print("STATUS=OK_MIGRATION_OS_REFRESH")
print("LIVE_PAYLOAD=docs/MIGRATION_OS_LIVE_PAYLOAD.json")
print("REFRESH_SIGNAL=docs/MIGRATION_OS_REFRESH_SIGNAL.txt")
print("DATA_HASH=" + payload["live_meta"]["data_hash"])
print("ROW_COUNT=" + str(payload.get("row_count", "")))
print("FUNCTION_INDEX_COUNT=" + str(payload.get("function_index_count", "")))
'@
[System.IO.File]::WriteAllText($tmp, $python, [System.Text.UTF8Encoding]::new($false))
try {
  python $tmp
  if ($LASTEXITCODE -ne 0) { Fail "python refresh failed exit=$LASTEXITCODE" }
} finally {
  Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
}

if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot "docs\MIGRATION_OS_LIVE_PAYLOAD.json") -PathType Leaf)) { Fail "MIGRATION_OS_LIVE_PAYLOAD_MISSING" }
if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot "docs\MIGRATION_OS_REFRESH_SIGNAL.txt") -PathType Leaf)) { Fail "MIGRATION_OS_REFRESH_SIGNAL_MISSING" }
