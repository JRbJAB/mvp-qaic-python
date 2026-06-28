"""CDC + Dev Tracker Reflex page.

Standalone route page for the MVP UI CDC + Dev Tracker surface.
No broker, no order, no sizing, no Sheet/BQ write.
"""

from __future__ import annotations

import reflex as rx


def _metric(label: str, value: str) -> rx.Component:
    return rx.box(
        rx.text(label, font_size="0.8em", opacity="0.75"),
        rx.heading(value, size="4"),
        padding="0.8em",
        border="1px solid #e5e7eb",
        border_radius="12px",
        min_width="150px",
    )


def _row(tracker_id: str, kind: str, status: str, action: str) -> rx.Component:
    return rx.hstack(
        rx.text(tracker_id, width="110px"),
        rx.text(kind, width="130px"),
        rx.text(status, width="120px"),
        rx.text(action, flex="1"),
        padding="0.65em",
        border_bottom="1px solid #f1f5f9",
        align="center",
        width="100%",
    )


def cdc_dev_tracker_reflex_page() -> rx.Component:
    """Render the CDC + Dev Tracker page using the Migration Tracker layout spirit."""
    return rx.box(
        rx.vstack(
            rx.heading("CDC + Dev Tracker", size="7"),
            rx.text("UI style: Migration Tracker | Scope: CDC tracker + Dev tracker"),
            rx.hstack(
                _metric("CDC items", "4"),
                _metric("Dev items", "4"),
                _metric("Review", "Human"),
                _metric("Route", "/cdc-dev-tracker"),
                wrap="wrap",
                spacing="3",
                width="100%",
            ),
            rx.hstack(
                rx.text("Filters:"),
                rx.text("ALL"),
                rx.text("CDC_TRACKER"),
                rx.text("DEV_TRACKER"),
                spacing="4",
                width="100%",
            ),
            rx.box(
                _row("CDC-001", "CDC_TRACKER", "REVIEW", "Validate observable CDC requirements"),
                _row("CDC-002", "CDC_TRACKER", "TODO", "Map UI sections to CDC requirements"),
                _row("DEV-001", "DEV_TRACKER", "IN_PROGRESS", "Wire screen in MVP UI"),
                _row("DEV-002", "DEV_TRACKER", "TODO", "Run final local smoke"),
                border="1px solid #e5e7eb",
                border_radius="12px",
                width="100%",
            ),
            rx.box(
                rx.heading("Detail panel", size="4"),
                rx.text("Operator review required before any live action. No broker/order/sizing."),
                padding="1em",
                border="1px solid #e5e7eb",
                border_radius="12px",
                width="100%",
            ),
            rx.box(
                rx.heading("Next actions", size="4"),
                rx.text("R5: runtime smoke unique for /cdc-dev-tracker."),
                padding="1em",
                border="1px solid #e5e7eb",
                border_radius="12px",
                width="100%",
            ),
            spacing="4",
            width="100%",
        ),
        padding="2em",
        width="100%",
    )

