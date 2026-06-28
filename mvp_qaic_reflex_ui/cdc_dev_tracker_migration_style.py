"""CDC + Dev Tracker contract using the Migration Tracker visual contract.

This module is runtime-free and side-effect free. It provides a stable data
contract that can be consumed by Reflex UI modules without launching Reflex.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

TrackerKind = Literal["CDC_TRACKER", "DEV_TRACKER"]
TrackerStatus = Literal["TODO", "IN_PROGRESS", "REVIEW", "BLOCKED", "DONE"]

MIGRATION_TRACKER_STYLE_CONTRACT: dict[str, object] = {
    "ui_style_source": "MIGRATION_TRACKER",
    "same_columns": True,
    "summary_kpi_bar": True,
    "filter_bar": True,
    "tracker_table": True,
    "detail_panel": True,
    "next_actions_panel": True,
    "operator_review_required": True,
}

TRACKER_COLUMNS: tuple[str, ...] = (
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
)


@dataclass(frozen=True)
class TrackerRow:
    """One CDC or development tracker row."""

    tracker_id: str
    tracker_kind: TrackerKind
    domain: str
    scope: str
    source: str
    target: str
    status: TrackerStatus
    priority: str
    owner: str
    evidence: str
    next_action: str


def default_tracker_rows() -> list[TrackerRow]:
    """Return initial rows for the CDC + Dev Tracker screen."""

    return [
        TrackerRow(
            tracker_id="CDC-001",
            tracker_kind="CDC_TRACKER",
            domain="MVP_UI",
            scope="CDC + Dev Tracker",
            source="Migration Tracker visual contract",
            target="CDC tracker table",
            status="IN_PROGRESS",
            priority="HIGH",
            owner="operator",
            evidence="MVP_UI_CDC_DEV_TRACKER_MIGRATION_STYLE_R1G_STATUS.json",
            next_action="Wire navigation and runtime smoke.",
        ),
        TrackerRow(
            tracker_id="DEV-001",
            tracker_kind="DEV_TRACKER",
            domain="MVP_UI",
            scope="Reflex screen",
            source="cdc_dev_tracker_screen_migration_style.py",
            target="/cdc-dev-tracker",
            status="REVIEW",
            priority="HIGH",
            owner="developer",
            evidence="MVP_UI_CDC_DEV_TRACKER_SCREEN_MIGRATION_STYLE_R2D_STATUS.json",
            next_action="Attach the screen to navigation safely.",
        ),
    ]


def tracker_rows_as_dicts() -> list[dict[str, str]]:
    """Return tracker rows as dictionaries for UI rendering and JSON samples."""

    return [asdict(row) for row in default_tracker_rows()]


def tracker_summary(rows: list[TrackerRow] | None = None) -> dict[str, int]:
    """Return KPI counts compatible with the Migration Tracker summary bar."""

    selected_rows = rows if rows is not None else default_tracker_rows()
    total = len(selected_rows)
    done = sum(1 for row in selected_rows if row.status == "DONE")
    blocked = sum(1 for row in selected_rows if row.status == "BLOCKED")
    review = sum(1 for row in selected_rows if row.status == "REVIEW")
    in_progress = sum(1 for row in selected_rows if row.status == "IN_PROGRESS")
    return {
        "total": total,
        "done": done,
        "blocked": blocked,
        "review": review,
        "in_progress": in_progress,
    }


def migration_style_contract() -> dict[str, object]:
    """Return a copy of the UI style contract."""

    return dict(MIGRATION_TRACKER_STYLE_CONTRACT)
