from __future__ import annotations

import re
import subprocess
from pathlib import Path

from mvp_qaic_py.reflex_private_preview_operator_script_dry_build_r21t_e import (
    DRY_BUILD_ID,
    NEXT_STEP,
    OPERATOR_DRY_BUILD_SECTIONS,
    PS1_PATH,
    R21T_E_FILES,
    REFLEX_VERSION,
    REQUIRED_DRY_BUILD_ENTRY_IDS,
    build_private_preview_operator_script_dry_build,
    build_private_preview_operator_script_dry_build_with_sources,
    operator_script_dry_build_to_dict,
    render_private_preview_operator_script_dry_build_markdown,
    validate_private_preview_operator_script_dry_build,
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_r21t_e_exact_four_required_files_exist_and_imports_are_valid() -> None:
    assert len(R21T_E_FILES) == 4
    assert len({path.as_posix() for path in R21T_E_FILES}) == 4
    for target in R21T_E_FILES:
        assert target.exists()

    dry_build = build_private_preview_operator_script_dry_build()
    payload = operator_script_dry_build_to_dict(dry_build)

    assert payload["dry_build_id"] == DRY_BUILD_ID
    assert payload["R21T_E_PRIVATE_PREVIEW_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN"] == "READY"
    assert validate_private_preview_operator_script_dry_build(payload) == ()


def test_r21t_e_binds_r21t_d_operator_script_review() -> None:
    payload = build_private_preview_operator_script_dry_build_with_sources()
    bindings = payload["source_bindings"]
    summaries = payload["source_summaries"]

    assert bindings["SOURCE_R21T_D_OPERATOR_SCRIPT_REVIEW_BOUND"] is True
    assert summaries["r21t_d_operator_script_review"] == (
        "R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW_ONLY"
    )
    assert summaries["r21t_d_status"] == "READY"
    assert summaries["r21t_d_reflex_version"] == REFLEX_VERSION
    assert summaries["r21t_d_next_step"] == DRY_BUILD_ID


def test_r21t_e_contains_all_required_status_tokens() -> None:
    tokens = build_private_preview_operator_script_dry_build_with_sources()[
        "dry_build_tokens"
    ]

    assert tokens["R21T_E_PRIVATE_PREVIEW_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN"] == "READY"
    assert tokens["SOURCE_R21T_D_OPERATOR_SCRIPT_REVIEW_BOUND"] is True
    assert tokens["SCRIPT_DRY_BUILD_ONLY"] is True
    assert tokens["SCRIPT_FILE_CREATED"] is True
    assert tokens["PS1_CREATED"] is True
    assert tokens["SCRIPT_EXECUTED"] is False
    assert tokens["RUNNER_EXECUTED"] is False
    assert tokens["RUNTIME_EXECUTION_ALLOWED"] is False
    assert tokens["NO_RUNTIME_EXECUTION"] is True
    assert tokens["NO_DOCKER_EXECUTION"] is True
    assert tokens["NO_REFLEX_APP_START"] is True
    assert tokens["NO_PREVIEW_ATTEMPT"] is True
    assert tokens["NO_PORTS_OPENED"] is True
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
    assert tokens["REFLEX_RUNTIME_RUNNER_CHAIN"] == (
        "STOPPED_AFTER_OPERATOR_SCRIPT_DRY_BUILD"
    )
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


def test_r21t_e_dry_build_sections_and_entries_are_no_run_only() -> None:
    payload = build_private_preview_operator_script_dry_build_with_sources()

    assert tuple(payload["dry_build_sections"]) == OPERATOR_DRY_BUILD_SECTIONS
    assert payload["dry_build_sections"] == [
        "STRICT_PREFLIGHT_DRY_PLAN",
        "HARD_TIMEOUT_NATIVE_CALLS_REQUIRED_LATER",
        "PINNED_IMAGE_PREFLIGHT_REQUIRED_LATER",
        "PRIVATE_PORT_PREFLIGHT_REQUIRED_LATER",
        "FULL_HEAD_COPY_BY_ARCHIVE_TAR_REQUIRED_LATER",
        "POLICY_GUARD_CHECKS_REQUIRED_LATER",
        "HELP_VERSION_EVIDENCE_REUSE",
        "PREVIEW_READINESS_PROBES_REQUIRED_LATER",
        "FAILURE_STOP_DIAGNOSTICS_REQUIRED_LATER",
        "SUMMARY_NO_RUN_ONLY",
    ]

    entries = payload["dry_build_entries"]
    assert [entry["ordinal"] for entry in entries] == sorted(
        entry["ordinal"] for entry in entries
    )
    assert [entry["dry_build_entry_id"] for entry in entries] == list(
        REQUIRED_DRY_BUILD_ENTRY_IDS
    )
    assert all(entry["dry_build_only"] is True for entry in entries)
    assert all(entry["script_execution_allowed"] is False for entry in entries)
    assert all(entry["runtime_execution_allowed"] is False for entry in entries)
    assert all(entry["preview_readiness_claimed"] is False for entry in entries)


def test_r21t_e_markdown_is_text_only_and_names_next_step() -> None:
    markdown = render_private_preview_operator_script_dry_build_markdown()

    assert "R21T-E Private Preview Operator Script Dry Build" in markdown
    assert "R21T_E_PRIVATE_PREVIEW_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN=READY" in markdown
    assert "SOURCE_R21T_D_OPERATOR_SCRIPT_REVIEW_BOUND" in markdown
    assert "`SCRIPT_DRY_BUILD_ONLY` = `True`" in markdown
    assert "SCRIPT_FILE_CREATED" in markdown
    assert "PS1_CREATED" in markdown
    assert "SCRIPT_EXECUTED" in markdown
    assert "RUNNER_EXECUTED" in markdown
    assert "RUNTIME_EXECUTION_ALLOWED" in markdown
    assert "NO_RUNTIME_EXECUTION" in markdown
    assert "NO_DOCKER_EXECUTION" in markdown
    assert "NO_REFLEX_APP_START" in markdown
    assert "NO_PREVIEW_ATTEMPT" in markdown
    assert "NO_PORTS_OPENED" in markdown
    assert "HTTP_FRONTEND_NON_EMPTY_REQUIRED" in markdown
    assert "TCP_ONLY_NOT_PREVIEW_READY" in markdown
    assert "PREVIEW_ONLY_AFTER_HTTP_PASS" in markdown
    assert "NO_FRONTEND_HOST_FLAG" in markdown
    assert "HARD_TIMEOUT_REQUIRED" in markdown
    assert "GIT_ARCHIVE_HEAD_COPY_REQUIRED" in markdown
    assert f"NEXT={NEXT_STEP}" in markdown
    assert "<html" not in markdown.lower()


def test_r21t_e_ps1_exists_was_not_executed_and_is_ps51_safe_text() -> None:
    assert PS1_PATH.exists()
    text = _read(PS1_PATH)

    assert "FINAL_STATUS=R21T_E_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN_ONLY" in text
    assert "SCRIPT_EXECUTED=False" in text
    assert "RUNNER_EXECUTED=False" in text
    assert "Set-StrictMode -Version 2.0" in text
    assert "[System.IO.Directory]::CreateDirectory" in text
    assert "New-Item -LiteralPath" not in text
    assert "&&" not in text
    assert "? " not in text
    assert "::new(" not in text


def test_r21t_e_new_files_have_no_forbidden_runtime_or_write_strings() -> None:
    forbidden_patterns = (
        r"\breflex\s+run\b",
        r"\bdocker\s+run\b",
        r"(?m)^\s*&?\s*docker(\.exe)?\s+",
        r"(?m)^\s*&?\s*python(\.exe)?\s+",
        r"(?m)^\s*&?\s*reflex(\.exe)?\s+",
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

    for target in R21T_E_FILES:
        text = _read(target).lower()
        for pattern in forbidden_patterns:
            assert re.search(pattern.lower(), text) is None, (target, pattern)


def test_no_extra_r21t_e_runtime_html_export_or_shell_artifacts_are_tracked() -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "--others", "--cached", "--exclude-standard"],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.splitlines()

    r21t_e_paths = [path for path in tracked if "r21t_e" in path.lower()]

    assert sorted(r21t_e_paths) == sorted(path.as_posix() for path in R21T_E_FILES)
    assert all(not path.lower().endswith("." + "ht" + "ml") for path in r21t_e_paths)
    assert all("export" not in path.lower() for path in r21t_e_paths)
