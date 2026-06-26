"""Mission Control panel for local tracker auto-update status."""

from __future__ import annotations
import json

from pathlib import Path
from typing import Any

from mvp_qaic_reflex_ui.tracker_auto_update import build_tracker_auto_update_snapshot

try:
    import reflex as rx
except Exception:  # noqa: BLE001
    rx = None  # type: ignore[assignment]


def _require_reflex() -> Any:
    if rx is None:
        raise RuntimeError("reflex is required to render this panel")
    return rx


def tracker_auto_update_panel(repo_root: str | Path | None = None) -> Any:
    reflex = _require_reflex()
    snapshot = build_tracker_auto_update_snapshot(repo_root or Path.cwd())
    trackers = snapshot.get("trackers", {})

    def row(label: str, key: str) -> Any:
        payload = trackers.get(key, {})
        exists = payload.get("exists")
        path = payload.get("path", "")
        return reflex.hstack(
            reflex.badge(label),
            reflex.text(f"exists={exists}", size="2"),
            reflex.text(str(path), size="2"),
            spacing="3",
            flex_wrap="wrap",
        )

    return reflex.card(
        reflex.vstack(
            reflex.heading("Auto-update Trackers", size="4"),
            reflex.text(
                "Fondation locale : Dev Tracking, CDC Tracker et Migration Tracker "
                "sont lus depuis docs/, 05_EXPORTS/ et CSV CLASP. "
                "Le runtime LocalAppData doit être synchronisé.",
                size="2",
            ),
            reflex.hstack(
                reflex.badge(snapshot.get("status", "LOCAL_FILES")),
                reflex.badge(snapshot.get("sync_state", "SYNC_REQUIRED")),
                spacing="3",
                flex_wrap="wrap",
            ),
            row("Dev Tracking", "dev_tracking"),
            row("CDC Tracker", "cdc_tracker"),
            row("Migration Tracker", "migration_tracker"),
            row("CLASP CSV", "clasp_imports"),
            reflex.link(reflex.button("Ouvrir le panneau détaillé"), href="/trackers/auto-update"),
            spacing="3",
        ),
        width="100%",
    )


# --- P12F_R7_ENRICH_EXISTING_MC_LIST_FIXED_START ---
def _load_p12f_global_migration_summary(repo_root: str | Path | None = None) -> dict[str, Any]:
    root = Path(repo_root or Path.cwd())
    summary_path = root / "docs" / "MIGRATION_GLOBAL_MATRIX_SUMMARY.json"
    if not summary_path.exists():
        return {
            "total_rows": 0,
            "by_scope": {},
            "by_status": {},
            "by_target_layer": {},
            "by_module_family": {},
            "source_csv_rows": 0,
            "script_inventory_count": 0,
            "function_index_count": 0,
            "missing": str(summary_path),
        }
    try:
        return json.loads(summary_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return {
            "total_rows": 0,
            "by_scope": {},
            "by_status": {},
            "by_target_layer": {},
            "by_module_family": {},
            "source_csv_rows": 0,
            "script_inventory_count": 0,
            "function_index_count": 0,
            "error": str(exc),
        }


def _p12f_metric_line(reflex: Any, label: str, value: Any) -> Any:
    return reflex.hstack(
        reflex.text(label, font_weight="600", min_width="14rem"),
        reflex.text(str(value)),
        spacing="3",
        align="center",
        width="100%",
    )


def migration_global_matrix_existing_list_rows(repo_root: str | Path | None = None) -> list[Any]:
    reflex = _require_reflex()
    summary = _load_p12f_global_migration_summary(repo_root)
    by_scope = summary.get("by_scope", {}) or {}
    by_status = summary.get("by_status", {}) or {}
    top_statuses = sorted(by_status.items(), key=lambda item: item[1], reverse=True)[:8]

    status_rows = [_p12f_metric_line(reflex, status, count) for status, count in top_statuses]
    if not status_rows:
        status_rows = [reflex.text("Aucun statut migration charge.", color="gray")]

    return [
        reflex.divider(),
        reflex.heading("Migration globale - synthese integree", size="4"),
        reflex.text(
            "Vue globale ajoutee a la liste Mission Control existante. "
            "Les statuts machine restent en anglais; la decision humaine reste obligatoire.",
            size="2",
            color="gray",
        ),
        _p12f_metric_line(reflex, "global_matrix_rows", summary.get("total_rows", 0)),
        _p12f_metric_line(reflex, "sheets_cockpits", by_scope.get("SHEETS_COCKPIT", 0)),
        _p12f_metric_line(reflex, "apps_script_files", by_scope.get("APPS_SCRIPT_FILE", 0)),
        _p12f_metric_line(reflex, "apps_script_functions", by_scope.get("APPS_SCRIPT_FUNCTION", 0)),
        _p12f_metric_line(reflex, "feature_clusters", by_scope.get("FEATURE_CLUSTER", 0)),
        _p12f_metric_line(reflex, "future_architecture", by_scope.get("FUTURE_ARCHITECTURE", 0)),
        reflex.heading("Statuts migration principaux", size="3"),
        reflex.vstack(*status_rows, spacing="2", width="100%"),
        reflex.link(
            "Ouvrir le detail de la matrice migration",
            href="/migration/global",
            underline="always",
        ),
    ]


_p12f_original_tracker_auto_update_panel = tracker_auto_update_panel


def tracker_auto_update_panel(repo_root: str | Path | None = None) -> Any:
    reflex = _require_reflex()
    return reflex.vstack(
        _p12f_original_tracker_auto_update_panel(repo_root),
        reflex.card(
            reflex.vstack(
                *migration_global_matrix_existing_list_rows(repo_root),
                spacing="3",
                align="start",
                width="100%",
            ),
            width="100%",
        ),
        spacing="4",
        width="100%",
    )


# --- P12F_R7_ENRICH_EXISTING_MC_LIST_FIXED_END ---
