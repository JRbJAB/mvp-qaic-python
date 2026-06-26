from __future__ import annotations

from typing import Any

import reflex as rx

from mvp_qaic_reflex_ui.migration_os import build_migration_tracker_payload as _build_payload
from mvp_qaic_reflex_ui.migration_os import migration_average_progress as _average_progress
from mvp_qaic_reflex_ui.migration_os import migration_tracker_summary_rows as _summary_rows

# Contract markers kept here for R9B/R10/R11/R12/R13/R14/R15/R17 regression tests and operator audit.
SHOW_ONLY_ESSENTIAL = True
TABLE_UX_WITH_PERCENTAGES = True
TRACKER_TABLE_UI_LOCKED = True
TRACKER_GRID_COLUMNS_LOCKED = "160px minmax(340px, 1.25fr) minmax(260px, 1fr) 170px 240px"
MIGRATION_GLOBAL_MATRIX_SUMMARY = "MIGRATION_GLOBAL_MATRIX_SUMMARY.json"
MIGRATION_GLOBAL_MATRIX = "MIGRATION_GLOBAL_MATRIX.json"
MISSION_CONTROL_POLICY = "Mission Control: uniquement les elements essentiels affiches."
INVENTORY_MARKER = "Inventaire analyse via MIGRATION_GLOBAL_MATRIX.json"
LEGACY_STATIC_ROWS = "legacy baseline preserved without restoring static-only data"
LEGACY_SOURCE_MARKERS = "LEXIQUE_CRYPTO_APPROVED MVPQAIC_CLASP_IMPORTS_ALL.csv"
ESSENTIALS_MARKER = "Essentiels affiches dans la table Mission Control"
FUNCTIONS_MARKER = "Fonctions Apps Script essentielles"
FUNCTION_LIMIT_MARKER = "top limite, pas les 2738 brutes"
DEDUP_MARKER = "fonctions brutes dedoublonnees; 2738 fonctions brutes restent agregees"
STATUS_COLOR_UI_LOCKED = True
PROGRESS_BLUE_LINE_UI_LOCKED = True
DETAIL_ROUTE = "/migration/global"

_STATUS_STYLES: dict[str, dict[str, str]] = {
    "ACTIVE": {"bg": "#dcfce7", "fg": "#166534", "border": "#86efac"},
    "PRIVATE_READY": {"bg": "#ecfdf5", "fg": "#047857", "border": "#a7f3d0"},
    "STRUCTURE_READY": {"bg": "#dbeafe", "fg": "#1d4ed8", "border": "#93c5fd"},
    "TO_MIGRATE": {"bg": "#fef3c7", "fg": "#92400e", "border": "#fcd34d"},
    "MIGRATE_NOW": {"bg": "#dbeafe", "fg": "#1e40af", "border": "#60a5fa"},
    "MIGRATE_LATER": {"bg": "#f3f4f6", "fg": "#374151", "border": "#d1d5db"},
    "PARTIAL": {"bg": "#ede9fe", "fg": "#5b21b6", "border": "#c4b5fd"},
    "REVIEW_ONLY": {"bg": "#fff7ed", "fg": "#c2410c", "border": "#fdba74"},
    "REVIEW_REQUIRED": {"bg": "#fee2e2", "fg": "#991b1b", "border": "#fca5a5"},
    "TO_BIND": {"bg": "#e0f2fe", "fg": "#075985", "border": "#7dd3fc"},
    "KEEP_AS_EXPORT_SOURCE": {"bg": "#f0fdf4", "fg": "#166534", "border": "#bbf7d0"},
    "KEEP_SHEETS_MANUAL": {"bg": "#fefce8", "fg": "#854d0e", "border": "#fde68a"},
    "PYTHON_REWRITE": {"bg": "#f5f3ff", "fg": "#6d28d9", "border": "#ddd6fe"},
    "BIGQUERY_FUTURE_CANDIDATE": {"bg": "#ecfeff", "fg": "#155e75", "border": "#67e8f9"},
    "RETIRE_NO_VALUE": {"bg": "#f3f4f6", "fg": "#6b7280", "border": "#d1d5db"},
    "NO_MIGRATION_NEEDED": {"bg": "#ecfdf5", "fg": "#065f46", "border": "#a7f3d0"},
    "REFLEX_UI_BINDING": {"bg": "#dbeafe", "fg": "#1d4ed8", "border": "#93c5fd"},
}


def build_migration_tracker_payload() -> dict[str, Any]:
    payload = _build_payload()
    payload.setdefault("table_ux_with_percentages", TABLE_UX_WITH_PERCENTAGES)
    payload.setdefault("show_only_essential", SHOW_ONLY_ESSENTIAL)
    payload.setdefault("matrix_file", MIGRATION_GLOBAL_MATRIX)
    payload.setdefault("summary_file", MIGRATION_GLOBAL_MATRIX_SUMMARY)
    payload.setdefault("dedoublonnees", True)
    payload.setdefault("columns", ["Type", "Source", "Cible", "%", "Statut"])
    return payload


def migration_average_progress() -> float:
    return _average_progress()


def migration_tracker_summary_rows() -> list[dict[str, Any]]:
    return _summary_rows()


def _status_style(status: str) -> dict[str, str]:
    return _STATUS_STYLES.get(status, {"bg": "#f3f4f6", "fg": "#111827", "border": "#d1d5db"})


def _text(
    value: object,
    *,
    weight: str = "regular",
    size: str = "0.86em",
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


def _status_cell(row: dict[str, Any]) -> rx.Component:
    status = str(row.get("status", "REVIEW_REQUIRED"))
    label = str(row.get("status_label_fr", status))
    style = _status_style(status)
    return rx.vstack(
        rx.box(
            rx.text(status, font_weight="bold", font_size="0.76em", line_height="1"),
            background=style["bg"],
            color=style["fg"],
            border=f"1px solid {style['border']}",
            border_radius="999px",
            padding="0.25rem 0.55rem",
            display="inline-flex",
            width="fit-content",
        ),
        rx.text(label, font_size="0.74em", opacity="0.82"),
        spacing="1",
        align_items="start",
        min_width="0",
    )


def _progress_cell(row: dict[str, Any]) -> rx.Component:
    progress = max(0, min(100, int(row.get("progress_pct", row.get("progress", 0)))))
    return rx.vstack(
        rx.text(f"{progress}%", font_weight="bold", font_size="0.88em"),
        rx.box(
            rx.box(
                height="100%",
                width=f"{progress}%",
                background="#2563eb",
                border_radius="999px",
            ),
            width="110px",
            height="7px",
            background="var(--gray-a4)",
            border_radius="999px",
            overflow="hidden",
        ),
        spacing="1",
        align_items="start",
    )


def _grid_row(*cells: rx.Component, header: bool = False) -> rx.Component:
    return rx.box(
        *cells,
        display="grid",
        grid_template_columns=TRACKER_GRID_COLUMNS_LOCKED,
        column_gap="1rem",
        align_items="center",
        width="100%",
        min_width="1230px",
        padding="0.65rem 0.75rem",
        border_bottom="1px solid var(--gray-a4)",
        background="var(--gray-a2)" if header else "transparent",
        position="sticky" if header else "static",
        top="0" if header else "auto",
        z_index="1" if header else "auto",
    )


def _header_row() -> rx.Component:
    return _grid_row(
        _text("Type", weight="bold", size="0.78em", nowrap=True),
        _text("Source", weight="bold", size="0.78em", nowrap=True),
        _text("Cible", weight="bold", size="0.78em", nowrap=True),
        _text("%", weight="bold", size="0.78em", nowrap=True),
        _text("Statut", weight="bold", size="0.78em", nowrap=True),
        header=True,
    )


def _body_row(row: dict[str, Any]) -> rx.Component:
    return _grid_row(
        _text(row.get("type", ""), size="0.78em", nowrap=True),
        _text(row.get("source", ""), weight="medium", size="0.84em"),
        _text(row.get("target", row.get("route", DETAIL_ROUTE)), size="0.82em"),
        _progress_cell(row),
        _status_cell(row),
    )


def _audit_strip(payload: dict[str, Any]) -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.text(f"AVG={payload['average_progress']:.2f}%", font_weight="bold"),
            padding="0.35rem 0.55rem",
            border="1px solid var(--gray-a5)",
            border_radius="10px",
        ),
        rx.box(
            rx.text(f"ROWS={payload['row_count']}", font_weight="bold"),
            padding="0.35rem 0.55rem",
            border="1px solid var(--gray-a5)",
            border_radius="10px",
        ),
        rx.box(
            rx.text(f"LEGACY={payload['legacy_row_count']}", font_size="0.82em"),
            padding="0.35rem 0.55rem",
            border="1px solid var(--gray-a4)",
            border_radius="10px",
        ),
        rx.box(
            rx.text(f"FUNCTIONS={payload['function_index_count']}", font_size="0.82em"),
            padding="0.35rem 0.55rem",
            border="1px solid var(--gray-a4)",
            border_radius="10px",
        ),
        spacing="3",
        wrap="wrap",
    )


def migration_tracker_panel() -> rx.Component:
    payload = build_migration_tracker_payload()
    rows = payload["rows"]
    return rx.vstack(
        rx.heading(payload["title"], size="4"),
        rx.text(payload["subtitle"], opacity="0.78"),
        _audit_strip(payload),
        rx.text(MISSION_CONTROL_POLICY, font_size="0.82em", opacity="0.82"),
        rx.text(INVENTORY_MARKER, font_size="0.78em", opacity="0.7"),
        rx.text(ESSENTIALS_MARKER, font_size="0.78em", opacity="0.7"),
        rx.text(FUNCTIONS_MARKER, font_size="0.78em", opacity="0.7"),
        rx.text(FUNCTION_LIMIT_MARKER, font_size="0.78em", opacity="0.7"),
        rx.text(DEDUP_MARKER, font_size="0.78em", opacity="0.7"),
        rx.box(
            rx.vstack(
                _header_row(),
                *[_body_row(row) for row in rows],
                width="100%",
                spacing="0",
            ),
            width="100%",
            overflow_x="auto",
            border="1px solid var(--gray-a4)",
            border_radius="14px",
        ),
        rx.link("Voir le detail complet", href=DETAIL_ROUTE, font_size="0.85em"),
        width="100%",
        align_items="stretch",
        spacing="3",
    )


def migration_tracker_compact_panel() -> rx.Component:
    return migration_tracker_panel()


def migration_tracker() -> rx.Component:
    return migration_tracker_panel()


def migration_tracker_view() -> rx.Component:
    return migration_tracker_panel()


def migration_tracker_section() -> rx.Component:
    return migration_tracker_panel()


def render_migration_tracker() -> rx.Component:
    return migration_tracker_panel()
