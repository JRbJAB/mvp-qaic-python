from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .gem_prompt_runtime_cli import GemRuntimeRequest, write_runtime_pack

VERSION = "MVP_QAIC_P118_PROMPT_GEM_DAILY_OPERATOR_SHORTCUT_0_1_0_SAFE"

SAFETY_MARKERS = (
    "MVP_PUBLIC_SCOPE",
    "HUMAN_REVIEW_ONLY",
    "LOCAL_ONLY",
    "DAILY_OPERATOR_SHORTCUT",
    "COPY_PASTE_TO_GEM_ONLY",
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
    "NO_OCR_CLAIM",
    "NO_AUTOMATED_VISUAL_EXTRACTION",
    "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
)

DEFAULT_PORTFOLIO_INPUT = (
    "BTC 0.10 value EUR 6500; ETH 1.20 value EUR 4200; "
    "USDC 1000 value EUR 920; source=daily_manual_placeholder; "
    "human_review_required=true; prices_not_verified=true."
)


@dataclass(frozen=True)
class DailyShortcutRequest:
    output_dir: str | Path
    pasted_text: str | None = None
    pasted_text_file: str | None = None
    image_reference: str | None = None
    structured_json_file: str | None = None
    notes: str | None = None
    run_id: str = "DAILY-GEM-REVIEW"
    generated_at_utc: str | None = None
    use_default_sample: bool = False


def _read_optional_text(pasted_text: str | None, pasted_text_file: str | None) -> str | None:
    if pasted_text and pasted_text_file:
        raise ValueError("Use either pasted_text or pasted_text_file, not both.")
    if pasted_text_file:
        return Path(pasted_text_file).read_text(encoding="utf-8")
    return pasted_text


def _read_optional_json(path: str | None) -> Mapping[str, Any] | None:
    if not path:
        return None
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("structured_json_file must contain a JSON object.")
    return payload


def resolve_input_mode(request: DailyShortcutRequest) -> str:
    active = [
        bool(request.pasted_text or request.pasted_text_file or request.use_default_sample),
        bool(request.image_reference),
        bool(request.structured_json_file),
    ]
    if sum(active) == 0:
        raise ValueError(
            "Provide pasted text/file, image reference, structured JSON, or --use-default-sample."
        )
    if sum(active) > 1:
        raise ValueError("Use only one input type per daily shortcut run.")

    if request.image_reference:
        return "IMAGE_REVIEW_REQUIRED"
    if request.structured_json_file:
        return "STRUCTURED"
    return "PASTED_TEXT_DRAFT"


def build_daily_contract() -> dict[str, Any]:
    return {
        "contract": "P118_PROMPT_GEM_DAILY_OPERATOR_SHORTCUT",
        "version": VERSION,
        "status": "LOCAL_ONLY_READY_FOR_DAILY_MANUAL_USE",
        "primary_command": "python -m mvp_qaic_py.gem_prompt_daily_shortcut",
        "daily_output": "P118_RUNTIME_PACK/P116_GEM_PROMPT_COPY_PASTE.md",
        "operator_steps": [
            "Put portfolio text in a local input file or provide an image reference.",
            "Run the daily shortcut command.",
            "Open P118_RUNTIME_PACK/P116_GEM_PROMPT_COPY_PASTE.md.",
            "Copy manually into GEM.",
            "Paste GEM response into the next review queue.",
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
            "cancel_order",
            "replace_order",
            "auto_sizing",
            "revolutx_real_access_from_mvp",
            "secret_logging",
        ],
        "safety_markers": list(SAFETY_MARKERS),
    }


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _commands_markdown() -> str:
    return "\n".join(
        [
            "# P118 Daily Operator Shortcut Commands",
            "",
            "## Recommended: pasted text file",
            "",
            "```powershell",
            'python -m mvp_qaic_py.gem_prompt_daily_shortcut --output-dir "05_EXPORTS/DAILY_GEM_REVIEW" --pasted-text-file "portfolio_input.txt" --notes "Daily manual portfolio review. Human review only." --run-id "DAILY-GEM-REVIEW"',
            "```",
            "",
            "## Screenshot reference mode",
            "",
            "```powershell",
            'python -m mvp_qaic_py.gem_prompt_daily_shortcut --output-dir "05_EXPORTS/DAILY_GEM_IMAGE_REVIEW" --image-reference "portfolio_capture.png" --notes "Image reference only. No OCR claim." --run-id "DAILY-GEM-IMAGE-REVIEW"',
            "```",
            "",
            "## Local smoke/sample mode",
            "",
            "```powershell",
            'python -m mvp_qaic_py.gem_prompt_daily_shortcut --output-dir "05_EXPORTS/DAILY_GEM_SAMPLE" --use-default-sample --run-id "DAILY-GEM-SAMPLE"',
            "```",
            "",
        ]
    )


def _operator_shortcut_readme() -> str:
    return "\n".join(
        [
            "# P118 Daily GEM Operator Shortcut",
            "",
            "## What this does",
            "",
            "Creates a daily local runtime pack and a GEM copy-paste prompt.",
            "",
            "## Fast path",
            "",
            "1. Create `portfolio_input.txt` locally.",
            "2. Run the pasted-text command from `P118_DAILY_COMMANDS.md`.",
            "3. Open `P118_RUNTIME_PACK/P116_GEM_PROMPT_COPY_PASTE.md`.",
            "4. Copy it into GEM manually.",
            "5. Save GEM response for P119 response capture/review queue.",
            "",
            "## Safety",
            "",
            "- HUMAN_REVIEW_ONLY.",
            "- NO_OCR_CLAIM.",
            "- NO_BROKER / NO_ORDER / NO_AUTO_SIZING.",
            "- NO_REVOLUTX_REAL_ACCESS_FROM_MVP.",
            "",
        ]
    )


def _report_markdown(result: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "# P118 Daily Operator Shortcut Report",
            "",
            f"- status: {result['status']}",
            f"- version: {VERSION}",
            f"- output_dir: {result['output_dir']}",
            f"- input_mode: {result['input_mode']}",
            f"- runtime_pack_dir: {result['runtime_pack_dir']}",
            "- safety: HUMAN_REVIEW_ONLY / NO_OCR_CLAIM / NO_BROKER / NO_ORDER / NO_SIZING",
            "",
            "## Generated prompt",
            "",
            "`P118_RUNTIME_PACK/P116_GEM_PROMPT_COPY_PASTE.md`",
            "",
            "## Next",
            "",
            "P119_PROMPT_GEM_RESPONSE_CAPTURE_AND_REVIEW_QUEUE",
            "",
        ]
    )


def write_daily_shortcut_pack(request: DailyShortcutRequest) -> dict[str, Any]:
    out = Path(request.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    input_mode = resolve_input_mode(request)
    pasted_text = _read_optional_text(request.pasted_text, request.pasted_text_file)
    structured = _read_optional_json(request.structured_json_file)

    if request.use_default_sample:
        pasted_text = DEFAULT_PORTFOLIO_INPUT

    runtime_dir = out / "P118_RUNTIME_PACK"
    runtime_result = write_runtime_pack(
        runtime_dir,
        GemRuntimeRequest(
            input_mode=input_mode,
            pasted_text=pasted_text,
            structured_portfolio=structured,
            image_reference=request.image_reference,
            notes=request.notes or "P118 daily operator shortcut. Human review only.",
            run_id=request.run_id,
            generated_at_utc=request.generated_at_utc,
        ),
    )

    contract_path = out / "P118_DAILY_CONTRACT.json"
    commands_path = out / "P118_DAILY_COMMANDS.md"
    readme_path = out / "P118_DAILY_README.md"
    sample_input_path = out / "P118_SAMPLE_PORTFOLIO_INPUT.txt"
    manifest_path = out / "P118_DAILY_MANIFEST.json"
    report_path = out / "P118_DAILY_REPORT.md"

    result: dict[str, Any] = {
        "status": "EXPORTED",
        "step": "P118_PROMPT_GEM_DAILY_OPERATOR_SHORTCUT",
        "version": VERSION,
        "output_dir": str(out),
        "input_mode": input_mode,
        "runtime_pack_dir": str(runtime_dir),
        "runtime_prompt": str(runtime_dir / "P116_GEM_PROMPT_COPY_PASTE.md"),
        "files": [],
        "safety_markers": list(SAFETY_MARKERS),
    }

    _write_json(contract_path, build_daily_contract())
    commands_path.write_text(_commands_markdown(), encoding="utf-8")
    readme_path.write_text(_operator_shortcut_readme(), encoding="utf-8")
    sample_input_path.write_text(DEFAULT_PORTFOLIO_INPUT + "\n", encoding="utf-8")
    _write_json(manifest_path, {**result, "runtime_files": runtime_result["files"]})
    report_path.write_text(_report_markdown(result), encoding="utf-8")

    result["files"] = [
        str(contract_path),
        str(commands_path),
        str(readme_path),
        str(sample_input_path),
        str(manifest_path),
        str(report_path),
        *runtime_result["files"],
    ]
    return result


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.gem_prompt_daily_shortcut",
        description="Generate a daily local GEM prompt runtime pack.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--pasted-text")
    parser.add_argument("--pasted-text-file")
    parser.add_argument("--image-reference")
    parser.add_argument("--structured-json-file")
    parser.add_argument("--notes")
    parser.add_argument("--run-id", default="DAILY-GEM-REVIEW")
    parser.add_argument("--generated-at-utc")
    parser.add_argument("--use-default-sample", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = write_daily_shortcut_pack(
        DailyShortcutRequest(
            output_dir=args.output_dir,
            pasted_text=args.pasted_text,
            pasted_text_file=args.pasted_text_file,
            image_reference=args.image_reference,
            structured_json_file=args.structured_json_file,
            notes=args.notes,
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
            use_default_sample=args.use_default_sample,
        )
    )
    print(result["status"])
    print(result["output_dir"])
    print(result["runtime_prompt"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
