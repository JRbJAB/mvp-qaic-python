from __future__ import annotations

import re
from pathlib import Path

from mvp_qaic_py.cockpit_queue_visual_planning_r21m import (
    REQUIRED_LANE_IDS,
    WORKFLOW_ID,
    build_cockpit_queue_visual_planning,
    model_to_dict,
    render_visual_planning_markdown,
    validate_cockpit_queue_visual_planning,
)


R21M_FILES = (
    Path("mvp_qaic_py/cockpit_queue_visual_planning_r21m.py"),
    Path("docs/PRODUCT/R21M_COCKPIT_QUEUE_VISUAL_PLANNING_NO_RUNTIME.md"),
    Path("tests/test_r21m_cockpit_queue_visual_planning.py"),
)


def test_r21m_required_files_and_imports_exist() -> None:
    for target in R21M_FILES:
        assert target.exists()

    model = build_cockpit_queue_visual_planning()
    payload = model_to_dict(model)

    assert payload["workflow_id"] == WORKFLOW_ID
    assert payload["source_r21k_contract"] == "BOUND"
    assert payload["source_r21l_model_binding"] == "BOUND"
    assert validate_cockpit_queue_visual_planning(model) == ()


def test_r21m_model_contains_required_trace_tokens_and_lanes() -> None:
    payload = model_to_dict()
    traces = payload["traces"]
    lane_ids = {lane["lane_id"] for lane in payload["lanes"]}

    assert traces["source_r21k_contract"] == "BOUND"
    assert traces["source_r21l_model_binding"] == "BOUND"
    assert traces["SOURCE_R21J_R6_VALIDATED"] is True
    assert traces["COCKPIT_QUEUE_VISUAL_PLANNING"] == "READY"
    assert traces["COCKPIT_QUEUE_DATA_CONTRACT"] == "BOUND"
    assert traces["COCKPIT_QUEUE_MODEL_BINDING"] == "BOUND"
    assert set(REQUIRED_LANE_IDS).issubset(lane_ids)


def test_r21m_trace_booleans_and_execution_locks_are_correct() -> None:
    payload = model_to_dict()
    traces = payload["traces"]
    locks = payload["execution_locks"]

    for key in (
        "BRAND_CONFIG_TRACE_COCKPIT_READY",
        "UI_TRACKER_TRACE_COCKPIT_READY",
        "TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY",
        "CDC_CONTRACT_TRACE_COCKPIT_READY",
        "QAIC_BRIDGE_TRACE_COCKPIT_READY",
        "preserve_q_candlesticks_signal_line",
    ):
        assert traces[key] is True

    assert traces["QAIT_CHARTE_TEMPLATE"] == "BOUND"
    assert traces["MVP_QAIC_LOGO_VALIDATED"] == "BOUND"
    assert traces["qaic_execution_allowed"] is False
    assert locks["qaic_execution_allowed"] is False
    assert locks["human_review_required"] is True


def test_r21m_model_blocks_runtime_and_external_execution_surfaces() -> None:
    payload = model_to_dict()
    locks = payload["execution_locks"]
    export_token = "05" + "_EXPORTS"
    text = repr(payload)

    assert locks["no_codex_runtime"] is True
    assert locks["no_runtime"] is True
    assert locks["no_docker"] is True
    assert locks["no_reflex_run"] is True
    assert locks["no_provider_call"] is True
    assert locks["no_broker_order_sizing"] is True
    assert locks["no_sheet_bq_write"] is True
    assert locks["no_html_output"] is True
    assert locks["no_export_directory_output"] is True
    assert "<html" not in text.lower()
    assert export_token not in text


def test_r21m_visual_lanes_are_deterministic_and_cockpit_ready() -> None:
    first = model_to_dict()
    second = model_to_dict()

    assert first == second
    assert [lane["ordinal"] for lane in first["lanes"]] == sorted(
        lane["ordinal"] for lane in first["lanes"]
    )
    assert [lane["lane_id"] for lane in first["lanes"]] == list(REQUIRED_LANE_IDS)
    assert all(lane["cockpit_ready"] is True for lane in first["lanes"])
    assert all(card["cockpit_ready"] is True for lane in first["lanes"] for card in lane["cards"])


def test_r21m_markdown_contains_visual_plan_and_end_plan() -> None:
    markdown = render_visual_planning_markdown()

    assert "R21M Cockpit Queue Visual Planning" in markdown
    assert "Cockpit Visual Plan" in markdown
    assert "End-Plan" in markdown
    assert "operator_queue_status" in markdown
    assert "R21M" in markdown
    assert "R21N" in markdown
    assert "R21O" in markdown
    assert "R21P" in markdown
    assert "R21Q" in markdown
    assert "Reflex runtime remains paused and separate" in markdown
    assert "<html" not in markdown.lower()


def test_r21m_files_have_no_forbidden_runtime_command_or_frontend_host_flag() -> None:
    forbidden_patterns = (
        r"\b" + "reflex" + r"\s+" + "run" + r"\b",
        r"\b" + "docker" + r"\s+" + "run" + r"\b",
        "--frontend" + "-host",
        "index" + ".html",
        "05" + "_EXPORTS",
    )

    for target in R21M_FILES:
        text = target.read_text(encoding="utf-8").lower()
        for pattern in forbidden_patterns:
            assert re.search(pattern.lower(), text) is None
