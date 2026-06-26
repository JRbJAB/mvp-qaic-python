param(
  [Parameter(Mandatory=$true)]
  [string]$RepoRoot,
  [int]$Limit = 200
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $RepoRoot)) { throw "REPO_ROOT_MISSING=$RepoRoot" }
Set-Location -LiteralPath $RepoRoot
$env:QAIC_REPO_ROOT = $RepoRoot
$env:PYTHONPATH = $RepoRoot

$py = @"
from __future__ import annotations

import os
import sys
from pathlib import Path

repo = Path(os.environ["QAIC_REPO_ROOT"]).resolve()
sys.path.insert(0, str(repo))
os.chdir(repo)

from mvp_qaic_reflex_ui.migration_decision_workbench import export_decision_queue

queue = export_decision_queue(repo, limit=int($Limit))
print("STATUS=OK_MIGRATION_DECISION_QUEUE_EXPORTED")
print("QUEUE=docs/MIGRATION_DECISION_QUEUE.json")
print("QUEUE_COUNT=" + str(queue.get("queue_count")))
print("OVERLAY_DECISION_COUNT=" + str(queue.get("overlay_decision_count")))
"@

$pyPath = Join-Path $env:TEMP ("qaic_export_migration_decision_queue_" + [guid]::NewGuid().ToString("N") + ".py")
Set-Content -LiteralPath $pyPath -Value $py -Encoding UTF8
try {
  python $pyPath
  if ($LASTEXITCODE -ne 0) { throw "python queue export failed: $LASTEXITCODE" }
}
finally {
  Remove-Item -LiteralPath $pyPath -Force -ErrorAction SilentlyContinue
}
