from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p152a_prompt_source_binding_for_real_gem import (
    ACTIVE_PROMPT_SOURCE_ID,
    STATUS_READY,
    BindingRequest,
    build_binding,
    run_binding,
)


def _p152():
    return {
        "status": "P152_STOP_WAIT_REAL_GEM_RESPONSE_FILE_READY",
        "google_sheets_write": False,
        "public_deploy": False,
        "auto_apply_gem_response": False,
    }


def _p144():
    return {
        "status": "P144_PROMPT_COCKPIT_WORKFLOWS_RENDERED_LOCAL_READONLY",
        "steps": [
            {
                "workflow_type": "prompt_library",
                "title": "📘 PROMPT_LIBRARY",
                "operator_goal": "Choisir prompt",
            },
            {
                "workflow_type": "variant_control",
                "title": "🎛️ VARIANT",
                "operator_goal": "Choisir variante",
            },
        ],
    }


def test_build_binding_active_source_ready():
    binding = build_binding(_p152(), _p144(), ACTIVE_PROMPT_SOURCE_ID)
    assert binding["status"] == STATUS_READY
    assert binding["selected_prompt_source"]["allowed_for_p152"] is True
    assert binding["historical_reference_count"] == 2
    assert binding["blocker_count"] == 0
    assert binding["safety"]["google_sheets_write"] is False


def test_build_binding_blocks_historical_source():
    binding = build_binding(_p152(), _p144(), "HIST_SHEETS_001_PROMPT_LIBRARY")
    assert binding["status"] == "P152A_PROMPT_SOURCE_BINDING_BLOCKED"
    assert binding["blocker_count"] == 1


def test_run_binding_writes_outputs(tmp_path: Path):
    p152 = tmp_path / "p152.json"
    p144 = tmp_path / "p144.json"
    p152.write_text(json.dumps(_p152()), encoding="utf-8")
    p144.write_text(json.dumps(_p144()), encoding="utf-8")
    out = tmp_path / "out"
    binding = run_binding(
        BindingRequest(
            p152_summary_path=p152,
            p144_model_path=p144,
            output_dir=out,
            prompt_source_id=ACTIVE_PROMPT_SOURCE_ID,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
        )
    )
    assert binding["status"] == STATUS_READY
    assert (out / "P152A_PROMPT_SOURCE_BINDING.json").exists()
    assert (out / "P152A_PROMPT_SOURCE_OPTIONS.csv").exists()
    assert (out / "P152A_SUMMARY.json").exists()


def test_cli(tmp_path: Path):
    p152 = tmp_path / "p152.json"
    p144 = tmp_path / "p144.json"
    p152.write_text(json.dumps(_p152()), encoding="utf-8")
    p144.write_text(json.dumps(_p144()), encoding="utf-8")
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p152a_prompt_source_binding_for_real_gem",
            "--p152-summary",
            str(p152),
            "--p144-model",
            str(p144),
            "--output-dir",
            str(out),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_READY in completed.stdout
    assert f"prompt_source_id={ACTIVE_PROMPT_SOURCE_ID}" in completed.stdout
