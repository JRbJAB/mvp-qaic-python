from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_reflex_ui.tracker_auto_update import (
    build_tracker_auto_update_snapshot,
    format_tracker_auto_update_markdown,
    write_tracker_auto_update_snapshot,
)


def test_tracker_auto_update_reads_local_sources(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "05_EXPORTS" / "P_TEST").mkdir(parents=True)
    (tmp_path / "docs" / "WEB_ARCHITECTURE_SITEMAP.json").write_text(
        json.dumps({"status": "OK", "routes": [{"route": "/"}]}),
        encoding="utf-8",
    )
    (tmp_path / "docs" / "MIGRATION_TRACKER.json").write_text(
        json.dumps({"status": "OK", "items": [{"name": "Sheets"}]}),
        encoding="utf-8",
    )
    (tmp_path / "05_EXPORTS" / "P_TEST" / "report.md").write_text("# report", encoding="utf-8")
    csv_path = tmp_path / "docs" / "MVPQAIC_CLASP_IMPORTS_ALL.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "record_type",
                "module_family",
                "severity",
                "script_file_name",
                "function_name",
                "calls_urlfetch",
                "writes_sheet_likely",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "record_type": "SCRIPT_INVENTORY",
                "module_family": "CORE",
                "severity": "LOW",
                "script_file_name": "a.js",
                "function_name": "runA",
                "calls_urlfetch": "NO",
                "writes_sheet_likely": "NO",
            }
        )

    snapshot = build_tracker_auto_update_snapshot(tmp_path)

    assert snapshot["status"] == "LOCAL_FILES_SYNC_REQUIRED"
    assert snapshot["safety_flags"]["HUMAN_REVIEW_ONLY"] is True
    assert snapshot["trackers"]["dev_tracking"]["file_count"] >= 1
    assert snapshot["trackers"]["cdc_tracker"]["exists"] is True
    assert snapshot["trackers"]["migration_tracker"]["exists"] is True
    assert snapshot["trackers"]["clasp_imports"]["rows_scanned"] == 1


def test_tracker_auto_update_writes_snapshot_files(tmp_path: Path) -> None:
    snapshot = write_tracker_auto_update_snapshot(tmp_path)
    md = format_tracker_auto_update_markdown(snapshot)

    assert (tmp_path / "docs" / "TRACKER_AUTO_UPDATE_SNAPSHOT.json").exists()
    assert (tmp_path / "docs" / "TRACKER_AUTO_UPDATE_SNAPSHOT.md").exists()
    assert "Auto-update Trackers" in md
