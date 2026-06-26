from pathlib import Path


def test_p12f_r7_enriches_existing_mission_control_list_without_new_panel() -> None:
    source = Path("mvp_qaic_reflex_ui/mission_control_auto_update_panel.py").read_text(
        encoding="utf-8"
    )
    assert "P12F_R7_ENRICH_EXISTING_MC_LIST_FIXED" in source
    assert "migration_global_matrix_existing_list_rows" in source
    assert "MIGRATION_GLOBAL_MATRIX_SUMMARY.json" in source
    assert "global_matrix_rows" in source
    assert "sheets_cockpits" in source
    assert "apps_script_functions" in source
    assert "/migration/global" in source
    assert "new_mission_control_panel" not in source.lower()


def test_p12f_r7_keeps_global_detail_route_as_drilldown_only() -> None:
    app_source = Path("mvp_qaic_reflex_ui/mvp_qaic_reflex_ui.py").read_text(encoding="utf-8")
    assert "/migration/global" in app_source
    mc_source = Path("mvp_qaic_reflex_ui/mission_control_auto_update_panel.py").read_text(
        encoding="utf-8"
    )
    assert "Ouvrir le detail de la matrice migration" in mc_source
