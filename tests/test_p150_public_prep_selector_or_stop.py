from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p150_public_prep_selector_or_stop import (
    STATUS_READY,
    SelectorRequest,
    build_selector,
    run_selector,
)


def _p149():
    return {
        "status": "P149_MIGRATION_CLOSE_GATE_READY_LOCAL_PRIVATE",
        "migration_close_ready": True,
        "mvp_prompt_cockpit_local_private_ready": True,
        "evidence_ok_count": 9,
        "required_export_count": 9,
        "blocker_count": 0,
        "safety": {"google_sheets_write": False, "public_deploy": False},
    }


def test_build_selector_recommends_release_pack():
    selector = build_selector(_p149())
    assert selector["status"] == STATUS_READY
    assert selector["recommended_next"] == "P150B_LOCAL_PRIVATE_RELEASE_PACK"
    assert selector["blocker_count"] == 0
    assert selector["safety"]["google_sheets_write"] is False
    assert selector["safety"]["public_deploy"] is False


def test_run_selector_writes_outputs(tmp_path: Path):
    p149 = tmp_path / "p149.json"
    p149.write_text(json.dumps(_p149()), encoding="utf-8")
    out = tmp_path / "out"
    selector = run_selector(
        SelectorRequest(
            p149_report_path=p149,
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
        )
    )
    assert selector["status"] == STATUS_READY
    assert (out / "P150_PUBLIC_PREP_SELECTOR.json").exists()
    assert (out / "P150_NEXT_OPTIONS.csv").exists()
    assert (out / "P150_SUMMARY.json").exists()


def test_cli(tmp_path: Path):
    p149 = tmp_path / "p149.json"
    p149.write_text(json.dumps(_p149()), encoding="utf-8")
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p150_public_prep_selector_or_stop",
            "--p149-report",
            str(p149),
            "--output-dir",
            str(out),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_READY in completed.stdout
    assert "recommended_next=P150B_LOCAL_PRIVATE_RELEASE_PACK" in completed.stdout
