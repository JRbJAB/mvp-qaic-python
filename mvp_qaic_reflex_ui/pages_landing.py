"""Landing and priority pages for MVP QAIC Reflex."""

from __future__ import annotations

import reflex as rx

from .layout import page_shell, placeholder_body
from .theme import LANDING_SECTIONS, get_landing_sections, safety_panel, section_card, status_pill


def _section_by_id(section_id: str) -> dict[str, str]:
    for section in LANDING_SECTIONS:
        if section["section_id"] == section_id:
            return dict(section)
    raise KeyError(section_id)


def home() -> rx.Component:
    sections = get_landing_sections()
    return page_shell(
        "🏠 Home / Mission Control",
        "Landing page opérateur pour piloter le MVP QAIC Reflex.",
        rx.vstack(
            rx.box(
                rx.vstack(
                    rx.heading("Mission Control", size="6"),
                    rx.text(
                        "Priorité actuelle : structurer l'accueil, le suivi dev, le CDC, "
                        "l'architecture web, la documentation registry et l'architecture registry.",
                        size="3",
                    ),
                    rx.hstack(
                        status_pill("APP_RUNNING_LOCAL", "ok"),
                        status_pill("REFLEX_FOUNDATION", "ok"),
                        status_pill("THEME_FOUNDATION", "ok"),
                        status_pill("ADMIN_NEXT", "warning"),
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
            safety_panel(),
            rx.heading("Sections prioritaires", size="5"),
            rx.vstack(
                *[section_card(section) for section in sections],
                spacing="3",
                width="100%",
                align="start",
            ),
            spacing="4",
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
        "Architecture WebApp Reflex, routes, composants et couches données.",
        placeholder_body(
            section["title"],
            section["route"],
            "Cette page cartographiera landing, admin, lexique, prompt lab, GEM portfolio et future exposition publique.",
        ),
        section["route"],
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
