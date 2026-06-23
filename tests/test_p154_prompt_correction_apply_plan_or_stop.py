from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p154_prompt_correction_apply_plan_or_stop import (
    STATUS_READY,
    ApplyPlanRequest,
    build_report,
    run_apply_plan,
)


def _p153():
    return {
        "status": "P153_CORRECTION_LOOP_REAL_CASE_READY_REVIEW_ONLY",
        "prompt_source_id": "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW",
        "source_p152_status": "P152_REAL_GEM_RESPONSE_IMPORTED_LOCAL_REVIEW",
        "source_p152_validation_status": "VALIDATED_FOR_HUMAN_REVIEW",
        "blocker_count": 0,
        "apply_allowed": False,
        "safety": {
            "google_sheets_write": False,
            "public_deploy": False,
            "auto_apply_gem_response": False,
        },
        "actions": [
            {
                "action_id": "A1",
                "action_type": "FINAL_HUMAN_REVIEW",
                "priority": "P0",
                "source": "P152",
                "description": "Review",
                "recommended_change": "Review manually",
            },
            {
                "action_id": "A2",
                "action_type": "PROMPT_IMPROVEMENT_PROPOSAL",
                "priority": "P1",
                "source": "P132",
                "description": "Improve",
                "recommended_change": "Improve prompt",
            },
        ],
    }


def test_build_report_ready():
    report = build_report(_p153())
    assert report["status"] == STATUS_READY
    assert report["apply_allowed"] is False
    assert report["apply_now_yes_count"] == 0
    assert report["plan_row_count"] == 2
    assert report["safety"]["google_sheets_write"] is False


def test_run_apply_plan_writes_outputs(tmp_path: Path):
    p153 = tmp_path / "p153.json"
    p153.write_text(json.dumps(_p153()), encoding="utf-8")
    out = tmp_path / "out"
    report = run_apply_plan(
        ApplyPlanRequest(
            p153_report_path=p153,
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
        )
    )
    assert report["status"] == STATUS_READY
    assert (out / "P154_PROMPT_CORRECTION_APPLY_PLAN.csv").exists()
    assert (out / "P154_SUMMARY.json").exists()


def test_cli(tmp_path: Path):
    p153 = tmp_path / "p153.json"
    p153.write_text(json.dumps(_p153()), encoding="utf-8")
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p154_prompt_correction_apply_plan_or_stop",
            "--p153-report",
            str(p153),
            "--output-dir",
            str(out),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_READY in completed.stdout
    assert "apply_allowed=false" in completed.stdout
