from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.p178_operator_shortcut_private_cockpit_handoff import (
    build_operator_handoff_payload,
)


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


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def build_private_cockpit_usage_close_payload(
    project_root: str | Path,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    root = Path(project_root)
    generated = generated_at or _utc_now()
    handoff = build_operator_handoff_payload(root)

    launcher_path = root / "00_OPERATOR_SHORTCUTS" / "P178_RUN_PRIVATE_COCKPIT.ps1"
    handoff_path = root / "00_OPERATOR_SHORTCUTS" / "P178_OPERATOR_HANDOFF.md"

    blockers: list[str] = list(handoff.get("blockers", []))
    if not handoff.get("handoff_ready"):
        blockers.append("P178_HANDOFF_NOT_READY")
    if not launcher_path.exists():
        blockers.append("MISSING_OPERATOR_LAUNCHER")
    if not handoff_path.exists():
        blockers.append("MISSING_OPERATOR_HANDOFF")

    launcher_text = _read_text(launcher_path) if launcher_path.exists() else ""
    handoff_text = _read_text(handoff_path) if handoff_path.exists() else ""

    checks = [
        {
            "check_id": "launcher_exists",
            "status": "PASS" if launcher_path.exists() else "FAIL",
        },
        {
            "check_id": "handoff_exists",
            "status": "PASS" if handoff_path.exists() else "FAIL",
        },
        {
            "check_id": "launcher_private_host",
            "status": "PASS"
            if "--host 127.0.0.1" in launcher_text and "0.0.0.0" not in launcher_text
            else "FAIL",
        },
        {
            "check_id": "launcher_private_port",
            "status": "PASS" if "--port 8088" in launcher_text else "FAIL",
        },
        {
            "check_id": "handoff_private_url",
            "status": "PASS" if "http://127.0.0.1:8088" in handoff_text else "FAIL",
        },
        {
            "check_id": "handoff_safety",
            "status": "PASS"
            if "Broker/order/sizing: False" in handoff_text
            and "Auto apply GEM response: False" in handoff_text
            else "FAIL",
        },
    ]

    failed_checks = [row["check_id"] for row in checks if row["status"] != "PASS"]
    blockers.extend(f"FAILED_CHECK:{check}" for check in failed_checks)

    close_ready = not blockers and len(checks) == 6

    return {
        "STATUS": "OK_P179_PRIVATE_COCKPIT_OPERATOR_USAGE_CLOSE_READY"
        if close_ready
        else "BLOCKED_P179_PRIVATE_COCKPIT_OPERATOR_USAGE_CLOSE",
        "generated_at": generated,
        "project_root": str(root),
        "source_step": "P178_OPERATOR_SHORTCUT_AND_PRIVATE_COCKPIT_HANDOFF",
        "launcher_path": str(launcher_path),
        "handoff_path": str(handoff_path),
        "private_url": "http://127.0.0.1:8088",
        "check_count": len(checks),
        "pass_count": sum(1 for row in checks if row["status"] == "PASS"),
        "fail_count": len(failed_checks),
        "checks": checks,
        "close_ready": close_ready,
        "blocker_count": len(blockers),
        "blockers": blockers,
        **SAFETY_FLAGS,
        "recommended_next": "PRIVATE_PROMPT_COCKPIT_CLOSED_READY_FOR_REAL_OPERATOR_USE_OR_P180_OPTIONAL_POLISH",
    }


def run_private_cockpit_usage_smoke(
    project_root: str | Path,
    *,
    timeout_seconds: int = 45,
) -> dict[str, Any]:
    root = Path(project_root)
    base = build_private_cockpit_usage_close_payload(root)
    if not base["close_ready"]:
        return {
            **base,
            "usage_smoke_executed": False,
            "usage_smoke_ok": False,
            "route_success_count": 0,
            "server_started_by_smoke": False,
            "server_stopped_after_smoke": False,
            "recommended_next": "P179_R2_REPAIR_OPERATOR_USAGE_SMOKE",
        }

    command = [
        sys.executable,
        "-m",
        "mvp_qaic_py.p174_nicegui_private_local_launch_operator_smoke",
        "--project-root",
        str(root),
        "--run-smoke",
        "--json",
        "--timeout-seconds",
        str(timeout_seconds),
    ]

    completed = subprocess.run(
        command,
        cwd=str(root),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout_seconds + 20,
        check=False,
    )

    stdout = completed.stdout.strip()
    payload = json.loads(stdout) if stdout.startswith("{") else {}

    smoke_ok = completed.returncode == 0 and payload.get("smoke_ok") is True
    blockers = list(base["blockers"])
    if not smoke_ok:
        blockers.append("P174_USAGE_SMOKE_FAILED")

    return {
        **base,
        "STATUS": "OK_P179_PRIVATE_COCKPIT_OPERATOR_USAGE_SMOKE_CLOSED"
        if smoke_ok and not blockers
        else "BLOCKED_P179_PRIVATE_COCKPIT_OPERATOR_USAGE_SMOKE",
        "usage_smoke_executed": True,
        "usage_smoke_ok": smoke_ok,
        "route_success_count": payload.get("route_success_count", 0),
        "server_started_by_smoke": payload.get("server_started_by_smoke", False),
        "server_stopped_after_smoke": payload.get("server_stopped_after_smoke", False),
        "stdout_tail": "\n".join(completed.stdout.splitlines()[-30:]),
        "stderr_tail": "\n".join(completed.stderr.splitlines()[-30:]),
        "blockers": blockers,
        "blocker_count": len(blockers),
        "recommended_next": "PRIVATE_PROMPT_COCKPIT_CLOSED_READY_FOR_REAL_OPERATOR_USE"
        if smoke_ok and not blockers
        else "P179_R2_REPAIR_OPERATOR_USAGE_SMOKE",
    }


def export_private_cockpit_usage_close(
    payload: dict[str, Any],
    export_dir: str | Path,
) -> dict[str, Any]:
    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)
    payload = {**payload, "export_dir": str(export_path)}

    (export_path / "P179_PRIVATE_COCKPIT_USAGE_CLOSE_RESULT.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "private_url",
        "check_count",
        "pass_count",
        "fail_count",
        "close_ready",
        "usage_smoke_executed",
        "usage_smoke_ok",
        "route_success_count",
        "server_started_by_smoke",
        "server_stopped_after_smoke",
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
    (export_path / "P179_SUMMARY.json").write_text(
        json.dumps({key: payload.get(key) for key in summary_keys}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    close_report = [
        "# P179 Private Cockpit Operator Usage Smoke Or Close",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- private_url: {payload['private_url']}",
        f"- close_ready: {payload['close_ready']}",
        f"- usage_smoke_executed: {payload['usage_smoke_executed']}",
        f"- usage_smoke_ok: {payload['usage_smoke_ok']}",
        f"- route_success_count: {payload['route_success_count']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "Résultat:",
        "- Cockpit privé local prêt pour usage opérateur réel si status OK.",
        "- Raccourci opérateur disponible dans 00_OPERATOR_SHORTCUTS.",
        "- Handoff opérateur disponible dans 00_OPERATOR_SHORTCUTS.",
        "",
        "Safety:",
        "- GEM_CALL_EXECUTED=False",
        "- AUTO_APPLY_GEM_RESPONSE=False",
        "- SOURCE_PROMPT_MODIFIED=False",
        "- GOOGLE_SHEETS_WRITE=False",
        "- LIVE_GOOGLE_API_CALL_FROM_PYTHON=False",
        "- APPS_SCRIPT_EXECUTION=False",
        "- CLASP_PUSH=False",
        "- PUBLIC_SERVE=False",
        "- BROKER=False",
        "- ORDER=False",
        "- SIZING=False",
        "",
        "Next:",
        f"- {payload['recommended_next']}",
    ]
    (export_path / "P179_PRIVATE_COCKPIT_CLOSE_REPORT.md").write_text(
        "\n".join(close_report) + "\n",
        encoding="utf-8",
    )

    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="P179 private cockpit operator usage smoke or close."
    )
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--timeout-seconds", type=int, default=45)
    parser.add_argument("--run-usage-smoke", action="store_true")
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.run_usage_smoke:
        payload = run_private_cockpit_usage_smoke(
            args.project_root, timeout_seconds=args.timeout_seconds
        )
    else:
        payload = build_private_cockpit_usage_close_payload(args.project_root)

    if args.write_export:
        if not args.export_dir:
            raise SystemExit("--export-dir is required with --write-export")
        payload = export_private_cockpit_usage_close(payload, args.export_dir)

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"CLOSE_READY={payload['close_ready']}")
        print(f"USAGE_SMOKE_OK={payload.get('usage_smoke_ok', False)}")
        print(f"BLOCKER_COUNT={payload['blocker_count']}")

    return 0 if payload.get("usage_smoke_ok", False) or payload["close_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
