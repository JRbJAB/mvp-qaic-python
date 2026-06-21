from __future__ import annotations

import pytest

from qaic_core.contracts.migration import (
    MIGRATION_SAFETY_MARKERS,
    contract_spec_to_dict,
    contract_validation_result_to_dict,
    get_contract,
    list_contract_ids,
    migration_contract_registry,
    validate_contract_record,
    validate_contract_records,
)


def complete_trade_plan_row() -> dict[str, object]:
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


def test_registry_contains_core_migration_contracts() -> None:
    assert list_contract_ids() == (
        "decision_journal.v1",
        "public_market_snapshot.v1",
        "runtime_output.v1",
        "trade_plan_input.v1",
    )
    assert set(migration_contract_registry()) == set(list_contract_ids())


def test_trade_plan_contract_passes_complete_row() -> None:
    contract = get_contract("trade_plan_input.v1")
    result = validate_contract_record(complete_trade_plan_row(), contract)
    payload = contract_validation_result_to_dict(result)

    assert payload["status"] == "PASS"
    assert payload["missing_fields"] == []
    assert payload["empty_fields"] == []
    assert payload["blockers"] == []


def test_trade_plan_contract_reports_missing_and_empty_fields() -> None:
    contract = get_contract("trade_plan_input.v1")
    row = {
        "signal_id": "",
        "risk_guard": "HUMAN_REVIEW_ONLY,NO_BROKER,NO_ORDER,NO_SIZING",
        "asset": "BTC",
    }

    result = validate_contract_record(row, contract)
    payload = contract_validation_result_to_dict(result)

    assert payload["status"] == "REVIEW_REQUIRED"
    assert "current_price" in payload["missing_fields"]
    assert "entry_price" in payload["missing_fields"]
    assert "signal_id" in payload["empty_fields"]
    assert "MISSING_REQUIRED_FIELDS" in payload["blockers"]
    assert "EMPTY_REQUIRED_FIELDS" in payload["blockers"]


def test_unexpected_fields_are_advisory_by_default() -> None:
    contract = get_contract("trade_plan_input.v1")
    row = complete_trade_plan_row()
    row["extra_column"] = "kept for review"

    result = validate_contract_record(row, contract)
    payload = contract_validation_result_to_dict(result)

    assert payload["status"] == "PASS"
    assert payload["unexpected_fields"] == ["extra_column"]
    assert "UNEXPECTED_FIELDS" not in payload["blockers"]


def test_unexpected_fields_can_be_blocked_for_strict_migration() -> None:
    contract = get_contract("trade_plan_input.v1")
    row = complete_trade_plan_row()
    row["extra_column"] = "bad"

    result = validate_contract_record(row, contract, allow_unexpected_fields=False)
    payload = contract_validation_result_to_dict(result)

    assert payload["status"] == "REVIEW_REQUIRED"
    assert payload["unexpected_fields"] == ["extra_column"]
    assert "UNEXPECTED_FIELDS" in payload["blockers"]


def test_validate_multiple_records_aggregates_counts_and_fields() -> None:
    contract = get_contract("trade_plan_input.v1")
    bad_row = {"signal_id": "SIG-2", "risk_guard": "", "asset": "ETH"}

    result = validate_contract_records([complete_trade_plan_row(), bad_row], contract)
    payload = contract_validation_result_to_dict(result)

    assert payload["status"] == "REVIEW_REQUIRED"
    assert payload["row_count"] == 2
    assert payload["valid_row_count"] == 1
    assert payload["invalid_row_count"] == 1
    assert "risk_guard" in payload["empty_fields"]
    assert "current_price" in payload["missing_fields"]


def test_empty_record_sequence_requires_review() -> None:
    contract = get_contract("decision_journal.v1")
    result = validate_contract_records([], contract)
    payload = contract_validation_result_to_dict(result)

    assert payload["status"] == "REVIEW_REQUIRED"
    assert payload["row_count"] == 0
    assert payload["blockers"] == ["NO_ROWS"]


def test_public_market_snapshot_contract_matches_provider_shape() -> None:
    contract = get_contract("public_market_snapshot.v1")
    row = {
        "provider_version": "mvp_qaic.public_market_provider_readonly.v1",
        "provider": "PUBLIC_MARKET_READONLY",
        "asset": "BTC",
        "symbol": "BTC",
        "current_price": 68000,
        "quote_currency": "USD",
        "status": "OK",
        "live_readonly": True,
        "network_called": True,
        "broker_called": False,
        "order_created": False,
        "sizing_created": False,
    }

    result = validate_contract_record(row, contract)
    assert result.status == "PASS"


def test_contract_spec_to_dict_is_stable() -> None:
    contract = get_contract("runtime_output.v1")
    payload = contract_spec_to_dict(contract)

    assert payload["contract_id"] == "runtime_output.v1"
    assert payload["version"] == "mvp_qaic.migration_contracts.v1"
    assert payload["safety_markers"] == list(MIGRATION_SAFETY_MARKERS)
    field_names = [field["name"] for field in payload["fields"]]
    assert "decision_status" in field_names
    assert "no_order_no_sizing" in field_names


def test_unknown_contract_fails_controlled() -> None:
    with pytest.raises(KeyError, match="unknown migration contract"):
        get_contract("missing.v1")


def test_migration_safety_markers_are_explicit() -> None:
    assert MIGRATION_SAFETY_MARKERS == (
        "MIGRATION_READONLY",
        "SCHEMA_VALIDATION_ONLY",
        "NO_GOOGLE_LIVE_WRITE",
        "NO_SHEET_WRITE",
        "NO_BROKER",
        "NO_ORDER",
        "NO_SIZING",
        "NO_SECRET",
    )
