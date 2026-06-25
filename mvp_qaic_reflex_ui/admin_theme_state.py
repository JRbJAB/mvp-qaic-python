"""Interactive theme state foundation for the private MVP QAIC admin UI."""

from __future__ import annotations

from collections.abc import Mapping

import reflex as rx

from .theme import THEME_OPTIONS, UI_THEME


DEFAULT_THEME_STATE = {
    "mode": UI_THEME["default_mode"],
    "accent": UI_THEME["primary_accent"],
    "radius": UI_THEME["radius"],
    "density": UI_THEME["density"],
    "panel_background": UI_THEME["panel_background"],
}


def validate_theme_choice(field: str, value: str) -> bool:
    if field == "mode":
        return value in THEME_OPTIONS["modes"]
    if field == "accent":
        return value in THEME_OPTIONS["accents"]
    if field == "radius":
        return value in THEME_OPTIONS["radius"]
    if field == "density":
        return value in THEME_OPTIONS["density"]
    if field == "panel_background":
        return value in THEME_OPTIONS["panel_background"]
    return False


def build_theme_state_payload(state: Mapping[str, str] | None = None) -> dict[str, object]:
    current = dict(DEFAULT_THEME_STATE if state is None else state)
    return {
        "theme_state_status": "READY_INTERACTIVE_LOCAL",
        "current": current,
        "allowed": {key: list(value) for key, value in THEME_OPTIONS.items()},
        "write_mode": "IN_MEMORY_ONLY",
        "public_deploy": False,
        "live_action": False,
        "human_review_only": True,
    }


def theme_state_summary_rows() -> dict[str, object]:
    payload = build_theme_state_payload()
    current = payload["current"]
    return {
        "status": payload["theme_state_status"],
        "mode": current["mode"],
        "accent": current["accent"],
        "radius": current["radius"],
        "density": current["density"],
        "panel_background": current["panel_background"],
        "write_mode": payload["write_mode"],
    }


class ThemeSettingsState(rx.State):
    """Local in-memory UI state for theme controls."""

    mode: str = "system"
    accent: str = "blue"
    radius: str = "large"
    density: str = "comfortable"
    panel_background: str = "solid"

    def set_light_mode(self) -> None:
        self.mode = "light"

    def set_dark_mode(self) -> None:
        self.mode = "dark"

    def set_system_mode(self) -> None:
        self.mode = "system"

    def set_blue_accent(self) -> None:
        self.accent = "blue"

    def set_cyan_accent(self) -> None:
        self.accent = "cyan"

    def set_indigo_accent(self) -> None:
        self.accent = "indigo"

    def set_compact_density(self) -> None:
        self.density = "compact"

    def set_comfortable_density(self) -> None:
        self.density = "comfortable"

    def set_spacious_density(self) -> None:
        self.density = "spacious"

    def reset_theme(self) -> None:
        self.mode = "system"
        self.accent = "blue"
        self.radius = "large"
        self.density = "comfortable"
        self.panel_background = "solid"


def theme_state_component() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Interactive theme state", size="4"),
            rx.text(
                "État local en mémoire pour préparer light/dark/system, accent et densité.",
                size="3",
            ),
            rx.hstack(
                rx.button("Light", on_click=ThemeSettingsState.set_light_mode),
                rx.button("Dark", on_click=ThemeSettingsState.set_dark_mode),
                rx.button("System", on_click=ThemeSettingsState.set_system_mode),
                spacing="2",
                wrap="wrap",
            ),
            rx.hstack(
                rx.button("Blue", on_click=ThemeSettingsState.set_blue_accent),
                rx.button("Cyan", on_click=ThemeSettingsState.set_cyan_accent),
                rx.button("Indigo", on_click=ThemeSettingsState.set_indigo_accent),
                spacing="2",
                wrap="wrap",
            ),
            rx.hstack(
                rx.button("Compact", on_click=ThemeSettingsState.set_compact_density),
                rx.button("Comfortable", on_click=ThemeSettingsState.set_comfortable_density),
                rx.button("Spacious", on_click=ThemeSettingsState.set_spacious_density),
                spacing="2",
                wrap="wrap",
            ),
            rx.button("Reset theme", on_click=ThemeSettingsState.reset_theme),
            rx.divider(),
            rx.text("Current mode:", weight="bold"),
            rx.text(ThemeSettingsState.mode),
            rx.text("Current accent:", weight="bold"),
            rx.text(ThemeSettingsState.accent),
            rx.text("Current density:", weight="bold"),
            rx.text(ThemeSettingsState.density),
            spacing="3",
            align="start",
            width="100%",
        ),
        border="1px solid rgba(0, 0, 0, 0.10)",
        border_radius="14px",
        padding="1rem",
        width="100%",
        background="#F8FAFC",
    )
