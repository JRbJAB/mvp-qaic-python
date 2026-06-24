from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.p172_nicegui_private_cockpit_render_local_cache_panels import (
    build_private_cockpit_render_model,
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
    "server_started_by_smoke": False,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _nicegui_available() -> bool:
    return importlib.util.find_spec("nicegui") is not None


def build_private_runner_config(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8088,
    preview_limit: int = 5,
    require_nicegui: bool = False,
    generated_at: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    render_payload = build_private_cockpit_render_model(root, preview_limit=preview_limit)
    generated = generated_at or _utc_now()

    blockers: list[str] = list(render_payload.get("blockers", []))
    if host != "127.0.0.1":
        blockers.append("PUBLIC_OR_NON_LOCAL_HOST_BLOCKED")
    if port <= 0 or port > 65535:
        blockers.append("INVALID_LOCAL_PORT")

    nicegui_available = _nicegui_available()
    if require_nicegui and not nicegui_available:
        blockers.append("NICEGUI_IMPORT_NOT_AVAILABLE")

    route_rows: list[dict[str, Any]] = []
    for route in render_payload.get("routes", []):
        route_rows.append(
            {
                "route": route["route"],
                "label": route["label"],
                "host": host,
                "port": port,
                "public_access_allowed": False,
                "route_status": "READY_FOR_PRIVATE_LOCAL_RUNNER",
            }
        )

    smoke_ok = (
        bool(render_payload.get("render_ready"))
        and len(route_rows) == 3
        and host == "127.0.0.1"
        and 0 < port <= 65535
        and not blockers
    )

    return {
        "STATUS": "OK_P173_NICEGUI_PRIVATE_LOCAL_RUNNER_SMOKE_READY_REVIEW_ONLY"
        if smoke_ok
        else "BLOCKED_P173_NICEGUI_PRIVATE_LOCAL_RUNNER_SMOKE",
        "generated_at": generated,
        "project_root": str(root),
        "source_step": "P172_NICEGUI_PRIVATE_COCKPIT_RENDER_LOCAL_CACHE",
        "host": host,
        "port": port,
        "preview_limit": preview_limit,
        "nicegui_import_available": nicegui_available,
        "require_nicegui": require_nicegui,
        "route_count": len(route_rows),
        "route_rows": route_rows,
        "render_panel_count": render_payload.get("render_panel_count", 0),
        "ready_render_panel_count": render_payload.get("ready_render_panel_count", 0),
        "smoke_ok": smoke_ok,
        "blocker_count": len(blockers),
        "blockers": blockers,
        "launch_command": (
            "python -m mvp_qaic_py.p173_nicegui_private_local_runner "
            "--project-root . --host 127.0.0.1 --port 8088 --serve-private"
        ),
        **SAFETY_FLAGS,
        "recommended_next": "P174_NICEGUI_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE",
    }


def export_private_runner_smoke(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    host: str = "127.0.0.1",
    port: int = 8088,
    preview_limit: int = 5,
    require_nicegui: bool = False,
) -> dict[str, Any]:
    root = Path(project_root)
    if export_dir is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = root / "05_EXPORTS" / f"P173_NICEGUI_PRIVATE_LOCAL_RUNNER_SMOKE_{stamp}"
    else:
        export_path = Path(export_dir)

    export_path.mkdir(parents=True, exist_ok=True)
    payload = build_private_runner_config(
        root,
        host=host,
        port=port,
        preview_limit=preview_limit,
        require_nicegui=require_nicegui,
    )
    payload["export_dir"] = str(export_path)

    (export_path / "P173_PRIVATE_LOCAL_RUNNER_CONFIG.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "source_step",
        "export_dir",
        "host",
        "port",
        "preview_limit",
        "nicegui_import_available",
        "require_nicegui",
        "route_count",
        "render_panel_count",
        "ready_render_panel_count",
        "smoke_ok",
        "blocker_count",
        "blockers",
        "launch_command",
        "google_sheets_write",
        "live_google_api_call_from_python",
        "apps_script_execution",
        "clasp_push",
        "public_serve",
        "broker",
        "order",
        "sizing",
        "raw_operator_exports_committed",
        "server_started_by_smoke",
        "recommended_next",
    ]
    (export_path / "P173_SUMMARY.json").write_text(
        json.dumps({key: payload[key] for key in summary_keys}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with (export_path / "P173_PRIVATE_LOCAL_ROUTES.csv").open(
        "w", encoding="utf-8", newline=""
    ) as file_obj:
        fieldnames = ["route", "label", "host", "port", "public_access_allowed", "route_status"]
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(payload["route_rows"])

    launcher = "\n".join(
        [
            '$ErrorActionPreference = "Stop"',
            "chcp 65001 | Out-Null",
            "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8",
            "$OutputEncoding = [System.Text.Encoding]::UTF8",
            "",
            "# Private local launch only. Do not change host to 0.0.0.0.",
            'Set-Location -LiteralPath "C:\\Users\\Julie\\Documents\\JRb-Dev\\MVP_QAIC_PY_WORK_20260623_192901"',
            "python -m mvp_qaic_py.p173_nicegui_private_local_runner --project-root . --host 127.0.0.1 --port 8088 --serve-private",
            "",
        ]
    )
    (export_path / "P173_RUN_PRIVATE_LOCAL_COCKPIT.ps1").write_text(launcher, encoding="utf-8")

    report_lines = [
        "# P173 NiceGUI Private Local Runner And Smoke",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- host: {payload['host']}",
        f"- port: {payload['port']}",
        f"- nicegui_import_available: {payload['nicegui_import_available']}",
        f"- route_count: {payload['route_count']}",
        f"- render_panel_count: {payload['render_panel_count']}",
        f"- ready_render_panel_count: {payload['ready_render_panel_count']}",
        f"- smoke_ok: {payload['smoke_ok']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "Decision:",
        "- Private runner config is ready for 127.0.0.1 only.",
        "- Smoke does not start a long-running server.",
        "- P174 may run the local operator launch.",
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
        "- P174_NICEGUI_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE",
    ]
    (export_path / "P173_PRIVATE_LOCAL_RUNNER_SMOKE_REPORT.md").write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    return payload


def serve_private(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8088,
    show: bool = True,
) -> None:
    if host != "127.0.0.1":
        raise ValueError("Only 127.0.0.1 is allowed for private local runner.")

    try:
        from nicegui import ui
    except Exception as exc:  # pragma: no cover - depends on operator environment
        raise RuntimeError("NiceGUI is not available in this environment.") from exc

    render_payload = build_private_cockpit_render_model(project_root)
    panels = render_payload.get("render_panels", [])
    panel_by_slot = {panel.get("ui_slot"): panel for panel in panels}

    prompt_text = "\n".join(
        [
            "# MVP QAIC — GEM Portfolio Image Review",
            "",
            "Réponds en français.",
            "Analyse une capture portfolio crypto.",
            "Extrais uniquement les données visibles.",
            "N'invente aucun prix, PRU, quantité, PnL, TP, SL ou exposition.",
            "Retourne REVIEW_REQUIRED si données insuffisantes.",
            "Aucun ordre, aucun sizing, aucun auto-apply.",
            "Conserve les enums techniques exacts.",
            "",
            "Sortie attendue:",
            "- JSON structuré",
            "- missing_data",
            "- blockers",
            "- safety_audit",
            "- décision humaine review-only",
        ]
    )

    def _rows_for(panel: dict[str, Any]) -> list[dict[str, Any]]:
        header = [str(item) for item in panel.get("preview_header", [])]
        raw_rows = panel.get("preview_rows", [])
        rows: list[dict[str, Any]] = []
        for row in raw_rows:
            if isinstance(row, dict):
                rows.append({str(key): value for key, value in row.items()})
            elif isinstance(row, list):
                rows.append(
                    {header[index]: value for index, value in enumerate(row) if index < len(header)}
                )
        return rows

    def _columns_for(panel: dict[str, Any]) -> list[dict[str, Any]]:
        header = [str(item) for item in panel.get("preview_header", [])]
        if not header:
            rows = _rows_for(panel)
            header = list(rows[0].keys()) if rows else ["status"]
        return [
            {"name": column, "label": column, "field": column, "align": "left", "sortable": True}
            for column in header[:12]
        ]

    def _status_card(title: str, value: str, caption: str) -> None:
        with ui.card().classes("qaic-card"):
            ui.label(title).classes("qaic-card-title")
            ui.label(value).classes("qaic-card-value")
            ui.label(caption).classes("qaic-card-caption")

    def _panel_table(
        panel: dict[str, Any] | None, empty: str = "Aucune donnée disponible."
    ) -> None:
        if not panel:
            ui.label(empty).classes("qaic-muted")
            return
        ui.label(str(panel.get("panel_title", "Panel"))).classes("qaic-section-title")
        ui.label(
            f"Source: {panel.get('source_id', '?')} · Rows: {panel.get('row_count', 0)}"
        ).classes("qaic-muted")
        rows = _rows_for(panel)
        columns = _columns_for(panel)
        ui.table(columns=columns, rows=rows, row_key=columns[0]["name"]).classes("qaic-table")

    def _render_cockpit(default_tab: str = "dashboard") -> None:
        ui.add_head_html(
            """
            <style>
              body { background: #f6f7fb; }
              .qaic-shell { max-width: 1440px; margin: 0 auto; }
              .qaic-hero {
                background: linear-gradient(135deg, #0f172a, #1e3a8a);
                color: white; border-radius: 22px; padding: 28px;
                box-shadow: 0 14px 35px rgba(15, 23, 42, .18);
              }
              .qaic-title { font-size: 34px; font-weight: 800; letter-spacing: -.02em; }
              .qaic-subtitle { opacity: .86; font-size: 15px; margin-top: 6px; }
              .qaic-card {
                border-radius: 18px; padding: 18px; min-width: 210px;
                box-shadow: 0 8px 22px rgba(15, 23, 42, .08);
              }
              .qaic-card-title { font-size: 12px; text-transform: uppercase; color: #64748b; font-weight: 700; }
              .qaic-card-value { font-size: 28px; font-weight: 800; color: #0f172a; margin-top: 4px; }
              .qaic-card-caption { font-size: 13px; color: #64748b; margin-top: 4px; }
              .qaic-section-title { font-size: 21px; font-weight: 800; color: #0f172a; margin-top: 8px; }
              .qaic-muted { color: #64748b; font-size: 14px; }
              .qaic-table { width: 100%; border-radius: 16px; overflow: hidden; }
              .qaic-panel { background: white; border-radius: 18px; padding: 18px; }
              .qaic-danger { color: #b91c1c; font-weight: 700; }
              .qaic-ok { color: #047857; font-weight: 800; }
            </style>
            """
        )

        with ui.column().classes("qaic-shell w-full gap-5 p-6"):
            with ui.row().classes("qaic-hero w-full items-center justify-between"):
                with ui.column().classes("gap-1"):
                    ui.label("MVP QAIC — Private Cockpit").classes("qaic-title")
                    ui.label("Prompt GEM · Cache local · Review-only · 127.0.0.1").classes(
                        "qaic-subtitle"
                    )
                with ui.column().classes("items-end gap-2"):
                    ui.badge("PRIVATE LOCAL", color="green").classes("text-md")
                    ui.label("No Sheet write · No broker · No auto-apply").classes("qaic-subtitle")

            with ui.row().classes("w-full gap-4"):
                _status_card("Status", "READY", str(render_payload.get("STATUS", "UNKNOWN")))
                _status_card("Panels", str(len(panels)), "Sources locales rendues")
                _status_card("Routes", "6", "/ /prompt /cache /review /journal /lexique")
                _status_card("Safety", "LOCKED", "Review-only, no order, no sizing")

            with ui.tabs().classes("w-full") as tabs:
                tab_dashboard = ui.tab("Dashboard")
                tab_prompt = ui.tab("Prompt GEM")
                tab_cache = ui.tab("Cache local")
                tab_review = ui.tab("Review")
                tab_journal = ui.tab("Journal")
                tab_lexique = ui.tab("Lexique")

            selected = {
                "dashboard": tab_dashboard,
                "prompt": tab_prompt,
                "cache": tab_cache,
                "review": tab_review,
                "journal": tab_journal,
                "lexique": tab_lexique,
            }.get(default_tab, tab_dashboard)

            with ui.tab_panels(tabs, value=selected).classes("w-full"):
                with ui.tab_panel(tab_dashboard):
                    with ui.column().classes("qaic-panel w-full gap-4"):
                        ui.label("Vue opérateur").classes("qaic-section-title")
                        ui.label(
                            "Cockpit privé utilisable pour préparer le prompt GEM, consulter le cache "
                            "et faire une review humaine sans écriture live."
                        ).classes("qaic-muted")
                        with ui.row().classes("gap-4"):
                            for panel in panels:
                                _status_card(
                                    str(panel.get("panel_title", "Panel")),
                                    str(panel.get("row_count", 0)),
                                    str(panel.get("source_id", "?")),
                                )

                with ui.tab_panel(tab_prompt):
                    with ui.column().classes("qaic-panel w-full gap-4"):
                        ui.label("Prompt GEM portfolio").classes("qaic-section-title")
                        ui.label(
                            "Copie ce prompt, puis colle la capture dans GEM manuellement."
                        ).classes("qaic-muted")
                        ui.textarea(value=prompt_text).props("outlined autogrow").classes("w-full")
                        ui.button(
                            "Copier le prompt",
                            on_click=lambda: ui.run_javascript(
                                f"navigator.clipboard.writeText({json.dumps(prompt_text)})"
                            ),
                        ).props("color=primary")
                        ui.label("Auto-apply désactivé · GEM call Python désactivé").classes(
                            "qaic-ok"
                        )
                        _panel_table(panel_by_slot.get("prompt_source_selector"))

                with ui.tab_panel(tab_cache):
                    with ui.column().classes("qaic-panel w-full gap-4"):
                        ui.label("Cache local").classes("qaic-section-title")
                        ui.label(
                            "Toutes les sources locales disponibles en lecture seule."
                        ).classes("qaic-muted")
                        for panel in panels:
                            _panel_table(panel)

                with ui.tab_panel(tab_review):
                    with ui.column().classes("qaic-panel w-full gap-4"):
                        ui.label("Review humaine").classes("qaic-section-title")
                        ui.label(
                            "Prévisualisation uniquement. Apply decision et patch prompt restent bloqués."
                        ).classes("qaic-muted")
                        ui.badge("APPLY BLOCKED", color="red")
                        _panel_table(panel_by_slot.get("human_review_workbench_panel"))

                with ui.tab_panel(tab_journal):
                    with ui.column().classes("qaic-panel w-full gap-4"):
                        ui.label("Journal").classes("qaic-section-title")
                        _panel_table(panel_by_slot.get("decision_history_panel"))

                with ui.tab_panel(tab_lexique):
                    with ui.column().classes("qaic-panel w-full gap-4"):
                        ui.label("Lexique / contexte cockpit").classes("qaic-section-title")
                        _panel_table(panel_by_slot.get("lexique_context_panel"))

    @ui.page("/")
    def home() -> None:
        _render_cockpit("dashboard")

    @ui.page("/prompt")
    def prompt() -> None:
        _render_cockpit("prompt")

    @ui.page("/cache")
    def cache() -> None:
        _render_cockpit("cache")

    @ui.page("/review")
    def review() -> None:
        _render_cockpit("review")

    @ui.page("/journal")
    def journal() -> None:
        _render_cockpit("journal")

    @ui.page("/lexique")
    def lexique() -> None:
        _render_cockpit("lexique")

    @ui.page("/favicon.ico")
    def favicon() -> None:
        ui.response(status_code=204)

    ui.run(host=host, port=port, reload=False, show=show)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P173 private local NiceGUI runner smoke.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8088)
    parser.add_argument("--preview-limit", type=int, default=5)
    parser.add_argument("--require-nicegui", action="store_true")
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--serve-private", action="store_true")
    parser.add_argument("--no-show", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.serve_private:
        serve_private(args.project_root, host=args.host, port=args.port, show=not args.no_show)
        return 0

    if args.write_export:
        payload = export_private_runner_smoke(
            args.project_root,
            export_dir=args.export_dir,
            host=args.host,
            port=args.port,
            preview_limit=args.preview_limit,
            require_nicegui=args.require_nicegui,
        )
    else:
        payload = build_private_runner_config(
            args.project_root,
            host=args.host,
            port=args.port,
            preview_limit=args.preview_limit,
            require_nicegui=args.require_nicegui,
        )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"ROUTE_COUNT={payload['route_count']}")
        print(f"SMOKE_OK={payload['smoke_ok']}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0 if payload["smoke_ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
