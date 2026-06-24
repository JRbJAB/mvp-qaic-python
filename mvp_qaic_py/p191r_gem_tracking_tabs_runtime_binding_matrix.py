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


EXPECTED_LAYERS: list[dict[str, str]] = [
    {
        "layer_id": "GEM_CAPTURE_INBOX",
        "expected_sheet_tab": "GEM_CAPTURE_INBOX",
        "local_path": "00_OPERATOR_EXPORTS/P181_CAPTURE_INBOX",
        "python_handler": "p181/p183 capture workflow",
        "nicegui_route": "/capture",
        "purpose": "Stocker les captures portfolio à traiter.",
    },
    {
        "layer_id": "GEM_RESPONSE_INBOX",
        "expected_sheet_tab": "GEM_RESPONSE_INBOX",
        "local_path": "00_OPERATOR_EXPORTS/P181_GEM_RESPONSES",
        "python_handler": "p184 parser",
        "nicegui_route": "/responses",
        "purpose": "Stocker les réponses GEM collées localement.",
    },
    {
        "layer_id": "GEM_SESSION_LOG",
        "expected_sheet_tab": "GEM_SESSION_LOG",
        "local_path": "00_OPERATOR_EXPORTS/P181_SESSION_LOG",
        "python_handler": "p183 session linker",
        "nicegui_route": "/sessions",
        "purpose": "Relier capture, prompt, réponse et session.",
    },
    {
        "layer_id": "GEM_ROUNDTRIP",
        "expected_sheet_tab": "GEM_ROUNDTRIP_STATUS",
        "local_path": "05_EXPORTS",
        "python_handler": "p185/p186 roundtrip",
        "nicegui_route": "/roundtrip",
        "purpose": "Valider le cycle capture → prompt → réponse → review.",
    },
    {
        "layer_id": "GEM_REVIEW_GATE",
        "expected_sheet_tab": "GEM_REVIEW_GATE",
        "local_path": "mvp_qaic_py/p187_real_manual_portfolio_case_review_gate.py",
        "python_handler": "p187 real manual gate",
        "nicegui_route": "/review",
        "purpose": "Bloquer ou valider le passage en review humaine.",
    },
    {
        "layer_id": "GEM_REAL_CASE_DECISION",
        "expected_sheet_tab": "GEM_REAL_CASE_DECISION",
        "local_path": "mvp_qaic_py/p188_real_case_ui_operator_decision_gate.py",
        "python_handler": "p188 real case UI gate",
        "nicegui_route": "/real-case",
        "purpose": "Afficher WAITING_INPUTS ou READY_FOR_HUMAN_DECISION.",
    },
    {
        "layer_id": "GEM_DECISION_JOURNAL",
        "expected_sheet_tab": "GEM_DECISION_JOURNAL",
        "local_path": "05_EXPORTS",
        "python_handler": "decision journal bridge",
        "nicegui_route": "/review",
        "purpose": "Tracer les décisions humaines review-only.",
    },
    {
        "layer_id": "PROMPT_HISTORY_LIBRARY",
        "expected_sheet_tab": "PROMPT_HISTORY_LIBRARY",
        "local_path": "mvp_qaic_py/p182_prompt_history_library_version_studio.py",
        "python_handler": "p182 prompt library",
        "nicegui_route": "/prompt",
        "purpose": "Suivre prompt actif, historiques et références.",
    },
    {
        "layer_id": "PROMPT_MIGRATION_MATRIX",
        "expected_sheet_tab": "PROMPT_MIGRATION_MATRIX",
        "local_path": "mvp_qaic_py/p189h_historical_prompt_quality_audit.py",
        "python_handler": "p189h historical audit",
        "nicegui_route": "/migration",
        "purpose": "Qualifier les prompts historiques: merge/archive/reject/review.",
    },
    {
        "layer_id": "RUNTIME_MIGRATION_TRACKER",
        "expected_sheet_tab": "RUNTIME_MIGRATION_TRACKER",
        "local_path": "mvp_qaic_py/p190r_runtime_migration_tracker_live_readonly.py",
        "python_handler": "p190r runtime tracker",
        "nicegui_route": "/migration",
        "purpose": "Suivre migration onglets/scripts/fonctions/Python/routes.",
    },
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _exists(root: Path, raw_path: str) -> bool:
    return (root / raw_path).exists()


def _count_files(root: Path, raw_path: str) -> int:
    path = root / raw_path
    if not path.exists():
        return 0
    if path.is_file():
        return 1
    return sum(
        1 for item in path.iterdir() if item.is_file() and item.name.lower() != "desktop.ini"
    )


def _route_exists(root: Path, route: str) -> bool:
    p173 = root / "mvp_qaic_py" / "p173_nicegui_private_local_runner.py"
    if not p173.exists():
        return False
    return f'@ui.page("{route}")' in p173.read_text(encoding="utf-8", errors="replace")


def _handler_status(root: Path, handler: str) -> str:
    lowered = handler.lower()
    if (
        "p182" in lowered
        and (root / "mvp_qaic_py" / "p182_prompt_history_library_version_studio.py").exists()
    ):
        return "BOUND"
    if (
        "p183" in lowered
        and (root / "mvp_qaic_py" / "p183_capture_to_session_link_prompt_run_workflow.py").exists()
    ):
        return "BOUND"
    if (
        "p184" in lowered
        and (root / "mvp_qaic_py" / "p184_real_gem_session_review_response_parser.py").exists()
    ):
        return "BOUND"
    if (
        "p185" in lowered
        and (root / "mvp_qaic_py" / "p185_real_operator_capture_response_ui_roundtrip.py").exists()
    ):
        return "BOUND"
    if (
        "p186" in lowered
        and (root / "mvp_qaic_py" / "p186_real_operator_roundtrip_smoke.py").exists()
    ):
        return "BOUND"
    if (
        "p187" in lowered
        and (root / "mvp_qaic_py" / "p187_real_manual_portfolio_case_review_gate.py").exists()
    ):
        return "BOUND"
    if (
        "p188" in lowered
        and (root / "mvp_qaic_py" / "p188_real_case_ui_operator_decision_gate.py").exists()
    ):
        return "BOUND"
    if (
        "p189h" in lowered
        and (root / "mvp_qaic_py" / "p189h_historical_prompt_quality_audit.py").exists()
    ):
        return "BOUND"
    if (
        "p190r" in lowered
        and (root / "mvp_qaic_py" / "p190r_runtime_migration_tracker_live_readonly.py").exists()
    ):
        return "BOUND"
    if "decision journal" in lowered:
        return "PARTIAL_LOCAL_EXPORTS"
    if "p181" in lowered:
        return "PARTIAL_UI_WORKFLOW"
    return "REVIEW"


def _score_layer(
    *, source_exists: bool, route_exists: bool, handler_status: str, file_count: int
) -> int:
    score = 0
    score += 25 if source_exists else 0
    score += 25 if route_exists else 0
    score += (
        25
        if handler_status in {"BOUND", "PARTIAL_UI_WORKFLOW"}
        else 10
        if handler_status == "PARTIAL_LOCAL_EXPORTS"
        else 0
    )
    score += 15 if file_count > 0 else 0
    score += 10
    return min(100, score)


def _runtime_status(score: int) -> str:
    if score >= 90:
        return "BOUND_RUNTIME_VISIBLE"
    if score >= 70:
        return "BOUND_PARTIAL"
    if score >= 45:
        return "DISCOVERED_NEEDS_BINDING"
    return "EXPECTED_NOT_READY"


def _next_action(status: str) -> str:
    if status == "BOUND_RUNTIME_VISIBLE":
        return "KEEP_TRACKING"
    if status == "BOUND_PARTIAL":
        return "ADD_MISSING_RUNTIME_EVIDENCE"
    if status == "DISCOVERED_NEEDS_BINDING":
        return "BIND_ROUTE_OR_HANDLER"
    return "CREATE_LAYER_OR_IMPORT_SNAPSHOT"


def build_gem_tracking_tabs_runtime_binding_matrix(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    layers: list[dict[str, Any]] = []

    for spec in EXPECTED_LAYERS:
        source_exists = _exists(root, spec["local_path"])
        file_count = _count_files(root, spec["local_path"])
        route_ok = _route_exists(root, spec["nicegui_route"])
        handler_status = _handler_status(root, spec["python_handler"])
        score = _score_layer(
            source_exists=source_exists,
            route_exists=route_ok,
            handler_status=handler_status,
            file_count=file_count,
        )
        status = _runtime_status(score)

        layers.append(
            {
                **spec,
                "source_exists": source_exists,
                "local_file_count": file_count,
                "route_bound": route_ok,
                "handler_status": handler_status,
                "binding_percent": score,
                "runtime_status": status,
                "next_action": _next_action(status),
            }
        )

    ready_count = sum(1 for row in layers if row["runtime_status"] == "BOUND_RUNTIME_VISIBLE")
    partial_count = sum(1 for row in layers if row["runtime_status"] == "BOUND_PARTIAL")
    missing_count = sum(1 for row in layers if row["runtime_status"] == "EXPECTED_NOT_READY")
    coverage = round(sum(int(row["binding_percent"]) for row in layers) / len(layers), 1)

    blockers: list[str] = []
    if not _route_exists(root, "/gem-tracking"):
        blockers.append("GEM_TRACKING_ROUTE_NOT_BOUND")
    if missing_count > 0:
        blockers.append("SOME_GEM_TRACKING_LAYERS_NOT_READY")

    coverage_rows = [
        {"metric": "layer_count", "value": len(layers), "status": "INFO"},
        {"metric": "ready_layer_count", "value": ready_count, "status": "OK"},
        {"metric": "partial_layer_count", "value": partial_count, "status": "REVIEW"},
        {
            "metric": "missing_layer_count",
            "value": missing_count,
            "status": "WARNING" if missing_count else "OK",
        },
        {
            "metric": "binding_coverage_percent",
            "value": coverage,
            "status": "OK" if coverage >= 75 else "REVIEW",
        },
        {
            "metric": "blocker_count",
            "value": len(blockers),
            "status": "OK" if not blockers else "REVIEW",
        },
    ]

    return {
        "STATUS": "OK_P191R_GEM_TRACKING_TABS_RUNTIME_BINDING_MATRIX_READY",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "layer_count": len(layers),
        "ready_layer_count": ready_count,
        "partial_layer_count": partial_count,
        "missing_layer_count": missing_count,
        "binding_coverage_percent": coverage,
        "layers": layers,
        "coverage_rows": coverage_rows,
        "blocker_count": len(blockers),
        "blockers": blockers,
        **SAFETY_FLAGS,
        "recommended_next": "P192R_GEM_TRACKING_TABS_CSV_EXPORT_AND_OPERATOR_VIEW_POLISH",
    }


def _http_ok(url: str) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P191R"})
        with urllib.request.urlopen(request, timeout=2.0) as response:
            return 200 <= int(response.status) < 500
    except Exception:
        return False


def run_gem_tracking_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8099,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_gem_tracking_tabs_runtime_binding_matrix(root)

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
        "STATUS": "OK_P191R_GEM_TRACKING_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P191R_GEM_TRACKING_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_gem_tracking_tabs_runtime_binding_matrix(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P191R_GEM_TRACKING_TABS_RUNTIME_BINDING_MATRIX_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = (
        run_gem_tracking_route_smoke(root)
        if run_route_smoke
        else build_gem_tracking_tabs_runtime_binding_matrix(root)
    )
    payload["export_dir"] = str(export_path)

    (export_path / "P191R_GEM_TRACKING_BINDING_MATRIX.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with (export_path / "P191R_GEM_TRACKING_BINDING_MATRIX.csv").open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file_obj:
        fieldnames = [
            "layer_id",
            "expected_sheet_tab",
            "runtime_status",
            "binding_percent",
            "local_path",
            "source_exists",
            "local_file_count",
            "python_handler",
            "handler_status",
            "nicegui_route",
            "route_bound",
            "next_action",
            "purpose",
        ]
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        for row in payload["layers"]:
            writer.writerow({key: row.get(key) for key in fieldnames})

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "layer_count",
        "ready_layer_count",
        "partial_layer_count",
        "missing_layer_count",
        "binding_coverage_percent",
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
    summary = {key: payload.get(key) for key in summary_keys}
    (export_path / "P191R_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "# P191R GEM Tracking Tabs Runtime Binding Matrix",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- layer_count: {payload['layer_count']}",
        f"- ready_layer_count: {payload['ready_layer_count']}",
        f"- binding_coverage_percent: {payload['binding_coverage_percent']}",
        f"- blocker_count: {payload['blocker_count']}",
        f"- route_smoke_ok: {payload.get('route_smoke_ok')}",
        "",
        "## Layers",
    ]
    for row in payload["layers"]:
        lines.append(
            f"- {row['layer_id']}: {row['runtime_status']} / "
            f"{row['binding_percent']}% / tab={row['expected_sheet_tab']} / "
            f"next={row['next_action']}"
        )
    lines.extend(
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
            "- P192R_GEM_TRACKING_TABS_CSV_EXPORT_AND_OPERATOR_VIEW_POLISH",
        ]
    )
    (export_path / "P191R_REPORT.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P191R GEM tracking binding matrix.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_gem_tracking_tabs_runtime_binding_matrix(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_gem_tracking_tabs_runtime_binding_matrix(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"LAYER_COUNT={payload['layer_count']}")
        print(f"BINDING_COVERAGE_PERCENT={payload['binding_coverage_percent']}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0 if payload["layer_count"] > 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
