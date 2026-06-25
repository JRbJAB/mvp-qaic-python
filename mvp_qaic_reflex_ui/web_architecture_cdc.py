"""Web architecture CDC and visual sitemap components."""

from __future__ import annotations

from collections.abc import Mapping

import reflex as rx

from .theme import status_pill
from .visual_theme import metric_grid

WEB_ARCHITECTURE_SCHEMA_ASSET = "/mvp_qaic_web_architecture_schema.svg"
WEB_ARCHITECTURE_DOCS = {
    "cdc": "docs/WEB_ARCHITECTURE_CDC.md",
    "sitemap": "docs/WEB_ARCHITECTURE_SITEMAP.json",
    "schema": "docs/WEB_ARCHITECTURE_SCHEMA.svg",
    "asset": "assets/mvp_qaic_web_architecture_schema.svg",
}
SITEMAP_PLUGIN_STATUS = "EXPLICIT_ENABLED"

SITEMAP_NODES = [
    {
        "id": "home",
        "title": "Home / Mission Control",
        "route": "/",
        "layer": "Mission",
        "status": "PRIVATE_READY",
        "progress_percent": 85,
        "description": "Landing opérateur, KPI, navigation principale.",
    },
    {
        "id": "dev_tracking",
        "title": "Dev Tracking",
        "route": "/dev-tracking",
        "layer": "Operations",
        "status": "STRUCTURE_READY",
        "progress_percent": 45,
        "description": "Suivi lots Pxxx, commits, tags, gates et dette.",
    },
    {
        "id": "cdc_tracker",
        "title": "CDC Tracker",
        "route": "/cdc-tracker",
        "layer": "Governance",
        "status": "STRUCTURE_READY",
        "progress_percent": 60,
        "description": "CDC produit, décisions, gaps, validations.",
    },
    {
        "id": "architecture_web",
        "title": "Architecture Web",
        "route": "/architecture-web",
        "layer": "Architecture",
        "status": "ACTIVE",
        "progress_percent": 70,
        "description": "Schéma pro, sitemap, CDC tracker et cockpit registry.",
    },
    {
        "id": "sitemap",
        "title": "Visual Sitemap",
        "route": "/sitemap",
        "layer": "Architecture",
        "status": "ACTIVE",
        "progress_percent": 65,
        "description": "Vue dédiée du schéma et des routes Reflex.",
    },
    {
        "id": "documentation_registry",
        "title": "Documentation Registry",
        "route": "/documentation-registry",
        "layer": "Documentation",
        "status": "STRUCTURE_READY",
        "progress_percent": 45,
        "description": "Registre docs, exports, prompts, preuves et versions.",
    },
    {
        "id": "architecture_registry",
        "title": "Architecture & Registry",
        "route": "/architecture-registry",
        "layer": "Architecture",
        "status": "TO_STRUCTURE",
        "progress_percent": 45,
        "description": "Registry modules, routes, données, cockpits et contrats.",
    },
    {
        "id": "admin_center",
        "title": "Admin Center",
        "route": "/admin",
        "layer": "Admin",
        "status": "PRIVATE_READY",
        "progress_percent": 75,
        "description": "Administration privée runtime, thème, routes, data binding.",
    },
    {
        "id": "admin_theme",
        "title": "Theme Settings",
        "route": "/admin/theme",
        "layer": "Admin",
        "status": "PRIVATE_READY",
        "progress_percent": 85,
        "description": "Thème global, toggle clair/sombre, localStorage.",
    },
    {
        "id": "admin_runtime",
        "title": "Runtime Admin",
        "route": "/admin/runtime",
        "layer": "Admin",
        "status": "PRIVATE_READY",
        "progress_percent": 80,
        "description": "Runtime privé Reflex frontend/backend.",
    },
    {
        "id": "admin_routes",
        "title": "Routes Admin",
        "route": "/admin/routes",
        "layer": "Admin",
        "status": "PRIVATE_READY",
        "progress_percent": 75,
        "description": "Inventaire routes Reflex.",
    },
    {
        "id": "admin_data_binding",
        "title": "Data Binding Admin",
        "route": "/admin/data-binding",
        "layer": "Admin",
        "status": "PRIVATE_READY",
        "progress_percent": 70,
        "description": "Binding local readonly docs/exports.",
    },
    {
        "id": "prompt_lab",
        "title": "Prompt Lab",
        "route": "/prompt-lab",
        "layer": "Product",
        "status": "STRUCTURE_READY",
        "progress_percent": 45,
        "description": "Prompts, GEM, human review, payloads.",
    },
    {
        "id": "gem_portfolio",
        "title": "GEM Portfolio",
        "route": "/gem-portfolio",
        "layer": "Product",
        "status": "STRUCTURE_READY",
        "progress_percent": 35,
        "description": "Capture portefeuille, JSON, revue humaine.",
    },
    {
        "id": "lexique",
        "title": "Lexique Knowledge",
        "route": "/lexique-knowledge",
        "layer": "Knowledge",
        "status": "STRUCTURE_READY",
        "progress_percent": 40,
        "description": "Lexique, concepts, méthode publique future.",
    },
    {
        "id": "qaic_bridge",
        "title": "QAIC Bridge",
        "route": "/qaic-bridge",
        "layer": "Private Bridge",
        "status": "REVIEW_ONLY",
        "progress_percent": 25,
        "description": "Lien futur read-only vers backend QAIC privé.",
    },
    {
        "id": "settings_safety",
        "title": "Settings Safety",
        "route": "/settings-safety",
        "layer": "Safety",
        "status": "STRUCTURE_READY",
        "progress_percent": 50,
        "description": "Rappels sécurité, limites MVP/QAIC.",
    },
]

CDC_TRACKER_ROWS = [
    {
        "cdc_id": "CDC-001",
        "section": "Landing",
        "title": "Home / Mission Control",
        "route": "/",
        "cockpit": "Mission Control",
        "status": "PRIVATE_READY",
        "progress_percent": 85,
        "evidence": "P07/P10",
        "next_action": "Brancher indicateurs réels MVP.",
    },
    {
        "cdc_id": "CDC-002",
        "section": "Tracking",
        "title": "Dev Tracking",
        "route": "/dev-tracking",
        "cockpit": "Dev Cockpit",
        "status": "STRUCTURE_READY",
        "progress_percent": 45,
        "evidence": "P07",
        "next_action": "Connecter historique lots/tags/exports.",
    },
    {
        "cdc_id": "CDC-003",
        "section": "CDC",
        "title": "CDC Tracker",
        "route": "/cdc-tracker",
        "cockpit": "CDC Cockpit",
        "status": "STRUCTURE_READY",
        "progress_percent": 60,
        "evidence": "P12A-R1",
        "next_action": "Ajouter décisions, owners, blockers.",
    },
    {
        "cdc_id": "CDC-004",
        "section": "Architecture",
        "title": "Architecture Web",
        "route": "/architecture-web",
        "cockpit": "Architecture Cockpit",
        "status": "ACTIVE",
        "progress_percent": 70,
        "evidence": "P12A-R1",
        "next_action": "Finaliser flux data et contrats.",
    },
    {
        "cdc_id": "CDC-005",
        "section": "Sitemap",
        "title": "Visual Sitemap",
        "route": "/sitemap",
        "cockpit": "Sitemap Cockpit",
        "status": "ACTIVE",
        "progress_percent": 65,
        "evidence": "P12A-R1 + SitemapPlugin",
        "next_action": "Review visuelle et enrichissement liens.",
    },
    {
        "cdc_id": "CDC-006",
        "section": "Documentation",
        "title": "Documentation Registry",
        "route": "/documentation-registry",
        "cockpit": "Docs Registry",
        "status": "STRUCTURE_READY",
        "progress_percent": 45,
        "evidence": "P07",
        "next_action": "Indexer docs et exports utiles.",
    },
    {
        "cdc_id": "CDC-007",
        "section": "Registry",
        "title": "Architecture & Registry",
        "route": "/architecture-registry",
        "cockpit": "Registry Cockpit",
        "status": "TO_STRUCTURE",
        "progress_percent": 45,
        "evidence": "P07",
        "next_action": "Finaliser registry routes/modules/docs.",
    },
    {
        "cdc_id": "CDC-008",
        "section": "Admin",
        "title": "Admin Center",
        "route": "/admin",
        "cockpit": "Admin Cockpit",
        "status": "PRIVATE_READY",
        "progress_percent": 75,
        "evidence": "P08/P10",
        "next_action": "Ajouter contrôle qualité runtime détaillé.",
    },
    {
        "cdc_id": "CDC-009",
        "section": "Admin",
        "title": "Runtime Admin",
        "route": "/admin/runtime",
        "cockpit": "Runtime Cockpit",
        "status": "PRIVATE_READY",
        "progress_percent": 80,
        "evidence": "P08/P11B",
        "next_action": "Ajouter smoke history et incidents.",
    },
    {
        "cdc_id": "CDC-010",
        "section": "Admin",
        "title": "Theme Admin",
        "route": "/admin/theme",
        "cockpit": "Theme Cockpit",
        "status": "PRIVATE_READY",
        "progress_percent": 85,
        "evidence": "P10/P11D",
        "next_action": "Runtime persistence smoke.",
    },
    {
        "cdc_id": "CDC-011",
        "section": "Prompt",
        "title": "Prompt Lab",
        "route": "/prompt-lab",
        "cockpit": "Prompt Cockpit",
        "status": "STRUCTURE_READY",
        "progress_percent": 45,
        "evidence": "P07",
        "next_action": "Brancher prompts P132/P133/P157.",
    },
    {
        "cdc_id": "CDC-012",
        "section": "GEM",
        "title": "GEM Portfolio",
        "route": "/gem-portfolio",
        "cockpit": "GEM Review Cockpit",
        "status": "STRUCTURE_READY",
        "progress_percent": 35,
        "evidence": "P07",
        "next_action": "Brancher import capture et revue JSON.",
    },
    {
        "cdc_id": "CDC-013",
        "section": "Lexique",
        "title": "Lexique Knowledge",
        "route": "/lexique-knowledge",
        "cockpit": "Knowledge Cockpit",
        "status": "STRUCTURE_READY",
        "progress_percent": 40,
        "evidence": "P07",
        "next_action": "Brancher lexique validé et méthode publique.",
    },
    {
        "cdc_id": "CDC-014",
        "section": "Bridge",
        "title": "QAIC Bridge",
        "route": "/qaic-bridge",
        "cockpit": "QAIC Bridge Cockpit",
        "status": "REVIEW_ONLY",
        "progress_percent": 25,
        "evidence": "Boundary MVP/QAIC",
        "next_action": "Contrat read-only uniquement.",
    },
    {
        "cdc_id": "CDC-015",
        "section": "Safety",
        "title": "Settings Safety",
        "route": "/settings-safety",
        "cockpit": "Safety Cockpit",
        "status": "STRUCTURE_READY",
        "progress_percent": 50,
        "evidence": "Safety policy",
        "next_action": "Centraliser limites public/privé.",
    },
]

COCKPIT_REGISTRY_ROWS = [
    {
        "cockpit": "Mission Control",
        "route": "/",
        "purpose": "Pilotage opérateur global.",
        "priority": "P0",
        "status": "PRIVATE_READY",
    },
    {
        "cockpit": "Architecture Cockpit",
        "route": "/architecture-web",
        "purpose": "Schéma, sitemap, CDC et architecture cible.",
        "priority": "P0",
        "status": "ACTIVE",
    },
    {
        "cockpit": "CDC Cockpit",
        "route": "/cdc-tracker",
        "purpose": "Exigences, avancement, blockers, décisions.",
        "priority": "P0",
        "status": "STRUCTURE_READY",
    },
    {
        "cockpit": "Docs Registry",
        "route": "/documentation-registry",
        "purpose": "Inventaire docs, exports, prompts, preuves.",
        "priority": "P0",
        "status": "STRUCTURE_READY",
    },
    {
        "cockpit": "Admin Cockpit",
        "route": "/admin",
        "purpose": "Runtime, thème, routes, data binding.",
        "priority": "P0",
        "status": "PRIVATE_READY",
    },
    {
        "cockpit": "Prompt/GEM Cockpit",
        "route": "/prompt-lab",
        "purpose": "Prompt workflows et revue GEM.",
        "priority": "P1",
        "status": "STRUCTURE_READY",
    },
    {
        "cockpit": "Lexique Cockpit",
        "route": "/lexique-knowledge",
        "purpose": "Concepts, méthode, pédagogie publique future.",
        "priority": "P1",
        "status": "STRUCTURE_READY",
    },
    {
        "cockpit": "QAIC Bridge Cockpit",
        "route": "/qaic-bridge",
        "purpose": "Pont futur read-only vers QAIC privé.",
        "priority": "P1",
        "status": "REVIEW_ONLY",
    },
]


def cdc_progress_average() -> float:
    return round(
        sum(row["progress_percent"] for row in CDC_TRACKER_ROWS) / len(CDC_TRACKER_ROWS),
        2,
    )


def architecture_summary_metrics() -> tuple[dict[str, str], ...]:
    return (
        {
            "label": "CDC progress",
            "value": f"{cdc_progress_average()}%",
            "detail": f"{len(CDC_TRACKER_ROWS)} tracked CDC rows.",
            "tone": "accent",
        },
        {
            "label": "Sitemap nodes",
            "value": str(len(SITEMAP_NODES)),
            "detail": "Routes and modules mapped.",
            "tone": "success",
        },
        {
            "label": "Cockpits",
            "value": str(len(COCKPIT_REGISTRY_ROWS)),
            "detail": "Essential cockpits to structure.",
            "tone": "accent",
        },
        {
            "label": "Sitemap plugin",
            "value": "ON",
            "detail": "SitemapPlugin explicit in rxconfig.",
            "tone": "success",
        },
    )


def architecture_schema_panel() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading("Schema pro — Web Architecture & Sitemap", size="5"),
                    rx.text(
                        "Carte visuelle versionnee: pages Reflex, cockpits, "
                        "data contracts, runtime, safety gates et statut CDC.",
                        size="3",
                        color="var(--gray-11)",
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                status_pill("SVG_VERSIONED", "ok"),
                status_pill("SITEMAP_PLUGIN_ON", "ok"),
                spacing="2",
                align="center",
                width="100%",
            ),
            rx.image(
                src=WEB_ARCHITECTURE_SCHEMA_ASSET,
                alt="MVP QAIC Web Architecture CDC and Visual Sitemap",
                width="100%",
                border_radius="16px",
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        border="1px solid var(--gray-6)",
        border_radius="20px",
        padding="1rem",
        width="100%",
        background="var(--gray-2)",
    )


def _status_level(status: object) -> str:
    value = str(status)
    if value in {"ACTIVE", "PRIVATE_READY"}:
        return "ok"
    if value in {"TO_STRUCTURE", "STRUCTURE_READY", "REVIEW_ONLY"}:
        return "warning"
    return "info"


def _cdc_grid_header() -> rx.Component:
    return rx.grid(
        rx.text("CDC", size="2", weight="bold"),
        rx.text("Section", size="2", weight="bold"),
        rx.text("Route", size="2", weight="bold"),
        rx.text("Cockpit", size="2", weight="bold"),
        rx.text("Status", size="2", weight="bold"),
        rx.text("Progress", size="2", weight="bold"),
        rx.text("Next", size="2", weight="bold"),
        columns="7",
        spacing="3",
        width="100%",
        padding="0.65rem",
        background="var(--gray-3)",
        border_radius="12px",
    )


def _cdc_grid_row(row: Mapping[str, object]) -> rx.Component:
    return rx.grid(
        rx.text(str(row["cdc_id"]), size="2", weight="bold"),
        rx.text(str(row["section"]), size="2"),
        rx.link(str(row["route"]), href=str(row["route"]), size="2"),
        rx.text(str(row["cockpit"]), size="2"),
        status_pill(str(row["status"]), _status_level(row["status"])),
        rx.text(f"{row['progress_percent']}%", size="2", weight="bold"),
        rx.text(str(row["next_action"]), size="2"),
        columns="7",
        spacing="3",
        width="100%",
        padding="0.65rem",
        border_bottom="1px solid var(--gray-5)",
    )


def cdc_tracker_table() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("CDC Tracker — routes, cockpits, % realise", size="5"),
                rx.spacer(),
                status_pill(f"AVG={cdc_progress_average()}%", "info"),
                status_pill(f"ROWS={len(CDC_TRACKER_ROWS)}", "info"),
                width="100%",
            ),
            _cdc_grid_header(),
            *[_cdc_grid_row(row) for row in CDC_TRACKER_ROWS],
            spacing="2",
            align="start",
            width="100%",
        ),
        border="1px solid var(--gray-6)",
        border_radius="20px",
        padding="1rem",
        width="100%",
        background="var(--gray-1)",
    )


def _cockpit_card(row: Mapping[str, object]) -> rx.Component:
    return rx.link(
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(str(row["cockpit"]), weight="bold", size="3"),
                    rx.spacer(),
                    status_pill(str(row["priority"]), "info"),
                    width="100%",
                ),
                rx.text(str(row["purpose"]), size="2", color="var(--gray-11)"),
                rx.hstack(
                    status_pill(str(row["status"]), _status_level(row["status"])),
                    rx.text(str(row["route"]), size="2"),
                    spacing="2",
                    wrap="wrap",
                ),
                spacing="3",
                align="start",
                width="100%",
            ),
            border="1px solid var(--gray-6)",
            border_radius="16px",
            padding="1rem",
            background="var(--gray-2)",
            width="100%",
        ),
        href=str(row["route"]),
        text_decoration="none",
        width="100%",
    )


def cockpit_registry_grid() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Cockpits essentiels a envisager / structurer", size="5"),
            rx.grid(
                *[_cockpit_card(row) for row in COCKPIT_REGISTRY_ROWS],
                columns="2",
                spacing="4",
                width="100%",
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        border="1px solid var(--gray-6)",
        border_radius="20px",
        padding="1rem",
        width="100%",
        background="var(--gray-1)",
    )


def architecture_docs_panel() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Source de verite architecture", size="5"),
            rx.text("Artifacts versionnes pour CDC, sitemap et schema SVG.", size="3"),
            *[
                rx.hstack(
                    rx.text(key, size="2", weight="bold", min_width="90px"),
                    rx.code(value, size="2"),
                    spacing="3",
                    align="center",
                )
                for key, value in WEB_ARCHITECTURE_DOCS.items()
            ],
            rx.hstack(
                status_pill("NO_PUBLIC_DEPLOY", "ok"),
                status_pill("NO_BROKER", "ok"),
                status_pill("NO_SHEET_WRITE", "ok"),
                status_pill("NO_BIGQUERY_WRITE", "ok"),
                spacing="2",
                wrap="wrap",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        border="1px solid var(--gray-6)",
        border_radius="20px",
        padding="1rem",
        width="100%",
        background="var(--gray-2)",
    )


def architecture_web_cdc_body() -> rx.Component:
    return rx.vstack(
        architecture_schema_panel(),
        metric_grid(architecture_summary_metrics()),
        cdc_tracker_table(),
        cockpit_registry_grid(),
        architecture_docs_panel(),
        spacing="5",
        align="start",
        width="100%",
    )


def sitemap_page_body() -> rx.Component:
    return rx.vstack(
        architecture_schema_panel(),
        rx.heading("Sitemap nodes", size="5"),
        rx.grid(
            *[
                rx.link(
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text(str(node["layer"]), size="2", weight="bold"),
                                rx.spacer(),
                                status_pill(
                                    str(node["status"]),
                                    _status_level(node["status"]),
                                ),
                                width="100%",
                            ),
                            rx.heading(str(node["title"]), size="4"),
                            rx.text(str(node["description"]), size="2"),
                            rx.text(str(node["route"]), size="2", weight="bold"),
                            rx.text(
                                f"{node['progress_percent']}% realise",
                                size="2",
                                color="var(--gray-11)",
                            ),
                            spacing="3",
                            align="start",
                            width="100%",
                        ),
                        border="1px solid var(--gray-6)",
                        border_radius="16px",
                        padding="1rem",
                        background="var(--gray-2)",
                        width="100%",
                    ),
                    href=str(node["route"]),
                    text_decoration="none",
                    width="100%",
                )
                for node in SITEMAP_NODES
            ],
            columns="3",
            spacing="4",
            width="100%",
        ),
        architecture_docs_panel(),
        spacing="5",
        align="start",
        width="100%",
    )
