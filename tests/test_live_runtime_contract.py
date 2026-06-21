from __future__ import annotations

import pytest

from qaic_core.live.live_contract import (
    LIVE_READONLY_MODE,
    REQUIRED_LIVE_SAFETY_MARKERS,
    LiveRuntimeInput,
    live_runtime_result_to_dict,
)
from qaic_core.live.runtime import evaluate_live_trade_plan


def complete_live_payload() -> dict[str, object]:
    return {
        "signal_id": "SIG-BTC-LIVE-001",
        "risk_guard": "HUMAN_REVIEW_ONLY,NO_BROKER,NO_ORDER,NO_SIZING",
        "asset": "BTC",
        "current_price": 68000,
        "entry_price": 67200,
        "tp1": 70000,
        "tp2": 73500,
        "tp3": 78000,
        "stop_loss": 65000,
        "invalidation_level": 65000,
    }


def test_live_runtime_foundation_is_readonly_and_human_review_only() -> None:
    result = evaluate_live_trade_plan(complete_live_payload())
    payload = live_runtime_result_to_dict(result)

    assert payload["mode"] == "LIVE_READONLY"
    assert payload["decision_status"] == "REVIEW_REQUIRED"
    assert payload["human_decision_only"] is True
    assert payload["no_order_no_sizing"] is True
    assert payload["live_readonly"] is True
    assert payload["network_called"] is False
    assert payload["broker_called"] is False
    assert payload["order_created"] is False
    assert payload["sizing_created"] is False


def test_live_runtime_requires_readonly_mode() -> None:
    live_input = LiveRuntimeInput(
        mode="LIVE_EXECUTION",
        provider="LOCAL_PAYLOAD",
        payload=complete_live_payload(),
    )

    result = evaluate_live_trade_plan(live_input)
    payload = live_runtime_result_to_dict(result)

    assert payload["decision_status"] == "BLOCKED"
    assert "LIVE_MODE_NOT_READONLY" in payload["blockers"]
    assert payload["network_called"] is False
    assert payload["order_created"] is False


def test_live_runtime_safety_markers_are_explicit() -> None:
    assert REQUIRED_LIVE_SAFETY_MARKERS == (
        "LIVE_READONLY",
        "HUMAN_REVIEW_ONLY",
        "NO_BROKER",
        "NO_ORDER",
        "NO_SIZING",
        "NO_AUTO_TRAILING_ORDER",
        "NO_SECRET",
        "NO_NETWORK_CALL_BY_DEFAULT",
    )


def test_live_runtime_blocks_incomplete_safety_markers() -> None:
    live_input = LiveRuntimeInput(
        mode=LIVE_READONLY_MODE,
        provider="LOCAL_PAYLOAD",
        payload=complete_live_payload(),
        safety_markers=("LIVE_READONLY", "HUMAN_REVIEW_ONLY"),
    )

    result = evaluate_live_trade_plan(live_input)
    payload = live_runtime_result_to_dict(result)

    assert payload["decision_status"] == "BLOCKED"
    assert "LIVE_SAFETY_MARKERS_INCOMPLETE" in payload["blockers"]


def test_live_runtime_propagates_trade_plan_blockers() -> None:
    record = complete_live_payload()
    record["requested_action"] = "Place an automatic trailing stop order after TP1."

    result = evaluate_live_trade_plan(record)
    payload = live_runtime_result_to_dict(result)

    assert payload["decision_status"] == "BLOCKED"
    assert "FORBIDDEN_AUTO_ORDER_REQUEST" in payload["blockers"]
    assert "NO_AUTO_TRAILING_ORDER" in payload["blockers"]
    assert payload["broker_called"] is False
    assert payload["order_created"] is False


def test_live_runtime_propagates_missing_trade_plan_data() -> None:
    result = evaluate_live_trade_plan(
        {
            "signal_id": "SIG-MISSING-001",
            "risk_guard": "HUMAN_REVIEW_ONLY,NO_BROKER,NO_ORDER,NO_SIZING",
            "asset": "ETH",
        }
    )
    payload = live_runtime_result_to_dict(result)

    assert payload["decision_status"] == "REVIEW_REQUIRED"
    assert "current_price" in payload["missing_data"]
    assert "entry_price" in payload["missing_data"]
    assert payload["network_called"] is False


def test_live_runtime_rejects_non_mapping_payload() -> None:
    with pytest.raises(TypeError, match="live runtime payload must be a mapping"):
        evaluate_live_trade_plan("BTC")  # type: ignore[arg-type]


def test_live_runtime_is_deterministic() -> None:
    first = live_runtime_result_to_dict(evaluate_live_trade_plan(complete_live_payload()))
    second = live_runtime_result_to_dict(evaluate_live_trade_plan(complete_live_payload()))

    assert first == second
