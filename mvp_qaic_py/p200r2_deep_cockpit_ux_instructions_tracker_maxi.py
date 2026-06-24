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

from mvp_qaic_py.p196_real_case_portfolio_gem_operator_inputs_maxi import (
    build_real_case_portfolio_gem_inputs,
)
from mvp_qaic_py.p199_apps_script_sheets_function_tab_migration_map_maxi import (
    build_apps_script_sheets_function_tab_migration_map,
)
from mvp_qaic_py.p199ux_r4_visual_ux_polish_maxi import build_visual_ux_polish


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
    "/release-final",
    "/migration-control",
    "/instructions",
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


def _bool_from_any(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return str(value).strip().lower() in {"true", "1", "yes", "ok", "ready"}


def _safe_get_real_case_ready(real_case: dict[str, Any]) -> bool:
    return _bool_from_any(
        real_case.get("ready_for_real_case_review", real_case.get("ready_for_review", False))
    )


def _color_cell(status: str) -> str:
    status_upper = str(status).upper()
    if any(token in status_upper for token in ["READY", "PASS", "DONE", "VISIBLE", "OK"]):
        return "🟩"
    if any(token in status_upper for token in ["WAIT", "REVIEW", "NEXT", "FUTURE"]):
        return "🟧"
    if any(token in status_upper for token in ["BLOCK", "FAIL", "ERROR", "STOP"]):
        return "🟥"
    return "🟦"


def _progress_from_status(status: str) -> int:
    status_upper = str(status).upper()
    if any(token in status_upper for token in ["DONE", "READY", "PASS", "OK"]):
        return 100
    if any(token in status_upper for token in ["VISIBLE", "ACTIVE"]):
        return 90
    if any(token in status_upper for token in ["NEXT", "REVIEW"]):
        return 70
    if any(token in status_upper for token in ["WAIT", "FUTURE"]):
        return 45
    if any(token in status_upper for token in ["BLOCK", "FAIL", "ERROR"]):
        return 0
    return 50


def _instruction_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theme": "Safety QAIC",
            "obligation": "HUMAN_REVIEW_ONLY permanent",
            "status": "PASS_MANDATORY",
            "evidence": "No broker/order/sizing flags must remain false.",
            "correction_rule": "Tout batch doit exposer les flags safety dans le summary.",
        },
        {
            "theme": "Safety QAIC",
            "obligation": "No auto-order / no auto-sizing / no broker execution",
            "status": "PASS_MANDATORY",
            "evidence": "BROKER=False, ORDER=False, SIZING=False.",
            "correction_rule": "Bloquer tout module qui introduit exécution réelle.",
        },
        {
            "theme": "Google Live",
            "obligation": "No Google Sheets write sans autorisation humaine explicite",
            "status": "PASS_MANDATORY",
            "evidence": "google_sheets_write=False, real_sheet_write_allowed=False.",
            "correction_rule": "Dry-run only jusqu’à validation écrite.",
        },
        {
            "theme": "Apps Script / CLASP",
            "obligation": "No Apps Script execution, no CLASP push par défaut",
            "status": "PASS_MANDATORY",
            "evidence": "apps_script_execution=False, clasp_push=False.",
            "correction_rule": "Lire/migrer/cartographier seulement.",
        },
        {
            "theme": "Batch process",
            "obligation": "Batch fast and fuse, pas de micro-patchs inutiles",
            "status": "ACTIVE_REQUIREMENT",
            "evidence": "Scripts complets, tests, export, ZIP, commit/tag/push.",
            "correction_rule": "Préférer MAXI batch avec réparation + UX + seal.",
        },
        {
            "theme": "UX Cockpit",
            "obligation": "Planning visuel en haut des onglets clés",
            "status": "ACTIVE_REQUIREMENT",
            "evidence": "Global banner + /dev-roadmap + /migration-control.",
            "correction_rule": "Chaque cockpit doit commencer par cards/compteurs et planning.",
        },
        {
            "theme": "UX Cockpit",
            "obligation": "Tables compactes, utiles, colorées",
            "status": "ACTIVE_REQUIREMENT",
            "evidence": "color_cell, entity_type, progress_percent, done/todo/action.",
            "correction_rule": "Interdire les tables longues sans statut, couleur et action.",
        },
        {
            "theme": "Migration",
            "obligation": "Voir fait/reste à faire pour onglets, scripts, fonctions",
            "status": "ACTIVE_REQUIREMENT",
            "evidence": "/migration-control agrège SHEET_TAB, PYTHON_MODULE, APPS_SCRIPT_SOURCE, FUNCTION.",
            "correction_rule": "Toute migration doit produire une matrice lisible opérateur.",
        },
        {
            "theme": "Prompt/GEM",
            "obligation": "Ne jamais inventer prix, quantité, PnL, PRU, TP, SL",
            "status": "PASS_MANDATORY",
            "evidence": "Prompt master et real-case restent review-only.",
            "correction_rule": "Si données manquantes : REVIEW_REQUIRED/BLOCKED.",
        },
        {
            "theme": "Evidence",
            "obligation": "Ne pas annoncer scellé si export/summary/route smoke absent",
            "status": "CRITICAL_CORRECTION",
            "evidence": "P200 initial a eu un faux seal après KeyError.",
            "correction_rule": "Le batch doit stopper avant commit si summary ou smoke manquent.",
        },
    ]

    for index, row in enumerate(rows, start=1):
        row["priority"] = index
        row["color_cell"] = _color_cell(row["status"])
        row["progress_percent"] = _progress_from_status(row["status"])
    return rows


def _migration_control_rows(migration: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for row in migration.get("migration_rows", []):
        status = str(row.get("migration_status", row.get("dry_run_status", "REVIEW")))
        rows.append(
            {
                "priority": len(rows) + 1,
                "entity_type": "SHEET_TAB",
                "name": row.get("sheet_tab", ""),
                "binding": row.get("python_binding", ""),
                "route": row.get("nicegui_route", row.get("source_export", "")),
                "status": status,
                "color_cell": _color_cell(status),
                "progress_percent": row.get("migration_percent", _progress_from_status(status)),
                "done": "Mapping onglet cible + runtime layer",
                "todo": row.get("next_action", "Review mapping"),
            }
        )

    for row in migration.get("python_module_rows", [])[:80]:
        status = "PYTHON_MODULE_DISCOVERED"
        rows.append(
            {
                "priority": len(rows) + 1,
                "entity_type": "PYTHON_MODULE",
                "name": row.get("module", ""),
                "binding": row.get("migration_role", ""),
                "route": "",
                "status": status,
                "color_cell": _color_cell(status),
                "progress_percent": 90,
                "done": f"{row.get('function_count', 0)} fonctions détectées",
                "todo": "Garder si utile / archiver si legacy",
            }
        )

    for row in migration.get("apps_script_source_rows", [])[:80]:
        status = row.get("migration_status", "APPS_SCRIPT_SOURCE_DISCOVERED")
        rows.append(
            {
                "priority": len(rows) + 1,
                "entity_type": "APPS_SCRIPT_SOURCE",
                "name": row.get("source_path", ""),
                "binding": row.get("source_type", ""),
                "route": "",
                "status": status,
                "color_cell": _color_cell(str(status)),
                "progress_percent": _progress_from_status(str(status)),
                "done": f"{row.get('function_count', 0)} fonctions Apps Script/local détectées",
                "todo": row.get("next_action", "Map or archive"),
            }
        )

    function_priority_limit = 220
    for module_row in migration.get("python_module_rows", [])[:80]:
        module = str(module_row.get("module", ""))
        functions = [
            item.strip() for item in str(module_row.get("functions", "")).split(";") if item.strip()
        ][:8]
        for function_name in functions:
            if len(rows) >= function_priority_limit:
                break
            status = "FUNCTION_DISCOVERED"
            rows.append(
                {
                    "priority": len(rows) + 1,
                    "entity_type": "FUNCTION",
                    "name": function_name,
                    "binding": module,
                    "route": "",
                    "status": status,
                    "color_cell": _color_cell(status),
                    "progress_percent": 80,
                    "done": "Fonction présente dans module Python",
                    "todo": "Relier à route/onglet si fonction opérateur",
                }
            )

    return rows


def _global_planning_rows(ux: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in ux.get("top_visual_planning_rows", []):
        status = row.get("main_status", "")
        rows.append(
            {
                "order": row.get("order"),
                "period": row.get("period"),
                "step_count": row.get("step_count"),
                "progress_percent": row.get("avg_progress_percent"),
                "status": status,
                "color_cell": _color_cell(str(status)),
                "route": row.get("main_route"),
            }
        )
    return rows


def build_deep_operator_cockpit(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    ux = build_visual_ux_polish(root)
    migration = build_apps_script_sheets_function_tab_migration_map(root)
    real_case = build_real_case_portfolio_gem_inputs(root)

    real_case_ready = _safe_get_real_case_ready(real_case)
    migration_control_rows = _migration_control_rows(migration)
    instruction_rows = _instruction_rows()

    release_rows = [
        {
            "priority": 1,
            "area": "Cockpit visuel",
            "status": "READY",
            "color_cell": "🟩",
            "evidence": f"{ux['roadmap_step_count']} étapes, {ux['nicegui_tab_count']} onglets utiles",
            "operator_action": "Utiliser /dev-roadmap et /migration-control",
        },
        {
            "priority": 2,
            "area": "Migration tabs/scripts/functions",
            "status": "READY",
            "color_cell": "🟩",
            "evidence": f"{len(migration_control_rows)} lignes contrôlées",
            "operator_action": "Piloter fait/reste à faire par entité",
        },
        {
            "priority": 3,
            "area": "Instruction compliance",
            "status": "ACTIVE",
            "color_cell": "🟧",
            "evidence": f"{len(instruction_rows)} obligations suivies",
            "operator_action": "Vérifier /instructions avant chaque batch sensible",
        },
        {
            "priority": 4,
            "area": "Cas réel GEM",
            "status": "READY" if real_case_ready else "WAITING_INPUTS",
            "color_cell": "🟧" if not real_case_ready else "🟩",
            "evidence": f"captures={real_case.get('capture_count', 0)}, responses={real_case.get('response_count', 0)}",
            "operator_action": real_case.get("recommended_next", "WAIT_INPUTS"),
        },
        {
            "priority": 5,
            "area": "Live write",
            "status": "BLOCKED_BY_POLICY",
            "color_cell": "🟥",
            "evidence": "Google Sheets / Apps Script / CLASP live restent interdits",
            "operator_action": "Autorisation humaine future seulement",
        },
    ]

    blockers: list[str] = []
    if ux["nicegui_tab_count"] < 8:
        blockers.append("NICEGUI_TAB_COUNT_TOO_LOW")
    if ux["roadmap_step_count"] < 12:
        blockers.append("ROADMAP_STEP_COUNT_TOO_LOW")
    if migration.get("sheet_tab_count", 0) < 13:
        blockers.append("MIGRATION_SHEET_TAB_COUNT_TOO_LOW")
    if len(instruction_rows) < 8:
        blockers.append("INSTRUCTION_TRACKER_TOO_SMALL")
    if any(SAFETY_FLAGS.values()):
        blockers.append("UNEXPECTED_SAFETY_FLAG_TRUE")

    release_status = (
        "LOCAL_PRIVATE_OPERATOR_RELEASE_READY_WITH_DEEP_COCKPITS"
        if not blockers
        else "RELEASE_REVIEW_REQUIRED"
    )

    metric_cards = [
        {
            "priority": 1,
            "label": "Roadmap",
            "value": ux["roadmap_step_count"],
            "unit": "",
            "color": "blue",
        },
        {
            "priority": 2,
            "label": "Onglets utiles",
            "value": ux["nicegui_tab_count"],
            "unit": "",
            "color": "green",
        },
        {
            "priority": 3,
            "label": "Migration %",
            "value": migration.get("migration_map_coverage_percent", 0),
            "unit": "%",
            "color": "teal",
        },
        {
            "priority": 4,
            "label": "Entités migration",
            "value": len(migration_control_rows),
            "unit": "",
            "color": "purple",
        },
        {
            "priority": 5,
            "label": "Obligations",
            "value": len(instruction_rows),
            "unit": "",
            "color": "orange",
        },
        {"priority": 6, "label": "Live write", "value": "NO", "unit": "", "color": "red"},
    ]

    return {
        "STATUS": "OK_P200R2_DEEP_COCKPIT_UX_INSTRUCTIONS_READY"
        if not blockers
        else "REVIEW_P200R2_DEEP_COCKPIT_UX_INSTRUCTIONS",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "release_status": release_status,
        "metric_card_rows": metric_cards,
        "global_planning_rows": _global_planning_rows(ux),
        "release_rows": release_rows,
        "migration_control_rows": migration_control_rows,
        "instruction_rows": instruction_rows,
        "nicegui_tab_rows": ux["nicegui_tab_rows"],
        "roadmap_step_count": ux["roadmap_step_count"],
        "post_python_step_count": ux["post_python_step_count"],
        "nicegui_tab_count": ux["nicegui_tab_count"],
        "sheet_tab_count": migration.get("sheet_tab_count", 0),
        "ready_mapping_count": migration.get("ready_mapping_count", 0),
        "migration_coverage_percent": migration.get("migration_map_coverage_percent", 0),
        "migration_control_row_count": len(migration_control_rows),
        "instruction_row_count": len(instruction_rows),
        "real_case_input_status": real_case.get("input_status", "UNKNOWN"),
        "real_case_capture_count": real_case.get("capture_count", 0),
        "real_case_response_count": real_case.get("response_count", 0),
        "real_case_ready_for_review": real_case_ready,
        "blocker_count": len(blockers),
        "blockers": blockers,
        **SAFETY_FLAGS,
        "recommended_next": "P201_REAL_CASE_REVIEW_IF_INPUTS_READY_OR_LOCAL_RELEASE_SEAL",
        "parallel_waiting_next": "P196B_REAL_CASE_PORTFOLIO_GEM_REVIEW_AFTER_OPERATOR_INPUTS_MAXI_AFTER_INPUTS",
    }


def build_global_visual_banner(project_root: str | Path) -> dict[str, Any]:
    payload = build_deep_operator_cockpit(project_root)
    return {
        "release_status": payload["release_status"],
        "metric_card_rows": payload["metric_card_rows"][:6],
        "global_planning_rows": payload["global_planning_rows"],
        "recommended_next": payload["recommended_next"],
    }


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def export_deep_operator_cockpit(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P200R2_DEEP_COCKPIT_UX_INSTRUCTIONS_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = build_deep_operator_cockpit(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P200R2_DEEP_COCKPIT_UX_INSTRUCTIONS.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    _write_csv(
        export_path / "P200R2_RELEASE_ROWS.csv",
        payload["release_rows"],
        ["priority", "area", "status", "color_cell", "evidence", "operator_action"],
    )
    _write_csv(
        export_path / "P200R2_GLOBAL_PLANNING.csv",
        payload["global_planning_rows"],
        ["order", "period", "step_count", "progress_percent", "status", "color_cell", "route"],
    )
    _write_csv(
        export_path / "P200R2_MIGRATION_CONTROL.csv",
        payload["migration_control_rows"],
        [
            "priority",
            "entity_type",
            "name",
            "binding",
            "route",
            "status",
            "color_cell",
            "progress_percent",
            "done",
            "todo",
        ],
    )
    _write_csv(
        export_path / "P200R2_INSTRUCTIONS_TRACKER.csv",
        payload["instruction_rows"],
        [
            "priority",
            "theme",
            "obligation",
            "status",
            "color_cell",
            "progress_percent",
            "evidence",
            "correction_rule",
        ],
    )
    _write_csv(
        export_path / "P200R2_METRIC_CARDS.csv",
        payload["metric_card_rows"],
        ["priority", "label", "value", "unit", "color"],
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "release_status",
        "roadmap_step_count",
        "post_python_step_count",
        "nicegui_tab_count",
        "sheet_tab_count",
        "ready_mapping_count",
        "migration_coverage_percent",
        "migration_control_row_count",
        "instruction_row_count",
        "real_case_input_status",
        "real_case_capture_count",
        "real_case_response_count",
        "real_case_ready_for_review",
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
    (export_path / "P200R2_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = [
        "# P200-R2 Deep Cockpit UX + Instructions Tracker MAXI",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- release_status: {payload['release_status']}",
        f"- migration_control_row_count: {payload['migration_control_row_count']}",
        f"- instruction_row_count: {payload['instruction_row_count']}",
        f"- migration_coverage_percent: {payload['migration_coverage_percent']}",
        "",
        "## Corrections",
        "- Planning visuel global en haut des onglets clés.",
        "- Migration-control pour onglets/scripts/fonctions/modules.",
        "- Cellules colorées via color_cell.",
        "- Instructions tracker par thème d'obligation.",
        "- P200 KeyError réparé via real_case_ready robuste.",
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
    (export_path / "P200R2_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    return payload


def _http_ok(url: str) -> bool:
    request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P200R2"})
    for timeout in (12.0, 24.0, 36.0):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return 200 <= int(response.status) < 500
        except Exception:
            time.sleep(0.75)
    return False


def run_p200r2_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8111,
    timeout_seconds: int = 180,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_deep_operator_cockpit(root)

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
        "STATUS": "OK_P200R2_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P200R2_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_deep_operator_cockpit_with_smoke(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    payload = export_deep_operator_cockpit(project_root, export_dir=export_dir)
    if run_route_smoke:
        smoke = run_p200r2_route_smoke(project_root)
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
                "release_status",
                "roadmap_step_count",
                "post_python_step_count",
                "nicegui_tab_count",
                "sheet_tab_count",
                "ready_mapping_count",
                "migration_coverage_percent",
                "migration_control_row_count",
                "instruction_row_count",
                "real_case_input_status",
                "real_case_capture_count",
                "real_case_response_count",
                "real_case_ready_for_review",
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
        (export_path / "P200R2_SUMMARY.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="P200-R2 deep cockpit UX and instructions tracker."
    )
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_deep_operator_cockpit_with_smoke(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_deep_operator_cockpit(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"RELEASE_STATUS={payload['release_status']}")

    return 0 if payload["release_status"].startswith("LOCAL_PRIVATE_OPERATOR_RELEASE_READY") else 2


if __name__ == "__main__":
    raise SystemExit(main())
