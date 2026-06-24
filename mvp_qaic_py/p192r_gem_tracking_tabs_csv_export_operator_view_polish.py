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


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _operator_status(runtime_status: str) -> str:
    if runtime_status == "BOUND_RUNTIME_VISIBLE":
        return "OK_READY"
    if runtime_status == "BOUND_PARTIAL":
        return "REVIEW_EVIDENCE_TO_COMPLETE"
    if runtime_status == "DISCOVERED_NEEDS_BINDING":
        return "BINDING_REQUIRED"
    return "NOT_READY"


def _operator_action(layer: dict[str, Any]) -> str:
    layer_id = str(layer["layer_id"])
    runtime_status = str(layer["runtime_status"])

    if runtime_status == "BOUND_RUNTIME_VISIBLE":
        return "KEEP_TRACKING"

    if layer_id == "GEM_ROUNDTRIP":
        return "ADD_ROUNDTRIP_STATUS_EXPORT_OR_BIND_EXISTING_EVIDENCE"

    if layer_id == "GEM_DECISION_JOURNAL":
        return "ADD_DECISION_JOURNAL_RUNTIME_EXPORT_OR_BIND_LOCAL_JOURNAL"

    return str(layer.get("next_action") or "REVIEW")


def _priority(layer: dict[str, Any]) -> int:
    status = _operator_status(str(layer["runtime_status"]))
    if status == "NOT_READY":
        return 1
    if status == "BINDING_REQUIRED":
        return 2
    if status == "REVIEW_EVIDENCE_TO_COMPLETE":
        return 3
    return 9


def _evidence_summary(layer: dict[str, Any]) -> str:
    return (
        f"path_exists={layer['source_exists']}; "
        f"files={layer['local_file_count']}; "
        f"route={layer['route_bound']}; "
        f"handler={layer['handler_status']}; "
        f"binding={layer['binding_percent']}%"
    )


def build_gem_tracking_operator_view(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    base = build_gem_tracking_tabs_runtime_binding_matrix(root)

    operator_rows: list[dict[str, Any]] = []
    for layer in base["layers"]:
        row = {
            "priority": _priority(layer),
            "layer_id": layer["layer_id"],
            "expected_sheet_tab": layer["expected_sheet_tab"],
            "operator_status": _operator_status(str(layer["runtime_status"])),
            "runtime_status": layer["runtime_status"],
            "binding_percent": layer["binding_percent"],
            "operator_action": _operator_action(layer),
            "local_path": layer["local_path"],
            "nicegui_route": layer["nicegui_route"],
            "python_handler": layer["python_handler"],
            "evidence_summary": _evidence_summary(layer),
            "purpose": layer["purpose"],
        }
        operator_rows.append(row)

    operator_rows.sort(
        key=lambda row: (
            int(row["priority"]),
            -int(row["binding_percent"]),
            str(row["layer_id"]),
        )
    )

    ready_count = sum(1 for row in operator_rows if row["operator_status"] == "OK_READY")
    review_count = sum(1 for row in operator_rows if row["operator_status"] != "OK_READY")
    coverage = round(
        sum(int(row["binding_percent"]) for row in operator_rows) / len(operator_rows),
        1,
    )

    export_rows = [
        {
            "export_name": "P192R_GEM_TRACKING_OPERATOR_VIEW.csv",
            "purpose": "Vue opérateur priorisée avec actions suivantes.",
            "status": "PLANNED",
        },
        {
            "export_name": "P192R_GEM_TRACKING_LAYER_STATUS.csv",
            "purpose": "Statuts runtime détaillés par couche GEM.",
            "status": "PLANNED",
        },
        {
            "export_name": "P192R_GEM_TRACKING_ACTIONS.csv",
            "purpose": "Actions restantes pour finaliser les couches partielles.",
            "status": "PLANNED",
        },
    ]

    blockers: list[str] = []
    if not any(row["layer_id"] == "GEM_DECISION_JOURNAL" for row in operator_rows):
        blockers.append("GEM_DECISION_JOURNAL_LAYER_MISSING")
    if not any(row["layer_id"] == "GEM_ROUNDTRIP" for row in operator_rows):
        blockers.append("GEM_ROUNDTRIP_LAYER_MISSING")

    return {
        "STATUS": "OK_P192R_GEM_TRACKING_OPERATOR_VIEW_READY",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "layer_count": len(operator_rows),
        "ready_count": ready_count,
        "review_count": review_count,
        "operator_coverage_percent": coverage,
        "operator_rows": operator_rows,
        "export_rows": export_rows,
        "base_binding_coverage_percent": base["binding_coverage_percent"],
        "base_blocker_count": base["blocker_count"],
        "base_blockers": base["blockers"],
        "blocker_count": len(blockers),
        "blockers": blockers,
        **SAFETY_FLAGS,
        "recommended_next": "P193R_GEM_DECISION_JOURNAL_AND_ROUNDTRIP_EVIDENCE_BINDING",
    }


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fieldnames})


def export_gem_tracking_operator_view(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P192R_GEM_TRACKING_OPERATOR_VIEW_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = build_gem_tracking_operator_view(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P192R_GEM_TRACKING_OPERATOR_VIEW.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    operator_fields = [
        "priority",
        "layer_id",
        "expected_sheet_tab",
        "operator_status",
        "runtime_status",
        "binding_percent",
        "operator_action",
        "local_path",
        "nicegui_route",
        "python_handler",
        "evidence_summary",
        "purpose",
    ]
    _write_csv(
        export_path / "P192R_GEM_TRACKING_OPERATOR_VIEW.csv",
        payload["operator_rows"],
        operator_fields,
    )

    status_fields = [
        "layer_id",
        "operator_status",
        "runtime_status",
        "binding_percent",
        "expected_sheet_tab",
        "local_path",
        "nicegui_route",
        "python_handler",
        "evidence_summary",
    ]
    _write_csv(
        export_path / "P192R_GEM_TRACKING_LAYER_STATUS.csv",
        payload["operator_rows"],
        status_fields,
    )

    actions = [row for row in payload["operator_rows"] if row["operator_status"] != "OK_READY"]
    _write_csv(
        export_path / "P192R_GEM_TRACKING_ACTIONS.csv",
        actions,
        operator_fields,
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "layer_count",
        "ready_count",
        "review_count",
        "operator_coverage_percent",
        "base_binding_coverage_percent",
        "base_blocker_count",
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
    (export_path / "P192R_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = [
        "# P192R GEM Tracking CSV Export + Operator View Polish",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- layer_count: {payload['layer_count']}",
        f"- ready_count: {payload['ready_count']}",
        f"- review_count: {payload['review_count']}",
        f"- operator_coverage_percent: {payload['operator_coverage_percent']}",
        "",
        "## Actions restantes",
    ]
    for row in actions:
        report.append(
            f"- {row['layer_id']}: {row['operator_status']} / "
            f"{row['operator_action']} / {row['evidence_summary']}"
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
            "- P193R_GEM_DECISION_JOURNAL_AND_ROUNDTRIP_EVIDENCE_BINDING",
        ]
    )
    (export_path / "P192R_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    return payload


def _http_ok(url: str) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P192R"})
        with urllib.request.urlopen(request, timeout=2.0) as response:
            return 200 <= int(response.status) < 500
    except Exception:
        return False


def run_operator_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8100,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_gem_tracking_operator_view(root)

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
        "STATUS": "OK_P192R_GEM_TRACKING_OPERATOR_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P192R_GEM_TRACKING_OPERATOR_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_gem_tracking_operator_view_with_smoke(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    payload = export_gem_tracking_operator_view(project_root, export_dir=export_dir)
    if run_route_smoke:
        smoke = run_operator_route_smoke(project_root)
        payload.update(
            {
                "route_results": smoke["route_results"],
                "route_success_count": smoke["route_success_count"],
                "route_smoke_ok": smoke["route_smoke_ok"],
                "server_started_by_smoke": smoke["server_started_by_smoke"],
                "server_stopped_after_smoke": smoke["server_stopped_after_smoke"],
                "STATUS": smoke["STATUS"],
            }
        )
        export_path = Path(payload["export_dir"])
        (export_path / "P192R_SUMMARY.json").write_text(
            json.dumps(
                {
                    key: payload.get(key)
                    for key in [
                        "STATUS",
                        "generated_at",
                        "project_root",
                        "export_dir",
                        "layer_count",
                        "ready_count",
                        "review_count",
                        "operator_coverage_percent",
                        "base_binding_coverage_percent",
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
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P192R GEM tracking operator view polish.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_gem_tracking_operator_view_with_smoke(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_gem_tracking_operator_view(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"LAYER_COUNT={payload['layer_count']}")
        print(f"READY_COUNT={payload['ready_count']}")
        print(f"REVIEW_COUNT={payload['review_count']}")

    return 0 if payload["layer_count"] > 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
