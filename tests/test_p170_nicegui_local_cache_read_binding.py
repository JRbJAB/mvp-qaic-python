from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p170_nicegui_local_cache_read_binding import (
    REQUIRED_CACHE_SOURCES,
    build_local_cache_binding_payload,
    export_local_cache_binding,
)


def _write_cache(project_root: Path) -> Path:
    cache_dir = project_root / "00_OPERATOR_EXPORTS" / "P168G_LOCAL_CACHE"
    cache_dir.mkdir(parents=True, exist_ok=True)
    for spec in REQUIRED_CACHE_SOURCES:
        with (cache_dir / spec["file_name"]).open("w", encoding="utf-8", newline="") as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(["id", "status", "value"])
            writer.writerow([spec["source_id"], "READY", "sample"])
    return cache_dir


def test_build_local_cache_binding_payload_ready(tmp_path: Path) -> None:
    _write_cache(tmp_path)

    payload = build_local_cache_binding_payload(
        tmp_path,
        generated_at="2026-06-24T00:00:00+00:00",
    )

    assert payload["STATUS"] == "OK_P170_NICEGUI_LOCAL_CACHE_READ_BINDING_READY_REVIEW_ONLY"
    assert payload["cache_source_count"] == 5
    assert payload["ready_source_count"] == 5
    assert payload["panel_count"] == 5
    assert payload["binding_ready"] is True
    assert payload["blocker_count"] == 0
    assert payload["google_sheets_write"] is False
    assert payload["live_google_api_call_from_python"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_build_local_cache_binding_payload_blocks_missing_cache_file(tmp_path: Path) -> None:
    cache_dir = _write_cache(tmp_path)
    (cache_dir / "MVP_QAIC_CONFIG.csv").unlink()

    payload = build_local_cache_binding_payload(tmp_path)

    assert payload["STATUS"] == "BLOCKED_P170_NICEGUI_LOCAL_CACHE_READ_BINDING"
    assert payload["binding_ready"] is False
    assert payload["blocker_count"] == 1
    assert payload["blockers"] == ["MISSING_CACHE_FILE:MVP_QAIC_CONFIG.csv"]
    assert payload["ready_source_count"] == 4


def test_export_local_cache_binding_writes_expected_files(tmp_path: Path) -> None:
    _write_cache(tmp_path)
    export_dir = tmp_path / "05_EXPORTS" / "P170_TEST_EXPORT"

    payload = export_local_cache_binding(tmp_path, export_dir=export_dir)

    assert payload["binding_ready"] is True
    assert (export_dir / "P170_NICEGUI_LOCAL_CACHE_BINDING_PAYLOAD.json").exists()
    assert (export_dir / "P170_SUMMARY.json").exists()
    assert (export_dir / "P170_NICEGUI_PANEL_BINDING_MAP.csv").exists()
    assert (export_dir / "P170_NICEGUI_LOCAL_CACHE_READ_BINDING_REPORT.md").exists()

    summary = json.loads((export_dir / "P170_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["ready_source_count"] == 5
    assert summary["panel_count"] == 5
    assert summary["recommended_next"] == "P171_NICEGUI_LOCAL_PROMPT_COCKPIT_BIND_CACHE_PANELS"
