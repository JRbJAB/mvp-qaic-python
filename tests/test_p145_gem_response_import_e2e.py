from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p145_gem_response_import_e2e import (
    STATUS_IMPORTED,
    ImportRequest,
    build_fixture_response,
    build_import_payload,
    run_import,
    validate_response,
)


def _p144():
    return {
        "status": "P144_PROMPT_COCKPIT_WORKFLOWS_RENDERED_LOCAL_READONLY",
        "workflow_step_count": 11,
    }


def test_validate_fixture_response():
    validation = validate_response(build_fixture_response())
    assert validation["status"] == "VALIDATED_FOR_HUMAN_REVIEW"
    assert validation["human_review_required"] is True
    assert validation["no_order_no_sizing"] is True


def test_build_import_payload_safety():
    payload = build_import_payload(
        _p144(), build_fixture_response(), "{}", source_path="fixture", fixture_used=True
    )
    assert payload["status"] == STATUS_IMPORTED
    assert payload["review_queue_item"]["status"] == "REVIEW_REQUIRED"
    assert "ORDER" in payload["review_queue_item"]["blocked_actions"]
    assert payload["safety"]["broker"] is False


def test_run_import_fixture_writes_outputs(tmp_path: Path):
    p144 = tmp_path / "p144.json"
    p144.write_text(json.dumps(_p144()), encoding="utf-8")
    out = tmp_path / "out"
    payload = run_import(
        ImportRequest(
            p144_model_path=p144,
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
            gem_response_file=None,
            use_fixture=True,
        )
    )
    assert payload["status"] == STATUS_IMPORTED
    assert (out / "P145_GEM_RESPONSE_IMPORT_PAYLOAD.json").exists()
    assert (out / "P145_SUMMARY.json").exists()


def test_cli_fixture(tmp_path: Path):
    p144 = tmp_path / "p144.json"
    p144.write_text(json.dumps(_p144()), encoding="utf-8")
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p145_gem_response_import_e2e",
            "--p144-model",
            str(p144),
            "--output-dir",
            str(out),
            "--use-fixture",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_IMPORTED in completed.stdout
    assert "auto_apply_gem_response=false" in completed.stdout
