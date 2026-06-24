"""P168C read-only Sheets export/import or API binding decision layer.

This module stays inside MVP_QAIC_PY. It does not call Google APIs, does not
write Google Sheets, and does not modify runtime prompts. It consumes the P168B
snapshot/read-plan export and creates a deterministic operator handoff for one
of two safe read-only paths:

1. immediate local export/import snapshots (CSV/XLSX provided by the operator),
2. later Google Sheets API read-only binding once local OAuth/service auth is set.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

STEP = "P168C_SHEETS_READONLY_EXPORT_IMPORT_OR_API_BINDING"
STATUS = "P168C_SHEETS_READONLY_BINDING_READY_REVIEW_ONLY"
EXPORT_PREFIX_P168B = "P168B_SHEETS_DATA_SNAPSHOT_LAYER_READONLY_"
EXPORT_PREFIX_P168C = "P168C_SHEETS_READONLY_EXPORT_IMPORT_OR_API_BINDING_"

SAFETY_FLAGS: dict[str, bool] = {
    "review_only": True,
    "runtime_prompt_modified": False,
    "apply_allowed": False,
    "google_sheets_write": False,
    "live_google_api_call_from_python": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "public_deploy": False,
}

MANIFEST_COLUMNS = [
    "snapshot_id",
    "source_key",
    "spreadsheet_id",
    "spreadsheet_title",
    "tab_name",
    "bounded_range",
    "local_file",
    "file_type",
    "row_count",
    "column_count",
    "captured_at",
    "checksum_sha256",
    "operator_review_status",
]

API_CONTRACT_FIELDS = [
    "source_key",
    "spreadsheet_id",
    "tab_name",
    "bounded_range",
    "value_render_option",
    "read_only_scope",
    "max_cells_guard",
    "write_allowed",
]


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


def discover_latest_p168b_export(project_root: Path) -> Path | None:
    return discover_latest_export(project_root, EXPORT_PREFIX_P168B)


def read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"json_error": str(path)}
    return value if isinstance(value, dict) else {"json_not_object": str(path)}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys: list[str] = []
        for row in rows:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def p168b_summary_path(export_dir: Path) -> Path:
    return export_dir / "P168B_SUMMARY.json"


def p168b_bounded_read_plan_path(export_dir: Path) -> Path:
    return export_dir / "P168B_BOUNDED_READ_PLAN.csv"


def build_binding_strategy(read_plan_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_plan_rows:
        required = (row.get("required_before_python_port") or "").upper()
        priority = row.get("priority", "")
        if required == "NO" or priority == "REFERENCE_ONLY":
            action = "REFERENCE_ONLY_NO_MVP_IMPORT"
            preferred_path = "NO_IMPORT"
            ready_now = "NO"
        elif required == "YES":
            action = "SNAPSHOT_REQUIRED_BEFORE_PORT"
            preferred_path = "LOCAL_EXPORT_IMPORT_FIRST"
            ready_now = "YES_WITH_OPERATOR_EXPORT"
        else:
            action = "SNAPSHOT_REVIEW_BEFORE_PORT"
            preferred_path = "LOCAL_EXPORT_IMPORT_FIRST"
            ready_now = "REVIEW"
        rows.append(
            {
                "source_key": row.get("source_key") or "LIVE_SHEET_MVP_QAIC_DEV",
                "spreadsheet_id": row.get("spreadsheet_id", ""),
                "spreadsheet_title": row.get("spreadsheet_title", ""),
                "tab_name": row.get("tab_name", ""),
                "bounded_range": row.get("bounded_range", ""),
                "snapshot_filename": row.get("snapshot_filename", ""),
                "priority": priority,
                "required_before_python_port": required,
                "binding_action": action,
                "preferred_path_now": preferred_path,
                "api_binding_later": "GOOGLE_SHEETS_API_READONLY",
                "ready_now": ready_now,
                "write_allowed": "NO",
                "live_api_call_from_python_now": "NO",
            }
        )
    return rows


def build_manifest_template(read_plan_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    now = utc_now_iso()
    for row in read_plan_rows:
        if (row.get("required_before_python_port") or "").upper() == "NO":
            continue
        rows.append(
            {
                "snapshot_id": "PENDING_OPERATOR_EXPORT",
                "source_key": row.get("source_key") or "LIVE_SHEET_MVP_QAIC_DEV",
                "spreadsheet_id": row.get("spreadsheet_id", ""),
                "spreadsheet_title": row.get("spreadsheet_title", ""),
                "tab_name": row.get("tab_name", ""),
                "bounded_range": row.get("bounded_range", ""),
                "local_file": row.get("snapshot_filename", ""),
                "file_type": "CSV_OR_XLSX",
                "row_count": "PENDING",
                "column_count": "PENDING",
                "captured_at": now,
                "checksum_sha256": "PENDING",
                "operator_review_status": "PENDING_EXPORT",
            }
        )
    return rows


def build_api_contract_rows(read_plan_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_plan_rows:
        if (row.get("required_before_python_port") or "").upper() == "NO":
            continue
        bounded_range = row.get("bounded_range", "")
        rows.append(
            {
                "source_key": row.get("source_key") or "LIVE_SHEET_MVP_QAIC_DEV",
                "spreadsheet_id": row.get("spreadsheet_id", ""),
                "tab_name": row.get("tab_name", ""),
                "bounded_range": bounded_range,
                "value_render_option": "FORMATTED_VALUE",
                "read_only_scope": "spreadsheets.readonly",
                "max_cells_guard": "50000",
                "write_allowed": "NO",
            }
        )
    return rows


def _markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    lines = [header, sep]
    for row in rows:
        lines.append(
            "| " + " | ".join(str(row.get(field, "")).replace("|", "/") for field in fields) + " |"
        )
    return "\n".join(lines) + "\n"


def build_report(
    *,
    p168b_export_dir: Path | None,
    p168b_summary: dict[str, Any],
    binding_rows: list[dict[str, Any]],
    manifest_rows: list[dict[str, Any]],
    blocker_count: int,
) -> str:
    lines = [
        "# P168C — Sheets read-only export/import or API binding",
        "",
        "## Decision",
        "",
        "Use `LOCAL_EXPORT_IMPORT_FIRST` now for MVP_QAIC_PY, then add Google Sheets API read-only binding later after local OAuth/service auth is explicitly configured.",
        "",
        "## Source",
        "",
        f"- P168B export: `{p168b_export_dir}`",
        f"- P168B hierarchy locked: `{p168b_summary.get('hierarchy_locked')}`",
        f"- Blocker count: `{blocker_count}`",
        "",
        "## Safety",
        "",
        "- Google Sheets write: `False`",
        "- Live Google API call from Python now: `False`",
        "- Apps Script execution: `False`",
        "- CLASP push: `False`",
        "- Broker/order/sizing: `False`",
        "",
        "## Binding strategy",
        "",
        _markdown_table(
            binding_rows,
            [
                "tab_name",
                "bounded_range",
                "binding_action",
                "preferred_path_now",
                "api_binding_later",
            ],
        ),
        "",
        "## Operator manifest template",
        "",
        _markdown_table(
            manifest_rows[:10],
            ["tab_name", "bounded_range", "local_file", "operator_review_status"],
        ),
        "",
        "## Next",
        "",
        "P168D_LOCAL_SNAPSHOT_IMPORT_READER_FROM_OPERATOR_EXPORTS",
    ]
    return "\n".join(lines)


def build_outputs(project_root: Path) -> Path:
    p168b_export = discover_latest_p168b_export(project_root)
    p168b_summary = read_json_if_exists(p168b_summary_path(p168b_export)) if p168b_export else {}
    read_plan_rows = (
        read_csv_rows(p168b_bounded_read_plan_path(p168b_export)) if p168b_export else []
    )

    blockers: list[str] = []
    if p168b_export is None:
        blockers.append("MISSING_P168B_EXPORT")
    if not p168b_summary.get("hierarchy_locked"):
        blockers.append("P168B_HIERARCHY_NOT_LOCKED")
    if len(read_plan_rows) < 5:
        blockers.append("P168B_BOUNDED_READ_PLAN_TOO_SMALL")

    binding_rows = build_binding_strategy(read_plan_rows)
    manifest_rows = build_manifest_template(read_plan_rows)
    api_rows = build_api_contract_rows(read_plan_rows)
    required_snapshot_count = sum(
        1 for row in manifest_rows if row.get("operator_review_status") == "PENDING_EXPORT"
    )

    export_dir = project_root / "05_EXPORTS" / f"{EXPORT_PREFIX_P168C}{utc_stamp()}"
    export_dir.mkdir(parents=True, exist_ok=True)

    write_csv(export_dir / "P168C_READONLY_BINDING_STRATEGY.csv", binding_rows)
    write_csv(
        export_dir / "P168C_EXPORT_IMPORT_MANIFEST_TEMPLATE.csv", manifest_rows, MANIFEST_COLUMNS
    )
    write_csv(export_dir / "P168C_API_BINDING_CONTRACT.csv", api_rows, API_CONTRACT_FIELDS)

    api_contract_md = "\n".join(
        [
            "# P168C API binding contract — future read-only only",
            "",
            "This is a contract for a future local Python Google Sheets API reader.",
            "It must use read-only scope, bounded ranges, and no Sheets write calls.",
            "",
            _markdown_table(api_rows, API_CONTRACT_FIELDS),
        ]
    )
    (export_dir / "P168C_API_BINDING_CONTRACT.md").write_text(api_contract_md, encoding="utf-8")

    instructions = "\n".join(
        [
            "# P168C local export/import instructions",
            "",
            "1. Keep working in `C:\\Users\\Julie\\Documents\\JRb-Dev\\MVP_QAIC_PY_WORK_...`, not in Google Drive Git repo.",
            "2. Export the MVP Google Sheet tabs listed in `P168C_EXPORT_IMPORT_MANIFEST_TEMPLATE.csv` as CSV or XLSX.",
            "3. Put files under `04_SNAPSHOTS/MVP_QAIC/` in the repo work clone.",
            "4. Do not write back to Google Sheets.",
            "5. Run the next batch to validate/import local snapshots.",
            "",
            "Next: `P168D_LOCAL_SNAPSHOT_IMPORT_READER_FROM_OPERATOR_EXPORTS`.",
        ]
    )
    (export_dir / "P168C_LOCAL_EXPORT_IMPORT_INSTRUCTIONS.md").write_text(
        instructions, encoding="utf-8"
    )

    report = build_report(
        p168b_export_dir=p168b_export,
        p168b_summary=p168b_summary,
        binding_rows=binding_rows,
        manifest_rows=manifest_rows,
        blocker_count=len(blockers),
    )
    (export_dir / "P168C_BINDING_REPORT.md").write_text(report, encoding="utf-8")

    summary: dict[str, Any] = {
        "step": STEP,
        "status": STATUS,
        "created_at": utc_now_iso(),
        "p168b_export_dir": str(p168b_export) if p168b_export else "",
        "hierarchy_locked": bool(p168b_summary.get("hierarchy_locked")),
        "binding_strategy_count": len(binding_rows),
        "manifest_template_count": len(manifest_rows),
        "api_contract_count": len(api_rows),
        "required_snapshot_count": required_snapshot_count,
        "preferred_path_now": "LOCAL_EXPORT_IMPORT_FIRST",
        "api_binding_later": "GOOGLE_SHEETS_API_READONLY",
        "blockers": blockers,
        "blocker_count": len(blockers),
        "next": "P168D_LOCAL_SNAPSHOT_IMPORT_READER_FROM_OPERATOR_EXPORTS",
        **SAFETY_FLAGS,
    }
    (export_dir / "P168C_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(STATUS)
    print(f"hierarchy_locked={summary['hierarchy_locked']}")
    print(f"binding_strategy_count={summary['binding_strategy_count']}")
    print(f"manifest_template_count={summary['manifest_template_count']}")
    print(f"api_contract_count={summary['api_contract_count']}")
    print(f"required_snapshot_count={summary['required_snapshot_count']}")
    print(f"preferred_path_now={summary['preferred_path_now']}")
    print(f"live_google_api_call_from_python={summary['live_google_api_call_from_python']}")
    print(f"google_sheets_write={summary['google_sheets_write']}")
    print(f"blocker_count={summary['blocker_count']}")
    print(f"output_dir={export_dir}")
    print(f"next={summary['next']}")
    return export_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=STEP)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    build_outputs(args.project_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
