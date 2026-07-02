from __future__ import annotations

import re
import subprocess
from pathlib import Path

from mvp_qaic_py.reflex_preview_runner_spec_r21s import (
    NEXT_STEP,
    REQUIRED_PHASES,
    REQUIRED_SPEC_ENTRY_IDS,
    SPEC_ID,
    build_preview_runner_spec,
    build_preview_runner_spec_with_sources,
    render_preview_runner_spec_markdown,
    spec_to_dict,
    validate_preview_runner_spec,
)


R21S_FILES = (
    Path("mvp_qaic_py/reflex_preview_runner_spec_r21s.py"),
    Path("docs/PRODUCT/R21S_REFLEX_PREVIEW_RUNNER_SPEC_REVIEW_ONLY.md"),
    Path("tests/test_r21s_reflex_preview_runner_spec.py"),
)


def test_r21s_required_files_and_imports_exist() -> None:
    for target in R21S_FILES:
        assert target.exists()

    spec = build_preview_runner_spec()
    payload = spec_to_dict(spec)

    assert payload["spec_id"] == SPEC_ID
    assert payload["R21S_REFLEX_PREVIEW_RUNNER_SPEC"] == "READY"
    assert validate_preview_runner_spec(payload) == ()


def test_r21s_binds_r21r_preview_strategy_audit() -> None:
    payload = build_preview_runner_spec_with_sources()
    bindings = payload["source_bindings"]
    summaries = payload["source_summaries"]

    assert bindings["SOURCE_R21R_PREVIEW_STRATEGY_BOUND"] is True
    assert summaries["r21r_preview_strategy"] == (
        "R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT_DOCS_ONLY"
    )
    assert summaries["r21r_status"] == "READY"
    assert summaries["r21r_next_step"] == SPEC_ID


def test_r21s_contains_required_review_only_tokens() -> None:
    tokens = build_preview_runner_spec_with_sources()["review_only_tokens"]

    assert tokens["R21S_REFLEX_PREVIEW_RUNNER_SPEC"] == "READY"
    assert tokens["SOURCE_R21R_PREVIEW_STRATEGY_BOUND"] is True
    assert tokens["RUNNER_SPEC_REVIEW_ONLY"] is True
    assert tokens["RUNNER_EXECUTED"] is False
    assert tokens["REFLEX_RUNTIME_STATUS"] == "PAUSED"
    assert tokens["REFLEX_RUNTIME_RUNNER_CHAIN"] == "STOPPED_UNTIL_HUMAN_APPROVAL"
    assert tokens["HUMAN_APPROVED_PRIVATE_PREVIEW_REQUIRED"] is True
    assert tokens["REFLEX_CLI_HELP_CAPTURE_REQUIRED"] is True
    assert tokens["REFLEX_VERSION_CAPTURE_REQUIRED"] is True
    assert tokens["NO_FRONTEND_HOST_FLAG"] is True
    assert tokens["NO_PUBLIC_DEPLOY"] is True
    assert tokens["NO_REFLEX_DEPLOY"] is True
    assert tokens["PS51_COMPATIBLE"] is True
    assert tokens["PROMPT_MD_REQUIRED"] is True
    assert tokens["RUNNER_SHORT_REQUIRED"] is True
    assert tokens["NO_GIANT_CONSOLE_PROMPT"] is True
    assert tokens["TARGETED_STAGING_ONLY"] is True
    assert tokens["NO_GIT_ADD_DOT"] is True
    assert tokens["NO_RESET"] is True
    assert tokens["DIRTY_START_STOP_NO_WRITE"] is True
    assert tokens["FAILED_TESTS_NO_COMMIT_NO_TAG_NO_PUSH"] is True
    assert tokens["HTTP_FRONTEND_NON_EMPTY_REQUIRED"] is True
    assert tokens["TCP_ONLY_NOT_PREVIEW_READY"] is True
    assert tokens["PREVIEW_ONLY_AFTER_HTTP_PASS"] is True
    assert tokens["HTTP_FAIL_STOP_AND_DIAG"] is True
    assert tokens["NO_RUNTIME"] is True
    assert tokens["NO_DOCKER"] is True
    assert tokens["NO_REFLEX_RUN"] is True
    assert tokens["NO_PROVIDER_CALL"] is True
    assert tokens["NO_BROKER_ORDER_SIZING"] is True
    assert tokens["NO_SHEET_BQ_WRITE"] is True
    assert tokens["NO_HTML_OUTPUT"] is True
    assert tokens["NEXT"] == NEXT_STEP


def test_r21s_required_runner_review_phases_are_present() -> None:
    payload = build_preview_runner_spec_with_sources()

    assert tuple(payload["required_phases"]) == REQUIRED_PHASES
    assert payload["required_phases"] == [
        "RUNNER_PREFLIGHT",
        "EVIDENCE_COLLECTION",
        "VALIDATION",
        "SUMMARY",
    ]


def test_r21s_spec_map_is_deterministic_review_only_and_complete() -> None:
    first = build_preview_runner_spec_with_sources()
    second = build_preview_runner_spec_with_sources()
    entries = first["spec_entries"]

    assert first == second
    assert [entry["ordinal"] for entry in entries] == sorted(entry["ordinal"] for entry in entries)
    assert [entry["spec_entry_id"] for entry in entries] == list(REQUIRED_SPEC_ENTRY_IDS)
    assert all(entry["human_review_required"] is True for entry in entries)
    assert all(entry["runtime_execution_allowed"] is False for entry in entries)


def test_r21s_markdown_is_text_only_and_names_next_step() -> None:
    markdown = render_preview_runner_spec_markdown()

    assert "R21S Reflex Preview Runner Spec" in markdown
    assert "R21S_REFLEX_PREVIEW_RUNNER_SPEC=READY" in markdown
    assert "SOURCE_R21R_PREVIEW_STRATEGY_BOUND" in markdown
    assert "RUNNER_SPEC_REVIEW_ONLY" in markdown
    assert "RUNNER_EXECUTED" in markdown
    assert "REFLEX_RUNTIME_STATUS" in markdown
    assert "REFLEX_RUNTIME_RUNNER_CHAIN" in markdown
    assert "REFLEX_CLI_HELP_CAPTURE_REQUIRED" in markdown
    assert "REFLEX_VERSION_CAPTURE_REQUIRED" in markdown
    assert "HTTP_FRONTEND_NON_EMPTY_REQUIRED" in markdown
    assert "NO_REFLEX_RUN" in markdown
    assert f"NEXT={NEXT_STEP}" in markdown
    assert "<html" not in markdown.lower()


def test_r21s_files_have_no_forbidden_runtime_or_write_strings() -> None:
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

    for target in R21S_FILES:
        text = target.read_text(encoding="utf-8").lower()
        for pattern in forbidden_patterns:
            assert re.search(pattern.lower(), text) is None


def test_no_r21s_html_or_runtime_file_is_tracked() -> None:
    tracked = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.splitlines()

    r21s_paths = [path.lower() for path in tracked if "r21s" in path.lower()]

    assert all(not path.endswith(".html") for path in r21s_paths)
    assert all(not path.endswith(".ps1") for path in r21s_paths)
    assert all("export" not in path for path in r21s_paths)
