from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_py.p158_manual_prompt_patch_apply_or_stop import (
    P157_READY_STATUS,
    P158_BLOCKED_STATUS,
    P158_WAITING_STATUS,
    build_and_write_export,
    load_p157_source,
    review_manual_apply_gate,
)


def write_p157_export(root: Path, *, unsafe: bool = False, status: str = P157_READY_STATUS) -> Path:
    export_dir = (
        root / "05_EXPORTS" / "P157_PROMPT_PATCH_CANDIDATE_REVIEW_OR_APPLY_GATE_20260623_141418"
    )
    export_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "P157_STATUS": status,
        "PROMPT_SOURCE_ID": "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW",
        "PATCH_CANDIDATE_FOUND": True,
        "PATCH_CANDIDATE_CREATED": True,
        "PATCH_SAFE_FOR_REVIEW": True,
        "UNSAFE_MARKER_COUNT": 0,
        "BLOCKER_COUNT": 0,
        "APPLY_ALLOWED": False,
        "PROMPT_SOURCE_MODIFIED": False,
        "GOOGLE_SHEETS_WRITE": False,
        "PUBLIC_DEPLOY": False,
    }
    if unsafe:
        summary["UNSAFE_MARKER_COUNT"] = 1
    (export_dir / "P157_SUMMARY.json").write_text(json.dumps(summary), encoding="utf-8")
    candidate = "# Patch candidate\n\nreview-only, no apply, human review, apply_allowed=false\n"
    if unsafe:
        candidate += "\nplace order now\n"
    (export_dir / "P157_PROMPT_PATCH_CANDIDATE_READBACK.md").write_text(candidate, encoding="utf-8")
    return export_dir


def test_p158_loads_p157_source(tmp_path: Path) -> None:
    source_dir = write_p157_export(tmp_path)
    source = load_p157_source(tmp_path, source_dir=source_dir)

    assert source.summary["P157_STATUS"] == P157_READY_STATUS
    assert "Patch candidate" in source.candidate_text


def test_p158_stops_waiting_for_manual_authorization(tmp_path: Path) -> None:
    write_p157_export(tmp_path)
    summary = review_manual_apply_gate(tmp_path)

    assert summary.status == P158_WAITING_STATUS
    assert summary.candidate_ready_for_manual_apply is True
    assert summary.manual_apply_authorized is False
    assert summary.source_patch_applied is False
    assert summary.apply_allowed is False
    assert summary.prompt_source_modified is False
    assert summary.blocker_count == 1
    assert "WAITING_MANUAL_APPLY_AUTHORIZATION" in summary.blockers


def test_p158_blocks_unsafe_candidate(tmp_path: Path) -> None:
    write_p157_export(tmp_path, unsafe=True)
    summary = review_manual_apply_gate(tmp_path)

    assert summary.status == P158_BLOCKED_STATUS
    assert summary.candidate_ready_for_manual_apply is False
    assert summary.unsafe_marker_count >= 1
    assert "UNSAFE_MARKERS_FOUND" in summary.blockers
    assert summary.source_patch_applied is False


def test_p158_blocks_wrong_p157_status(tmp_path: Path) -> None:
    write_p157_export(tmp_path, status="P157_STOP_PATCH_CANDIDATE_REVIEW_BLOCKED")
    summary = review_manual_apply_gate(tmp_path)

    assert summary.status == P158_BLOCKED_STATUS
    assert "P157_STATUS_NOT_READY" in summary.blockers


def test_p158_writes_export_files(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[tool.pytest.ini_options]\n", encoding="utf-8")
    write_p157_export(tmp_path)
    summary = build_and_write_export(tmp_path)
    output_dir = Path(summary.output_dir)

    assert (output_dir / "P158_SUMMARY.json").exists()
    assert (output_dir / "P158_MANUAL_APPLY_DECISION.csv").exists()
    assert (output_dir / "P158_MANUAL_APPLY_GATE.md").exists()
    assert (output_dir / "P158_PROMPT_PATCH_CANDIDATE_READBACK.md").exists()
    assert (output_dir / "P158_HANDOFF.md").exists()


def test_p158_never_modifies_prompt_source_flags(tmp_path: Path) -> None:
    write_p157_export(tmp_path)
    summary = review_manual_apply_gate(tmp_path)

    assert summary.google_sheets_write is False
    assert summary.live_google_sheets_read is False
    assert summary.public_deploy is False
    assert summary.no_apps_script_execution is True
    assert summary.no_clasp_push is True
    assert summary.no_broker is True
    assert summary.no_order is True
    assert summary.no_sizing is True
    assert summary.no_auto_apply_gem_response is True
