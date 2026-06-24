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
            ui.label("Review humaine").classes("qaic-section-title")
            ui.badge("APPLY BLOCKED", color="red")
            ui.label("Prévisualisation uniquement. Aucune écriture live.").classes("qaic-muted")
            _panel_table(panel_by_slot.get("human_review_workbench_panel"))

    def _cache_page() -> None:
        with _shell("cache"):
            ui.label("Cache local").classes("qaic-section-title")
            for panel in panels:
                _panel_table(panel)

    def _journal_page() -> None:
        with _shell("journal"):
            ui.label("Journal").classes("qaic-section-title")
            _panel_table(panel_by_slot.get("decision_history_panel"))

    def _lexique_page() -> None:
        with _shell("lexique"):
            ui.label("Lexique / contexte").classes("qaic-section-title")
            _panel_table(panel_by_slot.get("lexique_context_panel"))

    def _roundtrip_page() -> None:
        with _shell("roundtrip"):
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
