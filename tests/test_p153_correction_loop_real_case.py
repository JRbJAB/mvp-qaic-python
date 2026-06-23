from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p153_correction_loop_real_case import (
    STATUS_READY,
    CorrectionLoopRequest,
    build_report,
    run_correction_loop,
)


def _p152():
    return {
        "status": "P152_REAL_GEM_RESPONSE_IMPORTED_LOCAL_REVIEW",
        "mode": "REAL_GEM_RESPONSE_FILE_IMPORT",
        "validation_status": "VALIDATED_FOR_HUMAN_REVIEW",
        "blocker_count": 0,
        "warnings": [],
        "blockers": [],
        "safety": {
            "google_sheets_write": False,
            "public_deploy": False,
            "auto_apply_gem_response": False,
        },
        "response_payload": {
            "status": "REVIEW_REQUIRED",
            "reference_currency": "USD",
            "image_used": True,
            "human_review_required": True,
            "no_order_no_sizing": True,
            "NO_AUTO_APPLY": True,
        },
    }


def _p152a():
    return {
        "status": "P152A_PROMPT_SOURCE_BINDING_READY_FOR_REAL_GEM",
        "prompt_source_id": "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW",
        "selected_prompt_source": {"status": "ACTIVE_FOR_P152_REAL_GEM"},
        "safety": {"google_sheets_write": False},
    }


def test_build_report_ready():
    report = build_report(_p152(), _p152a())
    assert report["status"] == STATUS_READY
    assert report["blocker_count"] == 0
    assert report["apply_allowed"] is False
    assert report["action_count"] >= 2
    assert report["safety"]["google_sheets_write"] is False


def test_run_correction_loop_writes_outputs(tmp_path: Path):
    p152 = tmp_path / "p152.json"
    p152a = tmp_path / "p152a.json"
    p152.write_text(json.dumps(_p152()), encoding="utf-8")
    p152a.write_text(json.dumps(_p152a()), encoding="utf-8")
    out = tmp_path / "out"
    report = run_correction_loop(
        CorrectionLoopRequest(
            p152_report_path=p152,
            p152a_binding_path=p152a,
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
        )
    )
    assert report["status"] == STATUS_READY
    assert (out / "P153_CORRECTION_ACTIONS.csv").exists()
    assert (out / "P153_SUMMARY.json").exists()


def test_cli(tmp_path: Path):
    p152 = tmp_path / "p152.json"
    p152a = tmp_path / "p152a.json"
    p152.write_text(json.dumps(_p152()), encoding="utf-8")
    p152a.write_text(json.dumps(_p152a()), encoding="utf-8")
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p153_correction_loop_real_case",
            "--p152-report",
            str(p152),
            "--p152a-binding",
            str(p152a),
            "--output-dir",
            str(out),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_READY in completed.stdout
    assert "apply_allowed=false" in completed.stdout
