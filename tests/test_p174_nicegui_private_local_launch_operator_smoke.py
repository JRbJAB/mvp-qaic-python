from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_py.p174_nicegui_private_local_launch_operator_smoke import (
    build_launch_operator_smoke_plan,
    export_launch_operator_smoke,
)


def test_build_launch_operator_smoke_plan_private_only(tmp_path: Path) -> None:
    payload = build_launch_operator_smoke_plan(tmp_path)

    assert payload["STATUS"] == "READY_P174_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE_PLAN"
    assert payload["host"] == "127.0.0.1"
    assert payload["port"] == 8088
    assert payload["route_count"] == 3
    assert payload["blocker_count"] == 0
    assert payload["public_serve"] is False
    assert payload["google_sheets_write"] is False
    assert payload["live_google_api_call_from_python"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_build_launch_operator_smoke_plan_blocks_public_host(tmp_path: Path) -> None:
    payload = build_launch_operator_smoke_plan(tmp_path, host="0.0.0.0")

    assert payload["STATUS"] == "BLOCKED_P174_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE_PLAN"
    assert payload["blocker_count"] == 1
    assert payload["blockers"] == ["PUBLIC_OR_NON_LOCAL_HOST_BLOCKED"]


def test_export_launch_operator_smoke_writes_expected_files(tmp_path: Path) -> None:
    payload = build_launch_operator_smoke_plan(tmp_path)
    payload = {
        **payload,
        "STATUS": "OK_P174_NICEGUI_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE",
        "route_results": [
            {"route": "/", "url": "http://127.0.0.1:8088/", "ok": True},
            {"route": "/cache", "url": "http://127.0.0.1:8088/cache", "ok": True},
            {"route": "/review", "url": "http://127.0.0.1:8088/review", "ok": True},
        ],
        "route_success_count": 3,
        "smoke_ok": True,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": True,
        "recommended_next": "P175_NICEGUI_OPERATOR_ERGONOMICS_POLISH",
    }
    export_dir = tmp_path / "05_EXPORTS" / "P174_TEST_EXPORT"

    exported = export_launch_operator_smoke(payload, export_dir)

    assert exported["smoke_ok"] is True
    assert (export_dir / "P174_PRIVATE_LOCAL_LAUNCH_SMOKE_RESULT.json").exists()
    assert (export_dir / "P174_SUMMARY.json").exists()
    assert (export_dir / "P174_PRIVATE_LOCAL_ROUTE_SMOKE.csv").exists()
    assert (export_dir / "P174_PRIVATE_LOCAL_LAUNCH_SMOKE_REPORT.md").exists()

    summary = json.loads((export_dir / "P174_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["route_success_count"] == 3
    assert summary["recommended_next"] == "P175_NICEGUI_OPERATOR_ERGONOMICS_POLISH"
