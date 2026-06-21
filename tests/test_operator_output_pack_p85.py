from __future__ import annotations

from mvp_qaic_py.operator.operator_output_pack import (
    build_operator_output_pack,
    render_operator_output_markdown,
)


def test_p85a_operator_output_pack_ready() -> None:
    pack = build_operator_output_pack()

    assert pack["status"] == "OK_P85A_OPERATOR_OUTPUT_PACK_READY"
    assert pack["bridge_status"] == "OK_P83B_LOCAL_BRIDGE_DRYRUN_MODULE_READY"
    assert pack["contract_status"] == "OK_P81R_P82_LIVE_SHEETS_CONTRACT_READY"
    assert pack["planned_route_count"] == 4
    assert pack["ready_route_count"] == 3
    assert pack["human_approval_required_count"] == 1
    assert pack["blocked_route_count"] == 0
    assert pack["write_route_count"] == 0


def test_p85a_operator_output_pack_safety_flags() -> None:
    pack = build_operator_output_pack()

    assert pack["sheet_write"] is False
    assert pack["apps_script_execution"] is False
    assert pack["clasp_push"] is False
    assert pack["broker_execution"] is False
    assert pack["order_execution"] is False
    assert pack["auto_sizing_execution"] is False
    assert pack["google_rest_local_diag"] is False


def test_p85a_blocks_unknown_action() -> None:
    pack = build_operator_output_pack(requested_action="APPEND_TO_SHEET")

    assert pack["status"] == "BLOCKED_P85A_OPERATOR_OUTPUT_PACK"
    assert pack["action_allowed"] is False
    assert pack["blocked_reason"] == "UNSAFE_OR_UNKNOWN_OPERATOR_ACTION"
    assert pack["write_route_count"] == 0


def test_p85a_markdown_render_contains_required_sections() -> None:
    pack = build_operator_output_pack()
    markdown = render_operator_output_markdown(pack)

    assert "P85A Operator Output Pack" in markdown
    assert "OK_P85A_OPERATOR_OUTPUT_PACK_READY" in markdown
    assert "NO_SHEET_WRITE" in markdown
    assert "P83_ROUTE_JOURNAL_QUEUE_TO_DECISION_JOURNAL" in markdown
    assert "HUMAN_APPROVAL_REQUIRED" in markdown
