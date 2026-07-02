from __future__ import annotations

import re
import subprocess
from pathlib import Path

from mvp_qaic_py.product_continuation_final_seal_r21q import (
    NEXT_STEP,
    REQUIRED_SEAL_IDS,
    SEAL_ID,
    build_product_continuation_final_seal,
    build_product_continuation_with_sources,
    render_product_continuation_markdown,
    seal_to_dict,
    validate_product_continuation_final_seal,
)


R21Q_FILES = (
    Path("mvp_qaic_py/product_continuation_final_seal_r21q.py"),
    Path("docs/PRODUCT/R21Q_PRODUCT_CONTINUATION_FINAL_SEAL_NO_RUNTIME.md"),
    Path("tests/test_r21q_product_continuation_final_seal.py"),
)


def test_r21q_required_files_and_imports_exist() -> None:
    for target in R21Q_FILES:
        assert target.exists()

    seal = build_product_continuation_final_seal()
    payload = seal_to_dict(seal)

    assert payload["seal_id"] == SEAL_ID
    assert payload["PRODUCT_CONTINUATION_FINAL_SEAL"] == "READY"
    assert validate_product_continuation_final_seal(payload) == ()


def test_r21q_binds_r21o_review_packet_and_r21p_handoff() -> None:
    payload = build_product_continuation_with_sources()
    bindings = payload["source_bindings"]
    summaries = payload["source_summaries"]

    assert bindings["SOURCE_R21O_QAIC_REVIEW_PACKET_BOUND"] is True
    assert bindings["SOURCE_R21P_OPERATOR_HANDOFF_BOUND"] is True
    assert summaries["r21o_review_packet"] == "R21O_QAIC_REVIEW_PACKET_FINAL_NO_RUNTIME"
    assert summaries["r21o_status"] == "READY"
    assert summaries["r21p_operator_handoff"] == (
        "R21P_OPERATOR_HANDOFF_MEMO_AND_COCKPIT_TRACE_MAP_NO_RUNTIME"
    )
    assert summaries["r21p_operator_handoff_status"] == "READY"
    assert summaries["r21p_cockpit_trace_map_status"] == "READY"
    assert summaries["r21p_next_step"] == SEAL_ID


def test_r21q_contains_required_product_chain_tokens_and_safety_locks() -> None:
    payload = build_product_continuation_with_sources()
    chain = payload["product_chain_flags"]
    locks = payload["safety_locks"]

    assert chain["PRODUCT_CONTINUATION_FINAL_SEAL"] == "READY"
    assert chain["QAIC_REVIEW_PACKET_FINAL"] == "READY"
    assert chain["OPERATOR_HANDOFF_MEMO"] == "READY"
    assert chain["COCKPIT_TRACE_MAP"] == "READY"
    assert chain["PRODUCT_CHAIN_NO_RUNTIME"] is True
    assert chain["REFLEX_RUNTIME_STATUS"] == "PAUSED"
    assert chain["FALLBACK_STATIC_WYSIWYG_ALLOWED"] is True

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


def test_r21q_seal_map_is_deterministic_review_only_and_complete() -> None:
    first = build_product_continuation_with_sources()
    second = build_product_continuation_with_sources()
    entries = first["seal_entries"]

    assert first == second
    assert [entry["ordinal"] for entry in entries] == sorted(entry["ordinal"] for entry in entries)
    assert [entry["seal_entry_id"] for entry in entries] == list(REQUIRED_SEAL_IDS)
    assert all(entry["human_review_required"] is True for entry in entries)
    assert all(entry["qaic_execution_allowed"] is False for entry in entries)


def test_r21q_markdown_is_text_only_and_names_next_step() -> None:
    markdown = render_product_continuation_markdown()

    assert "R21Q Product Continuation Final Seal" in markdown
    assert "PRODUCT_CONTINUATION_FINAL_SEAL=READY" in markdown
    assert "SOURCE_R21O_QAIC_REVIEW_PACKET_BOUND" in markdown
    assert "SOURCE_R21P_OPERATOR_HANDOFF_BOUND" in markdown
    assert "QAIC_REVIEW_PACKET_FINAL" in markdown
    assert "OPERATOR_HANDOFF_MEMO" in markdown
    assert "COCKPIT_TRACE_MAP" in markdown
    assert "REFLEX_RUNTIME_STATUS" in markdown
    assert f"NEXT={NEXT_STEP}" in markdown
    assert "<html" not in markdown.lower()


def test_r21q_files_have_no_forbidden_runtime_or_write_strings() -> None:
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
        "reflex" + r"\s+" + "deploy",
        "public" + r"\s+" + "deploy",
        "05" + "_EXPORTS",
    )

    for target in R21Q_FILES:
        text = target.read_text(encoding="utf-8").lower()
        for pattern in forbidden_patterns:
            assert re.search(pattern.lower(), text) is None


def test_no_r21q_html_file_is_tracked() -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "*.html"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()

    assert all("r21q" not in path.lower() for path in tracked)
    assert all("product_continuation_final_seal" not in path.lower() for path in tracked)
