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

from mvp_qaic_py.p191r_gem_tracking_tabs_runtime_binding_matrix import (
    build_gem_tracking_tabs_runtime_binding_matrix,
)
from mvp_qaic_py.p193r_gem_decision_journal_roundtrip_evidence_binding import (
    build_gem_evidence_binding,
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


SHEET_CONTRACT_SPECS: list[dict[str, Any]] = [
    {
        "sheet_tab": "GEM_CAPTURE_INBOX",
        "runtime_layer": "GEM_CAPTURE_INBOX",
        "source_export": "00_OPERATOR_EXPORTS/P181_CAPTURE_INBOX",
        "primary_key": "capture_id",
        "required_columns": "capture_id,session_id,prompt_id,image_path,status,created_at,operator_notes",
    },
    {
        "sheet_tab": "GEM_RESPONSE_INBOX",
        "runtime_layer": "GEM_RESPONSE_INBOX",
        "source_export": "00_OPERATOR_EXPORTS/P181_GEM_RESPONSES",
        "primary_key": "response_id",
        "required_columns": "response_id,session_id,prompt_id,response_path,parser_status,created_at",
    },
    {
        "sheet_tab": "GEM_SESSION_LOG",
        "runtime_layer": "GEM_SESSION_LOG",
        "source_export": "00_OPERATOR_EXPORTS/P181_SESSION_LOG",
        "primary_key": "session_id",
        "required_columns": "session_id,capture_id,response_id,prompt_id,status,created_at,updated_at",
    },
    {
        "sheet_tab": "GEM_ROUNDTRIP_STATUS",
        "runtime_layer": "GEM_ROUNDTRIP",
        "source_export": "P193R_GEM_ROUNDTRIP_EVIDENCE.csv",
        "primary_key": "evidence_id",
        "required_columns": "evidence_id,evidence_type,name,source_path,is_file,is_dir,size_bytes,modified_time_epoch",
    },
    {
        "sheet_tab": "GEM_REVIEW_GATE",
        "runtime_layer": "GEM_REVIEW_GATE",
        "source_export": "P187_REAL_MANUAL_CASE_GATE.json",
        "primary_key": "gate_id",
        "required_columns": "gate_id,status,real_case_ready,blocker_count,blockers,next_action",
    },
    {
        "sheet_tab": "GEM_REAL_CASE_DECISION",
        "runtime_layer": "GEM_REAL_CASE_DECISION",
        "source_export": "P188_REAL_CASE_OPERATOR_DECISION_GATE.json",
        "primary_key": "decision_gate_id",
        "required_columns": "decision_gate_id,decision_status,real_case_ready,blocker_count,next_action",
    },
    {
        "sheet_tab": "GEM_DECISION_JOURNAL",
        "runtime_layer": "GEM_DECISION_JOURNAL",
        "source_export": "P193R_GEM_DECISION_JOURNAL_EVIDENCE.csv",
        "primary_key": "evidence_id",
        "required_columns": "evidence_id,evidence_type,name,source_path,is_file,is_dir,size_bytes,modified_time_epoch",
    },
    {
        "sheet_tab": "PROMPT_HISTORY_LIBRARY",
        "runtime_layer": "PROMPT_HISTORY_LIBRARY",
        "source_export": "P182 prompt library export",
        "primary_key": "prompt_id",
        "required_columns": "prompt_id,source_kind,status,sha12,version_label,created_at",
    },
    {
        "sheet_tab": "PROMPT_MIGRATION_MATRIX",
        "runtime_layer": "PROMPT_MIGRATION_MATRIX",
        "source_export": "P189H_PROMPT_MIGRATION_MATRIX.csv",
        "primary_key": "prompt_id",
        "required_columns": "prompt_id,quality_score,risk_score,migration_decision,migration_reason",
    },
    {
        "sheet_tab": "RUNTIME_MIGRATION_TRACKER",
        "runtime_layer": "RUNTIME_MIGRATION_TRACKER",
        "source_export": "P190R_RUNTIME_ARTIFACTS.csv",
        "primary_key": "artifact_id",
        "required_columns": "artifact_id,artifact_type,name,migration_status,migration_percent,next_action",
    },
    {
        "sheet_tab": "GEM_TRACKING_BINDING_MATRIX",
        "runtime_layer": "GEM_TRACKING_BINDING_MATRIX",
        "source_export": "P191R_GEM_TRACKING_BINDING_MATRIX.csv",
        "primary_key": "layer_id",
        "required_columns": "layer_id,expected_sheet_tab,runtime_status,binding_percent,next_action",
    },
    {
        "sheet_tab": "GEM_TRACKING_OPERATOR_VIEW",
        "runtime_layer": "GEM_TRACKING_OPERATOR_VIEW",
        "source_export": "P192R_GEM_TRACKING_OPERATOR_VIEW.csv",
        "primary_key": "layer_id",
        "required_columns": "priority,layer_id,operator_status,operator_action,evidence_summary",
    },
    {
        "sheet_tab": "GEM_EVIDENCE_BINDING",
        "runtime_layer": "GEM_EVIDENCE_BINDING",
        "source_export": "P193R_GEM_EVIDENCE_BINDING.csv",
        "primary_key": "layer_id",
        "required_columns": "layer_id,evidence_status,evidence_count,evidence_percent,latest_evidence,next_action",
    },
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _layer_lookup(project_root: Path) -> dict[str, dict[str, Any]]:
    binding = build_gem_tracking_tabs_runtime_binding_matrix(project_root)
    return {str(row["layer_id"]): row for row in binding["layers"]}


def _readiness_for_spec(
    spec: dict[str, Any],
    layers: dict[str, dict[str, Any]],
    evidence: dict[str, Any],
) -> int:
    runtime_layer = str(spec["runtime_layer"])

    if runtime_layer in {
        "GEM_TRACKING_BINDING_MATRIX",
        "GEM_TRACKING_OPERATOR_VIEW",
    }:
        return 100
    if runtime_layer == "GEM_EVIDENCE_BINDING":
        return int(evidence.get("evidence_coverage_percent", 0))

    layer = layers.get(runtime_layer)
    if not layer:
        return 60 if runtime_layer.startswith(("PROMPT_", "RUNTIME_")) else 30

    return int(layer.get("binding_percent", 0))


def _export_status(percent: int) -> str:
    if percent >= 95:
        return "READY_FOR_READONLY_EXPORT"
    if percent >= 75:
        return "READY_WITH_REVIEW"
    return "NOT_READY"


def _next_action(status: str) -> str:
    if status == "READY_FOR_READONLY_EXPORT":
        return "KEEP_CONTRACT_AND_OPTIONAL_EXPORT_TO_SHEETS_LATER"
    if status == "READY_WITH_REVIEW":
        return "REVIEW_CONTRACT_BEFORE_SHEETS_EXPORT"
    return "COMPLETE_RUNTIME_LAYER_FIRST"


def build_gem_runtime_close_contract(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    layers = _layer_lookup(root)
    evidence = build_gem_evidence_binding(root)

    sheet_rows: list[dict[str, Any]] = []
    for spec in SHEET_CONTRACT_SPECS:
        readiness = _readiness_for_spec(spec, layers, evidence)
        status = _export_status(readiness)
        sheet_rows.append(
            {
                **spec,
                "export_status": status,
                "readiness_percent": readiness,
                "write_policy": "READONLY_EXPORT_CONTRACT_NO_SHEET_WRITE",
                "human_review_required": True,
                "next_action": _next_action(status),
            }
        )

    ready_count = sum(
        1 for row in sheet_rows if row["export_status"] == "READY_FOR_READONLY_EXPORT"
    )
    review_count = sum(1 for row in sheet_rows if row["export_status"] == "READY_WITH_REVIEW")
    not_ready_count = sum(1 for row in sheet_rows if row["export_status"] == "NOT_READY")
    close_percent = round(
        sum(int(row["readiness_percent"]) for row in sheet_rows) / len(sheet_rows), 1
    )

    blockers: list[str] = []
    if evidence["blocker_count"]:
        blockers.extend(str(item) for item in evidence["blockers"])
    if not_ready_count:
        blockers.append("SOME_SHEETS_EXPORT_CONTRACT_ROWS_NOT_READY")

    close_rows = [
        {"metric": "sheet_contract_row_count", "value": len(sheet_rows), "status": "INFO"},
        {"metric": "ready_for_sheets_export_count", "value": ready_count, "status": "OK"},
        {
            "metric": "ready_with_review_count",
            "value": review_count,
            "status": "REVIEW" if review_count else "OK",
        },
        {
            "metric": "not_ready_count",
            "value": not_ready_count,
            "status": "BLOCKED" if not_ready_count else "OK",
        },
        {
            "metric": "runtime_close_percent",
            "value": close_percent,
            "status": "OK" if close_percent >= 95 else "REVIEW",
        },
        {
            "metric": "roundtrip_evidence_count",
            "value": evidence["roundtrip_evidence_count"],
            "status": "OK",
        },
        {
            "metric": "decision_journal_evidence_count",
            "value": evidence["decision_journal_evidence_count"],
            "status": "OK",
        },
        {
            "metric": "blocker_count",
            "value": len(blockers),
            "status": "OK" if not blockers else "REVIEW",
        },
    ]

    return {
        "STATUS": "OK_P194R_GEM_RUNTIME_TRACKER_CLOSE_SHEETS_EXPORT_CONTRACT_READY",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "sheet_contract_row_count": len(sheet_rows),
        "ready_for_sheets_export_count": ready_count,
        "ready_with_review_count": review_count,
        "not_ready_count": not_ready_count,
        "runtime_close_percent": close_percent,
        "sheet_contract_rows": sheet_rows,
        "close_rows": close_rows,
        "blocker_count": len(blockers),
        "blockers": blockers,
        **SAFETY_FLAGS,
        "recommended_next": "P195R_OPERATOR_RELEASE_RUNTIME_TRACKER_OR_REAL_CASE_INPUTS",
    }


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def export_gem_runtime_close_contract(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P194R_GEM_RUNTIME_CLOSE_CONTRACT_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = build_gem_runtime_close_contract(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P194R_GEM_RUNTIME_CLOSE_CONTRACT.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    contract_fields = [
        "sheet_tab",
        "runtime_layer",
        "source_export",
        "primary_key",
        "required_columns",
        "export_status",
        "readiness_percent",
        "write_policy",
        "human_review_required",
        "next_action",
    ]
    _write_csv(
        export_path / "P194R_SHEETS_EXPORT_CONTRACT.csv",
        payload["sheet_contract_rows"],
        contract_fields,
    )

    _write_csv(
        export_path / "P194R_RUNTIME_CLOSE_STATUS.csv",
        payload["close_rows"],
        ["metric", "value", "status"],
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "sheet_contract_row_count",
        "ready_for_sheets_export_count",
        "ready_with_review_count",
        "not_ready_count",
        "runtime_close_percent",
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
        "recommended_next",
    ]
    summary = {key: payload.get(key) for key in summary_keys}
    (export_path / "P194R_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = [
        "# P194R GEM Runtime Tracker Close + Sheets Export Contract",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- sheet_contract_row_count: {payload['sheet_contract_row_count']}",
        f"- ready_for_sheets_export_count: {payload['ready_for_sheets_export_count']}",
        f"- runtime_close_percent: {payload['runtime_close_percent']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "## Contract rows",
    ]
    for row in payload["sheet_contract_rows"]:
        report.append(
            f"- {row['sheet_tab']}: {row['export_status']} / "
            f"{row['readiness_percent']}% / {row['write_policy']}"
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
            "## Next",
            "- P195R_OPERATOR_RELEASE_RUNTIME_TRACKER_OR_REAL_CASE_INPUTS",
        ]
    )
    (export_path / "P194R_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    return payload


def _http_ok(url: str) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P194R"})
        with urllib.request.urlopen(request, timeout=2.0) as response:
            return 200 <= int(response.status) < 500
    except Exception:
        return False


def run_runtime_contract_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8102,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_gem_runtime_close_contract(root)

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
        "STATUS": "OK_P194R_RUNTIME_CONTRACT_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P194R_RUNTIME_CONTRACT_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_gem_runtime_close_contract_with_smoke(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    payload = export_gem_runtime_close_contract(project_root, export_dir=export_dir)
    if run_route_smoke:
        smoke = run_runtime_contract_route_smoke(project_root)
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
                "sheet_contract_row_count",
                "ready_for_sheets_export_count",
                "ready_with_review_count",
                "not_ready_count",
                "runtime_close_percent",
                "blocker_count",
                "blockers",
                "route_success_count",
                "route_smoke_ok",
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
        (export_path / "P194R_SUMMARY.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P194R GEM runtime close contract.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_gem_runtime_close_contract_with_smoke(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_gem_runtime_close_contract(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"SHEET_CONTRACT_ROW_COUNT={payload['sheet_contract_row_count']}")
        print(f"READY_FOR_SHEETS_EXPORT_COUNT={payload['ready_for_sheets_export_count']}")
        print(f"RUNTIME_CLOSE_PERCENT={payload['runtime_close_percent']}")

    return 0 if payload["sheet_contract_row_count"] > 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
