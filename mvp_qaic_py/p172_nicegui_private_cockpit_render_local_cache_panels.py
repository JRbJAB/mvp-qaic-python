from __future__ import annotations

import argparse
import csv
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.p171_nicegui_local_prompt_cockpit_bind_cache_panels import (
    build_cockpit_panel_model,
)


SAFETY_FLAGS: dict[str, bool] = {
    "google_sheets_write": False,
    "live_google_api_call_from_python": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "public_serve": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "raw_operator_exports_committed": False,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_csv_preview(
    cache_dir: Path, file_name: str, limit: int
) -> tuple[list[str], list[dict[str, str]], int]:
    path = cache_dir / file_name
    with path.open("r", encoding="utf-8-sig", newline="", errors="replace") as file_obj:
        rows = list(csv.reader(file_obj))

    if not rows:
        return [], [], 0

    header = [str(value) for value in rows[0]]
    data_rows = rows[1:]
    preview: list[dict[str, str]] = []

    for raw_row in data_rows[:limit]:
        item: dict[str, str] = {}
        for index, column in enumerate(header):
            item[column] = str(raw_row[index]) if index < len(raw_row) else ""
        preview.append(item)

    return header, preview, len(data_rows)


def _render_table_html(header: list[str], rows: list[dict[str, str]]) -> str:
    if not header:
        return "<p class='muted'>No rows available.</p>"

    head = "".join(f"<th>{html.escape(column)}</th>" for column in header)
    body_rows = []
    for row in rows:
        cells = "".join(f"<td>{html.escape(str(row.get(column, '')))}</td>" for column in header)
        body_rows.append(f"<tr>{cells}</tr>")

    body = "\n".join(body_rows) if body_rows else "<tr><td colspan='99'>No preview rows.</td></tr>"
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def build_private_cockpit_render_model(
    project_root: str | Path,
    *,
    preview_limit: int = 5,
    generated_at: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    p171_payload = build_cockpit_panel_model(root, preview_limit=preview_limit)
    cache_dir = Path(str(p171_payload.get("cache_dir")))
    generated = generated_at or _utc_now()

    render_panels: list[dict[str, Any]] = []
    blockers: list[str] = list(p171_payload.get("blockers", []))

    for panel in p171_payload.get("panels", []):
        file_name = str(panel["file_name"])
        path = cache_dir / file_name
        if not path.exists():
            blockers.append(f"MISSING_RENDER_CACHE_FILE:{file_name}")
            continue

        header, preview_rows, row_count = _read_csv_preview(cache_dir, file_name, preview_limit)
        render_panels.append(
            {
                "panel_id": panel["panel_id"],
                "ui_slot": panel["ui_slot"],
                "panel_title": panel["panel_title"],
                "source_id": panel["source_id"],
                "file_name": file_name,
                "row_count": row_count,
                "preview_limit": preview_limit,
                "preview_header": header,
                "preview_rows": preview_rows,
                "render_status": "READY_FOR_PRIVATE_HTML_RENDER",
                "nicegui_component_hint": "ui.card + ui.table",
                "write_allowed": False,
                "live_api_allowed": False,
                "public_access_allowed": False,
                "human_review_required": True,
            }
        )

    ready_render_panel_count = len(render_panels)
    render_ready = (
        bool(p171_payload.get("cockpit_ready")) and ready_render_panel_count == 5 and not blockers
    )

    return {
        "STATUS": "OK_P172_NICEGUI_PRIVATE_COCKPIT_RENDER_READY_REVIEW_ONLY"
        if render_ready
        else "BLOCKED_P172_NICEGUI_PRIVATE_COCKPIT_RENDER",
        "generated_at": generated,
        "project_root": str(root),
        "source_step": "P171_NICEGUI_LOCAL_PROMPT_COCKPIT_CACHE_PANELS",
        "cache_dir": str(cache_dir),
        "host": "127.0.0.1",
        "port": 8088,
        "route_count": 3,
        "routes": [
            {"route": "/", "label": "Home", "public_access_allowed": False},
            {"route": "/cache", "label": "Cache panels", "public_access_allowed": False},
            {"route": "/review", "label": "Human review", "public_access_allowed": False},
        ],
        "render_panel_count": len(render_panels),
        "ready_render_panel_count": ready_render_panel_count,
        "render_ready": render_ready,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "render_panels": render_panels,
        **SAFETY_FLAGS,
        "recommended_next": "P173_NICEGUI_PRIVATE_LOCAL_RUNNER_AND_SMOKE",
    }


def render_static_private_cockpit_html(payload: dict[str, Any]) -> str:
    panels = []
    for panel in payload.get("render_panels", []):
        table = _render_table_html(panel["preview_header"], panel["preview_rows"])
        panels.append(
            "\n".join(
                [
                    "<section class='panel'>",
                    f"<h2>{html.escape(panel['panel_title'])}</h2>",
                    f"<p><strong>Source:</strong> {html.escape(panel['source_id'])} | "
                    f"<strong>Rows:</strong> {panel['row_count']} | "
                    f"<strong>Mode:</strong> LOCAL_CACHE_READ_ONLY</p>",
                    table,
                    "</section>",
                ]
            )
        )

    panel_html = "\n".join(panels)
    status = html.escape(str(payload["STATUS"]))

    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>MVP QAIC — Private Local Cockpit Preview</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; background: #f6f7f9; color: #111; }}
header {{ background: white; border: 1px solid #ddd; border-radius: 12px; padding: 18px; margin-bottom: 18px; }}
.panel {{ background: white; border: 1px solid #ddd; border-radius: 12px; padding: 16px; margin-bottom: 16px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 12px; }}
th, td {{ border: 1px solid #ddd; padding: 6px; vertical-align: top; }}
th {{ background: #f0f0f0; text-align: left; }}
.badge {{ display: inline-block; padding: 4px 8px; border: 1px solid #bbb; border-radius: 999px; background: #fafafa; }}
.muted {{ color: #666; }}
</style>
</head>
<body>
<header>
<h1>MVP QAIC â€” Private Local Cockpit Preview</h1>
<p class="badge">{status}</p>
<p>Host prÃ©vu: 127.0.0.1 | Port prÃ©vu: 8088 | Public serve: False | Google Sheets write: False</p>
</header>
{panel_html}
</body>
</html>
"""


def export_private_cockpit_render(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    preview_limit: int = 5,
) -> dict[str, Any]:
    root = Path(project_root)
    if export_dir is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = root / "05_EXPORTS" / f"P172_NICEGUI_PRIVATE_COCKPIT_RENDER_{stamp}"
    else:
        export_path = Path(export_dir)

    export_path.mkdir(parents=True, exist_ok=True)
    payload = build_private_cockpit_render_model(root, preview_limit=preview_limit)
    payload["export_dir"] = str(export_path)

    (export_path / "P172_PRIVATE_COCKPIT_RENDER_MODEL.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "source_step",
        "cache_dir",
        "export_dir",
        "host",
        "port",
        "route_count",
        "render_panel_count",
        "ready_render_panel_count",
        "render_ready",
        "blocker_count",
        "blockers",
        "google_sheets_write",
        "live_google_api_call_from_python",
        "apps_script_execution",
        "clasp_push",
        "public_serve",
        "broker",
        "order",
        "sizing",
        "raw_operator_exports_committed",
        "recommended_next",
    ]
    (export_path / "P172_SUMMARY.json").write_text(
        json.dumps({key: payload[key] for key in summary_keys}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with (export_path / "P172_PRIVATE_COCKPIT_RENDER_PANELS.csv").open(
        "w", encoding="utf-8", newline=""
    ) as file_obj:
        fieldnames = [
            "panel_id",
            "ui_slot",
            "panel_title",
            "source_id",
            "file_name",
            "row_count",
            "preview_limit",
            "render_status",
            "nicegui_component_hint",
            "write_allowed",
            "live_api_allowed",
            "public_access_allowed",
            "human_review_required",
        ]
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for panel in payload["render_panels"]:
            writer.writerow({key: panel[key] for key in fieldnames})

    html_text = render_static_private_cockpit_html(payload)
    (export_path / "P172_PRIVATE_COCKPIT_PREVIEW.html").write_text(html_text, encoding="utf-8")

    report_lines = [
        "# P172 NiceGUI Private Cockpit Render Local Cache Panels",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- render_panel_count: {payload['render_panel_count']}",
        f"- ready_render_panel_count: {payload['ready_render_panel_count']}",
        f"- render_ready: {payload['render_ready']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "Decision:",
        "- Render model and static HTML preview are ready from local cache.",
        "- Next step can build/launch the private NiceGUI runner on 127.0.0.1:8088.",
        "- No public serve.",
        "- No Google Sheets live API.",
        "- No Sheet write.",
        "",
        "Safety:",
        "- GOOGLE_SHEETS_WRITE=False",
        "- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False",
        "- APPS_SCRIPT_EXECUTION=False",
        "- CLASP_PUSH=False",
        "- PUBLIC_SERVE=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
        "",
        "Next:",
        "- P173_NICEGUI_PRIVATE_LOCAL_RUNNER_AND_SMOKE",
    ]
    (export_path / "P172_PRIVATE_COCKPIT_RENDER_REPORT.md").write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build P172 private cockpit render model.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--preview-limit", type=int, default=5)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.write_export:
        payload = export_private_cockpit_render(
            args.project_root,
            export_dir=args.export_dir,
            preview_limit=args.preview_limit,
        )
    else:
        payload = build_private_cockpit_render_model(
            args.project_root, preview_limit=args.preview_limit
        )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"RENDER_PANEL_COUNT={payload['render_panel_count']}")
        print(f"READY_RENDER_PANEL_COUNT={payload['ready_render_panel_count']}")
        print(f"RENDER_READY={payload['render_ready']}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0 if payload["render_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
