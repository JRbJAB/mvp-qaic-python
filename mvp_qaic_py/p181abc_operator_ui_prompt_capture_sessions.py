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


ROUTES = [
    "/",
    "/prompt",
    "/capture",
    "/responses",
    "/sessions",
    "/review",
    "/cache",
    "/journal",
    "/lexique",
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


def _http_ok(url: str) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P181ABC"})
        with urllib.request.urlopen(request, timeout=2.0) as response:
            return 200 <= int(response.status) < 500
    except Exception:
        return False


def build_p181abc_audit(
    project_root: str | Path, *, generated_at: str | None = None
) -> dict[str, Any]:
    root = Path(project_root)
    runner = root / "mvp_qaic_py" / "p173_nicegui_private_local_runner.py"
    code = runner.read_text(encoding="utf-8", errors="replace") if runner.exists() else ""

    required_tokens = [
        "Prompt Studio",
        "Capture Inbox",
        "GEM Response Inbox",
        "Sessions / interrogations",
        "ui.upload",
        "Sauver réponse GEM localement",
        "Copier prompt actif",
        "P181_CAPTURE_INBOX",
        "P181_GEM_RESPONSES",
        "P181_SESSION_LOG",
        '@ui.page("/capture")',
        '@ui.page("/responses")',
        '@ui.page("/sessions")',
        "APPLY BLOCKED",
    ]
    missing = [token for token in required_tokens if token not in code]
    ready = runner.exists() and not missing

    return {
        "STATUS": "OK_P181ABC_OPERATOR_UI_PROMPT_CAPTURE_SESSIONS_READY"
        if ready
        else "BLOCKED_P181ABC_OPERATOR_UI_PROMPT_CAPTURE_SESSIONS",
        "generated_at": generated_at or _utc_now(),
        "project_root": str(root),
        "runner_path": str(runner),
        "routes": ROUTES,
        "route_count": len(ROUTES),
        "required_token_count": len(required_tokens),
        "missing_token_count": len(missing),
        "missing_tokens": missing,
        "operator_ui_ready": ready,
        "blocker_count": len(missing),
        "blockers": [f"MISSING_TOKEN:{token}" for token in missing],
        **SAFETY_FLAGS,
        "recommended_next": "P182_PROMPT_HISTORY_LIBRARY_AND_VERSION_STUDIO",
    }


def run_p181abc_route_smoke(
    project_root: str | Path, *, timeout_seconds: int = 45
) -> dict[str, Any]:
    root = Path(project_root)
    audit = build_p181abc_audit(root)
    if not audit["operator_ui_ready"]:
        return {
            **audit,
            "route_success_count": 0,
            "route_smoke_ok": False,
            "server_started_by_smoke": False,
            "server_stopped_after_smoke": False,
        }

    command = [
        sys.executable,
        "-m",
        "mvp_qaic_py.p173_nicegui_private_local_runner",
        "--project-root",
        str(root),
        "--host",
        "127.0.0.1",
        "--port",
        "8088",
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

    route_results: list[dict[str, object]] = []
    route_smoke_ok = False
    server_stopped = False
    start = time.time()

    try:
        while time.time() - start < timeout_seconds:
            if process.poll() is not None:
                audit["blockers"].append("SERVER_EXITED_EARLY")
                break

            route_results = [
                {
                    "route": route,
                    "url": f"http://127.0.0.1:8088{route}",
                    "ok": _http_ok(f"http://127.0.0.1:8088{route}"),
                }
                for route in ROUTES
            ]
            if all(row["ok"] for row in route_results):
                route_smoke_ok = True
                break
            time.sleep(1.0)

        if not route_smoke_ok:
            audit["blockers"].append("ROUTES_NOT_READY_BEFORE_TIMEOUT")

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

    stdout_tail = ""
    stderr_tail = ""
    try:
        stdout, stderr = process.communicate(timeout=2)
        stdout_tail = "\n".join(stdout.splitlines()[-30:])
        stderr_tail = "\n".join(stderr.splitlines()[-30:])
    except Exception:
        pass

    blockers = list(audit["blockers"])
    route_success_count = sum(1 for row in route_results if row.get("ok"))

    return {
        **audit,
        "STATUS": "OK_P181ABC_OPERATOR_UI_PROMPT_CAPTURE_SESSIONS_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped and not blockers
        else "BLOCKED_P181ABC_OPERATOR_UI_PROMPT_CAPTURE_SESSIONS_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": route_success_count,
        "route_smoke_ok": route_smoke_ok and server_stopped and not blockers,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
        "stdout_tail": stdout_tail,
        "stderr_tail": stderr_tail,
        "blockers": blockers,
        "blocker_count": len(blockers),
        "recommended_next": "P182_PROMPT_HISTORY_LIBRARY_AND_VERSION_STUDIO"
        if route_smoke_ok and server_stopped and not blockers
        else "P181ABC_R2_REPAIR_OPERATOR_UI",
    }


def export_p181abc(payload: dict[str, Any], export_dir: str | Path) -> dict[str, Any]:
    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)
    payload = {**payload, "export_dir": str(export_path)}

    (export_path / "P181ABC_OPERATOR_UI_RESULT.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (export_path / "P181ABC_SUMMARY.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    report = [
        "# P181ABC Operator UI + Prompt Studio + Capture + Sessions",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- operator_ui_ready: {payload['operator_ui_ready']}",
        f"- route_count: {payload['route_count']}",
        f"- route_success_count: {payload.get('route_success_count', 0)}",
        f"- route_smoke_ok: {payload.get('route_smoke_ok', False)}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "Added UI zones:",
        "- Dashboard",
        "- Prompt Studio",
        "- Capture Inbox",
        "- GEM Response Inbox",
        "- Sessions / interrogations",
        "- Review",
        "- Cache",
        "- Journal",
        "- Lexique",
        "",
        "Safety:",
        "- PUBLIC_SERVE=False",
        "- GOOGLE_SHEETS_WRITE=False",
        "- GEM_CALL_EXECUTED=False",
        "- AUTO_APPLY_GEM_RESPONSE=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
        "",
        "Next:",
        f"- {payload['recommended_next']}",
    ]
    (export_path / "P181ABC_OPERATOR_UI_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P181ABC operator UI fast fuse.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--timeout-seconds", type=int, default=45)
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        run_p181abc_route_smoke(args.project_root, timeout_seconds=args.timeout_seconds)
        if args.run_route_smoke
        else build_p181abc_audit(args.project_root)
    )

    if args.write_export:
        if not args.export_dir:
            raise SystemExit("--export-dir is required with --write-export")
        payload = export_p181abc(payload, args.export_dir)

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"OPERATOR_UI_READY={payload['operator_ui_ready']}")
        print(f"ROUTE_SMOKE_OK={payload.get('route_smoke_ok', False)}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0 if payload.get("route_smoke_ok", False) or payload["operator_ui_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
