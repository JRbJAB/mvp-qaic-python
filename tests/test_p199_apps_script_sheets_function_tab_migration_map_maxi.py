from __future__ import annotations

from pathlib import Path

import mvp_qaic_py.p199_apps_script_sheets_function_tab_migration_map_maxi as p199


def test_apps_script_map_builds_from_dry_run_contract(monkeypatch, tmp_path: Path) -> None:
    def fake_dry(project_root: Path) -> dict[str, object]:
        return {
            "target_tab_rows": [
                {
                    "priority": idx,
                    "sheet_tab": f"GEM_TAB_{idx}",
                    "runtime_layer": f"GEM_LAYER_{idx}",
                    "source_export": "source.csv",
                    "dry_run_status": "DRY_RUN_READY",
                }
                for idx in range(1, 14)
            ]
        }

    monkeypatch.setattr(p199, "build_sheets_export_dry_run_contract_pack", fake_dry)

    pkg = tmp_path / "mvp_qaic_py"
    pkg.mkdir()
    (pkg / "p199_demo.py").write_text("def gem_layer_1():\n    return True\n", encoding="utf-8")

    payload = p199.build_apps_script_sheets_function_tab_migration_map(tmp_path)

    assert payload["sheet_tab_count"] == 13
    assert payload["python_module_count"] >= 1
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["google_sheets_write"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_collect_apps_script_sources_extracts_functions(tmp_path: Path) -> None:
    source_root = tmp_path / "apps_script"
    source_root.mkdir()
    (source_root / "Code.gs").write_text(
        "function MVPQAIC_Test(){ return true; }\nconst helper = () => true;\n",
        encoding="utf-8",
    )

    rows = p199._collect_apps_script_sources(tmp_path)

    assert len(rows) == 1
    assert rows[0]["function_count"] == 2
    assert "MVPQAIC_Test" in rows[0]["functions"]


def test_export_apps_script_map_writes_files(monkeypatch, tmp_path: Path) -> None:
    def fake_dry(project_root: Path) -> dict[str, object]:
        return {
            "target_tab_rows": [
                {
                    "priority": idx,
                    "sheet_tab": f"GEM_TAB_{idx}",
                    "runtime_layer": f"GEM_LAYER_{idx}",
                    "source_export": "source.csv",
                    "dry_run_status": "DRY_RUN_READY",
                }
                for idx in range(1, 14)
            ]
        }

    monkeypatch.setattr(p199, "build_sheets_export_dry_run_contract_pack", fake_dry)

    pkg = tmp_path / "mvp_qaic_py"
    pkg.mkdir()
    (pkg / "p199_demo.py").write_text("def gem_layer_1():\n    return True\n", encoding="utf-8")
    export_dir = tmp_path / "05_EXPORTS" / "P199_TEST_EXPORT"

    payload = p199.export_apps_script_sheets_function_tab_migration_map(
        tmp_path, export_dir=export_dir
    )

    assert payload["sheet_tab_count"] == 13
    assert (export_dir / "P199_APPS_SCRIPT_SHEETS_FUNCTION_TAB_MIGRATION_MAP.json").exists()
    assert (export_dir / "P199_MIGRATION_MAP.csv").exists()
    assert (export_dir / "P199_PYTHON_MODULES.csv").exists()
    assert (export_dir / "P199_APPS_SCRIPT_SOURCES.csv").exists()
    assert (export_dir / "P199_GATE_ROWS.csv").exists()
    assert (export_dir / "P199_VISUAL_PLANNING.csv").exists()
    assert (export_dir / "P199_SUMMARY.json").exists()
    assert (export_dir / "P199_REPORT.md").exists()
