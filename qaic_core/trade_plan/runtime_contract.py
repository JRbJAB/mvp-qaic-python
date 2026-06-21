from __future__ import annotations

import math
from dataclasses import dataclass, field
from numbers import Real
from typing import Any, Mapping

SAFETY_MARKERS: tuple[str, ...] = (
    "HUMAN_REVIEW_ONLY",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_AUTO_TRAILING_ORDER",
    "NO_SECRET",
    "NO_INVENTED_PRICE_TP_SL_TRAILING",
)

REQUIRED_INPUT_FIELDS: tuple[str, ...] = (
    "asset",
    "current_price",
    "entry_price",
    "tp1",
    "tp2",
    "tp3",
    "stop_loss",
    "invalidation_level",
)

REQUIRED_OUTPUT_FIELDS: tuple[str, ...] = (
    "decision_status",
    "missing_data",
    "blockers",
    "human_decision_only",
    "no_order_no_sizing",
)

NUMERIC_INPUT_FIELDS: tuple[str, ...] = (
    "current_price",
    "entry_price",
    "tp1",
    "tp2",
    "tp3",
    "stop_loss",
    "invalidation_level",
)

FORBIDDEN_ACTION_FIELDS: tuple[str, ...] = (
    "requested_action",
    "action_request",
    "instructions",
    "order_request",
    "user_request",
)

FORBIDDEN_AUTO_ORDER_TOKENS: tuple[str, ...] = (
    "automatic order",
    "auto order",
    "automatic trailing",
    "auto trailing",
    "trailing stop order",
    "place order",
    "place an order",
    "execute order",
    "execute trade",
    "buy automatically",
    "sell automatically",
)


@dataclass(frozen=True)
class TradePlanResult:
    decision_status: str
    missing_data: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    human_decision_only: bool = True
    no_order_no_sizing: bool = True
    safety_markers: tuple[str, ...] = SAFETY_MARKERS
    notes: tuple[str, ...] = field(default_factory=tuple)


def _as_record(request: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(request, Mapping):
        raise TypeError("trade plan request must be a mapping")
    return dict(request)


def _is_present(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return True


def _is_number_like(value: object) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, Real):
        return math.isfinite(float(value))
    if isinstance(value, str) and value.strip():
        try:
            return math.isfinite(float(value))
        except ValueError:
            return False
    return False


def _missing_critical_data(record: Mapping[str, Any]) -> tuple[str, ...]:
    missing: list[str] = []

    asset = record.get("asset")
    if not isinstance(asset, str) or not asset.strip():
        missing.append("asset")

    for field_name in NUMERIC_INPUT_FIELDS:
        if not _is_number_like(record.get(field_name)):
            missing.append(field_name)

    return tuple(missing)


def _request_text(record: Mapping[str, Any]) -> str:
    chunks: list[str] = []
    for field_name in FORBIDDEN_ACTION_FIELDS:
        value = record.get(field_name)
        if _is_present(value):
            chunks.append(str(value))
    return " ".join(chunks).lower()


def _forbidden_order_blockers(record: Mapping[str, Any]) -> tuple[str, ...]:
    text = _request_text(record)
    blockers: list[str] = []

    explicit_order_flag = any(
        record.get(flag_name) is True
        for flag_name in (
            "auto_order",
            "automatic_order",
            "place_order",
            "execute_order",
            "broker_order",
        )
    )
    token_hit = any(token in text for token in FORBIDDEN_AUTO_ORDER_TOKENS)
    order_with_execution_language = "order" in text and any(
        token in text
        for token in (
            "automatic",
            "auto",
            "place",
            "execute",
            "trailing",
            "after tp",
            "after tp1",
        )
    )

    if explicit_order_flag or token_hit or order_with_execution_language:
        blockers.append("FORBIDDEN_AUTO_ORDER_REQUEST")

    if "trailing" in text or record.get("auto_trailing_order") is True:
        blockers.append("NO_AUTO_TRAILING_ORDER")

    return tuple(dict.fromkeys(blockers))


def evaluate_trade_plan_request(request: Mapping[str, Any]) -> TradePlanResult:
    """Evaluate a local-only trade plan request under the MVP QAIC safety contract.

    The function never creates orders, never sizes positions, never calls a broker,
    and never invents missing prices, take-profits, stop-losses, or trailing rules.
    """

    record = _as_record(request)
    missing_data = _missing_critical_data(record)
    blockers = _forbidden_order_blockers(record)

    if blockers:
        return TradePlanResult(
            decision_status="BLOCKED",
            missing_data=missing_data,
            blockers=blockers,
            notes=(
                "Forbidden automatic order request detected.",
                "Human review only; no broker/order/sizing action is permitted.",
            ),
        )

    if missing_data:
        return TradePlanResult(
            decision_status="REVIEW_REQUIRED",
            missing_data=missing_data,
            blockers=("MISSING_CRITICAL_DATA",),
            notes=(
                "Critical trade plan data is missing or invalid.",
                "No price, TP, SL, trailing rule, quantity, PnL, or exposure was invented.",
            ),
        )

    return TradePlanResult(
        decision_status="REVIEW_REQUIRED",
        missing_data=(),
        blockers=(),
        notes=(
            "Trade plan data is structurally complete.",
            "Human decision required; no broker/order/sizing action is permitted.",
        ),
    )


def trade_plan_result_to_dict(result: TradePlanResult) -> dict[str, object]:
    return {
        "decision_status": result.decision_status,
        "missing_data": list(result.missing_data),
        "blockers": list(result.blockers),
        "human_decision_only": result.human_decision_only,
        "no_order_no_sizing": result.no_order_no_sizing,
        "safety_markers": list(result.safety_markers),
        "notes": list(result.notes),
    }
