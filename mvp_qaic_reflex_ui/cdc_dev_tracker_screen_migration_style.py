"""CDC + Dev Tracker screen model using the Migration Tracker UI contract.

Runtime-free by default. The module builds a deterministic view model that can
be wired into Reflex without broker/order/sizing/Sheet/BQ side effects.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from mvp_qaic_reflex_ui.cdc_dev_tracker_migration_style import (
    MIGRATION_TRACKER_STYLE_CONTRACT,
    TRACKER_COLUMNS,
    default_tracker_rows,
)

SCREEN_ROUTE = "/cdc-dev-tracker"
SCREEN_TITLE = "CDC + Dev Tracker"
SCREEN_STYLE_SOURCE = "MIGRATION_TRACKER"

SCREEN_SECTIONS = (
    "SUMMARY_KPI_BAR",
    "FILTER_BAR",
    "CDC_TRACKER_TABLE",
    "DEV_TRACKER_TABLE",
    "DETAIL_PANEL",
    "NEXT_ACTIONS_PANEL",
)


def _row_to_dict(row: object) -> dict[str, str]:
    if isinstance(row, dict):
        return {str(key): str(value) for key, value in row.items()}
    to_dict = getattr(row, "to_dict", None)
    if callable(to_dict):
        return {str(key): str(value) for key, value in to_dict().items()}
    raw = getattr(row, "__dict__", {})
    return {str(key): str(value) for key, value in raw.items()}


def _rows() -> list[dict[str, str]]:
    return [_row_to_dict(row) for row in default_tracker_rows()]


def _by_kind(rows: list[dict[str, str]], tracker_kind: str) -> list[dict[str, str]]:
    return [row for row in rows if row["tracker_kind"] == tracker_kind]


def build_summary_kpi_bar(rows: list[dict[str, str]]) -> dict[str, Any]:
    """Build summary cards aligned with the migration tracker layout."""

    status_counts = Counter(row["status"] for row in rows)
    kind_counts = Counter(row["tracker_kind"] for row in rows)
    return {
        "total_rows": len(rows),
        "cdc_rows": kind_counts.get("CDC_TRACKER", 0),
        "dev_rows": kind_counts.get("DEV_TRACKER", 0),
        "blocked_rows": status_counts.get("BLOCKED", 0),
        "review_rows": status_counts.get("REVIEW", 0),
        "done_rows": status_counts.get("DONE", 0),
    }


def build_filter_bar(rows: list[dict[str, str]]) -> dict[str, list[str]]:
    """Return deterministic filter values for the tracker screen."""

    return {
        "tracker_kind": sorted({row["tracker_kind"] for row in rows}),
        "domain": sorted({row["domain"] for row in rows}),
        "status": sorted({row["status"] for row in rows}),
        "priority": sorted({row["priority"] for row in rows}),
        "owner": sorted({row["owner"] for row in rows}),
    }


def choose_detail_row(
    rows: list[dict[str, str]], selected_tracker_id: str | None = None
) -> dict[str, str]:
    """Select a detail row with REVIEW/BLOCKED priority when no id is supplied."""

    if selected_tracker_id:
        for row in rows:
            if row["tracker_id"] == selected_tracker_id:
                return row

    for status in ("BLOCKED", "REVIEW", "IN_PROGRESS", "TODO", "DONE"):
        for row in rows:
            if row["status"] == status:
                return row

    return {}


def build_next_actions_panel(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Return actionable tracker rows in display order."""

    actionable_statuses = {"TODO", "IN_PROGRESS", "REVIEW", "BLOCKED"}
    return [
        {
            "tracker_id": row["tracker_id"],
            "status": row["status"],
            "priority": row["priority"],
            "next_action": row["next_action"],
        }
        for row in rows
        if row["status"] in actionable_statuses
    ]


def build_cdc_dev_tracker_screen_model(
    selected_tracker_id: str | None = None,
) -> dict[str, Any]:
    """Build the full CDC + Dev Tracker screen model."""

    rows = _rows()
    return {
        "screen_route": SCREEN_ROUTE,
        "screen_title": SCREEN_TITLE,
        "ui_style_source": SCREEN_STYLE_SOURCE,
        "migration_tracker_style_contract": MIGRATION_TRACKER_STYLE_CONTRACT,
        "sections": list(SCREEN_SECTIONS),
        "columns": list(TRACKER_COLUMNS),
        "summary_kpi_bar": build_summary_kpi_bar(rows),
        "filter_bar": build_filter_bar(rows),
        "cdc_tracker_table": _by_kind(rows, "CDC_TRACKER"),
        "dev_tracker_table": _by_kind(rows, "DEV_TRACKER"),
        "detail_panel": choose_detail_row(rows, selected_tracker_id),
        "next_actions_panel": build_next_actions_panel(rows),
        "qait_handoff_guard": {
            "required": True,
            "status": "FULLY_APPROVED_AND_GITIGNORE_RESOLVED",
        },
        "runtime_free_default": True,
        "no_broker_order_sizing": True,
        "no_sheet_bq_write": True,
    }


def assert_screen_contract(model: dict[str, Any]) -> None:
    """Raise AssertionError if the screen contract is incomplete."""

    required_sections = set(SCREEN_SECTIONS)
    actual_sections = set(model.get("sections", []))
    missing_sections = required_sections - actual_sections
    if missing_sections:
        raise AssertionError(f"Missing sections: {sorted(missing_sections)}")

    if model.get("ui_style_source") != SCREEN_STYLE_SOURCE:
        raise AssertionError("Screen must use the Migration Tracker style source")

    if model.get("screen_route") != SCREEN_ROUTE:
        raise AssertionError("Unexpected CDC + Dev Tracker screen route")
