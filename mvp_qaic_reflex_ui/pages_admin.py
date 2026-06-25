"""Private admin pages for MVP QAIC Reflex."""

from __future__ import annotations

import reflex as rx

from mvp_qaic_py.reflex_app.data_binding import build_local_data_binding_payload

from .admin_data_registry import (
    admin_registry_summary_rows,
    build_admin_data_registry_payload,
    registry_domain_rows,
)
from .admin_theme_state import theme_state_component, theme_state_summary_rows
from .layout import page_shell
from .visual_theme import admin_summary_panel, theme_runtime_panel
from .theme import (
    ADMIN_SECTIONS,
    SAFETY_FLAGS,
    THEME_OPTIONS,
    UI_THEME,
    get_admin_routes,
    get_all_routes,
    get_theme_contract,
    key_value_card,
    section_card,
    status_pill,
)


def _admin_section_by_id(section_id: str) -> dict[str, str]:
    for section in ADMIN_SECTIONS:
        if section["section_id"] == section_id:
            return dict(section)
    raise KeyError(section_id)


def admin_center() -> rx.Component:
    return page_shell(
        "🛠️ Admin Center",
        "Centre privé pour piloter runtime, thème, sécurité, routes et données locales.",
        rx.vstack(
            rx.hstack(
                status_pill("PRIVATE_LOCAL", "ok"),
                status_pill("NO_PUBLIC_DEPLOY", "ok"),
                status_pill("NO_BROKER", "ok"),
                status_pill("NO_ORDER", "ok"),
                spacing="2",
                wrap="wrap",
            ),
            admin_summary_panel(),
            rx.heading("Admin sections", size="5"),
            rx.vstack(
                *[section_card(section) for section in ADMIN_SECTIONS],
                spacing="3",
                width="100%",
                align="start",
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        "/admin",
    )


def admin_runtime() -> rx.Component:
    section = _admin_section_by_id("admin_runtime")
    rows = {
        "runtime_mode": "LOCAL_PRIVATE",
        "frontend_url": "http://localhost:3000/",
        "backend_url": "http://127.0.0.1:8000",
        "reflex_config": "rxconfig.py",
        "sitemap_plugin": "EXPLICIT_ENABLED",
        "radix_themes_plugin": "EXPLICIT_ENABLED",
        "public_deploy": False,
    }

    return page_shell(
        section["title"],
        section["description"],
        rx.vstack(
            key_value_card("Runtime contract", rows),
            key_value_card("Theme contract", get_theme_contract()),
            key_value_card("Admin data registry", admin_registry_summary_rows()),
            spacing="4",
            align="start",
            width="100%",
        ),
        section["route"],
    )


def admin_theme() -> rx.Component:
    section = _admin_section_by_id("admin_theme")
    rows = {
        "default_mode": UI_THEME["default_mode"],
        "primary_accent": UI_THEME["primary_accent"],
        "secondary_accent": UI_THEME["secondary_accent"],
        "radius": UI_THEME["radius"],
        "density": UI_THEME["density"],
        "panel_background": UI_THEME["panel_background"],
    }

    return page_shell(
        section["title"],
        section["description"],
        rx.vstack(
            theme_runtime_panel(),
            theme_state_component(),
            key_value_card("Theme state contract", theme_state_summary_rows()),
            key_value_card("Current theme", rows),
            key_value_card("Allowed theme options", THEME_OPTIONS),
            rx.box(
                rx.vstack(
                    rx.heading("Decision", size="4"),
                    rx.text(
                        "P09 ajoute l'état interactif local. Application visuelle complète dans P10.",
                        size="3",
                    ),
                    rx.hstack(
                        status_pill("THEME_STATE_READY", "ok"),
                        status_pill("LIGHT_DARK_SYSTEM_READY", "ok"),
                        status_pill("ACCENT_READY", "ok"),
                        status_pill("DENSITY_READY", "ok"),
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
                background="#F8FAFC",
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        section["route"],
    )


def admin_safety() -> rx.Component:
    section = _admin_section_by_id("admin_safety")
    return page_shell(
        section["title"],
        section["description"],
        rx.vstack(
            key_value_card("Safety flags", SAFETY_FLAGS),
            rx.hstack(
                status_pill("HUMAN_REVIEW_ONLY", "ok"),
                status_pill("NO_AUTO_ORDER", "ok"),
                status_pill("NO_AUTO_SIZING", "ok"),
                status_pill("NO_BROKER_EXECUTION", "ok"),
                status_pill("NO_EXTERNAL_WRITE", "ok"),
                spacing="2",
                wrap="wrap",
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        section["route"],
    )


def admin_routes() -> rx.Component:
    section = _admin_section_by_id("admin_routes")
    routes = get_all_routes()
    rows = {f"route_{idx + 1:02d}": route for idx, route in enumerate(routes)}

    return page_shell(
        section["title"],
        section["description"],
        rx.vstack(
            key_value_card("Route inventory", rows),
            key_value_card(
                "Route counts", {"admin_routes": len(get_admin_routes()), "all_routes": len(routes)}
            ),
            key_value_card("Registry domains", registry_domain_rows()),
            spacing="4",
            align="start",
            width="100%",
        ),
        section["route"],
    )


def admin_data_binding() -> rx.Component:
    section = _admin_section_by_id("admin_data_binding")
    payload = build_local_data_binding_payload()
    registry_payload = build_admin_data_registry_payload()
    rows = {
        "binding_mode": payload["binding_mode"],
        "docs_source_count": payload["docs_source_count"],
        "export_source_count": payload["export_source_count"],
        "write_allowed": False,
        "live_action": False,
    }

    return page_shell(
        section["title"],
        section["description"],
        rx.vstack(
            key_value_card("Local readonly data binding", rows),
            key_value_card("Admin data registry", admin_registry_summary_rows()),
            key_value_card("Registry domains", registry_domain_rows()),
            rx.hstack(
                status_pill("LOCAL_READONLY", "ok"),
                status_pill("NO_SHEET_WRITE", "ok"),
                status_pill("NO_BIGQUERY_WRITE", "ok"),
                status_pill(f"ROUTES={registry_payload['route_count']}", "info"),
                spacing="2",
                wrap="wrap",
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        section["route"],
    )
