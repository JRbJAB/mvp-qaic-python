"""Mission Control migration tracker for Sheets and Apps Script migration."""

from __future__ import annotations

from collections.abc import Mapping

import reflex as rx

from .theme import status_pill

MIGRATION_TRACKER_DOCS = {
    "json": "docs/MIGRATION_TRACKER.json",
    "markdown": "docs/MIGRATION_TRACKER.md",
}

MIGRATION_TRACKER_ROWS = [
    {
        "migration_id": "MIG-001",
        "source_type": "SHEET_TAB",
        "source_name": "LEXIQUE_CRYPTO_APPROVED",
        "target": "/lexique-knowledge",
        "scope": "Lexique KB",
        "status": "STRUCTURE_READY",
        "progress_percent": 40,
        "priority": "P0",
        "next_action": "Brancher export lexique validé + catégories + recherche.",
    },
    {
        "migration_id": "MIG-002",
        "source_type": "SHEET_TAB",
        "source_name": "GPT_QUALITY_DASHBOARD",
        "target": "/prompt-lab",
        "scope": "Prompt quality",
        "status": "TO_MIGRATE",
        "progress_percent": 30,
        "priority": "P0",
        "next_action": "Migrer métriques qualité prompt/GEM en cockpit Reflex.",
    },
    {
        "migration_id": "MIG-003",
        "source_type": "SHEET_TAB",
        "source_name": "PROMPT_IMPROVEMENT_QUEUE",
        "target": "/prompt-lab",
        "scope": "Prompt correction loop",
        "status": "TO_MIGRATE",
        "progress_percent": 30,
        "priority": "P0",
        "next_action": "Lister corrections, statuts, priorités et human review.",
    },
    {
        "migration_id": "MIG-004",
        "source_type": "SHEET_TAB",
        "source_name": "DECISION_JOURNAL",
        "target": "/cdc-tracker",
        "scope": "Decision journal",
        "status": "PARTIAL",
        "progress_percent": 45,
        "priority": "P0",
        "next_action": "Créer journal web read-only avec décisions, blockers, evidence.",
    },
    {
        "migration_id": "MIG-005",
        "source_type": "SHEET_TAB",
        "source_name": "QAIC_RUNTIME_COCKPIT_VIEW",
        "target": "/admin/runtime",
        "scope": "Runtime cockpit",
        "status": "PARTIAL",
        "progress_percent": 70,
        "priority": "P0",
        "next_action": "Brancher historique smoke/runtime et incidents.",
    },
    {
        "migration_id": "MIG-006",
        "source_type": "SHEET_TAB",
        "source_name": "QAIC_RUNTIME_BRIDGE_STATUS",
        "target": "/qaic-bridge",
        "scope": "MVP/QAIC bridge",
        "status": "REVIEW_ONLY",
        "progress_percent": 35,
        "priority": "P1",
        "next_action": "Contrat read-only, pas de broker/order/sizing.",
    },
    {
        "migration_id": "MIG-007",
        "source_type": "SHEET_TAB",
        "source_name": "🎛️ BENCHMARK_AI_TRADE",
        "target": "/prompt-lab",
        "scope": "Benchmark prompt/GEM",
        "status": "TO_MIGRATE",
        "progress_percent": 30,
        "priority": "P1",
        "next_action": "Migrer benchmark en lecture locale avec scoring compact.",
    },
    {
        "migration_id": "MIG-008",
        "source_type": "APPS_SCRIPT_FILE",
        "source_name": "mvpqaic_09_p1_journal_core.gs",
        "target": "/cdc-tracker",
        "scope": "Journal core",
        "status": "PARTIAL",
        "progress_percent": 50,
        "priority": "P0",
        "next_action": "Porter logique idempotence/journal en Python local review-only.",
    },
    {
        "migration_id": "MIG-009",
        "source_type": "APPS_SCRIPT_FUNCTION",
        "source_name": "Decision journal append / duplicate guard",
        "target": "/cdc-tracker",
        "scope": "Journal idempotence",
        "status": "PARTIAL",
        "progress_percent": 45,
        "priority": "P0",
        "next_action": "Formaliser tests duplicate guard côté Python.",
    },
    {
        "migration_id": "MIG-010",
        "source_type": "FUNCTIONALITY",
        "source_name": "P132/P133 GEM portfolio multimodal prompt",
        "target": "/gem-portfolio",
        "scope": "GEM portfolio review",
        "status": "STRUCTURE_READY",
        "progress_percent": 55,
        "priority": "P0",
        "next_action": "UI import capture + réponse GEM + revue humaine.",
    },
    {
        "migration_id": "MIG-011",
        "source_type": "FUNCTIONALITY",
        "source_name": "Prompt correction loop P153/P154/P155/P159",
        "target": "/prompt-lab",
        "scope": "Prompt workbench",
        "status": "STRUCTURE_READY",
        "progress_percent": 50,
        "priority": "P0",
        "next_action": "Brancher actions correction + apply gate review-only.",
    },
    {
        "migration_id": "MIG-012",
        "source_type": "FUNCTIONALITY",
        "source_name": "Safety gates no-order/no-sizing/no-public-deploy",
        "target": "/settings-safety",
        "scope": "Safety cockpit",
        "status": "PRIVATE_READY",
        "progress_percent": 80,
        "priority": "P0",
        "next_action": "Centraliser affichage et audit sécurité.",
    },
    {
        "migration_id": "MIG-013",
        "source_type": "DOC_EXPORT",
        "source_name": "WEB_ARCHITECTURE_CDC.md / SITEMAP.json / SCHEMA.svg",
        "target": "/architecture-web",
        "scope": "Architecture CDC",
        "status": "ACTIVE",
        "progress_percent": 85,
        "priority": "P0",
        "next_action": "Review visuelle + enrichissement data contracts.",
    },
    {
        "migration_id": "MIG-014",
        "source_type": "INVENTORY",
        "source_name": "MVPQAIC_CLASP_IMPORTS_ALL.csv",
        "target": "/architecture-registry",
        "scope": "Apps Script inventory",
        "status": "TO_BIND",
        "progress_percent": 20,
        "priority": "P0",
        "next_action": "Importer inventaire scripts/fonctions pour tracker exhaustif.",
    },
    {
        "migration_id": "MIG-015",
        "source_type": "INVENTORY",
        "source_name": "MVPQAIC_CLASP_IMPORTS_ALL_HEADERS.csv",
        "target": "/architecture-registry",
        "scope": "Headers/contracts",
        "status": "TO_BIND",
        "progress_percent": 20,
        "priority": "P1",
        "next_action": "Mapper headers Sheets vers contrats Reflex/Python.",
    },
]


def migration_average_progress() -> float:
    return round(
        sum(row["progress_percent"] for row in MIGRATION_TRACKER_ROWS)
        / len(MIGRATION_TRACKER_ROWS),
        2,
    )


def _status_level(status: object) -> str:
    value = str(status)
    if value in {"ACTIVE", "PRIVATE_READY"}:
        return "ok"
    if value in {"PARTIAL", "STRUCTURE_READY", "REVIEW_ONLY", "TO_BIND"}:
        return "warning"
    if value in {"TO_MIGRATE"}:
        return "info"
    return "info"


def build_migration_tracker_payload() -> dict[str, object]:
    return {
        "tracker_status": "READY_COMPACT_MISSION_PANEL",
        "row_count": len(MIGRATION_TRACKER_ROWS),
        "average_progress": migration_average_progress(),
        "source_scope": "Sheets + Apps Script + exported docs",
        "mission_route": "/",
        "public_deploy": False,
        "broker_order_sizing": False,
        "sheet_write": False,
        "bigquery_write": False,
        "rows": [dict(row) for row in MIGRATION_TRACKER_ROWS],
    }


def migration_tracker_summary_rows() -> dict[str, object]:
    payload = build_migration_tracker_payload()
    return {
        "tracker_status": payload["tracker_status"],
        "row_count": payload["row_count"],
        "average_progress": f"{payload['average_progress']}%",
        "source_scope": payload["source_scope"],
        "sheet_write": payload["sheet_write"],
        "bigquery_write": payload["bigquery_write"],
    }


def _progress_bar(value: object) -> rx.Component:
    pct = int(value)
    return rx.box(
        rx.box(
            height="8px",
            width=f"{pct}%",
            background="var(--accent-9)",
            border_radius="999px",
        ),
        width="100%",
        background="var(--gray-4)",
        border_radius="999px",
        overflow="hidden",
    )


def _migration_grid_header() -> rx.Component:
    return rx.grid(
        rx.text("Type", size="1", weight="bold"),
        rx.text("Source", size="1", weight="bold"),
        rx.text("Cible", size="1", weight="bold"),
        rx.text("%", size="1", weight="bold"),
        rx.text("Statut", size="1", weight="bold"),
        columns="5",
        spacing="2",
        width="100%",
        padding="0.5rem",
        background="var(--gray-3)",
        border_radius="12px",
    )


def _migration_grid_row(row: Mapping[str, object]) -> rx.Component:
    return rx.grid(
        rx.text(str(row["source_type"]), size="1", color="var(--gray-11)"),
        rx.vstack(
            rx.text(str(row["source_name"]), size="1", weight="bold"),
            rx.text(str(row["scope"]), size="1", color="var(--gray-11)"),
            spacing="1",
            align="start",
        ),
        rx.link(str(row["target"]), href=str(row["target"]), size="1"),
        rx.vstack(
            rx.text(f"{row['progress_percent']}%", size="1", weight="bold"),
            _progress_bar(row["progress_percent"]),
            spacing="1",
            align="start",
            width="100%",
        ),
        status_pill(str(row["status"]), _status_level(row["status"])),
        columns="5",
        spacing="2",
        width="100%",
        padding="0.5rem",
        border_bottom="1px solid var(--gray-5)",
        align_items="center",
    )


def migration_tracker_compact_panel() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading("Migration Tracker — Sheets / Apps Script → Reflex", size="5"),
                    rx.text(
                        "Onglets, scripts, fonctions et fonctionnalités essentielles à migrer.",
                        size="2",
                        color="var(--gray-11)",
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                status_pill(f"AVG={migration_average_progress()}%", "info"),
                status_pill(f"ROWS={len(MIGRATION_TRACKER_ROWS)}", "info"),
                width="100%",
                align="center",
            ),
            rx.box(
                rx.vstack(
                    _migration_grid_header(),
                    *[_migration_grid_row(row) for row in MIGRATION_TRACKER_ROWS],
                    spacing="0",
                    width="100%",
                ),
                width="100%",
                overflow_x="hidden",
            ),
            rx.hstack(
                status_pill("NO_SHEET_WRITE", "ok"),
                status_pill("NO_BIGQUERY_WRITE", "ok"),
                status_pill("NO_BROKER", "ok"),
                status_pill("HUMAN_REVIEW", "ok"),
                spacing="2",
                wrap="wrap",
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
