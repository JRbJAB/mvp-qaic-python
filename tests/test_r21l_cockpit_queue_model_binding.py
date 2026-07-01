from __future__ import annotations

from pathlib import Path

from mvp_qaic_py.cockpit_queue_data_contract_r21k import contract_to_dict
from mvp_qaic_py.cockpit_queue_model_binding_r21l import (
    MODEL_ID,
    build_cockpit_queue_model,
    list_cockpit_rows,
    list_cockpit_sections,
    render_cockpit_queue_model_markdown,
    validate_cockpit_queue_model,
)


def test_r21l_binds_r21k_contract_semantics() -> None:
    source = contract_to_dict()
    model = build_cockpit_queue_model()

    assert model["model_id"] == MODEL_ID
    assert model["source_contract"]["contract_id"] == source["contract_id"]
    assert model["source_contract"]["status"] == source["status"]
    assert model["source_contract"]["source_chain"] == source["source_chain"]
    assert model["source_contract"]["source_tag"] == source["source_tag"]
    assert model["source_contract"]["validated"] is True

    source_field_keys = {field["key"] for field in source["fields"]}
    model_field_keys = {row["source_contract_field"] for row in model["rows"]}
    assert {
        "qaic_bridge_trace",
        "operator_review_queue",
        "ui_tracker_trace",
        "tool_registry_cdc_trace",
        "cdc_contract_trace",
        "brand_config_trace",
    }.issubset(source_field_keys)
    assert model_field_keys - {"policy_flags"} <= source_field_keys


def test_r21l_required_cockpit_traces_are_present() -> None:
    model = build_cockpit_queue_model()
    traces = model["traces"]

    assert traces["SOURCE_R21K_CONTRACT_VALIDATED"] is True
    assert traces["SOURCE_R21J_R6_VALIDATED"] is True
    assert traces["BRAND_CONFIG_TRACE_COCKPIT_READY"] is True
    assert traces["UI_TRACKER_TRACE_COCKPIT_READY"] is True
    assert traces["TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY"] is True
    assert traces["CDC_CONTRACT_TRACE_COCKPIT_READY"] is True
    assert traces["QAIC_BRIDGE_TRACE_COCKPIT_READY"] is True
    assert traces["COCKPIT_QUEUE_MODEL_BINDING"] is True
    assert traces["qaic_execution_allowed"] is False
    assert traces["human_review_required"] is True


def test_r21l_safety_policy_is_review_only() -> None:
    model = build_cockpit_queue_model()
    traces = model["traces"]
    source_policy = model["source_policy_flags"]

    assert traces["qaic_execution_allowed"] is False
    assert traces["human_review_required"] is True
    assert source_policy["qaic_execution_allowed"] is False
    assert source_policy["human_review_required"] is True
    assert all(row["qaic_execution_allowed"] is False for row in model["rows"])
    assert all(row["human_review_required"] is True for row in model["rows"])


def test_r21l_sections_include_required_minimum() -> None:
    sections = list_cockpit_sections()
    section_ids = {section["section_id"] for section in sections}

    assert {
        "qaic_bridge",
        "operator_queue",
        "ui_tracker",
        "tool_registry_cdc",
        "cdc_contract",
        "brand_config",
        "safety_locks",
    }.issubset(section_ids)
    assert all(section["cockpit_ready"] is True for section in sections)


def test_r21l_rows_are_stable_deterministic_and_cockpit_ready() -> None:
    first = list_cockpit_rows()
    second = list_cockpit_rows()

    assert first == second
    assert [row["ordinal"] for row in first] == sorted(row["ordinal"] for row in first)
    assert [row["row_id"] for row in first] == [
        "R21L-QAIC-BRIDGE-001",
        "R21L-OPERATOR-QUEUE-002",
        "R21L-UI-TRACKER-003",
        "R21L-TOOL-REGISTRY-004",
        "R21L-CDC-CONTRACT-005",
        "R21L-BRAND-CONFIG-006",
        "R21L-SAFETY-LOCKS-007",
    ]
    assert all(row["cockpit_ready"] is True for row in first)
    assert all(row["source_trace"] for row in first)
    assert validate_cockpit_queue_model() == ()


def test_r21l_markdown_is_not_html_and_has_no_export_reference() -> None:
    markdown = render_cockpit_queue_model_markdown()
    export_ref = "05" + "_EXPORTS"

    assert "R21L Cockpit Queue Model Binding" in markdown
    assert "qaic_bridge" in markdown
    assert "<html" not in markdown.lower()
    assert export_ref not in markdown


def test_r21l_files_have_no_forbidden_literals() -> None:
    targets = [
        Path("docs/PRODUCT/R21L_COCKPIT_QUEUE_MODEL_BINDING_NO_RUNTIME.md"),
        Path("mvp_qaic_py/cockpit_queue_model_binding_r21l.py"),
        Path("tests/test_r21l_cockpit_queue_model_binding.py"),
    ]
    forbidden = [
        "reflex" + " run",
        "docker" + " run",
        "--frontend" + "-host",
        "provider_call_allowed" + "=True",
        "broker_order_sizing_allowed" + "=True",
        "sheet_bq_write_allowed" + "=True",
        "execution_allowed" + "=True",
        "index" + ".html",
        "05" + "_EXPORTS",
    ]

    for target in targets:
        text = target.read_text(encoding="utf-8")
        for phrase in forbidden:
            assert phrase not in text


def test_r21l_model_introduces_no_html_output_or_export_reference() -> None:
    model = build_cockpit_queue_model()
    text = repr(model)
    export_ref = "05" + "_EXPORTS"

    assert "<html" not in text.lower()
    assert "html_output" not in text.lower()
    assert export_ref not in text
