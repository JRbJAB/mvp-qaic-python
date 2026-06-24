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
}


REVIEW_WAIVERS: list[dict[str, str]] = [
    {
        "waiver_id": "ROUNDTRIP_STATUS_REVIEW_ACCEPTED",
        "scope": "GEM_ROUNDTRIP_STATUS",
        "reason": "Evidence exists and route/runtime are usable; Sheets export contract remains human-review only.",
        "policy": "ALLOW_OPERATOR_RELEASE_DO_NOT_WRITE_SHEETS",
    },
    {
        "waiver_id": "DECISION_JOURNAL_CONTRACT_DEFERRED",
        "scope": "GEM_DECISION_JOURNAL",
        "reason": "Decision evidence exists but future tab schema needs human validation before any Sheet write.",
        "policy": "ALLOW_OPERATOR_RELEASE_BLOCK_LIVE_SHEETS_WRITE",
    },
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _gate(gate: str, status: str, value: str, reason: str) -> dict[str, str]:
    return {"gate": gate, "status": status, "value": value, "reason": reason}


def _next_work_rows(runtime_close_percent: float) -> list[dict[str, Any]]:
    rows = [
        {
            "priority": 1,
            "workstream": "REAL_CASE_PORTFOLIO_GEM",
            "status": "READY_WAITING_INPUTS",
            "next_pack": "P196_REAL_CASE_PORTFOLIO_GEM_OPERATOR_INPUTS_MAXI",
            "reason": "Runtime UI, capture/response/session/review layers are ready. Needs real capture + real GEM response.",
        },
        {
            "priority": 2,
            "workstream": "PROMPT_HISTORICAL_MASTER",
            "status": "READY_FOR_MAXI_BATCH",
            "next_pack": "P197_PROMPT_MASTER_FROM_HISTORICAL_AUDIT_AND_REGRESSION_MAXI",
            "reason": "Historical prompt inventory/audit exists; next is master candidate + regression, not micro review.",
        },
        {
            "priority": 3,
            "workstream": "SHEETS_EXPORT_DRY_RUN",
            "status": "READY_READONLY_CONTRACT_ONLY",
            "next_pack": "P198_SHEETS_EXPORT_DRY_RUN_CONTRACT_PACK_MAXI",
            "reason": f"Runtime close at {runtime_close_percent}%; live Sheet write stays blocked until human validation.",
        },
        {
            "priority": 4,
            "workstream": "APPS_SCRIPT_SHEETS_MIGRATION_MAP",
            "status": "READY_FOR_AUDIT_MAXI",
            "next_pack": "P199_APPS_SCRIPT_SHEETS_FUNCTION_TAB_MIGRATION_MAP_MAXI",
            "reason": "Runtime tracker exists; remaining migration map can be grouped by tabs/scripts/functions.",
        },
    ]
    return rows


def build_operator_release_runtime_tracker(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    contract = build_gem_runtime_close_contract(root)
    runtime_close_percent = float(contract["runtime_close_percent"])

    release_ready = (
        runtime_close_percent >= 95
        and int(contract["sheet_contract_row_count"]) == 13
        and bool(contract["ready_for_sheets_export_count"])
        and not SAFETY_FLAGS["google_sheets_write"]
        and not SAFETY_FLAGS["gem_call_executed"]
        and not SAFETY_FLAGS["broker"]
        and not SAFETY_FLAGS["order"]
        and not SAFETY_FLAGS["sizing"]
    )

    operator_release_status = (
        "READY_WITH_REVIEW_WAIVERS" if release_ready else "BLOCKED_OPERATOR_RELEASE"
    )

    release_gate_rows = [
        _gate(
            "runtime_close_percent",
            "PASS" if runtime_close_percent >= 95 else "REVIEW",
            str(runtime_close_percent),
            "Runtime GEM coverage is high enough for operator release.",
        ),
        _gate(
            "sheets_contract_rows",
            "PASS" if int(contract["sheet_contract_row_count"]) == 13 else "FAIL",
            str(contract["sheet_contract_row_count"]),
            "All expected future Sheets tabs are represented in the contract.",
        ),
        _gate(
            "review_waivers",
            "PASS",
            str(len(REVIEW_WAIVERS)),
            "Waivers allow operator runtime release but do not allow live Sheet write.",
        ),
        _gate(
            "live_sheet_write",
            "PASS",
            "False",
            "All Sheets integration remains read-only/contract-only.",
        ),
        _gate(
            "gem_call",
            "PASS",
            "False",
            "No GEM call executed from Python.",
        ),
        _gate(
            "broker_order_sizing",
            "PASS",
            "False",
            "No broker/order/sizing path enabled.",
        ),
    ]

    blockers: list[str] = []
    if not release_ready:
        blockers.append("OPERATOR_RELEASE_NOT_READY")
    if int(contract["not_ready_count"]) > 1:
        blockers.append("TOO_MANY_NOT_READY_CONTRACT_ROWS")

    next_rows = _next_work_rows(runtime_close_percent)

    return {
        "STATUS": "OK_P195R_OPERATOR_RELEASE_RUNTIME_TRACKER_READY"
        if not blockers
        else "REVIEW_P195R_OPERATOR_RELEASE_RUNTIME_TRACKER",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "operator_release_status": operator_release_status,
        "runtime_close_percent": runtime_close_percent,
        "sheet_contract_row_count": contract["sheet_contract_row_count"],
        "ready_for_sheets_export_count": contract["ready_for_sheets_export_count"],
        "ready_with_review_count": contract["ready_with_review_count"],
        "not_ready_count": contract["not_ready_count"],
        "review_waiver_count": len(REVIEW_WAIVERS),
        "review_waivers": REVIEW_WAIVERS,
        "release_gate_rows": release_gate_rows,
        "next_work_rows": next_rows,
        "selected_next_pack": next_rows[0]["next_pack"],
        "expected_route_count": len(ROUTES),
        "blocker_count": len(blockers),
        "blockers": blockers,
        "sheets_export_allowed": False,
        "operator_runtime_release_allowed": release_ready,
        **SAFETY_FLAGS,
        "recommended_next": next_rows[0]["next_pack"],
    }


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def export_operator_release_runtime_tracker(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P195R_OPERATOR_RELEASE_RUNTIME_TRACKER_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = build_operator_release_runtime_tracker(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P195R_OPERATOR_RELEASE_RUNTIME_TRACKER.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    _write_csv(
        export_path / "P195R_RELEASE_GATES.csv",
        payload["release_gate_rows"],
        ["gate", "status", "value", "reason"],
    )

    _write_csv(
        export_path / "P195R_NEXT_WORK_SELECTOR.csv",
        payload["next_work_rows"],
        ["priority", "workstream", "status", "next_pack", "reason"],
    )

    _write_csv(
        export_path / "P195R_REVIEW_WAIVERS.csv",
        payload["review_waivers"],
        ["waiver_id", "scope", "reason", "policy"],
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "operator_release_status",
        "runtime_close_percent",
        "sheet_contract_row_count",
        "ready_for_sheets_export_count",
        "ready_with_review_count",
        "not_ready_count",
        "review_waiver_count",
        "selected_next_pack",
        "expected_route_count",
        "blocker_count",
        "blockers",
        "sheets_export_allowed",
        "operator_runtime_release_allowed",
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
        "recommended_next",
    ]
    summary = {key: payload.get(key) for key in summary_keys}
    (export_path / "P195R_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = [
        "# P195R Operator Release Runtime Tracker + Next Work Selector MAXI",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- operator_release_status: {payload['operator_release_status']}",
        f"- runtime_close_percent: {payload['runtime_close_percent']}",
        f"- selected_next_pack: {payload['selected_next_pack']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "## Release gates",
    ]
    for row in payload["release_gate_rows"]:
        report.append(f"- {row['gate']}: {row['status']} / {row['value']} / {row['reason']}")

    report.extend(["", "## Next work selector"])
    for row in payload["next_work_rows"]:
        report.append(
            f"- P{row['priority']} {row['workstream']}: {row['status']} -> {row['next_pack']}"
        )

    report.extend(
        [
            "",
            "## Safety",
            "- GEM_CALL_EXECUTED=False",
            "- GOOGLE_SHEETS_WRITE=False",
            "- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False",
            "- APPS_SCRIPT_EXECUTION=False",
            "- CLASP_PUSH=False",
            "- PUBLIC_SERVE=False",
            "- BROKER=False",
            "- ORDER=False",
            "- SIZING=False",
            "",
            "## Selected next",
            f"- {payload['selected_next_pack']}",
        ]
    )
    (export_path / "P195R_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    return payload


def _http_ok(url: str) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P195R"})
        with urllib.request.urlopen(request, timeout=2.0) as response:
            return 200 <= int(response.status) < 500
    except Exception:
        return False


def run_operator_release_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8103,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_operator_release_runtime_tracker(root)

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
        "STATUS": "OK_P195R_OPERATOR_RELEASE_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P195R_OPERATOR_RELEASE_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_operator_release_runtime_tracker_with_smoke(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    payload = export_operator_release_runtime_tracker(project_root, export_dir=export_dir)
    if run_route_smoke:
        smoke = run_operator_release_route_smoke(project_root)
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
                "operator_release_status",
                "runtime_close_percent",
                "sheet_contract_row_count",
                "ready_for_sheets_export_count",
                "ready_with_review_count",
                "not_ready_count",
                "review_waiver_count",
                "selected_next_pack",
                "expected_route_count",
                "route_success_count",
                "route_smoke_ok",
                "blocker_count",
                "blockers",
                "sheets_export_allowed",
                "operator_runtime_release_allowed",
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
                "recommended_next",
            ]
        }
        (export_path / "P195R_SUMMARY.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P195R operator release runtime tracker.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_operator_release_runtime_tracker_with_smoke(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_operator_release_runtime_tracker(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"OPERATOR_RELEASE_STATUS={payload['operator_release_status']}")
        print(f"SELECTED_NEXT_PACK={payload['selected_next_pack']}")

    return 0 if payload["operator_runtime_release_allowed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
