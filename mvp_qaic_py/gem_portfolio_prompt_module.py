from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


GEM_PORTFOLIO_PROMPT_SAFETY: dict[str, bool] = {
    "mvp_public_scope": True,
    "qaic_private_backend_separated": True,
    "human_review_only": True,
    "gem_ready_prompt_only": True,
    "no_ocr_claim": True,
    "no_image_visual_extraction_without_human": True,
    "no_revolutx_real_access": True,
    "no_broker": True,
    "no_order": True,
    "no_cancel": True,
    "no_replace_order": True,
    "no_auto_sizing": True,
    "no_secret_log": True,
    "no_sheet_write": True,
    "no_apps_script_execution": True,
    "no_clasp": True,
    "no_public_deploy": True,
}

SUPPORTED_PORTFOLIO_INPUT_MODES: tuple[str, ...] = (
    "NONE",
    "PASTED_TEXT",
    "STRUCTURED",
    "IMAGE_REVIEW_REQUIRED",
)


def _now_iso(now_utc: str | None = None) -> str:
    if now_utc:
        return now_utc
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_portfolio_input(
    *,
    pasted_text: str | None = None,
    structured_positions: list[dict[str, Any]] | None = None,
    image_reference: str | None = None,
) -> dict[str, Any]:
    pasted = (pasted_text or "").strip()
    structured = structured_positions or []
    image_ref = (image_reference or "").strip()

    missing_data: list[str] = []
    blockers: list[str] = []
    review_notes: list[str] = []

    if image_ref:
        mode = "IMAGE_REVIEW_REQUIRED"
        review_notes.append(
            "Image/capture supplied: visual extraction must be reviewed by a human or external OCR tool."
        )
        missing_data.append("portfolio_image_visual_extraction")
    elif structured:
        mode = "STRUCTURED"
    elif pasted:
        mode = "PASTED_TEXT"
    else:
        mode = "NONE"
        missing_data.append("portfolio_input")

    normalized_positions: list[dict[str, Any]] = []
    for index, item in enumerate(structured, start=1):
        symbol = str(item.get("symbol", "")).strip().upper()
        quantity = item.get("quantity")
        avg_price = item.get("avg_price")
        value = item.get("value")
        normalized_positions.append(
            {
                "row": index,
                "symbol": symbol,
                "quantity": quantity,
                "avg_price": avg_price,
                "value": value,
                "review_required": not bool(symbol),
            }
        )
        if not symbol:
            missing_data.append(f"position_{index}_symbol")

    if pasted and len(pasted) < 20:
        review_notes.append("Pasted portfolio text is short; user should verify completeness.")

    return {
        "portfolio_input_mode": mode,
        "pasted_text": pasted,
        "structured_positions": normalized_positions,
        "image_reference": image_ref,
        "missing_data": sorted(set(missing_data)),
        "blockers": blockers,
        "review_notes": review_notes,
        "ocr_performed": False,
        "human_review_required": True,
    }


def build_expected_output_schema() -> dict[str, Any]:
    return {
        "decision_status": "REVIEW_REQUIRED | BLOCKED | INFORMATIONAL_REVIEW_ONLY",
        "analysis_level": "INSUFFICIENT_DATA | PARTIAL_PORTFOLIO_REVIEW | PORTFOLIO_REVIEW_READY",
        "portfolio_summary": {
            "detected_assets": "list[str]",
            "exposure_notes": "list[str]",
            "concentration_flags": "list[str]",
        },
        "missing_data": "list[str]",
        "blockers": "list[str]",
        "questions_for_user": "list[str]",
        "human_decision_only": True,
        "no_order_no_sizing": True,
    }


def build_gem_prompt_payload(
    *,
    user_goal: str,
    portfolio_input: dict[str, Any],
    market_context: str | None = None,
    risk_profile: str | None = None,
    now_utc: str | None = None,
) -> dict[str, Any]:
    goal = (user_goal or "").strip() or "Review crypto portfolio in educational, human-review mode."
    context = (market_context or "").strip()
    risk = (risk_profile or "").strip() or "UNSPECIFIED"

    missing_data = list(portfolio_input.get("missing_data", []))
    blockers = list(portfolio_input.get("blockers", []))
    review_questions: list[str] = []

    if portfolio_input["portfolio_input_mode"] == "NONE":
        review_questions.append(
            "Paste portfolio text, provide structured positions, or attach an image/capture for human review."
        )
    if portfolio_input["portfolio_input_mode"] == "IMAGE_REVIEW_REQUIRED":
        review_questions.append(
            "Confirm the assets, quantities, values and prices visible in the capture before analysis."
        )
    if risk == "UNSPECIFIED":
        missing_data.append("risk_profile")
        review_questions.append(
            "What is the intended risk profile: conservative, balanced, aggressive, or custom?"
        )

    return {
        "prompt_id": "P112_GEM_PORTFOLIO_PROMPT_USUAL_MODULE",
        "created_at_utc": _now_iso(now_utc),
        "user_goal": goal,
        "portfolio_input_mode": portfolio_input["portfolio_input_mode"],
        "portfolio_input": portfolio_input,
        "market_context": context,
        "risk_profile": risk,
        "missing_data": sorted(set(missing_data)),
        "blockers": blockers,
        "review_questions": review_questions,
        "expected_output_schema": build_expected_output_schema(),
        "safety": dict(GEM_PORTFOLIO_PROMPT_SAFETY),
        "human_decision_only": True,
        "no_order_no_sizing": True,
        "next": "P113_PORTFOLIO_INPUT_NORMALIZER_AND_IMAGE_REVIEW_WORKFLOW",
    }


def render_gem_ready_prompt(payload: dict[str, Any]) -> str:
    portfolio_input = payload["portfolio_input"]
    structured_positions = portfolio_input.get("structured_positions", [])
    pasted_text = portfolio_input.get("pasted_text", "")
    image_reference = portfolio_input.get("image_reference", "")

    positions_md = (
        "\n".join(
            f"- {item.get('symbol') or 'UNKNOWN'} | quantity={item.get('quantity')} | avg_price={item.get('avg_price')} | value={item.get('value')}"
            for item in structured_positions
        )
        or "- No structured positions provided."
    )

    missing = "\n".join(f"- `{item}`" for item in payload["missing_data"]) or "- None detected."
    blockers = "\n".join(f"- `{item}`" for item in payload["blockers"]) or "- None."
    questions = "\n".join(f"- {item}" for item in payload["review_questions"]) or "- None."

    return f"""# GEM Portfolio Review Prompt — MVP QAIC P112

## Safety contract

You are running in educational support / human-review-only mode.

- Do not place, prepare, size, replace, cancel, or automate any order.
- Do not invent portfolio values, entry prices, current prices, stop-loss, take-profit, trailing orders, or risk sizing.
- If portfolio data is missing, ambiguous, or image-only, return `REVIEW_REQUIRED` and list `missing_data`.
- If the user asks for automatic order execution, return `BLOCKED`.
- Keep `human_decision_only=true` and `no_order_no_sizing=true`.

## User goal

{payload["user_goal"]}

## Portfolio input mode

`{payload["portfolio_input_mode"]}`

## Portfolio pasted text

```text
{pasted_text or "NONE"}
```

## Portfolio image / capture reference

`{image_reference or "NONE"}`

If this is image/capture based, do not claim OCR or visual extraction unless explicit extracted text is supplied. Ask for human confirmation of visible assets/quantities/values.

## Structured positions

{positions_md}

## Market context

```text
{payload["market_context"] or "NONE"}
```

## Risk profile

`{payload["risk_profile"]}`

## Missing data already known

{missing}

## Blockers already known

{blockers}

## Questions for user

{questions}

## Required output JSON shape

```json
{json.dumps(payload["expected_output_schema"], ensure_ascii=False, indent=2)}
```
"""


def summarize_gem_prompt_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "prompt_id": payload["prompt_id"],
        "portfolio_input_mode": payload["portfolio_input_mode"],
        "missing_data_count": len(payload["missing_data"]),
        "blocker_count": len(payload["blockers"]),
        "human_decision_only": payload["human_decision_only"],
        "no_order_no_sizing": payload["no_order_no_sizing"],
        "next": payload["next"],
    }


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
