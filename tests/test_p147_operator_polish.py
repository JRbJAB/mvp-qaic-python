from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p147_operator_polish import (
    STATUS_RENDERED,
    PolishRequest,
    build_polish_model,
    run_polish,
)


def _queue():
    return {
        "status": "P146_CORRECTION_QUEUE_UI_RENDERED_LOCAL_REVIEW_ONLY",
        "queue_item_count": 2,
        "ui_policy": {
            "review_only": True,
            "apply_button_enabled": False,
            "sheet_write_enabled": False,
            "auto_apply_enabled": False,
        },
    }


def _workflow():
    return {
        "status": "P144_PROMPT_COCKPIT_WORKFLOWS_RENDERED_LOCAL_READONLY",
        "workflow_step_count": 2,
        "steps": [
            {"workflow_type": "prompt_library", "title": "📘 PROMPT_LIBRARY", "priority": "P0"},
            {"workflow_type": "variant_control", "title": "🎛️ VARIANT", "priority": "P1"},
        ],
    }


def test_build_polish_model_safety():
    model = build_polish_model(_queue(), _workflow())
    assert model["status"] == STATUS_RENDERED
    assert model["review_policy"]["apply_to_sheet_enabled"] is False
    assert model["review_policy"]["broker_actions_enabled"] is False
    assert model["safety"]["local_private_only"] is True
    assert len(model["shortcuts"]) >= 3


def test_run_polish_writes_outputs(tmp_path: Path):
    q = tmp_path / "queue.json"
    w = tmp_path / "workflow.json"
    q.write_text(json.dumps(_queue()), encoding="utf-8")
    w.write_text(json.dumps(_workflow()), encoding="utf-8")
    out = tmp_path / "out"
    model = run_polish(
        PolishRequest(
            p146_queue_path=q,
            p144_model_path=w,
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
        )
    )
    assert model["status"] == STATUS_RENDERED
    assert (out / "P147_OPERATOR_POLISH_MODEL.json").exists()
    assert (out / "P147_OPERATOR_SHORTCUTS.csv").exists()
    assert (out / "P147_SUMMARY.json").exists()


def test_cli(tmp_path: Path):
    q = tmp_path / "queue.json"
    w = tmp_path / "workflow.json"
    q.write_text(json.dumps(_queue()), encoding="utf-8")
    w.write_text(json.dumps(_workflow()), encoding="utf-8")
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p147_operator_polish",
            "--p146-queue",
            str(q),
            "--p144-model",
            str(w),
            "--output-dir",
            str(out),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_RENDERED in completed.stdout
    assert "apply_to_sheet_enabled=false" in completed.stdout
