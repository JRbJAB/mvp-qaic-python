from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.p199ux_r2_dev_roadmap_tabs_ergonomics_maxi import (
    build_dev_roadmap_tabs_ergonomics,
)


ROUTES = [
    "/",
    "/prompt",
    "/capture",
    "/responses",
    "/sessions",
    "/roundtrip",
    "/real-case",
    "/migration",
    "/gem-tracking",
    "/gem-tracking-operator",
    "/gem-evidence",
    "/runtime-contract",
    "/operator-release",
    "/real-case-inputs",
    "/prompt-master",
    "/sheets-export",
    "/apps-script-map",
    "/dev-roadmap",
    "/review",
]

SAFETY_FLAGS: dict[str, bool] = {
    "gem_call_executed": False,
    "google_sheets_write": False,
    "live_google_api_call_from_python": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "public_serve": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
    "source_prompt_modified": False,
    "real_sheet_write_allowed": False,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _metric_cards(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "metric_id": "roadmap_steps",
            "label": "Étapes roadmap",
            "value": payload["roadmap_step_count"],
            "unit": "",
            "color": "blue",
            "priority": 1,
        },
        {
            "metric_id": "current_steps",
            "label": "En cours",
            "value": payload["current_step_count"],
            "unit": "",
            "color": "orange",
            "priority": 2,
        },
        {
            "metric_id": "post_python",
            "label": "Post-Python",
            "value": payload["post_python_step_count"],
            "unit": "",
            "color": "purple",
            "priority": 3,
        },
        {
            "metric_id": "nicegui_tabs",
            "label": "Onglets utiles",
            "value": payload["nicegui_tab_count"],
            "unit": "",
            "color": "green",
            "priority": 4,
        },
        {
            "metric_id": "migration_coverage",
            "label": "Coverage migration",
            "value": payload["migration_coverage_percent"],
            "unit": "%",
            "color": "teal",
            "priority": 5,
        },
        {
            "metric_id": "sheet_tabs",
            "label": "Onglets Sheets",
            "value": payload["sheet_tab_count"],
            "unit": "",
            "color": "indigo",
            "priority": 6,
        },
    ]


def _top_visual_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    order = ["PASSÉ", "EN COURS", "EN ATTENTE", "AVENIR PROCHE", "POST-PYTHON"]
    rows = []
    roadmap = payload["roadmap_rows"]
    for idx, period in enumerate(order, start=1):
        period_rows = [row for row in roadmap if row["period"] == period]
        avg = (
            round(
                sum(int(row["progress_percent"]) for row in period_rows) / len(period_rows),
                1,
            )
            if period_rows
            else 0
        )
        rows.append(
            {
                "order": idx,
                "period": period,
                "step_count": len(period_rows),
                "avg_progress_percent": avg,
                "main_status": _period_status(period),
                "main_route": period_rows[0]["visible_route"] if period_rows else "",
            }
        )
    return rows


def _period_status(period: str) -> str:
    if period == "PASSÉ":
        return "DONE"
    if period == "EN COURS":
        return "ACTIVE"
    if period == "EN ATTENTE":
        return "WAITING_INPUTS"
    if period == "AVENIR PROCHE":
        return "NEXT"
    return "FUTURE"


def build_visual_ux_polish(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    base = build_dev_roadmap_tabs_ergonomics(root)

    payload = {
        **base,
        "STATUS": "OK_P199UX_R4_VISUAL_UX_POLISH_READY",
        "generated_at": _utc_now(),
        "ux_status": "VISUAL_PLANNING_TOP_COMPACT_TABLES_COLLAPSIBLE_NAV_READY",
        "metric_card_rows": _metric_cards(base),
        "top_visual_planning_rows": _top_visual_rows(base),
        "compact_table_policy": {
            "density": "dense",
            "wrap_cells": False,
            "operator_first_columns": True,
            "horizontal_scroll": True,
            "max_visible_rows_before_scroll": 12,
        },
        "navigation_policy": {
            "mode": "collapsible_quick_navigation",
            "default_state": "collapsed",
            "wide_screen_goal": "give more horizontal room to data tables",
            "routes": [
                "/dev-roadmap",
                "/migration",
                "/apps-script-map",
                "/sheets-export",
                "/prompt-master",
                "/real-case-inputs",
                "/operator-release",
            ],
        },
        **SAFETY_FLAGS,
        "recommended_next": "P200_OPERATOR_RELEASE_COCKPIT_FINAL_MAXI",
    }
    return payload


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def export_visual_ux_polish(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P199UX_R4_VISUAL_UX_POLISH_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = build_visual_ux_polish(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P199UX_R4_VISUAL_UX_POLISH.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    _write_csv(
        export_path / "P199UX_R4_METRIC_CARDS.csv",
        payload["metric_card_rows"],
        ["priority", "metric_id", "label", "value", "unit", "color"],
    )

    _write_csv(
        export_path / "P199UX_R4_TOP_VISUAL_PLANNING.csv",
        payload["top_visual_planning_rows"],
        ["order", "period", "step_count", "avg_progress_percent", "main_status", "main_route"],
    )

    _write_csv(
        export_path / "P199UX_R4_VISUAL_ROADMAP.csv",
        payload["roadmap_rows"],
        ["order", "period", "lane", "status", "progress_percent", "visible_route", "next_action"],
    )

    _write_csv(
        export_path / "P199UX_R4_NICEGUI_TABS_USABILITY.csv",
        payload["nicegui_tab_rows"],
        ["route", "label_fr", "purpose", "data_rendered", "operator_value", "status"],
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "ux_status",
        "roadmap_status",
        "roadmap_step_count",
        "done_step_count",
        "current_step_count",
        "post_python_step_count",
        "nicegui_tab_count",
        "sheet_tab_count",
        "ready_mapping_count",
        "migration_coverage_percent",
        "blocker_count",
        "blockers",
        "gem_call_executed",
        "google_sheets_write",
        "live_google_api_call_from_python",
        "apps_script_execution",
        "clasp_push",
        "public_serve",
        "broker",
        "order",
        "sizing",
        "auto_apply_gem_response",
        "source_prompt_modified",
        "real_sheet_write_allowed",
        "recommended_next",
        "parallel_waiting_next",
    ]
    summary = {key: payload.get(key) for key in summary_keys}
    (export_path / "P199UX_R4_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = [
        "# P199UX-R4 Visual UX Polish MAXI",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- ux_status: {payload['ux_status']}",
        f"- roadmap_step_count: {payload['roadmap_step_count']}",
        f"- nicegui_tab_count: {payload['nicegui_tab_count']}",
        f"- migration_coverage_percent: {payload['migration_coverage_percent']}",
        "",
        "## Corrections UX",
        "- Planning visuel en haut",
        "- Couleurs et compteurs plus visibles",
        "- Tables compactes",
        "- Navigation rapide escamotable",
        "- Données utiles par onglet",
        "",
        "## Safety",
        "- GOOGLE_SHEETS_WRITE=False",
        "- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False",
        "- APPS_SCRIPT_EXECUTION=False",
        "- CLASP_PUSH=False",
        "- GEM_CALL_EXECUTED=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
        "",
        "## Next",
        f"- {payload['recommended_next']}",
    ]
    (export_path / "P199UX_R4_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    return payload


def _http_ok(url: str) -> bool:
    request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P199UX-R4"})
    for timeout in (12.0, 24.0, 36.0):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return 200 <= int(response.status) < 500
        except Exception:
            time.sleep(0.75)
    return False


def run_visual_ux_polish_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8109,
    timeout_seconds: int = 150,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_visual_ux_polish(root)

    command = [
        sys.executable,
        "-m",
        "mvp_qaic_py.p173_nicegui_private_local_runner",
        "--project-root",
        str(root),
        "--host",
        host,
        "--port",
        str(port),
        "--serve-private",
        "--no-show",
    ]

    process = subprocess.Popen(
        command,
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    route_results: list[dict[str, Any]] = []
    route_smoke_ok = False
    server_stopped = False
    start = time.time()

    try:
        while time.time() - start < timeout_seconds:
            if process.poll() is not None:
                break
            route_results = [
                {
                    "route": route,
                    "url": f"http://{host}:{port}{route}",
                    "ok": _http_ok(f"http://{host}:{port}{route}"),
                }
                for route in ROUTES
            ]
            if all(row["ok"] for row in route_results):
                route_smoke_ok = True
                break
            time.sleep(1.5)
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
                server_stopped = True
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)
                server_stopped = True
        else:
            server_stopped = True

    return {
        **payload,
        "STATUS": "OK_P199UX_R4_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P199UX_R4_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_visual_ux_polish_with_smoke(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    payload = export_visual_ux_polish(project_root, export_dir=export_dir)
    if run_route_smoke:
        smoke = run_visual_ux_polish_route_smoke(project_root)
        payload.update(
            {
                "STATUS": smoke["STATUS"],
                "route_results": smoke["route_results"],
                "route_success_count": smoke["route_success_count"],
                "route_smoke_ok": smoke["route_smoke_ok"],
                "server_started_by_smoke": smoke["server_started_by_smoke"],
                "server_stopped_after_smoke": smoke["server_stopped_after_smoke"],
            }
        )
        export_path = Path(payload["export_dir"])
        summary = {
            key: payload.get(key)
            for key in [
                "STATUS",
                "generated_at",
                "project_root",
                "export_dir",
                "ux_status",
                "roadmap_status",
                "roadmap_step_count",
                "done_step_count",
                "current_step_count",
                "post_python_step_count",
                "nicegui_tab_count",
                "sheet_tab_count",
                "ready_mapping_count",
                "migration_coverage_percent",
                "route_success_count",
                "route_smoke_ok",
                "blocker_count",
                "blockers",
                "gem_call_executed",
                "google_sheets_write",
                "live_google_api_call_from_python",
                "apps_script_execution",
                "clasp_push",
                "public_serve",
                "broker",
                "order",
                "sizing",
                "auto_apply_gem_response",
                "source_prompt_modified",
                "real_sheet_write_allowed",
                "recommended_next",
                "parallel_waiting_next",
            ]
        }
        (export_path / "P199UX_R4_SUMMARY.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P199UX-R4 visual UX polish.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_visual_ux_polish_with_smoke(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_visual_ux_polish(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"UX_STATUS={payload['ux_status']}")
        print(f"NICEGUI_TAB_COUNT={payload['nicegui_tab_count']}")

    return 0 if payload["nicegui_tab_count"] >= 8 and not payload["google_sheets_write"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
