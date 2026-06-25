from mvp_qaic_py.reflex_app.preview_selector import (
    build_private_preview_command,
    build_private_preview_selector_payload,
    selector_is_safe_for_local_private_preview,
)


def test_private_preview_command_is_manual_local_only():
    command = build_private_preview_command()

    assert command.host == "127.0.0.1"
    assert command.port == 3000
    assert command.server_start_allowed is False
    assert command.browser_open_allowed is False
    assert command.public_deploy_allowed is False
    assert command.live_action_allowed is False
    assert command.operator_must_run_manually is True
    assert "reflex" in command.command


def test_private_preview_selector_payload_is_safe():
    payload = build_private_preview_selector_payload()

    assert payload["selector_status"] == "READY_FOR_MANUAL_PRIVATE_PREVIEW"
    assert payload["server_start_allowed_now"] is False
    assert payload["browser_open_allowed_now"] is False
    assert payload["public_deploy_allowed"] is False
    assert payload["live_action_allowed"] is False
    assert payload["operator_must_run_manually"] is True
    assert payload["data_binding_mode"] == "LOCAL_READONLY"
    assert payload["host"] == "127.0.0.1"
    assert payload["ui_navigation_group_count"] == 6
    assert payload["ui_navigation_item_count"] >= 16
    assert payload["docs_source_count"] >= 3
    assert payload["export_source_count"] >= 1


def test_private_preview_selector_global_safety_boolean():
    assert selector_is_safe_for_local_private_preview() is True
