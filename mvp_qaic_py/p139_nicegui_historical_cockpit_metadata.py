from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P139_NICEGUI_HISTORICAL_COCKPIT_METADATA_CAPTURE_1.0.0_SAFE"
STATUS_CAPTURED = "P139_METADATA_CAPTURED"
SPREADSHEET_ID = "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0"

COCKPIT_SOURCE_TABS = [
    "📘 PROMPT_LIBRARY",
    "🎛️ PROMPT_VARIANT_CONTROL_CENTER",
    "🚀 PROMPT_RUN_QUEUE",
    "🧩 PROMPT_READY_TO_COPY",
    "🧠 PROMPT_CONTEXT_PACKS",
    "🔗 PROMPT_LEXIQUE_BRIDGE",
    "GPT_PROMPT_RUNTIME_SPEC",
    "OUTPUT_TEMPLATES",
    "DATA_REQUIREMENTS",
    "QAIC_OUTPUT_CONTRACT",
    "🤖 AI_RUNTIME_REFERENCE",
]

SAFETY_MARKERS = {
    "live_google_sheets_read": True,
    "google_sheets_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "public_deploy": False,
    "secrets_exported": False,
}


@dataclass(frozen=True)
class CaptureRequest:
    spreadsheet_id: str
    output_dir: Path
    run_id: str
    generated_at_utc: str
    max_header_rows: int
    repo_root: Path | None
    live_read: bool


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def quote_sheet_name(title: str) -> str:
    return "'" + title.replace("'", "''") + "'"


def get_access_token() -> str:
    for env_name in ("MVP_QAIC_GOOGLE_ACCESS_TOKEN", "GOOGLE_OAUTH_ACCESS_TOKEN"):
        value = os.environ.get(env_name)
        if value:
            return value.strip()

    # Prefer ADC because P138C-R9 created a custom OAuth ADC token with Sheets/Drive scopes.
    commands = [
        ["gcloud", "auth", "application-default", "print-access-token"],
        ["gcloud", "auth", "print-access-token"],
    ]
    diagnostics: list[str] = []
    for command in commands:
        try:
            completed = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            token = completed.stdout.strip()
            if token:
                return token
            diagnostics.append(" ".join(command) + "=EMPTY")
        except Exception as exc:
            diagnostics.append(" ".join(command) + f"=FAILED:{type(exc).__name__}")

    raise RuntimeError(
        "No Google access token found for P139 read-only capture. Diagnostics: "
        + " ; ".join(diagnostics)
        + " ; Run P138C-R9 auth or set MVP_QAIC_GOOGLE_ACCESS_TOKEN."
    )


def http_json(url: str, token: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Google Sheets API HTTP {exc.code}: {detail}") from exc


def build_metadata_url(spreadsheet_id: str) -> str:
    fields = (
        "spreadsheetId,"
        "properties(title,locale,timeZone,autoRecalc),"
        "sheets("
        "properties(sheetId,title,index,sheetType,hidden,rightToLeft,"
        "tabColor,tabColorStyle,gridProperties(rowCount,columnCount,frozenRowCount,frozenColumnCount,hideGridlines)),"
        "conditionalFormats,basicFilter,filterViews,protectedRanges,charts,developerMetadata"
        ")"
    )
    params = urllib.parse.urlencode({"includeGridData": "false", "fields": fields})
    return f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}?{params}"


def build_values_url(spreadsheet_id: str, sheet_titles: list[str], max_header_rows: int) -> str:
    ranges = [f"{quote_sheet_name(title)}!1:{max_header_rows}" for title in sheet_titles]
    params = urllib.parse.urlencode(
        {
            "majorDimension": "ROWS",
            "valueRenderOption": "FORMATTED_VALUE",
            "ranges": ranges,
        },
        doseq=True,
    )
    return (
        f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values:batchGet?{params}"
    )


def fetch_live_spreadsheet(
    spreadsheet_id: str, max_header_rows: int
) -> tuple[dict[str, Any], dict[str, list[list[str]]]]:
    token = get_access_token()
    metadata = http_json(build_metadata_url(spreadsheet_id), token=token)

    titles = [
        sheet.get("properties", {}).get("title", "")
        for sheet in metadata.get("sheets", [])
        if sheet.get("properties", {}).get("title")
    ]
    values_response = http_json(
        build_values_url(spreadsheet_id, titles, max_header_rows), token=token
    )

    values_by_title: dict[str, list[list[str]]] = {}
    for title, value_range in zip(titles, values_response.get("valueRanges", []), strict=False):
        raw_rows = value_range.get("values", [])
        values_by_title[title] = [[str(cell) for cell in row] for row in raw_rows]

    return metadata, values_by_title


def _count(value: Any) -> int:
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        return len(value)
    return 0


def _first_non_empty_row(rows: list[list[str]]) -> list[str]:
    for row in rows:
        if any(str(cell).strip() for cell in row):
            return row
    return []


def normalize_sheet(
    sheet: dict[str, Any],
    header_rows: list[list[str]],
    cockpit_targets: set[str],
) -> dict[str, Any]:
    props = sheet.get("properties", {})
    grid = props.get("gridProperties", {})
    title = props.get("title", "")

    first_row = _first_non_empty_row(header_rows)
    columns = [str(value).strip() for value in first_row if str(value).strip()]
    route_slug = (
        title.lower()
        .replace(" ", "_")
        .replace("🎛️", "control")
        .replace("📘", "library")
        .replace("🚀", "run")
        .replace("🧩", "ready")
        .replace("🧠", "context")
        .replace("🔗", "bridge")
        .replace("🤖", "runtime")
    )

    return {
        "sheet_id": props.get("sheetId"),
        "title": title,
        "index": props.get("index"),
        "sheet_type": props.get("sheetType"),
        "hidden": bool(props.get("hidden", False)),
        "right_to_left": bool(props.get("rightToLeft", False)),
        "row_count": int(grid.get("rowCount", 0) or 0),
        "column_count": int(grid.get("columnCount", 0) or 0),
        "frozen_row_count": int(grid.get("frozenRowCount", 0) or 0),
        "frozen_column_count": int(grid.get("frozenColumnCount", 0) or 0),
        "hide_gridlines": bool(grid.get("hideGridlines", False)),
        "has_tab_color": bool(props.get("tabColor") or props.get("tabColorStyle")),
        "conditional_format_rule_count": _count(sheet.get("conditionalFormats", [])),
        "filter_view_count": _count(sheet.get("filterViews", [])),
        "has_basic_filter": bool(sheet.get("basicFilter")),
        "protected_range_count": _count(sheet.get("protectedRanges", [])),
        "chart_count": _count(sheet.get("charts", [])),
        "developer_metadata_count": _count(sheet.get("developerMetadata", [])),
        "header_rows_preview": header_rows,
        "detected_columns": columns,
        "detected_column_count": len(columns),
        "is_cockpit_source_tab": title in cockpit_targets,
        "nicegui_route": f"/cockpit/{route_slug}",
        "suggested_component": "DataGridCard" if columns else "SheetSummaryCard",
        "replica_priority": "P0" if title in cockpit_targets else "P2",
    }


def build_payload(
    metadata: dict[str, Any],
    values_by_title: dict[str, list[list[str]]],
    *,
    run_id: str,
    generated_at_utc: str,
    spreadsheet_id: str,
    max_header_rows: int,
    live_read: bool,
) -> dict[str, Any]:
    cockpit_targets = set(COCKPIT_SOURCE_TABS)
    sheets = [
        normalize_sheet(
            sheet,
            values_by_title.get(sheet.get("properties", {}).get("title", ""), []),
            cockpit_targets,
        )
        for sheet in metadata.get("sheets", [])
    ]
    sheets.sort(key=lambda row: (row.get("index") is None, row.get("index", 999999)))

    cockpit_found = [row["title"] for row in sheets if row["is_cockpit_source_tab"]]
    cockpit_missing = [title for title in COCKPIT_SOURCE_TABS if title not in cockpit_found]

    nicegui_spec = {
        "spec_id": "P139_NICEGUI_HISTORICAL_COCKPIT_UI_REPLICA_SPEC",
        "layout_fidelity_level": "STRUCTURE_HEADER_GRID_METADATA_V1",
        "recommended_next_step": "P140_NICEGUI_COCKPIT_REPLICA_RENDERER_FROM_METADATA",
        "routes": [
            {
                "route": row["nicegui_route"],
                "title": row["title"],
                "priority": row["replica_priority"],
                "component": row["suggested_component"],
                "frozen_columns": row["frozen_column_count"],
                "detected_columns": row["detected_columns"],
            }
            for row in sheets
            if row["is_cockpit_source_tab"]
        ],
        "navigation_groups": [
            {
                "group": "Prompt cockpit historique",
                "routes": [row["nicegui_route"] for row in sheets if row["is_cockpit_source_tab"]],
            }
        ],
        "rendering_rules": {
            "preserve_sheet_order": True,
            "preserve_frozen_columns": True,
            "preserve_header_names": True,
            "show_hidden_tabs_as_archived": True,
            "no_sheet_write": True,
            "no_auto_apply": True,
        },
    }

    return {
        "status": STATUS_CAPTURED,
        "version": VERSION,
        "run_id": run_id,
        "generated_at_utc": generated_at_utc,
        "spreadsheet_id": spreadsheet_id,
        "spreadsheet_title": metadata.get("properties", {}).get("title"),
        "spreadsheet_locale": metadata.get("properties", {}).get("locale"),
        "spreadsheet_time_zone": metadata.get("properties", {}).get("timeZone"),
        "live_google_sheets_read": live_read,
        "google_sheets_write": False,
        "max_header_rows": max_header_rows,
        "sheet_count": len(sheets),
        "cockpit_source_tab_count": len(cockpit_found),
        "cockpit_source_tabs_found": cockpit_found,
        "cockpit_source_tabs_missing": cockpit_missing,
        "sheets": sheets,
        "nicegui_replica_spec": nicegui_spec,
        "safety": dict(SAFETY_MARKERS),
        "next": "P140_NICEGUI_COCKPIT_REPLICA_RENDERER_FROM_METADATA",
    }


def write_outputs(payload: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)

    payload_path = output_dir / "P139_UI_METADATA_PAYLOAD.json"
    spec_json_path = output_dir / "P139_NICEGUI_UI_REPLICA_SPEC.json"
    csv_path = output_dir / "P139_SHEET_UI_METADATA.csv"
    md_path = output_dir / "P139_NICEGUI_UI_REPLICA_SPEC.md"
    runbook_path = output_dir / "P139_CAPTURE_RUNBOOK.md"

    payload_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    spec_json_path.write_text(
        json.dumps(payload["nicegui_replica_spec"], ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    rows = payload.get("sheets", [])
    csv_fields = [
        "index",
        "sheet_id",
        "title",
        "is_cockpit_source_tab",
        "replica_priority",
        "nicegui_route",
        "suggested_component",
        "row_count",
        "column_count",
        "frozen_row_count",
        "frozen_column_count",
        "hide_gridlines",
        "has_tab_color",
        "conditional_format_rule_count",
        "filter_view_count",
        "has_basic_filter",
        "protected_range_count",
        "chart_count",
        "detected_column_count",
        "detected_columns",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_fields)
        writer.writeheader()
        for row in rows:
            out = {field: row.get(field, "") for field in csv_fields}
            out["detected_columns"] = " | ".join(row.get("detected_columns", []))
            writer.writerow(out)

    route_lines = "\n".join(
        f"- `{route['route']}` — {route['title']} — {route['component']}"
        for route in payload["nicegui_replica_spec"]["routes"]
    )
    md_path.write_text(
        "\n".join(
            [
                "# P139 — NiceGUI Historical Cockpit UI Replica Spec",
                "",
                f"- Status: `{payload['status']}`",
                f"- Spreadsheet: `{payload.get('spreadsheet_title')}`",
                f"- Sheet count: `{payload['sheet_count']}`",
                f"- Cockpit source tabs found: `{payload['cockpit_source_tab_count']}`",
                f"- Live read: `{payload['live_google_sheets_read']}`",
                f"- Sheet write: `{payload['google_sheets_write']}`",
                "",
                "## NiceGUI routes",
                "",
                route_lines or "- No cockpit route detected.",
                "",
                "## Next",
                "",
                f"`{payload['next']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    runbook_path.write_text(
        "\n".join(
            [
                "# P139 Capture Runbook",
                "",
                "Read-only capture of Google Sheets cockpit metadata for a future NiceGUI replica.",
                "",
                "Safety:",
                "- No Google Sheets write",
                "- No Apps Script execution",
                "- No CLASP push",
                "- No broker/order/sizing",
                "- No public deploy",
                "",
                f"Run ID: `{payload['run_id']}`",
                f"Generated: `{payload['generated_at_utc']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {
        "payload_json": str(payload_path),
        "spec_json": str(spec_json_path),
        "sheet_metadata_csv": str(csv_path),
        "spec_markdown": str(md_path),
        "runbook": str(runbook_path),
    }


def load_json_file(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_capture(
    request: CaptureRequest, *, metadata_json: Path | None = None, values_json: Path | None = None
) -> dict[str, Any]:
    if request.live_read:
        metadata, values_by_title = fetch_live_spreadsheet(
            request.spreadsheet_id, request.max_header_rows
        )
    else:
        if not metadata_json:
            raise ValueError("metadata_json is required when live_read=false")
        metadata = load_json_file(metadata_json)
        if values_json and values_json.exists():
            values_by_title = load_json_file(values_json)
        else:
            values_by_title = {}

    payload = build_payload(
        metadata,
        values_by_title,
        run_id=request.run_id,
        generated_at_utc=request.generated_at_utc,
        spreadsheet_id=request.spreadsheet_id,
        max_header_rows=request.max_header_rows,
        live_read=request.live_read,
    )
    output_files = write_outputs(payload, request.output_dir)
    payload["output_files"] = output_files

    summary_path = request.output_dir / "P139_SUMMARY.json"
    summary = {
        "status": payload["status"],
        "sheet_count": payload["sheet_count"],
        "cockpit_source_tab_count": payload["cockpit_source_tab_count"],
        "live_google_sheets_read": payload["live_google_sheets_read"],
        "google_sheets_write": payload["google_sheets_write"],
        "output_dir": str(request.output_dir),
        "next": payload["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="P139 NiceGUI historical cockpit metadata capture."
    )
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--spreadsheet-id", default=SPREADSHEET_ID)
    parser.add_argument("--run-id", default="P139-NICEGUI-HISTORICAL-COCKPIT-METADATA-CAPTURE")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    parser.add_argument("--max-header-rows", type=int, default=5)
    parser.add_argument("--live-read", action="store_true")
    parser.add_argument("--metadata-json", default=None)
    parser.add_argument("--values-json", default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    request = CaptureRequest(
        spreadsheet_id=args.spreadsheet_id,
        output_dir=Path(args.output_dir),
        run_id=args.run_id,
        generated_at_utc=args.generated_at_utc,
        max_header_rows=args.max_header_rows,
        repo_root=Path(args.repo_root) if args.repo_root else None,
        live_read=bool(args.live_read),
    )
    payload = run_capture(
        request,
        metadata_json=Path(args.metadata_json) if args.metadata_json else None,
        values_json=Path(args.values_json) if args.values_json else None,
    )
    print(payload["status"])
    print(f"sheet_count={payload['sheet_count']}")
    print(f"cockpit_source_tab_count={payload['cockpit_source_tab_count']}")
    print(f"live_google_sheets_read={str(payload['live_google_sheets_read']).lower()}")
    print(f"google_sheets_write={str(payload['google_sheets_write']).lower()}")
    print(f"output_dir={request.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
