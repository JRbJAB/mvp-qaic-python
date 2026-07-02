from __future__ import annotations

import re
import subprocess
from pathlib import Path

from mvp_qaic_py.qaic_review_packet_final_r21o import (
    EXPORT_SCOPE_KEY,
    PACKET_ID,
    REQUIRED_PACKET_SECTIONS,
    build_review_packet_with_sources,
    packet_to_dict,
    render_review_packet_markdown,
    validate_review_packet,
)


R21O_FILES = (
    Path("mvp_qaic_py/qaic_review_packet_final_r21o.py"),
    Path("docs/PRODUCT/R21O_QAIC_REVIEW_PACKET_FINAL_NO_RUNTIME.md"),
    Path("tests/test_r21o_qaic_review_packet_final.py"),
)

TRACE_TOKENS = (
    "BRAND_CONFIG_TRACE_COCKPIT_READY",
    "UI_TRACKER_TRACE_COCKPIT_READY",
    "TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY",
    "CDC_CONTRACT_TRACE_COCKPIT_READY",
    "QAIC_BRIDGE_TRACE_COCKPIT_READY",
)

SOURCE_TOKENS = (
    "SOURCE_R21J_QUEUE_BOUND",
    "SOURCE_R21K_DATA_CONTRACT_BOUND",
    "SOURCE_R21L_MODEL_BINDING_BOUND",
    "SOURCE_R21M_VISUAL_PLANNING_BOUND",
    "SOURCE_R21N_LOCAL_PREVIEW_BOUND",
)


def test_r21o_required_files_and_imports_exist() -> None:
    for target in R21O_FILES:
        assert target.exists()

    payload = packet_to_dict()
    assert payload["packet_id"] == PACKET_ID
    assert payload["QAIC_REVIEW_PACKET_FINAL"] == "READY"
    assert validate_review_packet(payload) == ()


def test_r21o_packet_binds_required_sources_and_prior_payloads() -> None:
    payload = build_review_packet_with_sources()
    sources = payload["source_bindings"]
    summaries = payload["source_summaries"]

    for key in SOURCE_TOKENS:
        assert sources[key] is True

    assert summaries["r21j_queue"] == "docs/PRODUCT/R21J_OPERATOR_QAIC_REVIEW_QUEUE_NO_RUNTIME.md"
    assert summaries["r21k_data_contract"] == "R21K_COCKPIT_QUEUE_DATA_CONTRACT_NO_RUNTIME"
    assert summaries["r21l_model_binding"] == "R21L_COCKPIT_QUEUE_MODEL_BINDING_NO_RUNTIME"
    assert summaries["r21m_visual_planning"] == "R21M_COCKPIT_QUEUE_VISUAL_PLANNING_NO_RUNTIME"
    assert summaries["r21n_local_preview"] == "R21N_LOCAL_COCKPIT_PREVIEW_NO_RUNTIME"


def test_r21o_packet_contains_required_trace_tokens_and_safety_locks() -> None:
    payload = build_review_packet_with_sources()
    traces = payload["trace_flags"]
    locks = payload["safety_locks"]

    for key in TRACE_TOKENS:
        assert traces[key] is True

    assert locks["HUMAN_REVIEW_REQUIRED"] is True
    assert locks["QAIC_EXECUTION_ALLOWED"] is False
    assert locks["REVIEW_ONLY_HANDOFF"] is True
    assert locks["NO_RUNTIME"] is True
    assert locks["NO_DOCKER"] is True
    assert locks["NO_REFLEX_RUN"] is True
    assert locks["NO_PROVIDER_CALL"] is True
    assert locks["NO_BROKER_ORDER_SIZING"] is True
    assert locks["NO_SHEET_BQ_WRITE"] is True
    assert locks["NO_HTML_OUTPUT"] is True
    assert locks[EXPORT_SCOPE_KEY] is True


def test_r21o_sections_are_deterministic_review_only_and_complete() -> None:
    first = build_review_packet_with_sources()
    second = build_review_packet_with_sources()
    sections = first["sections"]

    assert first == second
    assert [section["ordinal"] for section in sections] == sorted(
        section["ordinal"] for section in sections
    )
    assert [section["section_id"] for section in sections] == list(REQUIRED_PACKET_SECTIONS)
    assert all(section["human_review_required"] is True for section in sections)
    assert all(section["qaic_execution_allowed"] is False for section in sections)


def test_r21o_markdown_is_text_only_and_names_next_step() -> None:
    markdown = render_review_packet_markdown()

    assert "R21O QAIC Review Packet Final" in markdown
    assert "QAIC_REVIEW_PACKET_FINAL=READY" in markdown
    assert "SOURCE_R21J_QUEUE_BOUND" in markdown
    assert "QAIC_BRIDGE_TRACE_COCKPIT_READY" in markdown
    assert "NEXT=R21P_OPERATOR_HANDOFF_MEMO_AND_COCKPIT_TRACE_MAP_NO_RUNTIME" in markdown
    assert "<html" not in markdown.lower()


def test_r21o_files_have_no_forbidden_runtime_or_export_strings() -> None:
    forbidden_patterns = (
        r"\b" + "reflex" + r"\s+" + "run" + r"\b",
        r"\b" + "docker" + r"\s+" + "run" + r"\b",
        "--frontend" + "-host",
        "provider_call_allowed" + "=true",
        "broker_order_sizing_allowed" + "=true",
        "sheet_bq_write_allowed" + "=true",
        "execution_allowed" + "=true",
        "git" + r"\s+" + "add" + r"\s+\.",
        r"\b" + "re" + "set" + r"\b",
        "05" + "_EXPORTS",
    )

    for target in R21O_FILES:
        text = target.read_text(encoding="utf-8").lower()
        for pattern in forbidden_patterns:
            assert re.search(pattern.lower(), text) is None


def test_no_r21o_html_file_is_tracked() -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "*.html"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()

    assert all("r21o" not in path.lower() for path in tracked)
    assert all("qaic_review_packet_final" not in path.lower() for path in tracked)
