from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p148_sync_strategy_readonly import (
    STATUS_RENDERED,
    SyncStrategyRequest,
    build_strategy,
    run_strategy,
)


def _p147():
    return {
        "status": "P147_OPERATOR_POLISH_RENDERED_LOCAL_PRIVATE",
        "review_policy": {
            "apply_to_sheet_enabled": False,
            "auto_apply_gem_response_enabled": False,
        },
    }


def _p143b():
    return {
        "status": "P143B_DATA_PREVIEW_SOURCE_EXPANSION_RENDERED_LOCAL_READONLY",
        "bindings": [
            {
                "page_id": "library",
                "title": "📘 PROMPT_LIBRARY",
                "route": "/library",
                "binding_mode": "csv_match",
                "source_csv": "PROMPT_LIBRARY.csv",
                "source_filename": "PROMPT_LIBRARY.csv",
                "source_rows_total": 10,
                "preview_row_count": 5,
            }
        ],
    }


def test_build_strategy_readonly_policy():
    strategy = build_strategy(_p147(), _p143b())
    assert strategy["status"] == STATUS_RENDERED
    assert strategy["registry_row_count"] == 1
    assert strategy["policy"]["write_back_allowed_now"] is False
    assert strategy["policy"]["future_sheet_write_requires_explicit_go"] is True
    assert strategy["safety"]["google_sheets_write"] is False


def test_run_strategy_writes_outputs(tmp_path: Path):
    p147 = tmp_path / "p147.json"
    p143b = tmp_path / "p143b.json"
    p147.write_text(json.dumps(_p147()), encoding="utf-8")
    p143b.write_text(json.dumps(_p143b()), encoding="utf-8")
    out = tmp_path / "out"
    strategy = run_strategy(
        SyncStrategyRequest(
            p147_model_path=p147,
            p143b_binding_path=p143b,
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
        )
    )
    assert strategy["status"] == STATUS_RENDERED
    assert (out / "P148_SYNC_STRATEGY_READONLY.json").exists()
    assert (out / "P148_SOURCE_REGISTRY.csv").exists()
    assert (out / "P148_SUMMARY.json").exists()


def test_cli(tmp_path: Path):
    p147 = tmp_path / "p147.json"
    p143b = tmp_path / "p143b.json"
    p147.write_text(json.dumps(_p147()), encoding="utf-8")
    p143b.write_text(json.dumps(_p143b()), encoding="utf-8")
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p148_sync_strategy_readonly",
            "--p147-model",
            str(p147),
            "--p143b-binding",
            str(p143b),
            "--output-dir",
            str(out),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_RENDERED in completed.stdout
    assert "future_sheet_write_requires_explicit_go=true" in completed.stdout
