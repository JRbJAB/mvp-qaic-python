from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p152_real_gem_response_import_or_stop import (
    STATUS_IMPORTED,
    STATUS_STOP,
    RealImportRequest,
    run_import_or_stop,
    validate_real_payload,
)


def _p151():
    return {
        "status": "P151_RELEASE_PACK_VERIFY_LAUNCH_SMOKE_READY",
        "launch_smoke_ready": True,
        "google_sheets_write": False,
        "public_deploy": False,
        "server_launch_executed": False,
    }


def _real_payload():
    return {
        "status": "REVIEW_REQUIRED",
        "human_review_required": True,
        "no_order_no_sizing": True,
        "NO_AUTO_APPLY": True,
        "source_type": "text",
    }


def test_stop_without_real_file(tmp_path: Path):
    p151 = tmp_path / "p151.json"
    p151.write_text(json.dumps(_p151()), encoding="utf-8")
    out = tmp_path / "out"
    report = run_import_or_stop(
        RealImportRequest(
            p151_summary_path=p151,
            gem_response_file=None,
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
        )
    )
    assert report["status"] == STATUS_STOP
    assert report["real_gem_file_provided"] is False
    assert (out / "P152_SUMMARY.json").exists()


def test_import_real_file(tmp_path: Path):
    p151 = tmp_path / "p151.json"
    gem = tmp_path / "gem.json"
    p151.write_text(json.dumps(_p151()), encoding="utf-8")
    gem.write_text(json.dumps(_real_payload()), encoding="utf-8")
    out = tmp_path / "out"
    report = run_import_or_stop(
        RealImportRequest(
            p151_summary_path=p151,
            gem_response_file=gem,
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
        )
    )
    assert report["status"] == STATUS_IMPORTED
    assert report["validation_status"] == "VALIDATED_FOR_HUMAN_REVIEW"
    assert report["blocker_count"] == 0


def test_validate_payload_blocks_missing_safety():
    validation = validate_real_payload({"status": "OK"}, "{}")
    assert validation["status"] == "BLOCKED"
    assert "HUMAN_REVIEW_REQUIRED_NOT_TRUE" in validation["blockers"]


def test_cli_stop(tmp_path: Path):
    p151 = tmp_path / "p151.json"
    p151.write_text(json.dumps(_p151()), encoding="utf-8")
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p152_real_gem_response_import_or_stop",
            "--p151-summary",
            str(p151),
            "--output-dir",
            str(out),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_STOP in completed.stdout
    assert "google_sheets_write=false" in completed.stdout
