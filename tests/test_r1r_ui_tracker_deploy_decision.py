from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_reflex_ui.common.tracker_deploy_decision import deploy_decision_status

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_r1r_deploy_decision_status() -> None:
    payload = deploy_decision_status(REPO_ROOT)
    assert payload["ready"] is True
    assert payload["status"] == "MVP_R1R_UI_TRACKER_DEPLOY_DECISION_READY"
    assert payload["private_reflex_route_deploy_allowed"] is True
    assert payload["public_reflex_deploy_allowed"] is False
    assert payload["required_files_ok"] is True
    assert payload["missing_required_files"] == []
    assert (
        payload["decision"]["private_reflex_route_deploy"] == "APPROVE_PRIVATE_REFLEX_ROUTE_DEPLOY"
    )
    assert payload["decision"]["public_reflex_deploy"] == "BLOCK_PUBLIC_REFLEX_DEPLOY"


def test_r1r_deploy_decision_cli(tmp_path: Path) -> None:
    out = tmp_path / "ui_tracker_deploy_decision_gate.json"
    result = subprocess.run(
        [
            sys.executable,
            "tools/ui_tracker_deploy_decision_gate.py",
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
    assert "STATUS=MVP_R1R_UI_TRACKER_DEPLOY_DECISION_READY" in result.stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["ready"] is True
    assert payload["private_reflex_route_deploy_allowed"] is True
    assert payload["public_reflex_deploy_allowed"] is False
