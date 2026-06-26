from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import reflex as rx


STATUS_LABELS_FR: dict[str, str] = {
    "MIGRATE_NOW": "A migrer maintenant",
    "MIGRATE_LATER": "A migrer plus tard",
    "KEEP_SHEETS_MANUAL": "Garder dans Sheets en controle manuel",
    "KEEP_AS_EXPORT_SOURCE": "Garder comme source export / inventaire",
    "PYTHON_REWRITE": "Reecriture Python",
    "REFLEX_UI_BINDING": "Brancher a l'interface Reflex",
    "BIGQUERY_FUTURE_CANDIDATE": "Candidat BigQuery futur",
    "RETIRE_NO_VALUE": "Ne pas migrer / faible valeur",
    "NO_MIGRATION_NEEDED": "Pas de migration necessaire",
    "REVIEW_REQUIRED": "Revue humaine necessaire",
}

ESSENTIAL_STATUS_ORDER = [
    "MIGRATE_NOW",
    "PYTHON_REWRITE",
    "BIGQUERY_FUTURE_CANDIDATE",
    "REVIEW_REQUIRED",
    "REFLEX_UI_BINDING",
    "MIGRATE_LATER",
    "KEEP_SHEETS_MANUAL",
    "KEEP_AS_EXPORT_SOURCE",
]

SCOPE_LIMITS = {
    "SHEETS_COCKPIT": 19,
    "APPS_SCRIPT_FILE": 22,
    "APPS_SCRIPT_FUNCTION": 30,
    "FEATURE_CLUSTER": 10,
    "FUTURE_ARCHITECTURE": 5,
}

KEY_FAMILIES = {
    "QAIC_BRIDGE",
    "PROMPT_ENGINE",
    "KNOWLEDGE_SEARCH",
    "JOURNAL",
    "AUDIT_INVENTORY",
    "SCRIPT_REGISTRY",
    "FUTURE_PLATFORM",
}

SHOW_ONLY_ESSENTIAL = True


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _docs_root() -> Path:
    return _repo_root() / "docs"


def _load_json_file(path: Path, default: Any) -> Any:
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return default
    return default


def _summary() -> dict[str, Any]:
    data = _load_json_file(_docs_root() / "MIGRATION_GLOBAL_MATRIX_SUMMARY.json", {})
    return data if isinstance(data, dict) else {}


def _matrix_rows() -> list[dict[str, Any]]:
    data = _load_json_file(_docs_root() / "MIGRATION_GLOBAL_MATRIX.json", [])
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        for key in ("rows", "items", "matrix", "records"):
            rows = data.get(key)
            if isinstance(rows, list):
                return [row for row in rows if isinstance(row, dict)]
    return []


def _text_value(row: dict[str, Any], *keys: str, fallback: str = "") -> str:
    for key in keys:
        value = row.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return fallback


def _status(row: dict[str, Any]) -> str:
    return _text_value(row, "status", "migration_status", fallback="REVIEW_REQUIRED")


def _scope(row: dict[str, Any]) -> str:
    return _text_value(row, "scope", "item_scope", "migration_scope")


def _module_family(row: dict[str, Any]) -> str:
    return _text_value(row, "module_family", "family")


def _priority_rank(row: dict[str, Any]) -> tuple[int, int, str]:
    status = _status(row)
    family = _module_family(row)
    status_rank = ESSENTIAL_STATUS_ORDER.index(status) if status in ESSENTIAL_STATUS_ORDER else 99
    family_rank = 0 if family in KEY_FAMILIES else 1
    source = _text_value(
        row, "source", "source_name", "source_key", "script_name", "function_name", "name"
    )
    return (status_rank, family_rank, source)


def _is_essential(row: dict[str, Any]) -> bool:
    scope = _scope(row)
    status = _status(row)
    if scope in {"SHEETS_COCKPIT", "FEATURE_CLUSTER", "FUTURE_ARCHITECTURE"}:
        return True
    if scope == "APPS_SCRIPT_FILE":
        return status in {
            "MIGRATE_NOW",
            "PYTHON_REWRITE",
            "KEEP_AS_EXPORT_SOURCE",
            "BIGQUERY_FUTURE_CANDIDATE",
            "REVIEW_REQUIRED",
            "MIGRATE_LATER",
        }
    if scope == "APPS_SCRIPT_FUNCTION":
        return (
            status
            in {
                "MIGRATE_NOW",
                "PYTHON_REWRITE",
                "BIGQUERY_FUTURE_CANDIDATE",
                "REVIEW_REQUIRED",
                "REFLEX_UI_BINDING",
            }
            and _module_family(row) in KEY_FAMILIES
        )
    return False


def _essential_rows_for_scope(rows: list[dict[str, Any]], scope: str) -> list[dict[str, Any]]:
    limit = SCOPE_LIMITS.get(scope, 10)
    selected = [row for row in rows if _scope(row) == scope and _is_essential(row)]
    return sorted(selected, key=_priority_rank)[:limit]


def _metric_card(label: str, value: Any, detail: str = "") -> rx.Component:
    return rx.box(
        rx.text(str(value), size="6", weight="bold"),
        rx.text(label, size="2", weight="medium"),
        rx.cond(detail != "", rx.text(detail, size="1", color="gray"), rx.fragment()),
        padding="0.75rem",
        border="1px solid var(--gray-5)",
        border_radius="0.75rem",
        min_width="11rem",
    )


def _count_row(code: str, count: Any, label: str) -> rx.Component:
    return rx.hstack(
        rx.badge(code, variant="soft"),
        rx.text(str(count), weight="bold"),
        rx.text(label, color="gray"),
        justify="between",
        width="100%",
        padding_y="0.25rem",
    )


def _matrix_item(row: dict[str, Any]) -> rx.Component:
    source = _text_value(
        row,
        "source",
        "source_name",
        "source_key",
        "script_name",
        "function_name",
        "name",
        fallback="source inconnue",
    )
    target = _text_value(
        row, "target", "target_layer", "target_route", "target_view", fallback="cible a confirmer"
    )
    status = _status(row)
    family = _module_family(row)
    label = STATUS_LABELS_FR.get(status, "Statut a confirmer")
    return rx.box(
        rx.hstack(
            rx.text(source, weight="medium"),
            rx.badge(status, variant="soft"),
            align="center",
            justify="between",
            width="100%",
        ),
        rx.text(label, size="1", color="gray"),
        rx.text(target, size="1", color="gray"),
        rx.cond(family != "", rx.text(family, size="1", color="gray"), rx.fragment()),
        padding="0.55rem",
        border="1px solid var(--gray-4)",
        border_radius="0.6rem",
        width="100%",
    )


def _scope_preview(
    title: str, rows: list[dict[str, Any]], empty: str, note: str = ""
) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text(title, size="3", weight="bold"),
            rx.cond(note != "", rx.text(note, size="1", color="gray"), rx.fragment()),
            justify="between",
            align="center",
            width="100%",
        ),
        rx.cond(
            len(rows) > 0,
            rx.vstack(*[_matrix_item(row) for row in rows], spacing="2", width="100%"),
            rx.text(empty, color="gray"),
        ),
        padding="0.75rem",
        border="1px solid var(--gray-5)",
        border_radius="0.75rem",
        width="100%",
    )


def migration_tracker_panel() -> rx.Component:
    summary = _summary()
    rows = _matrix_rows()
    by_scope = summary.get("by_scope", {}) if isinstance(summary.get("by_scope", {}), dict) else {}
    by_status = (
        summary.get("by_status", {}) if isinstance(summary.get("by_status", {}), dict) else {}
    )
    total_rows = summary.get("total_rows", len(rows))
    source_csv_rows = summary.get("source_csv_rows", "?")
    script_inventory_count = summary.get(
        "script_inventory_count", by_scope.get("APPS_SCRIPT_FILE", "?")
    )
    function_index_count = summary.get(
        "function_index_count", by_scope.get("APPS_SCRIPT_FUNCTION", "?")
    )

    cockpit_rows = _essential_rows_for_scope(rows, "SHEETS_COCKPIT")
    script_rows = _essential_rows_for_scope(rows, "APPS_SCRIPT_FILE")
    function_rows = _essential_rows_for_scope(rows, "APPS_SCRIPT_FUNCTION")
    feature_rows = _essential_rows_for_scope(rows, "FEATURE_CLUSTER")
    future_rows = _essential_rows_for_scope(rows, "FUTURE_ARCHITECTURE")
    essential_visible_count = (
        len(cockpit_rows)
        + len(script_rows)
        + len(function_rows)
        + len(feature_rows)
        + len(future_rows)
    )
    status_rows = [
        _count_row(status, by_status.get(status, 0), STATUS_LABELS_FR.get(status, status))
        for status in ESSENTIAL_STATUS_ORDER
        if by_status.get(status, 0)
    ]

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "Migration Tracker — vision essentielle vivante", size="5", weight="bold"
                    ),
                    rx.text(
                        "Vue Mission Control: uniquement les cockpits, scripts, fonctions et fonctionnalites utiles au pilotage.",
                        color="gray",
                    ),
                    rx.text(
                        "Les fonctions brutes non essentielles restent agregees dans l'inventaire et accessibles en drill-down.",
                        size="1",
                        color="gray",
                    ),
                    align_items="start",
                    spacing="1",
                ),
                rx.link("Detail complet", href="/migration/global"),
                justify="between",
                align="start",
                width="100%",
            ),
            rx.hstack(
                _metric_card(
                    "Inventaire analyse", total_rows, "lignes techniques, non affichees en vrac"
                ),
                _metric_card("Essentiels affiches", essential_visible_count, "vue Mission Control"),
                _metric_card(
                    "Cockpits Sheets", by_scope.get("SHEETS_COCKPIT", 0), "source globale"
                ),
                _metric_card("Scripts Apps Script", script_inventory_count, "inventaire"),
                _metric_card(
                    "Fonctions Apps Script",
                    function_index_count,
                    "agregees, top essentiel seulement",
                ),
                _metric_card("Lignes CSV source", source_csv_rows, "CLASP imports"),
                wrap="wrap",
                spacing="3",
                width="100%",
            ),
            rx.box(
                rx.text("Statuts migration principaux", size="3", weight="bold"),
                *status_rows,
                width="100%",
                padding="0.75rem",
                border="1px solid var(--gray-5)",
                border_radius="0.75rem",
            ),
            _scope_preview(
                "Cockpits Sheets essentiels", cockpit_rows, "Aucun cockpit trouve dans la matrice."
            ),
            _scope_preview(
                "Scripts Apps Script essentiels",
                script_rows,
                "Aucun script essentiel trouve dans la matrice.",
            ),
            _scope_preview(
                "Fonctions Apps Script essentielles",
                function_rows,
                "Aucune fonction essentielle trouvee dans la matrice.",
                "top limite, pas les 2738 brutes",
            ),
            _scope_preview(
                "Fonctionnalites metier",
                feature_rows,
                "Aucune fonctionnalite trouvee dans la matrice.",
            ),
            _scope_preview(
                "Architecture future / BigQuery",
                future_rows,
                "Aucune cible future trouvee dans la matrice.",
            ),
            rx.text(
                "Refresh: lancer la commande R8C/R8+, puis rafraichir Mission Control. Pas de liste brute 2794 dans le cockpit principal.",
                size="1",
                color="gray",
            ),
            align_items="stretch",
            spacing="4",
            width="100%",
        ),
        width="100%",
    )


def migration_tracker() -> rx.Component:
    return migration_tracker_panel()


def migration_tracker_view() -> rx.Component:
    return migration_tracker_panel()


def migration_tracker_section() -> rx.Component:
    return migration_tracker_panel()


def render_migration_tracker() -> rx.Component:
    return migration_tracker_panel()


def migration_average_progress(*args: object, **kwargs: object) -> rx.Component:
    return migration_tracker_panel()


def build_migration_tracker_payload(*args: object, **kwargs: object) -> rx.Component:
    return migration_tracker_panel()


def migration_tracker_summary_rows(*args: object, **kwargs: object) -> rx.Component:
    return migration_tracker_panel()


def migration_tracker_compact_panel(*args: object, **kwargs: object) -> rx.Component:
    return migration_tracker_panel()
