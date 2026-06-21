from __future__ import annotations

import pytest

from mvp_qaic_py.bridge.local_bridge_dryrun import (
    LOCAL_BRIDGE_ROUTES,
    assert_local_bridge_is_readonly,
    build_local_bridge_dryrun_payload,
)


def test_p83b_local_bridge_dryrun_ready() -> None:
    payload = build_local_bridge_dryrun_payload()

    assert payload["status"] == "OK_P83B_LOCAL_BRIDGE_DRYRUN_MODULE_READY"
    assert payload["contract_status"] == "OK_P81R_P82_LIVE_SHEETS_CONTRACT_READY"
    assert payload["planned_route_count"] == 4
    assert payload["write_route_count"] == 0
    assert payload["human_approval_required_count"] == 1
    assert payload["next"] == "P83C_PUSH_OR_P84_LOCAL_OPERATOR_BRIDGE_SMOKE"


def test_p83b_routes_are_readonly_or_dryrun_only() -> None:
    payload = build_local_bridge_dryrun_payload()

    for route in payload["planned_routes"]:
        assert route["write_allowed"] is False
        assert route["mode"] in {"DRY_RUN_ONLY", "READ_ONLY"}


def test_p83b_expected_routes_present() -> None:
    route_ids = {route.route_id for route in LOCAL_BRIDGE_ROUTES}

    assert "P83_ROUTE_PAYLOAD_TO_OPERATOR_REVIEW" in route_ids
    assert "P83_ROUTE_RESPONSE_INTAKE_TO_JOURNAL_QUEUE" in route_ids
    assert "P83_ROUTE_JOURNAL_QUEUE_TO_DECISION_JOURNAL" in route_ids
    assert "P83_ROUTE_RUNTIME_STATUS_READ" in route_ids


def test_p83b_readonly_assertion_passes() -> None:
    payload = build_local_bridge_dryrun_payload()
    assert_local_bridge_is_readonly(payload)


def test_p83b_readonly_assertion_blocks_write_route() -> None:
    payload = build_local_bridge_dryrun_payload()
    payload["planned_routes"][0]["write_allowed"] = True

    with pytest.raises(ValueError, match="Write routes are forbidden"):
        assert_local_bridge_is_readonly(payload)


def test_p83b_contract_gap_requires_review() -> None:
    payload = build_local_bridge_dryrun_payload(available_tabs=("GPT_INPUT_PAYLOADS",))

    assert payload["status"] == "REVIEW_REQUIRED_P83B_CONTRACT_GAP"
    assert payload["planned_route_count"] == 4
    assert all(route["status"] == "BLOCKED_BY_CONTRACT" for route in payload["planned_routes"])
