from __future__ import annotations

import re
import subprocess
from pathlib import Path

from mvp_qaic_py.operator_handoff_trace_map_r21p import (
    HANDOFF_ID,
    REQUIRED_TRACE_IDS,
    build_operator_handoff_trace_map,
    build_operator_handoff_with_sources,
    render_operator_handoff_markdown,
    trace_map_to_dict,
    validate_operator_handoff_trace_map,
)


R21P_FILES = (
    Path("mvp_qaic_py/operator_handoff_trace_map_r21p.py"),
    Path("docs/PRODUCT/R21P_OPERATOR_HANDOFF_MEMO_AND_COCKPIT_TRACE_MAP_NO_RUNTIME.md"),
    Path("tests/test_r21p_operator_handoff_trace_map.py"),
)

TRACE_TOKENS = (
    "BRAND_CONFIG_TRACE_COCKPIT_READY",
    "UI_TRACKER_TRACE_COCKPIT_READY",
    "TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY",
    "CDC_CONTRACT_TRACE_COCKPIT_READY",
    "QAIC_BRIDGE_TRACE_COCKPIT_READY",
)


def test_r21p_required_files_and_imports_exist() -> None:
    for target in R21P_FILES:
        assert target.exists()

    trace_map = build_operator_handoff_trace_map()
    payload = trace_map_to_dict(trace_map)

    assert payload["handoff_id"] == HANDOFF_ID
    assert payload["OPERATOR_HANDOFF_MEMO"] == "READY"
    assert payload["COCKPIT_TRACE_MAP"] == "READY"
    assert validate_operator_handoff_trace_map(payload) == ()


def test_r21p_binds_r21o_review_packet_and_r21n_local_preview() -> None:
    payload = build_operator_handoff_with_sources()
    bindings = payload["source_bindings"]
    summaries = payload["source_summaries"]

    assert bindings["SOURCE_R21O_QAIC_REVIEW_PACKET_BOUND"] is True
    assert bindings["SOURCE_R21N_LOCAL_PREVIEW_BOUND"] is True
    assert summaries["r21o_review_packet"] == "R21O_QAIC_REVIEW_PACKET_FINAL_NO_RUNTIME"
    assert summaries["r21n_local_preview"] == "R21N_LOCAL_COCKPIT_PREVIEW_NO_RUNTIME"
    assert summaries["r21o_next_step"] == HANDOFF_ID


def test_r21p_contains_required_trace_tokens_and_safety_locks() -> None:
    payload = build_operator_handoff_with_sources()
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


def test_r21p_trace_map_is_deterministic_review_only_and_complete() -> None:
    first = build_operator_handoff_with_sources()
    second = build_operator_handoff_with_sources()
    traces = first["traces"]

    assert first == second
    assert [entry["ordinal"] for entry in traces] == sorted(entry["ordinal"] for entry in traces)
    assert [entry["trace_id"] for entry in traces] == list(REQUIRED_TRACE_IDS)
    assert all(entry["human_review_required"] is True for entry in traces)
    assert all(entry["qaic_execution_allowed"] is False for entry in traces)


def test_r21p_markdown_is_text_only_and_names_next_step() -> None:
    markdown = render_operator_handoff_markdown()

    assert "R21P Operator Handoff Memo" in markdown
    assert "OPERATOR_HANDOFF_MEMO=READY" in markdown
    assert "COCKPIT_TRACE_MAP=READY" in markdown
    assert "SOURCE_R21O_QAIC_REVIEW_PACKET_BOUND" in markdown
    assert "SOURCE_R21N_LOCAL_PREVIEW_BOUND" in markdown
    assert "QAIC_BRIDGE_TRACE_COCKPIT_READY" in markdown
    assert "NEXT=R21Q_PRODUCT_CONTINUATION_FINAL_SEAL_NO_RUNTIME" in markdown
    assert "<html" not in markdown.lower()


def test_r21p_files_have_no_forbidden_runtime_or_write_strings() -> None:
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

    for target in R21P_FILES:
        text = target.read_text(encoding="utf-8").lower()
        for pattern in forbidden_patterns:
            assert re.search(pattern.lower(), text) is None


def test_no_r21p_html_file_is_tracked() -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "*.html"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()

    assert all("r21p" not in path.lower() for path in tracked)
    assert all("operator_handoff_trace_map" not in path.lower() for path in tracked)
