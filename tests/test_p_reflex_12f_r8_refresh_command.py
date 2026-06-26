from __future__ import annotations

from pathlib import Path


def test_p12f_r8_refresh_command_exists_and_is_no_scan() -> None:
    repo = Path(__file__).resolve().parents[1]
    script = repo / "scripts" / "RUN_P_REFLEX_12F_REFRESH_GLOBAL_MIGRATION_MATRIX.ps1"
    assert script.exists()
    text = script.read_text(encoding="utf-8")
    assert "migration_global_matrix" in text
    assert "--write" in text
    assert "MIGRATION_GLOBAL_MATRIX_SUMMARY.json" in text
    assert "Get-ChildItem" not in text
    assert "Q:\\" not in text


def test_p12f_r8_refresh_command_keeps_mission_control_as_entrypoint() -> None:
    repo = Path(__file__).resolve().parents[1]
    panel = repo / "mvp_qaic_reflex_ui" / "mission_control_auto_update_panel.py"
    detail = repo / "mvp_qaic_reflex_ui" / "global_migration_page.py"
    assert panel.exists()
    assert detail.exists()
    text = panel.read_text(encoding="utf-8")
    assert (
        "MIGRATION_GLOBAL_MATRIX_SUMMARY" in text or "MIGRATION_GLOBAL_MATRIX_SUMMARY.json" in text
    )
    assert "/migration/global" in text
