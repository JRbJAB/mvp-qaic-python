from __future__ import annotations

import re
import subprocess
from pathlib import Path

from mvp_qaic_py.reflex_private_preview_operator_script_arming_review_r21t_f import (
    ARMING_REVIEW_ID,
    ARMING_REVIEW_SECTIONS,
    NEXT_STEP,
    R21T_E_PS1_PATH,
    R21T_F_FILES,
    REFLEX_VERSION,
    REQUIRED_ARMING_ENTRY_IDS,
    REQUIRED_FINAL_OPERATOR_MARKER,
    build_private_preview_operator_script_arming_review,
    build_private_preview_operator_script_arming_review_with_sources,
    operator_script_arming_review_to_dict,
    render_private_preview_operator_script_arming_review_markdown,
    validate_private_preview_operator_script_arming_review,
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_r21t_f_exact_three_required_files_exist_and_imports_are_valid() -> None:
    assert len(R21T_F_FILES) == 3
    assert len({path.as_posix() for path in R21T_F_FILES}) == 3
    for target in R21T_F_FILES:
        assert target.exists()

    arming_review = build_private_preview_operator_script_arming_review()
    payload = operator_script_arming_review_to_dict(arming_review)

    assert payload["arming_review_id"] == ARMING_REVIEW_ID
    assert (
        payload["R21T_F_PRIVATE_PREVIEW_OPERATOR_SCRIPT_REVIEW_AND_ARMING_NO_RUN"]
        == "READY"
    )
    assert validate_private_preview_operator_script_arming_review(payload) == ()


def test_r21t_f_binds_r21t_e_dry_build_and_ps1_exists_without_execution() -> None:
    payload = build_private_preview_operator_script_arming_review_with_sources()
    bindings = payload["source_bindings"]
    summaries = payload["source_summaries"]

    assert bindings["SOURCE_R21T_E_DRY_BUILD_BOUND"] is True
    assert bindings["OPERATOR_SCRIPT_EXISTS"] is True
    assert bindings["OPERATOR_SCRIPT_EXECUTED"] is False
    assert R21T_E_PS1_PATH.exists()
    assert summaries["r21t_e_dry_build"] == (
        "R21T_E_PRIVATE_PREVIEW_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN"
    )
    assert summaries["r21t_e_status"] == "READY"
    assert summaries["r21t_e_script_executed"] is False
    assert summaries["r21t_e_runtime_execution_allowed"] is False
    assert summaries["r21t_e_reflex_version"] == REFLEX_VERSION
    assert summaries["r21t_e_next_step"] == ARMING_REVIEW_ID


def test_r21t_f_contains_all_required_status_tokens() -> None:
    tokens = build_private_preview_operator_script_arming_review_with_sources()[
        "arming_review_tokens"
    ]

    assert tokens["R21T_F_PRIVATE_PREVIEW_OPERATOR_SCRIPT_REVIEW_AND_ARMING_NO_RUN"] == (
        "READY"
    )
    assert tokens["SOURCE_R21T_E_DRY_BUILD_BOUND"] is True
    assert tokens["OPERATOR_SCRIPT_EXISTS"] is True
    assert tokens["OPERATOR_SCRIPT_EXECUTED"] is False
    assert tokens["ARMING_REVIEW_ONLY"] is True
    assert tokens["ARMING_READY"] is False
    assert tokens["RUNTIME_ARMED"] is False
    assert tokens["RUNTIME_EXECUTION_ALLOWED"] is False
    assert tokens["SCRIPT_EXECUTION_ALLOWED"] is False
    assert tokens["NO_RUNTIME_EXECUTION"] is True
    assert tokens["NO_DOCKER_EXECUTION"] is True
    assert tokens["NO_REFLEX_APP_START"] is True
    assert tokens["NO_PREVIEW_ATTEMPT"] is True
    assert tokens["NO_PORTS_OPENED"] is True
    assert tokens["NO_BROWSER"] is True
    assert tokens["REFLEX_VERSION"] == "0.9.6.post1"
    assert tokens["HELP_VERSION_CAPTURE_PASSED"] is True
    assert tokens["NO_FRONTEND_HOST_FLAG"] is True
    assert tokens["HTTP_FRONTEND_NON_EMPTY_REQUIRED"] is True
    assert tokens["TCP_ONLY_NOT_PREVIEW_READY"] is True
    assert tokens["PREVIEW_ONLY_AFTER_HTTP_PASS"] is True
    assert tokens["REFLEX_RUNTIME_STATUS"] == "PAUSED"
    assert tokens["REFLEX_RUNTIME_RUNNER_CHAIN"] == (
        "STOPPED_AFTER_ARMING_REVIEW_NO_RUN"
    )
    assert tokens["REQUIRED_FINAL_OPERATOR_MARKER"] == REQUIRED_FINAL_OPERATOR_MARKER
    assert tokens["FINAL_OPERATOR_MARKER_PRESENT"] is False
    assert tokens["PS51_COMPATIBLE"] is True
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


def test_r21t_f_arming_sections_entries_and_final_marker_gate_are_closed() -> None:
    payload = build_private_preview_operator_script_arming_review_with_sources()

    assert tuple(payload["arming_review_sections"]) == ARMING_REVIEW_SECTIONS
    assert payload["arming_review_sections"] == [
        "R21T_E_DRY_BUILD_BINDING",
        "OPERATOR_SCRIPT_EXISTENCE_REVIEW",
        "SCRIPT_NOT_EXECUTED",
        "ARMING_REVIEW_ONLY_BOUNDARY",
        "FINAL_OPERATOR_MARKER_GATE_REQUIRED",
        "RUNTIME_REMAINS_PAUSED",
        "READINESS_REQUIRES_HTTP_FRONTEND",
        "RUNNER_HARDENING_REQUIREMENTS_PRESERVED",
        "SAFETY_LOCKS_CLOSED",
        "R21T_G_NEXT_GATE",
    ]

    entries = payload["arming_review_entries"]
    assert [entry["ordinal"] for entry in entries] == sorted(
        entry["ordinal"] for entry in entries
    )
    assert [entry["arming_entry_id"] for entry in entries] == list(
        REQUIRED_ARMING_ENTRY_IDS
    )
    assert all(entry["arming_review_only"] is True for entry in entries)
    assert all(entry["arming_ready"] is False for entry in entries)
    assert all(entry["runtime_armed"] is False for entry in entries)
    assert all(entry["script_execution_allowed"] is False for entry in entries)

    tokens = payload["arming_review_tokens"]
    assert tokens["REQUIRED_FINAL_OPERATOR_MARKER"] == (
        "R21T_G_OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN_TRUE"
    )
    assert tokens["FINAL_OPERATOR_MARKER_PRESENT"] is False


def test_r21t_f_markdown_is_text_only_and_names_next_step() -> None:
    markdown = render_private_preview_operator_script_arming_review_markdown()

    assert "R21T-F Private Preview Operator Script Review and Arming" in markdown
    assert "R21T_F_PRIVATE_PREVIEW_OPERATOR_SCRIPT_REVIEW_AND_ARMING_NO_RUN=READY" in (
        markdown
    )
    assert "SOURCE_R21T_E_DRY_BUILD_BOUND" in markdown
    assert "OPERATOR_SCRIPT_EXISTS" in markdown
    assert "OPERATOR_SCRIPT_EXECUTED" in markdown
    assert "ARMING_REVIEW_ONLY" in markdown
    assert "ARMING_READY" in markdown
    assert "RUNTIME_ARMED" in markdown
    assert "SCRIPT_EXECUTION_ALLOWED" in markdown
    assert "FINAL_OPERATOR_MARKER_PRESENT" in markdown
    assert "HTTP_FRONTEND_NON_EMPTY_REQUIRED" in markdown
    assert "TCP_ONLY_NOT_PREVIEW_READY" in markdown
    assert "PREVIEW_ONLY_AFTER_HTTP_PASS" in markdown
    assert "NO_FRONTEND_HOST_FLAG" in markdown
    assert "HARD_TIMEOUT_REQUIRED" in markdown
    assert "GIT_ARCHIVE_HEAD_COPY_REQUIRED" in markdown
    assert f"NEXT={NEXT_STEP}" in markdown
    assert "<html" not in markdown.lower()


def test_r21t_f_ps1_review_confirms_artifact_is_not_executed() -> None:
    assert R21T_E_PS1_PATH.exists()
    text = _read(R21T_E_PS1_PATH)

    assert "FINAL_STATUS=R21T_E_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN_ONLY" in text
    assert "SCRIPT_EXECUTED=False" in text
    assert "RUNNER_EXECUTED=False" in text
    assert "Set-StrictMode -Version 2.0" in text
    assert "[System.IO.Directory]::CreateDirectory" in text
    assert "New-Item -LiteralPath" not in text
    assert "&&" not in text
    assert "? " not in text
    assert "::new(" not in text


def test_r21t_f_new_files_have_no_forbidden_runtime_or_write_strings() -> None:
    forbidden_patterns = (
        r"\breflex\s+" + "run" + r"\b",
        r"\bdocker\s+" + "run" + r"\b",
        r"(?m)^\s*&?\s*" + "docker" + r"(\.exe)?\s+",
        r"(?m)^\s*&?\s*" + "python" + r"(\.exe)?\s+",
        r"(?m)^\s*&?\s*" + "reflex" + r"(\.exe)?\s+",
        "--frontend" + "-host",
        "invoke" + "-expression",
        "invoke" + "-webrequest",
        r"\b" + "cu" + "rl" + r"\b",
        "start" + "-process",
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
        r"\." + "ht" + "ml" + r"\b",
    )

    for target in R21T_F_FILES:
        text = _read(target).lower()
        for pattern in forbidden_patterns:
            assert re.search(pattern.lower(), text) is None, (target, pattern)


def test_no_extra_r21t_f_files_or_runtime_artifacts_are_tracked() -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "--others", "--cached", "--exclude-standard"],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.splitlines()

    r21t_f_paths = [path for path in tracked if "r21t_f" in path.lower()]

    assert sorted(r21t_f_paths) == sorted(path.as_posix() for path in R21T_F_FILES)
    assert all(not path.lower().endswith("." + "ht" + "ml") for path in r21t_f_paths)
    assert all("export" not in path.lower() for path in r21t_f_paths)
