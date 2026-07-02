from __future__ import annotations

import re
import subprocess
from pathlib import Path

from mvp_qaic_py.reflex_private_preview_operator_script_review_r21t_d import (
    NEXT_STEP,
    OPERATOR_SCRIPT_SECTIONS,
    REFLEX_VERSION,
    REQUIRED_OPERATOR_ENTRY_IDS,
    REVIEW_ID,
    build_private_preview_operator_script_review,
    build_private_preview_operator_script_review_with_sources,
    operator_script_review_to_dict,
    render_private_preview_operator_script_markdown,
    validate_private_preview_operator_script_review,
)


R21T_D_FILES = (
    Path("mvp_qaic_py/reflex_private_preview_operator_script_review_r21t_d.py"),
    Path("docs/PRODUCT/R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW_ONLY.md"),
    Path("tests/test_r21t_d_private_preview_operator_script_review.py"),
)


def test_r21t_d_required_files_and_imports_exist() -> None:
    for target in R21T_D_FILES:
        assert target.exists()

    review = build_private_preview_operator_script_review()
    payload = operator_script_review_to_dict(review)

    assert payload["review_id"] == REVIEW_ID
    assert payload["R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW"] == "READY"
    assert validate_private_preview_operator_script_review(payload) == ()


def test_r21t_d_binds_r21t_c_runner_build_review() -> None:
    payload = build_private_preview_operator_script_review_with_sources()
    bindings = payload["source_bindings"]
    summaries = payload["source_summaries"]

    assert bindings["SOURCE_R21T_C_BUILD_REVIEW_BOUND"] is True
    assert summaries["r21t_c_runner_build_review"] == (
        "R21T_C_PRIVATE_PREVIEW_RUNNER_BUILD_REVIEW_ONLY"
    )
    assert summaries["r21t_c_status"] == "READY"
    assert summaries["r21t_c_reflex_version"] == REFLEX_VERSION
    assert summaries["r21t_c_next_step"] == REVIEW_ID


def test_r21t_d_contains_required_operator_script_review_tokens() -> None:
    tokens = build_private_preview_operator_script_review_with_sources()[
        "operator_script_review_tokens"
    ]

    assert tokens["R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW"] == "READY"
    assert tokens["SOURCE_R21T_C_BUILD_REVIEW_BOUND"] is True
    assert tokens["OPERATOR_SCRIPT_REVIEW_ONLY"] is True
    assert tokens["SCRIPT_FILE_CREATED"] is False
    assert tokens["PS1_CREATED"] is False
    assert tokens["SCRIPT_EXECUTED"] is False
    assert tokens["RUNNER_EXECUTED"] is False
    assert tokens["RUNTIME_EXECUTION_ALLOWED"] is False
    assert tokens["NO_RUNTIME_EXECUTION"] is True
    assert tokens["NO_DOCKER_CALL"] is True
    assert tokens["NO_REFLEX_APP_START"] is True
    assert tokens["NO_PREVIEW_ATTEMPT"] is True
    assert tokens["NO_PORTS"] is True
    assert tokens["NO_BROWSER"] is True
    assert tokens["REFLEX_VERSION"] == "0.9.6.post1"
    assert tokens["HELP_VERSION_CAPTURE_PASSED"] is True
    assert tokens["HELP_FORBIDDEN_FRONTEND_HOST_FOUND"] is False
    assert tokens["NO_FRONTEND_HOST_FLAG"] is True
    assert tokens["PRIVATE_MAPPING_REQUIRED"] is True
    assert tokens["HTTP_FRONTEND_NON_EMPTY_REQUIRED"] is True
    assert tokens["TCP_ONLY_NOT_PREVIEW_READY"] is True
    assert tokens["PREVIEW_ONLY_AFTER_HTTP_PASS"] is True
    assert tokens["REFLEX_RUNTIME_STATUS"] == "PAUSED"
    assert tokens["REFLEX_RUNTIME_RUNNER_CHAIN"] == "STOPPED_AFTER_OPERATOR_SCRIPT_REVIEW"
    assert tokens["PS51_COMPATIBLE"] is True
    assert tokens["PROMPT_MD_REQUIRED"] is True
    assert tokens["RUNNER_SHORT_REQUIRED"] is True
    assert tokens["NO_GIANT_CONSOLE_PROMPT"] is True
    assert tokens["HARD_TIMEOUT_REQUIRED"] is True
    assert tokens["IMAGE_PREFLIGHT_REQUIRED"] is True
    assert tokens["PORT_PREFLIGHT_REQUIRED"] is True
    assert tokens["GIT_ARCHIVE_HEAD_COPY_REQUIRED"] is True
    assert tokens["POLICY_GUARDS_REQUIRED"] is True
    assert tokens["TRANSIENT_REPORTS_UNDER_RUN_REPORTS"] is True
    assert tokens["TARGETED_STAGING_ONLY"] is True
    assert tokens["NO_GIT_ADD_DOT"] is True
    assert tokens["NO_RESET"] is True
    assert tokens["NO_PUBLIC_DEPLOY"] is True
    assert tokens["NO_REFLEX_DEPLOY"] is True
    assert tokens["NO_PROVIDER_CALL"] is True
    assert tokens["NO_BROKER_ORDER_SIZING"] is True
    assert tokens["NO_SHEET_BQ_WRITE"] is True
    assert tokens["NO_HTML_OUTPUT"] is True
    assert tokens["NEXT"] == NEXT_STEP


def test_r21t_d_required_future_operator_sections_are_metadata_only() -> None:
    payload = build_private_preview_operator_script_review_with_sources()

    assert tuple(payload["operator_script_sections"]) == OPERATOR_SCRIPT_SECTIONS
    assert payload["operator_script_sections"] == [
        "STRICT_PREFLIGHT",
        "HARD_TIMEOUT_NATIVE_CALLS",
        "PINNED_IMAGE_CHECK",
        "PRIVATE_PORT_CHECKS",
        "FULL_HEAD_COPY_BY_ARCHIVE_TAR",
        "POLICY_GUARD_CHECKS",
        "HELP_VERSION_EVIDENCE_REUSE",
        "PREVIEW_READINESS_PROBES",
        "FAILURE_STOP_DIAGNOSTICS",
        "SUMMARY",
    ]


def test_r21t_d_operator_map_is_deterministic_review_only_and_complete() -> None:
    first = build_private_preview_operator_script_review_with_sources()
    second = build_private_preview_operator_script_review_with_sources()
    entries = first["operator_entries"]

    assert first == second
    assert [entry["ordinal"] for entry in entries] == sorted(entry["ordinal"] for entry in entries)
    assert [entry["operator_entry_id"] for entry in entries] == list(REQUIRED_OPERATOR_ENTRY_IDS)
    assert all(entry["metadata_only"] is True for entry in entries)
    assert all(entry["script_action_allowed"] is False for entry in entries)
    assert all(entry["runtime_action_allowed"] is False for entry in entries)
    assert all(entry["preview_readiness_claimed"] is False for entry in entries)


def test_r21t_d_markdown_is_text_only_and_names_next_step() -> None:
    markdown = render_private_preview_operator_script_markdown()

    assert "R21T-D Private Preview Runner Operator Script" in markdown
    assert "R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW=READY" in markdown
    assert "SOURCE_R21T_C_BUILD_REVIEW_BOUND" in markdown
    assert "`OPERATOR_SCRIPT_REVIEW_ONLY` = `True`" in markdown
    assert "SCRIPT_FILE_CREATED" in markdown
    assert "PS1_CREATED" in markdown
    assert "SCRIPT_EXECUTED" in markdown
    assert "RUNNER_EXECUTED" in markdown
    assert "RUNTIME_EXECUTION_ALLOWED" in markdown
    assert "NO_RUNTIME_EXECUTION" in markdown
    assert "NO_DOCKER_CALL" in markdown
    assert "NO_REFLEX_APP_START" in markdown
    assert "NO_PREVIEW_ATTEMPT" in markdown
    assert "HTTP_FRONTEND_NON_EMPTY_REQUIRED" in markdown
    assert "TCP_ONLY_NOT_PREVIEW_READY" in markdown
    assert "PREVIEW_ONLY_AFTER_HTTP_PASS" in markdown
    assert "NO_FRONTEND_HOST_FLAG" in markdown
    assert "HARD_TIMEOUT_REQUIRED" in markdown
    assert "GIT_ARCHIVE_HEAD_COPY_REQUIRED" in markdown
    assert f"NEXT={NEXT_STEP}" in markdown
    assert "<html" not in markdown.lower()


def test_r21t_d_files_have_no_forbidden_runtime_or_write_strings() -> None:
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
        "browser" + r"\s+" + "open",
        "05" + "_EXPORTS",
    )

    for target in R21T_D_FILES:
        text = target.read_text(encoding="utf-8").lower()
        for pattern in forbidden_patterns:
            assert re.search(pattern.lower(), text) is None


def test_no_r21t_d_script_html_runtime_or_export_file_is_tracked() -> None:
    tracked = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.splitlines()

    r21t_d_paths = [path.lower() for path in tracked if "r21t_d" in path.lower()]

    assert all(not path.endswith(".html") for path in r21t_d_paths)
    assert all(not path.endswith(".ps1") for path in r21t_d_paths)
    assert all("export" not in path for path in r21t_d_paths)
