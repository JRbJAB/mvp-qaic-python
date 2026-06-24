from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_py.p182_prompt_history_library_version_studio import (
    build_prompt_history_library,
    export_prompt_history_library,
)


def test_build_prompt_history_library_ready() -> None:
    payload = build_prompt_history_library(Path.cwd())

    assert payload["STATUS"] == "OK_P182_PROMPT_HISTORY_LIBRARY_VERSION_STUDIO_READY"
    assert payload["library_ready"] is True
    assert payload["prompt_version_count"] >= 1
    assert payload["active_prompt_count"] >= 1
    assert payload["blocker_count"] == 0
    assert payload["gem_call_executed"] is False
    assert payload["google_sheets_write"] is False
    assert payload["auto_apply_gem_response"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_export_prompt_history_library_writes_expected_files(tmp_path: Path) -> None:
    project = tmp_path
    package_dir = project / "mvp_qaic_py"
    package_dir.mkdir(parents=True)
    runner = package_dir / "p173_nicegui_private_local_runner.py"
    runner.write_text(
        "MVP QAIC — GEM Portfolio Image Review\nprompt gem portfolio image review_required\n",
        encoding="utf-8",
    )

    export_dir = project / "05_EXPORTS" / "P182_TEST_EXPORT"
    payload = export_prompt_history_library(project, export_dir=export_dir)

    assert payload["library_ready"] is True
    assert (export_dir / "P182_PROMPT_HISTORY_LIBRARY.json").exists()
    assert (export_dir / "P182_SUMMARY.json").exists()
    assert (export_dir / "P182_PROMPT_HISTORY_LIBRARY.csv").exists()
    assert (export_dir / "P182_PROMPT_HISTORY_LIBRARY_REPORT.md").exists()

    summary = json.loads((export_dir / "P182_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["recommended_next"] == "P183_CAPTURE_TO_SESSION_LINK_AND_PROMPT_RUN_WORKFLOW"
