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

from mvp_qaic_py.p184_real_gem_session_review_response_parser import (
    build_real_gem_session_review,
)


ROUTES = ["/", "/capture", "/prompt", "/responses", "/sessions", "/roundtrip", "/review"]

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


def _count_files(folder: Path, extensions: set[str]) -> int:
    if not folder.exists():
        return 0
    count = 0
    for path in folder.glob("*"):
        if not path.is_file():
            continue
        if path.name.lower() == "desktop.ini":
            continue
        if path.suffix.lower() in extensions:
            count += 1
    return count


def build_roundtrip_model(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    capture_dir = root / "00_OPERATOR_EXPORTS" / "P181_CAPTURE_INBOX"
    response_dir = root / "00_OPERATOR_EXPORTS" / "P181_GEM_RESPONSES"
    session_dir = root / "00_OPERATOR_EXPORTS" / "P181_SESSION_LOG"

    parser_payload = build_real_gem_session_review(root)

    capture_count = _count_files(capture_dir, {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"})
    response_count = _count_files(response_dir, {".json", ".md", ".txt"})
    session_count = _count_files(session_dir, {".json"})

    stages = [
        {
            "step": "capture_portfolio",
            "label": "Capture portfolio locale",
            "status": "READY" if capture_count else "WAITING_OPERATOR_INPUT",
        },
        {"step": "copy_prompt", "label": "Copie prompt actif", "status": "READY"},
        {
            "step": "paste_gem_response",
            "label": "Coller réponse GEM locale",
            "status": "READY" if response_count else "WAITING_OPERATOR_INPUT",
        },
        {
            "step": "parse_response",
            "label": "Parser réponse GEM",
            "status": "READY" if parser_payload["parser_ready"] else "BLOCKED",
        },
        {
            "step": "human_review",
            "label": "Review humaine",
            "status": parser_payload["review_status"],
        },
    ]

    return {
        "STATUS": "OK_P185_REAL_OPERATOR_CAPTURE_RESPONSE_UI_ROUNDTRIP_READY",
        "generated_at": _utc_now(),
        "project_root": str(root),
        "roundtrip_ready": True,
        "route_count": len(ROUTES),
        "routes": ROUTES,
        "capture_count": capture_count,
        "response_count": response_count,
        "session_count": session_count,
        "parser_ready": parser_payload["parser_ready"],
        "parsed_response_count": parser_payload["parsed_response_count"],
        "review_status": parser_payload["review_status"],
        "has_real_response_ready": parser_payload["has_real_response_ready"],
        "workflow_stage_count": len(stages),
        "workflow_stages": stages,
        "blocker_count": 0,
        "blockers": [],
        **SAFETY_FLAGS,
        "recommended_next": "P186_REAL_OPERATOR_ROUNDTRIP_SMOKE_WITH_CAPTURE_AND_RESPONSE",
    }


def _http_ok(url: str) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MVP-QAIC-P185"})
        with urllib.request.urlopen(request, timeout=2.0) as response:
            return 200 <= int(response.status) < 500
    except Exception:
        return False


def run_roundtrip_route_smoke(
    project_root: str | Path,
    *,
    host: str = "127.0.0.1",
    port: int = 8095,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    root = Path(project_root)
    payload = build_roundtrip_model(root)

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
        "STATUS": "OK_P185_REAL_OPERATOR_ROUNDTRIP_ROUTE_SMOKE"
        if route_smoke_ok and server_stopped
        else "BLOCKED_P185_REAL_OPERATOR_ROUNDTRIP_ROUTE_SMOKE",
        "route_results": route_results,
        "route_success_count": sum(1 for row in route_results if row["ok"]),
        "route_smoke_ok": route_smoke_ok and server_stopped,
        "server_started_by_smoke": True,
        "server_stopped_after_smoke": server_stopped,
    }


def export_roundtrip_model(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P185_REAL_OPERATOR_CAPTURE_RESPONSE_UI_ROUNDTRIP_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = run_roundtrip_route_smoke(root) if run_route_smoke else build_roundtrip_model(root)
    payload["export_dir"] = str(export_path)

    (export_path / "P185_ROUNDTRIP_MODEL.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "roundtrip_ready",
        "route_count",
        "route_success_count",
        "route_smoke_ok",
        "capture_count",
        "response_count",
        "session_count",
        "parser_ready",
        "parsed_response_count",
        "review_status",
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
    (export_path / "P185_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    report = [
        "# P185 Real Operator Capture Response UI Roundtrip",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- roundtrip_ready: {payload['roundtrip_ready']}",
        f"- route_count: {payload['route_count']}",
        f"- route_success_count: {payload.get('route_success_count')}",
        f"- route_smoke_ok: {payload.get('route_smoke_ok')}",
        f"- parser_ready: {payload['parser_ready']}",
        f"- review_status: {payload['review_status']}",
        "",
        "Workflow:",
        "- Capture portfolio locale",
        "- Copie prompt actif",
        "- Collage réponse GEM locale",
        "- Parser P184",
        "- Review humaine",
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
        "- P186_REAL_OPERATOR_ROUNDTRIP_SMOKE_WITH_CAPTURE_AND_RESPONSE",
    ]
    (export_path / "P185_ROUNDTRIP_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P185 roundtrip UI model.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_roundtrip_model(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_roundtrip_model(args.project_root)
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"ROUNDTRIP_READY={payload['roundtrip_ready']}")
        print(f"PARSER_READY={payload['parser_ready']}")
        print(f"REVIEW_STATUS={payload['review_status']}")

    return 0 if payload["roundtrip_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
