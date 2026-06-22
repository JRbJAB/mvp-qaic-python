from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .gem_prompt_runner_pack import (
    SAFETY_MARKERS as P114_SAFETY_MARKERS,
    build_expected_gem_output_schema,
    build_gem_prompt_runner_pack,
)

VERSION = "MVP_QAIC_P116_PROMPT_GEM_RUNTIME_MINI_CLI_0_1_0_SAFE"

P116_SAFETY_MARKERS = tuple(
    dict.fromkeys(
        (
            *P114_SAFETY_MARKERS,
            "P116_MINI_CLI_LOCAL_ONLY",
            "NO_LIVE_PROVIDER_CALL",
            "NO_IMAGE_OCR_RUNTIME",
            "NO_AUTOMATED_VISUAL_EXTRACTION",
            "COPY_PASTE_TO_GEM_ONLY",
        )
    )
)

SUPPORTED_INPUT_MODES = (
    "NONE",
    "PASTED_TEXT",
    "PASTED_TEXT_DRAFT",
    "STRUCTURED",
    "IMAGE_REVIEW_REQUIRED",
)


@dataclass(frozen=True)
class GemRuntimeRequest:
    input_mode: str
    pasted_text: str | None = None
    structured_portfolio: Mapping[str, Any] | None = None
    image_reference: str | None = None
    notes: str | None = None
    run_id: str | None = None
    generated_at_utc: str | None = None


def _read_text_or_file(value: str | None, file_path: str | None) -> str | None:
    if value and file_path:
        raise ValueError("Use either direct text or file path, not both.")
    if file_path:
        return Path(file_path).read_text(encoding="utf-8")
    return value


def _read_structured_json(file_path: str | None) -> Mapping[str, Any] | None:
    if not file_path:
        return None
    payload = json.loads(Path(file_path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Structured portfolio JSON must be an object.")
    return payload


def build_runtime_contract() -> dict[str, Any]:
    return {
        "contract": "P116_PROMPT_GEM_RUNTIME_MINI_CLI",
        "version": VERSION,
        "status": "LOCAL_ONLY_HUMAN_REVIEW",
        "supported_input_modes": list(SUPPORTED_INPUT_MODES),
        "output_files": [
            "P116_RUNTIME_PAYLOAD.json",
            "P116_GEM_PROMPT_COPY_PASTE.md",
            "P116_EXPECTED_GEM_OUTPUT_SCHEMA.json",
            "P116_RUNTIME_CONTRACT.json",
            "P116_RUNTIME_REPORT.md",
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
        "safety_markers": list(P116_SAFETY_MARKERS),
    }


def _build_runtime_prompt_markdown(
    runner_payload: Mapping[str, Any], request: GemRuntimeRequest
) -> str:
    base_prompt = str(runner_payload["gem_prompt_markdown"]).rstrip()
    lines = [
        base_prompt,
        "",
        "---",
        "## P116 Runtime input reference",
        "",
        "This section is the user-provided source input for manual GEM review.",
        "Do not infer hidden positions, quantities, prices, or values from it.",
        "",
        f"- input_mode: {request.input_mode}",
    ]

    if request.pasted_text:
        lines.extend(
            [
                "",
                "### Pasted portfolio text",
                "```text",
                request.pasted_text.strip(),
                "```",
            ]
        )

    if request.structured_portfolio:
        lines.extend(
            [
                "",
                "### Structured portfolio JSON",
                "```json",
                json.dumps(
                    request.structured_portfolio, ensure_ascii=False, indent=2, sort_keys=True
                ),
                "```",
            ]
        )

    if request.image_reference:
        lines.extend(
            [
                "",
                "### Image reference",
                f"- {request.image_reference}",
                "- Human review only. No OCR claim. No automated visual extraction claim.",
            ]
        )

    if request.notes:
        lines.extend(
            [
                "",
                "### Notes",
                request.notes.strip(),
            ]
        )

    lines.extend(
        [
            "",
            "## P116 Safety reminder",
            "- HUMAN_REVIEW_ONLY.",
            "- NO_OCR_CLAIM.",
            "- NO_BROKER / NO_ORDER / NO_AUTO_SIZING.",
            "- NO_REVOLUTX_REAL_ACCESS_FROM_MVP.",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def build_runtime_payload(request: GemRuntimeRequest) -> dict[str, Any]:
    if request.input_mode not in SUPPORTED_INPUT_MODES:
        raise ValueError(f"Unsupported input_mode: {request.input_mode}")

    runner_payload = build_gem_prompt_runner_pack(
        input_mode=request.input_mode,
        pasted_text=request.pasted_text,
        structured_portfolio=request.structured_portfolio,
        image_reference=request.image_reference,
        notes=request.notes,
        run_id=request.run_id,
        generated_at_utc=request.generated_at_utc,
    )

    return {
        "step": "P116_PROMPT_GEM_RUNTIME_MINI_CLI",
        "version": VERSION,
        "status": "REVIEW_REQUIRED",
        "runtime_mode": "LOCAL_COPY_PASTE_TO_GEM_ONLY",
        "request": {
            "input_mode": request.input_mode,
            "pasted_text_available": bool(request.pasted_text),
            "structured_portfolio_available": bool(request.structured_portfolio),
            "image_reference": request.image_reference,
            "notes": request.notes,
            "run_id": request.run_id,
            "generated_at_utc": request.generated_at_utc,
        },
        "p114_runner_payload": runner_payload,
        "expected_gem_output_schema": build_expected_gem_output_schema(),
        "gem_prompt_markdown": _build_runtime_prompt_markdown(runner_payload, request),
        "contract": build_runtime_contract(),
        "safety_markers": list(P116_SAFETY_MARKERS),
        "human_review_only": True,
        "no_order_no_sizing": True,
        "no_ocr_claim": True,
        "no_revolutx_real_access": True,
    }


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _build_report(payload: Mapping[str, Any], output_dir: str) -> str:
    p114_payload = payload["p114_runner_payload"]
    normalized = p114_payload.get("normalized_portfolio_input", {})
    missing_data = normalized.get("missing_data", [])
    blockers = normalized.get("blockers", [])

    return "\n".join(
        [
            "# P116 Prompt GEM Runtime Mini CLI Report",
            "",
            f"- status: {payload['status']}",
            f"- version: {payload['version']}",
            f"- runtime_mode: {payload['runtime_mode']}",
            f"- output_dir: {output_dir}",
            f"- input_mode: {payload['request']['input_mode']}",
            f"- missing_data_count: {len(missing_data)}",
            f"- blocker_count: {len(blockers)}",
            "- safety: HUMAN_REVIEW_ONLY / NO_OCR_CLAIM / NO_BROKER / NO_ORDER / NO_SIZING",
            "- usage: copy P116_GEM_PROMPT_COPY_PASTE.md into GEM manually",
            "",
            "## Next",
            "",
            "P117_PROMPT_GEM_RUNTIME_USABILITY_PACK_OR_P116B_CLI_REVIEW",
            "",
        ]
    )


def write_runtime_pack(output_dir: str | Path, request: GemRuntimeRequest) -> dict[str, Any]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    payload = build_runtime_payload(request)
    contract = build_runtime_contract()
    schema = payload["expected_gem_output_schema"]

    payload_path = out / "P116_RUNTIME_PAYLOAD.json"
    prompt_path = out / "P116_GEM_PROMPT_COPY_PASTE.md"
    schema_path = out / "P116_EXPECTED_GEM_OUTPUT_SCHEMA.json"
    contract_path = out / "P116_RUNTIME_CONTRACT.json"
    report_path = out / "P116_RUNTIME_REPORT.md"

    _write_json(payload_path, payload)
    prompt_path.write_text(payload["gem_prompt_markdown"].rstrip() + "\n", encoding="utf-8")
    _write_json(schema_path, schema)
    _write_json(contract_path, contract)
    report_path.write_text(_build_report(payload, str(out)), encoding="utf-8")

    return {
        "status": "EXPORTED",
        "step": "P116_PROMPT_GEM_RUNTIME_MINI_CLI",
        "output_dir": str(out),
        "files": [
            str(payload_path),
            str(prompt_path),
            str(schema_path),
            str(contract_path),
            str(report_path),
        ],
        "safety_markers": list(P116_SAFETY_MARKERS),
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m mvp_qaic_py.gem_prompt_runtime_cli",
        description="Generate a local copy-paste GEM portfolio review prompt pack.",
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--input-mode", choices=SUPPORTED_INPUT_MODES, default="IMAGE_REVIEW_REQUIRED"
    )
    parser.add_argument("--pasted-text")
    parser.add_argument("--pasted-text-file")
    parser.add_argument("--structured-json-file")
    parser.add_argument("--image-reference")
    parser.add_argument("--notes")
    parser.add_argument("--run-id")
    parser.add_argument("--generated-at-utc")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    pasted_text = _read_text_or_file(args.pasted_text, args.pasted_text_file)
    structured = _read_structured_json(args.structured_json_file)

    result = write_runtime_pack(
        args.output_dir,
        GemRuntimeRequest(
            input_mode=args.input_mode,
            pasted_text=pasted_text,
            structured_portfolio=structured,
            image_reference=args.image_reference,
            notes=args.notes,
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        ),
    )

    print(result["status"])
    print(result["output_dir"])
    for path in result["files"]:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
