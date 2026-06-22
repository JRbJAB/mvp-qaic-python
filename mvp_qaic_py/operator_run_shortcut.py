from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

VERSION = "MVP_QAIC_P127_OPERATOR_RUN_SHORTCUT_LOCAL_ONLY_0_1_1_ZIP_SAFE"

SAFETY_MARKERS = (
    "LOCAL_ONLY",
    "OPERATOR_SHORTCUT_ONLY",
    "HUMAN_REVIEW_ONLY",
    "NO_INDEX_EDIT",
    "NO_CLASP",
    "NO_APPS_SCRIPT_EXECUTION",
    "NO_SHEET_WRITE",
    "NO_PUBLIC_DEPLOY",
    "NO_BROKER",
    "NO_ORDER",
    "NO_CANCEL",
    "NO_REPLACE_ORDER",
    "NO_AUTO_SIZING",
    "NO_AUTO_APPLY_GEM_RESPONSE",
    "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
)

OUTPUT_FILES = (
    "P127_OPERATOR_RUN_SHORTCUT.ps1",
    "P127_ONE_COMMAND_OPERATOR_GUIDE.md",
    "P127_OPERATOR_DAILY_RUNBOOK.md",
    "P127_SHORTCUT_CHECKLIST.csv",
    "P127_SHORTCUT_CONTRACT.json",
    "P127_SHORTCUT_MANIFEST.json",
    "P127_README.md",
)


@dataclass(frozen=True)
class OperatorRunShortcutRequest:
    output_dir: str | Path
    run_id: str = "P127-OPERATOR-RUN-SHORTCUT"
    generated_at_utc: str | None = None
    notes: str | None = None


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _write_checklist(path: Path) -> None:
    rows = [
        ("1", "Create local P124 folder", "YES", "LOCAL_ONLY", "READY"),
        ("2", "Fill portfolio_input.txt manually", "YES", "HUMAN_REVIEW_ONLY", "OPERATOR_ACTION"),
        (
            "3",
            "Paste GEM answer into gem_response.txt",
            "YES",
            "NO_AUTO_APPLY_GEM_RESPONSE",
            "OPERATOR_ACTION",
        ),
        ("4", "Run P125 review UX", "YES", "NO_SHEET_WRITE", "READY"),
        ("5", "Run P126 local registry", "YES", "REGISTRY_ONLY", "READY"),
    ]
    fields = ["step", "name", "required", "safety", "status"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for step, name, required, safety, status in rows:
            writer.writerow(
                {
                    "step": step,
                    "name": name,
                    "required": required,
                    "safety": safety,
                    "status": status,
                }
            )


def build_shortcut_contract() -> dict[str, Any]:
    return {
        "contract": "P127_OPERATOR_RUN_SHORTCUT_LOCAL_ONLY",
        "version": VERSION,
        "status": "SHORTCUT_READY",
        "purpose": "Provide one local operator shortcut to prepare P124 input, run P125 review, and refresh P126 registry.",
        "does_not": [
            "run Apps Script",
            "write Google Sheets",
            "push clasp",
            "deploy public web app",
            "execute broker operation",
            "place order",
            "cancel order",
            "replace order",
            "auto-size position",
            "access Revolut X real account from MVP",
            "auto-apply GEM response",
        ],
        "operator_boundaries": [
            "portfolio_input.txt is filled manually",
            "GEM prompt is pasted manually",
            "GEM response is pasted manually",
            "all outputs remain local",
        ],
        "safety_markers": list(SAFETY_MARKERS),
        "outputs": list(OUTPUT_FILES),
    }


def _shortcut_script() -> str:
    return r"""
# P127 Operator Run Shortcut
# LOCAL ONLY / HUMAN REVIEW ONLY / NO SHEET WRITE / NO BROKER / NO ORDER / NO SIZING

$ErrorActionPreference = "Stop"
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

function Fail($Message) { throw "[P127 SHORTCUT BLOCKED] $Message" }

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$CandidateRepo = Resolve-Path -LiteralPath (Join-Path $Here "..\..") -ErrorAction SilentlyContinue
if (-not $CandidateRepo) { Fail "Cannot resolve repo root from shortcut location" }

$RepoRoot = $CandidateRepo.Path
$PyProject = Join-Path $RepoRoot "pyproject.toml"
$PackageDir = Join-Path $RepoRoot "mvp_qaic_py"
if (-not (Test-Path -LiteralPath $PyProject)) { Fail "pyproject.toml not found" }
if (-not (Test-Path -LiteralPath $PackageDir)) { Fail "mvp_qaic_py package not found" }

Set-Location -LiteralPath $RepoRoot

$PythonExe = (Get-Command python.exe -ErrorAction Stop).Source
$ExportsDir = Join-Path $RepoRoot "05_EXPORTS"
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"

$P124Dir = Join-Path $ExportsDir ("P127_RUN_P124_INPUT_" + $Stamp)
$P125Dir = Join-Path $ExportsDir ("P127_RUN_P125_REVIEW_" + $Stamp)
$P126Dir = Join-Path $ExportsDir ("P127_RUN_P126_REGISTRY_" + $Stamp)

[System.IO.Directory]::CreateDirectory($P124Dir) | Out-Null
[System.IO.Directory]::CreateDirectory($P125Dir) | Out-Null
[System.IO.Directory]::CreateDirectory($P126Dir) | Out-Null

$OldPythonPath = $env:PYTHONPATH
$env:PYTHONPATH = $RepoRoot

& $PythonExe -m mvp_qaic_py.gem_loop_input_helper `
  --output-dir $P124Dir `
  --run-id ("P127-P124-" + $Stamp) `
  --generated-at-utc "2026-06-22T00:00:00Z" `
  --notes "P127 shortcut created local P124 input folder. Operator must fill portfolio and GEM response manually."

if ($LASTEXITCODE -ne 0) { Fail "P124 input helper failed" }

Write-Host ""
Write-Host "P124 folder created:"
Write-Host $P124Dir
Write-Host ""
Write-Host "ACTION REQUIRED:"
Write-Host "1. Fill portfolio_input.txt"
Write-Host "2. Run the P118 prompt command from P124_OPERATOR_COMMANDS.md"
Write-Host "3. Paste GEM answer into gem_response.txt"
Write-Host "4. Run P125 and P126 commands below manually."
Write-Host ""
Write-Host "P125 review command:"
Write-Host "python -m mvp_qaic_py.gem_manual_test_review_pack --output-dir `"$P125Dir`" --p124-run-dir `"$P124Dir`" --run-id P127-P125-$Stamp"
Write-Host ""
Write-Host "P126 registry command:"
Write-Host "python -m mvp_qaic_py.daily_run_registry --output-dir `"$P126Dir`" --exports-dir `"$ExportsDir`" --run-id P127-P126-$Stamp"
Write-Host ""
Write-Host "SAFETY: HUMAN_REVIEW_ONLY / NO_SHEET_WRITE / NO_BROKER / NO_ORDER / NO_SIZING / NO_AUTO_APPLY_GEM_RESPONSE / NO_REVOLUTX_REAL_ACCESS_FROM_MVP"

$env:PYTHONPATH = $OldPythonPath
"""


def _one_command_guide() -> str:
    return """
# P127 One Command Operator Guide

Run:

```powershell
& .\\P127_OPERATOR_RUN_SHORTCUT.ps1
```

The shortcut creates a local P124 folder and prints the next P125/P126 commands.

## Manual stop points

1. Fill `portfolio_input.txt` manually.
2. Copy the prompt into GEM manually.
3. Paste the GEM answer into `gem_response.txt` manually.
4. Run P125 review UX.
5. Run P126 registry.

## Safety

- HUMAN_REVIEW_ONLY
- NO_SHEET_WRITE
- NO_AUTO_APPLY_GEM_RESPONSE
- NO_BROKER
- NO_ORDER
- NO_AUTO_SIZING
- NO_REVOLUTX_REAL_ACCESS_FROM_MVP
"""


def _daily_runbook() -> str:
    return """
# P127 Operator Daily Runbook

## Goal

Provide a repeatable local workflow for MVP QAIC daily prompt testing.

## Chain

P124 local input helper -> manual portfolio input -> manual GEM response -> P125 review UX -> P126 registry.

## Allowed

- Local files
- Human review
- Prompt preparation
- Manual GEM copy/paste
- Local registry

## Forbidden

- Apps Script execution
- Sheet write
- clasp push
- public deploy
- broker action
- order/cancel/replace
- sizing
- Revolut X real access from MVP
"""


def _readme() -> str:
    return """
# P127 Shortcut Pack

This pack is a local operator shortcut for the MVP QAIC prompt workflow.

It does not execute trading, does not write Sheets, does not call Apps Script, and does not access Revolut X real accounts from MVP.
"""


def write_operator_run_shortcut_pack(request: OperatorRunShortcutRequest) -> dict[str, Any]:
    out = Path(request.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    shortcut_path = out / "P127_OPERATOR_RUN_SHORTCUT.ps1"
    guide_path = out / "P127_ONE_COMMAND_OPERATOR_GUIDE.md"
    runbook_path = out / "P127_OPERATOR_DAILY_RUNBOOK.md"
    checklist_path = out / "P127_SHORTCUT_CHECKLIST.csv"
    contract_path = out / "P127_SHORTCUT_CONTRACT.json"
    manifest_path = out / "P127_SHORTCUT_MANIFEST.json"
    readme_path = out / "P127_README.md"

    _write(shortcut_path, _shortcut_script())
    _write(guide_path, _one_command_guide())
    _write(runbook_path, _daily_runbook())
    _write_checklist(checklist_path)
    _write_json(contract_path, build_shortcut_contract())
    _write(readme_path, _readme())

    manifest = {
        "status": "OPERATOR_RUN_SHORTCUT_READY",
        "step": "P127_OPERATOR_RUN_SHORTCUT_LOCAL_ONLY",
        "version": VERSION,
        "run_id": request.run_id,
        "generated_at_utc": request.generated_at_utc,
        "output_dir": str(out),
        "file_count": len(OUTPUT_FILES),
        "human_review_only": True,
        "no_sheet_write": True,
        "no_auto_apply_gem_response": True,
        "no_order_no_sizing": True,
        "shortcut_ready": True,
        "safety_markers": list(SAFETY_MARKERS),
        "files": [
            str(shortcut_path),
            str(guide_path),
            str(runbook_path),
            str(checklist_path),
            str(contract_path),
            str(readme_path),
        ],
        "next": "REAL_GEM_TEST_OR_P128_PROMPT_INPUT_IMAGE_CAPTURE_HUMAN_REVIEW",
    }
    _write_json(manifest_path, manifest)
    manifest["files"].append(str(manifest_path))
    return manifest


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.operator_run_shortcut",
        description="Create P127 local operator run shortcut pack.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P127-OPERATOR-RUN-SHORTCUT")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--notes")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_operator_run_shortcut_pack(
        OperatorRunShortcutRequest(
            output_dir=args.output_dir,
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
            notes=args.notes,
        )
    )
    print(result["status"])
    print(result["file_count"])
    print(result["output_dir"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
