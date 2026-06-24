from __future__ import annotations

from pathlib import Path

from mvp_qaic_py.p192r_gem_tracking_tabs_csv_export_operator_view_polish import (
    build_gem_tracking_operator_view,
    export_gem_tracking_operator_view,
)


def test_operator_view_marks_partial_layers(tmp_path: Path) -> None:
    pkg = tmp_path / "mvp_qaic_py"
    pkg.mkdir()
    (pkg / "p173_nicegui_private_local_runner.py").write_text(
        '@ui.page("/gem-tracking-operator")\ndef ops():\n    pass\n'
        '@ui.page("/review")\ndef review():\n    pass\n',
        encoding="utf-8",
    )

    payload = build_gem_tracking_operator_view(tmp_path)

    assert payload["layer_count"] == 10
    assert payload["review_count"] >= 1
    assert any(row["operator_status"] != "OK_READY" for row in payload["operator_rows"])
    assert payload["gem_call_executed"] is False
    assert payload["google_sheets_write"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_operator_view_ready_layers_with_sources_and_routes(tmp_path: Path) -> None:
    pkg = tmp_path / "mvp_qaic_py"
    pkg.mkdir()
    (pkg / "p173_nicegui_private_local_runner.py").write_text(
        '@ui.page("/capture")\ndef capture():\n    pass\n',
        encoding="utf-8",
    )
    inbox = tmp_path / "00_OPERATOR_EXPORTS" / "P181_CAPTURE_INBOX"
    inbox.mkdir(parents=True)
    (inbox / "capture.png").write_bytes(b"image")
    (pkg / "p183_capture_to_session_link_prompt_run_workflow.py").write_text(
        "x=1", encoding="utf-8"
    )

    payload = build_gem_tracking_operator_view(tmp_path)
    capture = next(
        row for row in payload["operator_rows"] if row["layer_id"] == "GEM_CAPTURE_INBOX"
    )

    assert capture["operator_status"] == "OK_READY"
    assert capture["operator_action"] == "KEEP_TRACKING"


def test_export_operator_view_writes_csvs(tmp_path: Path) -> None:
    export_dir = tmp_path / "05_EXPORTS" / "P192R_TEST_EXPORT"

    payload = export_gem_tracking_operator_view(tmp_path, export_dir=export_dir)

    assert payload["layer_count"] == 10
    assert (export_dir / "P192R_GEM_TRACKING_OPERATOR_VIEW.json").exists()
    assert (export_dir / "P192R_GEM_TRACKING_OPERATOR_VIEW.csv").exists()
    assert (export_dir / "P192R_GEM_TRACKING_LAYER_STATUS.csv").exists()
    assert (export_dir / "P192R_GEM_TRACKING_ACTIONS.csv").exists()
    assert (export_dir / "P192R_SUMMARY.json").exists()
    assert (export_dir / "P192R_REPORT.md").exists()
