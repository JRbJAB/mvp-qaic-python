from __future__ import annotations

from pathlib import Path

from mvp_qaic_py.p190r_runtime_migration_tracker_live_readonly import (
    build_runtime_migration_tracker,
    export_runtime_migration_tracker,
)


def test_runtime_tracker_discovers_python_and_gem_layers(tmp_path: Path) -> None:
    pkg = tmp_path / "mvp_qaic_py"
    tests = tmp_path / "tests"
    pkg.mkdir()
    tests.mkdir()
    (pkg / "p173_nicegui_private_local_runner.py").write_text(
        'from nicegui import ui\n@ui.page("/migration")\ndef migration():\n    pass\n',
        encoding="utf-8",
    )
    (pkg / "p190r_runtime_migration_tracker_live_readonly.py").write_text(
        "def build_runtime_migration_tracker():\n    pass\n",
        encoding="utf-8",
    )
    (tests / "test_p190r_runtime_migration_tracker_live_readonly.py").write_text(
        "def test_ok():\n    assert True\n",
        encoding="utf-8",
    )

    payload = build_runtime_migration_tracker(tmp_path)

    assert payload["artifact_count"] >= 3
    assert any(row["name"] == "/migration" for row in payload["artifacts"])
    assert any(row["name"] == "RUNTIME_MIGRATION_TRACKER" for row in payload["gem_tracking_rows"])
    assert payload["gem_call_executed"] is False
    assert payload["google_sheets_write"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_runtime_tracker_discovers_csv_sheet_snapshot(tmp_path: Path) -> None:
    export_dir = tmp_path / "05_EXPORTS"
    export_dir.mkdir()
    (export_dir / "GEM_DECISION_JOURNAL.csv").write_text(
        "run_id,status,decision,prompt_id,response_id,blocker_count\nr1,WAIT,REVIEW,p1,resp1,0\n",
        encoding="utf-8",
    )

    payload = build_runtime_migration_tracker(tmp_path)

    assert any(row["artifact_type"] == "SHEET_TAB_OR_CSV_SNAPSHOT" for row in payload["artifacts"])


def test_export_runtime_migration_tracker_writes_expected_files(tmp_path: Path) -> None:
    pkg = tmp_path / "mvp_qaic_py"
    pkg.mkdir()
    (pkg / "p190r_runtime_migration_tracker_live_readonly.py").write_text(
        "def x():\n    pass\n",
        encoding="utf-8",
    )
    export_dir = tmp_path / "05_EXPORTS" / "P190R_TEST_EXPORT"

    payload = export_runtime_migration_tracker(tmp_path, export_dir=export_dir)

    assert payload["artifact_count"] >= 1
    assert (export_dir / "P190R_RUNTIME_MIGRATION_TRACKER.json").exists()
    assert (export_dir / "P190R_RUNTIME_ARTIFACTS.csv").exists()
    assert (export_dir / "P190R_GEM_TRACKING_LAYERS.csv").exists()
    assert (export_dir / "P190R_SUMMARY.json").exists()
    assert (export_dir / "P190R_REPORT.md").exists()
