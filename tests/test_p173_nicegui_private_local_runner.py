from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p170_nicegui_local_cache_read_binding import REQUIRED_CACHE_SOURCES
from mvp_qaic_py.p173_nicegui_private_local_runner import (
    build_private_runner_config,
    export_private_runner_smoke,
)


def _write_cache(project_root: Path) -> None:
    cache_dir = project_root / "00_OPERATOR_EXPORTS" / "P168G_LOCAL_CACHE"
    cache_dir.mkdir(parents=True, exist_ok=True)
    for spec in REQUIRED_CACHE_SOURCES:
        with (cache_dir / spec["file_name"]).open("w", encoding="utf-8", newline="") as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(["id", "status", "value"])
            writer.writerow([spec["source_id"], "READY", "sample"])


def test_build_private_runner_config_smoke_ok(tmp_path: Path) -> None:
    _write_cache(tmp_path)

    payload = build_private_runner_config(
        tmp_path,
        generated_at="2026-06-24T00:00:00+00:00",
    )

    assert payload["STATUS"] == "OK_P173_NICEGUI_PRIVATE_LOCAL_RUNNER_SMOKE_READY_REVIEW_ONLY"
    assert payload["host"] == "127.0.0.1"
    assert payload["port"] == 8088
    assert payload["route_count"] == 3
    assert payload["render_panel_count"] == 5
    assert payload["ready_render_panel_count"] == 5
    assert payload["smoke_ok"] is True
    assert payload["blocker_count"] == 0
    assert payload["server_started_by_smoke"] is False
    assert payload["public_serve"] is False
    assert payload["google_sheets_write"] is False
    assert payload["live_google_api_call_from_python"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_build_private_runner_config_blocks_public_host(tmp_path: Path) -> None:
    _write_cache(tmp_path)

    payload = build_private_runner_config(tmp_path, host="0.0.0.0")

    assert payload["STATUS"] == "BLOCKED_P173_NICEGUI_PRIVATE_LOCAL_RUNNER_SMOKE"
    assert payload["smoke_ok"] is False
    assert "PUBLIC_OR_NON_LOCAL_HOST_BLOCKED" in payload["blockers"]


def test_export_private_runner_smoke_writes_expected_files(tmp_path: Path) -> None:
    _write_cache(tmp_path)
    export_dir = tmp_path / "05_EXPORTS" / "P173_TEST_EXPORT"

    payload = export_private_runner_smoke(tmp_path, export_dir=export_dir)

    assert payload["smoke_ok"] is True
    assert (export_dir / "P173_PRIVATE_LOCAL_RUNNER_CONFIG.json").exists()
    assert (export_dir / "P173_SUMMARY.json").exists()
    assert (export_dir / "P173_PRIVATE_LOCAL_ROUTES.csv").exists()
    assert (export_dir / "P173_RUN_PRIVATE_LOCAL_COCKPIT.ps1").exists()
    assert (export_dir / "P173_PRIVATE_LOCAL_RUNNER_SMOKE_REPORT.md").exists()

    summary = json.loads((export_dir / "P173_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["recommended_next"] == "P174_NICEGUI_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE"
    assert summary["server_started_by_smoke"] is False
