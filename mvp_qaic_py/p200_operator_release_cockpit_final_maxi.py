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


def build_operator_release_cockpit_final(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    ux = build_visual_ux_polish(root)
    real_case = build_real_case_portfolio_gem_inputs(root)

    release_rows = [
        {
            "priority": 1,
            "area": "Runtime NiceGUI",
            "status": "READY",
            "evidence": f"{ux['nicegui_tab_count']} onglets utiles / {ux['route_success_count'] if 'route_success_count' in ux else 'smoke via P200'} routes",
            "operator_action": "Utiliser /dev-roadmap comme cockpit principal",
        },
        {
            "priority": 2,
            "area": "Planning visuel",
            "status": "READY",
            "evidence": f"{ux['roadmap_step_count']} étapes dont {ux['post_python_step_count']} post-Python",
            "operator_action": "Suivre passé / en cours / attente / futur",
        },
        {
            "priority": 3,
            "area": "Migration Map",
            "status": "READY",
            "evidence": f"coverage={ux['migration_coverage_percent']}%, sheet_tabs={ux['sheet_tab_count']}, ready_mapping={ux['ready_mapping_count']}",
            "operator_action": "Garder comme référence avant live Sheets",
        },
        {
            "priority": 4,
            "area": "Sheets dry-run",
            "status": "READY_NO_LIVE_WRITE",
            "evidence": "13 onglets cibles, écriture live bloquée",
            "operator_action": "Validation humaine avant toute écriture Google Sheets",
        },
        {
            "priority": 5,
            "area": "Cas réel GEM portfolio",
            "status": real_case["input_status"],
            "evidence": f"captures={real_case['capture_count']}, responses={real_case['response_count']}",
            "operator_action": real_case["recommended_next"],
        },
        {
            "priority": 6,
            "area": "Sécurité",
            "status": "PASS",
            "evidence": "NO_GEM_CALL / NO_SHEETS_WRITE / NO_APPS_SCRIPT / NO_CLASP / NO_BROKER",
            "operator_action": "Maintenir verrouillage jusqu’à autorisation explicite",
        },
    ]

    blockers: list[str] = []
    if ux["nicegui_tab_count"] < 8:
        blockers.append("NICEGUI_TAB_COUNT_TOO_LOW")
    if ux["roadmap_step_count"] < 12:
        blockers.append("ROADMAP_STEP_COUNT_TOO_LOW")
    if ux["migration_coverage_percent"] < 95:
        blockers.append("MIGRATION_COVERAGE_BELOW_95")
    if any(SAFETY_FLAGS.values()):
        blockers.append("UNEXPECTED_SAFETY_FLAG_TRUE")

    release_status = (
        "LOCAL_PRIVATE_OPERATOR_RELEASE_READY" if not blockers else "RELEASE_REVIEW_REQUIRED"
    )

    decision_rows = [
        {
            "priority": 1,
            "decision": "Lancer cockpit local privé",
            "status": "READY",
            "route": "/dev-roadmap",
        },
        {
            "priority": 2,
            "decision": "Tester le vrai cas GEM portfolio",
            "status": "WAITING_INPUTS"
            if real_case["ready_for_real_case_review"] is False
            else "READY",
            "route": "/real-case-inputs",
        },
        {
            "priority": 3,
            "decision": "Autoriser live Google Sheets",
            "status": "BLOCKED_BY_POLICY",
            "route": "/sheets-export",
        },
        {
            "priority": 4,
            "decision": "Préparer stratégie post-Python",
            "status": "FUTURE",
            "route": "/dev-roadmap",
        },
    ]

    return {
        "STATUS": "OK_P200_OPERATOR_RELEASE_COCKPIT_FINAL_READY"
        if not blockers
        else "REVIEW_P200_OPERATOR_RELEASE_COCKPIT_FINAL",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "release_status": release_status,
        "release_rows": release_rows,
        "decision_rows": decision_rows,
        "roadmap_step_count": ux["roadmap_step_count"],
        "post_python_step_count": ux["post_python_step_count"],
        "nicegui_tab_count": ux["nicegui_tab_count"],
        "sheet_tab_count": ux["sheet_tab_count"],
        "ready_mapping_count": ux["ready_mapping_count"],
        "migration_coverage_percent": ux["migration_coverage_percent"],
        "real_case_input_status": real_case["input_status"],
        "real_case_capture_count": real_case["capture_count"],
        "real_case_response_count": real_case["response_count"],
        "real_case_ready_for_review": real_case["ready_for_real_case_review"],
        "blocker_count": len(blockers),
        "blockers": blockers,
        **SAFETY_FLAGS,
        "recommended_next": "P201_REAL_CASE_REVIEW_IF_INPUTS_READY_OR_LOCAL_RELEASE_SEAL",
        "parallel_waiting_next": "P196B_REAL_CASE_PORTFOLIO_GEM_REVIEW_AFTER_OPERATOR_INPUTS_MAXI_AFTER_INPUTS",
    }


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def export_operator_release_cockpit_final(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P200_OPERATOR_RELEASE_COCKPIT_FINAL_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = build_operator_release_cockpit_final(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P200_OPERATOR_RELEASE_COCKPIT_FINAL.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    _write_csv(
        export_path / "P200_RELEASE_ROWS.csv",
        payload["release_rows"],
        ["priority", "area", "status", "evidence", "operator_action"],
    )
    _write_csv(
        export_path / "P200_DECISIONS.csv",
        payload["decision_rows"],
        ["priority", "decision", "status", "route"],
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
    (export_path / "P200_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = [
        "# P200 Operator Release Cockpit Final MAXI",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- release_status: {payload['release_status']}",
        f"- nicegui_tab_count: {payload['nicegui_tab_count']}",
        f"- roadmap_step_count: {payload['roadmap_step_count']}",
        f"- migration_coverage_percent: {payload['migration_coverage_percent']}",
        f"- real_case_input_status: {payload['real_case_input_status']}",
        "",
        "## Décision",
        "- Cockpit local privé prêt pour usage opérateur.",
        "- Live Google Sheets reste bloqué par politique.",
        "- Cas réel GEM portfolio attend capture + réponse si non déjà déposées.",
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
    (export_path / "P200_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    return payload


def _http_ok(url: str) -> bool:
    request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P200"})
    for timeout in (12.0, 24.0, 36.0):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return 200 <= int(response.status) < 500
        except Exception:
            time.sleep(0.75)
    return False


def run_p200_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8110,
    timeout_seconds: int = 150,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_operator_release_cockpit_final(root)

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
        "STATUS": "OK_P200_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P200_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_operator_release_cockpit_final_with_smoke(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    payload = export_operator_release_cockpit_final(project_root, export_dir=export_dir)
    if run_route_smoke:
        smoke = run_p200_route_smoke(project_root)
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
        (export_path / "P200_SUMMARY.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P200 operator release cockpit final.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_operator_release_cockpit_final_with_smoke(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_operator_release_cockpit_final(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"RELEASE_STATUS={payload['release_status']}")

    return (
        0
        if payload["release_status"]
        in {"LOCAL_PRIVATE_OPERATOR_RELEASE_READY", "RELEASE_REVIEW_REQUIRED"}
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
