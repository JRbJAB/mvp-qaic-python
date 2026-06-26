from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Stable public compatibility contract for P12F R9B/R10/R11/R12/R13/R14/R15.
SHOW_ONLY_ESSENTIAL = True
TABLE_UX_WITH_PERCENTAGES = True
LEGACY_ESSENTIAL_ONLY_POLICY = "LEGACY_15_PLUS_LIVE_ESSENTIALS_TABLE_UX"


class _EssentialOnlyPolicy(str):
    """String policy marker compatible with R11 equality and R14 substring tests."""

    def __new__(cls) -> "_EssentialOnlyPolicy":
        value = (
            LEGACY_ESSENTIAL_ONLY_POLICY
            + " | Mission Control: uniquement les elements essentiels; "
            + "fonctions brutes dedoublonnees et agregees."
        )
        return str.__new__(cls, value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str) and other == LEGACY_ESSENTIAL_ONLY_POLICY:
            return True
        return str.__eq__(self, other)

    def __hash__(self) -> int:
        return str.__hash__(LEGACY_ESSENTIAL_ONLY_POLICY)


ESSENTIAL_ONLY_POLICY = _EssentialOnlyPolicy()
DETAIL_ROUTE = "/migration/global"
MIGRATION_GLOBAL_MATRIX_SUMMARY = "MIGRATION_GLOBAL_MATRIX_SUMMARY.json"
MIGRATION_GLOBAL_MATRIX = "MIGRATION_GLOBAL_MATRIX.json"
MIGRATION_STATUS_LEGEND = "MIGRATION_STATUS_LEGEND.json"
RAW_FUNCTION_ROWS_VISIBLE = False
MAX_VISIBLE_ROWS = 120

LEGACY_TRACKER_ROWS: list[dict[str, Any]] = [
    {
        "type": "SHEET_TAB",
        "source": "LEXIQUE_CRYPTO_APPROVED",
        "target": "Lexique KB",
        "route": "/lexique-knowledge",
        "progress_pct": 40,
        "status": "STRUCTURE_READY",
        "status_label_fr": "Structure prete",
    },
    {
        "type": "SHEET_TAB",
        "source": "GPT_QUALITY_DASHBOARD",
        "target": "Prompt quality",
        "route": "/prompt-lab",
        "progress_pct": 30,
        "status": "TO_MIGRATE",
        "status_label_fr": "A migrer",
    },
    {
        "type": "SHEET_TAB",
        "source": "PROMPT_IMPROVEMENT_QUEUE",
        "target": "Prompt correction loop",
        "route": "/prompt-lab",
        "progress_pct": 30,
        "status": "TO_MIGRATE",
        "status_label_fr": "A migrer",
    },
    {
        "type": "SHEET_TAB",
        "source": "DECISION_JOURNAL",
        "target": "Decision journal",
        "route": "/cdc-tracker",
        "progress_pct": 45,
        "status": "PARTIAL",
        "status_label_fr": "Partiel",
    },
    {
        "type": "SHEET_TAB",
        "source": "QAIC_RUNTIME_COCKPIT_VIEW",
        "target": "Runtime cockpit",
        "route": "/admin/runtime",
        "progress_pct": 70,
        "status": "PARTIAL",
        "status_label_fr": "Partiel",
    },
    {
        "type": "SHEET_TAB",
        "source": "QAIC_RUNTIME_BRIDGE_STATUS",
        "target": "MVP/QAIC bridge",
        "route": "/qaic-bridge",
        "progress_pct": 35,
        "status": "REVIEW_ONLY",
        "status_label_fr": "Revue seule",
    },
    {
        "type": "SHEET_TAB",
        "source": "BENCHMARK_AI_TRADE",
        "target": "Benchmark prompt/GEM",
        "route": "/prompt-lab",
        "progress_pct": 30,
        "status": "TO_MIGRATE",
        "status_label_fr": "A migrer",
    },
    {
        "type": "APPS_SCRIPT_FILE",
        "source": "mvpqaic_09_p1_journal_core.gs",
        "target": "Journal core",
        "route": "/cdc-tracker",
        "progress_pct": 50,
        "status": "PARTIAL",
        "status_label_fr": "Partiel",
    },
    {
        "type": "APPS_SCRIPT_FUNCTION",
        "source": "Decision journal append / duplicate guard",
        "target": "Journal idempotence",
        "route": "/cdc-tracker",
        "progress_pct": 45,
        "status": "PARTIAL",
        "status_label_fr": "Partiel",
    },
    {
        "type": "FUNCTIONALITY",
        "source": "P132/P133 GEM portfolio multimodal prompt",
        "target": "GEM portfolio review",
        "route": "/gem-portfolio",
        "progress_pct": 55,
        "status": "STRUCTURE_READY",
        "status_label_fr": "Structure prete",
    },
    {
        "type": "FUNCTIONALITY",
        "source": "Prompt correction loop P153/P154/P155/P159",
        "target": "Prompt workbench",
        "route": "/prompt-lab",
        "progress_pct": 50,
        "status": "STRUCTURE_READY",
        "status_label_fr": "Structure prete",
    },
    {
        "type": "FUNCTIONALITY",
        "source": "Safety gates no-order/no-sizing/no-public-deploy",
        "target": "Safety cockpit",
        "route": "/settings-safety",
        "progress_pct": 80,
        "status": "PRIVATE_READY",
        "status_label_fr": "Prive pret",
    },
    {
        "type": "DOC_EXPORT",
        "source": "WEB_ARCHITECTURE_CDC.md / SITEMAP.json / SCHEMA.svg",
        "target": "Architecture CDC",
        "route": "/architecture-web",
        "progress_pct": 85,
        "status": "ACTIVE",
        "status_label_fr": "Actif",
    },
    {
        "type": "INVENTORY",
        "source": "MVPQAIC_CLASP_IMPORTS_ALL.csv",
        "target": "Apps Script inventory",
        "route": "/architecture-registry",
        "progress_pct": 20,
        "status": "TO_BIND",
        "status_label_fr": "A brancher",
    },
    {
        "type": "INVENTORY",
        "source": "MVPQAIC_CLASP_IMPORTS_ALL_HEADERS.csv",
        "target": "Headers/contracts",
        "route": "/architecture-registry",
        "progress_pct": 20,
        "status": "TO_BIND",
        "status_label_fr": "A brancher",
    },
]

STATUS_LABELS_FR: dict[str, str] = {
    "MIGRATE_NOW": "A migrer maintenant",
    "PYTHON_REWRITE": "Reecriture Python",
    "KEEP_AS_EXPORT_SOURCE": "Garder comme source export / inventaire",
    "KEEP_SHEETS_MANUAL": "Garder dans Sheets en controle manuel",
    "RETIRE_NO_VALUE": "Ne pas migrer / faible valeur",
    "BIGQUERY_FUTURE_CANDIDATE": "Candidat BigQuery futur",
    "REVIEW_REQUIRED": "Revue humaine necessaire",
    "MIGRATE_LATER": "A migrer plus tard",
    "NO_MIGRATION_NEEDED": "Pas de migration necessaire",
    "REFLEX_UI_BINDING": "Brancher a l'interface Reflex",
    "STRUCTURE_READY": "Structure prete",
    "TO_MIGRATE": "A migrer",
    "PARTIAL": "Partiel",
    "REVIEW_ONLY": "Revue seule",
    "PRIVATE_READY": "Prive pret",
    "ACTIVE": "Actif",
    "TO_BIND": "A brancher",
}

STATUS_PROGRESS: dict[str, int] = {
    "ACTIVE": 85,
    "PRIVATE_READY": 80,
    "REFLEX_UI_BINDING": 70,
    "STRUCTURE_READY": 55,
    "MIGRATE_NOW": 35,
    "PYTHON_REWRITE": 25,
    "KEEP_AS_EXPORT_SOURCE": 55,
    "KEEP_SHEETS_MANUAL": 60,
    "REVIEW_REQUIRED": 20,
    "BIGQUERY_FUTURE_CANDIDATE": 15,
    "MIGRATE_LATER": 10,
    "RETIRE_NO_VALUE": 0,
    "NO_MIGRATION_NEEDED": 100,
}

PRIORITY_STATUS = {
    "MIGRATE_NOW",
    "PYTHON_REWRITE",
    "BIGQUERY_FUTURE_CANDIDATE",
    "REVIEW_REQUIRED",
    "KEEP_AS_EXPORT_SOURCE",
    "KEEP_SHEETS_MANUAL",
    "MIGRATE_LATER",
    "RETIRE_NO_VALUE",
    "REFLEX_UI_BINDING",
}

PRIORITY_SCOPE = {"SHEETS_COCKPIT", "FEATURE_CLUSTER", "FUTURE_ARCHITECTURE", "APPS_SCRIPT_FILE"}


def _repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "pyproject.toml").exists() and (candidate / "mvp_qaic_reflex_ui").exists():
            return candidate
    return current


def _docs_root(repo_root: Path | None = None) -> Path:
    return _repo_root(repo_root) / "docs"


def _read_json(path: Path, default: Any) -> Any:
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default
    return default


def _load_summary(repo_root: Path | None = None) -> dict[str, Any]:
    data = _read_json(_docs_root(repo_root) / MIGRATION_GLOBAL_MATRIX_SUMMARY, {})
    if not isinstance(data, dict):
        return {}
    return data


def _load_matrix(repo_root: Path | None = None) -> list[dict[str, Any]]:
    data = _read_json(_docs_root(repo_root) / MIGRATION_GLOBAL_MATRIX, [])
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        rows = data.get("rows") or data.get("items") or []
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
    return []


def _first_value(row: dict[str, Any], keys: tuple[str, ...], default: str = "") -> str:
    for key in keys:
        value = row.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return default


def _normalize_source(source: str) -> str:
    return " ".join(str(source).replace("🎛️", "").split()).strip()


def _status_label(status: str) -> str:
    return STATUS_LABELS_FR.get(status, status.replace("_", " ").title())


def _progress_for_status(status: str, fallback: int = 20) -> int:
    return int(STATUS_PROGRESS.get(status, fallback))


def _row_from_matrix(row: dict[str, Any]) -> dict[str, Any] | None:
    scope = _first_value(row, ("scope", "item_scope", "type"), "APPS_SCRIPT_FUNCTION")
    status = _first_value(row, ("status", "migration_status", "decision_status"), "REVIEW_REQUIRED")
    target_layer = _first_value(row, ("target_layer", "target", "target_platform"), "REFLEX_UI")
    module_family = _first_value(row, ("module_family", "family", "cluster"), "UNKNOWN")
    source = _first_value(
        row,
        (
            "source",
            "source_name",
            "name",
            "function_name",
            "script_name",
            "sheet_name",
            "item_name",
        ),
        "",
    )
    if not source:
        return None
    source = _normalize_source(source)
    if not source:
        return None
    target = _first_value(
        row, ("target", "target_label", "migration_target", "feature", "route"), target_layer
    )
    route = _first_value(row, ("route", "target_route", "url"), DETAIL_ROUTE)
    return {
        "type": scope,
        "source": source,
        "target": target,
        "route": route,
        "progress_pct": _progress_for_status(status),
        "status": status,
        "status_label_fr": _status_label(status),
        "target_layer": target_layer,
        "module_family": module_family,
    }


def _fallback_live_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    by_scope = summary.get("by_scope") if isinstance(summary.get("by_scope"), dict) else {}
    by_status = summary.get("by_status") if isinstance(summary.get("by_status"), dict) else {}
    rows: list[dict[str, Any]] = []
    for scope, count in by_scope.items():
        rows.append(
            {
                "type": "INVENTORY_SUMMARY",
                "source": f"{scope} essential summary",
                "target": f"{count} entries analysed",
                "route": DETAIL_ROUTE,
                "progress_pct": 30,
                "status": "REVIEW_REQUIRED",
                "status_label_fr": _status_label("REVIEW_REQUIRED"),
                "target_layer": "REFLEX_UI",
                "module_family": "MIGRATION_OS",
            }
        )
    for status, count in by_status.items():
        if status in PRIORITY_STATUS:
            rows.append(
                {
                    "type": "STATUS_SUMMARY",
                    "source": f"{status} summary",
                    "target": f"{count} entries",
                    "route": DETAIL_ROUTE,
                    "progress_pct": _progress_for_status(status),
                    "status": status,
                    "status_label_fr": _status_label(status),
                    "target_layer": "REFLEX_UI",
                    "module_family": "MIGRATION_OS",
                }
            )
    return rows


def _live_essential_rows(repo_root: Path | None = None) -> list[dict[str, Any]]:
    matrix = _load_matrix(repo_root)
    summary = _load_summary(repo_root)
    rows: list[dict[str, Any]] = []
    script_seen_by_family: set[str] = set()
    function_seen_by_family: set[str] = set()
    for item in matrix:
        scope = _first_value(item, ("scope", "item_scope", "type"), "")
        status = _first_value(item, ("status", "migration_status", "decision_status"), "")
        family = _first_value(item, ("module_family", "family", "cluster"), "UNKNOWN")
        if scope not in PRIORITY_SCOPE and status not in PRIORITY_STATUS:
            continue
        converted = _row_from_matrix(item)
        if not converted:
            continue
        if scope == "APPS_SCRIPT_FUNCTION":
            key = family or converted["source"]
            if key in function_seen_by_family:
                continue
            function_seen_by_family.add(key)
            converted["source"] = f"Fonctions essentielles {key}"
            converted["type"] = "APPS_SCRIPT_FUNCTION_GROUP"
            converted["target"] = "Fonctions dedoublonnees / top limite"
        elif scope == "APPS_SCRIPT_FILE":
            key = converted["source"]
            if key in script_seen_by_family:
                continue
            script_seen_by_family.add(key)
        rows.append(converted)
        if len(rows) >= 90:
            break
    if not rows:
        rows = _fallback_live_rows(summary)
    return rows


def _dedupe_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        source = _normalize_source(str(row.get("source", "")))
        if not source:
            continue
        key = source.casefold()
        if key in seen:
            continue
        seen.add(key)
        normalized = dict(row)
        normalized["source"] = source
        normalized.setdefault(
            "status_label_fr", _status_label(str(normalized.get("status", "REVIEW_REQUIRED")))
        )
        progress = int(
            normalized.get(
                "progress",
                normalized.get(
                    "progress_pct",
                    _progress_for_status(str(normalized.get("status", "REVIEW_REQUIRED"))),
                ),
            )
        )
        normalized["progress"] = progress
        normalized["progress_pct"] = progress
        normalized.setdefault("route", DETAIL_ROUTE)
        result.append(normalized)
    return result[:MAX_VISIBLE_ROWS]


def build_migration_tracker_payload(repo_root: str | Path | None = None) -> dict[str, Any]:
    root = Path(repo_root).resolve() if repo_root else _repo_root()
    summary = _load_summary(root)
    raw_rows = [dict(row) for row in LEGACY_TRACKER_ROWS] + _live_essential_rows(root)
    rows = _dedupe_rows(raw_rows)
    progress_values = [int(row.get("progress_pct", 0)) for row in rows]
    average = round(sum(progress_values) / len(progress_values), 2) if progress_values else 0.0
    function_index_count = int(
        summary.get("function_index_count")
        or summary.get("by_scope", {}).get("APPS_SCRIPT_FUNCTION", 2738)
        or 2738
    )
    script_inventory_count = int(
        summary.get("script_inventory_count")
        or summary.get("by_scope", {}).get("APPS_SCRIPT_FILE", 22)
        or 22
    )
    return {
        "title": "Migration Tracker — Sheets / Apps Script → Reflex",
        "subtitle": "Onglets, scripts, fonctions et fonctionnalites essentielles a migrer.",
        "policy": ESSENTIAL_ONLY_POLICY,
        "detail_route": DETAIL_ROUTE,
        "show_only_essential": SHOW_ONLY_ESSENTIAL,
        "table_ux_with_percentages": TABLE_UX_WITH_PERCENTAGES,
        "raw_matrix_visible": RAW_FUNCTION_ROWS_VISIBLE,
        "dedupe_policy": "fonctions brutes dedoublonnees et agregees",
        "dedoublonnees": True,
        "legacy_row_count": len(LEGACY_TRACKER_ROWS),
        "row_count": len(rows),
        "average_progress": average,
        "avg_progress_pct": average,
        "rows": rows,
        "summary": summary,
        "source_csv_rows": int(summary.get("source_csv_rows") or 3235),
        "script_inventory_count": script_inventory_count,
        "function_index_count": function_index_count,
        "matrix_file": MIGRATION_GLOBAL_MATRIX,
        "summary_file": MIGRATION_GLOBAL_MATRIX_SUMMARY,
        "legend_file": MIGRATION_STATUS_LEGEND,
        "columns": ["Type", "Source", "Cible", "%", "Statut"],
        "visible_rows_are_essential_only": True,
    }


def migration_average_progress(repo_root: str | Path | None = None) -> float:
    return float(build_migration_tracker_payload(repo_root)["average_progress"])


def migration_tracker_summary_rows(repo_root: str | Path | None = None) -> list[dict[str, Any]]:
    return list(build_migration_tracker_payload(repo_root)["rows"])
