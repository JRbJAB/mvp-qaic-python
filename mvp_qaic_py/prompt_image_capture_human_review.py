from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

VERSION = "MVP_QAIC_P128_PROMPT_INPUT_IMAGE_CAPTURE_HUMAN_REVIEW_0_1_0_SAFE"

SAFETY_MARKERS = (
    "LOCAL_ONLY",
    "IMAGE_CAPTURE_ONLY",
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
    "P128_IMAGE_CAPTURE_GUIDE.md",
    "P128_OPERATOR_VISUAL_NOTES_TEMPLATE.md",
    "P128_MANUAL_TRANSCRIPTION_TEMPLATE.md",
    "P128_IMAGE_CAPTURE_CHECKLIST.csv",
    "P128_IMAGE_INPUT_CONTRACT.json",
    "P128_IMAGE_CAPTURE_MANIFEST.json",
    "P128_README.md",
    "P128_IMAGE_CAPTURE_INBOX/README.md",
    "P128_IMAGE_CAPTURE_INBOX/.gitkeep",
)

ALLOWED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff")


@dataclass(frozen=True)
class PromptImageCaptureRequest:
    output_dir: str | Path
    run_id: str = "P128-PROMPT-IMAGE-CAPTURE"
    generated_at_utc: str | None = None
    image_path: str | Path | None = None
    image_label: str = "portfolio_screenshot_or_image"
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
        (
            "1",
            "Place screenshot/image in P128_IMAGE_CAPTURE_INBOX",
            "YES",
            "LOCAL_ONLY",
            "OPERATOR_ACTION",
        ),
        ("2", "Write visual notes manually", "YES", "HUMAN_REVIEW_ONLY", "OPERATOR_ACTION"),
        (
            "3",
            "Transcribe portfolio data manually",
            "YES",
            "MANUAL_TRANSCRIPTION_REQUIRED",
            "OPERATOR_ACTION",
        ),
        ("4", "Do not claim OCR or automated extraction", "YES", "NO_OCR_CLAIM", "READY"),
        (
            "5",
            "Do not invent missing portfolio values",
            "YES",
            "NO_INVENTED_PORTFOLIO_DATA",
            "READY",
        ),
        (
            "6",
            "Use manual transcription as P124 portfolio input",
            "YES",
            "NO_AUTO_APPLY_GEM_RESPONSE",
            "READY",
        ),
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


def _image_path_info(image_path: str | Path | None) -> dict[str, Any]:
    if not image_path:
        return {
            "image_path": None,
            "image_exists": False,
            "image_extension_allowed": False,
            "image_registered_only": False,
        }
    path = Path(image_path)
    exists = path.exists()
    suffix_allowed = path.suffix.lower() in ALLOWED_IMAGE_EXTENSIONS
    return {
        "image_path": str(path),
        "image_exists": exists,
        "image_extension_allowed": suffix_allowed,
        "image_registered_only": True,
    }


def build_image_input_contract() -> dict[str, Any]:
    return {
        "contract": "P128_PROMPT_INPUT_IMAGE_CAPTURE_HUMAN_REVIEW",
        "version": VERSION,
        "status": "IMAGE_CAPTURE_CONTRACT_READY",
        "purpose": "Prepare local capture folder and manual transcription templates for portfolio screenshots/images.",
        "allowed": [
            "register local image path",
            "store image in local inbox",
            "write human visual notes",
            "write manual transcription",
            "use manual transcription as P124 portfolio input",
        ],
        "forbidden": [
            "ocr_claim",
            "automated_visual_extraction",
            "invented_portfolio_data",
            "auto_apply_gem_response",
            "apps_script_execution",
            "sheet_write",
            "clasp_push",
            "public_deploy",
            "broker_execution",
            "order_execution",
            "auto_sizing",
            "revolutx_real_access_from_mvp",
        ],
        "manual_transcription_required": True,
        "no_ocr_claim": True,
        "no_automated_visual_extraction": True,
        "safety_markers": list(SAFETY_MARKERS),
        "outputs": list(OUTPUT_FILES),
    }


def _guide() -> str:
    return """
# P128 Image Capture Guide

## Goal

Prepare a local folder for portfolio screenshots/images before creating a GEM prompt.

## Workflow

1. Put the screenshot/image in `P128_IMAGE_CAPTURE_INBOX`.
2. Fill `P128_OPERATOR_VISUAL_NOTES_TEMPLATE.md`.
3. Fill `P128_MANUAL_TRANSCRIPTION_TEMPLATE.md`.
4. Copy only the manual transcription into P124 `portfolio_input.txt`.

## Hard boundary

P128 does not perform OCR.
P128 does not claim automated visual extraction.
P128 does not infer missing quantities, prices, portfolio values, or broker balances.
P128 does not write Sheets, run Apps Script, call brokers, place orders, or size positions.

## Required markers

- MANUAL_TRANSCRIPTION_REQUIRED
- NO_OCR_CLAIM
- NO_AUTOMATED_VISUAL_EXTRACTION
- NO_INVENTED_PORTFOLIO_DATA
- HUMAN_REVIEW_ONLY
"""


def _visual_notes_template() -> str:
    return """
# P128 Operator Visual Notes Template

image_file_name:
image_source:
capture_datetime_local:
portfolio_platform_visible:
assets_visible:
values_visible:
unclear_elements:
manual_review_notes:

Safety:
- HUMAN_REVIEW_ONLY
- NO_OCR_CLAIM
- NO_AUTOMATED_VISUAL_EXTRACTION
- NO_INVENTED_PORTFOLIO_DATA
"""


def _manual_transcription_template() -> str:
    return """
# P128 Manual Transcription Template

Copy this manually into P124 `portfolio_input.txt` after human review.

## Portfolio screenshot transcription

source_image_file:
transcribed_by:
transcription_datetime_local:
confidence: REVIEW

## Assets

ASSET_1:
- symbol:
- quantity:
- value_eur:
- source: manual_image_transcription
- confidence: REVIEW
- notes:

ASSET_2:
- symbol:
- quantity:
- value_eur:
- source: manual_image_transcription
- confidence: REVIEW
- notes:

## Missing / unclear data

- missing_current_prices:
- missing_timestamp:
- unclear_rows:

## Safety

HUMAN_REVIEW_ONLY
MANUAL_TRANSCRIPTION_REQUIRED
NO_OCR_CLAIM
NO_AUTOMATED_VISUAL_EXTRACTION
NO_INVENTED_PORTFOLIO_DATA
NO_BROKER
NO_ORDER
NO_SIZING
"""


def _readme() -> str:
    return """
# P128 Prompt Input Image Capture

This pack supports portfolio screenshot/image capture for manual prompt preparation.

It only creates a local inbox and human-review transcription templates.
No OCR is performed or claimed.
No automatic visual extraction is performed.
No portfolio data is invented.
"""


def _inbox_readme() -> str:
    return """
# P128 Image Capture Inbox

Place portfolio screenshots/images here.

Allowed extensions:
.png, .jpg, .jpeg, .webp, .gif, .bmp, .tif, .tiff

Do not assume values from the image automatically.
Use the manual transcription template.
"""


def write_prompt_image_capture_pack(request: PromptImageCaptureRequest) -> dict[str, Any]:
    out = Path(request.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    inbox = out / "P128_IMAGE_CAPTURE_INBOX"
    inbox.mkdir(parents=True, exist_ok=True)

    guide_path = out / "P128_IMAGE_CAPTURE_GUIDE.md"
    visual_notes_path = out / "P128_OPERATOR_VISUAL_NOTES_TEMPLATE.md"
    transcription_path = out / "P128_MANUAL_TRANSCRIPTION_TEMPLATE.md"
    checklist_path = out / "P128_IMAGE_CAPTURE_CHECKLIST.csv"
    contract_path = out / "P128_IMAGE_INPUT_CONTRACT.json"
    manifest_path = out / "P128_IMAGE_CAPTURE_MANIFEST.json"
    readme_path = out / "P128_README.md"
    inbox_readme_path = inbox / "README.md"
    gitkeep_path = inbox / ".gitkeep"

    _write(guide_path, _guide())
    _write(visual_notes_path, _visual_notes_template())
    _write(transcription_path, _manual_transcription_template())
    _write_checklist(checklist_path)
    _write_json(contract_path, build_image_input_contract())
    _write(readme_path, _readme())
    _write(inbox_readme_path, _inbox_readme())
    _write(gitkeep_path, "")

    image_info = _image_path_info(request.image_path)

    manifest = {
        "status": "IMAGE_CAPTURE_HUMAN_REVIEW_READY",
        "step": "P128_PROMPT_INPUT_IMAGE_CAPTURE_HUMAN_REVIEW",
        "version": VERSION,
        "run_id": request.run_id,
        "generated_at_utc": request.generated_at_utc,
        "output_dir": str(out),
        "image_capture_folder": str(inbox),
        "image_label": request.image_label,
        "image_path": image_info["image_path"],
        "image_exists": image_info["image_exists"],
        "image_extension_allowed": image_info["image_extension_allowed"],
        "image_registered_only": image_info["image_registered_only"],
        "manual_transcription_required": True,
        "no_ocr_claim": True,
        "no_automated_visual_extraction": True,
        "no_invented_portfolio_data": True,
        "human_review_only": True,
        "no_sheet_write": True,
        "no_auto_apply_gem_response": True,
        "no_order_no_sizing": True,
        "safety_markers": list(SAFETY_MARKERS),
        "files": [
            str(guide_path),
            str(visual_notes_path),
            str(transcription_path),
            str(checklist_path),
            str(contract_path),
            str(readme_path),
            str(inbox_readme_path),
            str(gitkeep_path),
        ],
        "next": "P129_IMAGE_TO_PROMPT_MANUAL_TRANSCRIPTION_BRIDGE_OR_REAL_GEM_TEST",
    }
    _write_json(manifest_path, manifest)
    manifest["files"].append(str(manifest_path))
    return manifest


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.prompt_image_capture_human_review",
        description="Create P128 local portfolio screenshot/image capture pack for human-review transcription.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P128-PROMPT-IMAGE-CAPTURE")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--image-path")
    parser.add_argument("--image-label", default="portfolio_screenshot_or_image")
    parser.add_argument("--notes")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_prompt_image_capture_pack(
        PromptImageCaptureRequest(
            output_dir=args.output_dir,
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
            image_path=args.image_path,
            image_label=args.image_label,
            notes=args.notes,
        )
    )
    print(result["status"])
    print(result["manual_transcription_required"])
    print(result["no_ocr_claim"])
    print(result["no_automated_visual_extraction"])
    print(result["output_dir"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
