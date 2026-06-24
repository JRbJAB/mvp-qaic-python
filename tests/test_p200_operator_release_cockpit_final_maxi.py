from __future__ import annotations

from pathlib import Path

import mvp_qaic_py.p200_operator_release_cockpit_final_maxi as p200


def test_p200_release_ready_when_dependencies_ready(monkeypatch, tmp_path: Path) -> None:
    def fake_ux(project_root: Path) -> dict[str, object]:
        return {
            "nicegui_tab_count": 9,
            "roadmap_step_count": 15,
            "post_python_step_count": 4,
            "sheet_tab_count": 13,
            "ready_mapping_count": 12,
            "migration_coverage_percent": 97.7,
        }

    def fake_real_case(project_root: Path) -> dict[str, object]:
        return {
            "input_status": "WAITING_OPERATOR_CAPTURE_AND_GEM_RESPONSE",
            "capture_count": 0,
            "response_count": 0,
            "ready_for_real_case_review": False,
            "recommended_next": "WAIT_OPERATOR_CAPTURE_AND_GEM_RESPONSE_THEN_RERUN_P196",
        }

    monkeypatch.setattr(p200, "build_visual_ux_polish", fake_ux)
    monkeypatch.setattr(p200, "build_real_case_portfolio_gem_inputs", fake_real_case)

    payload = p200.build_operator_release_cockpit_final(tmp_path)

    assert payload["release_status"] == "LOCAL_PRIVATE_OPERATOR_RELEASE_READY"
    assert payload["nicegui_tab_count"] == 9
    assert payload["blocker_count"] == 0
    assert payload["google_sheets_write"] is False
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_p200_release_review_when_coverage_low(monkeypatch, tmp_path: Path) -> None:
    def fake_ux(project_root: Path) -> dict[str, object]:
        return {
            "nicegui_tab_count": 9,
            "roadmap_step_count": 15,
            "post_python_step_count": 4,
            "sheet_tab_count": 13,
            "ready_mapping_count": 8,
            "migration_coverage_percent": 80.0,
        }

    def fake_real_case(project_root: Path) -> dict[str, object]:
        return {
            "input_status": "WAITING",
            "capture_count": 0,
            "response_count": 0,
            "ready_for_real_case_review": False,
            "recommended_next": "WAIT",
        }

    monkeypatch.setattr(p200, "build_visual_ux_polish", fake_ux)
    monkeypatch.setattr(p200, "build_real_case_portfolio_gem_inputs", fake_real_case)

    payload = p200.build_operator_release_cockpit_final(tmp_path)

    assert payload["release_status"] == "RELEASE_REVIEW_REQUIRED"
    assert "MIGRATION_COVERAGE_BELOW_95" in payload["blockers"]


def test_p200_export_writes_expected_files(monkeypatch, tmp_path: Path) -> None:
    def fake_ux(project_root: Path) -> dict[str, object]:
        return {
            "nicegui_tab_count": 9,
            "roadmap_step_count": 15,
            "post_python_step_count": 4,
            "sheet_tab_count": 13,
            "ready_mapping_count": 12,
            "migration_coverage_percent": 97.7,
        }

    def fake_real_case(project_root: Path) -> dict[str, object]:
        return {
            "input_status": "WAITING",
            "capture_count": 0,
            "response_count": 0,
            "ready_for_real_case_review": False,
            "recommended_next": "WAIT",
        }

    monkeypatch.setattr(p200, "build_visual_ux_polish", fake_ux)
    monkeypatch.setattr(p200, "build_real_case_portfolio_gem_inputs", fake_real_case)

    export_dir = tmp_path / "05_EXPORTS" / "P200_TEST"
    payload = p200.export_operator_release_cockpit_final(tmp_path, export_dir=export_dir)

    assert payload["release_status"] == "LOCAL_PRIVATE_OPERATOR_RELEASE_READY"
    assert (export_dir / "P200_OPERATOR_RELEASE_COCKPIT_FINAL.json").exists()
    assert (export_dir / "P200_RELEASE_ROWS.csv").exists()
    assert (export_dir / "P200_DECISIONS.csv").exists()
    assert (export_dir / "P200_SUMMARY.json").exists()
    assert (export_dir / "P200_REPORT.md").exists()
