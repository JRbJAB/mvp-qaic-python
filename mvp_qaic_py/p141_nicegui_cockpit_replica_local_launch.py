from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P141_NICEGUI_COCKPIT_REPLICA_LOCAL_LAUNCH_1.0.0_SAFE"
STATUS_READY = "P141_NICEGUI_LOCAL_LAUNCH_READY"
STATUS_LAUNCHED = "P141_NICEGUI_LOCAL_LAUNCH_SMOKE_PASSED"

SAFETY_MARKERS = {
    "host": "127.0.0.1",
    "public_deploy": False,
    "tunnel": False,
    "remote_access": False,
    "google_sheets_write": False,
    "live_google_sheets_read": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker": False,
    "order": False,
    "sizing": False,
    "auto_apply_gem_response": False,
}


@dataclass(frozen=True)
class LaunchRequest:
    p140_export_dir: Path
    output_dir: Path
    run_id: str
    generated_at_utc: str
    host: str
    port: int
    start_local_server: bool
    smoke_timeout_sec: int


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_p140_export(p140_export_dir: Path) -> tuple[Path, Path, dict[str, Any]]:
    model_path = p140_export_dir / "P140_NICEGUI_COMPONENT_MODEL.json"
    app_path = p140_export_dir / "P140_NICEGUI_REPLICA_APP.py"
    summary_path = p140_export_dir / "P140_SUMMARY.json"
    if not model_path.exists():
        raise FileNotFoundError(f"Missing P140 model: {model_path}")
    if not app_path.exists():
        raise FileNotFoundError(f"Missing P140 NiceGUI app: {app_path}")
    if not summary_path.exists():
        raise FileNotFoundError(f"Missing P140 summary: {summary_path}")

    model = load_json(model_path)
    if model.get("status") != "P140_NICEGUI_COCKPIT_REPLICA_RENDERED_FROM_METADATA":
        raise ValueError(f"Invalid P140 model status: {model.get('status')}")
    if int(model.get("cockpit_page_count", 0) or 0) <= 0:
        raise ValueError("P140 model cockpit_page_count must be > 0")
    return model_path, app_path, model


def routes_from_model(model: dict[str, Any]) -> list[str]:
    routes = ["/"]
    for page in model.get("pages", []):
        route = str(page.get("route") or "").strip()
        if route and route not in routes:
            routes.append(route)
    return routes


def build_launch_plan(
    request: LaunchRequest, model: dict[str, Any], app_path: Path
) -> dict[str, Any]:
    routes = routes_from_model(model)
    return {
        "status": STATUS_READY,
        "version": VERSION,
        "run_id": request.run_id,
        "generated_at_utc": request.generated_at_utc,
        "source_p140_export_dir": str(request.p140_export_dir),
        "nicegui_app_path": str(app_path),
        "local_url": f"http://{request.host}:{request.port}",
        "host": request.host,
        "port": request.port,
        "route_count": len(routes),
        "routes": routes,
        "cockpit_page_count": model.get("cockpit_page_count"),
        "launch_command": f'python "{app_path}"',
        "start_local_server_requested": request.start_local_server,
        "safety": dict(SAFETY_MARKERS),
        "next": "P142_UI_FIDELITY_SHELL",
    }


def http_get_status(url: str, timeout: float = 2.0) -> tuple[int | None, str]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return int(response.status), response.read(300).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return int(exc.code), exc.read(300).decode("utf-8", errors="replace")
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def wait_for_server(base_url: str, timeout_sec: int) -> bool:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        status, _ = http_get_status(base_url, timeout=2.0)
        if status and 200 <= status < 500:
            return True
        time.sleep(0.75)
    return False


def start_server(app_path: Path, output_dir: Path) -> dict[str, Any]:
    stdout_path = output_dir / "P141_NICEGUI_SERVER_STDOUT.log"
    stderr_path = output_dir / "P141_NICEGUI_SERVER_STDERR.log"
    stdout = stdout_path.open("w", encoding="utf-8")
    stderr = stderr_path.open("w", encoding="utf-8")

    creationflags = 0
    if os.name == "nt":
        creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)

    proc = subprocess.Popen(
        [sys.executable, str(app_path)],
        cwd=str(app_path.parent),
        stdout=stdout,
        stderr=stderr,
        stdin=subprocess.DEVNULL,
        creationflags=creationflags,
    )
    return {
        "pid": proc.pid,
        "stdout_log": str(stdout_path),
        "stderr_log": str(stderr_path),
    }


def smoke_routes(base_url: str, routes: list[str]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for route in routes:
        url = base_url.rstrip("/") + route
        status, body = http_get_status(url, timeout=5.0)
        results.append(
            {
                "route": route,
                "url": url,
                "http_status": status,
                "ok": bool(status and 200 <= status < 500),
                "body_preview": body[:120],
            }
        )
    return results


def write_outputs(plan: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    plan_path = output_dir / "P141_LOCAL_LAUNCH_PLAN.json"
    smoke_path = output_dir / "P141_ROUTE_SMOKE_RESULTS.csv"
    runbook_path = output_dir / "P141_LOCAL_LAUNCH_RUNBOOK.md"
    summary_path = output_dir / "P141_SUMMARY.json"

    plan_path.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    smoke_results = plan.get("smoke_results", [])
    with smoke_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["route", "url", "http_status", "ok", "body_preview"]
        )
        writer.writeheader()
        for row in smoke_results:
            writer.writerow({key: row.get(key, "") for key in writer.fieldnames})

    route_lines = "\n".join(f"- `{route}`" for route in plan.get("routes", []))
    runbook_path.write_text(
        "\n".join(
            [
                "# P141 — NiceGUI Cockpit Replica Local Launch",
                "",
                f"- Status: `{plan['status']}`",
                f"- Local URL: `{plan['local_url']}`",
                f"- NiceGUI app: `{plan['nicegui_app_path']}`",
                f"- Launch command: `{plan['launch_command']}`",
                "",
                "## Routes",
                "",
                route_lines,
                "",
                "## Safety",
                "",
                "- Localhost only: `127.0.0.1`",
                "- No public deploy",
                "- No Google Sheets write",
                "- No broker/order/sizing",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = {
        "status": plan["status"],
        "local_url": plan["local_url"],
        "server_pid": plan.get("server", {}).get("pid"),
        "route_count": plan.get("route_count"),
        "smoke_pass_count": sum(1 for row in smoke_results if row.get("ok")),
        "smoke_total_count": len(smoke_results),
        "google_sheets_write": False,
        "public_deploy": False,
        "output_dir": str(output_dir),
        "next": plan["next"],
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )

    return {
        "plan_json": str(plan_path),
        "smoke_csv": str(smoke_path),
        "runbook_md": str(runbook_path),
        "summary_json": str(summary_path),
    }


def run_launch(request: LaunchRequest) -> dict[str, Any]:
    _, app_path, model = validate_p140_export(request.p140_export_dir)
    plan = build_launch_plan(request, model, app_path)
    base_url = plan["local_url"]

    existing_ok = wait_for_server(base_url, timeout_sec=2)
    if request.start_local_server and not existing_ok:
        plan["server"] = start_server(app_path, request.output_dir)
        if not wait_for_server(base_url, timeout_sec=request.smoke_timeout_sec):
            plan["status"] = "P141_NICEGUI_LOCAL_LAUNCH_SERVER_NOT_READY"
            plan["smoke_results"] = []
            write_outputs(plan, request.output_dir)
            raise RuntimeError(f"NiceGUI server did not become ready at {base_url}")
        plan["server_reused"] = False
    elif existing_ok:
        plan["server"] = {"pid": None, "note": "existing server reused"}
        plan["server_reused"] = True
    else:
        plan["server"] = {"pid": None, "note": "start not requested"}
        plan["server_reused"] = False

    if request.start_local_server or existing_ok:
        plan["smoke_results"] = smoke_routes(base_url, plan["routes"])
        if not all(row.get("ok") for row in plan["smoke_results"]):
            plan["status"] = "P141_NICEGUI_LOCAL_LAUNCH_SMOKE_REVIEW_REQUIRED"
        else:
            plan["status"] = STATUS_LAUNCHED
    else:
        plan["smoke_results"] = []
        plan["status"] = STATUS_READY

    output_files = write_outputs(plan, request.output_dir)
    plan["output_files"] = output_files
    (request.output_dir / "P141_LOCAL_LAUNCH_PLAN.json").write_text(
        json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="P141 local launch smoke for P140 NiceGUI replica."
    )
    parser.add_argument("--p140-export-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--run-id", default="P141-NICEGUI-LOCAL-LAUNCH")
    parser.add_argument("--generated-at-utc", default=utc_now_iso())
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8088)
    parser.add_argument("--start-local-server", action="store_true")
    parser.add_argument("--smoke-timeout-sec", type=int, default=30)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    plan = run_launch(
        LaunchRequest(
            p140_export_dir=Path(args.p140_export_dir),
            output_dir=Path(args.output_dir),
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
            host=args.host,
            port=args.port,
            start_local_server=bool(args.start_local_server),
            smoke_timeout_sec=args.smoke_timeout_sec,
        )
    )
    print(plan["status"])
    print(f"local_url={plan['local_url']}")
    print(f"route_count={plan['route_count']}")
    print(f"server_pid={plan.get('server', {}).get('pid')}")
    print("google_sheets_write=false")
    print("public_deploy=false")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
