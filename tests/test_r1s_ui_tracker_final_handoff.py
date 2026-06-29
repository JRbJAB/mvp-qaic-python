from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_reflex_ui.common.tracker_final_handoff import final_handoff_status

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_r1s_final_handoff_status_ready() -> None:
    payload = final_handoff_status(REPO_ROOT)
    assert payload["ready"] is True
    assert payload["status"] == "MVP_R1S_UI_TRACKER_FINAL_HANDOFF_READY"
    assert payload["private_reflex_route_deploy_allowed"] is True
    assert payload["public_reflex_deploy_allowed"] is False
    assert (
        payload["public_reflex_deploy_status"]
        == "BLOCKED_UNTIL_REAL_REFLEX_BROWSER_RUNTIME_VISUAL_MATCH"
    )
    assert "/dev-tracking" in payload["routes"]
    assert "/cdc-dev-tracker" in payload["routes"]
    assert "/cdc-tracker" in payload["routes"]


def test_r1s_final_handoff_cli_writes_json(tmp_path: Path) -> None:
    out = tmp_path / "ui_tracker_final_handoff.json"
    result = subprocess.run(
        [
            sys.executable,
            "tools/ui_tracker_final_handoff_gate.py",
            "--out",
            str(out),
            "--repo",
            str(REPO_ROOT),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    assert "STATUS=MVP_R1S_UI_TRACKER_FINAL_HANDOFF_READY" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["ready"] is True
    assert payload["private_reflex_route_deploy_allowed"] is True
    assert payload["public_reflex_deploy_allowed"] is False
