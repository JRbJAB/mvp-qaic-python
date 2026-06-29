from mvp_qaic_reflex_ui.common.tracker_ui_tool_deployment import (
    REFLEX_PUBLIC_DEPLOY_STATUS_BLOCKED,
    TRACKER_RENDER_TYPES,
    TRACKER_TOOL_ROUTES,
    approved_oracle_path,
    deployment_status,
    validate_approved_oracle,
)


def test_ui_tracker_tool_deployment_status_is_ready_but_public_deploy_blocked():
    status = deployment_status()

    assert approved_oracle_path().exists()
    assert status.ui_tracker_tool_deployed is True
    assert status.approved_oracle_ok is True
    assert status.static_preview_supported is True
    assert status.reflex_public_deploy_allowed is False
    assert status.reflex_public_deploy_status == REFLEX_PUBLIC_DEPLOY_STATUS_BLOCKED
    assert status.status == "UI_TRACKER_TOOL_DEPLOYED_REFLEX_PUBLIC_DEPLOY_BLOCKED"


def test_ui_tracker_tool_routes_and_render_types_are_declared():
    assert "/dev-tracking" in TRACKER_TOOL_ROUTES
    assert "/cdc-dev-tracker" in TRACKER_TOOL_ROUTES
    assert "/cdc-tracker" in TRACKER_TOOL_ROUTES
    assert "migration_tracker_oracle" in TRACKER_RENDER_TYPES
    assert "cdc_dev_tracker" in TRACKER_RENDER_TYPES
    assert "dev_tracker" in TRACKER_RENDER_TYPES


def test_approved_visual_oracle_tokens_are_enforced():
    oracle_ok, missing, blue_visual_ok = validate_approved_oracle()

    assert oracle_ok is True
    assert missing == ()
    assert blue_visual_ok is True
