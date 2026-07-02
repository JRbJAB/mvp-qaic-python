from __future__ import annotations

import re
import subprocess
from pathlib import Path

from mvp_qaic_py.reflex_private_preview_approval_review_r21t_a import (
    APPROVAL_ID,
    NEXT_STEP,
    REQUIRED_APPROVAL_ENTRY_IDS,
    REQUIRED_OPERATOR_MARKER,
    REQUIRED_PHASES,
    approval_review_to_dict,
    build_private_preview_approval_review,
    build_private_preview_approval_review_with_sources,
    render_private_preview_approval_markdown,
    validate_private_preview_approval_review,
)


R21T_A_FILES = (
    Path("mvp_qaic_py/reflex_private_preview_approval_review_r21t_a.py"),
    Path("docs/PRODUCT/R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW_ONLY.md"),
    Path("tests/test_r21t_a_private_preview_approval_review.py"),
)


def test_r21t_a_required_files_and_imports_exist() -> None:
    for target in R21T_A_FILES:
        assert target.exists()

    review = build_private_preview_approval_review()
    payload = approval_review_to_dict(review)

    assert payload["approval_id"] == APPROVAL_ID
    assert payload["R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW"] == "READY"
    assert validate_private_preview_approval_review(payload) == ()


def test_r21t_a_binds_r21s_preview_runner_spec() -> None:
    payload = build_private_preview_approval_review_with_sources()
    bindings = payload["source_bindings"]
    summaries = payload["source_summaries"]

    assert bindings["SOURCE_R21S_PREVIEW_RUNNER_SPEC_BOUND"] is True
    assert summaries["r21s_preview_runner_spec"] == "R21S_REFLEX_PREVIEW_RUNNER_SPEC_REVIEW_ONLY"
    assert summaries["r21s_status"] == "READY"
    assert summaries["r21s_next_step"] == "R21T_HUMAN_APPROVED_PRIVATE_PREVIEW_ATTEMPT_ONLY"


def test_r21t_a_contains_required_approval_gate_tokens() -> None:
    tokens = build_private_preview_approval_review_with_sources()["approval_review_tokens"]

    assert tokens["R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW"] == "READY"
    assert tokens["SOURCE_R21S_PREVIEW_RUNNER_SPEC_BOUND"] is True
    assert tokens["HUMAN_APPROVED_PRIVATE_PREVIEW"] is False
    assert tokens["HUMAN_APPROVED_PRIVATE_PREVIEW_REQUIRED"] is True
    assert tokens["EXPLICIT_OPERATOR_MARKER_REQUIRED"] is True
    assert tokens["REQUIRED_OPERATOR_MARKER"] == REQUIRED_OPERATOR_MARKER
    assert tokens["RUNNER_REVIEW_ONLY"] is True
    assert tokens["RUNNER_EXECUTED"] is False
    assert tokens["RUNTIME_EXECUTION_ALLOWED"] is False
    assert tokens["REFLEX_RUNTIME_STATUS"] == "PAUSED"
    assert tokens["REFLEX_RUNTIME_RUNNER_CHAIN"] == "STOPPED_UNTIL_EXPLICIT_OPERATOR_MARKER"
    assert tokens["REFLEX_CLI_HELP_CAPTURE_REQUIRED"] is True
    assert tokens["REFLEX_VERSION_CAPTURE_REQUIRED"] is True
    assert tokens["HELP_VERSION_CAPTURE_BEFORE_PREVIEW"] is True
    assert tokens["NO_FRONTEND_HOST_FLAG"] is True
    assert tokens["NO_PUBLIC_DEPLOY"] is True
    assert tokens["NO_REFLEX_DEPLOY"] is True
    assert tokens["HTTP_FRONTEND_NON_EMPTY_REQUIRED"] is True
    assert tokens["TCP_ONLY_NOT_PREVIEW_READY"] is True
    assert tokens["PREVIEW_ONLY_AFTER_HTTP_PASS"] is True
    assert tokens["HTTP_FAIL_STOP_AND_DIAG"] is True
    assert tokens["PS51_COMPATIBLE"] is True
    assert tokens["PROMPT_MD_REQUIRED"] is True
    assert tokens["RUNNER_SHORT_REQUIRED"] is True
    assert tokens["NO_GIANT_CONSOLE_PROMPT"] is True
    assert tokens["TARGETED_STAGING_ONLY"] is True
    assert tokens["NO_GIT_ADD_DOT"] is True
    assert tokens["NO_RESET"] is True
    assert tokens["DIRTY_START_STOP_NO_WRITE"] is True
    assert tokens["FAILED_TESTS_NO_COMMIT_NO_TAG_NO_PUSH"] is True
    assert tokens["NO_RUNTIME"] is True
    assert tokens["NO_DOCKER"] is True
    assert tokens["NO_REFLEX_RUN"] is True
    assert tokens["NO_PROVIDER_CALL"] is True
    assert tokens["NO_BROKER_ORDER_SIZING"] is True
    assert tokens["NO_SHEET_BQ_WRITE"] is True
    assert tokens["NO_HTML_OUTPUT"] is True
    assert tokens["NEXT"] == NEXT_STEP


def test_r21t_a_required_runner_review_phases_are_present() -> None:
    payload = build_private_preview_approval_review_with_sources()

    assert tuple(payload["required_phases"]) == REQUIRED_PHASES
    assert payload["required_phases"] == [
        "RUNNER_PREFLIGHT",
        "EVIDENCE_COLLECTION",
        "VALIDATION",
        "SUMMARY",
    ]


def test_r21t_a_approval_map_is_deterministic_review_only_and_complete() -> None:
    first = build_private_preview_approval_review_with_sources()
    second = build_private_preview_approval_review_with_sources()
    entries = first["approval_entries"]

    assert first == second
    assert [entry["ordinal"] for entry in entries] == sorted(entry["ordinal"] for entry in entries)
    assert [entry["approval_entry_id"] for entry in entries] == list(REQUIRED_APPROVAL_ENTRY_IDS)
    assert all(entry["human_review_required"] is True for entry in entries)
    assert all(entry["runtime_execution_allowed"] is False for entry in entries)
    assert all(entry["marker_present"] is False for entry in entries)


def test_r21t_a_markdown_is_text_only_and_names_next_step() -> None:
    markdown = render_private_preview_approval_markdown()

    assert "R21T-A Human Approval Private Preview Runner" in markdown
    assert "R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW=READY" in markdown
    assert "SOURCE_R21S_PREVIEW_RUNNER_SPEC_BOUND" in markdown
    assert "`HUMAN_APPROVED_PRIVATE_PREVIEW` = `False`" in markdown
    assert "HUMAN_APPROVED_PRIVATE_PREVIEW_REQUIRED" in markdown
    assert "EXPLICIT_OPERATOR_MARKER_REQUIRED" in markdown
    assert REQUIRED_OPERATOR_MARKER in markdown
    assert "RUNNER_REVIEW_ONLY" in markdown
    assert "RUNNER_EXECUTED" in markdown
    assert "RUNTIME_EXECUTION_ALLOWED" in markdown
    assert "REFLEX_RUNTIME_STATUS" in markdown
    assert "REFLEX_RUNTIME_RUNNER_CHAIN" in markdown
    assert "REFLEX_CLI_HELP_CAPTURE_REQUIRED" in markdown
    assert "REFLEX_VERSION_CAPTURE_REQUIRED" in markdown
    assert "HELP_VERSION_CAPTURE_BEFORE_PREVIEW" in markdown
    assert "HTTP_FRONTEND_NON_EMPTY_REQUIRED" in markdown
    assert "NO_REFLEX_RUN" in markdown
    assert f"NEXT={NEXT_STEP}" in markdown
    assert "<html" not in markdown.lower()


def test_r21t_a_files_have_no_forbidden_runtime_or_write_strings() -> None:
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

    for target in R21T_A_FILES:
        text = target.read_text(encoding="utf-8").lower()
        for pattern in forbidden_patterns:
            assert re.search(pattern.lower(), text) is None


def test_no_r21t_a_html_runtime_or_export_file_is_tracked() -> None:
    tracked = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.splitlines()

    r21t_a_paths = [path.lower() for path in tracked if "r21t_a" in path.lower()]

    assert all(not path.endswith(".html") for path in r21t_a_paths)
    assert all(not path.endswith(".ps1") for path in r21t_a_paths)
    assert all("export" not in path for path in r21t_a_paths)
