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
        from nicegui import events, ui
    except Exception as exc:  # pragma: no cover - depends on operator environment
        raise RuntimeError("NiceGUI is not available in this environment.") from exc

    root = Path(project_root)
    capture_dir = root / "00_OPERATOR_EXPORTS" / "P181_CAPTURE_INBOX"
    response_dir = root / "00_OPERATOR_EXPORTS" / "P181_GEM_RESPONSES"
    session_dir = root / "00_OPERATOR_EXPORTS" / "P181_SESSION_LOG"
    capture_dir.mkdir(parents=True, exist_ok=True)
    response_dir.mkdir(parents=True, exist_ok=True)
    session_dir.mkdir(parents=True, exist_ok=True)

    render_payload = build_private_cockpit_render_model(root)
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

    def _now_id(prefix: str) -> str:
        import datetime as _dt

        return prefix + "-" + _dt.datetime.now().strftime("%Y%m%d-%H%M%S")

    def _save_upload(e: events.UploadEventArguments) -> None:
        safe_name = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in e.name)
        target = capture_dir / (_now_id("CAPTURE") + "_" + safe_name)
        with target.open("wb") as file_obj:
            file_obj.write(e.content.read())
        ui.notify(f"Capture sauvegardée localement: {target.name}", color="positive")

    def _save_text_file(prefix: str, text_value: str, folder: Path, suffix: str = ".md") -> Path:
        target = folder / (_now_id(prefix) + suffix)
        target.write_text(text_value, encoding="utf-8")
        return target

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
        ui.table(columns=columns, rows=rows, row_key=columns[0]["name"]).props(
            "flat bordered dense"
        ).classes("qaic-table")

    def _status_card(title: str, value: str, caption: str, tone: str = "neutral") -> None:
        tone_class = {
            "good": "qaic-card-good",
            "warn": "qaic-card-warn",
            "danger": "qaic-card-danger",
        }.get(tone, "qaic-card")
        with ui.card().classes(tone_class):
            ui.label(title).classes("qaic-card-title")
            ui.label(value).classes("qaic-card-value")
            ui.label(caption).classes("qaic-card-caption")

    def _nav_button(label: str, route: str, icon: str) -> None:
        ui.button(label, icon=icon, on_click=lambda r=route: ui.navigate.to(r)).props(
            "flat align=left"
        ).classes("qaic-nav-button")

    def _sessions_rows() -> list[dict[str, Any]]:
        captures = sorted(capture_dir.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)[:20]
        responses = sorted(response_dir.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)[
            :20
        ]
        rows: list[dict[str, Any]] = []
        for item in captures:
            rows.append({"type": "capture", "file": item.name, "folder": "P181_CAPTURE_INBOX"})
        for item in responses:
            rows.append({"type": "gem_response", "file": item.name, "folder": "P181_GEM_RESPONSES"})
        return rows[:30]

    def _session_columns() -> list[dict[str, Any]]:
        return [
            {"name": "type", "label": "type", "field": "type", "align": "left", "sortable": True},
            {"name": "file", "label": "file", "field": "file", "align": "left", "sortable": True},
            {
                "name": "folder",
                "label": "folder",
                "field": "folder",
                "align": "left",
                "sortable": True,
            },
        ]

    def _shell(active: str) -> None:
        ui.add_head_html(
            """
            <style>
              body { background: #eef2f7; font-family: Inter, Arial, sans-serif; }
              .qaic-app { max-width: 1500px; margin: 0 auto; }
              .qaic-top {
                background: linear-gradient(135deg, #08111f, #102b64 55%, #0f766e);
                color: white; border-radius: 24px; padding: 24px 28px;
                box-shadow: 0 16px 40px rgba(15, 23, 42, .20);
              }
              .qaic-title { font-size: 32px; font-weight: 900; letter-spacing: -.03em; }
              .qaic-subtitle { opacity: .88; font-size: 14px; margin-top: 5px; }
              .qaic-grid { display: grid; grid-template-columns: 250px 1fr; gap: 18px; }
              .qaic-sidebar {
                background: white; border-radius: 22px; padding: 16px;
                box-shadow: 0 10px 26px rgba(15, 23, 42, .08);
                min-height: 680px;
              }
              .qaic-main {
                background: white; border-radius: 22px; padding: 20px;
                box-shadow: 0 10px 26px rgba(15, 23, 42, .08);
                min-height: 680px;
              }
              .qaic-nav-button { width: 100%; justify-content: flex-start; margin: 3px 0; }
              .qaic-section-title { font-size: 22px; font-weight: 900; color: #0f172a; }
              .qaic-muted { color: #64748b; font-size: 14px; }
              .qaic-card, .qaic-card-good, .qaic-card-warn, .qaic-card-danger {
                border-radius: 18px; padding: 16px; min-width: 170px;
                box-shadow: 0 8px 20px rgba(15, 23, 42, .07);
              }
              .qaic-card-good { border-left: 6px solid #059669; }
              .qaic-card-warn { border-left: 6px solid #f59e0b; }
              .qaic-card-danger { border-left: 6px solid #dc2626; }
              .qaic-card-title { font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 800; }
              .qaic-card-value { font-size: 24px; font-weight: 900; color: #0f172a; margin-top: 4px; }
              .qaic-card-caption { font-size: 12px; color: #64748b; margin-top: 3px; }
              .qaic-table { width: 100%; border-radius: 14px; overflow: hidden; }
              .qaic-prompt-box textarea { font-family: Consolas, monospace; font-size: 13px; }
              .qaic-drop {
                border: 2px dashed #94a3b8; border-radius: 18px; padding: 18px;
                background: #f8fafc;
              }
            </style>
            """
        )

        with ui.column().classes("qaic-app w-full gap-5 p-5"):
            with ui.row().classes("qaic-top w-full items-center justify-between"):
                with ui.column().classes("gap-1"):
                    ui.label("MVP QAIC — Private Operator Cockpit").classes("qaic-title")
                    ui.label(
                        "Prompt Studio · Capture Inbox · GEM Response Inbox · Sessions · Review-only"
                    ).classes("qaic-subtitle")
                with ui.column().classes("items-end gap-2"):
                    ui.badge("127.0.0.1 ONLY", color="green")
                    ui.label("No Sheet write · No GEM call · No broker/order/sizing").classes(
                        "qaic-subtitle"
                    )

            with ui.element("div").classes("qaic-grid w-full"):
                with ui.column().classes("qaic-sidebar gap-2"):
                    ui.label("Navigation").classes("qaic-section-title")
                    _nav_button("Dashboard", "/", "dashboard")
                    _nav_button("Prompt Studio", "/prompt", "article")
                    _nav_button("Capture Inbox", "/capture", "image")
                    _nav_button("GEM Responses", "/responses", "data_object")
                    _nav_button("Sessions", "/sessions", "history")
                    _nav_button("Roundtrip", "/roundtrip", "sync_alt")
                    _nav_button("Real Case", "/real-case", "rule")
                    _nav_button("Migration", "/migration", "dashboard")
                    _nav_button("GEM Tracking", "/gem-tracking", "table_view")
                    _nav_button("GEM Ops", "/gem-tracking-operator", "fact_check")
                    _nav_button("GEM Evidence", "/gem-evidence", "inventory")
                    _nav_button("Runtime Contract", "/runtime-contract", "assignment")
                    _nav_button("Operator Release", "/operator-release", "rocket_launch")
                    _nav_button("Cas réel", "/real-case-inputs", "upload_file")
                    _nav_button("Prompt Master", "/prompt-master", "psychology")
                    _nav_button("Sheets Dry-run", "/sheets-export", "table_chart")
                    _nav_button("Migration Map", "/apps-script-map", "account_tree")
                    _nav_button("Dev Roadmap", "/dev-roadmap", "timeline")
                    _nav_button("Migration Control", "/migration-control", "fact_check")
                    _nav_button("Instructions", "/instructions", "rule")
                    _nav_button("Release Final", "/release-final", "verified")
                    _nav_button("Review", "/review", "fact_check")
                    _nav_button("Cache", "/cache", "storage")
                    _nav_button("Journal", "/journal", "list_alt")
                    _nav_button("Lexique", "/lexique", "menu_book")
                    ui.separator()
                    ui.label(f"Active: {active}").classes("qaic-muted")
                    ui.label("Mode: REVIEW_ONLY").classes("qaic-muted")
                    ui.label("Apply: BLOCKED").classes("qaic-muted")
                    ui.label("Broker: BLOCKED").classes("qaic-muted")

                with ui.column().classes("qaic-main gap-5") as main:
                    return main

    def _dashboard_page() -> None:
        with _shell("dashboard"):
            _render_global_visual_banner("dashboard")
            ui.label("Dashboard opérateur").classes("qaic-section-title")
            ui.label("Vue rapide du cockpit privé local et des sources prêtes.").classes(
                "qaic-muted"
            )
            with ui.row().classes("gap-4"):
                _status_card("UI", "READY", "P181ABC visual cockpit", "good")
                _status_card("Panels", str(len(panels)), "sources locales", "good")
                _status_card("Prompt", "ACTIVE", "portfolio image review", "good")
                _status_card("Apply", "BLOCKED", "human review only", "danger")
                _status_card("Sessions", str(len(_sessions_rows())), "local files", "warn")
            ui.separator()
            for panel in panels:
                _status_card(
                    str(panel.get("panel_title", "Panel")),
                    str(panel.get("row_count", 0)),
                    str(panel.get("source_id", "?")),
                    "good",
                )

    def _prompt_page() -> None:
        with _shell("prompt"):
            _render_global_visual_banner("prompt")
            ui.label("Prompt Studio").classes("qaic-section-title")
            ui.label(
                "Version active review-only. Les prompts historiques seront ajoutés en bibliothèque versionnée."
            ).classes("qaic-muted")
            ui.textarea(value=prompt_text).props("outlined autogrow").classes(
                "w-full qaic-prompt-box"
            )
            with ui.row().classes("gap-3"):
                ui.button(
                    "Copier prompt actif",
                    icon="content_copy",
                    on_click=lambda: ui.run_javascript(
                        f"navigator.clipboard.writeText({json.dumps(prompt_text)})"
                    ),
                ).props("color=primary")
                ui.button(
                    "Créer session locale",
                    icon="add",
                    on_click=lambda: ui.notify(
                        "Session locale à formaliser en P182/P183 — aucun apply automatique.",
                        color="warning",
                    ),
                )

            ui.separator()
            ui.label("Prompt History Library").classes("qaic-section-title")
            ui.label(
                "Inventaire versionné: prompt actif, prompts historiques, exports de référence. "
                "Aucun apply automatique."
            ).classes("qaic-muted")
            ui.table(
                columns=[
                    {
                        "name": "prompt_id",
                        "label": "prompt_id",
                        "field": "prompt_id",
                        "align": "left",
                        "sortable": True,
                    },
                    {
                        "name": "status",
                        "label": "status",
                        "field": "status",
                        "align": "left",
                        "sortable": True,
                    },
                    {
                        "name": "source",
                        "label": "source",
                        "field": "source",
                        "align": "left",
                        "sortable": True,
                    },
                ],
                rows=[
                    {
                        "prompt_id": "ACTIVE_GEM_PORTFOLIO_IMAGE_REVIEW",
                        "status": "ACTIVE_RUNTIME",
                        "source": "p173_private_cockpit",
                    },
                    {
                        "prompt_id": "HISTORICAL_PROMPT_EXPORTS",
                        "status": "HISTORICAL_REFERENCE_ONLY",
                        "source": "05_EXPORTS",
                    },
                    {
                        "prompt_id": "PROMPT_PATCH_HISTORY",
                        "status": "REFERENCE_AUDIT",
                        "source": "P152-P180 chain",
                    },
                ],
                row_key="prompt_id",
            ).props("flat bordered dense").classes("qaic-table")
            _panel_table(panel_by_slot.get("prompt_source_selector"))

    def _capture_page() -> None:
        with _shell("capture"):
            _render_global_visual_banner("capture")
            ui.label("Capture Inbox").classes("qaic-section-title")
            ui.label(
                "Upload local privé de captures portfolio. Coller depuis presse-papiers navigateur sera durci au prochain batch."
            ).classes("qaic-muted")
            with ui.column().classes("qaic-drop w-full gap-3"):
                ui.upload(on_upload=_save_upload, auto_upload=True).props("accept=image/*").classes(
                    "w-full"
                )
                ui.label(f"Dossier local: {capture_dir}").classes("qaic-muted")
            ui.separator()
            rows = [
                {"file": p.name, "folder": "P181_CAPTURE_INBOX"}
                for p in sorted(
                    capture_dir.glob("*"), key=lambda x: x.stat().st_mtime, reverse=True
                )[:20]
            ]
            ui.table(
                columns=[
                    {"name": "file", "label": "file", "field": "file", "align": "left"},
                    {"name": "folder", "label": "folder", "field": "folder", "align": "left"},
                ],
                rows=rows,
                row_key="file",
            ).props("flat bordered dense").classes("qaic-table")

    def _responses_page() -> None:
        with _shell("responses"):
            _render_global_visual_banner("responses")
            ui.label("GEM Response Inbox").classes("qaic-section-title")
            ui.label("P184 Response Parser").classes("qaic-section-title")
            ui.label(
                "Parser local review-only des réponses GEM sauvegardées. "
                "Aucun appel GEM, aucune écriture Sheets, aucun apply."
            ).classes("qaic-muted")
            ui.badge("LOCAL PARSER ONLY", color="green")
            ui.badge("AUTO APPLY BLOCKED", color="red")
            ui.label(
                "Coller ici la réponse GEM après interrogation manuelle. Sauvegarde locale review-only."
            ).classes("qaic-muted")
            response_box = (
                ui.textarea(placeholder="Coller réponse GEM ici...")
                .props("outlined autogrow")
                .classes("w-full qaic-prompt-box")
            )
            ui.button(
                "Sauver réponse GEM localement",
                icon="save",
                on_click=lambda: ui.notify(
                    f"Sauvegarde locale: {_save_text_file('GEM_RESPONSE', response_box.value or '', response_dir)}",
                    color="positive",
                ),
            ).props("color=primary")
            ui.separator()
            ui.table(
                columns=_session_columns(),
                rows=[row for row in _sessions_rows() if row["type"] == "gem_response"],
                row_key="file",
            ).props("flat bordered dense").classes("qaic-table")

    def _sessions_page() -> None:
        with _shell("sessions"):
            _render_global_visual_banner("sessions")
            ui.label("Sessions / interrogations").classes("qaic-section-title")
            ui.label(
                "Suivi local des captures et réponses GEM. Liaison capture ↔ prompt ↔ réponse à renforcer ensuite."
            ).classes("qaic-muted")
            ui.table(columns=_session_columns(), rows=_sessions_rows(), row_key="file").props(
                "flat bordered dense"
            ).classes("qaic-table")

            ui.separator()
            ui.label("P183 Session Workflow").classes("qaic-section-title")
            ui.label(
                "Chaînage local: capture portfolio → prompt actif → réponse GEM → session review-only."
            ).classes("qaic-muted")
            ui.button(
                "Créer session review-only depuis les derniers fichiers",
                icon="link",
                on_click=lambda: ui.notify(
                    "Session workflow P183: index local via module p183, aucun appel GEM, aucun apply.",
                    color="positive",
                ),
            ).props("color=primary")
            ui.label(f"Session log local: {session_dir}").classes("qaic-muted")

    def _review_page() -> None:
        with _shell("review"):
            _render_global_visual_banner("review")
            ui.label("Review humaine").classes("qaic-section-title")
            ui.badge("APPLY BLOCKED", color="red")
            ui.label("Prévisualisation uniquement. Aucune écriture live.").classes("qaic-muted")
            _panel_table(panel_by_slot.get("human_review_workbench_panel"))

    def _cache_page() -> None:
        with _shell("cache"):
            _render_global_visual_banner("cache")
            ui.label("Cache local").classes("qaic-section-title")
            for panel in panels:
                _panel_table(panel)

    def _journal_page() -> None:
        with _shell("journal"):
            _render_global_visual_banner("journal")
            ui.label("Journal").classes("qaic-section-title")
            _panel_table(panel_by_slot.get("decision_history_panel"))

    def _lexique_page() -> None:
        with _shell("lexique"):
            _render_global_visual_banner("lexique")
            ui.label("Lexique / contexte").classes("qaic-section-title")
            _panel_table(panel_by_slot.get("lexique_context_panel"))

    def _roundtrip_page() -> None:
        with _shell("roundtrip"):
            _render_global_visual_banner("roundtrip")
            ui.label("P185 Roundtrip Workbench").classes("qaic-section-title")
            ui.label(
                "Flux opérateur réel: capture portfolio → prompt actif → réponse GEM "
                "collée localement → parser P184 → session review-only."
            ).classes("qaic-muted")
            with ui.row().classes("gap-3"):
                ui.badge("LOCAL ONLY", color="green")
                ui.badge("NO GEM CALL", color="orange")
                ui.badge("AUTO APPLY BLOCKED", color="red")
                ui.badge("NO BROKER / NO ORDER / NO SIZING", color="red")
            with ui.row().classes("gap-3"):
                ui.button("1. Capture", icon="image", on_click=lambda: ui.navigate.to("/capture"))
                ui.button("2. Prompt", icon="article", on_click=lambda: ui.navigate.to("/prompt"))
                ui.button(
                    "3. Réponse GEM",
                    icon="data_object",
                    on_click=lambda: ui.navigate.to("/responses"),
                )
                ui.button(
                    "4. Sessions", icon="history", on_click=lambda: ui.navigate.to("/sessions")
                )
                ui.button(
                    "5. Review", icon="fact_check", on_click=lambda: ui.navigate.to("/review")
                )
            ui.separator()
            ui.label("Checklist opérateur").classes("qaic-section-title")
            ui.markdown(
                "- Upload ou colle une capture portfolio dans Capture Inbox.\n"
                "- Copie le prompt actif depuis Prompt Studio.\n"
                "- Interroge GEM manuellement hors Python.\n"
                "- Colle la réponse GEM dans GEM Response Inbox.\n"
                "- Le parser P184 contrôle JSON, sécurité, missing_data et blockers.\n"
                "- La décision finale reste humaine; aucun apply automatique."
            )
            ui.separator()
            ui.label("Statut sécurité").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "gate", "label": "gate", "field": "gate", "align": "left"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                ],
                rows=[
                    {"gate": "PUBLIC_SERVE", "status": "False"},
                    {"gate": "GEM_CALL_EXECUTED", "status": "False"},
                    {"gate": "AUTO_APPLY_GEM_RESPONSE", "status": "False"},
                    {"gate": "GOOGLE_SHEETS_WRITE", "status": "False"},
                    {"gate": "BROKER / ORDER / SIZING", "status": "False"},
                ],
                row_key="gate",
            ).props("flat bordered dense").classes("qaic-table")

    @ui.page("/roundtrip")
    def roundtrip() -> None:
        _roundtrip_page()

    def _real_case_page() -> None:
        with _shell("real-case"):
            _render_global_visual_banner("real-case")
            ui.label("P188 Real Case Decision Gate").classes("qaic-section-title")
            ui.label(
                "Gate opérateur réel: déposer une vraie capture portfolio et coller une vraie réponse GEM. "
                "Tant qu'un input manque, la décision reste WAIT."
            ).classes("qaic-muted")
            with ui.row().classes("gap-3"):
                ui.badge("HUMAN REVIEW REQUIRED", color="orange")
                ui.badge("AUTO APPLY BLOCKED", color="red")
                ui.badge("NO BROKER / NO ORDER / NO SIZING", color="red")
            ui.separator()
            ui.label("À déposer").classes("qaic-section-title")
            ui.markdown(
                "- Capture réelle: `00_OPERATOR_EXPORTS/P181_CAPTURE_INBOX/`\n"
                "- Réponse GEM réelle: `00_OPERATOR_EXPORTS/P181_GEM_RESPONSES/`\n"
                "- Fichiers `P186_SMOKE_*` ignorés automatiquement.\n"
                "- La décision finale reste humaine."
            )
            ui.separator()
            ui.label("Actions rapides").classes("qaic-section-title")
            with ui.row().classes("gap-3"):
                ui.button(
                    "Capture Inbox", icon="image", on_click=lambda: ui.navigate.to("/capture")
                )
                ui.button(
                    "GEM Responses",
                    icon="data_object",
                    on_click=lambda: ui.navigate.to("/responses"),
                )
                ui.button(
                    "Roundtrip", icon="sync_alt", on_click=lambda: ui.navigate.to("/roundtrip")
                )
                ui.button("Review", icon="fact_check", on_click=lambda: ui.navigate.to("/review"))

    @ui.page("/real-case")
    def real_case() -> None:
        _real_case_page()

    def _migration_page() -> None:
        from mvp_qaic_py.p190r_runtime_migration_tracker_live_readonly import (
            build_runtime_migration_tracker,
        )

        payload = build_runtime_migration_tracker(project_root)
        with _shell("migration"):
            _render_global_visual_banner("migration")
            ui.label("P190R Runtime Migration Tracker").classes("qaic-section-title")
            ui.label(
                "Vision runtime read-only: onglets de suivi GEM, scripts, fonctions, "
                "modules Python, tests, routes NiceGUI, prompts, exports, tags et % migration."
            ).classes("qaic-muted")

            with ui.row().classes("gap-3"):
                ui.badge(f"migration={payload['migration_percent']}%", color="blue")
                ui.badge(f"artifacts={payload['artifact_count']}", color="green")
                ui.badge(f"blockers={payload['blocker_count']}", color="red")
                ui.badge("READ ONLY", color="orange")

            ui.separator()
            ui.label("Coverage").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "area", "label": "area", "field": "area", "align": "left"},
                    {"name": "count", "label": "count", "field": "count", "align": "right"},
                    {"name": "percent", "label": "%", "field": "percent", "align": "right"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                ],
                rows=payload["coverage_rows"],
                row_key="area",
            ).props("flat bordered dense").classes("qaic-table")

            ui.separator()
            ui.label("GEM tracking tabs layer").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "name", "label": "onglet / layer", "field": "name", "align": "left"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                    {
                        "name": "migration_percent",
                        "label": "%",
                        "field": "migration_percent",
                        "align": "right",
                    },
                    {
                        "name": "next_action",
                        "label": "next_action",
                        "field": "next_action",
                        "align": "left",
                    },
                ],
                rows=payload["gem_tracking_rows"],
                row_key="name",
            ).props("flat bordered dense").classes("qaic-table")

            ui.separator()
            ui.label("Runtime artifacts").classes("qaic-section-title")
            ui.table(
                columns=[
                    {
                        "name": "artifact_type",
                        "label": "type",
                        "field": "artifact_type",
                        "align": "left",
                    },
                    {"name": "name", "label": "name", "field": "name", "align": "left"},
                    {
                        "name": "migration_status",
                        "label": "status",
                        "field": "migration_status",
                        "align": "left",
                    },
                    {
                        "name": "migration_percent",
                        "label": "%",
                        "field": "migration_percent",
                        "align": "right",
                    },
                    {
                        "name": "next_action",
                        "label": "next_action",
                        "field": "next_action",
                        "align": "left",
                    },
                ],
                rows=payload["artifacts"][:250],
                row_key="artifact_id",
            ).props("flat bordered dense").classes("qaic-table")

    @ui.page("/migration")
    def migration() -> None:
        _migration_page()

    def _gem_tracking_page() -> None:
        from mvp_qaic_py.p191r_gem_tracking_tabs_runtime_binding_matrix import (
            build_gem_tracking_tabs_runtime_binding_matrix,
        )

        payload = build_gem_tracking_tabs_runtime_binding_matrix(project_root)
        with _shell("gem-tracking"):
            _render_global_visual_banner("gem-tracking")
            ui.label("P191R GEM Tracking Tabs Runtime Binding Matrix").classes("qaic-section-title")
            ui.label(
                "Couche de suivi GEM: onglets/layers attendus, sources locales, "
                "routes NiceGUI, handlers Python, exports, statut runtime et actions suivantes."
            ).classes("qaic-muted")

            with ui.row().classes("gap-3"):
                ui.badge(f"layers={payload['layer_count']}", color="blue")
                ui.badge(f"ready={payload['ready_layer_count']}", color="green")
                ui.badge(f"coverage={payload['binding_coverage_percent']}%", color="purple")
                ui.badge(f"blockers={payload['blocker_count']}", color="red")
                ui.badge("READ ONLY", color="orange")

            ui.separator()
            ui.label("GEM tracking layers").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "layer_id", "label": "layer_id", "field": "layer_id", "align": "left"},
                    {
                        "name": "expected_sheet_tab",
                        "label": "expected sheet tab",
                        "field": "expected_sheet_tab",
                        "align": "left",
                    },
                    {
                        "name": "runtime_status",
                        "label": "runtime_status",
                        "field": "runtime_status",
                        "align": "left",
                    },
                    {
                        "name": "binding_percent",
                        "label": "%",
                        "field": "binding_percent",
                        "align": "right",
                    },
                    {
                        "name": "nicegui_route",
                        "label": "route",
                        "field": "nicegui_route",
                        "align": "left",
                    },
                    {
                        "name": "next_action",
                        "label": "next_action",
                        "field": "next_action",
                        "align": "left",
                    },
                ],
                rows=payload["layers"],
                row_key="layer_id",
            ).props("flat bordered dense").classes("qaic-table")

            ui.separator()
            ui.label("Runtime coverage").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "metric", "label": "metric", "field": "metric", "align": "left"},
                    {"name": "value", "label": "value", "field": "value", "align": "right"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                ],
                rows=payload["coverage_rows"],
                row_key="metric",
            ).props("flat bordered dense").classes("qaic-table")

    @ui.page("/gem-tracking")
    def gem_tracking() -> None:
        _gem_tracking_page()

    def _gem_tracking_operator_page() -> None:
        from mvp_qaic_py.p192r_gem_tracking_tabs_csv_export_operator_view_polish import (
            build_gem_tracking_operator_view,
        )

        payload = build_gem_tracking_operator_view(project_root)
        with _shell("gem-tracking-operator"):
            _render_global_visual_banner("gem-tracking-operator")
            ui.label("P192R GEM Tracking Operator View").classes("qaic-section-title")
            ui.label(
                "Vue opérateur: priorités, statuts lisibles, actions suivantes, "
                "preuves runtime et exports CSV pour les onglets/couches GEM."
            ).classes("qaic-muted")

            with ui.row().classes("gap-3"):
                ui.badge(f"layers={payload['layer_count']}", color="blue")
                ui.badge(f"ready={payload['ready_count']}", color="green")
                ui.badge(f"review={payload['review_count']}", color="orange")
                ui.badge(f"coverage={payload['operator_coverage_percent']}%", color="purple")
                ui.badge("READ ONLY", color="orange")

            ui.separator()
            ui.label("Priorités opérateur").classes("qaic-section-title")
            ui.table(
                columns=[
                    {
                        "name": "priority",
                        "label": "priority",
                        "field": "priority",
                        "align": "right",
                    },
                    {"name": "layer_id", "label": "layer", "field": "layer_id", "align": "left"},
                    {
                        "name": "operator_status",
                        "label": "status",
                        "field": "operator_status",
                        "align": "left",
                    },
                    {
                        "name": "operator_action",
                        "label": "action",
                        "field": "operator_action",
                        "align": "left",
                    },
                    {
                        "name": "evidence_summary",
                        "label": "evidence",
                        "field": "evidence_summary",
                        "align": "left",
                    },
                ],
                rows=payload["operator_rows"],
                row_key="layer_id",
            ).props("flat bordered dense").classes("qaic-table")

            ui.separator()
            ui.label("Exports opérateur").classes("qaic-section-title")
            ui.table(
                columns=[
                    {
                        "name": "export_name",
                        "label": "export",
                        "field": "export_name",
                        "align": "left",
                    },
                    {"name": "purpose", "label": "purpose", "field": "purpose", "align": "left"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                ],
                rows=payload["export_rows"],
                row_key="export_name",
            ).props("flat bordered dense").classes("qaic-table")

    @ui.page("/gem-tracking-operator")
    def gem_tracking_operator() -> None:
        _gem_tracking_operator_page()

    def _gem_evidence_page() -> None:
        from mvp_qaic_py.p193r_gem_decision_journal_roundtrip_evidence_binding import (
            build_gem_evidence_binding,
        )

        payload = build_gem_evidence_binding(project_root)
        with _shell("gem-evidence"):
            _render_global_visual_banner("gem-evidence")
            ui.label("P193R GEM Evidence Binding").classes("qaic-section-title")
            ui.label(
                "Binding read-only des preuves runtime: roundtrip GEM et journal de décision. "
                "Aucune écriture Sheets, aucun appel GEM, aucun broker."
            ).classes("qaic-muted")

            with ui.row().classes("gap-3"):
                ui.badge(f"roundtrip={payload['roundtrip_evidence_count']}", color="blue")
                ui.badge(f"journal={payload['decision_journal_evidence_count']}", color="green")
                ui.badge(f"coverage={payload['evidence_coverage_percent']}%", color="purple")
                ui.badge(f"blockers={payload['blocker_count']}", color="red")
                ui.badge("READ ONLY", color="orange")

            ui.separator()
            ui.label("Evidence binding").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "layer_id", "label": "layer", "field": "layer_id", "align": "left"},
                    {
                        "name": "evidence_status",
                        "label": "status",
                        "field": "evidence_status",
                        "align": "left",
                    },
                    {
                        "name": "evidence_count",
                        "label": "count",
                        "field": "evidence_count",
                        "align": "right",
                    },
                    {
                        "name": "evidence_percent",
                        "label": "%",
                        "field": "evidence_percent",
                        "align": "right",
                    },
                    {
                        "name": "latest_evidence",
                        "label": "latest",
                        "field": "latest_evidence",
                        "align": "left",
                    },
                    {
                        "name": "next_action",
                        "label": "next_action",
                        "field": "next_action",
                        "align": "left",
                    },
                ],
                rows=payload["binding_rows"],
                row_key="layer_id",
            ).props("flat bordered dense").classes("qaic-table")

            ui.separator()
            ui.label("Preuves récentes").classes("qaic-section-title")
            ui.table(
                columns=[
                    {
                        "name": "evidence_type",
                        "label": "type",
                        "field": "evidence_type",
                        "align": "left",
                    },
                    {"name": "name", "label": "name", "field": "name", "align": "left"},
                    {
                        "name": "source_path",
                        "label": "source_path",
                        "field": "source_path",
                        "align": "left",
                    },
                ],
                rows=payload["evidence_rows"][:150],
                row_key="evidence_id",
            ).props("flat bordered dense").classes("qaic-table")

    @ui.page("/gem-evidence")
    def gem_evidence() -> None:
        _gem_evidence_page()

    def _runtime_contract_page() -> None:
        from mvp_qaic_py.p194r_gem_runtime_tracker_close_sheets_export_contract import (
            build_gem_runtime_close_contract,
        )

        payload = build_gem_runtime_close_contract(project_root)
        with _shell("runtime-contract"):
            _render_global_visual_banner("runtime-contract")
            ui.label("P194R GEM Runtime Contract").classes("qaic-section-title")
            ui.label(
                "Clôture runtime GEM + contrat d'export Sheets futur. "
                "Lecture seule: aucune écriture Sheets, aucun Apps Script, aucun CLASP."
            ).classes("qaic-muted")

            with ui.row().classes("gap-3"):
                ui.badge(f"tabs={payload['sheet_contract_row_count']}", color="blue")
                ui.badge(f"ready={payload['ready_for_sheets_export_count']}", color="green")
                ui.badge(f"coverage={payload['runtime_close_percent']}%", color="purple")
                ui.badge(f"blockers={payload['blocker_count']}", color="red")
                ui.badge("READ ONLY", color="orange")

            ui.separator()
            ui.label("Contrat onglets Sheets futur").classes("qaic-section-title")
            ui.table(
                columns=[
                    {
                        "name": "sheet_tab",
                        "label": "sheet_tab",
                        "field": "sheet_tab",
                        "align": "left",
                    },
                    {
                        "name": "runtime_layer",
                        "label": "runtime_layer",
                        "field": "runtime_layer",
                        "align": "left",
                    },
                    {
                        "name": "export_status",
                        "label": "export_status",
                        "field": "export_status",
                        "align": "left",
                    },
                    {
                        "name": "readiness_percent",
                        "label": "%",
                        "field": "readiness_percent",
                        "align": "right",
                    },
                    {
                        "name": "write_policy",
                        "label": "write_policy",
                        "field": "write_policy",
                        "align": "left",
                    },
                    {
                        "name": "next_action",
                        "label": "next_action",
                        "field": "next_action",
                        "align": "left",
                    },
                ],
                rows=payload["sheet_contract_rows"],
                row_key="sheet_tab",
            ).props("flat bordered dense").classes("qaic-table")

            ui.separator()
            ui.label("Clôture runtime").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "metric", "label": "metric", "field": "metric", "align": "left"},
                    {"name": "value", "label": "value", "field": "value", "align": "right"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                ],
                rows=payload["close_rows"],
                row_key="metric",
            ).props("flat bordered dense").classes("qaic-table")

    @ui.page("/runtime-contract")
    def runtime_contract() -> None:
        _runtime_contract_page()

    def _operator_release_page() -> None:
        from mvp_qaic_py.p195r_operator_release_runtime_tracker_next_selector_maxi import (
            build_operator_release_runtime_tracker,
        )

        payload = build_operator_release_runtime_tracker(project_root)
        with _shell("operator-release"):
            _render_global_visual_banner("operator-release")
            ui.label("P195R Operator Release Runtime Tracker").classes("qaic-section-title")
            ui.label(
                "Clôture opérateur runtime GEM + sélecteur de prochain chantier MAXI. "
                "Read-only: aucune écriture Sheets, aucun Apps Script, aucun GEM call."
            ).classes("qaic-muted")

            with ui.row().classes("gap-3"):
                ui.badge(payload["operator_release_status"], color="green")
                ui.badge(f"runtime={payload['runtime_close_percent']}%", color="blue")
                ui.badge(f"routes={payload['expected_route_count']}", color="purple")
                ui.badge(f"waivers={payload['review_waiver_count']}", color="orange")
                ui.badge("READ ONLY", color="orange")

            ui.separator()
            ui.label("Release gates").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "gate", "label": "gate", "field": "gate", "align": "left"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                    {"name": "value", "label": "value", "field": "value", "align": "left"},
                    {"name": "reason", "label": "reason", "field": "reason", "align": "left"},
                ],
                rows=payload["release_gate_rows"],
                row_key="gate",
            ).props("flat bordered dense").classes("qaic-table")

            ui.separator()
            ui.label("Next work selector MAXI").classes("qaic-section-title")
            ui.table(
                columns=[
                    {
                        "name": "priority",
                        "label": "priority",
                        "field": "priority",
                        "align": "right",
                    },
                    {
                        "name": "workstream",
                        "label": "workstream",
                        "field": "workstream",
                        "align": "left",
                    },
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                    {
                        "name": "next_pack",
                        "label": "next_pack",
                        "field": "next_pack",
                        "align": "left",
                    },
                    {"name": "reason", "label": "reason", "field": "reason", "align": "left"},
                ],
                rows=payload["next_work_rows"],
                row_key="workstream",
            ).props("flat bordered dense").classes("qaic-table")

    @ui.page("/operator-release")
    def operator_release() -> None:
        _operator_release_page()

    def _real_case_inputs_page() -> None:
        from mvp_qaic_py.p196_real_case_portfolio_gem_operator_inputs_maxi import (
            build_real_case_portfolio_gem_inputs,
        )

        payload = build_real_case_portfolio_gem_inputs(project_root)
        with _shell("real-case-inputs"):
            _render_global_visual_banner("real-case-inputs")
            ui.label("P196 Real Case Portfolio GEM Inputs").classes("qaic-section-title")
            ui.label(
                "Pack opérateur pour vrai cas portfolio: capture écran, texte copié, "
                "réponse GEM collée, preuves locales et prochain statut review."
            ).classes("qaic-muted")

            with ui.row().classes("gap-3"):
                ui.badge(payload["input_status"], color="blue")
                ui.badge(f"captures={payload['capture_count']}", color="green")
                ui.badge(f"responses={payload['response_count']}", color="purple")
                ui.badge(f"ready={payload['ready_for_review']}", color="orange")
                ui.badge("NO GEM CALL", color="red")

            ui.separator()
            ui.label("Contrat d'inputs opérateur").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "input_id", "label": "input_id", "field": "input_id", "align": "left"},
                    {"name": "required", "label": "required", "field": "required", "align": "left"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                    {
                        "name": "local_path",
                        "label": "local_path",
                        "field": "local_path",
                        "align": "left",
                    },
                    {
                        "name": "operator_action",
                        "label": "operator_action",
                        "field": "operator_action",
                        "align": "left",
                    },
                ],
                rows=payload["input_contract_rows"],
                row_key="input_id",
            ).props("flat bordered dense").classes("qaic-table")

            ui.separator()
            ui.label("Étapes opérateur").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "step", "label": "step", "field": "step", "align": "right"},
                    {"name": "action", "label": "action", "field": "action", "align": "left"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                ],
                rows=payload["operator_steps"],
                row_key="step",
            ).props("flat bordered dense").classes("qaic-table")

    @ui.page("/real-case-inputs")
    def real_case_inputs() -> None:
        _real_case_inputs_page()

    def _prompt_master_page() -> None:
        from mvp_qaic_py.p197_prompt_master_from_historical_audit_and_regression_maxi import (
            build_prompt_master_historical_regression,
        )

        payload = build_prompt_master_historical_regression(project_root)
        selected = payload["selected_master_candidate"]

        with _shell("prompt-master"):
            _render_global_visual_banner("prompt-master")
            ui.label("P197 Prompt Master Historical Regression").classes("qaic-section-title")
            ui.label(
                "Fusion review-only: prompt actif, historiques, audit, candidat master, "
                "checklist de régression. Aucune modification du prompt source."
            ).classes("qaic-muted")

            with ui.row().classes("gap-3"):
                ui.badge(payload["master_status"], color="blue")
                ui.badge(f"candidates={payload['candidate_count']}", color="green")
                ui.badge(f"regression={payload['regression_check_count']}", color="purple")
                ui.badge(f"score={selected.get('score', 0)}", color="orange")
                ui.badge("NO SOURCE PATCH", color="red")

            ui.separator()
            ui.label("Master candidate").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "field", "label": "field", "field": "field", "align": "left"},
                    {"name": "value", "label": "value", "field": "value", "align": "left"},
                ],
                rows=[
                    {"field": "candidate_id", "value": selected.get("candidate_id", "")},
                    {"field": "source_path", "value": selected.get("source_path", "")},
                    {"field": "classification", "value": selected.get("classification", "")},
                    {"field": "score", "value": selected.get("score", 0)},
                    {"field": "decision", "value": selected.get("decision", "")},
                ],
                row_key="field",
            ).props("flat bordered dense").classes("qaic-table")

            ui.separator()
            ui.label("Regression checklist").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "check_id", "label": "check", "field": "check_id", "align": "left"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                    {"name": "severity", "label": "severity", "field": "severity", "align": "left"},
                    {"name": "rule", "label": "rule", "field": "rule", "align": "left"},
                ],
                rows=payload["regression_checks"],
                row_key="check_id",
            ).props("flat bordered dense").classes("qaic-table")

            ui.separator()
            ui.label("Prompt candidates").classes("qaic-section-title")
            ui.table(
                columns=[
                    {
                        "name": "candidate_id",
                        "label": "candidate",
                        "field": "candidate_id",
                        "align": "left",
                    },
                    {
                        "name": "classification",
                        "label": "classification",
                        "field": "classification",
                        "align": "left",
                    },
                    {"name": "score", "label": "score", "field": "score", "align": "right"},
                    {"name": "decision", "label": "decision", "field": "decision", "align": "left"},
                    {
                        "name": "source_path",
                        "label": "source",
                        "field": "source_path",
                        "align": "left",
                    },
                ],
                rows=payload["candidates"][:100],
                row_key="candidate_id",
            ).props("flat bordered dense").classes("qaic-table")

    @ui.page("/prompt-master")
    def prompt_master() -> None:
        _prompt_master_page()

    def _sheets_export_page() -> None:
        from mvp_qaic_py.p198_sheets_export_dry_run_contract_pack_maxi import (
            build_sheets_export_dry_run_contract_pack,
        )

        payload = build_sheets_export_dry_run_contract_pack(project_root)

        with _shell("sheets-export"):
            _render_global_visual_banner("sheets-export")
            ui.label("P198 Sheets Export Dry Run Contract Pack").classes("qaic-section-title")
            ui.label(
                "Vue dry-run avant toute écriture Sheets: onglets cibles, sources Python, colonnes, "
                "statuts, risques et ordre d'export. Aucune écriture Google Sheets."
            ).classes("qaic-muted")

            with ui.row().classes("gap-3"):
                ui.badge(payload["dry_run_status"], color="blue")
                ui.badge(f"tabs={payload['target_tab_count']}", color="green")
                ui.badge(f"ready={payload['ready_tab_count']}", color="purple")
                ui.badge(f"coverage={payload['dry_run_coverage_percent']}%", color="orange")
                ui.badge("NO SHEET WRITE", color="red")

            ui.separator()
            ui.label("Target tabs dry-run").classes("qaic-section-title")
            ui.table(
                columns=[
                    {
                        "name": "priority",
                        "label": "priority",
                        "field": "priority",
                        "align": "right",
                    },
                    {
                        "name": "sheet_tab",
                        "label": "sheet_tab",
                        "field": "sheet_tab",
                        "align": "left",
                    },
                    {
                        "name": "runtime_layer",
                        "label": "runtime_layer",
                        "field": "runtime_layer",
                        "align": "left",
                    },
                    {
                        "name": "dry_run_status",
                        "label": "status",
                        "field": "dry_run_status",
                        "align": "left",
                    },
                    {
                        "name": "estimated_rows",
                        "label": "rows",
                        "field": "estimated_rows",
                        "align": "right",
                    },
                    {
                        "name": "write_policy",
                        "label": "write_policy",
                        "field": "write_policy",
                        "align": "left",
                    },
                    {
                        "name": "next_action",
                        "label": "next_action",
                        "field": "next_action",
                        "align": "left",
                    },
                ],
                rows=payload["target_tab_rows"],
                row_key="sheet_tab",
            ).props("flat bordered dense").classes("qaic-table")

            ui.separator()
            ui.label("Export gates").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "gate", "label": "gate", "field": "gate", "align": "left"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                    {"name": "value", "label": "value", "field": "value", "align": "left"},
                    {"name": "reason", "label": "reason", "field": "reason", "align": "left"},
                ],
                rows=payload["gate_rows"],
                row_key="gate",
            ).props("flat bordered dense").classes("qaic-table")

            ui.separator()
            ui.label("Planning visuel").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "step", "label": "step", "field": "step", "align": "right"},
                    {"name": "lane", "label": "lane", "field": "lane", "align": "left"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                    {
                        "name": "next_pack",
                        "label": "next_pack",
                        "field": "next_pack",
                        "align": "left",
                    },
                ],
                rows=payload["visual_planning_rows"],
                row_key="step",
            ).props("flat bordered dense").classes("qaic-table")

    @ui.page("/sheets-export")
    def sheets_export() -> None:
        _sheets_export_page()

    def _apps_script_map_page() -> None:
        from mvp_qaic_py.p199_apps_script_sheets_function_tab_migration_map_maxi import (
            build_apps_script_sheets_function_tab_migration_map,
        )

        payload = build_apps_script_sheets_function_tab_migration_map(project_root)

        with _shell("apps-script-map"):
            _render_global_visual_banner("apps-script-map")
            ui.label("P199 Apps Script Migration Map").classes("qaic-section-title")
            ui.label(
                "Mapping visuel read-only: onglets Sheets, sources Apps Script, modules Python, "
                "routes NiceGUI, exports et statut de migration. Aucun CLASP, aucun Apps Script run."
            ).classes("qaic-muted")

            with ui.row().classes("gap-3"):
                ui.badge(payload["migration_map_status"], color="blue")
                ui.badge(f"tabs={payload['sheet_tab_count']}", color="green")
                ui.badge(f"python={payload['python_module_count']}", color="purple")
                ui.badge(f"apps_script={payload['apps_script_source_count']}", color="orange")
                ui.badge(f"coverage={payload['migration_map_coverage_percent']}%", color="teal")
                ui.badge("READ ONLY", color="red")

            ui.separator()
            ui.label("Migration matrix").classes("qaic-section-title")
            ui.table(
                columns=[
                    {
                        "name": "priority",
                        "label": "priority",
                        "field": "priority",
                        "align": "right",
                    },
                    {
                        "name": "sheet_tab",
                        "label": "sheet_tab",
                        "field": "sheet_tab",
                        "align": "left",
                    },
                    {
                        "name": "runtime_layer",
                        "label": "runtime_layer",
                        "field": "runtime_layer",
                        "align": "left",
                    },
                    {
                        "name": "python_binding",
                        "label": "python_binding",
                        "field": "python_binding",
                        "align": "left",
                    },
                    {
                        "name": "apps_script_binding",
                        "label": "apps_script_binding",
                        "field": "apps_script_binding",
                        "align": "left",
                    },
                    {
                        "name": "migration_status",
                        "label": "status",
                        "field": "migration_status",
                        "align": "left",
                    },
                    {
                        "name": "next_action",
                        "label": "next_action",
                        "field": "next_action",
                        "align": "left",
                    },
                ],
                rows=payload["migration_rows"],
                row_key="sheet_tab",
            ).props("flat bordered dense").classes("qaic-table")

            ui.separator()
            ui.label("Python modules").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "module", "label": "module", "field": "module", "align": "left"},
                    {
                        "name": "function_count",
                        "label": "functions",
                        "field": "function_count",
                        "align": "right",
                    },
                    {
                        "name": "migration_role",
                        "label": "role",
                        "field": "migration_role",
                        "align": "left",
                    },
                ],
                rows=payload["python_module_rows"][:120],
                row_key="module",
            ).props("flat bordered dense").classes("qaic-table")

            ui.separator()
            ui.label("Planning visuel").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "step", "label": "step", "field": "step", "align": "right"},
                    {"name": "lane", "label": "lane", "field": "lane", "align": "left"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                    {
                        "name": "next_pack",
                        "label": "next_pack",
                        "field": "next_pack",
                        "align": "left",
                    },
                ],
                rows=payload["visual_planning_rows"],
                row_key="step",
            ).props("flat bordered dense").classes("qaic-table")

    @ui.page("/apps-script-map")
    def apps_script_map() -> None:
        _apps_script_map_page()

    def _dev_roadmap_page() -> None:
        from mvp_qaic_py.p199ux_r4_visual_ux_polish_maxi import build_visual_ux_polish

        payload = build_visual_ux_polish(project_root)

        with _shell("dev-roadmap"):
            _render_global_visual_banner("dev-roadmap")
            ui.add_head_html("""
            <style id="p199ux-r4-polish">
              .qaic-hero-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap:10px; margin: 8px 0 12px 0; }
              .qaic-metric-card { border-radius: 14px; padding: 10px 12px; min-height: 84px; }
              .qaic-metric-value { font-size: 28px; font-weight: 800; line-height: 1; }
              .qaic-metric-label { font-size: 12px; opacity: .72; margin-top: 4px; }
              .qaic-compact-table .q-table td { padding: 4px 8px !important; font-size: 12px; white-space: nowrap; }
              .qaic-compact-table .q-table th { padding: 5px 8px !important; font-size: 11px; white-space: nowrap; font-weight: 700; }
              .qaic-compact-table { max-height: 460px; overflow:auto; }
              .qaic-top-section { margin-top: 4px; margin-bottom: 8px; }
            </style>
            """)

            ui.label("Dev Roadmap — planning visuel MVP QAIC").classes("qaic-section-title")
            ui.label(
                "Vue opérateur compacte: passé, en cours, attente, futur proche et post-Python. "
                "Les compteurs, couleurs et tables sont optimisés pour décider vite."
            ).classes("qaic-muted")

            with ui.element("div").classes("qaic-hero-grid"):
                for card in payload["metric_card_rows"]:
                    with ui.card().classes("qaic-metric-card"):
                        with ui.row().classes("items-center justify-between"):
                            ui.label(card["label"]).classes("qaic-metric-label")
                            ui.badge(str(card["color"]).upper(), color=card["color"])
                        ui.label(f"{card['value']}{card['unit']}").classes("qaic-metric-value")

            ui.separator()

            with ui.expansion(
                "Navigation rapide escamotable", icon="menu_open", value=False
            ).classes("w-full"):
                ui.label("Routes utiles").classes("qaic-muted")
                with ui.row().classes("gap-2"):
                    for route in payload["navigation_policy"]["routes"]:
                        ui.link(route, route).classes("q-pa-xs")

            ui.separator()

            ui.label("Planning visuel synthétique").classes("qaic-section-title qaic-top-section")
            ui.table(
                columns=[
                    {"name": "period", "label": "période", "field": "period", "align": "left"},
                    {
                        "name": "step_count",
                        "label": "étapes",
                        "field": "step_count",
                        "align": "right",
                    },
                    {
                        "name": "avg_progress_percent",
                        "label": "% moyen",
                        "field": "avg_progress_percent",
                        "align": "right",
                    },
                    {
                        "name": "main_status",
                        "label": "status",
                        "field": "main_status",
                        "align": "left",
                    },
                    {
                        "name": "main_route",
                        "label": "route",
                        "field": "main_route",
                        "align": "left",
                    },
                ],
                rows=payload["top_visual_planning_rows"],
                row_key="period",
            ).props("flat bordered dense separator=cell").classes("qaic-table qaic-compact-table")

            ui.separator()

            ui.label("Planning détaillé").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "order", "label": "#", "field": "order", "align": "right"},
                    {"name": "period", "label": "période", "field": "period", "align": "left"},
                    {"name": "lane", "label": "chantier", "field": "lane", "align": "left"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                    {
                        "name": "progress_percent",
                        "label": "%",
                        "field": "progress_percent",
                        "align": "right",
                    },
                    {
                        "name": "visible_route",
                        "label": "route",
                        "field": "visible_route",
                        "align": "left",
                    },
                    {
                        "name": "next_action",
                        "label": "next",
                        "field": "next_action",
                        "align": "left",
                    },
                ],
                rows=payload["roadmap_rows"],
                row_key="order",
            ).props("flat bordered dense separator=cell wrap-cells").classes(
                "qaic-table qaic-compact-table"
            )

            ui.separator()

            ui.label("Onglets NiceGUI — utilité réelle").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "route", "label": "route", "field": "route", "align": "left"},
                    {
                        "name": "label_fr",
                        "label": "nom métier",
                        "field": "label_fr",
                        "align": "left",
                    },
                    {"name": "purpose", "label": "utilité", "field": "purpose", "align": "left"},
                    {
                        "name": "data_rendered",
                        "label": "données",
                        "field": "data_rendered",
                        "align": "left",
                    },
                    {
                        "name": "operator_value",
                        "label": "valeur",
                        "field": "operator_value",
                        "align": "left",
                    },
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                ],
                rows=payload["nicegui_tab_rows"],
                row_key="route",
            ).props("flat bordered dense separator=cell wrap-cells").classes(
                "qaic-table qaic-compact-table"
            )

            ui.separator()

            ui.label("Prochaines décisions").classes("qaic-section-title")
            ui.table(
                columns=[
                    {"name": "priority", "label": "#", "field": "priority", "align": "right"},
                    {"name": "decision", "label": "décision", "field": "decision", "align": "left"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                    {
                        "name": "next_pack",
                        "label": "next pack",
                        "field": "next_pack",
                        "align": "left",
                    },
                ],
                rows=payload["decision_rows"],
                row_key="priority",
            ).props("flat bordered dense separator=cell wrap-cells").classes(
                "qaic-table qaic-compact-table"
            )

    @ui.page("/dev-roadmap")
    def dev_roadmap() -> None:
        _dev_roadmap_page()

    def _release_final_page() -> None:
        from mvp_qaic_py.p200r2_deep_cockpit_ux_instructions_tracker_maxi import (
            build_deep_operator_cockpit,
        )

        payload = build_deep_operator_cockpit(project_root)

        with _shell("release-final"):
            _render_global_visual_banner("release-final")
            ui.label("Release Final — cockpit opérateur réparé").classes("qaic-section-title")
            ui.label(
                "Synthèse finale fiable: release, sécurité, décisions, cas réel et live-write bloqué."
            ).classes("qaic-muted")

            with ui.row().classes("gap-3"):
                ui.badge(payload["release_status"], color="blue")
                ui.badge(f"migration={payload['migration_coverage_percent']}%", color="teal")
                ui.badge(f"instructions={payload['instruction_row_count']}", color="orange")
                ui.badge(f"rows={payload['migration_control_row_count']}", color="purple")
                ui.badge("NO LIVE WRITE", color="red")

            ui.separator()
            ui.table(
                columns=[
                    {"name": "color_cell", "label": "", "field": "color_cell", "align": "center"},
                    {"name": "area", "label": "zone", "field": "area", "align": "left"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                    {"name": "evidence", "label": "preuve", "field": "evidence", "align": "left"},
                    {
                        "name": "operator_action",
                        "label": "action",
                        "field": "operator_action",
                        "align": "left",
                    },
                ],
                rows=payload["release_rows"],
                row_key="priority",
            ).props("flat bordered dense separator=cell wrap-cells").classes(
                "qaic-table qaic-compact-table"
            )

    @ui.page("/release-final")
    def release_final() -> None:
        _release_final_page()

    def _render_global_visual_banner(active: str) -> None:
        """P200R2_GLOBAL_VISUAL_BANNER_MARKER: compact visual planning at top of key tabs."""
        if active not in {
            "dev-roadmap",
            "migration",
            "apps-script-map",
            "sheets-export",
            "release-final",
            "migration-control",
            "instructions",
            "operator-release",
        }:
            return
        try:
            from mvp_qaic_py.p200r2_deep_cockpit_ux_instructions_tracker_maxi import (
                build_global_visual_banner,
            )

            payload = build_global_visual_banner(project_root)
            with ui.expansion(
                "Planning visuel global / obligations", icon="dashboard", value=False
            ).classes("w-full"):
                with ui.row().classes("gap-2"):
                    for card in payload["metric_card_rows"]:
                        ui.badge(
                            f"{card['label']}: {card['value']}{card['unit']}", color=card["color"]
                        )
                ui.table(
                    columns=[
                        {
                            "name": "color_cell",
                            "label": "",
                            "field": "color_cell",
                            "align": "center",
                        },
                        {"name": "period", "label": "période", "field": "period", "align": "left"},
                        {
                            "name": "step_count",
                            "label": "étapes",
                            "field": "step_count",
                            "align": "right",
                        },
                        {
                            "name": "progress_percent",
                            "label": "%",
                            "field": "progress_percent",
                            "align": "right",
                        },
                        {"name": "status", "label": "status", "field": "status", "align": "left"},
                        {"name": "route", "label": "route", "field": "route", "align": "left"},
                    ],
                    rows=payload["global_planning_rows"],
                    row_key="period",
                ).props("flat bordered dense separator=cell").classes(
                    "qaic-table qaic-compact-table"
                )
        except Exception as exc:
            ui.badge(f"Planning global indisponible: {exc}", color="orange")

    def _migration_control_page() -> None:
        from mvp_qaic_py.p200r2_deep_cockpit_ux_instructions_tracker_maxi import (
            build_deep_operator_cockpit,
        )

        payload = build_deep_operator_cockpit(project_root)

        with _shell("migration-control"):
            _render_global_visual_banner("migration-control")
            ui.label("Migration Control — onglets / scripts / fonctions").classes(
                "qaic-section-title"
            )
            ui.label(
                "Table de contrôle colorée: ce qui est fait, ce qui reste à faire, et l'action opérateur."
            ).classes("qaic-muted")

            with ui.row().classes("gap-3"):
                ui.badge(f"rows={payload['migration_control_row_count']}", color="purple")
                ui.badge(f"tabs={payload['sheet_tab_count']}", color="green")
                ui.badge(f"coverage={payload['migration_coverage_percent']}%", color="teal")
                ui.badge("READ ONLY", color="red")

            ui.separator()
            ui.table(
                columns=[
                    {"name": "color_cell", "label": "", "field": "color_cell", "align": "center"},
                    {
                        "name": "entity_type",
                        "label": "type",
                        "field": "entity_type",
                        "align": "left",
                    },
                    {"name": "name", "label": "nom", "field": "name", "align": "left"},
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                    {
                        "name": "progress_percent",
                        "label": "%",
                        "field": "progress_percent",
                        "align": "right",
                    },
                    {"name": "done", "label": "fait", "field": "done", "align": "left"},
                    {"name": "todo", "label": "reste à faire", "field": "todo", "align": "left"},
                    {"name": "binding", "label": "binding", "field": "binding", "align": "left"},
                    {"name": "route", "label": "route", "field": "route", "align": "left"},
                ],
                rows=payload["migration_control_rows"],
                row_key="priority",
            ).props("flat bordered dense separator=cell wrap-cells").classes(
                "qaic-table qaic-compact-table"
            )

    @ui.page("/migration-control")
    def migration_control() -> None:
        _migration_control_page()

    def _instructions_page() -> None:
        from mvp_qaic_py.p200r2_deep_cockpit_ux_instructions_tracker_maxi import (
            build_deep_operator_cockpit,
        )

        payload = build_deep_operator_cockpit(project_root)

        with _shell("instructions"):
            _render_global_visual_banner("instructions")
            ui.label("Instructions Tracker — obligations par thème").classes("qaic-section-title")
            ui.label(
                "Suivi explicite des règles projet, sécurité, UX, migration, prompt/GEM et preuves."
            ).classes("qaic-muted")

            with ui.row().classes("gap-3"):
                ui.badge(f"obligations={payload['instruction_row_count']}", color="orange")
                ui.badge("HUMAN_REVIEW_ONLY", color="blue")
                ui.badge("NO LIVE WRITE", color="red")
                ui.badge("NO BROKER", color="purple")

            ui.separator()
            ui.table(
                columns=[
                    {"name": "color_cell", "label": "", "field": "color_cell", "align": "center"},
                    {"name": "theme", "label": "thème", "field": "theme", "align": "left"},
                    {
                        "name": "obligation",
                        "label": "obligation",
                        "field": "obligation",
                        "align": "left",
                    },
                    {"name": "status", "label": "status", "field": "status", "align": "left"},
                    {
                        "name": "progress_percent",
                        "label": "%",
                        "field": "progress_percent",
                        "align": "right",
                    },
                    {"name": "evidence", "label": "preuve", "field": "evidence", "align": "left"},
                    {
                        "name": "correction_rule",
                        "label": "règle correction",
                        "field": "correction_rule",
                        "align": "left",
                    },
                ],
                rows=payload["instruction_rows"],
                row_key="priority",
            ).props("flat bordered dense separator=cell wrap-cells").classes(
                "qaic-table qaic-compact-table"
            )

    @ui.page("/instructions")
    def instructions() -> None:
        _instructions_page()

    @ui.page("/")
    def home() -> None:
        _dashboard_page()

    @ui.page("/prompt")
    def prompt() -> None:
        _prompt_page()

    @ui.page("/capture")
    def capture() -> None:
        _capture_page()

    @ui.page("/responses")
    def responses() -> None:
        _responses_page()

    @ui.page("/sessions")
    def sessions() -> None:
        _sessions_page()

    @ui.page("/review")
    def review() -> None:
        _review_page()

    @ui.page("/cache")
    def cache() -> None:
        _cache_page()

    @ui.page("/journal")
    def journal() -> None:
        _journal_page()

    @ui.page("/lexique")
    def lexique() -> None:
        _lexique_page()

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
