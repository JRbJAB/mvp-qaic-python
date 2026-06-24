from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_py.p170_nicegui_local_cache_read_binding import REQUIRED_CACHE_SOURCES
from mvp_qaic_py.p175_nicegui_operator_ergonomics_polish import (
    build_operator_ergonomics_model,
    export_operator_ergonomics_model,
)


def _write_cache(project_root: Path) -> None:
    import csv

    cache_dir = project_root / "00_OPERATOR_EXPORTS" / "P168G_LOCAL_CACHE"
    cache_dir.mkdir(parents=True, exist_ok=True)
    for spec in REQUIRED_CACHE_SOURCES:
        with (cache_dir / spec["file_name"]).open("w", encoding="utf-8", newline="") as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(["id", "status", "value"])
            writer.writerow([spec["source_id"], "READY", "sample"])


def test_build_operator_ergonomics_model_ready(tmp_path: Path) -> None:
    _write_cache(tmp_path)

    payload = build_operator_ergonomics_model(
        tmp_path,
        generated_at="2026-06-24T00:00:00+00:00",
    )

    assert payload["STATUS"] == "OK_P175_NICEGUI_OPERATOR_ERGONOMICS_POLISH_READY_REVIEW_ONLY"
    assert payload["tab_count"] == 6
    assert payload["action_count"] == 5
    assert payload["panel_count"] == 5
    assert payload["ergonomics_ready"] is True
    assert payload["blocker_count"] == 0
    assert payload["public_serve"] is False
    assert payload["google_sheets_write"] is False
    assert payload["live_google_api_call_from_python"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False
    assert payload["auto_apply_gem_response"] is False


def test_operator_ergonomics_blocks_dangerous_actions(tmp_path: Path) -> None:
    _write_cache(tmp_path)

    payload = build_operator_ergonomics_model(tmp_path)
    actions = {row["action_id"]: row for row in payload["actions"]}

    assert actions["refresh_google_sheets_live"]["allowed"] is False
    assert actions["apply_prompt_patch"]["allowed"] is False
    assert actions["copy_prompt"]["allowed"] is True
    assert actions["save_gem_response_local_file"]["allowed"] is True


def test_export_operator_ergonomics_model_writes_expected_files(tmp_path: Path) -> None:
    _write_cache(tmp_path)
    export_dir = tmp_path / "05_EXPORTS" / "P175_TEST_EXPORT"

    payload = export_operator_ergonomics_model(tmp_path, export_dir=export_dir)

    assert payload["ergonomics_ready"] is True
    assert (export_dir / "P175_OPERATOR_ERGONOMICS_MODEL.json").exists()
    assert (export_dir / "P175_SUMMARY.json").exists()
    assert (export_dir / "P175_UI_TABS.csv").exists()
    assert (export_dir / "P175_UI_ACTIONS.csv").exists()
    assert (export_dir / "P175_OPERATOR_ERGONOMICS_REPORT.md").exists()

    summary = json.loads((export_dir / "P175_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["recommended_next"] == "P176_NICEGUI_REVIEW_ONLY_ACTIONS_AND_PROMPT_WORKFLOW"
