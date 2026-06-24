from __future__ import annotations

import argparse
import csv
import json
import re
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


EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _skip_path(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}
    return (
        bool(parts.intersection({item.lower() for item in EXCLUDED_DIRS}))
        or path.name.lower() == "desktop.ini"
    )


def _read_text(path: Path, limit: int = 20000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except Exception:
        return ""


def _extract_python_functions(text: str) -> list[str]:
    return sorted(set(re.findall(r"(?m)^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", text)))


def _extract_apps_script_functions(text: str) -> list[str]:
    names = set(re.findall(r"(?m)^\s*function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", text))
    names.update(re.findall(r"(?m)^\s*(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\(", text))
    return sorted(names)


def _migration_role_from_module(rel: str) -> str:
    lowered = rel.lower()
    if "p173" in lowered or "nicegui" in lowered:
        return "NICEGUI_RUNTIME_UI"
    if "p190" in lowered or "migration" in lowered:
        return "DEV_MIGRATION_TRACKER"
    if "p191" in lowered or "gem_tracking" in lowered:
        return "GEM_TRACKING_BINDING"
    if "p194" in lowered or "runtime_close" in lowered:
        return "RUNTIME_CONTRACT"
    if "p198" in lowered or "sheets_export" in lowered:
        return "SHEETS_EXPORT_DRY_RUN"
    if "prompt" in lowered:
        return "PROMPT_LAYER"
    if "test" in lowered:
        return "TEST_LAYER"
    return "PYTHON_SUPPORT"


def _collect_python_modules(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for base in [root / "mvp_qaic_py", root / "tests"]:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.py")):
            if _skip_path(path):
                continue
            text = _read_text(path)
            functions = _extract_python_functions(text)
            rel = _safe_rel(path, root)
            rows.append(
                {
                    "module": rel,
                    "function_count": len(functions),
                    "functions": ";".join(functions[:60]),
                    "migration_role": _migration_role_from_module(rel),
                }
            )
    return rows


def _collect_apps_script_sources(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    suffixes = {".gs", ".js", ".html"}
    candidate_roots = [
        root / "apps_script",
        root / "exports",
        root / "05_EXPORTS",
        root / "00_OPERATOR_EXPORTS",
    ]

    seen: set[Path] = set()
    for base in candidate_roots:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if len(rows) >= 300:
                break
            if not path.is_file() or _skip_path(path) or path.suffix.lower() not in suffixes:
                continue
            if path in seen:
                continue
            seen.add(path)
            text = _read_text(path)
            functions = _extract_apps_script_functions(text)
            rows.append(
                {
                    "source_path": _safe_rel(path, root),
                    "source_type": "APPS_SCRIPT_OR_WEBAPP_SOURCE",
                    "function_count": len(functions),
                    "functions": ";".join(functions[:80]),
                    "migration_status": "DISCOVERED_READONLY",
                    "next_action": "MAP_TO_PYTHON_OR_ARCHIVE_LEGACY",
                }
            )
    return rows


def _match_python_binding(runtime_layer: str, python_rows: list[dict[str, Any]]) -> str:
    tokens = [
        token.lower() for token in re.split(r"[^A-Za-z0-9]+", runtime_layer) if len(token) >= 4
    ]
    best = ""
    best_score = 0
    for row in python_rows:
        hay = f"{row['module']} {row['functions']} {row['migration_role']}".lower()
        score = sum(1 for token in tokens if token in hay)
        if score > best_score:
            best_score = score
            best = str(row["module"])
    return best


def _match_apps_script_binding(sheet_tab: str, apps_rows: list[dict[str, Any]]) -> str:
    tokens = [token.lower() for token in re.split(r"[^A-Za-z0-9]+", sheet_tab) if len(token) >= 4]
    best = ""
    best_score = 0
    for row in apps_rows:
        hay = f"{row['source_path']} {row['functions']}".lower()
        score = sum(1 for token in tokens if token in hay)
        if score > best_score:
            best_score = score
            best = str(row["source_path"])
    return best


def _status_for_row(sheet_row: dict[str, Any], python_binding: str, apps_binding: str) -> str:
    dry = str(sheet_row.get("dry_run_status", ""))
    if dry == "DRY_RUN_READY" and python_binding:
        return "PYTHON_READY_SHEETS_DRY_RUN_READY"
    if dry == "DRY_RUN_READY_WITH_REVIEW" and python_binding:
        return "PYTHON_READY_CONTRACT_REVIEW"
    if apps_binding and not python_binding:
        return "APPS_SCRIPT_SOURCE_FOUND_PYTHON_MAPPING_REVIEW"
    if python_binding:
        return "PYTHON_BINDING_READY_REVIEW"
    return "MAPPING_REVIEW_REQUIRED"


def build_apps_script_sheets_function_tab_migration_map(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    dry_run = build_sheets_export_dry_run_contract_pack(root)
    python_rows = _collect_python_modules(root)
    apps_rows = _collect_apps_script_sources(root)

    migration_rows: list[dict[str, Any]] = []
    for sheet_row in dry_run["target_tab_rows"]:
        python_binding = _match_python_binding(str(sheet_row["runtime_layer"]), python_rows)
        apps_binding = _match_apps_script_binding(str(sheet_row["sheet_tab"]), apps_rows)
        migration_status = _status_for_row(sheet_row, python_binding, apps_binding)
        migration_rows.append(
            {
                "priority": sheet_row["priority"],
                "sheet_tab": sheet_row["sheet_tab"],
                "runtime_layer": sheet_row["runtime_layer"],
                "source_export": sheet_row["source_export"],
                "python_binding": python_binding,
                "apps_script_binding": apps_binding,
                "dry_run_status": sheet_row["dry_run_status"],
                "migration_status": migration_status,
                "migration_percent": 100
                if migration_status == "PYTHON_READY_SHEETS_DRY_RUN_READY"
                else 85
                if python_binding
                else 50,
                "next_action": "KEEP_PYTHON_DRY_RUN_NO_LIVE_WRITE"
                if python_binding
                else "REVIEW_AND_BIND_PYTHON_MODULE",
            }
        )

    ready_rows = [
        row
        for row in migration_rows
        if row["migration_status"]
        in {"PYTHON_READY_SHEETS_DRY_RUN_READY", "PYTHON_READY_CONTRACT_REVIEW"}
    ]
    coverage = round(
        sum(int(row["migration_percent"]) for row in migration_rows) / len(migration_rows), 1
    )

    gate_rows = [
        {
            "gate": "NO_APPS_SCRIPT_EXECUTION",
            "status": "PASS",
            "value": "False",
            "reason": "P199 only scans local files and exports mapping.",
        },
        {
            "gate": "NO_CLASP_PUSH",
            "status": "PASS",
            "value": "False",
            "reason": "No CLASP command is executed.",
        },
        {
            "gate": "NO_GOOGLE_SHEETS_WRITE",
            "status": "PASS",
            "value": "False",
            "reason": "No Sheets API/write action.",
        },
        {
            "gate": "TARGET_TAB_COUNT",
            "status": "PASS" if len(migration_rows) == 13 else "FAIL",
            "value": str(len(migration_rows)),
            "reason": "Mapping inherits P198 target tabs.",
        },
        {
            "gate": "PYTHON_MODULES_DISCOVERED",
            "status": "PASS" if python_rows else "REVIEW",
            "value": str(len(python_rows)),
            "reason": "Python modules are the MVP runtime source for migration.",
        },
    ]

    visual_planning_rows = [
        {
            "step": 1,
            "lane": "DEV_MIGRATION_TRACKER",
            "status": "VISIBLE_NOW",
            "next_pack": "OPEN_/migration",
        },
        {
            "step": 2,
            "lane": "SHEETS_EXPORT_DRY_RUN",
            "status": "VISIBLE_NOW",
            "next_pack": "OPEN_/sheets-export",
        },
        {
            "step": 3,
            "lane": "APPS_SCRIPT_SHEETS_MIGRATION_MAP",
            "status": "THIS_BATCH",
            "next_pack": "P199",
        },
        {
            "step": 4,
            "lane": "FINAL_OPERATOR_RELEASE_COCKPIT",
            "status": "NEXT_MAXI",
            "next_pack": "P200",
        },
        {
            "step": 5,
            "lane": "REAL_GEM_CASE_REVIEW",
            "status": "WAITING_INPUTS",
            "next_pack": "P196B_AFTER_CAPTURE_RESPONSE",
        },
    ]

    blockers: list[str] = []
    if len(migration_rows) != 13:
        blockers.append("TARGET_TAB_MAPPING_COUNT_MISMATCH")
    if SAFETY_FLAGS["apps_script_execution"]:
        blockers.append("UNEXPECTED_APPS_SCRIPT_EXECUTION")
    if SAFETY_FLAGS["clasp_push"]:
        blockers.append("UNEXPECTED_CLASP_PUSH")
    if SAFETY_FLAGS["google_sheets_write"]:
        blockers.append("UNEXPECTED_GOOGLE_SHEETS_WRITE")

    return {
        "STATUS": "OK_P199_APPS_SCRIPT_SHEETS_FUNCTION_TAB_MIGRATION_MAP_READY"
        if not blockers
        else "REVIEW_P199_APPS_SCRIPT_SHEETS_FUNCTION_TAB_MIGRATION_MAP",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "migration_map_status": "READY_READONLY_NO_CLASP_NO_APPS_SCRIPT_EXEC",
        "sheet_tab_count": len(migration_rows),
        "ready_mapping_count": len(ready_rows),
        "python_module_count": len(python_rows),
        "apps_script_source_count": len(apps_rows),
        "migration_map_coverage_percent": coverage,
        "migration_rows": migration_rows,
        "python_module_rows": python_rows,
        "apps_script_source_rows": apps_rows,
        "gate_rows": gate_rows,
        "visual_planning_rows": visual_planning_rows,
        "blocker_count": len(blockers),
        "blockers": blockers,
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


def export_apps_script_sheets_function_tab_migration_map(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P199_APPS_SCRIPT_SHEETS_MIGRATION_MAP_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = build_apps_script_sheets_function_tab_migration_map(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P199_APPS_SCRIPT_SHEETS_FUNCTION_TAB_MIGRATION_MAP.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    _write_csv(
        export_path / "P199_MIGRATION_MAP.csv",
        payload["migration_rows"],
        [
            "priority",
            "sheet_tab",
            "runtime_layer",
            "source_export",
            "python_binding",
            "apps_script_binding",
            "dry_run_status",
            "migration_status",
            "migration_percent",
            "next_action",
        ],
    )

    _write_csv(
        export_path / "P199_PYTHON_MODULES.csv",
        payload["python_module_rows"],
        ["module", "function_count", "functions", "migration_role"],
    )

    _write_csv(
        export_path / "P199_APPS_SCRIPT_SOURCES.csv",
        payload["apps_script_source_rows"],
        [
            "source_path",
            "source_type",
            "function_count",
            "functions",
            "migration_status",
            "next_action",
        ],
    )

    _write_csv(
        export_path / "P199_GATE_ROWS.csv",
        payload["gate_rows"],
        ["gate", "status", "value", "reason"],
    )

    _write_csv(
        export_path / "P199_VISUAL_PLANNING.csv",
        payload["visual_planning_rows"],
        ["step", "lane", "status", "next_pack"],
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "migration_map_status",
        "sheet_tab_count",
        "ready_mapping_count",
        "python_module_count",
        "apps_script_source_count",
        "migration_map_coverage_percent",
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
    (export_path / "P199_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = [
        "# P199 Apps Script / Sheets / Function / Tab Migration Map MAXI",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- migration_map_status: {payload['migration_map_status']}",
        f"- sheet_tab_count: {payload['sheet_tab_count']}",
        f"- ready_mapping_count: {payload['ready_mapping_count']}",
        f"- python_module_count: {payload['python_module_count']}",
        f"- apps_script_source_count: {payload['apps_script_source_count']}",
        f"- migration_map_coverage_percent: {payload['migration_map_coverage_percent']}",
        "",
        "## Visible tools",
        "- /migration",
        "- /sheets-export",
        "- /apps-script-map",
        "",
        "## Safety",
        "- APPS_SCRIPT_EXECUTION=False",
        "- CLASP_PUSH=False",
        "- GOOGLE_SHEETS_WRITE=False",
        "- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False",
        "- GEM_CALL_EXECUTED=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
        "",
        "## Next",
        f"- {payload['recommended_next']}",
    ]
    (export_path / "P199_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    return payload


def _http_ok(url: str) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P199"})
        with urllib.request.urlopen(request, timeout=2.0) as response:
            return 200 <= int(response.status) < 500
    except Exception:
        return False


def run_apps_script_map_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8107,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_apps_script_sheets_function_tab_migration_map(root)

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
        "STATUS": "OK_P199_APPS_SCRIPT_MAP_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P199_APPS_SCRIPT_MAP_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_apps_script_sheets_function_tab_migration_map_with_smoke(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    payload = export_apps_script_sheets_function_tab_migration_map(
        project_root, export_dir=export_dir
    )
    if run_route_smoke:
        smoke = run_apps_script_map_route_smoke(project_root)
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
                "migration_map_status",
                "sheet_tab_count",
                "ready_mapping_count",
                "python_module_count",
                "apps_script_source_count",
                "migration_map_coverage_percent",
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
        (export_path / "P199_SUMMARY.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P199 Apps Script / Sheets migration map.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_apps_script_sheets_function_tab_migration_map_with_smoke(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_apps_script_sheets_function_tab_migration_map(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"SHEET_TAB_COUNT={payload['sheet_tab_count']}")
        print(f"MIGRATION_MAP_STATUS={payload['migration_map_status']}")

    return 0 if payload["sheet_tab_count"] == 13 and not payload["apps_script_execution"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
