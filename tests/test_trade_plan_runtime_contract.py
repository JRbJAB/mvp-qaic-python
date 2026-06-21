from __future__ import annotations

import pytest

from qaic_core.trade_plan.runtime_contract import (
    CONTRACT_VERSION,
    REQUIRED_OUTPUT_FIELDS,
    REQUIRED_RISK_GUARDS,
    SAFETY_MARKERS,
    evaluate_trade_plan_request,
    trade_plan_result_to_dict,
)


def complete_trade_plan_request() -> dict[str, object]:
    return {
        "signal_id": "SIG-BTC-001",
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


def test_complete_trade_plan_remains_human_review_only() -> None:
    result = evaluate_trade_plan_request(complete_trade_plan_request())
    payload = trade_plan_result_to_dict(result)

    assert payload["contract_version"] == CONTRACT_VERSION
    assert payload["decision_status"] == "REVIEW_REQUIRED"
    assert payload["missing_data"] == []
    assert payload["blockers"] == []
    assert payload["human_decision_only"] is True
    assert payload["no_order_no_sizing"] is True
    assert "HUMAN_REVIEW_ONLY" in payload["safety_markers"]
    assert "NO_ORDER" in payload["safety_markers"]
    assert "NO_SIZING" in payload["safety_markers"]


def test_missing_critical_data_returns_review_required_without_invention() -> None:
    result = evaluate_trade_plan_request(
        {
            "asset": "ETH",
            "current_price": 3100,
            "entry_price": 3000,
        }
    )
    payload = trade_plan_result_to_dict(result)

    assert payload["decision_status"] == "REVIEW_REQUIRED"
    assert "signal_id" in payload["missing_data"]
    assert "risk_guard" in payload["missing_data"]
    assert "tp1" in payload["missing_data"]
    assert "tp2" in payload["missing_data"]
    assert "tp3" in payload["missing_data"]
    assert "stop_loss" in payload["missing_data"]
    assert "invalidation_level" in payload["missing_data"]
    assert "MISSING_CRITICAL_DATA" in payload["blockers"]
    assert payload["human_decision_only"] is True
    assert payload["no_order_no_sizing"] is True
    assert "NO_INVENTED_PRICE_TP_SL_TRAILING" in payload["safety_markers"]


def test_incomplete_risk_guard_is_blocked() -> None:
    request = complete_trade_plan_request()
    request["risk_guard"] = "HUMAN_REVIEW_ONLY,NO_BROKER"

    result = evaluate_trade_plan_request(request)
    payload = trade_plan_result_to_dict(result)

    assert payload["decision_status"] == "BLOCKED"
    assert "RISK_GUARD_INCOMPLETE" in payload["blockers"]


def test_required_risk_guards_contract_is_explicit() -> None:
    assert REQUIRED_RISK_GUARDS == (
        "HUMAN_REVIEW_ONLY",
        "NO_BROKER",
        "NO_ORDER",
        "NO_SIZING",
    )


def test_forbidden_automatic_trailing_order_is_blocked() -> None:
    request = complete_trade_plan_request()
    request["requested_action"] = "Place an automatic trailing stop order after TP1."

    result = evaluate_trade_plan_request(request)
    payload = trade_plan_result_to_dict(result)

    assert payload["decision_status"] == "BLOCKED"
    assert "FORBIDDEN_AUTO_ORDER_REQUEST" in payload["blockers"]
    assert "NO_AUTO_TRAILING_ORDER" in payload["blockers"]
    assert payload["human_decision_only"] is True
    assert payload["no_order_no_sizing"] is True
    assert "NO_AUTO_TRAILING_ORDER" in payload["safety_markers"]


def test_forbidden_boolean_order_flag_is_blocked() -> None:
    request = complete_trade_plan_request()
    request["auto_order"] = True

    result = evaluate_trade_plan_request(request)
    payload = trade_plan_result_to_dict(result)

    assert payload["decision_status"] == "BLOCKED"
    assert "FORBIDDEN_AUTO_ORDER_REQUEST" in payload["blockers"]


def test_forbidden_sizing_request_is_blocked() -> None:
    request = complete_trade_plan_request()
    request["requested_action"] = "Calculate position size and quantity to buy."

    result = evaluate_trade_plan_request(request)
    payload = trade_plan_result_to_dict(result)

    assert payload["decision_status"] == "BLOCKED"
    assert "FORBIDDEN_SIZING_REQUEST" in payload["blockers"]
    assert payload["no_order_no_sizing"] is True


def test_forbidden_boolean_sizing_flag_is_blocked() -> None:
    request = complete_trade_plan_request()
    request["auto_sizing"] = True

    result = evaluate_trade_plan_request(request)
    payload = trade_plan_result_to_dict(result)

    assert payload["decision_status"] == "BLOCKED"
    assert "FORBIDDEN_SIZING_REQUEST" in payload["blockers"]


def test_invalid_numeric_field_is_missing_data() -> None:
    request = complete_trade_plan_request()
    request["tp1"] = "not-a-number"

    result = evaluate_trade_plan_request(request)
    payload = trade_plan_result_to_dict(result)

    assert payload["decision_status"] == "REVIEW_REQUIRED"
    assert "tp1" in payload["missing_data"]
    assert "MISSING_CRITICAL_DATA" in payload["blockers"]


def test_required_output_contract_keys_are_present() -> None:
    payload = trade_plan_result_to_dict(evaluate_trade_plan_request(complete_trade_plan_request()))

    for field_name in REQUIRED_OUTPUT_FIELDS:
        assert field_name in payload


def test_safety_marker_contract_is_complete() -> None:
    assert SAFETY_MARKERS == (
        "HUMAN_REVIEW_ONLY",
        "NO_BROKER",
        "NO_ORDER",
        "NO_SIZING",
        "NO_AUTO_TRAILING_ORDER",
        "NO_SECRET",
        "NO_INVENTED_PRICE_TP_SL_TRAILING",
    )


def test_trade_plan_result_is_deterministic() -> None:
    first = trade_plan_result_to_dict(evaluate_trade_plan_request(complete_trade_plan_request()))
    second = trade_plan_result_to_dict(evaluate_trade_plan_request(complete_trade_plan_request()))

    assert first == second


def test_non_mapping_request_is_rejected() -> None:
    with pytest.raises(TypeError, match="trade plan request must be a mapping"):
        evaluate_trade_plan_request("BTC")  # type: ignore[arg-type]
