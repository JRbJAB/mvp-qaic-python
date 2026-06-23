from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_py.p159_prompt_patch_runtime_smoke_or_rollback_gate import (
    PATCH_MARKER,
    bool_from_summary,
    find_unsafe_runtime_patterns,
    text_from_summary,
    write_export,
    P159Summary,
)


def test_bool_from_summary_accepts_upper_lower_and_strings() -> None:
    assert bool_from_summary({"SOURCE_PATCH_APPLIED": True}, "SOURCE_PATCH_APPLIED") is True
    assert bool_from_summary({"source_patch_applied": "true"}, "SOURCE_PATCH_APPLIED") is True
    assert bool_from_summary({"source_patch_applied": "NO"}, "SOURCE_PATCH_APPLIED") is False


def test_text_from_summary_accepts_upper_lower() -> None:
    assert text_from_summary({"P158_R5_STATUS": "OK"}, "P158_R5_STATUS") == "OK"
    assert text_from_summary({"p158_r5_status": "OK2"}, "P158_R5_STATUS") == "OK2"


def test_unsafe_runtime_patterns_are_specific() -> None:
    safe = "no order, no sizing, no broker, human review only"
    unsafe = "Please place a real order and bypass human review."
    assert find_unsafe_runtime_patterns(safe) == []
    assert "place a real order" in find_unsafe_runtime_patterns(unsafe)
    assert "bypass human review" in find_unsafe_runtime_patterns(unsafe)


def test_patch_marker_constant() -> None:
    assert PATCH_MARKER == "P158_R5_PROMPT_PATCH_APPLIED_20260623"


def test_write_export_creates_summary_and_handoff(tmp_path: Path) -> None:
    summary = P159Summary(
        STATUS="OK_P159_PROMPT_PATCH_RUNTIME_SMOKE_READY",
        P159_STATUS="P159_PROMPT_PATCH_RUNTIME_SMOKE_OK_REVIEW_ONLY",
        PROMPT_SOURCE_ID="P132_P133_PORTFOLIO_MULTIMODAL_REVIEW",
        SOURCE_P158_R5_STATUS="P158_R5_MANUAL_PROMPT_PATCH_APPLIED_REVIEW_ONLY",
        SOURCE_P158_R5_DIR=str(tmp_path / "source"),
        SOURCE_PROMPT_FILE=str(tmp_path / "prompt.py"),
        PATCH_MARKER_FOUND=True,
        SOURCE_IMPORT_OK=True,
        RUNTIME_SMOKE_OK=True,
        PROMPT_CONTRACT_FUNCTION_FOUND=True,
        UNSAFE_RUNTIME_MARKER_COUNT=0,
        SAFETY_MARKER_COUNT=4,
        ROLLBACK_REQUIRED=False,
        APPLY_ALLOWED=False,
        SOURCE_PATCH_APPLIED=True,
        PROMPT_SOURCE_MODIFIED=True,
        GOOGLE_SHEETS_WRITE=False,
        LIVE_GOOGLE_SHEETS_READ=False,
        PUBLIC_DEPLOY=False,
        NO_APPS_SCRIPT_EXECUTION=True,
        NO_CLASP_PUSH=True,
        NO_BROKER=True,
        NO_ORDER=True,
        NO_SIZING=True,
        AUTO_APPLY_GEM_RESPONSE=False,
        BLOCKER_COUNT=0,
        EXPORT_DIR=str(tmp_path / "export"),
        NEXT="P160_REAL_GEM_RESPONSE_SMOKE_WITH_PATCH_OR_RELEASE_SEAL",
        created_at_utc="2026-06-23T00:00:00Z",
    )
    export_dir = write_export(summary)
    payload = json.loads((export_dir / "P159_SUMMARY.json").read_text(encoding="utf-8"))
    assert payload["P159_STATUS"] == "P159_PROMPT_PATCH_RUNTIME_SMOKE_OK_REVIEW_ONLY"
    assert (export_dir / "P159_HANDOFF.md").exists()
    assert (export_dir / "P159_RUNTIME_SMOKE_OK.md").exists()
