from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P140_NICEGUI_COCKPIT_REPLICA_RENDERER_FROM_METADATA_1.0.0_SAFE"
STATUS_RENDERED = "P140_NICEGUI_COCKPIT_REPLICA_RENDERED_FROM_METADATA"

SAFETY_MARKERS = {
    "source": "P139_METADATA_ONLY",
    "live_google_sheets_read": False,
    "google_sheets_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "public_deploy": False,
}


@dataclass(frozen=True)
class RenderRequest:
    p139_payload_path: Path
    output_dir: Path
    run_id: str
    generated_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    value = (
        value.replace("📘", "library")
        .replace("🎛️", "control")
        .replace("🚀", "run")
        .replace("🧩", "ready")
        .replace("🧠", "context")
        .replace("🔗", "bridge")
        .replace("🤖", "runtime")
    )
    value = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    return value or "sheet"


def load_payload(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def cockpit_sheets(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [row for row in payload.get("sheets", []) if row.get("is_cockpit_source_tab")]
    return sorted(rows, key=lambda row: (row.get("index") is None, row.get("index", 999999)))


def build_component_model(payload: dict[str, Any]) -> dict[str, Any]:
    pages: list[dict[str, Any]] = []
    for sheet in cockpit_sheets(payload):
        title = str(sheet.get("title", ""))
        columns = [str(col) for col in sheet.get("detected_columns", [])]
        route = str(sheet.get("nicegui_route") or f"/cockpit/{slugify(title)}")
        pages.append(
            {
                "page_id": slugify(title),
                "title": title,
                "route": route,
                "component": sheet.get("suggested_component", "DataGridCard"),
                "priority": sheet.get("replica_priority", "P1"),
                "row_count": sheet.get("row_count", 0),
                "column_count": sheet.get("column_count", 0),
                "frozen_row_count": sheet.get("frozen_row_count", 0),
                "frozen_column_count": sheet.get("frozen_column_count", 0),
                "hide_gridlines": bool(sheet.get("hide_gridlines", False)),
                "has_basic_filter": bool(sheet.get("has_basic_filter", False)),
                "filter_view_count": sheet.get("filter_view_count", 0),
                "conditional_format_rule_count": sheet.get("conditional_format_rule_count", 0),
                "protected_range_count": sheet.get("protected_range_count", 0),
                "chart_count": sheet.get("chart_count", 0),
                "detected_columns": columns,
                "header_rows_preview": sheet.get("header_rows_preview", []),
            }
        )

    return {
        "status": STATUS_RENDERED,
        "version": VERSION,
        "spreadsheet_title": payload.get("spreadsheet_title"),
        "source_p139_status": payload.get("status"),
        "source_sheet_count": payload.get("sheet_count"),
        "cockpit_page_count": len(pages),
        "pages": pages,
        "navigation": {
            "title": "MVP QAIC — Cockpit historique",
            "items": [
                {"label": page["title"], "route": page["route"], "page_id": page["page_id"]}
                for page in pages
            ],
        },
        "rendering_policy": {
            "renderer": "NiceGUI metadata-driven replica",
            "data_mode": "metadata_preview_first",
            "future_data_binding": "P141_OR_LATER",
            "no_live_write": True,
            "no_public_deploy": True,
        },
        "safety": dict(SAFETY_MARKERS),
        "next": "P141_NICEGUI_COCKPIT_REPLICA_LOCAL_LAUNCH",
    }


def render_static_preview_html(model: dict[str, Any]) -> str:
    parts = [
        "<!doctype html><html lang='fr'><head><meta charset='utf-8'>",
        "<title>MVP QAIC Cockpit</title>",
        "<style>",
        "body{font-family:Arial,sans-serif;margin:0;background:#f7f7f8;color:#202124}",
        "header{background:#111827;color:white;padding:24px 32px}",
        "nav{display:flex;gap:8px;flex-wrap:wrap;padding:16px 32px;background:white;border-bottom:1px solid #e5e7eb}",
        "nav a{text-decoration:none;color:#111827;border:1px solid #d1d5db;border-radius:999px;padding:6px 12px}",
        "main{padding:24px 32px;display:grid;gap:18px}",
        ".card{background:white;border:1px solid #e5e7eb;border-radius:16px;padding:18px}",
        ".chip,.metric{display:inline-block;background:#eef2ff;border:1px solid #c7d2fe;border-radius:999px;padding:4px 9px;margin:3px;font-size:12px}",
        "table{border-collapse:collapse;width:100%;margin-top:10px;font-size:12px}td{border:1px solid #e5e7eb;padding:6px}",
        "</style></head><body>",
        "<header><h1>MVP QAIC — Cockpit historique</h1><p>Preview statique depuis P139 metadata. No live write / no broker / no deploy.</p></header>",
        "<nav>",
    ]
    for item in model.get("navigation", {}).get("items", []):
        parts.append(
            "<a href='#" + html.escape(item["page_id"]) + "'>" + html.escape(item["label"]) + "</a>"
        )
    parts.append("</nav><main>")
    for page in model.get("pages", []):
        parts.append("<section class='card' id='" + html.escape(page["page_id"]) + "'>")
        parts.append("<h2>" + html.escape(page["title"]) + "</h2>")
        parts.append("<code>" + html.escape(page["route"]) + "</code><br>")
        metrics = [
            f"{page.get('row_count', 0)} rows",
            f"{page.get('column_count', 0)} cols",
            f"freeze R{page.get('frozen_row_count', 0)} C{page.get('frozen_column_count', 0)}",
            f"{page.get('conditional_format_rule_count', 0)} rules",
        ]
        for metric in metrics:
            parts.append("<span class='metric'>" + html.escape(metric) + "</span>")
        parts.append("<div>")
        for col in page.get("detected_columns", [])[:12]:
            parts.append("<span class='chip'>" + html.escape(str(col)) + "</span>")
        parts.append("</div>")
        preview_rows = page.get("header_rows_preview", [])[:3]
        if preview_rows:
            parts.append("<table>")
            for row in preview_rows:
                parts.append(
                    "<tr>"
                    + "".join("<td>" + html.escape(str(cell)) + "</td>" for cell in row[:12])
                    + "</tr>"
                )
            parts.append("</table>")
        parts.append("</section>")
    parts.append("</main></body></html>")
    return "".join(parts)


def render_nicegui_app_py(model: dict[str, Any]) -> str:
    model_json_repr = repr(json.dumps(model, ensure_ascii=False, indent=2, sort_keys=True))
    lines = [
        "from __future__ import annotations",
        "import json",
        "from nicegui import ui",
        f"MODEL = json.loads({model_json_repr})",
        "",
        "@ui.page('/')",
        "def index():",
        "    ui.label(MODEL['navigation']['title']).classes('text-h4 q-mb-md')",
        "    ui.label('Replica metadata-driven — no Sheet write / no broker / local only').classes('text-caption')",
        "    with ui.row().classes('q-gutter-sm q-mt-md'):",
        "        for item in MODEL['navigation']['items']:",
        "            ui.link(item['label'], item['route']).classes('q-pa-sm')",
        "",
        "for page in MODEL['pages']:",
        "    route = page['route']",
        "    @ui.page(route)",
        "    def page_view(page=page):",
        "        ui.label(page['title']).classes('text-h5 q-mb-sm')",
        "        ui.label(page['route']).classes('text-caption')",
        "        with ui.row().classes('q-gutter-sm q-mt-md'):",
        "            ui.badge(f\"rows {page['row_count']}\")",
        "            ui.badge(f\"cols {page['column_count']}\")",
        "            ui.badge(f\"freeze R{page['frozen_row_count']} C{page['frozen_column_count']}\")",
        "        columns = [{'name': c, 'label': c, 'field': c} for c in page.get('detected_columns', [])[:20]]",
        "        ui.table(columns=columns, rows=[], row_key='id').classes('q-mt-md')",
        "",
        "if __name__ in {'__main__', '__mp_main__'}:",
        "    ui.run(host='127.0.0.1', port=8088, reload=False, show=True)",
    ]
    return "\n".join(lines) + "\n"


def write_outputs(model: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "P140_NICEGUI_COMPONENT_MODEL.json"
    html_path = output_dir / "P140_STATIC_PREVIEW.html"
    app_path = output_dir / "P140_NICEGUI_REPLICA_APP.py"
    md_path = output_dir / "P140_RENDERER_SPEC.md"
    summary_path = output_dir / "P140_SUMMARY.json"

    model_path.write_text(
        json.dumps(model, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    html_path.write_text(render_static_preview_html(model), encoding="utf-8")
    app_path.write_text(render_nicegui_app_py(model), encoding="utf-8")

    md_lines = [
        "# P140 — NiceGUI Cockpit Replica Renderer",
        "",
        f"- Status: `{model['status']}`",
        f"- Cockpit pages: `{model['cockpit_page_count']}`",
        "",
        "## Routes",
        "",
    ]
    md_lines.extend(f"- `{page['route']}` — {page['title']}" for page in model.get("pages", []))
    md_lines.extend(
        [
            "",
            "## Safety",
            "",
            "- No live read",
            "- No Sheet write",
            "- No broker/order/sizing",
            "",
            f"Next: `{model['next']}`",
            "",
        ]
    )
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    summary = {
        "status": model["status"],
        "cockpit_page_count": model["cockpit_page_count"],
        "source_sheet_count": model.get("source_sheet_count"),
        "google_sheets_write": False,
        "live_google_sheets_read": False,
        "output_dir": str(output_dir),
        "next": model["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    return {
        "model_json": str(model_path),
        "static_preview_html": str(html_path),
        "nicegui_app_py": str(app_path),
        "renderer_spec_md": str(md_path),
        "summary_json": str(summary_path),
    }


def run_render(request: RenderRequest) -> dict[str, Any]:
    payload = load_payload(request.p139_payload_path)
    model = build_component_model(payload)
    model["run_id"] = request.run_id
    model["generated_at_utc"] = request.generated_at_utc
    model["source_p139_payload_path"] = str(request.p139_payload_path)
    outputs = write_outputs(model, request.output_dir)
    model["output_files"] = outputs
    (request.output_dir / "P140_NICEGUI_COMPONENT_MODEL.json").write_text(
        json.dumps(model, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return model


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="P140 NiceGUI cockpit replica renderer from P139 metadata."
    )
    parser.add_argument("--p139-payload", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P140-NICEGUI-COCKPIT-REPLICA-RENDERER")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    model = run_render(
        RenderRequest(
            p139_payload_path=Path(args.p139_payload),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(model["status"])
    print(f"cockpit_page_count={model['cockpit_page_count']}")
    print("google_sheets_write=false")
    print("live_google_sheets_read=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
