"""Landing and priority pages for MVP QAIC Reflex."""

from __future__ import annotations

from typing import Any

import reflex as rx

from .layout import page_shell
from .migration_tracker import migration_tracker_compact_panel
from .migration_decision_workbench import migration_decision_workbench_compact_panel
from .qaic_bridge_operator_binding import build_qaic_bridge_operator_card
from .theme import LANDING_SECTIONS, get_landing_sections, safety_panel, section_card
from .visual_theme import metric_grid, mission_control_hero
from .web_architecture_cdc import architecture_web_cdc_body, sitemap_page_body
from .cdc_dev_tracker_reflex_page import cdc_tracker_reflex_page, dev_tracking_reflex_page
from .dev_lifecycle_tracker import (
    dev_lifecycle_tracker_panel as _r6n_vertical_dev_lifecycle_tracker_panel,
)


def _registry_body(label: str, route: str, description: str) -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.heading(label, size="5"),
                rx.text(description, size="3"),
                rx.text(f"Route: {route}", size="2"),
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


def _section_by_id(section_id: str) -> dict[str, str]:
    for section in LANDING_SECTIONS:
        if section["section_id"] == section_id:
            return dict(section)
    raise KeyError(section_id)


def home() -> rx.Component:
    sections = get_landing_sections()
    metrics = (
        {
            "label": "Mission sections",
            "value": "6",
            "detail": "Home, Dev, CDC, Web, Docs and Registry.",
            "tone": "accent",
        },
        {
            "label": "Admin sections",
            "value": "6",
            "detail": "Runtime, theme, safety, routes and data.",
            "tone": "accent",
        },
        {
            "label": "Runtime",
            "value": "LOCAL",
            "detail": "Private Reflex frontend and backend.",
            "tone": "success",
        },
        {
            "label": "Safety",
            "value": "LOCKED",
            "detail": "No broker, order, sizing or public deploy.",
            "tone": "warning",
        },
    )

    return page_shell(
        "🏠 Home / Mission Control",
        "Landing page opérateur pour piloter le MVP QAIC Reflex.",
        rx.vstack(
            mission_control_hero(),
            metric_grid(metrics),
            migration_tracker_compact_panel(),
            migration_decision_workbench_compact_panel(),
            safety_panel(),
            rx.heading("Sections prioritaires", size="5"),
            rx.grid(
                *[section_card(section) for section in sections],
                columns="2",
                spacing="4",
                width="100%",
            ),
            spacing="5",
            align="start",
            width="100%",
        ),
        "/",
    )


def mission_control() -> rx.Component:
    return home()


def dev_tracking() -> rx.Component:
    return dev_tracking_reflex_page()


def cdc_tracker() -> rx.Component:
    return cdc_tracker_reflex_page()


def architecture_web() -> rx.Component:
    section = _section_by_id("architecture_web")
    return page_shell(
        section["title"],
        "Schema pro, sitemap visuel, CDC tracker et cockpits essentiels.",
        architecture_web_cdc_body(),
        section["route"],
    )


def web_sitemap() -> rx.Component:
    return page_shell(
        "🧭 Visual Sitemap",
        "Carte visuelle des pages Reflex, cockpits, flux et statuts CDC.",
        sitemap_page_body(),
        "/sitemap",
    )


def documentation_registry() -> rx.Component:
    section = _section_by_id("documentation_registry")
    return page_shell(
        section["title"],
        "Registre documentation, exports, prompts et packs de décision.",
        _registry_body(
            section["title"],
            section["route"],
            "Cette page listera docs, versions, sources, usages et statut d'intégration.",
        ),
        section["route"],
    )


def architecture_registry() -> rx.Component:
    section = _section_by_id("architecture_registry")
    return page_shell(
        section["title"],
        "Réconciliation architecture, registry technique et modules actifs.",
        _registry_body(
            section["title"],
            section["route"],
            "Cette page finalisera les registres Architecture & Registry : routes, modules, docs, exports, runtime et sécurité.",
        ),
        section["route"],
    )


def lexique_knowledge() -> rx.Component:
    return page_shell(
        "Lexique Knowledge",
        "Knowledge base lexique-first.",
        _registry_body(
            "Lexique Knowledge",
            "/lexique-knowledge",
            "Structure prête pour termes, catégories, méthodes et signaux.",
        ),
        "/lexique-knowledge",
    )


def prompt_lab() -> rx.Component:
    return page_shell(
        "Prompt Lab",
        "Atelier prompt / GEM / human review.",
        _registry_body(
            "Prompt Lab",
            "/prompt-lab",
            "Structure prête pour prompts, context packs, réponse GEM et review queue.",
        ),
        "/prompt-lab",
    )


def gem_portfolio() -> rx.Component:
    return page_shell(
        "GEM Portfolio",
        "Capture portefeuille et revue multimodale.",
        _registry_body(
            "GEM Portfolio",
            "/gem-portfolio",
            "Structure prête pour captures, JSON, résumé lisible et human review.",
        ),
        "/gem-portfolio",
    )


def _qaic_bridge_body() -> rx.Component:
    card = build_qaic_bridge_operator_card()
    safety = card["safety"]
    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.heading(card["title"], size="5"),
                rx.text(card["contract_id"], size="3"),
                rx.text("Route: " + card["route"], size="2"),
                rx.text("Mode: " + card["mode"], size="2"),
                rx.text("Status: " + card["status"], size="2"),
                rx.text(
                    "Source: "
                    + card["source_system"]
                    + " / Target: "
                    + card["target_system"],
                    size="2",
                ),
                rx.text("Human review required: " + str(safety["human_review_required"]).lower(), size="2"),
                rx.text("QAIC execution allowed: " + str(safety["qaic_execution_allowed"]).lower(), size="2"),
                rx.text("No runtime: " + str(safety["no_runtime"]).lower(), size="2"),
                rx.text("No provider call: " + str(safety["no_provider_call"]).lower(), size="2"),
                rx.text(
                    "No broker/order sizing: "
                    + str(safety["no_broker_order_sizing"]).lower(),
                    size="2",
                ),
                rx.text("No Sheet/BQ write: " + str(safety["no_sheet_bq_write"]).lower(), size="2"),
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


def qaic_bridge() -> rx.Component:
    return page_shell(
        "QAIC Bridge",
        "Liaison future read-only vers backend QAIC prive.",
        _qaic_bridge_body(),
        "/qaic-bridge",
    )


def settings_safety() -> rx.Component:
    return page_shell(
        "Settings Safety",
        "Thèmes, sécurité, plugins et garde-fous.",
        _registry_body(
            "Settings Safety",
            "/settings-safety",
            "Structure prête pour light/dark/system, accent, density, safety flags et plugins Reflex.",
        ),
        "/settings-safety",
    )


# BEGIN_R6M_R7_AUTO_LIVE_DEV_TRACKING_OVERRIDE
# R6M used dev_lifecycle_tracker_page before R6N promoted the vertical panel.
# END_R6M_R7_AUTO_LIVE_DEV_TRACKING_OVERRIDE


# R6N-R5_BEGIN_VERTICAL_MIGRATION_STYLE_DEV_TRACKING
def dev_tracking_page() -> Any:
    if rx is None:
        return _r6n_vertical_dev_lifecycle_tracker_panel(compact=False, context="dev")
    return rx.box(
        _r6n_vertical_dev_lifecycle_tracker_panel(compact=False, context="dev"),
        padding="1em",
        width="100%",
    )


# R6N-R5_END_VERTICAL_MIGRATION_STYLE_DEV_TRACKING
