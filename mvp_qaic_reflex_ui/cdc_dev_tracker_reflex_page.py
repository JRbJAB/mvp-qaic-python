"""Real CDC + Dev Tracker cockpit for MVP QAIC Reflex.

V25_CDC_DELIVERY_TRACKER_COCKPIT
Source: static export of 📊 V25_CDC_DELIVERY_TRACKER.
No broker, no order, no sizing, no Sheet/BQ write.
"""

from __future__ import annotations

from typing import Any

import reflex as rx

from .layout import page_shell
from .common.tracker_reflex_kit import tracker_body, tracker_items_from_rows
from .dev_lifecycle_tracker import (
    cdc_lifecycle_tracker_panel as _r6n_vertical_cdc_lifecycle_tracker_panel,
    dev_lifecycle_tracker_panel as _r6m_r7_dev_lifecycle_tracker_panel,
)
from .v25_cdc_delivery_tracker_static import (
    DETAIL_ROWS,
    REAL_COCKPIT_MARKER,
    SOURCE_SHEET,
    SUMMARY_ROWS,
    cdc_kpis,
    critical_detail_rows,
    pct_value,
)

_STATUS_STYLES: dict[str, dict[str, str]] = {
    "DONE": {"bg": "#dcfce7", "fg": "#166534", "border": "#86efac"},
    "REVIEW": {"bg": "#fff7ed", "fg": "#c2410c", "border": "#fdba74"},
    "MISSING": {"bg": "#fee2e2", "fg": "#991b1b", "border": "#fca5a5"},
    "BLOCKED": {"bg": "#fee2e2", "fg": "#991b1b", "border": "#ef4444"},
    "PLANNED": {"bg": "#dbeafe", "fg": "#1d4ed8", "border": "#93c5fd"},
    "ON_TRACK": {"bg": "#dcfce7", "fg": "#166534", "border": "#86efac"},
    "WATCH": {"bg": "#fff7ed", "fg": "#c2410c", "border": "#fdba74"},
}

GRID_PHASES = "92px minmax(270px, 1.1fr) 92px 130px 110px 110px 130px minmax(260px, 1fr)"
GRID_DETAILS = "96px 70px 90px minmax(230px, 1fr) minmax(250px, 1fr) 120px 120px"


def _style_for(status: object) -> dict[str, str]:
    return _STATUS_STYLES.get(str(status), {"bg": "#f3f4f6", "fg": "#111827", "border": "#d1d5db"})


def _text(
    value: object,
    *,
    weight: str = "regular",
    size: str = "0.84em",
    opacity: str = "1",
    nowrap: bool = False,
) -> rx.Component:
    return rx.text(
        str(value),
        font_weight=weight,
        font_size=size,
        opacity=opacity,
        white_space="nowrap" if nowrap else "normal",
        overflow="hidden" if nowrap else "visible",
        text_overflow="ellipsis" if nowrap else "clip",
    )


def _status_pill(value: object) -> rx.Component:
    status = str(value or "REVIEW")
    style = _style_for(status)
    return rx.box(
        rx.text(status, font_weight="bold", font_size="0.74em", line_height="1"),
        background=style["bg"],
        color=style["fg"],
        border=f"1px solid {style['border']}",
        border_radius="999px",
        padding="0.28rem 0.58rem",
        width="fit-content",
    )


def _progress_bar(value: object, width: str = "118px") -> rx.Component:
    progress = pct_value(value)
    return rx.vstack(
        rx.text(f"{progress}%", font_weight="bold", font_size="0.86em"),
        rx.box(
            rx.box(
                height="100%", width=f"{progress}%", background="#2563eb", border_radius="999px"
            ),
            width=width,
            height="8px",
            background="var(--gray-a4)",
            border_radius="999px",
            overflow="hidden",
        ),
        spacing="1",
        align_items="start",
    )


def _kpi(label: str, value: object, detail: str = "") -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(label, font_size="0.76em", opacity="0.72"),
            rx.heading(str(value), size="4"),
            rx.text(detail, font_size="0.72em", opacity="0.72") if detail else rx.fragment(),
            spacing="1",
            align="start",
        ),
        padding="0.85rem",
        border="1px solid var(--gray-a4)",
        border_radius="14px",
        background="white",
        min_width="155px",
    )


def _phase_header() -> rx.Component:
    return rx.box(
        _text("Phase", weight="bold", size="0.76em", nowrap=True),
        _text("Nom", weight="bold", size="0.76em", nowrap=True),
        _text("Items", weight="bold", size="0.76em", nowrap=True),
        _text("Réalisé", weight="bold", size="0.76em", nowrap=True),
        _text("Done", weight="bold", size="0.76em", nowrap=True),
        _text("Review", weight="bold", size="0.76em", nowrap=True),
        _text("Reste h", weight="bold", size="0.76em", nowrap=True),
        _text("Next action", weight="bold", size="0.76em", nowrap=True),
        display="grid",
        grid_template_columns=GRID_PHASES,
        column_gap="0.9rem",
        align_items="center",
        min_width="1200px",
        padding="0.65rem 0.75rem",
        background="var(--gray-a2)",
        border_bottom="1px solid var(--gray-a4)",
        position="sticky",
        top="0",
        z_index="1",
    )


def _phase_row(row: dict[str, Any]) -> rx.Component:
    blocked = str(row.get("blocked", "0")).replace(",", ".")
    status = (
        "BLOCKED"
        if blocked not in ("", "0", "0.0", "0,0%") and row.get("phase_id") != "TOTAL"
        else "REVIEW"
    )
    if str(row.get("remaining_h", "0")).replace(",", ".") in ("0", "0.0", "0.00"):
        status = "DONE"
    return rx.box(
        _text(row.get("phase_id", ""), weight="bold", size="0.78em", nowrap=True),
        rx.vstack(
            _text(row.get("phase_name", ""), weight="medium", size="0.83em"),
            _status_pill(status),
            spacing="1",
            align="start",
        ),
        _text(row.get("items", ""), size="0.8em", nowrap=True),
        _progress_bar(row.get("realized_pct", "0")),
        _text(row.get("done", ""), size="0.8em", nowrap=True),
        _text(row.get("review", ""), size="0.8em", nowrap=True),
        _text(row.get("remaining_h", ""), weight="bold", size="0.8em", nowrap=True),
        _text(row.get("next_action", ""), size="0.78em"),
        display="grid",
        grid_template_columns=GRID_PHASES,
        column_gap="0.9rem",
        align_items="center",
        min_width="1200px",
        padding="0.65rem 0.75rem",
        border_bottom="1px solid var(--gray-a4)",
    )


def _details_header() -> rx.Component:
    return rx.box(
        _text("Statut", weight="bold", size="0.76em", nowrap=True),
        _text("Prio", weight="bold", size="0.76em", nowrap=True),
        _text("Phase", weight="bold", size="0.76em", nowrap=True),
        _text("Module", weight="bold", size="0.76em", nowrap=True),
        _text("Livrable", weight="bold", size="0.76em", nowrap=True),
        _text("Progress", weight="bold", size="0.76em", nowrap=True),
        _text("Reste h", weight="bold", size="0.76em", nowrap=True),
        display="grid",
        grid_template_columns=GRID_DETAILS,
        column_gap="0.9rem",
        align_items="center",
        min_width="1080px",
        padding="0.65rem 0.75rem",
        background="var(--gray-a2)",
        border_bottom="1px solid var(--gray-a4)",
        position="sticky",
        top="0",
        z_index="1",
    )


def _detail_row(row: dict[str, Any]) -> rx.Component:
    return rx.box(
        _status_pill(row.get("decision_status", "REVIEW")),
        _text(row.get("priority", ""), weight="bold", size="0.78em", nowrap=True),
        _text(row.get("phase_id", ""), size="0.78em", nowrap=True),
        rx.vstack(
            _text(row.get("module_name", ""), weight="medium"),
            _text(row.get("module_id", ""), size="0.72em", opacity="0.68"),
            spacing="1",
            align="start",
        ),
        _text(row.get("deliverable_name", ""), size="0.78em"),
        _progress_bar(row.get("realized_pct", "0"), width="96px"),
        _text(row.get("remaining_effort_hours", ""), weight="bold", size="0.78em", nowrap=True),
        display="grid",
        grid_template_columns=GRID_DETAILS,
        column_gap="0.9rem",
        align_items="center",
        min_width="1080px",
        padding="0.65rem 0.75rem",
        border_bottom="1px solid var(--gray-a4)",
    )


def _phase_table() -> rx.Component:
    return rx.box(
        rx.vstack(
            _phase_header(), *[_phase_row(row) for row in SUMMARY_ROWS], width="100%", spacing="0"
        ),
        width="100%",
        overflow_x="auto",
        border="1px solid var(--gray-a4)",
        border_radius="14px",
        background="white",
    )


def _priority_table() -> rx.Component:
    rows = critical_detail_rows(16)
    return rx.box(
        rx.vstack(
            _details_header(), *[_detail_row(row) for row in rows], width="100%", spacing="0"
        ),
        width="100%",
        overflow_x="auto",
        border="1px solid var(--gray-a4)",
        border_radius="14px",
        background="white",
    )


def cdc_dev_tracker_cockpit_body(view: str = "combined") -> rx.Component:
    kpis = cdc_kpis()
    cdc_items = tracker_items_from_rows(
        SUMMARY_ROWS,
        id_keys=("phase_id",),
        title_keys=("phase_name",),
        percent_keys=("realized_num", "realized_pct"),
        status_key="status",
        description_keys=("next_action",),
        route="/cdc-tracker",
        default_priority="P0",
    )
    dev_items = tracker_items_from_rows(
        critical_detail_rows(16),
        id_keys=("module_id", "phase_id"),
        title_keys=("deliverable_name", "module_name"),
        percent_keys=("realized_pct",),
        status_key="decision_status",
        description_keys=("module_name", "deliverable_name"),
        route="/dev-tracking",
        default_priority="P1",
    )
    source_detail = (
        f"{REAL_COCKPIT_MARKER} · {SOURCE_SHEET} · "
        f"{len(SUMMARY_ROWS)} CDC phases · {len(DETAIL_ROWS)} detail rows · "
        "No Sheet/BQ write, no trigger, no broker/order/sizing."
    )
    return tracker_body(
        cdc_items=cdc_items,
        dev_items=dev_items,
        source_label=(
            "V25 CDC delivery tracker rendered through the UI common tracker kit. "
            f"Global {kpis['realized_pct']} realized, status {kpis['status']}."
        ),
        source_detail=source_detail,
        view=view,
    )


def cdc_dev_tracker_reflex_page() -> rx.Component:
    return page_shell(
        "📊 CDC + Dev Tracker",
        "Cockpit réel basé sur V25_CDC_DELIVERY_TRACKER : progression, phases, priorités et reste à migrer.",
        cdc_dev_tracker_cockpit_body("combined"),
        "/cdc-dev-tracker",
    )


def cdc_tracker_reflex_page() -> rx.Component:
    return page_shell(
        "📊 CDC Tracker",
        "Suivi CDC réel : phases, % réalisé, reste à faire et critical path.",
        cdc_dev_tracker_cockpit_body("cdc"),
        "/cdc-tracker",
    )


def dev_tracking_reflex_page() -> rx.Component:
    return page_shell(
        "🧭 Dev Tracking",
        "Priorités de migration Sheets / Apps Script → Reflex issues du tracker V25.",
        cdc_dev_tracker_cockpit_body("dev"),
        "/dev-tracking",
    )


# BEGIN_R6M_R7_AUTO_LIVE_CDC_LIFECYCLE_PANEL
try:
    import reflex as _r6m_r7_rx
except Exception:  # pragma: no cover - Reflex optional in unit tests
    _r6m_r7_rx = None

_r6m_r7_base_cdc_dev_tracker_reflex_page = cdc_dev_tracker_reflex_page
_r6m_r7_base_cdc_tracker_reflex_page = cdc_tracker_reflex_page


def _r6m_r7_with_lifecycle(base_page):
    panel = _r6m_r7_dev_lifecycle_tracker_panel(compact=True)
    base = base_page()
    if _r6m_r7_rx is None:
        return {"lifecycle": panel, "cdc": base}
    return _r6m_r7_rx.vstack(panel, base, spacing="4", align="stretch", width="100%")


def cdc_dev_tracker_reflex_page():
    return _r6m_r7_with_lifecycle(_r6m_r7_base_cdc_dev_tracker_reflex_page)


def cdc_tracker_reflex_page():
    return _r6m_r7_with_lifecycle(_r6m_r7_base_cdc_tracker_reflex_page)


# END_R6M_R7_AUTO_LIVE_CDC_LIFECYCLE_PANEL

# R6N-R5_BEGIN_VERTICAL_MIGRATION_STYLE_CDC_TRACKER
_r6n_original_cdc_dev_tracker_reflex_page = cdc_dev_tracker_reflex_page
_r6n_original_cdc_tracker_reflex_page = cdc_tracker_reflex_page


def cdc_dev_tracker_reflex_page() -> Any:
    base = _r6n_original_cdc_dev_tracker_reflex_page()
    if rx is None:
        return {
            "lifecycle": _r6n_vertical_cdc_lifecycle_tracker_panel(compact=False),
            "base": base,
        }
    return rx.vstack(
        _r6n_vertical_cdc_lifecycle_tracker_panel(compact=False),
        base,
        spacing="4",
        align="stretch",
        width="100%",
    )


def cdc_tracker_reflex_page() -> Any:
    base = _r6n_original_cdc_tracker_reflex_page()
    if rx is None:
        return {
            "lifecycle": _r6n_vertical_cdc_lifecycle_tracker_panel(compact=False),
            "base": base,
        }
    return rx.vstack(
        _r6n_vertical_cdc_lifecycle_tracker_panel(compact=False),
        base,
        spacing="4",
        align="stretch",
        width="100%",
    )


# R6N-R5_END_VERTICAL_MIGRATION_STYLE_CDC_TRACKER
