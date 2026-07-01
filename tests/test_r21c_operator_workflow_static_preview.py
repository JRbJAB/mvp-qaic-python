from pathlib import Path

from mvp_qaic_py.operator_workflow_static_preview_r21c import (
    build_workflow_model,
    model_to_dict,
    render_static_preview,
    write_preview,
)


def test_r21c_model_keeps_runtime_paused_and_review_only() -> None:
    model = build_workflow_model()

    assert model.version == "R21C"
    assert model.route_reference == "/qaic-bridge"
    assert model.bridge_contract == "MVP_QAIC_TO_QAIC_BRIDGE_R1"
    assert model.policy_flags["reflex_runtime_paused"] is True
    assert model.policy_flags["no_runtime"] is True
    assert model.policy_flags["no_docker"] is True
    assert model.policy_flags["no_provider_call"] is True
    assert model.policy_flags["no_broker_order_sizing"] is True
    assert model.policy_flags["no_sheet_bq_write"] is True
    assert model.policy_flags["qaic_execution_allowed"] is False
    assert model.policy_flags["handoff_mode"] == "review_only_local_handoff"


def test_r21c_static_preview_contains_operator_workflow_and_forbids_live_actions() -> None:
    html = render_static_preview()

    assert "MVP QAIC Operator Workflow" in html
    assert "/qaic-bridge" in html
    assert "No Docker" in html
    assert "no-runtime" in html.lower()
    assert "broker/order/sizing" in html
    assert "MVP_QAIC_TO_QAIC_BRIDGE_R1" in html


def test_r21c_write_preview_outputs_html_and_manifest(tmp_path: Path) -> None:
    html_path, manifest_path = write_preview(tmp_path)

    assert html_path.exists()
    assert manifest_path.exists()
    assert "Operator Workflow" in html_path.read_text(encoding="utf-8")
    manifest = manifest_path.read_text(encoding="utf-8")
    assert "MVP_QAIC_TO_QAIC_BRIDGE_R1" in manifest
    assert model_to_dict(build_workflow_model())["policy_flags"]["no_runtime"] is True
