from __future__ import annotations

from mvp_qaic_reflex_ui.cdc_dev_tracker_migration_style import (
    MIGRATION_TRACKER_STYLE_CONTRACT,
    TRACKER_COLUMNS,
    filter_tracker_rows,
    migration_style_view_model,
    tracker_summary,
    tracker_table_rows,
)


def test_migration_tracker_style_contract_is_locked() -> None:
    assert MIGRATION_TRACKER_STYLE_CONTRACT["ui_style_source"] == "MIGRATION_TRACKER"
    assert MIGRATION_TRACKER_STYLE_CONTRACT["same_columns"] is True
    assert MIGRATION_TRACKER_STYLE_CONTRACT["summary_kpi_bar"] is True
    assert MIGRATION_TRACKER_STYLE_CONTRACT["filter_bar"] is True
    assert MIGRATION_TRACKER_STYLE_CONTRACT["tracker_table"] is True
    assert MIGRATION_TRACKER_STYLE_CONTRACT["detail_panel"] is True
    assert MIGRATION_TRACKER_STYLE_CONTRACT["next_actions_panel"] is True


def test_tracker_columns_match_expected_migration_style_shape() -> None:
    assert TRACKER_COLUMNS == [
        "tracker_id",
        "tracker_kind",
        "domain",
        "scope",
        "source",
        "target",
        "status",
        "priority",
        "owner",
        "evidence",
        "next_action",
    ]


def test_tracker_summary_counts_cdc_and_dev_rows() -> None:
    summary = tracker_summary()
    assert summary["total"] == 3
    assert summary["cdc_tracker"] == 2
    assert summary["dev_tracker"] == 1
    assert summary["in_progress"] == 1
    assert summary["todo"] == 1
    assert summary["review"] == 1


def test_filter_tracker_rows_and_table_rows_are_stable() -> None:
    dev_rows = filter_tracker_rows(tracker_kind="DEV_TRACKER")
    assert len(dev_rows) == 1
    assert dev_rows[0].tracker_id == "DEV-001"
    rows = tracker_table_rows(dev_rows)
    assert rows[0]["tracker_kind"] == "DEV_TRACKER"


def test_view_model_contains_migration_style_panels() -> None:
    view_model = migration_style_view_model()
    assert view_model["contract"] == MIGRATION_TRACKER_STYLE_CONTRACT
    assert view_model["columns"] == TRACKER_COLUMNS
    assert view_model["detail_panel"] == {
        "enabled": True,
        "source": "selected_tracker_row",
    }
    assert view_model["next_actions_panel"] == {
        "enabled": True,
        "source": "tracker_next_action",
    }
