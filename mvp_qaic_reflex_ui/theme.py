"""Theme and navigation contract for the MVP QAIC Reflex UI."""

from __future__ import annotations

from collections.abc import Mapping

import reflex as rx

UI_THEME = {
    "app_name": "MVP QAIC",
    "default_mode": "system",
    "primary_accent": "blue",
    "secondary_accent": "cyan",
    "radius": "large",
    "density": "comfortable",
    "panel_background": "solid",
    "mission": "Lexique-first Crypto Signal OS with prompt workflows and QAIC bridge.",
}

THEME_OPTIONS = {
    "modes": ("light", "dark", "system"),
    "accents": ("blue", "cyan", "indigo", "violet", "green", "amber", "red"),
    "radius": ("none", "small", "medium", "large", "full"),
    "density": ("compact", "comfortable", "spacious"),
    "panel_background": ("solid", "translucent"),
}

SAFETY_FLAGS = {
    "human_review_only": True,
    "no_auto_order": True,
    "no_auto_sizing": True,
    "no_broker_execution": True,
    "no_public_deploy": True,
    "no_apps_script_execution": True,
    "no_sheet_write": True,
    "no_bigquery_write": True,
}

LANDING_SECTIONS = (
    {
        "section_id": "home_mission_control",
        "icon": "🏠",
        "title": "Home / Mission Control",
        "route": "/",
        "status": "ACTIVE",
        "priority": "P0",
        "description": "Vue d'ensemble opérateur, état runtime, prochaines actions et garde-fous.",
    },
    {
        "section_id": "dev_tracking",
        "icon": "🧭",
        "title": "Dev Tracking",
        "route": "/dev-tracking",
        "status": "ACTIVE",
        "priority": "P0",
        "description": "Suivi des lots Reflex/MVP, HEAD Git, tags, tests, gates et dette technique.",
    },
    {
        "section_id": "cdc_tracker",
        "icon": "📘",
        "title": "CDC Tracker",
        "route": "/cdc-tracker",
        "status": "ACTIVE",
        "priority": "P0",
        "description": "Pilotage CDC, périmètre validé, décisions, gaps et prochains jalons.",
    },
    {
        "section_id": "architecture_web",
        "icon": "🧱",
        "title": "Architecture Web",
        "route": "/architecture-web",
        "status": "ACTIVE",
        "priority": "P0",
        "description": "Structure WebApp, routes, composants, données locales et future exposition publique.",
    },
    {
        "section_id": "documentation_registry",
        "icon": "📚",
        "title": "Documentation Registry",
        "route": "/documentation-registry",
        "status": "ACTIVE",
        "priority": "P0",
        "description": "Registre docs/exports/prompts, statut, source, version et usage produit.",
    },
    {
        "section_id": "architecture_registry",
        "icon": "🗂️",
        "title": "Architecture & Registry",
        "route": "/architecture-registry",
        "status": "TO_STRUCTURE",
        "priority": "P0",
        "description": "Réconciliation finale architecture, registry technique, modules et routes.",
    },
)

ADMIN_SECTIONS = (
    {
        "section_id": "admin_center",
        "icon": "🛠️",
        "title": "Admin Center",
        "route": "/admin",
        "status": "ACTIVE",
        "priority": "P0",
        "description": "Centre d'administration privé Reflex.",
    },
    {
        "section_id": "admin_runtime",
        "icon": "🟢",
        "title": "Runtime",
        "route": "/admin/runtime",
        "status": "ACTIVE",
        "priority": "P0",
        "description": "État frontend, backend, plugins, bindings et environnement local.",
    },
    {
        "section_id": "admin_theme",
        "icon": "🎨",
        "title": "Theme Settings",
        "route": "/admin/theme",
        "status": "ACTIVE",
        "priority": "P0",
        "description": "Modes light/dark/system, accent, radius, density et panel background.",
    },
    {
        "section_id": "admin_safety",
        "icon": "🛡️",
        "title": "Safety",
        "route": "/admin/safety",
        "status": "ACTIVE",
        "priority": "P0",
        "description": "Garde-fous no order/no sizing/no deploy/no external write.",
    },
    {
        "section_id": "admin_routes",
        "icon": "🧭",
        "title": "Routes",
        "route": "/admin/routes",
        "status": "ACTIVE",
        "priority": "P0",
        "description": "Inventaire des routes produit, admin et futures routes.",
    },
    {
        "section_id": "admin_data_binding",
        "icon": "🔗",
        "title": "Data Binding",
        "route": "/admin/data-binding",
        "status": "ACTIVE",
        "priority": "P0",
        "description": "Vue locale readonly des sources docs, exports, prompts et registry.",
    },
)

SECONDARY_ROUTES = (
    {"title": "Lexique Knowledge", "route": "/lexique-knowledge"},
    {"title": "Prompt Lab", "route": "/prompt-lab"},
    {"title": "GEM Portfolio", "route": "/gem-portfolio"},
    {"title": "QAIC Bridge", "route": "/qaic-bridge"},
    {"title": "Settings Safety", "route": "/settings-safety"},
)


def get_landing_sections() -> list[dict[str, str]]:
    return [dict(section) for section in LANDING_SECTIONS]


def get_admin_sections() -> list[dict[str, str]]:
    return [dict(section) for section in ADMIN_SECTIONS]


def get_primary_routes() -> list[str]:
    return [section["route"] for section in LANDING_SECTIONS]


def get_admin_routes() -> list[str]:
    return [section["route"] for section in ADMIN_SECTIONS]


def get_all_routes() -> list[str]:
    secondary = [item["route"] for item in SECONDARY_ROUTES]
    return get_primary_routes() + get_admin_routes() + secondary


def get_theme_contract() -> dict[str, object]:
    return {
        "theme": dict(UI_THEME),
        "theme_options": {key: list(value) for key, value in THEME_OPTIONS.items()},
        "safety_flags": dict(SAFETY_FLAGS),
        "primary_section_count": len(LANDING_SECTIONS),
        "admin_section_count": len(ADMIN_SECTIONS),
        "secondary_route_count": len(SECONDARY_ROUTES),
    }


def status_pill(label: str, level: str = "info") -> rx.Component:
    tone = {
        "ok": "#E7F8EF",
        "warning": "#FFF7DF",
        "critical": "#FFE8E8",
        "info": "#EEF4FF",
    }.get(level, "#EEF4FF")

    return rx.box(
        rx.text(label, size="2", weight="bold"),
        background=tone,
        border_radius="999px",
        padding="0.35rem 0.7rem",
        border="1px solid rgba(0, 0, 0, 0.08)",
    )


def section_card(section: Mapping[str, str]) -> rx.Component:
    return rx.link(
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(section["icon"], size="6"),
                    rx.vstack(
                        rx.text(section["title"], weight="bold", size="4"),
                        rx.text(section["route"], size="2"),
                        spacing="1",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.text(section["description"], size="3"),
                rx.hstack(
                    status_pill(
                        section["status"], "ok" if section["status"] == "ACTIVE" else "warning"
                    ),
                    status_pill(section["priority"], "info"),
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
            background="rgba(255, 255, 255, 0.75)",
        ),
        href=section["route"],
        width="100%",
        text_decoration="none",
    )


def key_value_card(title: str, rows: Mapping[str, object]) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading(title, size="4"),
            *[
                rx.hstack(
                    rx.text(str(key), size="2", weight="bold", min_width="180px"),
                    rx.text(str(value), size="2"),
                    spacing="3",
                    align="center",
                    width="100%",
                )
                for key, value in rows.items()
            ],
            spacing="2",
            align="start",
            width="100%",
        ),
        border="1px solid rgba(0, 0, 0, 0.10)",
        border_radius="14px",
        padding="1rem",
        width="100%",
        background="white",
    )


def safety_panel() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Safety gates", size="4"),
            rx.hstack(
                status_pill("HUMAN_REVIEW_ONLY", "ok"),
                status_pill("NO_ORDER", "ok"),
                status_pill("NO_SIZING", "ok"),
                status_pill("NO_PUBLIC_DEPLOY", "ok"),
                spacing="2",
                wrap="wrap",
            ),
            rx.text(
                "MVP QAIC reste une WebApp lexique/prompt/support décision. Pas d'exécution broker.",
                size="3",
            ),
            spacing="3",
            align="start",
        ),
        border="1px solid rgba(0, 0, 0, 0.10)",
        border_radius="14px",
        padding="1rem",
        width="100%",
        background="#F8FAFC",
    )
