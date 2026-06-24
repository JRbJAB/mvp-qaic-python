from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p168b_sheets_data_snapshot_layer_readonly import (
    DEFAULT_BOUNDED_READ_PLAN,
    MVP_SHEET_ID,
    QAIC_V25_SHEET_ID,
    build_outputs,
    build_snapshot_manifest,
    detect_csv_dimensions,
    discover_latest_export,
)


def test_discover_latest_export_uses_deterministic_name_sort(tmp_path: Path) -> None:
    older = tmp_path / "05_EXPORTS" / "P168A_HIERARCHY_AND_MIGRATION_ROADMAP_LOCK_20260623_010101"
    newer = tmp_path / "05_EXPORTS" / "P168A_HIERARCHY_AND_MIGRATION_ROADMAP_LOCK_20260623_020202"
    older.mkdir(parents=True)
    newer.mkdir(parents=True)
    found = discover_latest_export(tmp_path, "P168A_HIERARCHY_AND_MIGRATION_ROADMAP_LOCK_")
    assert found is not None
    assert found.name.endswith("020202")


def test_default_plan_preserves_mvp_and_reference_boundaries() -> None:
    ids = {row["spreadsheet_id"] for row in DEFAULT_BOUNDED_READ_PLAN}
    assert MVP_SHEET_ID in ids
    assert QAIC_V25_SHEET_ID in ids
    reference_rows = [
        row for row in DEFAULT_BOUNDED_READ_PLAN if row["spreadsheet_id"] == QAIC_V25_SHEET_ID
    ]
    assert reference_rows
    assert reference_rows[0]["required_before_python_port"] == "NO"


def test_detect_csv_dimensions(tmp_path: Path) -> None:
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("a,b,c\n1,2,3\n4,5\n", encoding="utf-8")
    assert detect_csv_dimensions(csv_path) == (3, 3)


def test_build_manifest_requires_p165_and_p168a_exports(tmp_path: Path) -> None:
    payload = build_snapshot_manifest(tmp_path)
    assert payload["status"] == "P168B_SHEETS_DATA_SNAPSHOT_LAYER_READY_READONLY"
    assert payload["blocker_count"] >= 2
    assert "MISSING_P165_SOURCE_ACCESS_EXPORT" in payload["blockers"]
    assert "MISSING_P168A_HIERARCHY_LOCK_EXPORT" in payload["blockers"]
    assert payload["safety_flags"]["google_sheets_write"] is False
    assert payload["safety_flags"]["live_google_api_call_from_python"] is False


def test_build_outputs_from_minimal_prior_exports(tmp_path: Path) -> None:
    p165 = (
        tmp_path
        / "05_EXPORTS"
        / "P165_R3_INITIAL_SHEET_APPS_SCRIPT_FUNCTIONAL_LAYER_20260623_010101"
    )
    p168a = tmp_path / "05_EXPORTS" / "P168A_HIERARCHY_AND_MIGRATION_ROADMAP_LOCK_20260623_010101"
    p165.mkdir(parents=True)
    p168a.mkdir(parents=True)
    (p165 / "P165_R3_SUMMARY.json").write_text(
        json.dumps({"status": "OK", "apps_script_module_count": 22}), encoding="utf-8"
    )
    (p168a / "P168A_SUMMARY.json").write_text(
        json.dumps({"status": "OK", "hierarchy_locked": True}), encoding="utf-8"
    )
    with (p165 / "P165_R3_SOURCE_REGISTRY.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source_key", "source_id", "title"])
        writer.writeheader()
        writer.writerow(
            {
                "source_key": "LIVE_SHEET_MVP_QAIC_DEV",
                "source_id": MVP_SHEET_ID,
                "title": "MVP",
            }
        )

    export_dir = build_outputs(tmp_path)
    summary = json.loads((export_dir / "P168B_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["blocker_count"] == 0
    assert summary["hierarchy_locked"] is True
    assert summary["source_registry_count"] == 1
    assert summary["bounded_read_plan_count"] >= 5
    assert (export_dir / "P168B_BOUNDED_READ_PLAN.csv").exists()
    assert (export_dir / "P168B_SNAPSHOT_LAYER_REPORT.md").exists()
