from __future__ import annotations

import argparse
import csv
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from mvp_qaic_py.image_manual_transcription_bridge import (
    ImageManualTranscriptionBridgeRequest,
    discover_latest_p128_dir,
    write_image_manual_transcription_bridge,
)

VERSION = "MVP_QAIC_P130_OPERATOR_E2E_IMAGE_PROMPT_LOOP_0_1_0_SAFE"

SAFETY_MARKERS = (
    "LOCAL_ONLY",
    "OPERATOR_E2E_LOOP_ONLY",
    "HUMAN_REVIEW_ONLY",
    "MANUAL_TRANSCRIPTION_REQUIRED",
    "NO_OCR_CLAIM",
    "NO_AUTOMATED_VISUAL_EXTRACTION",
    "NO_INVENTED_PORTFOLIO_DATA",
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
    "P130_E2E_OPERATOR_GUIDE.md",
    "P130_OPERATOR_COMMANDS.md",
    "P130_E2E_CHECKLIST.csv",
    "P130_E2E_CONTRACT.json",
    "P130_E2E_MANIFEST.json",
    "P130_README.md",
    "P130_P124_HANDOFF/portfolio_input.txt",
    "P130_P124_HANDOFF/gem_response.txt",
    "P130_P124_HANDOFF/run_notes.md",
)


@dataclass(frozen=True)
class OperatorE2EImagePromptLoopRequest:
    output_dir: str | Path
    exports_dir: str | Path | None = None
    p128_dir: str | Path | None = None
    manual_transcription_path: str | Path | None = None
    run_id: str = "P130-OPERATOR-E2E-IMAGE-PROMPT-LOOP"
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


def _resolve_p128_dir(
    p128_dir: str | Path | None,
    exports_dir: str | Path | None,
) -> Path | None:
    if p128_dir:
        return Path(p128_dir)
    if exports_dir:
        return discover_latest_p128_dir(exports_dir)
    return None


def _status_from_p129(p129_status: str) -> str:
    if p129_status == "P124_PORTFOLIO_INPUT_READY":
        return "E2E_READY_FOR_GEM_COPY_PASTE"
    if p129_status == "MANUAL_TRANSCRIPTION_PENDING":
        return "E2E_WAITING_FOR_MANUAL_TRANSCRIPTION"
    return "E2E_BLOCKED_REVIEW_REQUIRED"


def _write_checklist(path: Path, status: str) -> None:
    rows = [
        ("1", "P128 image capture folder exists", "YES", "LOCAL_ONLY", "READY"),
        (
            "2",
            "P129 bridge generated P124-compatible input",
            "YES",
            "MANUAL_TRANSCRIPTION_REQUIRED",
            status,
        ),
        ("3", "Copy/paste prompt to GEM manually", "YES", "HUMAN_REVIEW_ONLY", "OPERATOR_ACTION"),
        (
            "4",
            "Paste GEM response into gem_response.txt",
            "YES",
            "NO_AUTO_APPLY_GEM_RESPONSE",
            "OPERATOR_ACTION",
        ),
        ("5", "Run P125 review UX", "YES", "NO_SHEET_WRITE", "READY"),
        ("6", "Run P126 daily registry", "YES", "LOCAL_REGISTRY_ONLY", "READY"),
    ]
    fields = ["step", "name", "required", "safety", "status"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for step, name, required, safety, row_status in rows:
            writer.writerow(
                {
                    "step": step,
                    "name": name,
                    "required": required,
                    "safety": safety,
                    "status": row_status,
                }
            )


def build_e2e_contract() -> dict[str, Any]:
    return {
        "contract": "P130_OPERATOR_E2E_IMAGE_PROMPT_LOOP",
        "version": VERSION,
        "status": "E2E_CONTRACT_READY",
        "purpose": "Create a local operator handoff from P128 image/manual transcription to P129 bridge, P124 input, P125 review, and P126 registry.",
        "allowed": [
            "discover latest local P128 export folder",
            "run local P129 bridge",
            "write P124-compatible portfolio_input.txt",
            "write gem_response.txt placeholder",
            "write operator commands for P125 and P126",
            "write local manifest",
        ],
        "forbidden": [
            "ocr_claim",
            "automated_visual_extraction",
            "invented_portfolio_data",
            "apps_script_execution",
            "sheet_write",
            "clasp_push",
            "public_deploy",
            "broker_execution",
            "order_execution",
            "auto_sizing",
            "auto_apply_gem_response",
            "revolutx_real_access_from_mvp",
        ],
        "manual_transcription_required": True,
        "no_ocr_claim": True,
        "no_automated_visual_extraction": True,
        "no_invented_portfolio_data": True,
        "safety_markers": list(SAFETY_MARKERS),
        "outputs": list(OUTPUT_FILES),
    }


def _operator_guide(status: str, p128_dir: Path | None) -> str:
    return f"""
# P130 Operator E2E Image Prompt Loop

## Status

`{status}`

## Source P128

`{p128_dir or ""}`

## Loop

P128 image/manual transcription
-> P129-R1 bridge
-> P124 portfolio input handoff
-> manual GEM copy/paste
-> P125 review UX
-> P126 registry

## Important

P130 does not run GEM automatically.
P130 does not OCR images.
P130 does not extract image content automatically.
P130 does not invent quantities, values, prices, balances, or broker information.
P130 does not write Sheets, run Apps Script, call brokers, place orders, or size positions.
"""


def _operator_commands(
    p124_dir: Path, p125_dir: Path, p126_dir: Path, exports_dir: Path | None
) -> str:
    exports_text = str(exports_dir) if exports_dir else "<MVP_QAIC_PY>\\05_EXPORTS"
    return f"""
# P130 Operator Commands

## Step 1 — Check P124 handoff

Open:

```text
{p124_dir}
```

Use `portfolio_input.txt` as the portfolio input for the manual GEM prompt flow.

## Step 2 — Paste GEM answer

Paste the GEM answer into:

```text
{p124_dir / "gem_response.txt"}
```

## Step 3 — Run P125 review UX

```powershell
python -m mvp_qaic_py.gem_manual_test_review_pack --output-dir "{p125_dir}" --p124-run-dir "{p124_dir}" --run-id P130-P125
```

## Step 4 — Run P126 registry

```powershell
python -m mvp_qaic_py.daily_run_registry --output-dir "{p126_dir}" --exports-dir "{exports_text}" --run-id P130-P126
```

## Safety

HUMAN_REVIEW_ONLY / NO_OCR_CLAIM / NO_AUTOMATED_VISUAL_EXTRACTION / NO_INVENTED_PORTFOLIO_DATA / NO_SHEET_WRITE / NO_BROKER / NO_ORDER / NO_SIZING / NO_AUTO_APPLY_GEM_RESPONSE.
"""


def _run_notes(status: str) -> str:
    return f"""
# P130 P124 Handoff Run Notes

status: {status}

Fill or review this folder manually before any GEM prompt use.

Safety:
- HUMAN_REVIEW_ONLY
- MANUAL_TRANSCRIPTION_REQUIRED
- NO_OCR_CLAIM
- NO_AUTOMATED_VISUAL_EXTRACTION
- NO_INVENTED_PORTFOLIO_DATA
- NO_BROKER
- NO_ORDER
- NO_SIZING
- NO_AUTO_APPLY_GEM_RESPONSE
"""


def _readme() -> str:
    return """
# P130 Operator E2E Image Prompt Loop

P130 creates a local handoff chain from P128/P129 to P124/P125/P126.

It is not a live execution loop.
It is not an OCR pipeline.
It is not a broker pipeline.
It is a human-review operator workflow.
"""


def write_operator_e2e_image_prompt_loop(
    request: OperatorE2EImagePromptLoopRequest,
) -> dict[str, Any]:
    out = Path(request.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    exports_dir = Path(request.exports_dir) if request.exports_dir else None
    p128_dir = _resolve_p128_dir(request.p128_dir, exports_dir)

    p129_dir = out / "P130_P129_BRIDGE"
    p124_dir = out / "P130_P124_HANDOFF"
    p125_dir = out / "P130_P125_REVIEW_OUTBOX"
    p126_dir = out / "P130_P126_REGISTRY_OUTBOX"
    p124_dir.mkdir(parents=True, exist_ok=True)
    p125_dir.mkdir(parents=True, exist_ok=True)
    p126_dir.mkdir(parents=True, exist_ok=True)

    p129_result = write_image_manual_transcription_bridge(
        ImageManualTranscriptionBridgeRequest(
            output_dir=p129_dir,
            p128_dir=p128_dir,
            manual_transcription_path=request.manual_transcription_path,
            exports_dir=exports_dir,
            run_id=f"{request.run_id}-P129",
            generated_at_utc=request.generated_at_utc,
            notes=request.notes,
        )
    )

    e2e_status = _status_from_p129(str(p129_result["status"]))
    p129_p124_input = Path(str(p129_result["p124_input_path"]))
    p124_input = p124_dir / "portfolio_input.txt"
    if p129_p124_input.exists():
        shutil.copyfile(p129_p124_input, p124_input)
    else:
        _write(p124_input, _run_notes("E2E_BLOCKED_REVIEW_REQUIRED"))

    gem_response = p124_dir / "gem_response.txt"
    run_notes = p124_dir / "run_notes.md"
    _write(gem_response, "# Paste GEM response here manually.\n")
    _write(run_notes, _run_notes(e2e_status))

    guide_path = out / "P130_E2E_OPERATOR_GUIDE.md"
    commands_path = out / "P130_OPERATOR_COMMANDS.md"
    checklist_path = out / "P130_E2E_CHECKLIST.csv"
    contract_path = out / "P130_E2E_CONTRACT.json"
    manifest_path = out / "P130_E2E_MANIFEST.json"
    readme_path = out / "P130_README.md"

    _write(guide_path, _operator_guide(e2e_status, p128_dir))
    _write(commands_path, _operator_commands(p124_dir, p125_dir, p126_dir, exports_dir))
    _write_checklist(checklist_path, e2e_status)
    _write_json(contract_path, build_e2e_contract())
    _write(readme_path, _readme())

    manifest = {
        "status": e2e_status,
        "step": "P130_OPERATOR_E2E_IMAGE_PROMPT_LOOP",
        "version": VERSION,
        "run_id": request.run_id,
        "generated_at_utc": request.generated_at_utc,
        "output_dir": str(out),
        "exports_dir": str(exports_dir) if exports_dir else None,
        "p128_dir": str(p128_dir) if p128_dir else None,
        "p128_dir_valid": bool(p128_dir and str(p128_dir) != "G" and p128_dir.exists()),
        "p129_bridge_dir": str(p129_dir),
        "p129_status": p129_result["status"],
        "p129_blocker_count": p129_result["blocker_count"],
        "p129_missing_data_count": p129_result["missing_data_count"],
        "p124_handoff_dir": str(p124_dir),
        "p124_portfolio_input_path": str(p124_input),
        "gem_response_path": str(gem_response),
        "p125_review_outbox": str(p125_dir),
        "p126_registry_outbox": str(p126_dir),
        "e2e_ready_for_gem": e2e_status == "E2E_READY_FOR_GEM_COPY_PASTE",
        "waiting_for_manual_transcription": e2e_status == "E2E_WAITING_FOR_MANUAL_TRANSCRIPTION",
        "human_review_only": True,
        "manual_transcription_required": True,
        "no_ocr_claim": True,
        "no_automated_visual_extraction": True,
        "no_invented_portfolio_data": True,
        "no_sheet_write": True,
        "no_auto_apply_gem_response": True,
        "no_order_no_sizing": True,
        "safety_markers": list(SAFETY_MARKERS),
        "files": [
            str(guide_path),
            str(commands_path),
            str(checklist_path),
            str(contract_path),
            str(readme_path),
            str(p124_input),
            str(gem_response),
            str(run_notes),
        ],
        "next": "P131_REAL_IMAGE_TRANSCRIPTION_OPERATOR_TEST",
    }
    _write_json(manifest_path, manifest)
    manifest["files"].append(str(manifest_path))
    return manifest


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.operator_e2e_image_prompt_loop",
        description="Create P130 local operator E2E image prompt loop handoff.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--exports-dir")
    parser.add_argument("--p128-dir")
    parser.add_argument("--manual-transcription-path")
    parser.add_argument("--run-id", default="P130-OPERATOR-E2E-IMAGE-PROMPT-LOOP")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--notes")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_operator_e2e_image_prompt_loop(
        OperatorE2EImagePromptLoopRequest(
            output_dir=args.output_dir,
            exports_dir=args.exports_dir,
            p128_dir=args.p128_dir,
            manual_transcription_path=args.manual_transcription_path,
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
            notes=args.notes,
        )
    )
    print(result["status"])
    print(result["e2e_ready_for_gem"])
    print(result["waiting_for_manual_transcription"])
    print(result["p128_dir_valid"])
    print(result["output_dir"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
