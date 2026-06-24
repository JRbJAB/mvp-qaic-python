from __future__ import annotations

from pathlib import Path

import mvp_qaic_py.p200r2_deep_cockpit_ux_instructions_tracker_maxi as p200r2


def test_instructions_tracker_contains_mandatory_themes() -> None:
    rows = p200r2._instruction_rows()
    themes = {row["theme"] for row in rows}

    assert "Safety QAIC" in themes
    assert "UX Cockpit" in themes
    assert "Migration" in themes
    assert "Evidence" in themes
    assert all(row["color_cell"] for row in rows)
    assert any(row["status"] == "CRITICAL_CORRECTION" for row in rows)


def test_deep_cockpit_builds_colored_migration_and_no_live_flags(
    monkeypatch, tmp_path: Path
) -> None:
    def fake_ux(project_root: Path) -> dict[str, object]:
        return {
            "nicegui_tab_count": 9,
            "roadmap_step_count": 15,
            "post_python_step_count": 4,
            "nicegui_tab_rows": [],
            "top_visual_planning_rows": [
                {
                    "order": 1,
                    "period": "PASSÉ",
                    "step_count": 5,
                    "avg_progress_percent": 98.0,
                    "main_status": "DONE",
                    "main_route": "/migration",
                }
            ],
        }

    def fake_migration(project_root: Path) -> dict[str, object]:
        return {
            "sheet_tab_count": 13,
            "ready_mapping_count": 12,
            "migration_map_coverage_percent": 97.7,
            "migration_rows": [
                {
                    "sheet_tab": "GEM_TRACKING",
                    "runtime_layer": "GEM_TRACKING",
                    "python_binding": "mvp_qaic_py/demo.py",
                    "nicegui_route": "/gem-tracking",
                    "migration_status": "PYTHON_READY_SHEETS_DRY_RUN_READY",
                    "migration_percent": 100,
                    "next_action": "KEEP",
                }
            ],
            "python_module_rows": [
                {
                    "module": "mvp_qaic_py/demo.py",
                    "function_count": 2,
                    "functions": "a;b",
                    "migration_role": "DEMO",
                }
            ],
            "apps_script_source_rows": [
                {
                    "source_path": "apps_script/Code.gs",
                    "source_type": "GS",
                    "function_count": 1,
                    "functions": "run",
                    "migration_status": "DISCOVERED_READONLY",
                    "next_action": "MAP",
                }
            ],
        }

    def fake_real_case(project_root: Path) -> dict[str, object]:
        return {
            "input_status": "WAITING",
            "capture_count": 0,
            "response_count": 0,
            "ready_for_review": False,
            "recommended_next": "WAIT",
        }

    monkeypatch.setattr(p200r2, "build_visual_ux_polish", fake_ux)
    monkeypatch.setattr(
        p200r2, "build_apps_script_sheets_function_tab_migration_map", fake_migration
    )
    monkeypatch.setattr(p200r2, "build_real_case_portfolio_gem_inputs", fake_real_case)

    payload = p200r2.build_deep_operator_cockpit(tmp_path)

    assert payload["release_status"] == "LOCAL_PRIVATE_OPERATOR_RELEASE_READY_WITH_DEEP_COCKPITS"
    assert payload["migration_control_row_count"] >= 4
    assert payload["instruction_row_count"] >= 8
    assert all(row["color_cell"] for row in payload["migration_control_rows"])
    assert payload["google_sheets_write"] is False
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_export_deep_cockpit_writes_outputs(monkeypatch, tmp_path: Path) -> None:
    def fake_ux(project_root: Path) -> dict[str, object]:
        return {
            "nicegui_tab_count": 9,
            "roadmap_step_count": 15,
            "post_python_step_count": 4,
            "nicegui_tab_rows": [],
            "top_visual_planning_rows": [
                {
                    "order": 1,
                    "period": "PASSÉ",
                    "step_count": 5,
                    "avg_progress_percent": 98.0,
                    "main_status": "DONE",
                    "main_route": "/migration",
                }
            ],
        }

    def fake_migration(project_root: Path) -> dict[str, object]:
        return {
            "sheet_tab_count": 13,
            "ready_mapping_count": 12,
            "migration_map_coverage_percent": 97.7,
            "migration_rows": [],
            "python_module_rows": [],
            "apps_script_source_rows": [],
        }

    def fake_real_case(project_root: Path) -> dict[str, object]:
        return {
            "input_status": "WAITING",
            "capture_count": 0,
            "response_count": 0,
            "ready_for_real_case_review": False,
            "recommended_next": "WAIT",
        }

    monkeypatch.setattr(p200r2, "build_visual_ux_polish", fake_ux)
    monkeypatch.setattr(
        p200r2, "build_apps_script_sheets_function_tab_migration_map", fake_migration
    )
    monkeypatch.setattr(p200r2, "build_real_case_portfolio_gem_inputs", fake_real_case)

    export_dir = tmp_path / "05_EXPORTS" / "P200R2_TEST"
    payload = p200r2.export_deep_operator_cockpit(tmp_path, export_dir=export_dir)

    assert payload["instruction_row_count"] >= 8
    assert (export_dir / "P200R2_DEEP_COCKPIT_UX_INSTRUCTIONS.json").exists()
    assert (export_dir / "P200R2_RELEASE_ROWS.csv").exists()
    assert (export_dir / "P200R2_GLOBAL_PLANNING.csv").exists()
    assert (export_dir / "P200R2_MIGRATION_CONTROL.csv").exists()
    assert (export_dir / "P200R2_INSTRUCTIONS_TRACKER.csv").exists()
    assert (export_dir / "P200R2_SUMMARY.json").exists()
    assert (export_dir / "P200R2_REPORT.md").exists()
