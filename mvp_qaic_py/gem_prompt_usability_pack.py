from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from .gem_prompt_runtime_cli import GemRuntimeRequest, write_runtime_pack

VERSION = "MVP_QAIC_P117_PROMPT_GEM_RUNTIME_USABILITY_PACK_0_1_0_SAFE"

SAFETY_MARKERS = (
    "MVP_PUBLIC_SCOPE",
    "HUMAN_REVIEW_ONLY",
    "LOCAL_ONLY",
    "COPY_PASTE_TO_GEM_ONLY",
    "NO_INDEX_EDIT",
    "NO_CLASP",
    "NO_APPS_SCRIPT_EXECUTION",
    "NO_SHEET_WRITE",
    "NO_PUBLIC_DEPLOY",
    "NO_BROKER",
    "NO_ORDER",
    "NO_AUTO_SIZING",
    "NO_OCR_CLAIM",
    "NO_AUTOMATED_VISUAL_EXTRACTION",
    "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
)

DEFAULT_SAMPLE_PASTED_TEXT = (
    "BTC 0.10 value EUR 6500; ETH 1.20 value EUR 4200; "
    "USDC 1000 value EUR 920; source=manual sample; prices not verified."
)

DEFAULT_STRUCTURED_PORTFOLIO = {
    "source": "manual_sample",
    "human_review_only": True,
    "positions": [
        {"asset": "BTC", "quantity": "0.10", "value_eur": "6500", "confidence": "manual"},
        {"asset": "ETH", "quantity": "1.20", "value_eur": "4200", "confidence": "manual"},
        {"asset": "USDC", "quantity": "1000", "value_eur": "920", "confidence": "manual"},
    ],
    "notes": "Sample only. Do not infer live price, PnL, broker state, order, or sizing.",
}


def build_usability_contract() -> dict[str, Any]:
    return {
        "contract": "P117_PROMPT_GEM_RUNTIME_USABILITY_PACK",
        "version": VERSION,
        "status": "LOCAL_ONLY_READY_FOR_OPERATOR_REVIEW",
        "purpose": "Make P116 GEM prompt runtime usable for daily manual portfolio reviews.",
        "primary_command": "python -m mvp_qaic_py.gem_prompt_runtime_cli",
        "recommended_input_modes": [
            "PASTED_TEXT_DRAFT",
            "IMAGE_REVIEW_REQUIRED",
            "STRUCTURED",
        ],
        "forbidden": [
            "ocr_claim",
            "automated_visual_extraction",
            "apps_script_execution",
            "sheet_write",
            "clasp_push",
            "public_deploy",
            "broker_execution",
            "order_execution",
            "auto_sizing",
            "revolutx_real_access_from_mvp",
            "secret_logging",
        ],
        "safety_markers": list(SAFETY_MARKERS),
    }


def build_cli_commands() -> dict[str, str]:
    return {
        "pasted_text_file": (
            "python -m mvp_qaic_py.gem_prompt_runtime_cli "
            '--output-dir "05_EXPORTS/GEM_RUN_PASTED_TEXT" '
            "--input-mode PASTED_TEXT_DRAFT "
            '--pasted-text-file "portfolio_input.txt" '
            '--notes "Manual pasted portfolio review. Human review only." '
            '--run-id "MANUAL-GEM-RUN"'
        ),
        "image_review_required": (
            "python -m mvp_qaic_py.gem_prompt_runtime_cli "
            '--output-dir "05_EXPORTS/GEM_RUN_IMAGE_REVIEW" '
            "--input-mode IMAGE_REVIEW_REQUIRED "
            '--image-reference "portfolio_capture.png" '
            '--notes "Image reference only. No OCR claim. Human review required." '
            '--run-id "MANUAL-IMAGE-REVIEW"'
        ),
        "structured_json": (
            "python -m mvp_qaic_py.gem_prompt_runtime_cli "
            '--output-dir "05_EXPORTS/GEM_RUN_STRUCTURED" '
            "--input-mode STRUCTURED "
            '--structured-json-file "portfolio_structured.json" '
            '--notes "Structured manual input. Human review only." '
            '--run-id "MANUAL-STRUCTURED-REVIEW"'
        ),
    }


def build_operator_checklist() -> list[str]:
    return [
        "Confirm the input source: pasted text, screenshot reference, or structured JSON.",
        "Never claim OCR or automated visual extraction from screenshots.",
        "Confirm this remains a human review workflow before copying the prompt to GEM.",
        "Copy P116_GEM_PROMPT_COPY_PASTE.md manually into GEM.",
        "Verify assets, quantities, values, and dates before trusting any review.",
        "If critical data is missing, keep decision_status=REVIEW_REQUIRED.",
        "Never place, prepare, size, cancel, or replace orders from MVP.",
        "Keep Revolut X and broker execution in the separate private QAIC backend.",
        "Archive the generated runtime pack before using the result as evidence.",
    ]


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _quickstart_markdown() -> str:
    commands = build_cli_commands()
    return "\n".join(
        [
            "# P117 Prompt GEM Runtime Quickstart",
            "",
            "## Goal",
            "",
            "Generate a local GEM prompt pack for manual crypto portfolio review.",
            "",
            "## Fast path",
            "",
            "1. Put your portfolio text in `portfolio_input.txt`, or keep a screenshot reference path.",
            "2. Run one of the commands below.",
            "3. Open `P116_GEM_PROMPT_COPY_PASTE.md`.",
            "4. Copy it manually into GEM.",
            "5. Paste GEM output into the next review/journal workflow.",
            "",
            "## Commands",
            "",
            "### Pasted text file",
            "",
            "```powershell",
            commands["pasted_text_file"],
            "```",
            "",
            "### Screenshot / image reference",
            "",
            "```powershell",
            commands["image_review_required"],
            "```",
            "",
            "### Structured JSON",
            "",
            "```powershell",
            commands["structured_json"],
            "```",
            "",
            "## Hard safety",
            "",
            "- HUMAN_REVIEW_ONLY.",
            "- NO_OCR_CLAIM.",
            "- NO_BROKER / NO_ORDER / NO_AUTO_SIZING.",
            "- NO_REVOLUTX_REAL_ACCESS_FROM_MVP.",
            "",
        ]
    )


def _commands_markdown() -> str:
    commands = build_cli_commands()
    lines = ["# P117 CLI Commands", ""]
    for name, command in commands.items():
        lines.extend([f"## {name}", "", "```powershell", command, "```", ""])
    return "\n".join(lines)


def _checklist_markdown() -> str:
    lines = ["# P117 Operator Checklist", ""]
    for item in build_operator_checklist():
        lines.append(f"- [ ] {item}")
    lines.append("")
    return "\n".join(lines)


def _report_markdown(output_dir: str, runtime_sample_dir: str) -> str:
    return "\n".join(
        [
            "# P117 Prompt GEM Runtime Usability Pack Report",
            "",
            "- status: EXPORTED",
            f"- version: {VERSION}",
            f"- output_dir: {output_dir}",
            f"- sample_runtime_pack: {runtime_sample_dir}",
            "- safety: HUMAN_REVIEW_ONLY / NO_OCR_CLAIM / NO_BROKER / NO_ORDER / NO_SIZING",
            "",
            "## Recommendation",
            "",
            "Use the pasted-text command first for daily manual tests. Use image mode only as a reference workflow, with human review required.",
            "",
            "## Next",
            "",
            "P118_PROMPT_GEM_DAILY_OPERATOR_SHORTCUT_OR_P117B_REVIEW",
            "",
        ]
    )


def write_usability_pack(
    output_dir: str | Path, *, include_runtime_sample: bool = True
) -> dict[str, Any]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    contract_path = out / "P117_USABILITY_CONTRACT.json"
    quickstart_path = out / "P117_QUICKSTART.md"
    commands_path = out / "P117_CLI_COMMANDS.md"
    checklist_path = out / "P117_OPERATOR_CHECKLIST.md"
    pasted_sample_path = out / "P117_SAMPLE_PASTED_PORTFOLIO.txt"
    structured_sample_path = out / "P117_SAMPLE_STRUCTURED_PORTFOLIO.json"
    report_path = out / "P117_USABILITY_REPORT.md"

    runtime_sample_dir = out / "P117_SAMPLE_RUNTIME_PACK_PASTED_TEXT"

    _write_json(contract_path, build_usability_contract())
    quickstart_path.write_text(_quickstart_markdown(), encoding="utf-8")
    commands_path.write_text(_commands_markdown(), encoding="utf-8")
    checklist_path.write_text(_checklist_markdown(), encoding="utf-8")
    pasted_sample_path.write_text(DEFAULT_SAMPLE_PASTED_TEXT + "\n", encoding="utf-8")
    _write_json(structured_sample_path, DEFAULT_STRUCTURED_PORTFOLIO)

    runtime_result: dict[str, Any] | None = None
    if include_runtime_sample:
        runtime_result = write_runtime_pack(
            runtime_sample_dir,
            GemRuntimeRequest(
                input_mode="PASTED_TEXT_DRAFT",
                pasted_text=DEFAULT_SAMPLE_PASTED_TEXT,
                notes="P117 sample runtime pack. Human review only.",
                run_id="P117-SAMPLE-RUNTIME",
                generated_at_utc="2026-06-22T00:00:00Z",
            ),
        )

    report_path.write_text(_report_markdown(str(out), str(runtime_sample_dir)), encoding="utf-8")

    files = [
        str(contract_path),
        str(quickstart_path),
        str(commands_path),
        str(checklist_path),
        str(pasted_sample_path),
        str(structured_sample_path),
        str(report_path),
    ]
    if runtime_result:
        files.extend(runtime_result["files"])

    return {
        "status": "EXPORTED",
        "step": "P117_PROMPT_GEM_RUNTIME_USABILITY_PACK",
        "version": VERSION,
        "output_dir": str(out),
        "files": files,
        "runtime_sample_dir": str(runtime_sample_dir),
        "safety_markers": list(SAFETY_MARKERS),
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.gem_prompt_usability_pack",
        description="Generate P117 usability pack for the P116 GEM prompt runtime.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--no-runtime-sample", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_usability_pack(
        args.output_dir,
        include_runtime_sample=not args.no_runtime_sample,
    )
    print(result["status"])
    print(result["output_dir"])
    print(result["runtime_sample_dir"])
    for path in result["files"]:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
