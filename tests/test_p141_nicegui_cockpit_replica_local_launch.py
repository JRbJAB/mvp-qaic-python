from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mvp_qaic_py.p141_nicegui_cockpit_replica_local_launch import (
    STATUS_READY,
    LaunchRequest,
    build_launch_plan,
    routes_from_model,
    run_launch,
    validate_p140_export,
)


def _model():
    return {
        "status": "P140_NICEGUI_COCKPIT_REPLICA_RENDERED_FROM_METADATA",
        "cockpit_page_count": 2,
        "pages": [
            {"title": "A", "route": "/cockpit/a"},
            {"title": "B", "route": "/cockpit/b"},
        ],
    }


def _export_dir(tmp_path: Path) -> Path:
    root = tmp_path / "p140"
    root.mkdir()
    (root / "P140_NICEGUI_COMPONENT_MODEL.json").write_text(json.dumps(_model()), encoding="utf-8")
    (root / "P140_NICEGUI_REPLICA_APP.py").write_text("print('ok')\\n", encoding="utf-8")
    (root / "P140_SUMMARY.json").write_text(json.dumps({"status": "ok"}), encoding="utf-8")
    return root


def test_routes_from_model_includes_root():
    assert routes_from_model(_model()) == ["/", "/cockpit/a", "/cockpit/b"]


def test_validate_p140_export(tmp_path: Path):
    model_path, app_path, model = validate_p140_export(_export_dir(tmp_path))
    assert model_path.name == "P140_NICEGUI_COMPONENT_MODEL.json"
    assert app_path.name == "P140_NICEGUI_REPLICA_APP.py"
    assert model["cockpit_page_count"] == 2


def test_build_launch_plan_safety(tmp_path: Path):
    root = _export_dir(tmp_path)
    _, app_path, model = validate_p140_export(root)
    plan = build_launch_plan(
        LaunchRequest(
            p140_export_dir=root,
            output_dir=tmp_path / "out",
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
            host="127.0.0.1",
            port=8088,
            start_local_server=False,
            smoke_timeout_sec=1,
        ),
        model,
        app_path,
    )
    assert plan["status"] == STATUS_READY
    assert plan["route_count"] == 3
    assert plan["safety"]["public_deploy"] is False
    assert plan["safety"]["google_sheets_write"] is False


def test_run_launch_no_start_writes_outputs(tmp_path: Path):
    root = _export_dir(tmp_path)
    out = tmp_path / "out"
    plan = run_launch(
        LaunchRequest(
            p140_export_dir=root,
            output_dir=out,
            run_id="R",
            generated_at_utc="2026-06-23T00:00:00Z",
            host="127.0.0.1",
            port=65534,
            start_local_server=False,
            smoke_timeout_sec=1,
        )
    )
    assert plan["status"] == STATUS_READY
    assert (out / "P141_LOCAL_LAUNCH_PLAN.json").exists()
    assert (out / "P141_SUMMARY.json").exists()


def test_cli_no_start(tmp_path: Path):
    root = _export_dir(tmp_path)
    out = tmp_path / "out"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p141_nicegui_cockpit_replica_local_launch",
            "--p140-export-dir",
            str(root),
            "--output-dir",
            str(out),
            "--port",
            "65534",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert STATUS_READY in completed.stdout
    assert "public_deploy=false" in completed.stdout
