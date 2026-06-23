from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P142_UI_FIDELITY_SHELL_1.0.0_SAFE"
STATUS_RENDERED = "P142_UI_FIDELITY_SHELL_RENDERED"

SAFETY_MARKERS = {
    "source": "P140_P141_METADATA_ONLY",
    "live_google_sheets_read": False,
    "google_sheets_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "public_deploy": False,
    "localhost_only": True,
}


@dataclass(frozen=True)
class FidelityRequest:
    p140_model_path: Path
    p141_plan_path: Path
    output_dir: Path
    run_id: str
    generated_at_utc: str


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_inputs(p140_model: dict[str, Any], p141_plan: dict[str, Any]) -> None:
    if p140_model.get("status") != "P140_NICEGUI_COCKPIT_REPLICA_RENDERED_FROM_METADATA":
        raise ValueError(f"Invalid P140 model status: {p140_model.get('status')}")
    if p141_plan.get("status") != "P141_NICEGUI_LOCAL_LAUNCH_SMOKE_PASSED":
        raise ValueError(f"Invalid P141 launch status: {p141_plan.get('status')}")
    if int(p140_model.get("cockpit_page_count", 0) or 0) <= 0:
        raise ValueError("P140 cockpit_page_count must be > 0")
    routes = p141_plan.get("routes", [])
    if not routes:
        raise ValueError("P141 routes must not be empty")


def classify_page(page: dict[str, Any]) -> str:
    title = str(page.get("title", "")).upper()
    if "PROMPT_LIBRARY" in title:
        return "library"
    if "VARIANT" in title or "CONTROL" in title:
        return "control"
    if "RUN_QUEUE" in title or "READY" in title:
        return "operations"
    if "CONTEXT" in title or "LEXIQUE" in title:
        return "knowledge"
    if "RUNTIME" in title or "CONTRACT" in title or "TEMPLATES" in title:
        return "contracts"
    return "support"


def build_ui_shell_spec(
    p140_model: dict[str, Any], p141_plan: dict[str, Any], *, run_id: str, generated_at_utc: str
) -> dict[str, Any]:
    validate_inputs(p140_model, p141_plan)
    pages = p140_model.get("pages", [])
    route_status = {row.get("route"): row for row in p141_plan.get("smoke_results", [])}

    enhanced_pages: list[dict[str, Any]] = []
    for index, page in enumerate(pages):
        route = page.get("route")
        columns = [str(col) for col in page.get("detected_columns", [])]
        smoke = route_status.get(route, {})
        enhanced_pages.append(
            {
                "rank": index + 1,
                "page_id": page.get("page_id"),
                "title": page.get("title"),
                "route": route,
                "domain": classify_page(page),
                "component": page.get("component", "DataGridCard"),
                "priority": page.get("priority", "P1"),
                "row_count": page.get("row_count", 0),
                "column_count": page.get("column_count", 0),
                "frozen_row_count": page.get("frozen_row_count", 0),
                "frozen_column_count": page.get("frozen_column_count", 0),
                "detected_column_count": len(columns),
                "primary_columns": columns[:8],
                "overflow_column_count": max(0, len(columns) - 8),
                "smoke_ok": bool(smoke.get("ok", False)),
                "http_status": smoke.get("http_status"),
                "ui_block_type": "primary_table" if columns else "summary_card",
                "needs_data_binding": True,
            }
        )

    domains: dict[str, int] = {}
    for page in enhanced_pages:
        domains[page["domain"]] = domains.get(page["domain"], 0) + 1

    return {
        "status": STATUS_RENDERED,
        "version": VERSION,
        "run_id": run_id,
        "generated_at_utc": generated_at_utc,
        "source_p140_status": p140_model.get("status"),
        "source_p141_status": p141_plan.get("status"),
        "local_url": p141_plan.get("local_url"),
        "cockpit_page_count": len(enhanced_pages),
        "route_count": len(p141_plan.get("routes", [])),
        "domain_counts": domains,
        "pages": enhanced_pages,
        "layout": {
            "top_bar": True,
            "left_navigation": True,
            "quick_filters": ["domain", "priority", "smoke_ok"],
            "operator_banner": "Local private cockpit — no Sheet write / no broker / no public deploy",
            "table_density": "compact",
            "header_mode": "sticky",
            "card_mode": "sectioned",
        },
        "ui_tokens": {
            "font_family": "Inter, Arial, sans-serif",
            "surface": "#FFFFFF",
            "background": "#F7F7F8",
            "text_primary": "#111827",
            "text_muted": "#6B7280",
            "border": "#E5E7EB",
            "radius_card_px": 16,
            "density": "compact",
        },
        "migration_gates": {
            "p143_data_preview_binding_ready": True,
            "requires_live_sheet_write": False,
            "requires_public_deploy": False,
            "requires_broker": False,
        },
        "safety": dict(SAFETY_MARKERS),
        "next": "P143_DATA_PREVIEW_BINDING_LOCAL_READONLY",
    }


def render_shell_app(spec: dict[str, Any]) -> str:
    spec_repr = repr(json.dumps(spec, ensure_ascii=False, indent=2, sort_keys=True))
    lines = [
        "from __future__ import annotations",
        "import json",
        "from nicegui import ui",
        "",
        f"SPEC = json.loads({spec_repr})",
        "",
        "def _badge(text: str):",
        "    ui.badge(text).classes('q-mr-xs')",
        "",
        "@ui.page('/')",
        "def index():",
        "    ui.label('MVP QAIC — Cockpit historique').classes('text-h4 q-mb-sm')",
        "    ui.label(SPEC['layout']['operator_banner']).classes('text-caption')",
        "    with ui.row().classes('q-gutter-sm q-mt-md'):",
        "        _badge(f\"pages {SPEC['cockpit_page_count']}\")",
        "        _badge(f\"routes {SPEC['route_count']}\")",
        "        _badge('localhost only')",
        "        _badge('no Sheet write')",
        "    with ui.row().classes('q-gutter-md q-mt-lg'):",
        "        for page in SPEC['pages']:",
        "            with ui.card().classes('w-96'):",
        "                ui.label(page['title']).classes('text-subtitle1')",
        "                ui.label(page['route']).classes('text-caption')",
        "                with ui.row().classes('q-gutter-xs q-mt-sm'):",
        "                    _badge(page['domain'])",
        "                    _badge(page['priority'])",
        "                    _badge('smoke ok' if page['smoke_ok'] else 'review')",
        "                ui.separator().classes('q-my-sm')",
        "                ui.label(', '.join(page['primary_columns']) or 'No columns detected').classes('text-caption')",
        "",
        "for page in SPEC['pages']:",
        "    route = page['route']",
        "    @ui.page(route)",
        "    def page_view(page=page):",
        "        ui.link('← Cockpit', '/').classes('q-mb-md')",
        "        ui.label(page['title']).classes('text-h5')",
        "        ui.label(page['route']).classes('text-caption')",
        "        with ui.row().classes('q-gutter-sm q-mt-md'):",
        "            _badge(f\"domain {page['domain']}\")",
        "            _badge(f\"rows {page['row_count']}\")",
        "            _badge(f\"cols {page['column_count']}\")",
        "            _badge(f\"freeze R{page['frozen_row_count']} C{page['frozen_column_count']}\")",
        "        columns = [{'name': c, 'label': c, 'field': c} for c in page.get('primary_columns', [])]",
        "        ui.table(columns=columns, rows=[], row_key='id').classes('q-mt-md')",
        "        ui.label('P143 ajoutera le binding data preview local/read-only.').classes('text-caption q-mt-sm')",
        "",
        "if __name__ in {'__main__', '__mp_main__'}:",
        "    ui.run(host='127.0.0.1', port=8088, reload=False, show=True)",
    ]
    return "\n".join(lines) + "\n"


def write_outputs(spec: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    spec_path = output_dir / "P142_UI_FIDELITY_SHELL_SPEC.json"
    tokens_path = output_dir / "P142_UI_TOKENS.json"
    app_path = output_dir / "P142_NICEGUI_SHELL_APP.py"
    md_path = output_dir / "P142_UI_FIDELITY_SHELL.md"
    summary_path = output_dir / "P142_SUMMARY.json"

    spec_path.write_text(
        json.dumps(spec, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    tokens_path.write_text(
        json.dumps(spec["ui_tokens"], ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    app_path.write_text(render_shell_app(spec), encoding="utf-8")

    route_lines = "\n".join(
        f"- `{page['route']}` — {page['title']} — {page['domain']}" for page in spec["pages"]
    )
    md_path.write_text(
        "\n".join(
            [
                "# P142 — UI Fidelity Shell",
                "",
                f"- Status: `{spec['status']}`",
                f"- Pages: `{spec['cockpit_page_count']}`",
                f"- Routes: `{spec['route_count']}`",
                f"- Local URL: `{spec.get('local_url')}`",
                "",
                "## Routes",
                "",
                route_lines,
                "",
                "## Safety",
                "",
                "- No live Sheets read",
                "- No Sheet write",
                "- No public deploy",
                "- No broker/order/sizing",
                "",
                f"Next: `{spec['next']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = {
        "status": spec["status"],
        "cockpit_page_count": spec["cockpit_page_count"],
        "route_count": spec["route_count"],
        "domain_counts": spec["domain_counts"],
        "google_sheets_write": False,
        "live_google_sheets_read": False,
        "public_deploy": False,
        "output_dir": str(output_dir),
        "next": spec["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    return {
        "spec_json": str(spec_path),
        "tokens_json": str(tokens_path),
        "shell_app_py": str(app_path),
        "shell_md": str(md_path),
        "summary_json": str(summary_path),
    }


def run_fidelity(request: FidelityRequest) -> dict[str, Any]:
    p140_model = load_json(request.p140_model_path)
    p141_plan = load_json(request.p141_plan_path)
    spec = build_ui_shell_spec(
        p140_model,
        p141_plan,
        run_id=request.run_id,
        generated_at_utc=request.generated_at_utc,
    )
    spec["source_p140_model_path"] = str(request.p140_model_path)
    spec["source_p141_plan_path"] = str(request.p141_plan_path)
    outputs = write_outputs(spec, request.output_dir)
    spec["output_files"] = outputs
    (request.output_dir / "P142_UI_FIDELITY_SHELL_SPEC.json").write_text(
        json.dumps(spec, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return spec


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P142 UI fidelity shell from P140/P141 metadata.")
    parser.add_argument("--p140-model", required=True)
    parser.add_argument("--p141-plan", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P142-UI-FIDELITY-SHELL")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    spec = run_fidelity(
        FidelityRequest(
            p140_model_path=Path(args.p140_model),
            p141_plan_path=Path(args.p141_plan),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(spec["status"])
    print(f"cockpit_page_count={spec['cockpit_page_count']}")
    print(f"route_count={spec['route_count']}")
    print("google_sheets_write=false")
    print("public_deploy=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
