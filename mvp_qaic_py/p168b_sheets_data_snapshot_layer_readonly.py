"""P168B read-only Sheets data snapshot layer for MVP_QAIC_PY.

This module does not call Google APIs, does not write Google Sheets, and does not
modify runtime prompts. It turns the P165/P168A source registry into a local,
deterministic snapshot contract and can optionally inventory local XLSX/CSV
snapshots when an operator provides them.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

STEP = "P168B_SHEETS_DATA_SNAPSHOT_LAYER_READONLY"
STATUS = "P168B_SHEETS_DATA_SNAPSHOT_LAYER_READY_READONLY"

EXPORT_PREFIX_P165 = "P165_R3_INITIAL_SHEET_APPS_SCRIPT_FUNCTIONAL_LAYER_"
EXPORT_PREFIX_P168A = "P168A_HIERARCHY_AND_MIGRATION_ROADMAP_LOCK_"

MVP_SHEET_ID = "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0"
MVP_SHEET_TITLE = "🛠️ MVP QAIC — Crypto Signal OS — DEV"
QAIC_V25_SHEET_ID = "1vBwQ6GMfqBOfesIIpzBVGieTm-GcY9y_dXink_VY1Vg"
QAIC_V25_SHEET_TITLE = "📈 QAIC Crypto - V25 DEV"

SAFETY_FLAGS: dict[str, bool] = {
    "review_only": True,
    "runtime_prompt_modified": False,
    "apply_allowed": False,
    "google_sheets_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "public_deploy": False,
    "live_google_api_call_from_python": False,
}

# Keep the first snapshot layer bounded. Full tab exports can be added after the
# operator confirms which Google API/OAuth path is active on the local machine.
DEFAULT_BOUNDED_READ_PLAN: list[dict[str, Any]] = [
    {
        "priority": "P0",
        "spreadsheet_id": MVP_SHEET_ID,
        "spreadsheet_title": MVP_SHEET_TITLE,
        "tab_name": "CONFIG",
        "bounded_range": "A1:D200",
        "purpose": "Runtime project configuration, source folder IDs, setup/import timestamps, safety mode.",
        "snapshot_filename": "MVP_QAIC_DEV__CONFIG__A1_D200.csv",
        "required_before_python_port": "YES",
    },
    {
        "priority": "P0",
        "spreadsheet_id": MVP_SHEET_ID,
        "spreadsheet_title": MVP_SHEET_TITLE,
        "tab_name": "LEXIQUE_CRYPTO_APPROVED",
        "bounded_range": "A1:Z5000",
        "purpose": "Lexique/knowledge source for MVP prompt/webapp context.",
        "snapshot_filename": "MVP_QAIC_DEV__LEXIQUE_CRYPTO_APPROVED__A1_Z5000.csv",
        "required_before_python_port": "YES",
    },
    {
        "priority": "P0",
        "spreadsheet_id": MVP_SHEET_ID,
        "spreadsheet_title": MVP_SHEET_TITLE,
        "tab_name": "PROMPT_IMPROVEMENT_QUEUE",
        "bounded_range": "A1:Z5000",
        "purpose": "Prompt correction/review queue; no automatic apply.",
        "snapshot_filename": "MVP_QAIC_DEV__PROMPT_IMPROVEMENT_QUEUE__A1_Z5000.csv",
        "required_before_python_port": "YES",
    },
    {
        "priority": "P1",
        "spreadsheet_id": MVP_SHEET_ID,
        "spreadsheet_title": MVP_SHEET_TITLE,
        "tab_name": "DECISION_JOURNAL",
        "bounded_range": "A1:Z5000",
        "purpose": "Human review/decision history for MVP operator traceability.",
        "snapshot_filename": "MVP_QAIC_DEV__DECISION_JOURNAL__A1_Z5000.csv",
        "required_before_python_port": "YES",
    },
    {
        "priority": "P1",
        "spreadsheet_id": MVP_SHEET_ID,
        "spreadsheet_title": MVP_SHEET_TITLE,
        "tab_name": "GPT_QUALITY_DASHBOARD",
        "bounded_range": "A1:Z2000",
        "purpose": "Quality dashboard source for prompt cockpit prioritization.",
        "snapshot_filename": "MVP_QAIC_DEV__GPT_QUALITY_DASHBOARD__A1_Z2000.csv",
        "required_before_python_port": "REVIEW",
    },
    {
        "priority": "REFERENCE_ONLY",
        "spreadsheet_id": QAIC_V25_SHEET_ID,
        "spreadsheet_title": QAIC_V25_SHEET_TITLE,
        "tab_name": "REFERENCE_ONLY_NO_MVP_PORT",
        "bounded_range": "N/A",
        "purpose": "QAIC V25 remains backend/reference only; do not merge into MVP_QAIC_PY runtime.",
        "snapshot_filename": "NO_MVP_SNAPSHOT_REFERENCE_ONLY.csv",
        "required_before_python_port": "NO",
    },
]

LOCAL_SNAPSHOT_SCHEMA: list[dict[str, str]] = [
    {
        "field": "snapshot_id",
        "type": "string",
        "required": "YES",
        "description": "Deterministic ID: source_key + tab + range + timestamp.",
    },
    {
        "field": "source_key",
        "type": "string",
        "required": "YES",
        "description": "Logical source key, for example LIVE_SHEET_MVP_QAIC_DEV.",
    },
    {
        "field": "spreadsheet_id",
        "type": "string",
        "required": "YES",
        "description": "Raw Google Sheets ID.",
    },
    {
        "field": "spreadsheet_title",
        "type": "string",
        "required": "YES",
        "description": "Human-readable spreadsheet title.",
    },
    {"field": "tab_name", "type": "string", "required": "YES", "description": "Sheet tab name."},
    {
        "field": "bounded_range",
        "type": "string",
        "required": "YES",
        "description": "Finite A1 range used for read-only extraction.",
    },
    {
        "field": "local_file",
        "type": "string",
        "required": "YES",
        "description": "Local CSV/XLSX snapshot file path relative to repo.",
    },
    {
        "field": "row_count",
        "type": "integer",
        "required": "RECOMMENDED",
        "description": "Detected data rows when local snapshot is available.",
    },
    {
        "field": "column_count",
        "type": "integer",
        "required": "RECOMMENDED",
        "description": "Detected max columns when local snapshot is available.",
    },
    {
        "field": "captured_at",
        "type": "timestamp",
        "required": "YES",
        "description": "UTC timestamp when snapshot/manifest is generated.",
    },
    {
        "field": "read_mode",
        "type": "enum",
        "required": "YES",
        "description": "READ_ONLY_EXPORT, LOCAL_CSV, LOCAL_XLSX, or PLANNED_READ_ONLY.",
    },
]


@dataclass(frozen=True)
class LocalSnapshotInventory:
    local_file: str
    file_type: str
    row_count: int
    column_count: int
    sheet_names: str
    status: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%d_%H%M%S")


def discover_latest_export(project_root: Path, prefix: str) -> Path | None:
    exports_root = project_root / "05_EXPORTS"
    if not exports_root.exists():
        return None
    candidates = [p for p in exports_root.iterdir() if p.is_dir() and p.name.startswith(prefix)]
    return sorted(candidates, key=lambda p: p.name)[-1] if candidates else None


def read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"json_error": str(path)}
    return value if isinstance(value, dict) else {"json_not_object": str(path)}


def find_summary_json(export_dir: Path | None) -> dict[str, Any]:
    if export_dir is None:
        return {}
    candidates = sorted(export_dir.glob("*SUMMARY.json"), key=lambda p: p.name)
    return read_json_if_exists(candidates[-1]) if candidates else {}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _as_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _safe_snapshot_id(*parts: str) -> str:
    raw = "__".join(parts)
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", raw).strip("_")


def detect_csv_dimensions(path: Path) -> tuple[int, int]:
    row_count = 0
    max_columns = 0
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            for row in reader:
                row_count += 1
                max_columns = max(max_columns, len(row))
    except UnicodeDecodeError:
        with path.open("r", encoding="cp1252", newline="") as handle:
            reader = csv.reader(handle)
            for row in reader:
                row_count += 1
                max_columns = max(max_columns, len(row))
    return row_count, max_columns


def _xlsx_sheet_names(path: Path) -> list[str]:
    try:
        with zipfile.ZipFile(path) as zf:
            workbook_xml = ET.fromstring(zf.read("xl/workbook.xml"))
    except (KeyError, ET.ParseError, zipfile.BadZipFile):
        return []
    ns = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    return [
        sheet.attrib.get("name", "") for sheet in workbook_xml.findall("main:sheets/main:sheet", ns)
    ]


def _xlsx_first_sheet_dimensions(path: Path) -> tuple[int, int]:
    try:
        with zipfile.ZipFile(path) as zf:
            sheet_xml = ET.fromstring(zf.read("xl/worksheets/sheet1.xml"))
    except (KeyError, ET.ParseError, zipfile.BadZipFile):
        return 0, 0
    ns = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    rows = sheet_xml.findall(".//main:sheetData/main:row", ns)
    row_count = len(rows)
    max_columns = 0
    for row in rows:
        max_columns = max(max_columns, len(row.findall("main:c", ns)))
    return row_count, max_columns


def inventory_local_snapshots(
    project_root: Path, extra_snapshot_dir: Path | None = None
) -> list[LocalSnapshotInventory]:
    roots: list[Path] = []
    for relative in ["04_SNAPSHOTS", "05_EXPORTS", "data", "snapshots"]:
        candidate = project_root / relative
        if candidate.exists():
            roots.append(candidate)
    if extra_snapshot_dir and extra_snapshot_dir.exists():
        roots.append(extra_snapshot_dir)

    seen: set[Path] = set()
    inventories: list[LocalSnapshotInventory] = []
    for root in roots:
        for path in sorted(root.rglob("*"), key=lambda p: str(p)):
            if not path.is_file() or path in seen:
                continue
            seen.add(path)
            suffix = path.suffix.lower()
            if suffix == ".csv":
                rows, cols = detect_csv_dimensions(path)
                inventories.append(
                    LocalSnapshotInventory(
                        local_file=str(path.relative_to(project_root))
                        if path.is_relative_to(project_root)
                        else str(path),
                        file_type="CSV",
                        row_count=rows,
                        column_count=cols,
                        sheet_names="",
                        status="LOCAL_SNAPSHOT_DETECTED",
                    )
                )
            elif suffix == ".xlsx":
                sheet_names = _xlsx_sheet_names(path)
                rows, cols = _xlsx_first_sheet_dimensions(path)
                inventories.append(
                    LocalSnapshotInventory(
                        local_file=str(path.relative_to(project_root))
                        if path.is_relative_to(project_root)
                        else str(path),
                        file_type="XLSX",
                        row_count=rows,
                        column_count=cols,
                        sheet_names=" | ".join(sheet_names),
                        status="LOCAL_SNAPSHOT_DETECTED",
                    )
                )
    return inventories


def _load_p165_source_registry(p165_dir: Path | None) -> list[dict[str, str]]:
    if p165_dir is None:
        return []
    candidates = sorted(p165_dir.glob("*SOURCE_REGISTRY.csv"), key=lambda p: p.name)
    return read_csv_rows(candidates[-1]) if candidates else []


def _source_registry_rows(p165_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for row in p165_rows:
        raw = " ".join(str(value) for value in row.values())
        if MVP_SHEET_ID in raw or QAIC_V25_SHEET_ID in raw or "LIVE_SHEET" in raw:
            selected.append({key: value for key, value in row.items()})
    if selected:
        return selected
    return [
        {
            "source_key": "LIVE_SHEET_MVP_QAIC_DEV",
            "source_type": "GOOGLE_SHEET_READONLY",
            "title": MVP_SHEET_TITLE,
            "source_id": MVP_SHEET_ID,
            "boundary": "MVP_QAIC_PY_ALLOWED_READONLY",
        },
        {
            "source_key": "LIVE_SHEET_QAIC_CRYPTO_V25_DEV",
            "source_type": "GOOGLE_SHEET_REFERENCE_ONLY",
            "title": QAIC_V25_SHEET_TITLE,
            "source_id": QAIC_V25_SHEET_ID,
            "boundary": "QAIC_PY_REFERENCE_ONLY_NO_MVP_PORT",
        },
    ]


def build_snapshot_manifest(
    project_root: Path, extra_snapshot_dir: Path | None = None
) -> dict[str, Any]:
    p165_dir = discover_latest_export(project_root, EXPORT_PREFIX_P165)
    p168a_dir = discover_latest_export(project_root, EXPORT_PREFIX_P168A)
    p165_summary = find_summary_json(p165_dir)
    p168a_summary = find_summary_json(p168a_dir)
    p165_source_registry = _source_registry_rows(_load_p165_source_registry(p165_dir))
    local_snapshots = inventory_local_snapshots(project_root, extra_snapshot_dir)

    blockers: list[str] = []
    if p165_dir is None:
        blockers.append("MISSING_P165_SOURCE_ACCESS_EXPORT")
    if p168a_dir is None:
        blockers.append("MISSING_P168A_HIERARCHY_LOCK_EXPORT")
    if not p165_source_registry:
        blockers.append("MISSING_SHEET_SOURCE_REGISTRY")

    captured_at = utc_now_iso()
    planned_rows: list[dict[str, Any]] = []
    for plan in DEFAULT_BOUNDED_READ_PLAN:
        source_key = (
            "LIVE_SHEET_MVP_QAIC_DEV"
            if plan["spreadsheet_id"] == MVP_SHEET_ID
            else "LIVE_SHEET_QAIC_CRYPTO_V25_DEV"
        )
        planned_rows.append(
            {
                **plan,
                "source_key": source_key,
                "snapshot_id": _safe_snapshot_id(
                    source_key, str(plan["tab_name"]), str(plan["bounded_range"]), captured_at
                ),
                "captured_at": captured_at,
                "read_mode": "PLANNED_READ_ONLY",
                "local_file": "",
                "row_count": "",
                "column_count": "",
                "status": "WAITING_FOR_READONLY_EXPORT_OR_GOOGLE_API_READER",
            }
        )

    local_rows = [inventory.__dict__ for inventory in local_snapshots]

    return {
        "step": STEP,
        "status": STATUS,
        "generated_at": captured_at,
        "project": "MVP_QAIC_PY",
        "p165_export_dir": str(p165_dir) if p165_dir else "",
        "p168a_export_dir": str(p168a_dir) if p168a_dir else "",
        "p165_status": str(p165_summary.get("status") or p165_summary.get("P165_R3_STATUS") or ""),
        "p168a_status": str(p168a_summary.get("status") or p168a_summary.get("P168A_STATUS") or ""),
        "hierarchy_locked": bool(
            p168a_summary.get("hierarchy_locked")
            or p168a_summary.get("HIERARCHY_LOCKED")
            or p168a_dir
        ),
        "source_registry_rows": p165_source_registry,
        "source_registry_count": len(p165_source_registry),
        "bounded_read_plan": planned_rows,
        "bounded_read_plan_count": len(planned_rows),
        "local_snapshot_inventory": local_rows,
        "local_snapshot_count": len(local_rows),
        "schema": LOCAL_SNAPSHOT_SCHEMA,
        "safety_flags": SAFETY_FLAGS,
        "blockers": blockers,
        "blocker_count": len(blockers),
        "next": "P168C_SHEETS_READONLY_EXPORT_IMPORT_OR_API_BINDING"
        if not blockers
        else "STOP_FIX_SNAPSHOT_PREREQUISITES",
    }


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys: list[str] = []
        for row in rows:
            for key in row.keys():
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# P168B — Sheets Data Snapshot Layer Read-Only",
        "",
        f"- Status: `{payload['status']}`",
        f"- Project: `{payload['project']}`",
        f"- P165 export: `{payload['p165_export_dir']}`",
        f"- P168A export: `{payload['p168a_export_dir']}`",
        f"- Hierarchy locked: `{payload['hierarchy_locked']}`",
        f"- Sheet source registry rows: `{payload['source_registry_count']}`",
        f"- Bounded read plan rows: `{payload['bounded_read_plan_count']}`",
        f"- Local snapshot files detected: `{payload['local_snapshot_count']}`",
        f"- Blocker count: `{payload['blocker_count']}`",
        f"- Next: `{payload['next']}`",
        "",
        "## Boundary decision",
        "",
        "This batch keeps Sheets access inside `MVP_QAIC_PY` as read-only source/snapshot work.",
        "It does not move broker, order, sizing, Revolut X execution, or QAIC backend work into MVP.",
        "",
        "## Read-only snapshot contract",
        "",
        "Python can consume local CSV/XLSX snapshots and can later bind to Google Sheets API read-only credentials.",
        "This batch creates the deterministic manifest/schema and intentionally performs no Google Sheets write.",
        "",
        "## Priority tabs",
        "",
    ]
    for row in payload["bounded_read_plan"]:
        lines.append(
            f"- `{row['priority']}` `{row['spreadsheet_title']}` / `{row['tab_name']}` / `{row['bounded_range']}` → `{row['snapshot_filename']}`"
        )
    lines.extend(["", "## Safety flags", ""])
    for key, value in payload["safety_flags"].items():
        lines.append(f"- `{key}` = `{value}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_outputs(project_root: Path, extra_snapshot_dir: Path | None = None) -> Path:
    payload = build_snapshot_manifest(project_root, extra_snapshot_dir)
    export_dir = (
        project_root / "05_EXPORTS" / f"P168B_SHEETS_DATA_SNAPSHOT_LAYER_READONLY_{utc_stamp()}"
    )
    export_dir.mkdir(parents=True, exist_ok=True)

    write_csv(export_dir / "P168B_SHEETS_DATA_SOURCE_REGISTRY.csv", payload["source_registry_rows"])
    write_csv(export_dir / "P168B_BOUNDED_READ_PLAN.csv", payload["bounded_read_plan"])
    write_csv(
        export_dir / "P168B_LOCAL_SNAPSHOT_INVENTORY.csv", payload["local_snapshot_inventory"]
    )
    write_csv(export_dir / "P168B_LOCAL_SNAPSHOT_SCHEMA.csv", payload["schema"])
    write_report(export_dir / "P168B_SNAPSHOT_LAYER_REPORT.md", payload)
    (export_dir / "P168B_SUMMARY.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(STATUS)
    print(f"hierarchy_locked={payload['hierarchy_locked']}")
    print(f"source_registry_count={payload['source_registry_count']}")
    print(f"bounded_read_plan_count={payload['bounded_read_plan_count']}")
    print(f"local_snapshot_count={payload['local_snapshot_count']}")
    print("runtime_prompt_modified=False")
    print("apply_allowed=False")
    print("google_sheets_write=False")
    print(f"blocker_count={payload['blocker_count']}")
    print(f"output_dir={export_dir}")
    print(f"next={payload['next']}")
    return export_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=STEP)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--extra-snapshot-dir", default="")
    args = parser.parse_args(argv)
    project_root = Path(args.project_root).resolve()
    extra_snapshot_dir = (
        Path(args.extra_snapshot_dir).resolve() if args.extra_snapshot_dir else None
    )
    export_dir = build_outputs(project_root, extra_snapshot_dir)
    summary = read_json_if_exists(export_dir / "P168B_SUMMARY.json")
    return 0 if _as_int(summary.get("blocker_count")) == 0 else 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
