from pathlib import Path

from mvp_qaic_py.operator_reference_binding_handoff_r21i import (
    HANDOFF_MODE,
    SOURCE_BINDING,
    build_operator_reference_handoff,
    handoff_to_dict,
    render_handoff_markdown,
    validate_handoff,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_handoff_validates_safety_and_reference_families() -> None:
    handoff = build_operator_reference_handoff()

    assert handoff.status == "READY_FOR_QAIC_REFERENCE_REVIEW_ONLY_HANDOFF"
    assert handoff.source_binding == SOURCE_BINDING
    assert handoff.handoff_mode == HANDOFF_MODE
    assert validate_handoff(handoff) == []

    families = {item.family for item in handoff.references}
    assert {"ui_tracker", "tool_registry", "cdc", "bridge", "operator_workflow"} <= families


def test_handoff_has_no_runtime_or_live_write_escape_hatches() -> None:
    data = handoff_to_dict()
    flags = data["safety_flags"]

    assert flags["no_runtime"] is True
    assert flags["no_docker"] is True
    assert flags["no_reflex_run"] is True
    assert flags["no_provider_call"] is True
    assert flags["no_broker_order_sizing"] is True
    assert flags["no_sheet_bq_write"] is True
    assert flags["no_apps_script_execution"] is True
    assert flags["human_review_required"] is True
    assert flags["qaic_execution_allowed"] is False


def test_markdown_is_review_only_and_contains_bound_references() -> None:
    markdown = render_handoff_markdown()

    assert "R21H_UI_TRACKER_TOOL_REGISTRY_CDC_OPERATOR_WORKFLOW_BINDING" in markdown
    assert "docs/dev_tracking/TRACKER_RENDER_REFERENCE_REGISTRY.md" in markdown
    assert "data/tool_registry/tools_project_mvp_qaic.json" in markdown
    assert "MVP_QAIC_CDC_CONTRACT_FINAL_FUSED_v0.2.6.md" in markdown
    assert "MVP_QAIC_TO_QAIC_BRIDGE_R1" in markdown
    assert ".html" not in markdown.lower()
    assert "05_EXPORTS" not in markdown
    assert "reflex run" not in markdown.lower()


def test_source_reference_files_exist_or_are_suffix_resolvable() -> None:
    direct_paths = [
        "docs/FINAL/CURRENT_REFERENCE_INDEX.md",
        "docs/FINAL/R21F_DRIVE_FIRST_REFERENCE_LOCK_MEMO_20260701.md",
        "docs/PRODUCT/R21H_UI_TRACKER_TOOL_REGISTRY_CDC_OPERATOR_WORKFLOW_BINDING_NO_RUNTIME.md",
        "mvp_qaic_py/operator_workflow_reference_binding_r21h.py",
        "docs/dev_tracking/TRACKER_RENDER_REFERENCE_REGISTRY.md",
        "docs/dev_tracking/ui_tracker_tool_manifest.json",
        "docs/BRIDGE/MVP_QAIC_TO_QAIC_BRIDGE_CONTRACT_R1.md",
        "data/tool_registry/tools_project_mvp_qaic.json",
    ]
    for rel_path in direct_paths:
        assert (REPO_ROOT / rel_path).exists(), rel_path

    cdc_matches = list((REPO_ROOT / "docs/FINAL").glob("*MVP_QAIC_CDC_CONTRACT_FINAL_FUSED_v0.2.6.md"))
    assert len(cdc_matches) == 1
