"""Local auto-update tracker readers for MVP QAIC Reflex.

This module only reads local files already present in the repo/runtime copy.
It never calls external services, never writes Sheets/BigQuery, and never performs
broker/order/sizing actions.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SAFETY_FLAGS: dict[str, bool] = {
    "NO_PUBLIC_DEPLOY": True,
    "NO_LIVE_ACTION": True,
    "NO_BROKER_ORDER_SIZING": True,
    "NO_SHEET_WRITE": True,
    "NO_BIGQUERY_WRITE": True,
    "HUMAN_REVIEW_ONLY": True,
}

TRACKER_AUTO_UPDATE_STATUS = "LOCAL_FILES_SYNC_REQUIRED"
CDC_TRACKER_PATH = Path("docs/WEB_ARCHITECTURE_SITEMAP.json")
MIGRATION_TRACKER_PATH = Path("docs/MIGRATION_TRACKER.json")
TRACKER_SNAPSHOT_JSON = Path("docs/TRACKER_AUTO_UPDATE_SNAPSHOT.json")
TRACKER_SNAPSHOT_MD = Path("docs/TRACKER_AUTO_UPDATE_SNAPSHOT.md")
CLASP_IMPORTS_CANDIDATES: tuple[Path, ...] = (
    Path("docs/MVPQAIC_CLASP_IMPORTS_ALL.csv"),
    Path("02_SHEETS/EXPORTS_CSV/MVPQAIC_CLASP_IMPORTS_ALL.csv"),
    Path("EXPORTS_CSV/MVPQAIC_CLASP_IMPORTS_ALL.csv"),
)
DEV_TRACKING_ROOT = Path("05_EXPORTS")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _safe_read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "path": path.as_posix()}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - reader must report, not crash UI
        return {"exists": True, "path": path.as_posix(), "parse_ok": False, "error": str(exc)}

    summary: dict[str, Any] = {
        "exists": True,
        "path": path.as_posix(),
        "parse_ok": True,
        "type": type(data).__name__,
    }
    if isinstance(data, dict):
        summary["keys"] = sorted(str(k) for k in data.keys())[:40]
        for key in ("status", "version", "updated_at", "generated_at", "route", "title"):
            if key in data:
                summary[key] = data[key]
        for key in ("pages", "routes", "items", "entries", "modules", "tabs"):
            value = data.get(key)
            if isinstance(value, list):
                summary[f"{key}_count"] = len(value)
            elif isinstance(value, dict):
                summary[f"{key}_count"] = len(value)
    elif isinstance(data, list):
        summary["items_count"] = len(data)
        if data and isinstance(data[0], dict):
            summary["first_item_keys"] = sorted(str(k) for k in data[0].keys())[:30]
    return summary


def _latest_export_files(root: Path, limit: int = 20) -> dict[str, Any]:
    if not root.exists():
        return {"exists": False, "path": root.as_posix(), "latest_files": []}
    files = [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    latest = []
    for path in files[:limit]:
        stat = path.stat()
        latest.append(
            {
                "path": _rel(path, root.parent),
                "size_bytes": stat.st_size,
                "modified_at_local_epoch": int(stat.st_mtime),
            }
        )
    return {
        "exists": True,
        "path": root.as_posix(),
        "file_count": len(files),
        "latest_files": latest,
    }


def _find_clasp_imports_csv(repo_root: Path) -> Path | None:
    for rel in CLASP_IMPORTS_CANDIDATES:
        candidate = repo_root / rel
        if candidate.exists():
            return candidate
    for candidate in repo_root.glob("**/MVPQAIC_CLASP_IMPORTS_ALL.csv"):
        if ".git" not in candidate.parts:
            return candidate
    return None


def _csv_bool(value: str | None) -> bool:
    return str(value or "").strip().upper() in {"YES", "TRUE", "1", "Y"}


def _read_clasp_imports_summary(repo_root: Path, max_rows: int = 250_000) -> dict[str, Any]:
    path = _find_clasp_imports_csv(repo_root)
    if path is None:
        return {"exists": False, "path": "MVPQAIC_CLASP_IMPORTS_ALL.csv"}

    record_types: Counter[str] = Counter()
    module_families: Counter[str] = Counter()
    severity: Counter[str] = Counter()
    script_files: set[str] = set()
    function_names: set[str] = set()
    risk_counts: Counter[str] = Counter()
    rows = 0

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        for row in reader:
            rows += 1
            record_types[str(row.get("record_type") or "") or "<blank>"] += 1
            module_families[str(row.get("module_family") or "") or "<blank>"] += 1
            severity[str(row.get("severity") or "") or "<blank>"] += 1
            if row.get("script_file_name"):
                script_files.add(str(row["script_file_name"]))
            if row.get("function_name"):
                function_names.add(str(row["function_name"]))
            for key in (
                "has_network_logic",
                "has_bigquery_logic",
                "has_drive_logic",
                "has_properties_logic",
                "has_trigger_logic",
                "has_delete_or_clear_risk",
                "calls_spreadsheet",
                "calls_urlfetch",
                "calls_bigquery",
                "calls_trigger",
                "calls_properties",
                "calls_drive",
                "writes_sheet_likely",
            ):
                if _csv_bool(row.get(key)):
                    risk_counts[key] += 1
            if rows >= max_rows:
                break

    return {
        "exists": True,
        "path": _rel(path, repo_root),
        "rows_scanned": rows,
        "columns_count": len(columns),
        "columns": columns[:80],
        "record_type_counts": dict(record_types.most_common(20)),
        "module_family_counts": dict(module_families.most_common(20)),
        "severity_counts": dict(severity.most_common(20)),
        "script_file_count": len(script_files),
        "function_name_count": len(function_names),
        "risk_counts": dict(risk_counts.most_common()),
    }


def build_tracker_auto_update_snapshot(repo_root: str | Path | None = None) -> dict[str, Any]:
    root = Path(repo_root or Path.cwd()).resolve()
    snapshot = {
        "step": "P_REFLEX_12E_R2_AUTO_TRACKERS_SVG_VIEWER_REPO_LOCATOR_HARD_FIX",
        "status": TRACKER_AUTO_UPDATE_STATUS,
        "generated_at": _utc_now_iso(),
        "repo_root": str(root),
        "mode": "LOCAL_FILES_ONLY",
        "sync_state": "SYNC_REQUIRED_WHEN_RUNTIME_IS_OUTSIDE_REPO",
        "safety_flags": SAFETY_FLAGS,
        "trackers": {
            "dev_tracking": _latest_export_files(root / DEV_TRACKING_ROOT),
            "cdc_tracker": _safe_read_json(root / CDC_TRACKER_PATH),
            "migration_tracker": _safe_read_json(root / MIGRATION_TRACKER_PATH),
            "clasp_imports": _read_clasp_imports_summary(root),
        },
        "legend": {
            "dev_tracking": (
                "Suit lots Pxxx, commits, tags, tests, gates, smokes runtime, "
                "incidents et exports locaux."
            ),
            "cdc_tracker": (
                "Suit le cahier des charges produit/architecture depuis "
                "docs/WEB_ARCHITECTURE_SITEMAP.json."
            ),
            "migration_tracker": (
                "Suit la migration Sheets/Apps Script/exports vers Reflex/Python "
                "depuis docs/MIGRATION_TRACKER.json et l'inventaire CLASP CSV."
            ),
        },
    }
    return snapshot


def format_tracker_auto_update_markdown(snapshot: dict[str, Any]) -> str:
    trackers = snapshot.get("trackers", {})
    lines = [
        "# Auto-update Trackers — Snapshot local",
        "",
        f"- Status: `{snapshot.get('status')}`",
        f"- Mode: `{snapshot.get('mode')}`",
        f"- Sync state: `{snapshot.get('sync_state')}`",
        f"- Generated at: `{snapshot.get('generated_at')}`",
        "",
        "## Rôles",
        "",
        f"- Dev Tracking: {snapshot.get('legend', {}).get('dev_tracking')}",
        f"- CDC Tracker: {snapshot.get('legend', {}).get('cdc_tracker')}",
        f"- Migration Tracker: {snapshot.get('legend', {}).get('migration_tracker')}",
        "",
        "## Sources locales",
        "",
    ]
    for name, payload in trackers.items():
        exists = payload.get("exists")
        path = payload.get("path")
        lines.append(f"- `{name}`: exists=`{exists}` path=`{path}`")
        if "file_count" in payload:
            lines.append(f"  - file_count: `{payload['file_count']}`")
        if "rows_scanned" in payload:
            lines.append(f"  - rows_scanned: `{payload['rows_scanned']}`")
        if "script_file_count" in payload:
            lines.append(f"  - script_file_count: `{payload['script_file_count']}`")
        if "function_name_count" in payload:
            lines.append(f"  - function_name_count: `{payload['function_name_count']}`")
    lines.extend(["", "## Sécurité", ""])
    for key, value in snapshot.get("safety_flags", {}).items():
        lines.append(f"- `{key}` = `{value}`")
    lines.append("")
    return "\n".join(lines)


def write_tracker_auto_update_snapshot(repo_root: str | Path | None = None) -> dict[str, Any]:
    root = Path(repo_root or Path.cwd()).resolve()
    snapshot = build_tracker_auto_update_snapshot(root)
    json_path = root / TRACKER_SNAPSHOT_JSON
    md_path = root / TRACKER_SNAPSHOT_MD
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(format_tracker_auto_update_markdown(snapshot), encoding="utf-8")
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.write:
        snapshot = write_tracker_auto_update_snapshot(args.repo_root)
    else:
        snapshot = build_tracker_auto_update_snapshot(args.repo_root)
    print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
