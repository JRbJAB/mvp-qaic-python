from mvp_qaic_reflex_ui.common.tracker_ui_tool_deployment import deployment_status


def test_reflex_kit_preview_public_deploy_gate_is_closed_until_runtime_visual_match():
    status = deployment_status()

    assert status.ui_tracker_tool_deployed is True
    assert status.reflex_public_deploy_allowed is False
    assert (
        status.reflex_public_deploy_status
        == "BLOCKED_UNTIL_REAL_REFLEX_BROWSER_RUNTIME_VISUAL_MATCH"
    )


def test_reflex_kit_preview_gate_keeps_static_preview_separate_from_public_deploy():
    status = deployment_status()

    assert status.static_preview_supported is True
    assert status.approved_oracle_ok is True
    assert status.reflex_public_deploy_allowed is False
