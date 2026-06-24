from __future__ import annotations

from pathlib import Path

from mvp_qaic_py.p194r_gem_runtime_tracker_close_sheets_export_contract import (
    build_gem_runtime_close_contract,
    export_gem_runtime_close_contract,
)


def test_runtime_close_contract_builds_expected_sheet_contract(tmp_path: Path) -> None:
    pkg = tmp_path / "mvp_qaic_py"
    pkg.mkdir()
    (pkg / "p173_nicegui_private_local_runner.py").write_text(
        '@ui.page("/runtime-contract")\ndef x():\n    pass\n',
        encoding="utf-8",
    )
    exports = tmp_path / "05_EXPORTS"
    (exports / "P186_REAL_OPERATOR_ROUNDTRIP_SMOKE").mkdir(parents=True)
    (exports / "P186_REAL_OPERATOR_ROUNDTRIP_SMOKE" / "P186_SUMMARY.json").write_text(
        "{}", encoding="utf-8"
    )
    (exports / "P120_GEM_RESPONSE_DECISION_JOURNAL_BRIDGE").mkdir()
    (
        exports / "P120_GEM_RESPONSE_DECISION_JOURNAL_BRIDGE" / "P120_DECISION_JOURNAL_ENTRY.csv"
    ).write_text(
        "run_id,status\nr1,REVIEW\n",
        encoding="utf-8",
    )

    payload = build_gem_runtime_close_contract(tmp_path)

    assert payload["sheet_contract_row_count"] == 13
    assert any(row["sheet_tab"] == "GEM_DECISION_JOURNAL" for row in payload["sheet_contract_rows"])
    assert payload["gem_call_executed"] is False
    assert payload["google_sheets_write"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_runtime_close_contract_has_readonly_write_policy(tmp_path: Path) -> None:
    payload = build_gem_runtime_close_contract(tmp_path)

    assert payload["sheet_contract_row_count"] == 13
    assert all(
        row["write_policy"] == "READONLY_EXPORT_CONTRACT_NO_SHEET_WRITE"
        for row in payload["sheet_contract_rows"]
    )
    assert all(row["human_review_required"] is True for row in payload["sheet_contract_rows"])


def test_export_runtime_close_contract_writes_files(tmp_path: Path) -> None:
    export_dir = tmp_path / "05_EXPORTS" / "P194R_TEST_EXPORT"

    payload = export_gem_runtime_close_contract(tmp_path, export_dir=export_dir)

    assert payload["sheet_contract_row_count"] == 13
    assert (export_dir / "P194R_GEM_RUNTIME_CLOSE_CONTRACT.json").exists()
    assert (export_dir / "P194R_SHEETS_EXPORT_CONTRACT.csv").exists()
    assert (export_dir / "P194R_RUNTIME_CLOSE_STATUS.csv").exists()
    assert (export_dir / "P194R_SUMMARY.json").exists()
    assert (export_dir / "P194R_REPORT.md").exists()
