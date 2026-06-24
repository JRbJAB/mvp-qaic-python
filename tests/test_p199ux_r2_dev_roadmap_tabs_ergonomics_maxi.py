from __future__ import annotations

from pathlib import Path

import mvp_qaic_py.p199ux_r2_dev_roadmap_tabs_ergonomics_maxi as p199ux


def test_roadmap_includes_past_current_future_post_python(monkeypatch, tmp_path: Path) -> None:
    def fake_dry(project_root: Path) -> dict[str, object]:
        return {"dry_run_coverage_percent": 96.5}

    def fake_map(project_root: Path) -> dict[str, object]:
        return {
            "sheet_tab_count": 13,
            "ready_mapping_count": 12,
            "python_module_count": 293,
            "apps_script_source_count": 8,
            "migration_map_coverage_percent": 97.7,
        }

    monkeypatch.setattr(p199ux, "build_sheets_export_dry_run_contract_pack", fake_dry)
    monkeypatch.setattr(p199ux, "build_apps_script_sheets_function_tab_migration_map", fake_map)

    payload = p199ux.build_dev_roadmap_tabs_ergonomics(tmp_path)
    periods = {row["period"] for row in payload["roadmap_rows"]}

    assert {"PASSÉ", "EN COURS", "EN ATTENTE", "AVENIR PROCHE", "POST-PYTHON"}.issubset(periods)
    assert payload["roadmap_step_count"] >= 12
    assert payload["post_python_step_count"] >= 3
    assert payload["nicegui_tab_count"] >= 8
    assert payload["google_sheets_write"] is False
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_nicegui_tabs_are_operator_useful() -> None:
    rows = p199ux.NICEGUI_TAB_ROWS

    assert any(row["route"] == "/dev-roadmap" for row in rows)
    assert all(row["label_fr"] for row in rows)
    assert all(row["purpose"] for row in rows)
    assert all(row["data_rendered"] for row in rows)
    assert all(row["operator_value"] for row in rows)


def test_export_dev_roadmap_writes_outputs(monkeypatch, tmp_path: Path) -> None:
    def fake_dry(project_root: Path) -> dict[str, object]:
        return {"dry_run_coverage_percent": 96.5}

    def fake_map(project_root: Path) -> dict[str, object]:
        return {
            "sheet_tab_count": 13,
            "ready_mapping_count": 12,
            "python_module_count": 293,
            "apps_script_source_count": 8,
            "migration_map_coverage_percent": 97.7,
        }

    monkeypatch.setattr(p199ux, "build_sheets_export_dry_run_contract_pack", fake_dry)
    monkeypatch.setattr(p199ux, "build_apps_script_sheets_function_tab_migration_map", fake_map)

    export_dir = tmp_path / "05_EXPORTS" / "P199UX_R2_TEST_EXPORT"
    payload = p199ux.export_dev_roadmap_tabs_ergonomics(tmp_path, export_dir=export_dir)

    assert payload["roadmap_step_count"] >= 12
    assert (export_dir / "P199UX_R2_DEV_ROADMAP_TABS_ERGONOMICS.json").exists()
    assert (export_dir / "P199UX_R2_VISUAL_ROADMAP.csv").exists()
    assert (export_dir / "P199UX_R2_NICEGUI_TABS_USABILITY.csv").exists()
    assert (export_dir / "P199UX_R2_DECISIONS.csv").exists()
    assert (export_dir / "P199UX_R2_SUMMARY.json").exists()
    assert (export_dir / "P199UX_R2_REPORT.md").exists()
