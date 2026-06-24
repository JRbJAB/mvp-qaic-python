from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.p187_real_manual_portfolio_case_review_gate import (
    build_manual_portfolio_case_review_gate,
)


ROUTES = ["/", "/capture", "/responses", "/roundtrip", "/real-case", "/review"]

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


def build_real_case_operator_decision_gate(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    gate = build_manual_portfolio_case_review_gate(root)

    decision_status = "READY_FOR_HUMAN_DECISION" if gate["real_case_ready"] else "WAITING_INPUTS"
    operator_instruction = (
        "Vrai cas prêt: ouvrir /review et décider manuellement."
        if gate["real_case_ready"]
        else "Déposer une vraie capture portfolio puis coller une vraie réponse GEM."
    )

    return {
        "STATUS": "OK_P188_REAL_CASE_UI_OPERATOR_DECISION_GATE_READY",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "decision_status": decision_status,
        "operator_instruction": operator_instruction,
        "real_case_ready": gate["real_case_ready"],
        "human_review_required": True,
        "apply_allowed": False,
        "capture_count": gate["capture_count"],
        "response_count": gate["response_count"],
        "blocker_count": gate["blocker_count"],
        "blockers": gate["blockers"],
        "selected_capture": gate["selected_capture"],
        "selected_response": gate["selected_response"],
        "route_count": len(ROUTES),
        "routes": ROUTES,
        **SAFETY_FLAGS,
        "recommended_next": (
            "P189_REAL_CASE_REVIEW_DECISION_CAPTURE"
            if gate["real_case_ready"]
            else "WAIT_OPERATOR_REAL_CAPTURE_AND_GEM_RESPONSE"
        ),
    }


def _http_ok(url: str) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P188"})
        with urllib.request.urlopen(request, timeout=2.0) as response:
            return 200 <= int(response.status) < 500
    except Exception:
        return False


def run_real_case_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8097,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_real_case_operator_decision_gate(root)

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
        "STATUS": "OK_P188_REAL_CASE_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P188_REAL_CASE_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_real_case_operator_decision_gate(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P188_REAL_CASE_UI_OPERATOR_DECISION_GATE_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = (
        run_real_case_route_smoke(root)
        if run_route_smoke
        else build_real_case_operator_decision_gate(root)
    )
    payload["export_dir"] = str(export_path)

    (export_path / "P188_REAL_CASE_OPERATOR_DECISION_GATE.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "decision_status",
        "real_case_ready",
        "human_review_required",
        "apply_allowed",
        "capture_count",
        "response_count",
        "blocker_count",
        "blockers",
        "route_count",
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
    (export_path / "P188_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = [
        "# P188 Real Case UI Operator Decision Gate",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- decision_status: {payload['decision_status']}",
        f"- real_case_ready: {payload['real_case_ready']}",
        f"- capture_count: {payload['capture_count']}",
        f"- response_count: {payload['response_count']}",
        f"- blocker_count: {payload['blocker_count']}",
        f"- route_smoke_ok: {payload.get('route_smoke_ok')}",
        "",
        "Operator instruction:",
        payload["operator_instruction"],
        "",
        "Safety:",
        "- GEM_CALL_EXECUTED=False",
        "- AUTO_APPLY_GEM_RESPONSE=False",
        "- GOOGLE_SHEETS_WRITE=False",
        "- PUBLIC_SERVE=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
        "",
        "Next:",
        f"- {payload['recommended_next']}",
    ]
    (export_path / "P188_REAL_CASE_OPERATOR_DECISION_GATE_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P188 real case UI operator decision gate.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_real_case_operator_decision_gate(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_real_case_operator_decision_gate(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"DECISION_STATUS={payload['decision_status']}")
        print(f"REAL_CASE_READY={payload['real_case_ready']}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
