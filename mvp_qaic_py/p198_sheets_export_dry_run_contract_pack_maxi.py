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

from mvp_qaic_py.p194r_gem_runtime_tracker_close_sheets_export_contract import (
    build_gem_runtime_close_contract,
)
from mvp_qaic_py.p197_prompt_master_from_historical_audit_and_regression_maxi import (
    build_prompt_master_historical_regression,
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


def _safe_rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _estimate_rows_from_path(root: Path, source_export: str) -> int:
    source = str(source_export)
    candidates: list[Path] = []

    if source.endswith(".csv") or source.endswith(".json") or source.endswith(".md"):
        candidates.extend((root / "05_EXPORTS").rglob(Path(source).name)) if (
            root / "05_EXPORTS"
        ).exists() else None
    elif source.startswith("00_OPERATOR_EXPORTS"):
        path = root / source
        if path.exists():
            if path.is_dir():
                candidates.extend(
                    [
                        item
                        for item in path.rglob("*")
                        if item.is_file() and item.name.lower() != "desktop.ini"
                    ]
                )
            else:
                candidates.append(path)

    if not candidates:
        return 0

    total = 0
    for path in candidates[:20]:
        if path.suffix.lower() == ".csv":
            try:
                total += max(
                    0, len(path.read_text(encoding="utf-8", errors="replace").splitlines()) - 1
                )
            except Exception:
                total += 1
        elif path.is_file():
            total += 1
    return total


def _status_from_contract(row: dict[str, Any], estimated_rows: int) -> str:
    export_status = str(row.get("export_status", ""))
    if export_status == "READY_FOR_READONLY_EXPORT":
        return "DRY_RUN_READY"
    if export_status == "READY_WITH_REVIEW":
        return "DRY_RUN_READY_WITH_REVIEW"
    if estimated_rows > 0:
        return "DRY_RUN_DATA_FOUND_BUT_CONTRACT_REVIEW"
    return "DRY_RUN_WAITING_SOURCE"


def _next_action(status: str) -> str:
    if status == "DRY_RUN_READY":
        return "KEEP_DRY_RUN_ONLY_PREPARE_HUMAN_VALIDATION"
    if status == "DRY_RUN_READY_WITH_REVIEW":
        return "REVIEW_COLUMNS_BEFORE_ANY_LIVE_WRITE"
    if status == "DRY_RUN_DATA_FOUND_BUT_CONTRACT_REVIEW":
        return "VALIDATE_CONTRACT_MAPPING"
    return "WAIT_FOR_SOURCE_OR_BIND_EXPORT"


def build_sheets_export_dry_run_contract_pack(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    runtime_contract = build_gem_runtime_close_contract(root)
    prompt_master = build_prompt_master_historical_regression(root)

    target_rows: list[dict[str, Any]] = []
    for index, row in enumerate(runtime_contract["sheet_contract_rows"], start=1):
        estimated_rows = _estimate_rows_from_path(root, str(row.get("source_export", "")))
        dry_status = _status_from_contract(row, estimated_rows)
        target_rows.append(
            {
                "priority": index,
                "sheet_tab": row["sheet_tab"],
                "runtime_layer": row["runtime_layer"],
                "source_export": row["source_export"],
                "primary_key": row["primary_key"],
                "required_columns": row["required_columns"],
                "runtime_export_status": row["export_status"],
                "readiness_percent": row["readiness_percent"],
                "estimated_rows": estimated_rows,
                "dry_run_status": dry_status,
                "write_policy": "DRY_RUN_ONLY_NO_GOOGLE_SHEETS_WRITE",
                "human_review_required": True,
                "next_action": _next_action(dry_status),
            }
        )

    ready_count = sum(1 for row in target_rows if row["dry_run_status"] == "DRY_RUN_READY")
    review_count = sum(1 for row in target_rows if "REVIEW" in row["dry_run_status"])
    waiting_count = sum(
        1 for row in target_rows if row["dry_run_status"] == "DRY_RUN_WAITING_SOURCE"
    )
    coverage = round(
        sum(int(row["readiness_percent"]) for row in target_rows) / len(target_rows), 1
    )

    gates = [
        {
            "gate": "NO_GOOGLE_SHEETS_WRITE",
            "status": "PASS",
            "value": "False",
            "reason": "P198 creates payloads and contracts only.",
        },
        {
            "gate": "TARGET_TAB_CONTRACT_COUNT",
            "status": "PASS" if len(target_rows) == 13 else "FAIL",
            "value": str(len(target_rows)),
            "reason": "Expected 13 target tabs from P194 runtime contract.",
        },
        {
            "gate": "RUNTIME_CLOSE_PERCENT",
            "status": "PASS"
            if float(runtime_contract["runtime_close_percent"]) >= 95
            else "REVIEW",
            "value": str(runtime_contract["runtime_close_percent"]),
            "reason": "Runtime close must be high before dry-run export.",
        },
        {
            "gate": "PROMPT_MASTER_READY",
            "status": "PASS" if prompt_master["candidate_count"] > 0 else "REVIEW",
            "value": str(prompt_master["candidate_count"]),
            "reason": "Prompt master candidates available for future prompt tabs.",
        },
        {
            "gate": "LIVE_WRITE_AUTHORIZATION",
            "status": "BLOCKED_BY_POLICY",
            "value": "False",
            "reason": "No live Sheets write until explicit human authorization in a later batch.",
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
            "lane": "GEM_RUNTIME_TRACKING",
            "status": "VISIBLE_NOW",
            "next_pack": "OPEN_/gem-tracking",
        },
        {"step": 3, "lane": "SHEETS_EXPORT_DRY_RUN", "status": "THIS_BATCH", "next_pack": "P198"},
        {
            "step": 4,
            "lane": "APPS_SCRIPT_SHEETS_MIGRATION_MAP",
            "status": "NEXT_MAXI",
            "next_pack": "P199",
        },
        {"step": 5, "lane": "FINAL_OPERATOR_RELEASE", "status": "NEXT_MAXI", "next_pack": "P200"},
        {
            "step": 6,
            "lane": "REAL_GEM_CASE_REVIEW",
            "status": "WAITING_INPUTS",
            "next_pack": "P196B_AFTER_CAPTURE_RESPONSE",
        },
    ]

    blockers: list[str] = []
    if len(target_rows) != 13:
        blockers.append("TARGET_TAB_CONTRACT_COUNT_MISMATCH")
    if float(runtime_contract["runtime_close_percent"]) < 95:
        blockers.append("RUNTIME_CLOSE_BELOW_95")
    if SAFETY_FLAGS["google_sheets_write"]:
        blockers.append("UNEXPECTED_GOOGLE_SHEETS_WRITE")

    return {
        "STATUS": "OK_P198_SHEETS_EXPORT_DRY_RUN_CONTRACT_PACK_READY"
        if not blockers
        else "REVIEW_P198_SHEETS_EXPORT_DRY_RUN_CONTRACT_PACK",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "dry_run_status": "READY_DRY_RUN_ONLY_NO_LIVE_WRITE",
        "target_tab_count": len(target_rows),
        "ready_tab_count": ready_count,
        "review_tab_count": review_count,
        "waiting_tab_count": waiting_count,
        "dry_run_coverage_percent": coverage,
        "runtime_close_percent": runtime_contract["runtime_close_percent"],
        "prompt_candidate_count": prompt_master["candidate_count"],
        "target_tab_rows": target_rows,
        "gate_rows": gates,
        "visual_planning_rows": visual_planning_rows,
        "blocker_count": len(blockers),
        "blockers": blockers,
        **SAFETY_FLAGS,
        "recommended_next": "P199_APPS_SCRIPT_SHEETS_FUNCTION_TAB_MIGRATION_MAP_MAXI",
        "parallel_waiting_next": "P196B_REAL_CASE_PORTFOLIO_GEM_REVIEW_AFTER_OPERATOR_INPUTS_MAXI_AFTER_INPUTS",
    }


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def export_sheets_export_dry_run_contract_pack(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P198_SHEETS_EXPORT_DRY_RUN_CONTRACT_PACK_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = build_sheets_export_dry_run_contract_pack(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P198_SHEETS_EXPORT_DRY_RUN_CONTRACT_PACK.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    tab_fields = [
        "priority",
        "sheet_tab",
        "runtime_layer",
        "source_export",
        "primary_key",
        "required_columns",
        "runtime_export_status",
        "readiness_percent",
        "estimated_rows",
        "dry_run_status",
        "write_policy",
        "human_review_required",
        "next_action",
    ]
    _write_csv(
        export_path / "P198_TARGET_SHEET_TABS_DRY_RUN.csv", payload["target_tab_rows"], tab_fields
    )
    _write_csv(
        export_path / "P198_EXPORT_GATES.csv",
        payload["gate_rows"],
        ["gate", "status", "value", "reason"],
    )
    _write_csv(
        export_path / "P198_VISUAL_PLANNING.csv",
        payload["visual_planning_rows"],
        ["step", "lane", "status", "next_pack"],
    )

    dry_payload = {
        "mode": "DRY_RUN_ONLY_NO_GOOGLE_SHEETS_WRITE",
        "created_at": payload["generated_at"],
        "target_tabs": payload["target_tab_rows"],
        "write_allowed": False,
        "human_review_required": True,
        "safety_flags": SAFETY_FLAGS,
    }
    (export_path / "P198_DRY_RUN_WRITE_PAYLOAD.json").write_text(
        json.dumps(dry_payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "dry_run_status",
        "target_tab_count",
        "ready_tab_count",
        "review_tab_count",
        "waiting_tab_count",
        "dry_run_coverage_percent",
        "runtime_close_percent",
        "prompt_candidate_count",
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
    (export_path / "P198_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = [
        "# P198 Sheets Export Dry-Run Contract Pack MAXI",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- dry_run_status: {payload['dry_run_status']}",
        f"- target_tab_count: {payload['target_tab_count']}",
        f"- ready_tab_count: {payload['ready_tab_count']}",
        f"- dry_run_coverage_percent: {payload['dry_run_coverage_percent']}",
        f"- recommended_next: {payload['recommended_next']}",
        "",
        "## Visible tools",
        "- /migration: suivi dev migration",
        "- /gem-tracking: suivi couches GEM",
        "- /runtime-contract: contrat runtime",
        "- /sheets-export: dry-run Sheets",
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
    (export_path / "P198_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    return payload


def _http_ok(url: str) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P198"})
        with urllib.request.urlopen(request, timeout=2.0) as response:
            return 200 <= int(response.status) < 500
    except Exception:
        return False


def run_sheets_export_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8106,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_sheets_export_dry_run_contract_pack(root)

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
        "STATUS": "OK_P198_SHEETS_EXPORT_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P198_SHEETS_EXPORT_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_sheets_export_dry_run_contract_pack_with_smoke(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    payload = export_sheets_export_dry_run_contract_pack(project_root, export_dir=export_dir)
    if run_route_smoke:
        smoke = run_sheets_export_route_smoke(project_root)
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
                "dry_run_status",
                "target_tab_count",
                "ready_tab_count",
                "review_tab_count",
                "waiting_tab_count",
                "dry_run_coverage_percent",
                "runtime_close_percent",
                "prompt_candidate_count",
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
        (export_path / "P198_SUMMARY.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P198 Sheets export dry-run contract pack.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_sheets_export_dry_run_contract_pack_with_smoke(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_sheets_export_dry_run_contract_pack(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"TARGET_TAB_COUNT={payload['target_tab_count']}")
        print(f"DRY_RUN_STATUS={payload['dry_run_status']}")

    return 0 if payload["target_tab_count"] == 13 and not payload["google_sheets_write"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
