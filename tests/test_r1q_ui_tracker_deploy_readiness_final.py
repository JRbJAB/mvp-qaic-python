from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_reflex_ui.common.tracker_deploy_readiness import deploy_readiness_status

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_r1q_deploy_readiness_status_is_private_ready_public_blocked() -> None:
    payload = deploy_readiness_status(REPO_ROOT)
    assert payload["ready"] is True
    assert payload["required_files_ok"] is True
    assert payload["approved_oracle"]["ok"] is True
    assert payload["route_binding_ready"] is True
    assert payload["private_reflex_route_deploy_allowed"] is True
    assert payload["public_reflex_deploy_allowed"] is False
    assert (
        payload["public_reflex_deploy_status"]
        == "BLOCKED_UNTIL_REAL_REFLEX_BROWSER_RUNTIME_VISUAL_MATCH"
    )
    assert payload["status"] == "MVP_R1Q_UI_TRACKER_DEPLOY_READINESS_FINAL_READY"


def test_r1q_deploy_readiness_cli_writes_json(tmp_path: Path) -> None:
    out = tmp_path / "ui_tracker_deploy_readiness.json"
    result = subprocess.run(
        [
            sys.executable,
            "tools/ui_tracker_deploy_readiness_gate.py",
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
    assert "STATUS=MVP_R1Q_UI_TRACKER_DEPLOY_READINESS_FINAL_READY" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["ready"] is True
    assert payload["private_reflex_route_deploy_allowed"] is True
    assert payload["public_reflex_deploy_allowed"] is False
