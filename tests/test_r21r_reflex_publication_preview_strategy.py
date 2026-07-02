from __future__ import annotations

import re
import subprocess
from pathlib import Path

from mvp_qaic_py.reflex_publication_preview_strategy_r21r import (
    AUDIT_ID,
    NEXT_STEP,
    REQUIRED_AUDIT_IDS,
    audit_to_dict,
    build_preview_strategy_audit,
    build_preview_strategy_audit_with_sources,
    render_preview_strategy_markdown,
    validate_preview_strategy_audit,
)


R21R_FILES = (
    Path("mvp_qaic_py/reflex_publication_preview_strategy_r21r.py"),
    Path("docs/PRODUCT/R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT_DOCS_ONLY.md"),
    Path("tests/test_r21r_reflex_publication_preview_strategy.py"),
)


def test_r21r_required_files_and_imports_exist() -> None:
    for target in R21R_FILES:
        assert target.exists()

    audit = build_preview_strategy_audit()
    payload = audit_to_dict(audit)

    assert payload["audit_id"] == AUDIT_ID
    assert payload["R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT"] == "READY"
    assert validate_preview_strategy_audit(payload) == ()


def test_r21r_binds_r21q_product_continuation_final_seal() -> None:
    payload = build_preview_strategy_audit_with_sources()
    bindings = payload["source_bindings"]
    summaries = payload["source_summaries"]

    assert bindings["SOURCE_R21Q_PRODUCT_CONTINUATION_BOUND"] is True
    assert summaries["r21q_product_continuation"] == "R21Q_PRODUCT_CONTINUATION_FINAL_SEAL_NO_RUNTIME"
    assert summaries["r21q_status"] == "READY"
    assert summaries["r21q_next_step"] == AUDIT_ID


def test_r21r_contains_required_runtime_boundary_and_preview_gate_tokens() -> None:
    payload = build_preview_strategy_audit_with_sources()
    boundary = payload["runtime_boundary_flags"]
    gates = payload["preview_audit_gates"]

    assert boundary["R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT"] == "READY"
    assert boundary["REFLEX_RUNTIME_STATUS"] == "PAUSED"
    assert boundary["REFLEX_RUNTIME_RUNNER_CHAIN"] == "STOPPED"
    assert boundary["FALLBACK_STATIC_WYSIWYG_ALLOWED"] is True
    assert boundary["REFLEX_ALLOWED_NEXT_ONLY_AFTER_HUMAN_RUNNER_REVIEW"] is True

    assert gates["NO_DOCS_NO_ACTION"] is True
    assert gates["NO_HELP_NO_RUNTIME"] is True
    assert gates["HELP_FLAG_MISSING_COMMAND_FORBIDDEN"] is True
    assert gates["TCP_ONLY_NOT_PREVIEW_READY"] is True
    assert gates["HTTP_FAIL_STOP_AND_DIAG"] is True
    assert gates["PREVIEW_ONLY_AFTER_HTTP_PASS"] is True
    assert gates["HTTP_FRONTEND_NON_EMPTY_REQUIRED"] is True
    assert gates["REFLEX_CLI_HELP_CAPTURE_REQUIRED"] is True
    assert gates["REFLEX_VERSION_CAPTURE_REQUIRED"] is True
    assert gates["NO_FRONTEND_HOST_FLAG"] is True


def test_r21r_contains_required_safety_locks() -> None:
    locks = build_preview_strategy_audit_with_sources()["safety_locks"]

    assert locks["NO_PUBLIC_DEPLOY"] is True
    assert locks["NO_REFLEX_DEPLOY"] is True
    assert locks["NO_RUNTIME"] is True
    assert locks["NO_DOCKER"] is True
    assert locks["NO_REFLEX_RUN"] is True
    assert locks["NO_PROVIDER_CALL"] is True
    assert locks["NO_BROKER_ORDER_SIZING"] is True
    assert locks["NO_SHEET_BQ_WRITE"] is True
    assert locks["NO_HTML_OUTPUT"] is True


def test_r21r_audit_map_is_deterministic_review_only_and_complete() -> None:
    first = build_preview_strategy_audit_with_sources()
    second = build_preview_strategy_audit_with_sources()
    entries = first["audit_entries"]

    assert first == second
    assert [entry["ordinal"] for entry in entries] == sorted(entry["ordinal"] for entry in entries)
    assert [entry["audit_entry_id"] for entry in entries] == list(REQUIRED_AUDIT_IDS)
    assert all(entry["human_review_required"] is True for entry in entries)
    assert all(entry["qaic_execution_allowed"] is False for entry in entries)


def test_r21r_markdown_is_text_only_and_names_next_step() -> None:
    markdown = render_preview_strategy_markdown()

    assert "R21R Reflex Publication Preview Strategy Audit" in markdown
    assert "R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT=READY" in markdown
    assert "SOURCE_R21Q_PRODUCT_CONTINUATION_BOUND" in markdown
    assert "REFLEX_RUNTIME_STATUS" in markdown
    assert "REFLEX_RUNTIME_RUNNER_CHAIN" in markdown
    assert "HTTP_FRONTEND_NON_EMPTY_REQUIRED" in markdown
    assert "REFLEX_CLI_HELP_CAPTURE_REQUIRED" in markdown
    assert "REFLEX_VERSION_CAPTURE_REQUIRED" in markdown
    assert "NO_REFLEX_RUN" in markdown
    assert f"NEXT={NEXT_STEP}" in markdown
    assert "<html" not in markdown.lower()


def test_r21r_files_have_no_forbidden_runtime_or_write_strings() -> None:
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

    for target in R21R_FILES:
        text = target.read_text(encoding="utf-8").lower()
        for pattern in forbidden_patterns:
            assert re.search(pattern.lower(), text) is None


def test_no_r21r_html_file_is_tracked() -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "*.html"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()

    assert all("r21r" not in path.lower() for path in tracked)
    assert all("publication_preview_strategy" not in path.lower() for path in tracked)
