from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p146_correction_queue_ui import (
    STATUS_RENDERED,
    CorrectionRequest,
    build_queue_model,
    run_queue,
)


def _p145():
    return {
        "status": "P145_GEM_RESPONSE_IMPORT_E2E_VALIDATED_LOCAL_REVIEW",
        "validation": {
            "status": "VALIDATED_FOR_HUMAN_REVIEW",
            "blockers": [],
            "warnings": [],
            "human_review_required": True,
            "no_auto_apply": True,
            "no_order_no_sizing": True,
        },
        "response_payload": {"status": "REVIEW_REQUIRED", "NO_AUTO_APPLY": True},
    }


def _p144():
    return {
        "status": "P144_PROMPT_COCKPIT_WORKFLOWS_RENDERED_LOCAL_READONLY",
        "workflow_step_count": 1,
        "steps": [
            {
                "workflow_type": "prompt_library",
                "title": "📘 PROMPT_LIBRARY",
                "operator_goal": "Choisir un prompt.",
            }
        ],
    }


def test_build_queue_model_review_only():
    model = build_queue_model(_p145(), _p144())
    assert model["status"] == STATUS_RENDERED
    assert model["queue_item_count"] >= 1
    assert model["ui_policy"]["apply_button_enabled"] is False
    assert model["safety"]["google_sheets_write"] is False
    assert model["safety"]["broker"] is False


def test_run_queue_writes_outputs(tmp_path: Path):
    p145 = tmp_path / "p145.json"
    p144 = tmp_path / "p144.json"
    p145.write_text(json.dumps(_p145()), encoding="utf-8")
    p144.write_text(json.dumps(_p144()), encoding="utf-8")
    out = tmp_path / "out"
    model = run_queue(
        CorrectionRequest(
            p145_payload_path=p145,
            p144_model_path=p144,
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
        )
    )
    assert model["status"] == STATUS_RENDERED
    assert (out / "P146_CORRECTION_QUEUE_MODEL.json").exists()
    assert (out / "P146_CORRECTION_ACTIONS.csv").exists()
    assert (out / "P146_SUMMARY.json").exists()


def test_cli(tmp_path: Path):
    p145 = tmp_path / "p145.json"
    p144 = tmp_path / "p144.json"
    p145.write_text(json.dumps(_p145()), encoding="utf-8")
    p144.write_text(json.dumps(_p144()), encoding="utf-8")
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p146_correction_queue_ui",
            "--p145-payload",
            str(p145),
            "--p144-model",
            str(p144),
            "--output-dir",
            str(out),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_RENDERED in completed.stdout
    assert "apply_button_enabled=false" in completed.stdout
