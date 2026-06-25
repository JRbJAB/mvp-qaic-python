"""Visual design system for the MVP QAIC Reflex application."""

from __future__ import annotations

from collections.abc import Sequence

import reflex as rx


DESIGN_TOKENS = {
    "app_background": "var(--gray-1)",
    "sidebar_background": "var(--gray-2)",
    "topbar_background": "color-mix(in srgb, var(--gray-1) 88%, transparent)",
    "surface_background": "var(--gray-2)",
    "surface_elevated": "var(--gray-1)",
    "border": "var(--gray-6)",
    "text_primary": "var(--gray-12)",
    "text_secondary": "var(--gray-11)",
    "accent": "var(--accent-9)",
    "accent_soft": "var(--accent-3)",
    "accent_border": "var(--accent-7)",
    "success_soft": "var(--green-3)",
    "warning_soft": "var(--amber-3)",
    "critical_soft": "var(--red-3)",
    "radius_card": "16px",
    "radius_panel": "20px",
    "shadow_card": "0 8px 30px rgba(15, 23, 42, 0.06)",
    "shadow_hero": "0 20px 50px rgba(15, 23, 42, 0.10)",
}

APP_BACKGROUND = DESIGN_TOKENS["app_background"]
SIDEBAR_BACKGROUND = DESIGN_TOKENS["sidebar_background"]
TOPBAR_BACKGROUND = DESIGN_TOKENS["topbar_background"]
CONTENT_MAX_WIDTH = "1480px"


def color_mode_toggle() -> rx.Component:
    """Official Reflex light/dark color-mode toggle."""

    return rx.button(
        rx.color_mode_cond(
            rx.text("🌙 Mode sombre", size="2", weight="bold"),
            rx.text("☀️ Mode clair", size="2", weight="bold"),
        ),
        on_click=rx.toggle_color_mode,
        variant="soft",
        size="2",
        border_radius="999px",
    )


def metric_card(
    label: str,
    value: str,
    detail: str,
    tone: str = "accent",
) -> rx.Component:
    tone_background = {
        "accent": "var(--accent-3)",
        "success": "var(--green-3)",
        "warning": "var(--amber-3)",
        "neutral": "var(--gray-3)",
    }.get(tone, "var(--accent-3)")

    return rx.box(
        rx.vstack(
            rx.text(label, size="2", weight="bold", color="var(--gray-11)"),
            rx.heading(value, size="6", color="var(--gray-12)"),
            rx.text(detail, size="2", color="var(--gray-11)"),
            spacing="2",
            align="start",
        ),
        background=tone_background,
        border=f"1px solid {DESIGN_TOKENS['border']}",
        border_radius=DESIGN_TOKENS["radius_card"],
        padding="1rem",
        width="100%",
        min_height="132px",
    )


def metric_grid(metrics: Sequence[dict[str, str]]) -> rx.Component:
    return rx.grid(
        *[
            metric_card(
                metric["label"],
                metric["value"],
                metric["detail"],
                metric.get("tone", "accent"),
            )
            for metric in metrics
        ],
        columns="4",
        spacing="4",
        width="100%",
    )


def mission_control_hero() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "MVP QAIC · CRYPTO SIGNAL OS",
                        size="2",
                        weight="bold",
                        color="var(--accent-11)",
                    ),
                    rx.heading(
                        "Mission Control",
                        size="8",
                        color="var(--gray-12)",
                    ),
                    rx.text(
                        "Pilotage unifié du développement, du CDC, de "
                        "l’architecture Web, de la documentation et des registres.",
                        size="4",
                        color="var(--gray-11)",
                        max_width="760px",
                    ),
                    spacing="3",
                    align="start",
                ),
                rx.spacer(),
                rx.box(
                    rx.vstack(
                        rx.text("Runtime", size="2", weight="bold"),
                        rx.text("LOCAL PRIVATE", size="4", weight="bold"),
                        rx.text("Human review only", size="2"),
                        spacing="1",
                        align="end",
                    ),
                    background="var(--green-3)",
                    border="1px solid var(--green-7)",
                    border_radius="16px",
                    padding="1rem",
                ),
                width="100%",
                align="center",
                spacing="4",
            ),
            rx.hstack(
                rx.link(
                    rx.button("Ouvrir Admin Center", variant="solid"),
                    href="/admin",
                ),
                rx.link(
                    rx.button("Architecture Web", variant="soft"),
                    href="/architecture-web",
                ),
                rx.link(
                    rx.button("CDC Tracker", variant="soft"),
                    href="/cdc-tracker",
                ),
                spacing="3",
                wrap="wrap",
            ),
            spacing="5",
            align="start",
            width="100%",
        ),
        background=(
            "linear-gradient(135deg, var(--accent-3) 0%, var(--gray-1) 52%, var(--cyan-3) 100%)"
        ),
        border="1px solid var(--accent-6)",
        border_radius=DESIGN_TOKENS["radius_panel"],
        box_shadow=DESIGN_TOKENS["shadow_hero"],
        padding="1.5rem",
        width="100%",
    )


def theme_runtime_panel() -> rx.Component:
    """Display the currently active global Reflex appearance."""

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading("Global UI Theme", size="5"),
                    rx.text(
                        "Thème Reflex global appliqué à toutes les pages.",
                        size="3",
                        color="var(--gray-11)",
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                color_mode_toggle(),
                width="100%",
                align="center",
            ),
            rx.divider(),
            rx.hstack(
                rx.text("Apparence active :", weight="bold"),
                rx.color_mode_cond(
                    rx.text("LIGHT", weight="bold", color="var(--amber-11)"),
                    rx.text("DARK", weight="bold", color="var(--cyan-11)"),
                ),
                spacing="2",
            ),
            rx.hstack(
                rx.box(
                    width="48px",
                    height="48px",
                    border_radius="12px",
                    background="var(--accent-9)",
                ),
                rx.box(
                    width="48px",
                    height="48px",
                    border_radius="12px",
                    background="var(--accent-6)",
                ),
                rx.box(
                    width="48px",
                    height="48px",
                    border_radius="12px",
                    background="var(--gray-4)",
                ),
                spacing="2",
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        background="var(--gray-2)",
        border="1px solid var(--gray-6)",
        border_radius=DESIGN_TOKENS["radius_panel"],
        padding="1.25rem",
        width="100%",
        box_shadow=DESIGN_TOKENS["shadow_card"],
    )


def admin_summary_panel() -> rx.Component:
    return metric_grid(
        (
            {
                "label": "Admin routes",
                "value": "6",
                "detail": "Runtime, theme, safety, routes and data.",
                "tone": "accent",
            },
            {
                "label": "Registry mode",
                "value": "READ ONLY",
                "detail": "No persistent registry mutation.",
                "tone": "success",
            },
            {
                "label": "Theme mode",
                "value": "GLOBAL",
                "detail": "Radix theme with light/dark support.",
                "tone": "accent",
            },
            {
                "label": "Execution",
                "value": "BLOCKED",
                "detail": "No broker, order or sizing.",
                "tone": "warning",
            },
        )
    )
