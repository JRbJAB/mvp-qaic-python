from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


MVP_PUBLIC_SAFETY: dict[str, bool] = {
    "mvp_public_scope": True,
    "qaic_private_backend_separated": True,
    "portfolio_on_demand_supported": True,
    "image_capture_reference_supported": True,
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
    "public_educational_mode": True,
}

FORBIDDEN_EXECUTION_MARKERS: tuple[str, ...] = (
    "place order",
    "place an order",
    "execute order",
    "send order",
    "automatic order",
    "auto order",
    "trailing stop order",
    "market order",
    "limit order",
    "cancel order",
    "replace order",
    "auto sizing",
    "autosizing",
    "broker",
    "revolut x order",
    "revolutx order",
)

SECRET_MARKERS: tuple[str, ...] = (
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
    "authorization",
    "bearer",
    "password",
    "private_key",
    "secret",
    "token",
)

ASSET_RE = re.compile(r"\b(BTC|ETH|SOL|BNB|XRP|ADA|DOGE|LINK|AVAX|DOT|MATIC|NEAR)\b", re.I)
NUMBER_RE = re.compile(r"[-+]?\d+(?:[.,]\d+)?")


@dataclass(frozen=True)
class PortfolioLine:
    asset: str
    quantity: float | None = None
    avg_entry: float | None = None
    current_value: float | None = None
    pnl: float | None = None
    source: str = "parsed_text"

    def to_dict(self) -> dict[str, Any]:
        return {
            "asset": self.asset,
            "quantity": self.quantity,
            "avg_entry": self.avg_entry,
            "current_value": self.current_value,
            "pnl": self.pnl,
            "source": self.source,
        }


def _now_iso(now_utc: str | None = None) -> str:
    if now_utc:
        return now_utc
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _to_float(value: str | int | float | None) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = value.replace(" ", "").replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return None


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key, item in value.items():
            key_lower = str(key).lower()
            if any(marker in key_lower for marker in SECRET_MARKERS):
                out[key] = "REDACTED"
            else:
                out[key] = _redact(item)
        return out

    if isinstance(value, list):
        return [_redact(item) for item in value]

    if isinstance(value, str):
        lower = value.lower()
        if "bearer " in lower or "sk-" in lower or "revx_" in lower:
            return "REDACTED"
    return value


def _contains_forbidden_execution_intent(text: str) -> bool:
    lower = text.lower()
    return any(marker in lower for marker in FORBIDDEN_EXECUTION_MARKERS)


def parse_pasted_portfolio_text(text: str) -> dict[str, Any]:
    """Best-effort parser for portfolio text copied by the user."""
    raw = text or ""
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    positions: list[PortfolioLine] = []

    for line in lines:
        asset_match = ASSET_RE.search(line)
        if not asset_match:
            continue

        asset = asset_match.group(1).upper()
        numbers = [_to_float(match.group(0)) for match in NUMBER_RE.finditer(line)]
        numbers = [number for number in numbers if number is not None]

        quantity = numbers[0] if len(numbers) >= 1 else None
        avg_entry = numbers[1] if len(numbers) >= 2 else None
        current_value = numbers[2] if len(numbers) >= 3 else None
        pnl = numbers[3] if len(numbers) >= 4 else None

        positions.append(
            PortfolioLine(
                asset=asset,
                quantity=quantity,
                avg_entry=avg_entry,
                current_value=current_value,
                pnl=pnl,
            )
        )

    missing: list[str] = []
    if raw and not positions:
        missing.append("portfolio_text_assets_not_detected")
    if not raw:
        missing.append("portfolio_text_empty")

    return {
        "input_type": "pasted_text",
        "positions": [position.to_dict() for position in positions],
        "positions_count": len(positions),
        "missing_data": missing,
        "raw_text_available": bool(raw),
        "extraction_confidence": "LOW_BEST_EFFORT" if positions else "NONE",
    }


def normalize_structured_portfolio(
    portfolio: dict[str, Any] | list[dict[str, Any]],
) -> dict[str, Any]:
    rows: list[dict[str, Any]]
    if isinstance(portfolio, dict):
        nested = portfolio.get("positions") or portfolio.get("rows") or portfolio.get("items")
        rows = nested if isinstance(nested, list) else [portfolio]
    elif isinstance(portfolio, list):
        rows = portfolio
    else:
        rows = []

    clean_rows: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        asset = str(row.get("asset") or row.get("symbol") or row.get("ticker") or "").upper()
        clean_rows.append(
            {
                "asset": asset,
                "quantity": _to_float(row.get("quantity") or row.get("qty") or row.get("balance")),
                "avg_entry": _to_float(
                    row.get("avg_entry")
                    or row.get("entry_price")
                    or row.get("pru")
                    or row.get("average_buy_price")
                ),
                "current_value": _to_float(
                    row.get("current_value")
                    or row.get("value")
                    or row.get("value_eur")
                    or row.get("market_value")
                ),
                "pnl": _to_float(row.get("pnl") or row.get("pnl_eur") or row.get("unrealized_pnl")),
                "source": "structured",
            }
        )

    return {
        "input_type": "structured",
        "positions": clean_rows,
        "positions_count": len(clean_rows),
        "missing_data": [] if clean_rows else ["portfolio_structured_positions_empty"],
        "raw_text_available": False,
        "extraction_confidence": "HIGH_STRUCTURED" if clean_rows else "NONE",
    }


def build_image_capture_portfolio_reference(
    *,
    image_id: str | None = None,
    image_filename: str | None = None,
    user_notes: str = "",
) -> dict[str, Any]:
    """Represent a portfolio screenshot/capture without pretending local OCR happened."""
    return {
        "input_type": "image_capture",
        "image_id": image_id,
        "image_filename": image_filename,
        "user_notes": user_notes,
        "positions": [],
        "positions_count": 0,
        "missing_data": ["portfolio_image_visual_extraction_required"],
        "extraction_required": True,
        "extraction_instruction": (
            "Use the UI/LLM visual analysis layer to extract visible assets, quantities, "
            "average entry/PRU, value, PnL, and any missing fields. Do not invent hidden data."
        ),
        "extraction_confidence": "PENDING_VISUAL_EXTRACTION",
    }


def build_portfolio_context(
    *,
    portfolio_input: Any = None,
    portfolio_input_type: str = "none",
    image_id: str | None = None,
    image_filename: str | None = None,
    user_notes: str = "",
) -> dict[str, Any]:
    mode = (portfolio_input_type or "none").lower().strip()

    if mode in {"text", "pasted_text", "copy_paste", "copied_text"}:
        return parse_pasted_portfolio_text(str(portfolio_input or ""))

    if mode in {"structured", "json", "dict"}:
        if portfolio_input is None:
            return normalize_structured_portfolio([])
        return normalize_structured_portfolio(portfolio_input)

    if mode in {"image", "image_capture", "screenshot", "capture"}:
        return build_image_capture_portfolio_reference(
            image_id=image_id,
            image_filename=image_filename,
            user_notes=user_notes,
        )

    return {
        "input_type": "none",
        "positions": [],
        "positions_count": 0,
        "missing_data": ["portfolio_optional_not_provided"],
        "extraction_confidence": "NONE",
    }


def score_prompt_quality(
    *,
    user_prompt: str,
    portfolio_context: dict[str, Any],
    lexique_context: Any = None,
    methods_context: Any = None,
) -> dict[str, Any]:
    text = user_prompt.strip()
    missing_data = list(portfolio_context.get("missing_data", []))

    if not text:
        missing_data.append("user_prompt_empty")

    quality_score = 100
    if len(text) < 20:
        quality_score -= 20
    if portfolio_context.get("input_type") == "image_capture":
        quality_score -= 10
    if missing_data:
        quality_score -= min(45, 8 * len(missing_data))
    if not lexique_context:
        quality_score -= 8
    if not methods_context:
        quality_score -= 8

    safety_score = 100
    if _contains_forbidden_execution_intent(text):
        safety_score = 0

    data_completeness_score = max(0, 100 - 12 * len(missing_data))
    public_usefulness_score = max(0, min(100, quality_score))

    return {
        "quality_score": max(0, min(100, quality_score)),
        "public_safety_score": safety_score,
        "data_completeness_score": data_completeness_score,
        "public_usefulness_score": public_usefulness_score,
        "missing_data": missing_data,
    }


def build_mvp_public_prompt_payload(
    *,
    user_prompt: str,
    portfolio_input: Any = None,
    portfolio_input_type: str = "none",
    image_id: str | None = None,
    image_filename: str | None = None,
    lexique_context: Any = None,
    methods_context: Any = None,
    benchmark_context: Any = None,
    now_utc: str | None = None,
) -> dict[str, Any]:
    """Build the MVP public prompt/UI payload."""
    portfolio_context = build_portfolio_context(
        portfolio_input=portfolio_input,
        portfolio_input_type=portfolio_input_type,
        image_id=image_id,
        image_filename=image_filename,
        user_notes=user_prompt,
    )

    benchmark = score_prompt_quality(
        user_prompt=user_prompt,
        portfolio_context=portfolio_context,
        lexique_context=lexique_context,
        methods_context=methods_context,
    )

    blockers: list[str] = []
    if _contains_forbidden_execution_intent(user_prompt):
        blockers.append("FORBIDDEN_EXECUTION_OR_BROKER_INTENT")

    if blockers:
        decision_status = "BLOCKED"
    elif portfolio_context.get("input_type") == "image_capture":
        decision_status = "REVIEW_REQUIRED"
    elif benchmark["missing_data"]:
        decision_status = "REVIEW_REQUIRED"
    else:
        decision_status = "PUBLIC_PROMPT_READY"

    return {
        "runtime": "MVP_QAIC_PUBLIC_PROMPT_WEBAPP_BENCHMARK",
        "version": "P103_MVP_PUBLIC_PROMPT_WEBAPP_BENCHMARK_0_1_0",
        "created_at_utc": _now_iso(now_utc),
        "scope": {
            "mvp": "lexique_webapp_prompts_methods_public",
            "qaic_private": "backend_quant_risk_revolutx_execution_locked",
        },
        "decision_status": decision_status,
        "blockers": blockers,
        "missing_data": benchmark["missing_data"],
        "human_review_only": True,
        "public_educational_mode": True,
        "no_order_no_sizing": True,
        "safety": dict(MVP_PUBLIC_SAFETY),
        "prompt_request": {
            "user_prompt": user_prompt,
            "portfolio_context": _redact(portfolio_context),
            "lexique_context": _redact(lexique_context),
            "methods_context": _redact(methods_context),
            "benchmark_context": _redact(benchmark_context),
        },
        "benchmark": benchmark,
        "webapp_ui": {
            "recommended_sections": [
                "prompt_input",
                "portfolio_optional_input",
                "portfolio_image_capture",
                "lexique_context",
                "method_context",
                "benchmark_scores",
                "missing_data",
                "blockers",
                "human_review_output",
            ],
            "portfolio_input_modes": ["none", "pasted_text", "structured", "image_capture"],
        },
    }


def summarize_for_webapp(payload: dict[str, Any]) -> dict[str, Any]:
    request = payload.get("prompt_request", {})
    portfolio_context = request.get("portfolio_context", {}) if isinstance(request, dict) else {}
    benchmark = payload.get("benchmark", {}) if isinstance(payload.get("benchmark"), dict) else {}

    return {
        "decision_status": payload.get("decision_status"),
        "missing_data_count": len(payload.get("missing_data", [])),
        "blocker_count": len(payload.get("blockers", [])),
        "portfolio_input_type": portfolio_context.get("input_type"),
        "portfolio_positions_count": portfolio_context.get("positions_count"),
        "portfolio_extraction_required": portfolio_context.get("extraction_required") is True,
        "quality_score": benchmark.get("quality_score"),
        "public_safety_score": benchmark.get("public_safety_score"),
        "public_educational_mode": payload.get("public_educational_mode") is True,
        "no_order_no_sizing": payload.get("no_order_no_sizing") is True,
    }
