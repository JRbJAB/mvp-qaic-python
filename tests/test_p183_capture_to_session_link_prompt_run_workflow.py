from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_py.p183_capture_to_session_link_prompt_run_workflow import (
    build_capture_prompt_session_workflow,
    create_review_only_session,
    export_capture_session_workflow,
)


def _seed_project(project: Path) -> None:
    package_dir = project / "mvp_qaic_py"
    package_dir.mkdir(parents=True)
    (package_dir / "p173_nicegui_private_local_runner.py").write_text(
        "MVP QAIC — GEM Portfolio Image Review\nprompt gem portfolio image review_required\n",
        encoding="utf-8",
    )
    capture_dir = project / "00_OPERATOR_EXPORTS" / "P181_CAPTURE_INBOX"
    response_dir = project / "00_OPERATOR_EXPORTS" / "P181_GEM_RESPONSES"
    capture_dir.mkdir(parents=True)
    response_dir.mkdir(parents=True)
    (capture_dir / "capture.png").write_bytes(b"fake-image")
    (response_dir / "response.md").write_text("REVIEW_REQUIRED", encoding="utf-8")


def test_build_capture_prompt_session_workflow_ready(tmp_path: Path) -> None:
    _seed_project(tmp_path)

    payload = build_capture_prompt_session_workflow(tmp_path)

    assert payload["STATUS"] == "OK_P183_CAPTURE_TO_SESSION_LINK_WORKFLOW_READY"
    assert payload["workflow_ready"] is True
    assert payload["active_prompt_count"] >= 1
    assert payload["capture_count"] == 1
    assert payload["gem_response_count"] == 1
    assert payload["blocker_count"] == 0
    assert payload["gem_call_executed"] is False
    assert payload["google_sheets_write"] is False
    assert payload["auto_apply_gem_response"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_create_review_only_session_writes_session_json(tmp_path: Path) -> None:
    _seed_project(tmp_path)

    session = create_review_only_session(tmp_path)

    assert session["status"] == "SESSION_READY_FOR_HUMAN_REVIEW"
    assert session["human_review_required"] is True
    assert session["apply_allowed"] is False
    assert session["auto_apply_gem_response"] is False
    assert Path(session["session_path"]).exists()


def test_export_capture_session_workflow_writes_expected_files(tmp_path: Path) -> None:
    _seed_project(tmp_path)
    export_dir = tmp_path / "05_EXPORTS" / "P183_TEST_EXPORT"

    payload = export_capture_session_workflow(tmp_path, export_dir=export_dir, create_session=True)

    assert payload["workflow_ready"] is True
    assert payload["session_created"] is True
    assert (export_dir / "P183_CAPTURE_SESSION_WORKFLOW.json").exists()
    assert (export_dir / "P183_SUMMARY.json").exists()
    assert (export_dir / "P183_SESSION_LINK_INDEX.csv").exists()
    assert (export_dir / "P183_CAPTURE_SESSION_WORKFLOW_REPORT.md").exists()

    summary = json.loads((export_dir / "P183_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["recommended_next"] == "P184_REAL_GEM_SESSION_REVIEW_AND_RESPONSE_PARSER"
