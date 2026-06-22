from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

try:
    from . import gem_portfolio_prompt_module as _p112_prompt_module
except Exception:  # pragma: no cover - defensive import boundary
    _p112_prompt_module = None

try:
    from . import portfolio_input_normalizer as _p113_normalizer_module
except Exception:  # pragma: no cover - defensive import boundary
    _p113_normalizer_module = None


VERSION = "MVP_QAIC_P114_GEM_PROMPT_RUNNER_PACK_0_1_0_SAFE"
STATUS_REVIEW_REQUIRED = "REVIEW_REQUIRED"

INPUT_MODES = (
    "NONE",
    "PASTED_TEXT",
    "PASTED_TEXT_DRAFT",
    "STRUCTURED",
    "IMAGE_REVIEW_REQUIRED",
)

SAFETY_MARKERS = (
    "MVP_PUBLIC_SCOPE",
    "HUMAN_REVIEW_ONLY",
    "NO_OCR_CLAIM",
    "NO_IMAGE_VISUAL_EXTRACTION_WITHOUT_HUMAN",
    "NO_INVENTED_POSITION",
    "NO_INVENTED_PRICE",
    "NO_INVENTED_VALUE",
    "NO_REVOLUTX_REAL_ACCESS",
    "NO_BROKER",
    "NO_ORDER",
    "NO_CANCEL",
    "NO_REPLACE_ORDER",
    "NO_AUTO_SIZING",
    "NO_SECRET_LOG",
    "NO_SHEET_WRITE",
    "NO_APPS_SCRIPT_EXECUTION",
    "NO_CLASP",
    "NO_PUBLIC_DEPLOY",
)

NORMALIZER_CANDIDATES = (
    "normalize_portfolio_input",
    "build_portfolio_input_normalization",
    "normalize_portfolio_payload",
    "normalize_input",
)

PROMPT_BUILDER_CANDIDATES = (
    "build_gem_portfolio_prompt",
    "prepare_gem_portfolio_prompt",
    "build_portfolio_prompt",
    "build_prompt",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, Mapping):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v) for v in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if hasattr(value, "model_dump"):
        return _jsonable(value.model_dump())
    if hasattr(value, "dict"):
        return _jsonable(value.dict())
    return str(value)


def _call_candidate(
    module: Any, names: tuple[str, ...], kwargs: dict[str, Any]
) -> tuple[Any | None, str | None, list[str]]:
    warnings: list[str] = []
    if module is None:
        return None, None, ["module_not_available"]

    for name in names:
        func = getattr(module, name, None)
        if not callable(func):
            continue
        try:
            return func(**kwargs), name, warnings
        except TypeError as exc:
            warnings.append(f"{name}:type_error:{exc}")
        except ValueError as exc:
            warnings.append(f"{name}:value_error:{exc}")

    return None, None, warnings


def _fallback_normalize(
    *,
    input_mode: str,
    pasted_text: str | None,
    structured_portfolio: Mapping[str, Any] | None,
    image_reference: str | None,
    notes: str | None,
) -> dict[str, Any]:
    mode = input_mode.upper().strip() if input_mode else "NONE"
    missing_data: list[str] = []
    review_questions: list[str] = []

    if mode not in INPUT_MODES:
        missing_data.append("valid_input_mode")
        review_questions.append("Confirm the portfolio input mode.")

    if mode == "NONE":
        missing_data.extend(["portfolio_positions", "portfolio_values"])
        review_questions.append(
            "Provide portfolio positions as pasted text, structured JSON, or image reference."
        )
    elif mode == "IMAGE_REVIEW_REQUIRED":
        missing_data.extend(
            [
                "human_confirmed_asset_symbols",
                "human_confirmed_quantities",
                "human_confirmed_values",
                "human_confirmed_visible_prices_if_any",
            ]
        )
        review_questions.extend(
            [
                "Confirm every visible asset symbol.",
                "Confirm every visible quantity.",
                "Confirm every visible value.",
                "Confirm that no hidden line is being assumed.",
            ]
        )
    elif mode in {"PASTED_TEXT", "PASTED_TEXT_DRAFT"}:
        if not pasted_text or not pasted_text.strip():
            missing_data.append("pasted_portfolio_text")
        review_questions.append(
            "Confirm that the pasted text reflects the full portfolio and not a partial extract."
        )
    elif mode == "STRUCTURED":
        if not structured_portfolio:
            missing_data.append("structured_portfolio")
        review_questions.append(
            "Confirm that the structured payload is complete and human-reviewed."
        )

    return {
        "status": STATUS_REVIEW_REQUIRED,
        "source": "p114_fallback_normalizer",
        "input_mode": mode,
        "pasted_text_available": bool(pasted_text and pasted_text.strip()),
        "structured_portfolio_available": bool(structured_portfolio),
        "image_reference": image_reference,
        "notes": notes,
        "positions": [],
        "missing_data": missing_data,
        "blockers": [],
        "review_questions": review_questions,
        "human_review_required": True,
        "no_ocr_claim": True,
        "no_visual_extraction_claim": True,
        "safety_markers": list(SAFETY_MARKERS),
    }


def normalize_runner_input(
    *,
    input_mode: str = "NONE",
    pasted_text: str | None = None,
    structured_portfolio: Mapping[str, Any] | None = None,
    image_reference: str | None = None,
    notes: str | None = None,
) -> dict[str, Any]:
    candidate_kwargs = {
        "input_mode": input_mode,
        "pasted_text": pasted_text,
        "structured_portfolio": structured_portfolio,
        "image_reference": image_reference,
        "notes": notes,
    }
    result, callable_name, warnings = _call_candidate(
        _p113_normalizer_module,
        NORMALIZER_CANDIDATES,
        candidate_kwargs,
    )

    if result is None:
        normalized = _fallback_normalize(**candidate_kwargs)
        normalized["integration"] = {
            "p113_normalizer": "fallback_used",
            "warnings": warnings,
        }
        return normalized

    normalized = _jsonable(result)
    if not isinstance(normalized, dict):
        normalized = {"result": normalized}

    normalized.setdefault("status", STATUS_REVIEW_REQUIRED)
    normalized.setdefault("missing_data", [])
    normalized.setdefault("blockers", [])
    normalized.setdefault("human_review_required", True)
    normalized.setdefault("safety_markers", list(SAFETY_MARKERS))
    normalized["integration"] = {
        "p113_normalizer": callable_name,
        "warnings": warnings,
    }
    return normalized


def build_expected_gem_output_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "MVP QAIC P114 Expected GEM Portfolio Review Output",
        "type": "object",
        "additionalProperties": True,
        "required": [
            "decision_status",
            "missing_data",
            "blockers",
            "human_decision_only",
            "no_order_no_sizing",
            "safety_markers",
        ],
        "properties": {
            "decision_status": {
                "type": "string",
                "enum": ["REVIEW_REQUIRED", "BLOCKED", "HUMAN_REVIEW_ONLY"],
            },
            "missing_data": {"type": "array", "items": {"type": "string"}},
            "blockers": {"type": "array", "items": {"type": "string"}},
            "portfolio_review": {"type": "object"},
            "risk_notes": {"type": "array", "items": {"type": "string"}},
            "questions_for_human": {"type": "array", "items": {"type": "string"}},
            "human_decision_only": {"type": "boolean", "const": True},
            "no_order_no_sizing": {"type": "boolean", "const": True},
            "safety_markers": {"type": "array", "items": {"type": "string"}},
        },
    }


def _fallback_prompt(payload: Mapping[str, Any]) -> str:
    normalized = payload["normalized_portfolio_input"]
    schema = payload["expected_gem_output_schema"]

    return "\n".join(
        [
            "# MVP QAIC - GEM Portfolio Review Prompt",
            "",
            "## Mission",
            "Review the portfolio input for educational and decision-support purposes only.",
            "Return a structured JSON answer matching the expected schema.",
            "",
            "## Hard safety rules",
            "- HUMAN_REVIEW_ONLY.",
            "- Do not place, suggest placing, cancel, replace, or automate any order.",
            "- Do not calculate position sizing.",
            "- Do not claim OCR or automatic image extraction.",
            "- Do not invent assets, quantities, prices, values, TP, SL, or trailing levels.",
            "- If the input is incomplete or image-based, return REVIEW_REQUIRED with missing_data.",
            "",
            "## Normalized portfolio input",
            "```json",
            json.dumps(normalized, ensure_ascii=False, indent=2, sort_keys=True),
            "```",
            "",
            "## Expected output JSON schema",
            "```json",
            json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True),
            "```",
        ]
    )


def build_gem_prompt_markdown(payload: Mapping[str, Any]) -> str:
    candidate_kwargs = {
        "payload": payload,
        "normalized_input": payload.get("normalized_portfolio_input"),
        "expected_schema": payload.get("expected_gem_output_schema"),
        "safety_markers": list(SAFETY_MARKERS),
    }
    result, callable_name, warnings = _call_candidate(
        _p112_prompt_module,
        PROMPT_BUILDER_CANDIDATES,
        candidate_kwargs,
    )

    if result is None:
        return _fallback_prompt(payload)

    jsonable = _jsonable(result)
    if isinstance(jsonable, str):
        prompt = jsonable
    elif isinstance(jsonable, Mapping):
        prompt = str(
            jsonable.get("prompt_markdown")
            or jsonable.get("copy_paste_markdown")
            or jsonable.get("prompt")
            or _fallback_prompt(payload)
        )
    else:
        prompt = str(jsonable)

    footer = [
        "",
        "---",
        "P114 runner integration:",
        f"- p112_prompt_builder: {callable_name}",
        f"- p112_warnings: {warnings}",
    ]
    return prompt.rstrip() + "\n" + "\n".join(footer)


def build_gem_prompt_runner_pack(
    *,
    input_mode: str = "NONE",
    pasted_text: str | None = None,
    structured_portfolio: Mapping[str, Any] | None = None,
    image_reference: str | None = None,
    notes: str | None = None,
    run_id: str | None = None,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    generated_at = generated_at_utc or _utc_now()
    runner_id = run_id or f"P114-GEM-RUNNER-{generated_at.replace(':', '').replace('-', '')}"

    normalized = normalize_runner_input(
        input_mode=input_mode,
        pasted_text=pasted_text,
        structured_portfolio=structured_portfolio,
        image_reference=image_reference,
        notes=notes,
    )
    schema = build_expected_gem_output_schema()

    payload: dict[str, Any] = {
        "step": "P114_GEM_PROMPT_RUNNER_PACK_COPY_PASTE_AND_JSON_CONTRACT",
        "version": VERSION,
        "status": STATUS_REVIEW_REQUIRED,
        "run_id": runner_id,
        "generated_at_utc": generated_at,
        "input_mode": input_mode,
        "input": {
            "pasted_text": pasted_text,
            "structured_portfolio": _jsonable(structured_portfolio),
            "image_reference": image_reference,
            "notes": notes,
        },
        "normalized_portfolio_input": normalized,
        "expected_gem_output_schema": schema,
        "safety_markers": list(SAFETY_MARKERS),
        "human_review_only": True,
        "no_order_no_sizing": True,
        "no_ocr_claim": True,
        "no_revolutx_real_access": True,
    }
    payload["gem_prompt_markdown"] = build_gem_prompt_markdown(payload)
    return payload


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_runner_contract() -> dict[str, Any]:
    return {
        "contract": "P114_GEM_PROMPT_RUNNER_PACK_COPY_PASTE_AND_JSON_CONTRACT",
        "version": VERSION,
        "allowed_inputs": list(INPUT_MODES),
        "output_files": [
            "P114_GEM_RUNNER_PAYLOAD_SAMPLE.json",
            "P114_GEM_PROMPT_COPY_PASTE.md",
            "P114_EXPECTED_GEM_OUTPUT_SCHEMA.json",
            "P114_RUNNER_REPORT.md",
            "P114_RUNNER_CONTRACT.json",
        ],
        "safety_markers": list(SAFETY_MARKERS),
        "forbidden": [
            "index_edit",
            "clasp_push",
            "apps_script_execution",
            "sheet_write",
            "public_deploy",
            "broker_execution",
            "order_execution",
            "order_cancel",
            "order_replace",
            "auto_sizing",
            "ocr_claim",
            "invented_position",
            "invented_price",
            "invented_value",
            "revolutx_real_access_from_mvp",
        ],
    }


def build_runner_report_markdown(payload: Mapping[str, Any], output_dir: str) -> str:
    normalized = payload["normalized_portfolio_input"]
    missing_data = normalized.get("missing_data", [])
    blockers = normalized.get("blockers", [])

    return "\n".join(
        [
            "# P114 GEM Prompt Runner Pack Report",
            "",
            f"- status: {payload['status']}",
            f"- version: {payload['version']}",
            f"- run_id: {payload['run_id']}",
            f"- generated_at_utc: {payload['generated_at_utc']}",
            f"- output_dir: {output_dir}",
            f"- input_mode: {payload['input_mode']}",
            f"- missing_data_count: {len(missing_data)}",
            f"- blocker_count: {len(blockers)}",
            "- safety: HUMAN_REVIEW_ONLY / NO_BROKER / NO_ORDER / NO_SIZING / NO_OCR_CLAIM",
            "- revolutx: NO_REAL_ACCESS_FROM_MVP",
            "",
            "## Next",
            "P115_MODULE_MIGRATION_INVENTORY_APPS_SCRIPT_TO_PYTHON",
            "",
        ]
    )


def export_gem_prompt_runner_pack(
    output_dir: str | Path,
    *,
    input_mode: str = "IMAGE_REVIEW_REQUIRED",
    pasted_text: str | None = None,
    structured_portfolio: Mapping[str, Any] | None = None,
    image_reference: str | None = "portfolio_capture_reference_for_human_review.png",
    notes: str | None = "P114 sample pack. Image is a human-review reference only. No OCR claim.",
    run_id: str | None = "P114-SAMPLE",
    generated_at_utc: str | None = "2026-06-22T00:00:00Z",
) -> dict[str, Any]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    payload = build_gem_prompt_runner_pack(
        input_mode=input_mode,
        pasted_text=pasted_text,
        structured_portfolio=structured_portfolio,
        image_reference=image_reference,
        notes=notes,
        run_id=run_id,
        generated_at_utc=generated_at_utc,
    )
    contract = build_runner_contract()

    payload_path = out / "P114_GEM_RUNNER_PAYLOAD_SAMPLE.json"
    prompt_path = out / "P114_GEM_PROMPT_COPY_PASTE.md"
    schema_path = out / "P114_EXPECTED_GEM_OUTPUT_SCHEMA.json"
    report_path = out / "P114_RUNNER_REPORT.md"
    contract_path = out / "P114_RUNNER_CONTRACT.json"

    _write_json(payload_path, payload)
    prompt_path.write_text(payload["gem_prompt_markdown"].rstrip() + "\n", encoding="utf-8")
    _write_json(schema_path, payload["expected_gem_output_schema"])
    report_path.write_text(build_runner_report_markdown(payload, str(out)), encoding="utf-8")
    _write_json(contract_path, contract)

    return {
        "status": "EXPORTED",
        "step": "P114_GEM_PROMPT_RUNNER_PACK_COPY_PASTE_AND_JSON_CONTRACT",
        "output_dir": str(out),
        "files": [
            str(payload_path),
            str(prompt_path),
            str(schema_path),
            str(report_path),
            str(contract_path),
        ],
        "safety_markers": list(SAFETY_MARKERS),
    }
