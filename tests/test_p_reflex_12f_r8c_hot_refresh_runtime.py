from __future__ import annotations

from pathlib import Path


def test_p12f_r8c_refresh_command_syncs_runtime_and_hot_reload() -> None:
    repo = Path(__file__).resolve().parents[1]
    script = repo / "scripts" / "RUN_P_REFLEX_12F_REFRESH_GLOBAL_MIGRATION_MATRIX.ps1"
    text = script.read_text(encoding="utf-8")
    assert "RuntimeRoot" in text
    assert "SYNC RUNTIME DOCS FOR PAGE REFRESH" in text
    assert "RUNTIME_SYNC_OK=True" in text
    assert "HOT_RELOAD_TOUCH_OK" in text
    assert "mission_control_auto_update_panel.py" in text
    assert "NO_SERVER_RESTART_BROWSER_REFRESH_AFTER_HOT_RELOAD" in text


def test_p12f_r8c_no_new_mission_control_panel_and_detail_route_only() -> None:
    repo = Path(__file__).resolve().parents[1]
    source = (repo / "mvp_qaic_reflex_ui" / "mission_control_auto_update_panel.py").read_text(
        encoding="utf-8"
    )
    assert "migration_global_matrix_existing_list_rows" in source
    assert "/migration/global" in source
    assert "new_mission_control_panel" not in source.lower()
