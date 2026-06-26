param(
  [Parameter(Mandatory=$true)]
  [string]$RepoRoot
)

$ErrorActionPreference = "Stop"

Write-Host "===== QAIC MIGRATION OS REFRESH ====="
Write-Host "NO_PUBLIC_DEPLOY=true"
Write-Host "NO_LIVE_ACTION=true"
Write-Host "NO_BROKER_ORDER_SIZING=true"
Write-Host "NO_SHEET_WRITE=true"
Write-Host "NO_BIGQUERY_WRITE=true"
Write-Host "HUMAN_REVIEW_ONLY=true"

if (-not (Test-Path -LiteralPath $RepoRoot)) {
  throw "REPO_ROOT_MISSING=$RepoRoot"
}

Set-Location -LiteralPath $RepoRoot
$env:QAIC_REPO_ROOT = $RepoRoot
$env:PYTHONPATH = $RepoRoot

$overlay = Join-Path $RepoRoot "docs\MIGRATION_DECISION_OVERLAY.json"
if (-not (Test-Path -LiteralPath $overlay)) {
  '{ "version": "0.1.0", "decisions": [] }' | Set-Content -LiteralPath $overlay -Encoding UTF8
}

$inputs = @(
  "docs\MIGRATION_GLOBAL_MATRIX.json",
  "docs\MIGRATION_GLOBAL_MATRIX_SUMMARY.json",
  "docs\MIGRATION_DECISION_OVERLAY.json",
  "mvp_qaic_reflex_ui\migration_os.py"
)

foreach ($rel in $inputs) {
  $p = Join-Path $RepoRoot $rel
  if (-not (Test-Path -LiteralPath $p)) {
    throw "INPUT_MISSING=$rel"
  }
  Write-Host "INPUT_OK=$rel"
}

$py = @"
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
rows = payload.get("rows", [])

payload.setdefault("missing_legacy", [])
payload.setdefault("missing_essential", [])
payload.setdefault("duplicate_sources", [])
payload.setdefault("legacy_first_15_exact", payload.get("legacy_row_count") == 15)
payload.setdefault("raw_function_rows_visible", False)
payload.setdefault("row_count", len(rows))
payload.setdefault("function_index_count", 0)

hash_source = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
payload["data_hash"] = hashlib.sha256(hash_source.encode("utf-8")).hexdigest()[:16]
payload["refreshed_at_utc"] = datetime.now(timezone.utc).isoformat()
payload["live_meta"] = {
    "status": "OK_MIGRATION_OS_REFRESH",
    "data_hash": payload["data_hash"],
    "row_count": payload.get("row_count"),
    "function_index_count": payload.get("function_index_count"),
    "refreshed_at_utc": payload["refreshed_at_utc"],
}

docs = repo / "docs"
payload_path = docs / "MIGRATION_OS_LIVE_PAYLOAD.json"
signal_path = docs / "MIGRATION_OS_REFRESH_SIGNAL.txt"

tmp_payload = payload_path.with_suffix(payload_path.suffix + ".tmp")
tmp_payload.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
tmp_payload.replace(payload_path)

signal = {
    "status": "OK_MIGRATION_OS_REFRESH",
    "data_hash": payload["data_hash"],
    "row_count": payload.get("row_count"),
    "function_index_count": payload.get("function_index_count"),
    "refreshed_at_utc": payload["refreshed_at_utc"],
}
tmp_signal = signal_path.with_suffix(signal_path.suffix + ".tmp")
tmp_signal.write_text(json.dumps(signal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
tmp_signal.replace(signal_path)

print("STATUS=OK_MIGRATION_OS_REFRESH")
print("LIVE_PAYLOAD=docs/MIGRATION_OS_LIVE_PAYLOAD.json")
print("REFRESH_SIGNAL=docs/MIGRATION_OS_REFRESH_SIGNAL.txt")
print("DATA_HASH=" + payload["data_hash"])
print("ROW_COUNT=" + str(payload.get("row_count")))
print("FUNCTION_INDEX_COUNT=" + str(payload.get("function_index_count")))
"@

$pyPath = Join-Path $env:TEMP ("qaic_refresh_migration_os_" + [guid]::NewGuid().ToString("N") + ".py")
Set-Content -LiteralPath $pyPath -Value $py -Encoding UTF8

try {
  python $pyPath
  if ($LASTEXITCODE -ne 0) {
    throw "python refresh failed: PYTHON_REFRESH_FAILED=$LASTEXITCODE"
  }
}
finally {
  Remove-Item -LiteralPath $pyPath -Force -ErrorAction SilentlyContinue
}

if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot "docs\MIGRATION_OS_LIVE_PAYLOAD.json"))) {
  throw "LIVE_PAYLOAD_MISSING"
}
if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot "docs\MIGRATION_OS_REFRESH_SIGNAL.txt"))) {
  throw "REFRESH_SIGNAL_MISSING"
}
