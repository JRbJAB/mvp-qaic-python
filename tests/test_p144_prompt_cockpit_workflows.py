from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p144_prompt_cockpit_workflows import (
    STATUS_RENDERED,
    WorkflowRequest,
    build_workflow_model,
    classify_workflow,
    run_workflows,
)


def _binding():
    return {
        "status": "P143B_DATA_PREVIEW_SOURCE_EXPANSION_RENDERED_LOCAL_READONLY",
        "source_csv_count": 2,
        "cockpit_page_count": 3,
        "bindings": [
            {
                "title": "📘 PROMPT_LIBRARY",
                "route": "/library",
                "binding_mode": "csv_match",
                "preview_row_count": 2,
                "source_filename": "PROMPT_LIBRARY.csv",
            },
            {
                "title": "🎛️ PROMPT_VARIANT_CONTROL_CENTER",
                "route": "/variant",
                "binding_mode": "csv_match",
                "preview_row_count": 2,
                "source_filename": "VARIANT.csv",
            },
            {
                "title": "🧠 PROMPT_CONTEXT_PACKS",
                "route": "/context",
                "binding_mode": "csv_match",
                "preview_row_count": 2,
                "source_filename": "CONTEXT.csv",
            },
        ],
    }


def test_classify_workflow():
    assert classify_workflow({"title": "📘 PROMPT_LIBRARY"}) == "prompt_library"
    assert classify_workflow({"title": "🎛️ PROMPT_VARIANT_CONTROL_CENTER"}) == "variant_control"


def test_build_workflow_model_safety_and_gate():
    model = build_workflow_model(_binding())
    assert model["status"] == STATUS_RENDERED
    assert model["workflow_step_count"] == 3
    assert model["gates"]["p145_gem_response_import_ready"] is True
    assert model["gates"]["allows_auto_apply"] is False
    assert model["safety"]["broker"] is False


def test_run_workflows_writes_outputs(tmp_path: Path):
    path = tmp_path / "binding.json"
    path.write_text(json.dumps(_binding()), encoding="utf-8")
    out = tmp_path / "out"
    model = run_workflows(
        WorkflowRequest(
            p143b_binding_path=path,
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
        )
    )
    assert model["status"] == STATUS_RENDERED
    assert (out / "P144_PROMPT_WORKFLOW_MODEL.json").exists()
    assert (out / "P144_OPERATOR_ACTIONS.csv").exists()
    assert (out / "P144_SUMMARY.json").exists()


def test_cli(tmp_path: Path):
    path = tmp_path / "binding.json"
    path.write_text(json.dumps(_binding()), encoding="utf-8")
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p144_prompt_cockpit_workflows",
            "--p143b-binding",
            str(path),
            "--output-dir",
            str(out),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_RENDERED in completed.stdout
    assert "p145_gem_response_import_ready=true" in completed.stdout
