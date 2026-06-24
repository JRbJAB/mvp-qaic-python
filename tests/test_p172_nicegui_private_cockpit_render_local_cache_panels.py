from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p170_nicegui_local_cache_read_binding import REQUIRED_CACHE_SOURCES
from mvp_qaic_py.p172_nicegui_private_cockpit_render_local_cache_panels import (
    build_private_cockpit_render_model,
    export_private_cockpit_render,
    render_static_private_cockpit_html,
)


def _write_cache(project_root: Path) -> None:
    cache_dir = project_root / "00_OPERATOR_EXPORTS" / "P168G_LOCAL_CACHE"
    cache_dir.mkdir(parents=True, exist_ok=True)
    for spec in REQUIRED_CACHE_SOURCES:
        with (cache_dir / spec["file_name"]).open("w", encoding="utf-8", newline="") as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(["id", "status", "value"])
            writer.writerow([spec["source_id"], "READY", "sample"])


def test_build_private_cockpit_render_model_ready(tmp_path: Path) -> None:
    _write_cache(tmp_path)

    payload = build_private_cockpit_render_model(
        tmp_path,
        generated_at="2026-06-24T00:00:00+00:00",
    )

    assert payload["STATUS"] == "OK_P172_NICEGUI_PRIVATE_COCKPIT_RENDER_READY_REVIEW_ONLY"
    assert payload["render_panel_count"] == 5
    assert payload["ready_render_panel_count"] == 5
    assert payload["render_ready"] is True
    assert payload["blocker_count"] == 0
    assert payload["host"] == "127.0.0.1"
    assert payload["port"] == 8088
    assert payload["public_serve"] is False
    assert payload["google_sheets_write"] is False
    assert payload["live_google_api_call_from_python"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_render_static_private_cockpit_html_contains_private_panels(tmp_path: Path) -> None:
    _write_cache(tmp_path)
    payload = build_private_cockpit_render_model(tmp_path)

    html = render_static_private_cockpit_html(payload)

    assert "MVP QAIC — Private Local Cockpit Preview" in html
    assert "127.0.0.1" in html
    assert "Public serve: False" in html
    assert "Config cockpit" in html
    assert "Prompt source registry" in html
    assert "Decision journal" in html
    assert "Prompt review workbench" in html
    assert "Lexique or cockpit data" in html


def test_export_private_cockpit_render_writes_expected_files(tmp_path: Path) -> None:
    _write_cache(tmp_path)
    export_dir = tmp_path / "05_EXPORTS" / "P172_TEST_EXPORT"

    payload = export_private_cockpit_render(tmp_path, export_dir=export_dir)

    assert payload["render_ready"] is True
    assert (export_dir / "P172_PRIVATE_COCKPIT_RENDER_MODEL.json").exists()
    assert (export_dir / "P172_SUMMARY.json").exists()
    assert (export_dir / "P172_PRIVATE_COCKPIT_RENDER_PANELS.csv").exists()
    assert (export_dir / "P172_PRIVATE_COCKPIT_PREVIEW.html").exists()
    assert (export_dir / "P172_PRIVATE_COCKPIT_RENDER_REPORT.md").exists()

    summary = json.loads((export_dir / "P172_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["ready_render_panel_count"] == 5
    assert summary["recommended_next"] == "P173_NICEGUI_PRIVATE_LOCAL_RUNNER_AND_SMOKE"
