"""Landing and priority pages for MVP QAIC Reflex."""

from __future__ import annotations

import reflex as rx

from .layout import page_shell, placeholder_body
from .migration_tracker import migration_tracker_compact_panel
from .theme import LANDING_SECTIONS, get_landing_sections, safety_panel, section_card
from .visual_theme import metric_grid, mission_control_hero
from .web_architecture_cdc import architecture_web_cdc_body, sitemap_page_body


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
    section = _section_by_id("dev_tracking")
    return page_shell(
        section["title"],
        "Suivi des lots, gates, tests, tags et dette technique.",
        placeholder_body(
            section["title"],
            section["route"],
            "Cette page consolidera HEAD Git, statut remote, tags, tests, Ruff, runtime Reflex et prochaines actions.",
        ),
        section["route"],
    )


def cdc_tracker() -> rx.Component:
    section = _section_by_id("cdc_tracker")
    return page_shell(
        section["title"],
        "Pilotage CDC WebApp / MVP / QAIC liaison.",
        placeholder_body(
            section["title"],
            section["route"],
            "Cette page consolidera les exigences, décisions, livrables, gaps et validations CDC.",
        ),
        section["route"],
    )


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
        placeholder_body(
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
        placeholder_body(
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
        placeholder_body(
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
        placeholder_body(
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
        placeholder_body(
            "GEM Portfolio",
            "/gem-portfolio",
            "Structure prête pour captures, JSON, résumé lisible et human review.",
        ),
        "/gem-portfolio",
    )


def qaic_bridge() -> rx.Component:
    return page_shell(
        "QAIC Bridge",
        "Liaison future read-only vers backend QAIC privé.",
        placeholder_body(
            "QAIC Bridge",
            "/qaic-bridge",
            "Structure prête pour statut, contrats et liaison read-only. Aucun ordre.",
        ),
        "/qaic-bridge",
    )


def settings_safety() -> rx.Component:
    return page_shell(
        "Settings Safety",
        "Thèmes, sécurité, plugins et garde-fous.",
        placeholder_body(
            "Settings Safety",
            "/settings-safety",
            "Structure prête pour light/dark/system, accent, density, safety flags et plugins Reflex.",
        ),
        "/settings-safety",
    )
