from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

VERSION = "MVP_QAIC_P129_IMAGE_TO_PROMPT_MANUAL_TRANSCRIPTION_BRIDGE_0_1_0_SAFE"

SAFETY_MARKERS = (
    "LOCAL_ONLY",
    "IMAGE_TO_PROMPT_BRIDGE_ONLY",
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
    "P129_P124_PORTFOLIO_INPUT_FROM_MANUAL_TRANSCRIPTION.txt",
    "P129_IMAGE_TO_PROMPT_BRIDGE_REPORT.md",
    "P129_MANUAL_TRANSCRIPTION_REVIEW.csv",
    "P129_BRIDGE_CONTRACT.json",
    "P129_BRIDGE_MANIFEST.json",
    "P129_NEXT_ACTIONS.md",
    "P129_README.md",
)

FORBIDDEN_AUTOMATION_TERMS = (
    "ocr extracted",
    "ocr-extracted",
    "automatically extracted",
    "automated extraction",
    "auto extracted",
    "machine extracted",
    "detected automatically",
    "vision extracted",
)


@dataclass(frozen=True)
class ImageManualTranscriptionBridgeRequest:
    output_dir: str | Path
    p128_dir: str | Path | None = None
    manual_transcription_path: str | Path | None = None
    run_id: str = "P129-IMAGE-MANUAL-TRANSCRIPTION-BRIDGE"
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


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8-sig")


def _default_transcription_path(p128_dir: str | Path | None) -> Path | None:
    if not p128_dir:
        return None
    return Path(p128_dir) / "P128_MANUAL_TRANSCRIPTION_TEMPLATE.md"


def _resolve_transcription_path(
    p128_dir: str | Path | None,
    manual_transcription_path: str | Path | None,
) -> Path | None:
    if manual_transcription_path:
        return Path(manual_transcription_path)
    return _default_transcription_path(p128_dir)


def _field_has_value(text: str, prefix: str) -> bool:
    normalized_prefix = prefix.lower()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith(normalized_prefix):
            _, _, value = stripped.partition(":")
            if value.strip():
                return True
    return False


def _has_meaningful_asset_data(text: str) -> bool:
    return (
        _field_has_value(text, "- symbol:")
        and _field_has_value(text, "- quantity:")
        and _field_has_value(text, "- value_eur:")
    )


def _find_forbidden_automation_terms(text: str) -> list[str]:
    lower = text.lower()
    return [term for term in FORBIDDEN_AUTOMATION_TERMS if term in lower]


def _review_rows(text: str, path: Path | None) -> tuple[str, list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    if path is None:
        rows.append(
            {
                "severity": "BLOCKER",
                "code": "MISSING_TRANSCRIPTION_PATH",
                "message": "No manual transcription path was provided.",
            }
        )
        return "BLOCKED_REVIEW_REQUIRED", rows

    if not path.exists():
        rows.append(
            {
                "severity": "BLOCKER",
                "code": "MANUAL_TRANSCRIPTION_FILE_NOT_FOUND",
                "message": str(path),
            }
        )
        return "BLOCKED_REVIEW_REQUIRED", rows

    forbidden = _find_forbidden_automation_terms(text)
    for term in forbidden:
        rows.append(
            {
                "severity": "BLOCKER",
                "code": "FORBIDDEN_AUTOMATION_CLAIM",
                "message": term,
            }
        )
    if forbidden:
        return "BLOCKED_REVIEW_REQUIRED", rows

    if not _has_meaningful_asset_data(text):
        rows.append(
            {
                "severity": "MISSING_DATA",
                "code": "MANUAL_TRANSCRIPTION_PENDING",
                "message": "Fill symbol, quantity, and value_eur manually before using the P124 input.",
            }
        )
        return "MANUAL_TRANSCRIPTION_PENDING", rows

    rows.append(
        {
            "severity": "OK",
            "code": "P124_PORTFOLIO_INPUT_READY",
            "message": "Manual transcription contains symbol, quantity, and value_eur fields.",
        }
    )
    return "P124_PORTFOLIO_INPUT_READY", rows


def _write_review_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = ["severity", "code", "message"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _p124_input_text(transcription_text: str, status: str) -> str:
    return (
        "# P129 P124 Portfolio Input From Manual Image Transcription\n\n"
        "Status: " + status + "\n\n"
        "Safety:\n"
        "- HUMAN_REVIEW_ONLY\n"
        "- MANUAL_TRANSCRIPTION_REQUIRED\n"
        "- NO_OCR_CLAIM\n"
        "- NO_AUTOMATED_VISUAL_EXTRACTION\n"
        "- NO_INVENTED_PORTFOLIO_DATA\n"
        "- NO_BROKER\n"
        "- NO_ORDER\n"
        "- NO_SIZING\n"
        "- NO_AUTO_APPLY_GEM_RESPONSE\n\n"
        "Use this text as P124 `portfolio_input.txt` only after human review.\n\n"
        "## Manual transcription payload\n\n" + transcription_text.strip() + "\n"
    )


def build_bridge_contract() -> dict[str, Any]:
    return {
        "contract": "P129_IMAGE_TO_PROMPT_MANUAL_TRANSCRIPTION_BRIDGE",
        "version": VERSION,
        "status": "BRIDGE_CONTRACT_READY",
        "purpose": "Transform a manually filled P128 transcription file into P124-compatible portfolio input.",
        "allowed": [
            "read local manual transcription text",
            "write local P124-compatible input text",
            "write review CSV",
            "write manifest and next actions",
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


def _report(status: str, rows: list[dict[str, str]], transcription_path: Path | None) -> str:
    lines = [
        "# P129 Image To Prompt Manual Transcription Bridge Report",
        "",
        f"- status: `{status}`",
        f"- manual_transcription_path: `{transcription_path or ''}`",
        "- human_review_only: `true`",
        "- manual_transcription_required: `true`",
        "- no_ocr_claim: `true`",
        "- no_automated_visual_extraction: `true`",
        "- no_invented_portfolio_data: `true`",
        "- no_sheet_write: `true`",
        "",
        "## Review rows",
        "",
    ]
    for row in rows:
        lines.append(f"- {row['severity']} | {row['code']} | {row['message']}")
    return "\n".join(lines)


def _next_actions(status: str) -> str:
    if status == "P124_PORTFOLIO_INPUT_READY":
        action = "Copy `P129_P124_PORTFOLIO_INPUT_FROM_MANUAL_TRANSCRIPTION.txt` into a P124 run folder as `portfolio_input.txt`, then run the GEM prompt flow."
    elif status == "MANUAL_TRANSCRIPTION_PENDING":
        action = "Fill `P128_MANUAL_TRANSCRIPTION_TEMPLATE.md` manually with symbol, quantity, and value_eur, then rerun P129."
    else:
        action = "Resolve blockers in `P129_MANUAL_TRANSCRIPTION_REVIEW.csv`, then rerun P129."
    return (
        "# P129 Next Actions\n\n"
        f"- bridge_status: `{status}`\n"
        f"- next_action: {action}\n\n"
        "Safety: HUMAN_REVIEW_ONLY, NO_OCR_CLAIM, NO_AUTOMATED_VISUAL_EXTRACTION, NO_INVENTED_PORTFOLIO_DATA, NO_SHEET_WRITE, NO_BROKER, NO_ORDER, NO_SIZING.\n"
    )


def _readme() -> str:
    return """
# P129 Image To Prompt Manual Transcription Bridge

P129 bridges P128 manual transcription into a P124-compatible portfolio input file.

It does not OCR images.
It does not automatically extract visual data.
It does not invent portfolio quantities, prices, values, or balances.
"""


def write_image_manual_transcription_bridge(
    request: ImageManualTranscriptionBridgeRequest,
) -> dict[str, Any]:
    out = Path(request.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    transcription_path = _resolve_transcription_path(
        request.p128_dir,
        request.manual_transcription_path,
    )
    transcription_text = _read_text(transcription_path) if transcription_path else ""
    status, review_rows = _review_rows(transcription_text, transcription_path)

    p124_input_path = out / "P129_P124_PORTFOLIO_INPUT_FROM_MANUAL_TRANSCRIPTION.txt"
    report_path = out / "P129_IMAGE_TO_PROMPT_BRIDGE_REPORT.md"
    review_csv_path = out / "P129_MANUAL_TRANSCRIPTION_REVIEW.csv"
    contract_path = out / "P129_BRIDGE_CONTRACT.json"
    manifest_path = out / "P129_BRIDGE_MANIFEST.json"
    next_actions_path = out / "P129_NEXT_ACTIONS.md"
    readme_path = out / "P129_README.md"

    _write(p124_input_path, _p124_input_text(transcription_text, status))
    _write(report_path, _report(status, review_rows, transcription_path))
    _write_review_csv(review_csv_path, review_rows)
    _write_json(contract_path, build_bridge_contract())
    _write(next_actions_path, _next_actions(status))
    _write(readme_path, _readme())

    blocker_count = len([row for row in review_rows if row["severity"] == "BLOCKER"])
    missing_data_count = len([row for row in review_rows if row["severity"] == "MISSING_DATA"])

    manifest = {
        "status": status,
        "step": "P129_IMAGE_TO_PROMPT_MANUAL_TRANSCRIPTION_BRIDGE",
        "version": VERSION,
        "run_id": request.run_id,
        "generated_at_utc": request.generated_at_utc,
        "output_dir": str(out),
        "p128_dir": str(request.p128_dir) if request.p128_dir else None,
        "manual_transcription_path": str(transcription_path) if transcription_path else None,
        "p124_input_path": str(p124_input_path),
        "p124_input_ready": status == "P124_PORTFOLIO_INPUT_READY",
        "review_row_count": len(review_rows),
        "blocker_count": blocker_count,
        "missing_data_count": missing_data_count,
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
            str(p124_input_path),
            str(report_path),
            str(review_csv_path),
            str(contract_path),
            str(next_actions_path),
            str(readme_path),
        ],
        "next": "REAL_IMAGE_TRANSCRIPTION_TEST_OR_P130_OPERATOR_E2E_IMAGE_PROMPT_LOOP",
    }
    _write_json(manifest_path, manifest)
    manifest["files"].append(str(manifest_path))
    return manifest


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.image_manual_transcription_bridge",
        description="Create P129 bridge from P128 manual transcription to P124 portfolio input.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--p128-dir")
    parser.add_argument("--manual-transcription-path")
    parser.add_argument("--run-id", default="P129-IMAGE-MANUAL-TRANSCRIPTION-BRIDGE")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--notes")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_image_manual_transcription_bridge(
        ImageManualTranscriptionBridgeRequest(
            output_dir=args.output_dir,
            p128_dir=args.p128_dir,
            manual_transcription_path=args.manual_transcription_path,
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
            notes=args.notes,
        )
    )
    print(result["status"])
    print(result["p124_input_ready"])
    print(result["blocker_count"])
    print(result["missing_data_count"])
    print(result["output_dir"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
