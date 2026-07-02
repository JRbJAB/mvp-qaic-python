from __future__ import annotations

import re
import subprocess
from pathlib import Path

from mvp_qaic_py.reflex_help_version_capture_review_r21t_b import (
    NEXT_STEP,
    REFLEX_VERSION,
    REQUIRED_CAPTURE_ENTRY_IDS,
    REVIEW_ID,
    build_help_version_capture_review,
    build_help_version_capture_review_with_sources,
    help_version_capture_review_to_dict,
    render_help_version_capture_markdown,
    validate_help_version_capture_review,
)


R21T_B_FILES = (
    Path("mvp_qaic_py/reflex_help_version_capture_review_r21t_b.py"),
    Path("docs/PRODUCT/R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW_ONLY.md"),
    Path("tests/test_r21t_b_help_version_capture_review.py"),
)


def test_r21t_b_required_files_and_imports_exist() -> None:
    for target in R21T_B_FILES:
        assert target.exists()

    review = build_help_version_capture_review()
    payload = help_version_capture_review_to_dict(review)

    assert payload["review_id"] == REVIEW_ID
    assert payload["R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW"] == "READY"
    assert validate_help_version_capture_review(payload) == ()


def test_r21t_b_binds_r21t_a_approval_review() -> None:
    payload = build_help_version_capture_review_with_sources()
    bindings = payload["source_bindings"]
    summaries = payload["source_summaries"]

    assert bindings["SOURCE_R21T_A_APPROVAL_REVIEW_BOUND"] is True
    assert summaries["r21t_a_approval_review"] == (
        "R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW_ONLY"
    )
    assert summaries["r21t_a_status"] == "READY"
    assert summaries["r21t_a_required_marker"] == "HUMAN_APPROVED_PRIVATE_PREVIEW_TRUE"


def test_r21t_b_contains_required_help_version_capture_tokens() -> None:
    tokens = build_help_version_capture_review_with_sources()["help_version_review_tokens"]

    assert tokens["R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW"] == "READY"
    assert tokens["SOURCE_R21T_A_APPROVAL_REVIEW_BOUND"] is True
    assert tokens["HUMAN_APPROVED_PRIVATE_PREVIEW"] is True
    assert (
        tokens["HUMAN_APPROVED_PRIVATE_PREVIEW_MARKER"]
        == "HUMAN_APPROVED_PRIVATE_PREVIEW_TRUE"
    )
    assert tokens["HELP_VERSION_CAPTURE_EXECUTED"] is True
    assert tokens["REFLEX_VERSION_CAPTURED"] is True
    assert tokens["REFLEX_RUN_HELP_CAPTURED"] is True
    assert tokens["REFLEX_VERSION"] == REFLEX_VERSION
    assert tokens["HELP_ALLOWED_FLAGS_CAPTURED"] is True
    assert tokens["HELP_FORBIDDEN_FRONTEND_HOST_FOUND"] is False
    assert tokens["NO_FRONTEND_HOST_FLAG"] is True
    assert tokens["NO_RUNTIME_APP_START"] is True
    assert tokens["NO_PREVIEW_ATTEMPT"] is True
    assert tokens["NO_PORTS"] is True
    assert tokens["NO_BROWSER"] is True
    assert tokens["REFLEX_RUNTIME_STATUS"] == "PAUSED"
    assert tokens["REFLEX_RUNTIME_RUNNER_CHAIN"] == "STOPPED_AFTER_HELP_VERSION_CAPTURE"
    assert tokens["HTTP_FRONTEND_NON_EMPTY_REQUIRED"] is True
    assert tokens["TCP_ONLY_NOT_PREVIEW_READY"] is True
    assert tokens["PREVIEW_ONLY_AFTER_HTTP_PASS"] is True
    assert tokens["NO_PUBLIC_DEPLOY"] is True
    assert tokens["NO_REFLEX_DEPLOY"] is True
    assert tokens["NO_PROVIDER_CALL"] is True
    assert tokens["NO_BROKER_ORDER_SIZING"] is True
    assert tokens["NO_SHEET_BQ_WRITE"] is True
    assert tokens["NO_HTML_OUTPUT"] is True
    assert tokens["NEXT"] == NEXT_STEP


def test_r21t_b_evidence_files_are_recorded_under_run_reports() -> None:
    files = build_help_version_capture_review_with_sources()["evidence_files"]

    assert set(files) == {
        "VERSION_CAPTURE_FILE",
        "HELP_CAPTURE_FILE",
        "SUMMARY_EVIDENCE_FILE",
    }
    assert files["VERSION_CAPTURE_FILE"].endswith("REFLEX_VERSION.txt")
    assert files["HELP_CAPTURE_FILE"].endswith("REFLEX_RUN_HELP.txt")
    assert files["SUMMARY_EVIDENCE_FILE"].endswith("R21T_B_HELP_VERSION_EVIDENCE.txt")
    assert all("_RUN_REPORTS/MVP_QAIC_PY" in value for value in files.values())


def test_r21t_b_capture_map_is_deterministic_review_only_and_complete() -> None:
    first = build_help_version_capture_review_with_sources()
    second = build_help_version_capture_review_with_sources()
    entries = first["capture_entries"]

    assert first == second
    assert [entry["ordinal"] for entry in entries] == sorted(entry["ordinal"] for entry in entries)
    assert [entry["capture_entry_id"] for entry in entries] == list(REQUIRED_CAPTURE_ENTRY_IDS)
    assert all(entry["evidence_passed"] is True for entry in entries)
    assert all(entry["preview_readiness_claimed"] is False for entry in entries)
    assert all(entry["runtime_action_allowed"] is False for entry in entries)


def test_r21t_b_markdown_is_text_only_and_names_next_step() -> None:
    markdown = render_help_version_capture_markdown()

    assert "R21T-B Operator-Approved Help/Version Capture" in markdown
    assert "R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW=READY" in markdown
    assert "SOURCE_R21T_A_APPROVAL_REVIEW_BOUND" in markdown
    assert "`HUMAN_APPROVED_PRIVATE_PREVIEW` = `True`" in markdown
    assert "HUMAN_APPROVED_PRIVATE_PREVIEW_TRUE" in markdown
    assert "HELP_VERSION_CAPTURE_EXECUTED" in markdown
    assert "REFLEX_VERSION_CAPTURED" in markdown
    assert "REFLEX_RUN_HELP_CAPTURED" in markdown
    assert REFLEX_VERSION in markdown
    assert "HELP_ALLOWED_FLAGS_CAPTURED" in markdown
    assert "HELP_FORBIDDEN_FRONTEND_HOST_FOUND" in markdown
    assert "NO_FRONTEND_HOST_FLAG" in markdown
    assert "NO_PREVIEW_ATTEMPT" in markdown
    assert "HTTP_FRONTEND_NON_EMPTY_REQUIRED" in markdown
    assert f"NEXT={NEXT_STEP}" in markdown
    assert "<html" not in markdown.lower()


def test_r21t_b_files_have_no_forbidden_runtime_or_write_strings() -> None:
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

    for target in R21T_B_FILES:
        text = target.read_text(encoding="utf-8").lower()
        for pattern in forbidden_patterns:
            assert re.search(pattern.lower(), text) is None


def test_no_r21t_b_html_runtime_or_export_file_is_tracked() -> None:
    tracked = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.splitlines()

    r21t_b_paths = [path.lower() for path in tracked if "r21t_b" in path.lower()]

    assert all(not path.endswith(".html") for path in r21t_b_paths)
    assert all(not path.endswith(".ps1") for path in r21t_b_paths)
    assert all("export" not in path for path in r21t_b_paths)
