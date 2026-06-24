from __future__ import annotations

import argparse
import csv
import json
import socket
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SAFETY_FLAGS: dict[str, bool] = {
    "google_sheets_write": False,
    "live_google_api_call_from_python": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "public_serve": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "raw_operator_exports_committed": False,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _port_is_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1.0):
            return True
    except OSError:
        return False


def _http_ok(url: str, timeout_seconds: float = 2.0) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P174-Smoke"})
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return 200 <= int(response.status) < 500
    except Exception:
        return False


def build_launch_operator_smoke_plan(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8088,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    root = Path(project_root)
    routes = [
        {"route": "/", "url": f"http://{host}:{port}/"},
        {"route": "/cache", "url": f"http://{host}:{port}/cache"},
        {"route": "/review", "url": f"http://{host}:{port}/review"},
    ]
    blockers: list[str] = []
    if host != "127.0.0.1":
        blockers.append("PUBLIC_OR_NON_LOCAL_HOST_BLOCKED")
    if port <= 0 or port > 65535:
        blockers.append("INVALID_LOCAL_PORT")

    return {
        "STATUS": "READY_P174_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE_PLAN"
        if not blockers
        else "BLOCKED_P174_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE_PLAN",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "host": host,
        "port": port,
        "timeout_seconds": timeout_seconds,
        "routes": routes,
        "route_count": len(routes),
        "blocker_count": len(blockers),
        "blockers": blockers,
        "launch_command": [
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
        ],
        **SAFETY_FLAGS,
    }


def run_launch_operator_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8088,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    plan = build_launch_operator_smoke_plan(
        project_root,
        host=host,
        port=port,
        timeout_seconds=timeout_seconds,
    )
    blockers = list(plan["blockers"])

    if blockers:
        return {
            **plan,
            "STATUS": "BLOCKED_P174_NICEGUI_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE",
            "server_started_by_smoke": False,
            "server_stopped_after_smoke": False,
            "route_results": [],
            "route_success_count": 0,
            "smoke_ok": False,
            "recommended_next": "P174_R2_REPAIR_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE",
        }

    if _port_is_open(host, port):
        blockers.append("PORT_ALREADY_IN_USE_BEFORE_SMOKE")
        return {
            **plan,
            "STATUS": "BLOCKED_P174_NICEGUI_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE",
            "blockers": blockers,
            "blocker_count": len(blockers),
            "server_started_by_smoke": False,
            "server_stopped_after_smoke": False,
            "route_results": [],
            "route_success_count": 0,
            "smoke_ok": False,
            "recommended_next": "P174_R2_REPAIR_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE",
        }

    process = subprocess.Popen(
        plan["launch_command"],
        cwd=str(Path(project_root)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    route_results: list[dict[str, Any]] = []
    smoke_ok = False
    server_stopped = False
    start = time.time()

    try:
        while time.time() - start < timeout_seconds:
            if process.poll() is not None:
                blockers.append("SERVER_EXITED_EARLY")
                break

            current_results = []
            for route in plan["routes"]:
                ok = _http_ok(str(route["url"]))
                current_results.append({**route, "ok": ok})

            if all(row["ok"] for row in current_results):
                route_results = current_results
                smoke_ok = True
                break

            route_results = current_results
            time.sleep(1.0)

        if not smoke_ok and not blockers:
            blockers.append("ROUTES_NOT_READY_BEFORE_TIMEOUT")

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
        stdout_tail = ""
        stderr_tail = ""

    return {
        **plan,
        "STATUS": "OK_P174_NICEGUI_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE"
        if smoke_ok and server_stopped and not blockers
        else "BLOCKED_P174_NICEGUI_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE",
        "blockers": blockers,
        "blocker_count": len(blockers),
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row.get("ok")),
        "smoke_ok": smoke_ok and server_stopped and not blockers,
        "stdout_tail": stdout_tail,
        "stderr_tail": stderr_tail,
        "recommended_next": "P175_NICEGUI_OPERATOR_ERGONOMICS_POLISH"
        if smoke_ok and server_stopped and not blockers
        else "P174_R2_REPAIR_PRIVATE_LOCAL_LAUNCH_OPERATOR_SMOKE",
    }


def export_launch_operator_smoke(
    payload: dict[str, Any],
    export_dir: str | Path,
) -> dict[str, Any]:
    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)
    payload = {**payload, "export_dir": str(export_path)}

    (export_path / "P174_PRIVATE_LOCAL_LAUNCH_SMOKE_RESULT.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "host",
        "port",
        "timeout_seconds",
        "route_count",
        "route_success_count",
        "smoke_ok",
        "server_started_by_smoke",
        "server_stopped_after_smoke",
        "blocker_count",
        "blockers",
        "google_sheets_write",
        "live_google_api_call_from_python",
        "apps_script_execution",
        "clasp_push",
        "public_serve",
        "broker",
        "order",
        "sizing",
        "raw_operator_exports_committed",
        "recommended_next",
    ]
    (export_path / "P174_SUMMARY.json").write_text(
        json.dumps({key: payload[key] for key in summary_keys}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with (export_path / "P174_PRIVATE_LOCAL_ROUTE_SMOKE.csv").open(
        "w", encoding="utf-8", newline=""
    ) as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=["route", "url", "ok"])
        writer.writeheader()
        writer.writerows(payload["route_results"])

    report = [
        "# P174 NiceGUI Private Local Launch Operator Smoke",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- host: {payload['host']}",
        f"- port: {payload['port']}",
        f"- route_count: {payload['route_count']}",
        f"- route_success_count: {payload['route_success_count']}",
        f"- smoke_ok: {payload['smoke_ok']}",
        f"- server_started_by_smoke: {payload['server_started_by_smoke']}",
        f"- server_stopped_after_smoke: {payload['server_stopped_after_smoke']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "Safety:",
        "- PUBLIC_SERVE=False",
        "- GOOGLE_SHEETS_WRITE=False",
        "- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False",
        "- APPS_SCRIPT_EXECUTION=False",
        "- CLASP_PUSH=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
        "",
        "Next:",
        f"- {payload['recommended_next']}",
    ]
    (export_path / "P174_PRIVATE_LOCAL_LAUNCH_SMOKE_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P174 private local launch operator smoke.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8088)
    parser.add_argument("--timeout-seconds", type=int, default=45)
    parser.add_argument("--run-smoke", action="store_true")
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.run_smoke:
        payload = run_launch_operator_smoke(
            args.project_root,
            host=args.host,
            port=args.port,
            timeout_seconds=args.timeout_seconds,
        )
    else:
        payload = build_launch_operator_smoke_plan(
            args.project_root,
            host=args.host,
            port=args.port,
            timeout_seconds=args.timeout_seconds,
        )

    if args.write_export:
        if not args.export_dir:
            raise SystemExit("--export-dir is required with --write-export")
        payload = export_launch_operator_smoke(payload, args.export_dir)

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"ROUTE_COUNT={payload['route_count']}")
        print(f"SMOKE_OK={payload.get('smoke_ok', False)}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0 if payload.get("smoke_ok", False) or payload["STATUS"].startswith("READY_") else 2


if __name__ == "__main__":
    raise SystemExit(main())
