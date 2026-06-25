from __future__ import annotations

from pathlib import Path
from typing import Any

from mvp_qaic_py.private_admin_app.navigation import get_admin_navigation
from mvp_qaic_py.private_admin_app.shell import (
    build_private_admin_shell_payload,
    build_route_page_payload,
    render_admin_route_content,
)


def _apply_style(ui: Any) -> None:
    ui.query(".nicegui-content").classes("p-0")
    ui.add_head_html(
        """
        <style>
          body { background:#f6f7fb; }
          .mvp-shell { min-height:100vh; }
          .mvp-main { padding:18px; }
          .mvp-card {
            background:white;
            border-radius:18px;
            padding:18px;
            box-shadow:0 2px 14px rgba(0,0,0,.06);
          }
          .mvp-title { font-size:22px; font-weight:800; color:#111827; }
          .mvp-subtitle { font-size:13px; color:#4b5563; }
          .mvp-table {
            width:100%;
            border-collapse:collapse;
            margin:12px 0 20px 0;
            font-size:13px;
          }
          .mvp-table th {
            text-align:left;
            background:#111827;
            color:white;
            padding:8px;
          }
          .mvp-table td {
            border-bottom:1px solid #e5e7eb;
            padding:7px 8px;
            vertical-align:top;
          }
          .mvp-badge {
            display:inline-block;
            padding:4px 8px;
            border-radius:999px;
            background:#ecfdf5;
            color:#065f46;
            font-size:12px;
            font-weight:700;
          }
        </style>
        """
    )


def render_private_admin_normal_preview(
    ui: Any, project_root: str | Path, *, active_route: str = "/"
) -> dict[str, Any]:
    payload = build_private_admin_shell_payload(project_root)
    route_payload = build_route_page_payload(project_root, active_route=active_route)
    navigation = get_admin_navigation()

    _apply_style(ui)

    with ui.row().classes("mvp-shell w-full no-wrap"):
        with ui.left_drawer(value=True).classes("bg-white").props("bordered width=285"):
            ui.label("MVP QAIC").classes("text-xl font-bold q-pa-md")
            ui.label("Private Admin").classes("text-xs text-gray-500 q-px-md q-pb-md")
            for item in navigation:
                active = item["route"] == active_route
                label = f"{'● ' if active else ''}{item['label']}"
                ui.link(label, item["route"]).classes("block q-px-md q-py-sm text-sm")
            ui.separator().classes("q-my-md")
            ui.label("Safety").classes("text-xs font-bold q-px-md")
            ui.label("NO BROKER / NO ORDER / NO SIZING").classes("text-xs text-gray-600 q-pa-md")

        with ui.column().classes("mvp-main w-full"):
            with ui.header().classes("bg-white text-black shadow-sm"):
                ui.label(route_payload["title"]).classes("text-lg font-bold")
                ui.space()
                ui.label("HUMAN_REVIEW_ONLY").classes("mvp-badge")
            render_admin_route_content(ui, route_payload, payload)

    return {
        "STATUS": "OK_P219D2_PRIVATE_ADMIN_NORMAL_PREVIEW_RENDERED",
        "active_route": active_route,
        "navigation_count": len(navigation),
        "server_started": False,
        "browser_started": False,
        "provider_call_executed": False,
        "gem_call_executed": False,
        "broker": False,
        "order": False,
        "sizing": False,
    }


def register_private_admin_pages(ui: Any, project_root: str | Path) -> None:
    navigation = get_admin_navigation()

    for item in navigation:
        route = item["route"]

        def page(route: str = route) -> None:
            render_private_admin_normal_preview(ui, project_root, active_route=route)

        ui.page(route)(page)


def run_private_admin_app(
    *,
    project_root: str | Path,
    host: str = "127.0.0.1",
    port: int = 8096,
    show: bool = False,
    reload: bool = False,
) -> None:
    from nicegui import ui

    register_private_admin_pages(ui, project_root)
    ui.run(
        host=host,
        port=port,
        title="MVP QAIC — Private Admin",
        show=show,
        reload=reload,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8096)
    args = parser.parse_args()

    run_private_admin_app(
        project_root=args.project_root,
        host=args.host,
        port=args.port,
        show=False,
        reload=False,
    )


if __name__ == "__main__":
    main()
