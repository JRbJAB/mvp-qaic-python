"""Runtime-free screen model for CDC + Dev Tracker."""

from __future__ import annotations

from dataclasses import asdict

from mvp_qaic_reflex_ui.cdc_dev_tracker_migration_style import (
    TRACKER_COLUMNS,
    TrackerRow,
    default_tracker_rows,
    migration_style_contract,
    tracker_summary,
)

SCREEN_ROUTE = "/cdc-dev-tracker"
SCREEN_TITLE = "CDC + Dev Tracker"


def _row_to_dict(row: TrackerRow) -> dict[str, str]:
    return asdict(row)


def build_cdc_dev_tracker_screen_model() -> dict[str, object]:
    """Build a UI-ready model without starting Reflex."""

    rows = default_tracker_rows()
    row_dicts = [_row_to_dict(row) for row in rows]
    return {
        "route": SCREEN_ROUTE,
        "title": SCREEN_TITLE,
        "ui_style_source": "MIGRATION_TRACKER",
        "style_contract": migration_style_contract(),
        "summary_kpi_bar": tracker_summary(rows),
        "filter_bar": {
            "enabled": True,
            "fields": ["tracker_kind", "status", "priority", "owner"],
        },
        "columns": list(TRACKER_COLUMNS),
        "rows": row_dicts,
        "detail_panel": {
            "enabled": True,
            "default_tracker_id": row_dicts[0]["tracker_id"] if row_dicts else "",
        },
        "next_actions_panel": {
            "enabled": True,
            "items": [row["next_action"] for row in row_dicts],
        },
        "qait_handoff_guard": {
            "required": True,
            "status": "FULLY_APPROVED_AND_GITIGNORE_RESOLVED",
        },
    }


def screen_route() -> str:
    """Return the intended route for future Reflex registration."""

    return SCREEN_ROUTE
