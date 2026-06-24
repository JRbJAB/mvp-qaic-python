from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p170_nicegui_local_cache_read_binding import REQUIRED_CACHE_SOURCES
from mvp_qaic_py.p178_operator_shortcut_private_cockpit_handoff import (
    build_operator_handoff_payload,
    export_operator_handoff,
    render_launcher_ps1,
)


def _write_cache(project_root: Path) -> None:
    cache_dir = project_root / "00_OPERATOR_EXPORTS" / "P168G_LOCAL_CACHE"
    cache_dir.mkdir(parents=True, exist_ok=True)
    for spec in REQUIRED_CACHE_SOURCES:
        with (cache_dir / spec["file_name"]).open("w", encoding="utf-8", newline="") as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(["id", "status", "value"])
            writer.writerow([spec["source_id"], "READY", "sample"])


def test_build_operator_handoff_payload_ready(tmp_path: Path) -> None:
    _write_cache(tmp_path)

    payload = build_operator_handoff_payload(
        tmp_path,
        generated_at="2026-06-24T00:00:00+00:00",
    )

    assert payload["STATUS"] == "OK_P178_OPERATOR_SHORTCUT_PRIVATE_COCKPIT_HANDOFF_READY"
    assert payload["handoff_ready"] is True
    assert payload["operator_step_count"] == 7
    assert payload["blocker_count"] == 0
    assert payload["private_url"] == "http://127.0.0.1:8088"
    assert payload["public_serve"] is False
    assert payload["google_sheets_write"] is False
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_render_launcher_ps1_private_only(tmp_path: Path) -> None:
    launcher = render_launcher_ps1(tmp_path)

    assert "--host 127.0.0.1" in launcher
    assert "--port 8088" in launcher
    assert "--serve-private" in launcher
    assert "0.0.0.0" not in launcher
    assert "NO PUBLIC SERVE" in launcher


def test_export_operator_handoff_writes_expected_files(tmp_path: Path) -> None:
    _write_cache(tmp_path)
    export_dir = tmp_path / "05_EXPORTS" / "P178_TEST_EXPORT"

    payload = export_operator_handoff(tmp_path, export_dir=export_dir)

    assert payload["handoff_ready"] is True
    assert (tmp_path / "00_OPERATOR_SHORTCUTS" / "P178_RUN_PRIVATE_COCKPIT.ps1").exists()
    assert (tmp_path / "00_OPERATOR_SHORTCUTS" / "P178_OPERATOR_HANDOFF.md").exists()
    assert (export_dir / "P178_SUMMARY.json").exists()
    assert (export_dir / "P178_OPERATOR_HANDOFF_COPY.md").exists()
    assert (export_dir / "P178_OPERATOR_SHORTCUT_HANDOFF_REPORT.md").exists()

    summary = json.loads((export_dir / "P178_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["recommended_next"] == "P179_PRIVATE_COCKPIT_OPERATOR_USAGE_SMOKE_OR_CLOSE"
