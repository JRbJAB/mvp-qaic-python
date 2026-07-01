from mvp_qaic_py.operator_workflow_qaic_bridge_status_r21d import (
    QAIC_BRIDGE_CONTRACT_ID,
    QAIC_BRIDGE_ROUTE,
    REFLEX_RUNTIME_STATUS,
    build_bridge_operator_status,
    render_static_preview_html,
    render_status_markdown,
)


def test_r21d_status_keeps_reflex_paused_and_bridge_visible() -> None:
    status = build_bridge_operator_status()

    assert status.reflex_runtime_status == "PAUSED"
    assert REFLEX_RUNTIME_STATUS == "PAUSED"
    assert status.qaic_bridge_contract_id == QAIC_BRIDGE_CONTRACT_ID
    assert status.qaic_bridge_route == QAIC_BRIDGE_ROUTE == "/qaic-bridge"
    assert status.qaic_execution_allowed is False
    assert status.human_review_required is True


def test_r21d_safety_flags_forbid_live_actions() -> None:
    flags = build_bridge_operator_status().safety_flags

    assert flags["no_runtime"] is True
    assert flags["no_docker"] is True
    assert flags["no_reflex_run"] is True
    assert flags["no_provider_call"] is True
    assert flags["no_broker_order_sizing"] is True
    assert flags["no_sheet_bq_write"] is True
    assert flags["no_apps_script_execution"] is True


def test_r21d_markdown_and_static_preview_include_operator_decision_data() -> None:
    markdown = render_status_markdown()
    html = render_static_preview_html()

    assert "WORKFLOW_ID=R21D_OPERATOR_WORKFLOW_QAIC_BRIDGE_STATUS_NO_RUNTIME" in markdown
    assert "REFLEX_RUNTIME_STATUS=PAUSED" in markdown
    assert "QAIC_EXECUTION_ALLOWED=False" in markdown
    assert "MVP_QAIC_TO_QAIC_BRIDGE_R1" in html
    assert "/qaic-bridge" in html
    assert "Product work continues without runtime blocking" in html
