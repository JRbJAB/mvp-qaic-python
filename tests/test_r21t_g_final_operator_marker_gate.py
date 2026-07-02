from __future__ import annotations

import re
import subprocess
from pathlib import Path

from mvp_qaic_py.reflex_private_preview_final_operator_marker_gate_r21t_g import (
    MARKER_GATE_ID,
    MARKER_GATE_SECTIONS,
    NEXT_STEP,
    R21T_F_ARMING_REVIEW_ID,
    R21T_G_FILES,
    REFLEX_VERSION,
    REQUIRED_FINAL_OPERATOR_MARKER,
    REQUIRED_MARKER_ENTRY_IDS,
    build_final_operator_marker_gate,
    build_final_operator_marker_gate_with_sources,
    final_operator_marker_gate_to_dict,
    render_final_operator_marker_gate_markdown,
    validate_final_operator_marker_gate,
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_r21t_g_exact_three_required_files_exist_and_imports_are_valid() -> None:
    assert len(R21T_G_FILES) == 3
    assert len({path.as_posix() for path in R21T_G_FILES}) == 3
    for target in R21T_G_FILES:
        assert target.exists()

    marker_gate = build_final_operator_marker_gate()
    payload = final_operator_marker_gate_to_dict(marker_gate)

    assert payload["marker_gate_id"] == MARKER_GATE_ID
    assert payload["R21T_G_FINAL_OPERATOR_MARKER_GATE_NO_RUN"] == "READY"
    assert validate_final_operator_marker_gate(payload) == ()


def test_r21t_g_binds_r21t_f_arming_review_and_marker_is_absent() -> None:
    payload = build_final_operator_marker_gate_with_sources()
    bindings = payload["source_bindings"]
    summaries = payload["source_summaries"]

    assert bindings["SOURCE_R21T_F_ARMING_REVIEW_BOUND"] is True
    assert summaries["r21t_f_arming_review"] == R21T_F_ARMING_REVIEW_ID
    assert summaries["r21t_f_status"] == "READY"
    assert summaries["r21t_f_final_operator_marker"] == (
        "R21T_G_OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN_TRUE"
    )
    assert summaries["r21t_f_final_operator_marker_present"] is False
    assert summaries["r21t_f_arming_ready"] is False
    assert summaries["r21t_f_runtime_armed"] is False
    assert summaries["r21t_f_script_execution_allowed"] is False
    assert summaries["r21t_f_runtime_execution_allowed"] is False
    assert summaries["r21t_f_reflex_version"] == REFLEX_VERSION
    assert summaries["r21t_f_next_step"] == MARKER_GATE_ID


def test_r21t_g_contains_all_required_status_tokens() -> None:
    tokens = build_final_operator_marker_gate_with_sources()["marker_gate_tokens"]

    assert tokens["R21T_G_FINAL_OPERATOR_MARKER_GATE_NO_RUN"] == "READY"
    assert tokens["SOURCE_R21T_F_ARMING_REVIEW_BOUND"] is True
    assert tokens["MARKER_GATE_ONLY"] is True
    assert tokens["REQUIRED_FINAL_OPERATOR_MARKER"] == REQUIRED_FINAL_OPERATOR_MARKER
    assert tokens["FINAL_OPERATOR_MARKER_PRESENT"] is False
    assert tokens["FINAL_OPERATOR_MARKER_ACCEPTED"] is False
    assert tokens["OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN"] is False
    assert tokens["ARMING_REVIEW_PASSED"] is True
    assert tokens["ARMING_READY"] is False
    assert tokens["RUNTIME_ARMED"] is False
    assert tokens["SCRIPT_EXECUTION_ALLOWED"] is False
    assert tokens["RUNTIME_EXECUTION_ALLOWED"] is False
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
        "STOPPED_AT_FINAL_OPERATOR_MARKER_GATE_NO_RUN"
    )
    assert tokens["PS51_COMPATIBLE"] is True
    assert tokens["HARD_TIMEOUT_REQUIRED"] is True
    assert tokens["IMAGE_PREFLIGHT_REQUIRED"] is True
    assert tokens["PORT_PREFLIGHT_REQUIRED"] is True
    assert tokens["GIT_ARCHIVE_HEAD_COPY_REQUIRED"] is True
    assert tokens["POLICY_GUARDS_REQUIRED"] is True
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


def test_r21t_g_marker_sections_entries_and_execution_gate_are_closed() -> None:
    payload = build_final_operator_marker_gate_with_sources()

    assert tuple(payload["marker_gate_sections"]) == MARKER_GATE_SECTIONS
    assert payload["marker_gate_sections"] == [
        "R21T_F_ARMING_REVIEW_BINDING",
        "FINAL_OPERATOR_MARKER_REQUIRED_EXACT",
        "FINAL_OPERATOR_MARKER_ABSENT",
        "FINAL_OPERATOR_MARKER_NOT_ACCEPTED",
        "OPERATOR_APPROVAL_FALSE",
        "ARMING_REVIEW_PASSED_BUT_ARMING_NOT_READY",
        "RUNTIME_AND_SCRIPT_EXECUTION_CLOSED",
        "READINESS_REQUIRES_HTTP_FRONTEND",
        "RUNNER_HARDENING_REQUIREMENTS_PRESERVED",
        "SAFETY_LOCKS_CLOSED",
        "WAIT_FOR_OPERATOR_MARKER",
    ]

    entries = payload["marker_gate_entries"]
    assert [entry["ordinal"] for entry in entries] == sorted(
        entry["ordinal"] for entry in entries
    )
    assert [entry["marker_entry_id"] for entry in entries] == list(
        REQUIRED_MARKER_ENTRY_IDS
    )
    assert all(entry["marker_gate_only"] is True for entry in entries)
    assert all(entry["final_operator_marker_present"] is False for entry in entries)
    assert all(entry["final_operator_marker_accepted"] is False for entry in entries)
    assert all(
        entry["operator_approved_private_preview_run"] is False for entry in entries
    )
    assert all(entry["runtime_armed"] is False for entry in entries)
    assert all(entry["script_execution_allowed"] is False for entry in entries)
    assert all(entry["runtime_execution_allowed"] is False for entry in entries)


def test_r21t_g_markdown_is_text_only_and_names_next_step() -> None:
    markdown = render_final_operator_marker_gate_markdown()

    assert "R21T-G Final Operator Marker Gate" in markdown
    assert "R21T_G_FINAL_OPERATOR_MARKER_GATE_NO_RUN=READY" in markdown
    assert "SOURCE_R21T_F_ARMING_REVIEW_BOUND" in markdown
    assert "MARKER_GATE_ONLY" in markdown
    assert "REQUIRED_FINAL_OPERATOR_MARKER" in markdown
    assert "FINAL_OPERATOR_MARKER_PRESENT" in markdown
    assert "FINAL_OPERATOR_MARKER_ACCEPTED" in markdown
    assert "OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN" in markdown
    assert "ARMING_REVIEW_PASSED" in markdown
    assert "ARMING_READY" in markdown
    assert "RUNTIME_ARMED" in markdown
    assert "SCRIPT_EXECUTION_ALLOWED" in markdown
    assert "RUNTIME_EXECUTION_ALLOWED" in markdown
    assert "HTTP_FRONTEND_NON_EMPTY_REQUIRED" in markdown
    assert "TCP_ONLY_NOT_PREVIEW_READY" in markdown
    assert "PREVIEW_ONLY_AFTER_HTTP_PASS" in markdown
    assert "NO_FRONTEND_HOST_FLAG" in markdown
    assert "HARD_TIMEOUT_REQUIRED" in markdown
    assert "GIT_ARCHIVE_HEAD_COPY_REQUIRED" in markdown
    assert f"NEXT={NEXT_STEP}" in markdown
    assert "<html" not in markdown.lower()


def test_r21t_g_new_files_have_no_forbidden_runtime_or_write_strings() -> None:
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

    for target in R21T_G_FILES:
        text = _read(target).lower()
        for pattern in forbidden_patterns:
            assert re.search(pattern.lower(), text) is None, (target, pattern)


def test_no_extra_r21t_g_files_or_runtime_artifacts_are_tracked() -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "--others", "--cached", "--exclude-standard"],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.splitlines()

    r21t_g_paths = [path for path in tracked if "r21t_g" in path.lower()]

    assert sorted(r21t_g_paths) == sorted(path.as_posix() for path in R21T_G_FILES)
    assert all(not path.lower().endswith("." + "ht" + "ml") for path in r21t_g_paths)
    assert all("export" not in path.lower() for path in r21t_g_paths)
