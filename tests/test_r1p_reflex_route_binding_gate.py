from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_reflex_ui.common.tracker_route_binding import (
    ROUTE_BINDING_STATUS_READY,
    route_binding_status,
    route_bindings,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_r1p_route_bindings_are_exact() -> None:
    routes = [binding.route for binding in route_bindings()]
    assert routes == ["/dev-tracking", "/cdc-dev-tracker", "/cdc-tracker"]

    surfaces = {binding.surface for binding in route_bindings()}
    assert {"Dev Tracker", "CDC Dev Tracker", "CDC Tracker"} <= surfaces


def test_r1p_route_binding_status_ready() -> None:
    payload = route_binding_status(REPO_ROOT)

    assert payload["ready"] is True
    assert payload["status"] == ROUTE_BINDING_STATUS_READY
    assert payload["approved_oracle_exists"] is True
    assert payload["routes_bound"] is True
    assert payload["required_files_ok"] is True
    assert payload["reflex_public_deploy_allowed"] is False


def test_r1p_route_binding_gate_cli_writes_json(tmp_path: Path) -> None:
    out = tmp_path / "ui_tracker_route_binding_gate.json"
    result = subprocess.run(
        [
            sys.executable,
            "tools/ui_tracker_route_binding_gate.py",
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
    assert "STATUS=MVP_R1P_REFLEX_ROUTE_BINDING_READY" in result.stdout

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["ready"] is True
    assert payload["status"] == "MVP_R1P_REFLEX_ROUTE_BINDING_READY"
    assert payload["next_gate"] == "R1Q_DEPLOY_READINESS_FINAL"


def test_r1p_route_binding_keeps_public_deploy_blocked() -> None:
    payload = route_binding_status(REPO_ROOT)

    assert payload["reflex_public_deploy_allowed"] is False
    assert (
        payload["reflex_public_deploy_status"]
        == "BLOCKED_UNTIL_REAL_REFLEX_BROWSER_RUNTIME_VISUAL_MATCH"
    )
