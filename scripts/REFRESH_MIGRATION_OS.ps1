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
  '{ "version": "0.2.0", "decisions": [] }' | Set-Content -LiteralPath $overlay -Encoding UTF8
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
if not isinstance(rows, list):
    rows = []

overlay_path = repo / "docs" / "MIGRATION_DECISION_OVERLAY.json"
try:
    overlay = json.loads(overlay_path.read_text(encoding="utf-8-sig"))
except FileNotFoundError:
    overlay = {"version": "0.2.0", "decisions": []}

decisions = overlay.get("decisions", []) if isinstance(overlay, dict) else []
by_source = {}
for entry in decisions:
    if not isinstance(entry, dict):
        continue
    source = str(entry.get("source") or "").strip()
    if source:
        by_source[source] = entry

applied = 0
for row in rows:
    if not isinstance(row, dict):
        continue
    source = str(row.get("source") or row.get("Source") or row.get("name") or "").strip()
    decision = by_source.get(source)
    if decision:
        applied += 1
        row["decision_override"] = True
        row["decision_status"] = decision.get("decision_status")
        row["decision_note"] = decision.get("note", "")
        row["decision_reviewer"] = decision.get("reviewer", "")
        row["decision_updated_at_utc"] = decision.get("updated_at_utc", "")
        if decision.get("target"):
            row["target"] = decision.get("target")
            row["cible"] = decision.get("target")
        row["status"] = decision.get("decision_status")
        row["Statut"] = decision.get("decision_status")
    else:
        row.setdefault("decision_override", False)

payload["rows"] = rows
payload.setdefault("missing_legacy", [])
payload.setdefault("missing_essential", [])
payload.setdefault("duplicate_sources", [])
payload.setdefault("legacy_first_15_exact", payload.get("legacy_row_count") == 15)
payload.setdefault("raw_function_rows_visible", False)
payload.setdefault("row_count", len(rows))
payload.setdefault("function_index_count", 0)
payload["decision_overlay_count"] = len(by_source)
payload["decision_overlay_applied_count"] = applied

hash_source = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
payload["data_hash"] = hashlib.sha256(hash_source.encode("utf-8")).hexdigest()[:16]
payload["refreshed_at_utc"] = datetime.now(timezone.utc).isoformat()
payload["live_meta"] = {
    "status": "OK_MIGRATION_OS_REFRESH",
    "data_hash": payload["data_hash"],
    "row_count": payload.get("row_count"),
    "function_index_count": payload.get("function_index_count"),
    "decision_overlay_count": payload.get("decision_overlay_count"),
    "decision_overlay_applied_count": payload.get("decision_overlay_applied_count"),
    "refreshed_at_utc": payload["refreshed_at_utc"],
}

docs = repo / "docs"
payload_path = docs / "MIGRATION_OS_LIVE_PAYLOAD.json"
signal_path = docs / "MIGRATION_OS_REFRESH_SIGNAL.txt"

tmp_payload = payload_path.with_suffix(payload_path.suffix + ".tmp")
tmp_payload.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
tmp_payload.replace(payload_path)

signal = dict(payload["live_meta"])
tmp_signal = signal_path.with_suffix(signal_path.suffix + ".tmp")
tmp_signal.write_text(json.dumps(signal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
tmp_signal.replace(signal_path)

print("STATUS=OK_MIGRATION_OS_REFRESH")
print("LIVE_PAYLOAD=docs/MIGRATION_OS_LIVE_PAYLOAD.json")
print("REFRESH_SIGNAL=docs/MIGRATION_OS_REFRESH_SIGNAL.txt")
print("DATA_HASH=" + payload["data_hash"])
print("ROW_COUNT=" + str(payload.get("row_count")))
print("FUNCTION_INDEX_COUNT=" + str(payload.get("function_index_count")))
print("DECISION_OVERLAY_COUNT=" + str(payload.get("decision_overlay_count")))
print("DECISION_OVERLAY_APPLIED_COUNT=" + str(payload.get("decision_overlay_applied_count")))
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
