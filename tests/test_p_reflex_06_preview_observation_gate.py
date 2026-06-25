from mvp_qaic_py.reflex_app.preview_observation_gate import (
    build_preview_observation_gate,
    build_preview_observation_payload,
    gate_is_safe_and_ready,
)


def test_observation_gate_does_not_start_server_or_browser():
    gate = build_preview_observation_gate()

    assert gate.gate_status == "READY_FOR_OPERATOR_MANUAL_RUN"
    assert gate.expected_local_url == "http://127.0.0.1:3000"
    assert gate.server_started_by_gate is False
    assert gate.browser_opened_by_gate is False
    assert gate.public_deploy_allowed is False
    assert gate.live_action_allowed is False
    assert gate.observation_required is True


def test_observation_payload_is_selector_safe():
    payload = build_preview_observation_payload()

    assert payload["selector_safe"] is True
    assert payload["data_binding_mode"] == "LOCAL_READONLY"
    assert payload["ui_navigation_group_count"] == 6
    assert payload["ui_navigation_item_count"] >= 16
    assert payload["manual_command"][0] == "python"
    assert "reflex" in payload["manual_command"]
    assert payload["expected_local_url"] == "http://127.0.0.1:3000"


def test_gate_is_safe_and_ready():
    assert gate_is_safe_and_ready() is True
