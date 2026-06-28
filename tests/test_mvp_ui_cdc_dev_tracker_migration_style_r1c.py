from mvp_qaic_reflex_ui.cdc_dev_tracker_migration_style import (
    REQUIRED_QAIT_HANDOFF_FILES,
    TRACKER_COLUMNS,
    UI_STYLE_SOURCE,
    build_tracker_view_model,
    default_tracker_rows,
    validate_migration_tracker_style_contract,
)


def test_migration_tracker_style_contract_is_forced() -> None:
    model = build_tracker_view_model()

    assert UI_STYLE_SOURCE == "MIGRATION_TRACKER"
    assert model["ui_style_source"] == "MIGRATION_TRACKER"
    assert model["style_contract"]["same_columns"] is True
    assert model["style_contract"]["summary_kpi_bar"] is True
    assert model["style_contract"]["filter_bar"] is True
    assert model["style_contract"]["tracker_table"] is True
    assert model["style_contract"]["detail_panel"] is True
    assert model["style_contract"]["next_actions_panel"] is True
    assert validate_migration_tracker_style_contract() is True


def test_tracker_columns_match_expected_migration_tracker_shape() -> None:
    model = build_tracker_view_model()

    assert model["columns"] == TRACKER_COLUMNS
    assert "tracker_id" in TRACKER_COLUMNS
    assert "tracker_kind" in TRACKER_COLUMNS
    assert "next_action" in TRACKER_COLUMNS


def test_default_rows_cover_cdc_and_dev_tracker() -> None:
    rows = default_tracker_rows()
    kinds = {row.tracker_kind for row in rows}
    model = build_tracker_view_model(rows)

    assert kinds == {"CDC_TRACKER", "DEV_TRACKER"}
    assert model["summary"]["total"] == len(rows)
    assert model["summary"]["cdc"] >= 1
    assert model["summary"]["dev"] >= 1


def test_qait_handoff_files_are_explicit_source_of_truth() -> None:
    model = build_tracker_view_model()

    assert model["must_use_qait_handoff_files"] is True
    assert REQUIRED_QAIT_HANDOFF_FILES
    assert any("R13_STATUS" in path for path in REQUIRED_QAIT_HANDOFF_FILES)
    assert any("R15A_STATUS" in path for path in REQUIRED_QAIT_HANDOFF_FILES)
