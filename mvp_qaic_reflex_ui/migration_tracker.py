from __future__ import annotations

from typing import Any

import reflex as rx

from mvp_qaic_reflex_ui.migration_os import build_migration_tracker_payload as _build_payload
from mvp_qaic_reflex_ui.migration_os import migration_average_progress as _average_progress
from mvp_qaic_reflex_ui.migration_os import migration_tracker_summary_rows as _summary_rows

# Contract markers kept here for R9B/R10 regression tests and operator audit.
SHOW_ONLY_ESSENTIAL = True
TABLE_UX_WITH_PERCENTAGES = True
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
DETAIL_ROUTE = "/migration/global"


def build_migration_tracker_payload() -> dict[str, Any]:
    payload = _build_payload()
    payload.setdefault("table_ux_with_percentages", TABLE_UX_WITH_PERCENTAGES)
    payload.setdefault("show_only_essential", SHOW_ONLY_ESSENTIAL)
    payload.setdefault("matrix_file", MIGRATION_GLOBAL_MATRIX)
    payload.setdefault("summary_file", MIGRATION_GLOBAL_MATRIX_SUMMARY)
    payload.setdefault("dedoublonnees", True)
    return payload


def migration_average_progress() -> float:
    return _average_progress()


def migration_tracker_summary_rows() -> list[dict[str, Any]]:
    return _summary_rows()


def _cell(text: str, width: str = "auto", weight: str = "regular") -> rx.Component:
    return rx.text(str(text), width=width, font_weight=weight, font_size="0.82em")


def _status_cell(row: dict[str, Any]) -> rx.Component:
    status = str(row.get("status", "REVIEW_REQUIRED"))
    label = str(row.get("status_label_fr", status))
    return rx.vstack(
        rx.text(status, font_weight="bold", font_size="0.78em"),
        rx.text(label, font_size="0.72em", opacity="0.78"),
        spacing="1",
        align_items="start",
        min_width="150px",
    )


def _row_component(row: dict[str, Any]) -> rx.Component:
    progress = int(row.get("progress_pct", 0))
    return rx.hstack(
        _cell(str(row.get("type", "")), "120px"),
        _cell(str(row.get("source", "")), "minmax(220px, 1fr)", "medium"),
        _cell(str(row.get("target", row.get("route", DETAIL_ROUTE))), "180px"),
        _cell(f"{progress}%", "60px", "bold"),
        _status_cell(row),
        width="100%",
        align_items="center",
        spacing="3",
        padding_y="0.35rem",
        border_bottom="1px solid var(--gray-a4)",
    )


def _header_row() -> rx.Component:
    return rx.hstack(
        _cell("Type", "120px", "bold"),
        _cell("Source", "minmax(220px, 1fr)", "bold"),
        _cell("Cible", "180px", "bold"),
        _cell("%", "60px", "bold"),
        _cell("Statut", "150px", "bold"),
        width="100%",
        align_items="center",
        spacing="3",
        padding_y="0.45rem",
        border_bottom="1px solid var(--gray-a7)",
    )


def migration_tracker_panel() -> rx.Component:
    payload = build_migration_tracker_payload()
    rows = payload["rows"]
    return rx.vstack(
        rx.heading(payload["title"], size="4"),
        rx.text(payload["subtitle"], opacity="0.78"),
        rx.hstack(
            rx.text(f"AVG={payload['average_progress']:.2f}%", font_weight="bold"),
            rx.text(f"ROWS={payload['row_count']}", font_weight="bold"),
            rx.text(f"LEGACY={payload['legacy_row_count']}", opacity="0.82"),
            rx.text(f"INVENTORY={payload['source_csv_rows']}", opacity="0.82"),
            spacing="4",
            wrap="wrap",
        ),
        rx.text(MISSION_CONTROL_POLICY, font_size="0.82em", opacity="0.82"),
        rx.text(INVENTORY_MARKER, font_size="0.78em", opacity="0.7"),
        rx.text(ESSENTIALS_MARKER, font_size="0.78em", opacity="0.7"),
        rx.text(FUNCTIONS_MARKER, font_size="0.78em", opacity="0.7"),
        rx.text(FUNCTION_LIMIT_MARKER, font_size="0.78em", opacity="0.7"),
        rx.text(DEDUP_MARKER, font_size="0.78em", opacity="0.7"),
        rx.vstack(
            _header_row(),
            *[_row_component(row) for row in rows],
            width="100%",
            spacing="0",
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
