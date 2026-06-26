from __future__ import annotations
from pathlib import Path
from typing import Any
from mvp_qaic_reflex_ui.migration_global_matrix import build_matrix

try:
    import reflex as rx
except Exception:  # noqa: BLE001
    rx = None  # type: ignore[assignment]
GLOBAL_MIGRATION_ROUTE = "/migration/global"


def _require_reflex() -> Any:
    if rx is None:
        raise RuntimeError("reflex is required to render this page")
    return rx


def _rows(rows, scope, limit):
    return [r for r in rows if r.get("scope") == scope][:limit]


def global_migration_page() -> Any:
    reflex = _require_reflex()
    payload = build_matrix(Path.cwd())
    summary = payload.get("summary", {})
    rows = payload.get("rows", [])
    cockpit = _rows(rows, "SHEETS_COCKPIT", 50)
    future = _rows(rows, "FUTURE_ARCHITECTURE", 20)
    scripts = sorted(
        [r for r in rows if r.get("scope") == "APPS_SCRIPT_FILE"],
        key=lambda r: int(r.get("risk_score") or 0),
        reverse=True,
    )[:35]

    def card(r):
        return reflex.card(
            reflex.vstack(
                reflex.hstack(
                    reflex.badge(str(r.get("scope", ""))),
                    reflex.badge(str(r.get("migration_status", ""))),
                    reflex.text(str(r.get("migration_status_fr", "")), size="2"),
                    spacing="2",
                    flex_wrap="wrap",
                ),
                reflex.heading(str(r.get("source_name", "")), size="3"),
                reflex.text(str(r.get("target_layer", "")), size="2"),
                reflex.text(str(r.get("rationale", "")), size="2"),
                reflex.text(str(r.get("next_action", "")), size="2"),
                spacing="2",
            ),
            width="100%",
        )

    return reflex.container(
        reflex.vstack(
            reflex.heading("Migration globale", size="6"),
            reflex.text(
                "Vue consolidée Sheets, Apps Script, fonctions, fonctionnalités, Python/Reflex et BigQuery futur. Statuts machine anglais + libellés français.",
                size="2",
            ),
            reflex.hstack(
                reflex.badge(f"rows={summary.get('total_rows')}"),
                reflex.badge(f"scripts={summary.get('script_inventory_count')}"),
                reflex.badge(f"functions={summary.get('function_index_count')}"),
                spacing="3",
                flex_wrap="wrap",
            ),
            reflex.heading("Cockpits Sheets / vues essentielles", size="4"),
            *[card(r) for r in cockpit],
            reflex.heading("Scripts Apps Script prioritaires", size="4"),
            *[card(r) for r in scripts],
            reflex.heading("Évolutions architecture / BigQuery", size="4"),
            *[card(r) for r in future],
            spacing="4",
            width="100%",
        ),
        size="4",
        padding_y="1.5rem",
    )
