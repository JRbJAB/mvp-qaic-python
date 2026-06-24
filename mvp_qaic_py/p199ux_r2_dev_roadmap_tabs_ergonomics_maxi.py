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

from mvp_qaic_py.p198_sheets_export_dry_run_contract_pack_maxi import (
    build_sheets_export_dry_run_contract_pack,
)
from mvp_qaic_py.p199_apps_script_sheets_function_tab_migration_map_maxi import (
    build_apps_script_sheets_function_tab_migration_map,
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


NICEGUI_TAB_ROWS: list[dict[str, str]] = [
    {
        "route": "/migration",
        "label_fr": "Suivi dev migration",
        "purpose": "Voir l'état global de migration et les artefacts produits.",
        "data_rendered": "artefacts, statuts, modules, exports, routes, scores",
        "operator_value": "savoir où on en est sans relire tous les logs",
        "status": "VISIBLE",
    },
    {
        "route": "/dev-roadmap",
        "label_fr": "Roadmap visuelle",
        "purpose": "Piloter passé, en cours, futur et post-Python.",
        "data_rendered": "lanes, périodes, progrès, next packs, décisions",
        "operator_value": "prioriser les batchs MAXI et éviter les micro-étapes",
        "status": "THIS_BATCH",
    },
    {
        "route": "/sheets-export",
        "label_fr": "Dry-run Sheets",
        "purpose": "Préparer les onglets Sheets sans écriture live.",
        "data_rendered": "13 onglets cibles, colonnes, readiness, gates",
        "operator_value": "valider le futur cockpit Sheets avant autorisation write",
        "status": "VISIBLE",
    },
    {
        "route": "/apps-script-map",
        "label_fr": "Migration Map",
        "purpose": "Mapper Sheets, Apps Script/local HTML, Python, NiceGUI.",
        "data_rendered": "onglets, modules, fonctions, sources, migration %",
        "operator_value": "décider quoi garder, migrer, archiver ou revoir",
        "status": "VISIBLE",
    },
    {
        "route": "/gem-tracking",
        "label_fr": "Suivi GEM",
        "purpose": "Suivre capture, réponse, session, roundtrip et review GEM.",
        "data_rendered": "couches GEM, binding, evidence, statuts",
        "operator_value": "contrôler le flux prompt → réponse GEM → review",
        "status": "VISIBLE",
    },
    {
        "route": "/runtime-contract",
        "label_fr": "Contrat runtime",
        "purpose": "Fermer les contrats runtime GEM et Sheets futur.",
        "data_rendered": "contrats, readiness, blockers, write policy",
        "operator_value": "sécuriser les exports avant toute écriture",
        "status": "VISIBLE",
    },
    {
        "route": "/prompt-master",
        "label_fr": "Prompt Master",
        "purpose": "Comparer l'historique prompt et choisir un candidat master.",
        "data_rendered": "candidats, scores, checklist de régression",
        "operator_value": "améliorer le prompt sans auto-apply",
        "status": "VISIBLE",
    },
    {
        "route": "/real-case-inputs",
        "label_fr": "Cas réel portfolio",
        "purpose": "Déposer capture portfolio et réponse GEM réelle.",
        "data_rendered": "fichiers attendus, compteurs, blockers, next review",
        "operator_value": "lancer le vrai test opérateur dès inputs disponibles",
        "status": "WAITING_INPUTS",
    },
    {
        "route": "/operator-release",
        "label_fr": "Release opérateur",
        "purpose": "Synthèse opérateur et choix du prochain chantier.",
        "data_rendered": "gates, waivers, next work selector",
        "operator_value": "décision rapide avant release locale finale",
        "status": "VISIBLE",
    },
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _roadmap_rows(dry_run: dict[str, Any], migration_map: dict[str, Any]) -> list[dict[str, Any]]:
    coverage = int(round(float(migration_map.get("migration_map_coverage_percent", 0))))
    dry = int(round(float(dry_run.get("dry_run_coverage_percent", 0))))

    return [
        {
            "order": 1,
            "period": "PASSÉ",
            "lane": "Fondation Python MVP_QAIC_PY",
            "status": "DONE",
            "progress_percent": 100,
            "visible_route": "/migration",
            "next_action": "Conserver comme socle local privé",
        },
        {
            "order": 2,
            "period": "PASSÉ",
            "lane": "NiceGUI local privé",
            "status": "DONE",
            "progress_percent": 100,
            "visible_route": "/",
            "next_action": "Continuer polish UX utile",
        },
        {
            "order": 3,
            "period": "PASSÉ",
            "lane": "Prompt / capture / réponse GEM",
            "status": "DONE",
            "progress_percent": 95,
            "visible_route": "/prompt",
            "next_action": "Tester avec cas réel opérateur",
        },
        {
            "order": 4,
            "period": "PASSÉ",
            "lane": "GEM tracking / evidence / runtime contract",
            "status": "DONE",
            "progress_percent": 100,
            "visible_route": "/gem-tracking",
            "next_action": "Utiliser comme base journal / review",
        },
        {
            "order": 5,
            "period": "PASSÉ",
            "lane": "Prompt master historique",
            "status": "DONE_REVIEW_READY",
            "progress_percent": 95,
            "visible_route": "/prompt-master",
            "next_action": "Review humaine avant patch source futur",
        },
        {
            "order": 6,
            "period": "EN COURS",
            "lane": "Sheets export dry-run",
            "status": "READY_NO_LIVE_WRITE",
            "progress_percent": dry,
            "visible_route": "/sheets-export",
            "next_action": "Valider le contrat 13 onglets",
        },
        {
            "order": 7,
            "period": "EN COURS",
            "lane": "Migration Map Sheets / Apps Script / Python / NiceGUI",
            "status": "READY_READONLY",
            "progress_percent": coverage,
            "visible_route": "/apps-script-map",
            "next_action": "Garder la cartographie pour P200",
        },
        {
            "order": 8,
            "period": "EN COURS",
            "lane": "Roadmap visuelle opérateur",
            "status": "THIS_BATCH",
            "progress_percent": 100,
            "visible_route": "/dev-roadmap",
            "next_action": "Devenir page de pilotage principale",
        },
        {
            "order": 9,
            "period": "EN ATTENTE",
            "lane": "Vrai cas GEM portfolio",
            "status": "WAITING_CAPTURE_AND_RESPONSE",
            "progress_percent": 60,
            "visible_route": "/real-case-inputs",
            "next_action": "Déposer capture + réponse GEM réelle",
        },
        {
            "order": 10,
            "period": "AVENIR PROCHE",
            "lane": "Operator release cockpit final",
            "status": "NEXT_MAXI",
            "progress_percent": 80,
            "visible_route": "/operator-release",
            "next_action": "P200_OPERATOR_RELEASE_COCKPIT_FINAL_MAXI",
        },
        {
            "order": 11,
            "period": "AVENIR PROCHE",
            "lane": "Sheets live write gate",
            "status": "BLOCKED_BY_POLICY",
            "progress_percent": 40,
            "visible_route": "/sheets-export",
            "next_action": "Autorisation humaine explicite plus tard seulement",
        },
        {
            "order": 12,
            "period": "POST-PYTHON",
            "lane": "Google Sheets cockpit public/privé",
            "status": "FUTURE",
            "progress_percent": 25,
            "visible_route": "/sheets-export",
            "next_action": "Importer uniquement après validation live-write",
        },
        {
            "order": 13,
            "period": "POST-PYTHON",
            "lane": "WebApp publique MVP",
            "status": "FUTURE",
            "progress_percent": 20,
            "visible_route": "/dev-roadmap",
            "next_action": "Séparer public lexique/méthode/prompt du backend privé",
        },
        {
            "order": 14,
            "period": "POST-PYTHON",
            "lane": "QAIC backend privé trading",
            "status": "FUTURE_SEPARATE",
            "progress_percent": 15,
            "visible_route": "/dev-roadmap",
            "next_action": "Bridge futur vers QAIC, sans auto order/sizing",
        },
        {
            "order": 15,
            "period": "POST-PYTHON",
            "lane": "BigQuery / Cloud Run / IA gouvernée",
            "status": "FUTURE_AFTER_LOCAL_STABLE",
            "progress_percent": 10,
            "visible_route": "/dev-roadmap",
            "next_action": "Seulement après stabilité MVP local",
        },
    ]


def _decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "decision": "Clôturer cockpit opérateur final",
            "status": "NEXT",
            "next_pack": "P200_OPERATOR_RELEASE_COCKPIT_FINAL_MAXI",
        },
        {
            "priority": 2,
            "decision": "Traiter vrai cas portfolio GEM",
            "status": "WAITING_INPUTS",
            "next_pack": "P196B_AFTER_CAPTURE_AND_RESPONSE",
        },
        {
            "priority": 3,
            "decision": "Autoriser ou refuser live Sheets write",
            "status": "BLOCKED_BY_POLICY",
            "next_pack": "FUTURE_HUMAN_APPROVAL_ONLY",
        },
        {
            "priority": 4,
            "decision": "Évolution post-Python public/private",
            "status": "FUTURE",
            "next_pack": "POST_LOCAL_RELEASE_STRATEGY",
        },
    ]


def build_dev_roadmap_tabs_ergonomics(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    dry_run = build_sheets_export_dry_run_contract_pack(root)
    migration_map = build_apps_script_sheets_function_tab_migration_map(root)
    roadmap = _roadmap_rows(dry_run, migration_map)

    post_python_rows = [row for row in roadmap if row["period"] == "POST-PYTHON"]
    current_rows = [row for row in roadmap if row["period"] == "EN COURS"]
    done_rows = [row for row in roadmap if row["period"] == "PASSÉ"]

    return {
        "STATUS": "OK_P199UX_R2_DEV_ROADMAP_TABS_ERGONOMICS_READY",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "roadmap_status": "VISIBLE_PAST_CURRENT_FUTURE_POST_PYTHON",
        "roadmap_step_count": len(roadmap),
        "done_step_count": len(done_rows),
        "current_step_count": len(current_rows),
        "post_python_step_count": len(post_python_rows),
        "nicegui_tab_count": len(NICEGUI_TAB_ROWS),
        "sheet_tab_count": migration_map["sheet_tab_count"],
        "ready_mapping_count": migration_map["ready_mapping_count"],
        "migration_coverage_percent": migration_map["migration_map_coverage_percent"],
        "roadmap_rows": roadmap,
        "nicegui_tab_rows": NICEGUI_TAB_ROWS,
        "decision_rows": _decision_rows(),
        "migration_summary": {
            "sheet_tab_count": migration_map["sheet_tab_count"],
            "ready_mapping_count": migration_map["ready_mapping_count"],
            "python_module_count": migration_map["python_module_count"],
            "apps_script_source_count": migration_map["apps_script_source_count"],
            "migration_map_coverage_percent": migration_map["migration_map_coverage_percent"],
        },
        "blocker_count": 0,
        "blockers": [],
        **SAFETY_FLAGS,
        "recommended_next": "P200_OPERATOR_RELEASE_COCKPIT_FINAL_MAXI",
        "parallel_waiting_next": "P196B_REAL_CASE_PORTFOLIO_GEM_REVIEW_AFTER_OPERATOR_INPUTS_MAXI_AFTER_INPUTS",
    }


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def export_dev_roadmap_tabs_ergonomics(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P199UX_R2_DEV_ROADMAP_TABS_ERGONOMICS_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = build_dev_roadmap_tabs_ergonomics(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P199UX_R2_DEV_ROADMAP_TABS_ERGONOMICS.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    _write_csv(
        export_path / "P199UX_R2_VISUAL_ROADMAP.csv",
        payload["roadmap_rows"],
        ["order", "period", "lane", "status", "progress_percent", "visible_route", "next_action"],
    )
    _write_csv(
        export_path / "P199UX_R2_NICEGUI_TABS_USABILITY.csv",
        payload["nicegui_tab_rows"],
        ["route", "label_fr", "purpose", "data_rendered", "operator_value", "status"],
    )
    _write_csv(
        export_path / "P199UX_R2_DECISIONS.csv",
        payload["decision_rows"],
        ["priority", "decision", "status", "next_pack"],
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
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
    (export_path / "P199UX_R2_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = [
        "# P199UX-R2 Dev Roadmap + NiceGUI Tabs Ergonomics MAXI",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- roadmap_step_count: {payload['roadmap_step_count']}",
        f"- nicegui_tab_count: {payload['nicegui_tab_count']}",
        f"- sheet_tab_count: {payload['sheet_tab_count']}",
        f"- ready_mapping_count: {payload['ready_mapping_count']}",
        f"- migration_coverage_percent: {payload['migration_coverage_percent']}",
        "",
        "## Routes visibles",
        "- /migration",
        "- /dev-roadmap",
        "- /sheets-export",
        "- /apps-script-map",
        "- /prompt-master",
        "- /real-case-inputs",
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
    (export_path / "P199UX_R2_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    return payload


def _http_ok(url: str) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P199UX-R2"})
        with urllib.request.urlopen(request, timeout=2.0) as response:
            return 200 <= int(response.status) < 500
    except Exception:
        return False


def run_p199ux_r2_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8108,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_dev_roadmap_tabs_ergonomics(root)

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
            time.sleep(1.0)
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=8)
                server_stopped = True
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=8)
                server_stopped = True
        else:
            server_stopped = True

    return {
        **payload,
        "STATUS": "OK_P199UX_R2_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P199UX_R2_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_dev_roadmap_tabs_ergonomics_with_smoke(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    payload = export_dev_roadmap_tabs_ergonomics(project_root, export_dir=export_dir)
    if run_route_smoke:
        smoke = run_p199ux_r2_route_smoke(project_root)
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
        (export_path / "P199UX_R2_SUMMARY.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P199UX-R2 dev roadmap tabs ergonomics.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_dev_roadmap_tabs_ergonomics_with_smoke(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_dev_roadmap_tabs_ergonomics(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"ROADMAP_STEP_COUNT={payload['roadmap_step_count']}")
        print(f"NICEGUI_TAB_COUNT={payload['nicegui_tab_count']}")

    return 0 if payload["roadmap_step_count"] >= 12 and not payload["google_sheets_write"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
