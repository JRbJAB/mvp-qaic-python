from __future__ import annotations

from pathlib import Path

import mvp_qaic_py.p198_sheets_export_dry_run_contract_pack_maxi as p198


def test_sheets_export_dry_run_uses_contract_without_writing(monkeypatch, tmp_path: Path) -> None:
    def fake_runtime_contract(project_root: Path) -> dict[str, object]:
        rows = []
        for idx in range(13):
            rows.append(
                {
                    "sheet_tab": f"TAB_{idx}",
                    "runtime_layer": f"LAYER_{idx}",
                    "source_export": "sample.csv",
                    "primary_key": "id",
                    "required_columns": "id,status",
                    "export_status": "READY_FOR_READONLY_EXPORT",
                    "readiness_percent": 100,
                }
            )
        return {
            "sheet_contract_rows": rows,
            "runtime_close_percent": 96.5,
        }

    def fake_prompt_master(project_root: Path) -> dict[str, object]:
        return {"candidate_count": 10}

    monkeypatch.setattr(p198, "build_gem_runtime_close_contract", fake_runtime_contract)
    monkeypatch.setattr(p198, "build_prompt_master_historical_regression", fake_prompt_master)

    payload = p198.build_sheets_export_dry_run_contract_pack(tmp_path)

    assert payload["target_tab_count"] == 13
    assert payload["ready_tab_count"] == 13
    assert payload["dry_run_status"] == "READY_DRY_RUN_ONLY_NO_LIVE_WRITE"
    assert payload["google_sheets_write"] is False
    assert payload["real_sheet_write_allowed"] is False
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_sheets_export_dry_run_estimates_csv_rows(tmp_path: Path) -> None:
    exports = tmp_path / "05_EXPORTS" / "PACK"
    exports.mkdir(parents=True)
    (exports / "sample.csv").write_text("id,status\n1,OK\n2,OK\n", encoding="utf-8")

    count = p198._estimate_rows_from_path(tmp_path, "sample.csv")

    assert count == 2


def test_export_sheets_export_dry_run_writes_files(monkeypatch, tmp_path: Path) -> None:
    def fake_runtime_contract(project_root: Path) -> dict[str, object]:
        rows = []
        for idx in range(13):
            rows.append(
                {
                    "sheet_tab": f"TAB_{idx}",
                    "runtime_layer": f"LAYER_{idx}",
                    "source_export": "sample.csv",
                    "primary_key": "id",
                    "required_columns": "id,status",
                    "export_status": "READY_FOR_READONLY_EXPORT",
                    "readiness_percent": 100,
                }
            )
        return {
            "sheet_contract_rows": rows,
            "runtime_close_percent": 96.5,
        }

    def fake_prompt_master(project_root: Path) -> dict[str, object]:
        return {"candidate_count": 10}

    monkeypatch.setattr(p198, "build_gem_runtime_close_contract", fake_runtime_contract)
    monkeypatch.setattr(p198, "build_prompt_master_historical_regression", fake_prompt_master)

    export_dir = tmp_path / "05_EXPORTS" / "P198_TEST_EXPORT"
    payload = p198.export_sheets_export_dry_run_contract_pack(tmp_path, export_dir=export_dir)

    assert payload["target_tab_count"] == 13
    assert (export_dir / "P198_SHEETS_EXPORT_DRY_RUN_CONTRACT_PACK.json").exists()
    assert (export_dir / "P198_TARGET_SHEET_TABS_DRY_RUN.csv").exists()
    assert (export_dir / "P198_EXPORT_GATES.csv").exists()
    assert (export_dir / "P198_VISUAL_PLANNING.csv").exists()
    assert (export_dir / "P198_DRY_RUN_WRITE_PAYLOAD.json").exists()
    assert (export_dir / "P198_SUMMARY.json").exists()
    assert (export_dir / "P198_REPORT.md").exists()
