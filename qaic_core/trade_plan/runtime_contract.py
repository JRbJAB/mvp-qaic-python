from __future__ import annotations

import math
from dataclasses import dataclass, field
from numbers import Real
from typing import Any, Mapping

CONTRACT_VERSION = "mvp_qaic.trade_plan_runtime.v2"

SAFETY_MARKERS: tuple[str, ...] = (
    "HUMAN_REVIEW_ONLY",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_AUTO_TRAILING_ORDER",
    "NO_SECRET",
    "NO_INVENTED_PRICE_TP_SL_TRAILING",
)

REQUIRED_RISK_GUARDS: tuple[str, ...] = (
    "HUMAN_REVIEW_ONLY",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
)

REQUIRED_INPUT_FIELDS: tuple[str, ...] = (
    "signal_id",
    "risk_guard",
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
    "contract_version",
    "decision_status",
    "missing_data",
    "blockers",
    "human_decision_only",
    "no_order_no_sizing",
    "safety_markers",
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

TEXT_INPUT_FIELDS: tuple[str, ...] = (
    "signal_id",
    "risk_guard",
    "asset",
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

FORBIDDEN_SIZING_TOKENS: tuple[str, ...] = (
    "position size",
    "size position",
    "sizing",
    "calculate size",
    "how much to buy",
    "quantity to buy",
    "qty to buy",
    "amount to buy",
    "order quantity",
)


@dataclass(frozen=True)
class TradePlanResult:
    decision_status: str
    missing_data: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    human_decision_only: bool = True
    no_order_no_sizing: bool = True
    safety_markers: tuple[str, ...] = SAFETY_MARKERS
    contract_version: str = CONTRACT_VERSION
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

    for field_name in TEXT_INPUT_FIELDS:
        value = record.get(field_name)
        if not isinstance(value, str) or not value.strip():
            missing.append(field_name)

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


def _risk_guard_blockers(record: Mapping[str, Any]) -> tuple[str, ...]:
    risk_guard = record.get("risk_guard")
    if not isinstance(risk_guard, str) or not risk_guard.strip():
        return ()
    normalized = {
        part.strip().upper()
        for part in risk_guard.replace("|", ",").replace(";", ",").split(",")
        if part.strip()
    }
    missing = [guard for guard in REQUIRED_RISK_GUARDS if guard not in normalized]
    if missing:
        return ("RISK_GUARD_INCOMPLETE",)
    return ()


def _forbidden_action_blockers(record: Mapping[str, Any]) -> tuple[str, ...]:
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
    order_token_hit = any(token in text for token in FORBIDDEN_AUTO_ORDER_TOKENS)
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

    if explicit_order_flag or order_token_hit or order_with_execution_language:
        blockers.append("FORBIDDEN_AUTO_ORDER_REQUEST")

    if "trailing" in text or record.get("auto_trailing_order") is True:
        blockers.append("NO_AUTO_TRAILING_ORDER")

    explicit_sizing_flag = any(
        record.get(flag_name) is True
        for flag_name in (
            "auto_sizing",
            "sizing",
            "calculate_position_size",
            "position_sizing",
        )
    )
    sizing_token_hit = any(token in text for token in FORBIDDEN_SIZING_TOKENS)

    if explicit_sizing_flag or sizing_token_hit:
        blockers.append("FORBIDDEN_SIZING_REQUEST")

    return tuple(dict.fromkeys(blockers))


def evaluate_trade_plan_request(request: Mapping[str, Any]) -> TradePlanResult:
    """Evaluate a local-only trade plan request under the MVP QAIC safety contract.

    The function never creates orders, never sizes positions, never calls a broker,
    and never invents missing prices, take-profits, stop-losses, or trailing rules.
    """

    record = _as_record(request)
    missing_data = _missing_critical_data(record)
    blockers = (*_risk_guard_blockers(record), *_forbidden_action_blockers(record))

    if blockers:
        return TradePlanResult(
            decision_status="BLOCKED",
            missing_data=missing_data,
            blockers=tuple(dict.fromkeys(blockers)),
            notes=(
                "Blocking safety rule detected.",
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
        "contract_version": result.contract_version,
        "decision_status": result.decision_status,
        "missing_data": list(result.missing_data),
        "blockers": list(result.blockers),
        "human_decision_only": result.human_decision_only,
        "no_order_no_sizing": result.no_order_no_sizing,
        "safety_markers": list(result.safety_markers),
        "notes": list(result.notes),
    }
