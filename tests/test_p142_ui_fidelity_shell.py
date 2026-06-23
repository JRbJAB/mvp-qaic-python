from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p142_ui_fidelity_shell import (
    STATUS_RENDERED,
    FidelityRequest,
    build_ui_shell_spec,
    classify_page,
    run_fidelity,
)


def _p140():
    return {
        "status": "P140_NICEGUI_COCKPIT_REPLICA_RENDERED_FROM_METADATA",
        "cockpit_page_count": 2,
        "pages": [
            {
                "page_id": "library",
                "title": "📘 PROMPT_LIBRARY",
                "route": "/cockpit/library",
                "priority": "P0",
                "row_count": 10,
                "column_count": 3,
                "frozen_row_count": 1,
                "frozen_column_count": 1,
                "detected_columns": ["prompt_id", "raw_prompt_text", "status"],
            },
            {
                "page_id": "runtime",
                "title": "🤖 AI_RUNTIME_REFERENCE",
                "route": "/cockpit/runtime",
                "detected_columns": [],
            },
        ],
    }


def _p141():
    return {
        "status": "P141_NICEGUI_LOCAL_LAUNCH_SMOKE_PASSED",
        "local_url": "http://127.0.0.1:8088",
        "routes": ["/", "/cockpit/library", "/cockpit/runtime"],
        "smoke_results": [
            {"route": "/cockpit/library", "ok": True, "http_status": 200},
            {"route": "/cockpit/runtime", "ok": True, "http_status": 200},
        ],
    }


def test_classify_page():
    assert classify_page({"title": "📘 PROMPT_LIBRARY"}) == "library"
    assert classify_page({"title": "🤖 AI_RUNTIME_REFERENCE"}) == "contracts"


def test_build_ui_shell_spec_safety_and_pages():
    spec = build_ui_shell_spec(
        _p140(), _p141(), run_id="R", generated_at_utc="2026-06-23T00:00:00Z"
    )
    assert spec["status"] == STATUS_RENDERED
    assert spec["cockpit_page_count"] == 2
    assert spec["pages"][0]["domain"] == "library"
    assert spec["pages"][0]["smoke_ok"] is True
    assert spec["safety"]["google_sheets_write"] is False
    assert spec["migration_gates"]["p143_data_preview_binding_ready"] is True


def test_run_fidelity_writes_outputs(tmp_path: Path):
    p140 = tmp_path / "p140.json"
    p141 = tmp_path / "p141.json"
    out = tmp_path / "out"
    p140.write_text(json.dumps(_p140()), encoding="utf-8")
    p141.write_text(json.dumps(_p141()), encoding="utf-8")

    spec = run_fidelity(
        FidelityRequest(
            p140_model_path=p140,
            p141_plan_path=p141,
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
        )
    )
    assert spec["status"] == STATUS_RENDERED
    assert (out / "P142_NICEGUI_SHELL_APP.py").exists()
    assert (out / "P142_SUMMARY.json").exists()


def test_cli(tmp_path: Path):
    p140 = tmp_path / "p140.json"
    p141 = tmp_path / "p141.json"
    out = tmp_path / "out"
    p140.write_text(json.dumps(_p140()), encoding="utf-8")
    p141.write_text(json.dumps(_p141()), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p142_ui_fidelity_shell",
            "--p140-model",
            str(p140),
            "--p141-plan",
            str(p141),
            "--output-dir",
            str(out),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_RENDERED in completed.stdout
    assert "google_sheets_write=false" in completed.stdout
