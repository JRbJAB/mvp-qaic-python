"""Reusable layout components for the MVP QAIC Reflex UI."""

from __future__ import annotations

import reflex as rx

from .theme import ADMIN_SECTIONS, LANDING_SECTIONS, SECONDARY_ROUTES, UI_THEME, status_pill
from .visual_theme import (
    APP_BACKGROUND,
    CONTENT_MAX_WIDTH,
    SIDEBAR_BACKGROUND,
    TOPBAR_BACKGROUND,
    color_mode_toggle,
)


def navigation_items() -> list[dict[str, str]]:
    primary = [
        {
            "title": f"{section['icon']} {section['title']}",
            "route": section["route"],
            "kind": "primary",
        }
        for section in LANDING_SECTIONS
    ]
    admin = [
        {
            "title": f"{section['icon']} {section['title']}",
            "route": section["route"],
            "kind": "admin",
        }
        for section in ADMIN_SECTIONS
    ]
    secondary = [
        {
            "title": item["title"],
            "route": item["route"],
            "kind": "secondary",
        }
        for item in SECONDARY_ROUTES
    ]
    return primary + admin + secondary


def _nav_group(title: str, items: list[dict[str, str]], active_route: str) -> rx.Component:
    links = []
    for item in items:
        is_active = item["route"] == active_route
        links.append(
            rx.link(
                rx.box(
                    rx.text(item["title"], weight="bold" if is_active else "regular", size="3"),
                    padding="0.60rem 0.75rem",
                    border_radius="10px",
                    background="#EAF2FF" if is_active else "transparent",
                    width="100%",
                ),
                href=item["route"],
                width="100%",
                text_decoration="none",
            )
        )

    return rx.vstack(
        rx.text(title, size="2", weight="bold"),
        *links,
        spacing="1",
        align="start",
        width="100%",
    )


def sidebar(active_route: str = "/") -> rx.Component:
    items = navigation_items()
    primary = [item for item in items if item["kind"] == "primary"]
    admin = [item for item in items if item["kind"] == "admin"]
    secondary = [item for item in items if item["kind"] == "secondary"]

    return rx.box(
        rx.vstack(
            rx.heading("MVP QAIC", size="5"),
            rx.text("Crypto Signal OS", size="2"),
            rx.divider(),
            _nav_group("Mission", primary, active_route),
            rx.divider(),
            _nav_group("Admin", admin, active_route),
            rx.divider(),
            _nav_group("Modules", secondary, active_route),
            spacing="3",
            align="start",
            width="100%",
        ),
        width="300px",
        min_width="300px",
        padding="1rem",
        border_right="1px solid rgba(0, 0, 0, 0.10)",
        min_height="100vh",
        background=SIDEBAR_BACKGROUND,
    )


def topbar(title: str, subtitle: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading(title, size="7"),
                    rx.text(subtitle, size="3"),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                status_pill("LOCAL_PRIVATE", "ok"),
                status_pill(UI_THEME["default_mode"].upper(), "info"),
                color_mode_toggle(),
                spacing="3",
                align="center",
                width="100%",
            ),
            rx.divider(),
            spacing="4",
            align="start",
            width="100%",
        ),
        padding="1.25rem 1.5rem",
        width="100%",
        background=TOPBAR_BACKGROUND,
        position="sticky",
        top="0",
        z_index="20",
        backdrop_filter="blur(16px)",
    )


def page_shell(
    title: str, subtitle: str, body: rx.Component, active_route: str = "/"
) -> rx.Component:
    return rx.hstack(
        sidebar(active_route),
        rx.box(
            topbar(title, subtitle),
            rx.box(
                body,
                padding="0 1.5rem 2rem 1.5rem",
                width="100%",
                max_width=CONTENT_MAX_WIDTH,
                margin="0 auto",
            ),
            width="100%",
            min_height="100vh",
            background=APP_BACKGROUND,
        ),
        align="start",
        width="100%",
        min_height="100vh",
    )


def placeholder_body(label: str, route: str, description: str) -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.heading(label, size="5"),
                rx.text(description, size="3"),
                rx.text(f"Route: {route}", size="2"),
                rx.hstack(
                    status_pill("STRUCTURE_READY", "ok"),
                    status_pill("CONTENT_TO_CONNECT", "warning"),
                    spacing="2",
                    wrap="wrap",
                ),
                spacing="3",
                align="start",
            ),
            border="1px solid rgba(0, 0, 0, 0.10)",
            border_radius="14px",
            padding="1rem",
            width="100%",
            background="white",
        ),
        spacing="4",
        align="start",
        width="100%",
    )
