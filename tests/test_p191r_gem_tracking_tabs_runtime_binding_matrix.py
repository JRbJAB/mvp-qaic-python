from __future__ import annotations

from pathlib import Path

from mvp_qaic_py.p191r_gem_tracking_tabs_runtime_binding_matrix import (
    build_gem_tracking_tabs_runtime_binding_matrix,
    export_gem_tracking_tabs_runtime_binding_matrix,
)


def test_gem_tracking_binding_matrix_has_expected_layers(tmp_path: Path) -> None:
    pkg = tmp_path / "mvp_qaic_py"
    pkg.mkdir()
    (pkg / "p173_nicegui_private_local_runner.py").write_text(
        '@ui.page("/gem-tracking")\ndef gem_tracking():\n    pass\n'
        '@ui.page("/capture")\ndef capture():\n    pass\n',
        encoding="utf-8",
    )
    (pkg / "p190r_runtime_migration_tracker_live_readonly.py").write_text(
        "def x():\n    pass\n",
        encoding="utf-8",
    )

    payload = build_gem_tracking_tabs_runtime_binding_matrix(tmp_path)

    assert payload["layer_count"] == 10
    assert any(row["layer_id"] == "GEM_CAPTURE_INBOX" for row in payload["layers"])
    assert any(row["layer_id"] == "RUNTIME_MIGRATION_TRACKER" for row in payload["layers"])
    assert payload["gem_call_executed"] is False
    assert payload["google_sheets_write"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_gem_tracking_binding_matrix_counts_local_files(tmp_path: Path) -> None:
    inbox = tmp_path / "00_OPERATOR_EXPORTS" / "P181_CAPTURE_INBOX"
    inbox.mkdir(parents=True)
    (inbox / "capture.png").write_bytes(b"image")
    (inbox / "desktop.ini").write_text("ignored", encoding="utf-8")

    payload = build_gem_tracking_tabs_runtime_binding_matrix(tmp_path)
    capture_layer = next(row for row in payload["layers"] if row["layer_id"] == "GEM_CAPTURE_INBOX")

    assert capture_layer["source_exists"] is True
    assert capture_layer["local_file_count"] == 1


def test_export_gem_tracking_binding_matrix_writes_expected_files(tmp_path: Path) -> None:
    pkg = tmp_path / "mvp_qaic_py"
    pkg.mkdir()
    (pkg / "p173_nicegui_private_local_runner.py").write_text("", encoding="utf-8")
    export_dir = tmp_path / "05_EXPORTS" / "P191R_TEST_EXPORT"

    payload = export_gem_tracking_tabs_runtime_binding_matrix(
        tmp_path,
        export_dir=export_dir,
    )

    assert payload["layer_count"] == 10
    assert (export_dir / "P191R_GEM_TRACKING_BINDING_MATRIX.json").exists()
    assert (export_dir / "P191R_GEM_TRACKING_BINDING_MATRIX.csv").exists()
    assert (export_dir / "P191R_SUMMARY.json").exists()
    assert (export_dir / "P191R_REPORT.md").exists()
