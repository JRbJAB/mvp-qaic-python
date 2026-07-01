from __future__ import annotations

from pathlib import Path

from mvp_qaic_py.operator_workflow_reference_binding_r21h import (
    POLICY_FLAGS,
    REFERENCE_BINDINGS,
    build_operator_reference_binding_model,
    model_to_dict,
    render_binding_markdown,
    validate_reference_sources,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_r21h_binds_required_tracker_tool_registry_and_cdc_keys() -> None:
    keys = {binding.key for binding in REFERENCE_BINDINGS}
    assert "cdc_dev_tracker" in keys
    assert "dev_tracker" in keys
    assert "tool_registry_cdc" in keys
    assert "cdc_tracker" in keys
    assert "ui_tracker_tool_manifest" in keys
    assert "tool_registry_export" in keys
    assert "tool_registry_snapshot" in keys
    assert "cdc_final_contract" in keys
    assert "r21d_qaic_bridge_status" in keys
    assert "r21e_decision_journal_handoff" in keys


def test_r21h_reference_sources_validate_from_current_repo() -> None:
    validations = validate_reference_sources(REPO_ROOT)
    assert validations
    assert all(item.exists for item in validations), [item for item in validations if not item.exists]
    assert all(item.required_terms_ok for item in validations), [item for item in validations if not item.required_terms_ok]


def test_r21h_model_is_no_runtime_and_review_only() -> None:
    model = build_operator_reference_binding_model(REPO_ROOT)
    payload = model_to_dict(model)
    flags = payload["policy_flags"]
    assert payload["workflow"] == "R21H_BIND_UI_TRACKER_TOOL_REGISTRY_CDC_TO_OPERATOR_WORKFLOW_NO_RUNTIME"
    assert flags["drive_first_reference_lock_applied"] is True
    assert flags["no_runtime"] is True
    assert flags["no_reflex_run"] is True
    assert flags["no_docker"] is True
    assert flags["no_provider_call"] is True
    assert flags["no_broker_order_sizing"] is True
    assert flags["no_sheet_bq_write"] is True
    assert flags["qaic_execution_allowed"] is False
    assert model.status == "READY_FOR_OPERATOR_REVIEW_BINDING"


def test_r21h_markdown_output_does_not_create_html_or_preview_contract() -> None:
    markdown = render_binding_markdown(build_operator_reference_binding_model(REPO_ROOT))
    lowered = markdown.lower()
    assert "<html" not in lowered
    assert "index.html" not in lowered
    assert "05_exports" not in lowered
    assert POLICY_FLAGS["no_html_preview_output"] is True
