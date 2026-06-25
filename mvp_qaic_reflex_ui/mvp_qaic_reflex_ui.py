"""MVP QAIC local private Reflex UI.

Local shell only. No broker, no order, no sizing, no external writes.
"""

from __future__ import annotations

import reflex as rx

from mvp_qaic_py.reflex_app.app import page_registry_payload
from mvp_qaic_py.reflex_app.preview_observation_gate import (
    build_preview_observation_payload,
)


def _safe_text(value: object) -> str:
    return str(value).replace("{", "(").replace("}", ")")


def _route_page(title: str, route: str) -> rx.Component:
    payload = page_registry_payload()
    return rx.box(
        rx.vstack(
            rx.heading(title, size="6"),
            rx.text("MVP QAIC private local preview", weight="bold"),
            rx.text(f"Route: {route}"),
            rx.text(f"Registered routes: {payload['route_count']}"),
            rx.text("Safety: HUMAN_REVIEW_ONLY / NO_ORDER / NO_SIZING / NO_PUBLIC_DEPLOY"),
            spacing="4",
            align="start",
        ),
        padding="2rem",
    )


def index() -> rx.Component:
    payload = page_registry_payload()
    ui_shell = payload["ui_shell"]
    data_binding = payload["local_data_binding"]
    observation = build_preview_observation_payload()

    return rx.box(
        rx.vstack(
            rx.heading("MVP QAIC Global WebApp Shell", size="7"),
            rx.text("Private local operator preview", weight="bold"),
            rx.text("Safety locked: no order, no sizing, no broker execution, no public deploy."),
            rx.divider(),
            rx.heading("Status", size="5"),
            rx.text(f"Routes: {payload['route_count']}"),
            rx.text(f"Navigation groups: {ui_shell['navigation_group_count']}"),
            rx.text(f"Navigation items: {ui_shell['navigation_item_count']}"),
            rx.text(f"Data binding: {data_binding['binding_mode']}"),
            rx.text(f"Docs sources: {data_binding['docs_source_count']}"),
            rx.text(f"Export sources: {data_binding['export_source_count']}"),
            rx.text(f"Expected local URL: {observation['expected_local_url']}"),
            rx.divider(),
            rx.heading("Navigation", size="5"),
            rx.vstack(
                *[
                    rx.box(
                        rx.heading(_safe_text(group["title"]), size="4"),
                        rx.text(_safe_text(group["description"])),
                        rx.vstack(
                            *[
                                rx.link(
                                    _safe_text(item["title"]),
                                    href=item["route"],
                                )
                                for item in group["items"]
                            ],
                            align="start",
                        ),
                        border="1px solid #ddd",
                        border_radius="8px",
                        padding="1rem",
                        width="100%",
                    )
                    for group in ui_shell["groups"]
                ],
                spacing="4",
                width="100%",
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        padding="2rem",
        max_width="1100px",
        margin="0 auto",
    )


def architecture_web() -> rx.Component:
    return _route_page("Architecture Web", "/architecture-web")


def lexique_knowledge() -> rx.Component:
    return _route_page("Lexique Knowledge", "/lexique-knowledge")


def prompt_lab() -> rx.Component:
    return _route_page("Prompt Lab", "/prompt-lab")


def gem_portfolio() -> rx.Component:
    return _route_page("GEM Portfolio", "/gem-portfolio")


def qaic_bridge() -> rx.Component:
    return _route_page("QAIC Bridge", "/qaic-bridge")


def settings_safety() -> rx.Component:
    return _route_page("Settings Safety", "/settings-safety")


app = rx.App()
app.add_page(index, route="/", title="MVP QAIC")
app.add_page(architecture_web, route="/architecture-web", title="Architecture Web")
app.add_page(lexique_knowledge, route="/lexique-knowledge", title="Lexique Knowledge")
app.add_page(prompt_lab, route="/prompt-lab", title="Prompt Lab")
app.add_page(gem_portfolio, route="/gem-portfolio", title="GEM Portfolio")
app.add_page(qaic_bridge, route="/qaic-bridge", title="QAIC Bridge")
app.add_page(settings_safety, route="/settings-safety", title="Settings Safety")
