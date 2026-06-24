from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p170_nicegui_local_cache_read_binding import REQUIRED_CACHE_SOURCES
from mvp_qaic_py.p178_operator_shortcut_private_cockpit_handoff import export_operator_handoff
from mvp_qaic_py.p179_private_cockpit_operator_usage_smoke_or_close import (
    build_private_cockpit_usage_close_payload,
    export_private_cockpit_usage_close,
)


def _write_cache(project_root: Path) -> None:
    cache_dir = project_root / "00_OPERATOR_EXPORTS" / "P168G_LOCAL_CACHE"
    cache_dir.mkdir(parents=True, exist_ok=True)
    for spec in REQUIRED_CACHE_SOURCES:
        with (cache_dir / spec["file_name"]).open("w", encoding="utf-8", newline="") as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(["id", "status", "value"])
            writer.writerow([spec["source_id"], "READY", "sample"])


def test_build_private_cockpit_usage_close_payload_ready(tmp_path: Path) -> None:
    _write_cache(tmp_path)
    export_operator_handoff(tmp_path, export_dir=tmp_path / "05_EXPORTS" / "P178_TEST")

    payload = build_private_cockpit_usage_close_payload(
        tmp_path,
        generated_at="2026-06-24T00:00:00+00:00",
    )

    assert payload["STATUS"] == "OK_P179_PRIVATE_COCKPIT_OPERATOR_USAGE_CLOSE_READY"
    assert payload["close_ready"] is True
    assert payload["check_count"] == 6
    assert payload["pass_count"] == 6
    assert payload["fail_count"] == 0
    assert payload["blocker_count"] == 0
    assert payload["public_serve"] is False
    assert payload["google_sheets_write"] is False
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_private_cockpit_usage_close_blocks_missing_shortcut(tmp_path: Path) -> None:
    _write_cache(tmp_path)

    payload = build_private_cockpit_usage_close_payload(tmp_path)

    assert payload["STATUS"] == "BLOCKED_P179_PRIVATE_COCKPIT_OPERATOR_USAGE_CLOSE"
    assert payload["close_ready"] is False
    assert "MISSING_OPERATOR_LAUNCHER" in payload["blockers"]


def test_export_private_cockpit_usage_close_writes_expected_files(tmp_path: Path) -> None:
    _write_cache(tmp_path)
    export_operator_handoff(tmp_path, export_dir=tmp_path / "05_EXPORTS" / "P178_TEST")
    payload = build_private_cockpit_usage_close_payload(tmp_path)
    payload = {
        **payload,
        "usage_smoke_executed": True,
        "usage_smoke_ok": True,
        "route_success_count": 3,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": True,
    }
    export_dir = tmp_path / "05_EXPORTS" / "P179_TEST_EXPORT"

    exported = export_private_cockpit_usage_close(payload, export_dir)

    assert exported["usage_smoke_ok"] is True
    assert (export_dir / "P179_PRIVATE_COCKPIT_USAGE_CLOSE_RESULT.json").exists()
    assert (export_dir / "P179_SUMMARY.json").exists()
    assert (export_dir / "P179_PRIVATE_COCKPIT_CLOSE_REPORT.md").exists()

    summary = json.loads((export_dir / "P179_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["route_success_count"] == 3
