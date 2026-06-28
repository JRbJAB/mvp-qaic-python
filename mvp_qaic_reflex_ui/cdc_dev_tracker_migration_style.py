from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

TrackerKind = Literal["CDC_TRACKER", "DEV_TRACKER"]
TrackerStatus = Literal["TODO", "IN_PROGRESS", "REVIEW", "BLOCKED", "DONE"]

MIGRATION_TRACKER_STYLE_CONTRACT = {
    "ui_style_source": "MIGRATION_TRACKER",
    "same_columns": True,
    "summary_kpi_bar": True,
    "filter_bar": True,
    "tracker_table": True,
    "detail_panel": True,
    "next_actions_panel": True,
    "operator_review_required": True,
}

TRACKER_COLUMNS = [
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


@dataclass(frozen=True)
class TrackerRow:
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

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def default_tracker_rows() -> list[TrackerRow]:
    return [
        TrackerRow(
            tracker_id="CDC-001",
            tracker_kind="CDC_TRACKER",
            domain="MVP_UI",
            scope="cdc_dev_tracker",
            source="migration_tracker_style",
            target="cdc_tracker_screen",
            status="IN_PROGRESS",
            priority="HIGH",
            owner="operator",
            evidence="MVP_UI_CDC_DEV_TRACKER_MIGRATION_STYLE_R1G",
            next_action="wire_reflex_screen",
        ),
        TrackerRow(
            tracker_id="DEV-001",
            tracker_kind="DEV_TRACKER",
            domain="MVP_UI",
            scope="developer_execution_tracker",
            source="migration_tracker_style",
            target="dev_tracker_screen",
            status="TODO",
            priority="HIGH",
            owner="developer",
            evidence="MVP_UI_CDC_DEV_TRACKER_MIGRATION_STYLE_R1G",
            next_action="connect_to_existing_ui_navigation",
        ),
        TrackerRow(
            tracker_id="CDC-002",
            tracker_kind="CDC_TRACKER",
            domain="QAIT_HANDOFF",
            scope="handoff_contract_usage",
            source="qait_handoff_files",
            target="operator_review_flow",
            status="REVIEW",
            priority="MEDIUM",
            owner="operator",
            evidence="QAIT_HANDOFF_APPROVED_OPERATOR_SEALED",
            next_action="validate_next_real_input_packet",
        ),
    ]


def tracker_table_rows(rows: list[TrackerRow] | None = None) -> list[dict[str, str]]:
    source_rows = rows if rows is not None else default_tracker_rows()
    return [row.to_dict() for row in source_rows]


def tracker_summary(rows: list[TrackerRow] | None = None) -> dict[str, int]:
    source_rows = rows if rows is not None else default_tracker_rows()
    summary = {
        "total": len(source_rows),
        "cdc_tracker": 0,
        "dev_tracker": 0,
        "todo": 0,
        "in_progress": 0,
        "review": 0,
        "blocked": 0,
        "done": 0,
    }
    for row in source_rows:
        if row.tracker_kind == "CDC_TRACKER":
            summary["cdc_tracker"] += 1
        if row.tracker_kind == "DEV_TRACKER":
            summary["dev_tracker"] += 1
        summary[row.status.lower()] += 1
    return summary


def filter_tracker_rows(
    *,
    tracker_kind: TrackerKind | None = None,
    status: TrackerStatus | None = None,
) -> list[TrackerRow]:
    rows = default_tracker_rows()
    if tracker_kind is not None:
        rows = [row for row in rows if row.tracker_kind == tracker_kind]
    if status is not None:
        rows = [row for row in rows if row.status == status]
    return rows


def migration_style_view_model() -> dict[str, object]:
    rows = default_tracker_rows()
    return {
        "contract": MIGRATION_TRACKER_STYLE_CONTRACT,
        "columns": TRACKER_COLUMNS,
        "summary": tracker_summary(rows),
        "rows": tracker_table_rows(rows),
        "detail_panel": {
            "enabled": True,
            "source": "selected_tracker_row",
        },
        "next_actions_panel": {
            "enabled": True,
            "source": "tracker_next_action",
        },
    }
