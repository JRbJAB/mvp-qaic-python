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
    project_root: str | Path, *, host: str = "127.0.0.1", port: int = 8088, show: bool = True
) -> None:
    if host != "127.0.0.1":
        raise ValueError("Only 127.0.0.1 is allowed for private local runner.")

    try:
        from nicegui import ui
    except Exception as exc:  # pragma: no cover - depends on operator environment
        raise RuntimeError("NiceGUI is not available in this environment.") from exc

    render_payload = build_private_cockpit_render_model(project_root)

    @ui.page("/")
    def home() -> None:
        ui.label("MVP QAIC — Private Local Cockpit").classes("text-h4")
        ui.label("Private local runner only: 127.0.0.1")
        ui.label(f"Status: {render_payload['STATUS']}")

    @ui.page("/cache")
    def cache() -> None:
        ui.label("Local cache panels").classes("text-h5")
        for panel in render_payload.get("render_panels", []):
            with ui.card().classes("w-full"):
                ui.label(str(panel["panel_title"])).classes("text-h6")
                ui.label(f"Source: {panel['source_id']} | Rows: {panel['row_count']}")
                ui.table(
                    columns=[
                        {"name": col, "label": col, "field": col} for col in panel["preview_header"]
                    ],
                    rows=panel["preview_rows"],
                )

    @ui.page("/review")
    def review() -> None:
        ui.label("Human review workbench").classes("text-h5")
        ui.label("Review-only. No write, no broker, no order, no sizing.")

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
