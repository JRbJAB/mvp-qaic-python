from __future__ import annotations

from pathlib import Path

from mvp_qaic_py.p195r_operator_release_runtime_tracker_next_selector_maxi import (
    build_operator_release_runtime_tracker,
    export_operator_release_runtime_tracker,
)


def test_operator_release_builds_next_selector(tmp_path: Path) -> None:
    pkg = tmp_path / "mvp_qaic_py"
    pkg.mkdir()
    (pkg / "p173_nicegui_private_local_runner.py").write_text(
        '@ui.page("/operator-release")\ndef x():\n    pass\n',
        encoding="utf-8",
    )
    exports = tmp_path / "05_EXPORTS"
    (exports / "P186_REAL_OPERATOR_ROUNDTRIP_SMOKE").mkdir(parents=True)
    (exports / "P186_REAL_OPERATOR_ROUNDTRIP_SMOKE" / "P186_SUMMARY.json").write_text(
        "{}",
        encoding="utf-8",
    )
    (exports / "P120_GEM_RESPONSE_DECISION_JOURNAL_BRIDGE").mkdir()
    (
        exports / "P120_GEM_RESPONSE_DECISION_JOURNAL_BRIDGE" / "P120_DECISION_JOURNAL_ENTRY.csv"
    ).write_text(
        "run_id,status\nr1,REVIEW\n",
        encoding="utf-8",
    )

    payload = build_operator_release_runtime_tracker(tmp_path)

    assert payload["operator_runtime_release_allowed"] is True
    assert payload["sheets_export_allowed"] is False
    assert payload["selected_next_pack"] == "P196_REAL_CASE_PORTFOLIO_GEM_OPERATOR_INPUTS_MAXI"
    assert len(payload["next_work_rows"]) == 4
    assert payload["gem_call_executed"] is False
    assert payload["google_sheets_write"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_operator_release_contains_review_waivers(tmp_path: Path) -> None:
    payload = build_operator_release_runtime_tracker(tmp_path)

    assert payload["review_waiver_count"] == 2
    assert any(row["scope"] == "GEM_DECISION_JOURNAL" for row in payload["review_waivers"])
    assert payload["sheets_export_allowed"] is False


def test_export_operator_release_writes_files(tmp_path: Path) -> None:
    exports = tmp_path / "05_EXPORTS"
    (exports / "P186_REAL_OPERATOR_ROUNDTRIP_SMOKE").mkdir(parents=True)
    (exports / "P120_GEM_RESPONSE_DECISION_JOURNAL_BRIDGE").mkdir()
    export_dir = tmp_path / "05_EXPORTS" / "P195R_TEST_EXPORT"

    payload = export_operator_release_runtime_tracker(tmp_path, export_dir=export_dir)

    assert payload["selected_next_pack"] == "P196_REAL_CASE_PORTFOLIO_GEM_OPERATOR_INPUTS_MAXI"
    assert (export_dir / "P195R_OPERATOR_RELEASE_RUNTIME_TRACKER.json").exists()
    assert (export_dir / "P195R_RELEASE_GATES.csv").exists()
    assert (export_dir / "P195R_NEXT_WORK_SELECTOR.csv").exists()
    assert (export_dir / "P195R_REVIEW_WAIVERS.csv").exists()
    assert (export_dir / "P195R_SUMMARY.json").exists()
    assert (export_dir / "P195R_REPORT.md").exists()
