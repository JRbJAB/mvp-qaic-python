from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p140_nicegui_cockpit_replica_renderer import (
    STATUS_RENDERED,
    RenderRequest,
    build_component_model,
    render_static_preview_html,
    run_render,
    slugify,
)


def _p139_payload():
    return {
        "status": "P139_METADATA_CAPTURED",
        "spreadsheet_title": "DEV",
        "sheet_count": 132,
        "sheets": [
            {
                "title": "📘 PROMPT_LIBRARY",
                "index": 0,
                "is_cockpit_source_tab": True,
                "nicegui_route": "/cockpit/library_prompt_library",
                "suggested_component": "DataGridCard",
                "replica_priority": "P0",
                "row_count": 200,
                "column_count": 12,
                "frozen_row_count": 1,
                "frozen_column_count": 2,
                "detected_columns": ["prompt_id", "raw_prompt_text", "status"],
                "header_rows_preview": [["prompt_id", "raw_prompt_text", "status"]],
            },
            {"title": "OTHER", "index": 1, "is_cockpit_source_tab": False},
        ],
    }


def test_slugify_handles_emoji():
    assert slugify("📘 PROMPT_LIBRARY") == "library_prompt_library"


def test_build_component_model_keeps_only_cockpit_pages_and_safety():
    model = build_component_model(_p139_payload())
    assert model["status"] == STATUS_RENDERED
    assert model["cockpit_page_count"] == 1
    assert model["pages"][0]["title"] == "📘 PROMPT_LIBRARY"
    assert model["pages"][0]["frozen_column_count"] == 2
    assert model["safety"]["google_sheets_write"] is False


def test_static_preview_contains_route_and_columns():
    model = build_component_model(_p139_payload())
    preview = render_static_preview_html(model)
    assert "/cockpit/library_prompt_library" in preview
    assert "prompt_id" in preview
    assert "No live write" in preview


def test_run_render_writes_outputs(tmp_path: Path):
    payload_path = tmp_path / "p139.json"
    output_dir = tmp_path / "out"
    payload_path.write_text(json.dumps(_p139_payload()), encoding="utf-8")
    model = run_render(
        RenderRequest(
            p139_payload_path=payload_path,
            output_dir=output_dir,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
        )
    )
    assert model["status"] == STATUS_RENDERED
    assert (output_dir / "P140_STATIC_PREVIEW.html").exists()
    assert (output_dir / "P140_NICEGUI_REPLICA_APP.py").exists()
    assert (output_dir / "P140_SUMMARY.json").exists()


def test_cli(tmp_path: Path):
    payload_path = tmp_path / "p139.json"
    output_dir = tmp_path / "out"
    payload_path.write_text(json.dumps(_p139_payload()), encoding="utf-8")
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p140_nicegui_cockpit_replica_renderer",
            "--p139-payload",
            str(payload_path),
            "--output-dir",
            str(output_dir),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_RENDERED in completed.stdout
    assert "google_sheets_write=false" in completed.stdout
