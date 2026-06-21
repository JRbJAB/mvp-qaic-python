from __future__ import annotations

from typing import Any, Mapping

from qaic_core.live.live_contract import (
    LIVE_READONLY_MODE,
    REQUIRED_LIVE_SAFETY_MARKERS,
    LiveRuntimeInput,
    LiveRuntimeResult,
)
from qaic_core.trade_plan.runtime_contract import (
    evaluate_trade_plan_request,
)


def _normalize_live_input(payload: Mapping[str, Any] | LiveRuntimeInput) -> LiveRuntimeInput:
    if isinstance(payload, LiveRuntimeInput):
        return payload
    if not isinstance(payload, Mapping):
        raise TypeError("live runtime payload must be a mapping or LiveRuntimeInput")
    return LiveRuntimeInput(
        mode=str(payload.get("mode", LIVE_READONLY_MODE)),
        provider=str(payload.get("provider", "LOCAL_PAYLOAD")),
        payload=dict(payload.get("payload", payload)),
    )


def _missing_live_safety_markers(input_record: LiveRuntimeInput) -> tuple[str, ...]:
    declared = {marker.upper() for marker in input_record.safety_markers}
    return tuple(
        marker for marker in REQUIRED_LIVE_SAFETY_MARKERS if marker.upper() not in declared
    )


def evaluate_live_trade_plan(payload: Mapping[str, Any] | LiveRuntimeInput) -> LiveRuntimeResult:
    """Evaluate a live-read-only trade plan payload.

    P63 intentionally performs no network call, no broker call, no order creation,
    and no sizing. Real public-market providers are introduced only after this
    live-read-only contract is sealed.
    """

    live_input = _normalize_live_input(payload)
    missing_safety = _missing_live_safety_markers(live_input)

    blockers: list[str] = []
    if live_input.mode != LIVE_READONLY_MODE:
        blockers.append("LIVE_MODE_NOT_READONLY")
    if missing_safety:
        blockers.append("LIVE_SAFETY_MARKERS_INCOMPLETE")

    trade_result = evaluate_trade_plan_request(live_input.payload)

    if trade_result.decision_status == "BLOCKED":
        blockers.extend(trade_result.blockers)

    decision_status = "BLOCKED" if blockers else "REVIEW_REQUIRED"

    return LiveRuntimeResult(
        mode=LIVE_READONLY_MODE,
        provider=live_input.provider,
        decision_status=decision_status,
        missing_data=trade_result.missing_data,
        blockers=tuple(dict.fromkeys(blockers)),
        human_decision_only=True,
        no_order_no_sizing=True,
        safety_markers=REQUIRED_LIVE_SAFETY_MARKERS,
        live_readonly=True,
        network_called=False,
        broker_called=False,
        order_created=False,
        sizing_created=False,
        notes=(
            "Python live foundation active in read-only mode.",
            "No provider network call is performed in P63.",
            "No broker/order/sizing action is permitted.",
        ),
    )
