from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PORTFOLIO_INPUT_NORMALIZER_SAFETY: dict[str, bool] = {
    "mvp_public_scope": True,
    "qaic_private_backend_separated": True,
    "human_review_only": True,
    "portfolio_input_normalizer_only": True,
    "image_review_workflow_only": True,
    "no_ocr_claim": True,
    "no_image_visual_extraction_without_human": True,
    "no_invented_position": True,
    "no_invented_price": True,
    "no_invented_value": True,
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

DEFAULT_KNOWN_SYMBOLS: tuple[str, ...] = (
    "BTC",
    "ETH",
    "SOL",
    "NEAR",
    "VVV",
    "DASH",
    "DOT",
    "FET",
    "DOGE",
    "ATOM",
    "LINK",
    "ADA",
    "AVAX",
    "BNB",
    "MATIC",
    "POL",
    "XRP",
    "USDC",
    "USDT",
    "EUR",
    "USD",
)

COMMON_NON_SYMBOL_WORDS: set[str] = {
    "CRYPTO",
    "PORTFOLIO",
    "TOTAL",
    "VALUE",
    "PRICE",
    "AMOUNT",
    "QTY",
    "QUANTITY",
    "BALANCE",
    "ASSET",
    "NAME",
    "AVERAGE",
    "AVG",
    "GAIN",
    "LOSS",
    "PNL",
}


def _now_iso(now_utc: str | None = None) -> str:
    if now_utc:
        return now_utc
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_symbol(value: Any) -> str:
    return re.sub(r"[^A-Z0-9]", "", str(value or "").strip().upper())


def detect_symbols_from_text(
    text: str,
    *,
    known_symbols: tuple[str, ...] = DEFAULT_KNOWN_SYMBOLS,
) -> list[str]:
    tokens = re.findall(r"\b[A-Za-z][A-Za-z0-9]{1,9}\b", text or "")
    known = set(known_symbols)
    symbols: list[str] = []
    for token in tokens:
        candidate = normalize_symbol(token)
        if not candidate or candidate in COMMON_NON_SYMBOL_WORDS:
            continue
        if candidate in known or (candidate.isupper() and 2 <= len(candidate) <= 6):
            if candidate not in symbols:
                symbols.append(candidate)
    return symbols


def detect_numeric_tokens(text: str) -> list[str]:
    return re.findall(r"(?<![A-Za-z])[-+]?\d+(?:[.,]\d+)?%?", text or "")


def build_image_review_checklist(image_reference: str) -> list[str]:
    return [
        f"Confirm that the image/capture reference is correct: {image_reference}.",
        "List every visible asset symbol exactly as displayed.",
        "Confirm visible quantity/amount for each asset.",
        "Confirm visible fiat value for each asset if present.",
        "Confirm average entry price/cost basis only if it is explicitly visible.",
        "Confirm current price only if explicitly visible or provided as separate market context.",
        "Do not infer hidden rows or missing assets from the capture.",
        "Do not generate an order, sizing, stop-loss, take-profit, or trailing action.",
    ]


def normalize_structured_positions(positions: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(positions or [], start=1):
        symbol = normalize_symbol(item.get("symbol"))
        row_missing: list[str] = []
        if not symbol:
            row_missing.append("symbol")

        normalized.append(
            {
                "row": index,
                "symbol": symbol,
                "quantity": item.get("quantity"),
                "avg_price": item.get("avg_price"),
                "current_price": item.get("current_price"),
                "value": item.get("value"),
                "raw": item,
                "missing_fields": row_missing,
                "review_required": bool(row_missing),
            }
        )
    return normalized


def parse_pasted_text_draft_positions(text: str) -> list[dict[str, Any]]:
    draft_rows: list[dict[str, Any]] = []
    for line_no, raw_line in enumerate((text or "").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        symbols = detect_symbols_from_text(line)
        numeric_tokens = detect_numeric_tokens(line)
        if not symbols and not numeric_tokens:
            continue

        draft_rows.append(
            {
                "line_no": line_no,
                "raw_line": line,
                "symbols_detected": symbols,
                "numeric_tokens_detected": numeric_tokens,
                "review_required": True,
                "confidence": "DRAFT_REVIEW_REQUIRED",
                "notes": [
                    "Text parser does not assign numeric tokens to quantity/value/price automatically.",
                    "Human confirmation required before portfolio analysis.",
                ],
            }
        )
    return draft_rows


def normalize_portfolio_input_workflow(
    *,
    pasted_text: str | None = None,
    structured_positions: list[dict[str, Any]] | None = None,
    image_reference: str | None = None,
    user_goal: str | None = None,
    now_utc: str | None = None,
) -> dict[str, Any]:
    pasted = (pasted_text or "").strip()
    image_ref = (image_reference or "").strip()
    structured = normalize_structured_positions(structured_positions)

    missing_data: list[str] = []
    blockers: list[str] = []
    review_required_reasons: list[str] = []
    checklist: list[str] = []

    if image_ref:
        mode = "IMAGE_REVIEW_REQUIRED"
        missing_data.append("portfolio_image_visual_extraction")
        review_required_reasons.append("IMAGE_CAPTURE_REQUIRES_HUMAN_VISUAL_CONFIRMATION")
        checklist = build_image_review_checklist(image_ref)
    elif structured:
        mode = "STRUCTURED"
    elif pasted:
        mode = "PASTED_TEXT_DRAFT"
    else:
        mode = "NONE"
        missing_data.append("portfolio_input")
        review_required_reasons.append("NO_PORTFOLIO_INPUT_PROVIDED")

    draft_text_positions = parse_pasted_text_draft_positions(pasted)
    structured_missing = [
        f"position_{item['row']}_{field}"
        for item in structured
        for field in item.get("missing_fields", [])
    ]
    missing_data.extend(structured_missing)

    if pasted and not draft_text_positions:
        review_required_reasons.append("PASTED_TEXT_NOT_STRUCTURED_ENOUGH_FOR_DRAFT_EXTRACTION")

    asset_candidates = sorted(
        {symbol for item in structured for symbol in [item.get("symbol")] if symbol}
        | {
            symbol
            for row in draft_text_positions
            for symbol in row.get("symbols_detected", [])
            if symbol
        }
    )

    return {
        "runtime": "MVP_QAIC_PORTFOLIO_INPUT_NORMALIZER_IMAGE_REVIEW",
        "version": "P113_PORTFOLIO_INPUT_NORMALIZER_IMAGE_REVIEW_0_1_0",
        "created_at_utc": _now_iso(now_utc),
        "user_goal": (user_goal or "").strip() or "Prepare portfolio input for GEM prompt review.",
        "portfolio_input_mode": mode,
        "asset_candidates": asset_candidates,
        "structured_positions": structured,
        "pasted_text": pasted,
        "draft_text_positions": draft_text_positions,
        "image_reference": image_ref,
        "image_review_checklist": checklist,
        "missing_data": sorted(set(missing_data)),
        "blockers": blockers,
        "review_required_reasons": sorted(set(review_required_reasons)),
        "ocr_performed": False,
        "human_review_required": True,
        "analysis_allowed_now": mode in {"STRUCTURED", "PASTED_TEXT_DRAFT"} and not blockers,
        "gem_prompt_ready": True,
        "human_decision_only": True,
        "no_order_no_sizing": True,
        "safety": dict(PORTFOLIO_INPUT_NORMALIZER_SAFETY),
        "next": "P114_GEM_PROMPT_RUNNER_PACK_COPY_PASTE_AND_JSON_CONTRACT",
    }


def render_portfolio_review_markdown(workflow: dict[str, Any]) -> str:
    assets = ", ".join(workflow["asset_candidates"]) or "NONE"
    missing = "\n".join(f"- `{item}`" for item in workflow["missing_data"]) or "- None."
    reasons = "\n".join(f"- `{item}`" for item in workflow["review_required_reasons"]) or "- None."
    checklist = (
        "\n".join(f"- {item}" for item in workflow["image_review_checklist"])
        or "- Not image-based."
    )

    draft_lines = []
    for item in workflow["draft_text_positions"]:
        draft_lines.append(
            f"- line `{item['line_no']}` symbols={item['symbols_detected']} numbers={item['numeric_tokens_detected']}"
        )
    draft_md = "\n".join(draft_lines) or "- No text draft rows."

    return f"""# P113 — Portfolio Input Normalizer + Image Review Workflow

## Mode

`{workflow["portfolio_input_mode"]}`

## Asset candidates

`{assets}`

## Human review

human_review_required=`{workflow["human_review_required"]}`

## Missing data

{missing}

## Review required reasons

{reasons}

## Image review checklist

{checklist}

## Draft rows from pasted text

{draft_md}

## Safety

- NO_OCR_CLAIM
- NO_IMAGE_VISUAL_EXTRACTION_WITHOUT_HUMAN
- NO_INVENTED_POSITION
- NO_INVENTED_PRICE
- NO_INVENTED_VALUE
- NO_BROKER
- NO_ORDER
- NO_SIZING
"""


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
