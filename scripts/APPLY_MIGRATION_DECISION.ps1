param(
  [Parameter(Mandatory=$true)]
  [string]$RepoRoot,
  [Parameter(Mandatory=$true)]
  [string]$Source,
  [Parameter(Mandatory=$true)]
  [string]$DecisionStatus,
  [string]$Target = "",
  [string]$Note = "",
  [string]$Reviewer = "operator"
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

from mvp_qaic_reflex_ui.migration_decision_workbench import upsert_decision

entry = upsert_decision(
    repo,
    source=r'''$Source''',
    decision_status=r'''$DecisionStatus''',
    target=r'''$Target''',
    note=r'''$Note''',
    reviewer=r'''$Reviewer''',
)
print("STATUS=OK_MIGRATION_DECISION_APPLIED")
print("SOURCE=" + entry["source"])
print("DECISION_STATUS=" + entry["decision_status"])
"@

$pyPath = Join-Path $env:TEMP ("qaic_apply_migration_decision_" + [guid]::NewGuid().ToString("N") + ".py")
Set-Content -LiteralPath $pyPath -Value $py -Encoding UTF8
try {
  python $pyPath
  if ($LASTEXITCODE -ne 0) { throw "python decision apply failed: $LASTEXITCODE" }
}
finally {
  Remove-Item -LiteralPath $pyPath -Force -ErrorAction SilentlyContinue
}

powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $RepoRoot "scripts\REFRESH_MIGRATION_OS.ps1") -RepoRoot $RepoRoot
