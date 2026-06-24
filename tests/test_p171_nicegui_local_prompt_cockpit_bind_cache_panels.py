from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p170_nicegui_local_cache_read_binding import REQUIRED_CACHE_SOURCES
from mvp_qaic_py.p171_nicegui_local_prompt_cockpit_bind_cache_panels import (
    build_cockpit_panel_model,
    export_cockpit_panel_model,
)


def _write_cache(project_root: Path) -> None:
    cache_dir = project_root / "00_OPERATOR_EXPORTS" / "P168G_LOCAL_CACHE"
    cache_dir.mkdir(parents=True, exist_ok=True)
    for spec in REQUIRED_CACHE_SOURCES:
        with (cache_dir / spec["file_name"]).open("w", encoding="utf-8", newline="") as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(["id", "status", "value"])
            writer.writerow([spec["source_id"], "READY", "sample"])


def test_build_cockpit_panel_model_ready(tmp_path: Path) -> None:
    _write_cache(tmp_path)

    payload = build_cockpit_panel_model(
        tmp_path,
        generated_at="2026-06-24T00:00:00+00:00",
    )

    assert payload["STATUS"] == "OK_P171_NICEGUI_LOCAL_PROMPT_COCKPIT_PANELS_READY_REVIEW_ONLY"
    assert payload["panel_count"] == 5
    assert payload["ready_panel_count"] == 5
    assert payload["cockpit_ready"] is True
    assert payload["blocker_count"] == 0
    assert payload["recommended_launch_host"] == "127.0.0.1"
    assert payload["recommended_launch_port"] == 8088
    assert payload["public_serve"] is False
    assert payload["google_sheets_write"] is False
    assert payload["live_google_api_call_from_python"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_build_cockpit_panel_model_blocks_missing_cache(tmp_path: Path) -> None:
    _write_cache(tmp_path)
    missing = tmp_path / "00_OPERATOR_EXPORTS" / "P168G_LOCAL_CACHE" / "MVP_QAIC_CONFIG.csv"
    missing.unlink()

    payload = build_cockpit_panel_model(tmp_path)

    assert payload["STATUS"] == "BLOCKED_P171_NICEGUI_LOCAL_PROMPT_COCKPIT_PANELS"
    assert payload["cockpit_ready"] is False
    assert payload["blocker_count"] == 1
    assert payload["blockers"] == ["MISSING_CACHE_FILE:MVP_QAIC_CONFIG.csv"]
    assert payload["ready_panel_count"] == 4


def test_export_cockpit_panel_model_writes_expected_files(tmp_path: Path) -> None:
    _write_cache(tmp_path)
    export_dir = tmp_path / "05_EXPORTS" / "P171_TEST_EXPORT"

    payload = export_cockpit_panel_model(tmp_path, export_dir=export_dir)

    assert payload["cockpit_ready"] is True
    assert (export_dir / "P171_COCKPIT_PANEL_MODEL.json").exists()
    assert (export_dir / "P171_SUMMARY.json").exists()
    assert (export_dir / "P171_NICEGUI_PANEL_MODEL.csv").exists()
    assert (export_dir / "P171_COCKPIT_PANEL_MODEL_REPORT.md").exists()

    summary = json.loads((export_dir / "P171_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["ready_panel_count"] == 5
    assert summary["recommended_next"] == "P172_NICEGUI_PRIVATE_COCKPIT_RENDER_LOCAL_CACHE_PANELS"
