from __future__ import annotations

import argparse
import base64
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.p184_real_gem_session_review_response_parser import (
    parse_gem_response_text,
)
from mvp_qaic_py.p185_real_operator_capture_response_ui_roundtrip import (
    build_roundtrip_model,
    run_roundtrip_route_smoke,
)


PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMB/az+3WkAAAAASUVORK5CYII="
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


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _capture_dir(root: Path) -> Path:
    folder = root / "00_OPERATOR_EXPORTS" / "P181_CAPTURE_INBOX"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _response_dir(root: Path) -> Path:
    folder = root / "00_OPERATOR_EXPORTS" / "P181_GEM_RESPONSES"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def create_controlled_roundtrip_inputs(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    capture_path = _capture_dir(root) / "P186_SMOKE_PORTFOLIO_CAPTURE.png"
    response_path = _response_dir(root) / "P186_SMOKE_GEM_RESPONSE.json"

    capture_path.write_bytes(base64.b64decode(PNG_B64))

    response_payload = {
        "status": "REVIEW_REQUIRED",
        "input_mode": "IMAGE_USED",
        "image_usage_evidence": {"status": "IMAGE_USED"},
        "reference_currency": "USD",
        "portfolio_review": {
            "summary": "Controlled local smoke response; not real market advice.",
            "positions": [],
        },
        "missing_data": ["REAL_PORTFOLIO_CAPTURE_NOT_PROVIDED"],
        "blockers": ["HUMAN_REVIEW_REQUIRED", "NO_AUTO_APPLY"],
        "safety": {
            "no_order": True,
            "no_sizing": True,
            "auto_apply_gem_response": False,
            "broker": False,
        },
        "human_decision": "REVIEW_REQUIRED",
    }
    response_path.write_text(
        json.dumps(response_payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    parsed = parse_gem_response_text(
        response_path.read_text(encoding="utf-8"),
        source_name=response_path.name,
    )

    return {
        "capture_path": str(capture_path),
        "response_path": str(response_path),
        "capture_exists": capture_path.exists(),
        "response_exists": response_path.exists(),
        "parsed_response": parsed,
    }


def build_p186_roundtrip_smoke(
    project_root: str | Path,
    *,
    run_route_smoke: bool = False,
    route_port: int = 8096,
) -> dict[str, Any]:
    root = Path(project_root)
    inputs = create_controlled_roundtrip_inputs(root)
    roundtrip = build_roundtrip_model(root)
    route_payload: dict[str, Any] = {}

    if run_route_smoke:
        route_payload = run_roundtrip_route_smoke(root, port=route_port)

    parsed = inputs["parsed_response"]

    blockers: list[str] = []
    if not inputs["capture_exists"]:
        blockers.append("SMOKE_CAPTURE_NOT_CREATED")
    if not inputs["response_exists"]:
        blockers.append("SMOKE_RESPONSE_NOT_CREATED")
    if parsed["blocker_count"] != 0:
        blockers.append("PARSER_BLOCKERS_FOUND")
    if roundtrip["capture_count"] < 1:
        blockers.append("ROUNDTRIP_CAPTURE_COUNT_ZERO")
    if roundtrip["response_count"] < 1:
        blockers.append("ROUNDTRIP_RESPONSE_COUNT_ZERO")
    if roundtrip["parsed_response_count"] < 1:
        blockers.append("ROUNDTRIP_PARSED_RESPONSE_COUNT_ZERO")
    if run_route_smoke and route_payload.get("route_smoke_ok") is not True:
        blockers.append("ROUTE_SMOKE_FAILED")

    smoke_ready = not blockers
    status = (
        "OK_P186_REAL_OPERATOR_ROUNDTRIP_SMOKE_WITH_CAPTURE_AND_RESPONSE_READY"
        if smoke_ready
        else "BLOCKED_P186_REAL_OPERATOR_ROUNDTRIP_SMOKE"
    )

    return {
        "STATUS": status,
        "generated_at": _utc_now(),
        "project_root": str(root),
        "smoke_ready": smoke_ready,
        "capture_path": inputs["capture_path"],
        "response_path": inputs["response_path"],
        "capture_exists": inputs["capture_exists"],
        "response_exists": inputs["response_exists"],
        "capture_count": roundtrip["capture_count"],
        "response_count": roundtrip["response_count"],
        "session_count": roundtrip["session_count"],
        "parser_ready": roundtrip["parser_ready"],
        "parsed_response_count": roundtrip["parsed_response_count"],
        "review_status": roundtrip["review_status"],
        "parsed_smoke_response_status": parsed["review_status"],
        "parsed_smoke_response_blocker_count": parsed["blocker_count"],
        "parsed_smoke_response_warning_count": parsed["warning_count"],
        "route_smoke_requested": run_route_smoke,
        "route_count": route_payload.get("route_count"),
        "route_success_count": route_payload.get("route_success_count"),
        "route_smoke_ok": route_payload.get("route_smoke_ok"),
        "blocker_count": len(blockers),
        "blockers": blockers,
        **SAFETY_FLAGS,
        "recommended_next": "P187_REAL_MANUAL_PORTFOLIO_CASE_REVIEW_GATE",
    }


def export_p186_roundtrip_smoke(
    project_root: str | Path,
    *,
    export_dir: str | Path | None = None,
    run_route_smoke: bool = False,
) -> dict[str, Any]:
    root = Path(project_root)
    export_path = (
        Path(export_dir)
        if export_dir is not None
        else root / "05_EXPORTS" / f"P186_ROUNDTRIP_SMOKE_{_stamp()}"
    )
    export_path.mkdir(parents=True, exist_ok=True)

    payload = build_p186_roundtrip_smoke(root, run_route_smoke=run_route_smoke)
    payload["export_dir"] = str(export_path)

    (export_path / "P186_ROUNDTRIP_SMOKE_RESULT.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_keys = [
        "STATUS",
        "generated_at",
        "project_root",
        "export_dir",
        "smoke_ready",
        "capture_exists",
        "response_exists",
        "capture_count",
        "response_count",
        "session_count",
        "parser_ready",
        "parsed_response_count",
        "review_status",
        "route_smoke_requested",
        "route_count",
        "route_success_count",
        "route_smoke_ok",
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
    (export_path / "P186_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report = [
        "# P186 Real Operator Roundtrip Smoke With Capture And Response",
        "",
        f"- STATUS: {payload['STATUS']}",
        f"- smoke_ready: {payload['smoke_ready']}",
        f"- capture_exists: {payload['capture_exists']}",
        f"- response_exists: {payload['response_exists']}",
        f"- capture_count: {payload['capture_count']}",
        f"- response_count: {payload['response_count']}",
        f"- parsed_response_count: {payload['parsed_response_count']}",
        f"- route_smoke_ok: {payload['route_smoke_ok']}",
        f"- blocker_count: {payload['blocker_count']}",
        "",
        "Scope:",
        "- Controlled local capture file",
        "- Controlled local GEM response file",
        "- P184 parser validation",
        "- P185 roundtrip model",
        "- Private local route smoke",
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
        "- P187_REAL_MANUAL_PORTFOLIO_CASE_REVIEW_GATE",
    ]
    (export_path / "P186_ROUNDTRIP_SMOKE_REPORT.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P186 roundtrip smoke.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--export-dir", default=None)
    parser.add_argument("--write-export", action="store_true")
    parser.add_argument("--run-route-smoke", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    payload = (
        export_p186_roundtrip_smoke(
            args.project_root,
            export_dir=args.export_dir,
            run_route_smoke=args.run_route_smoke,
        )
        if args.write_export
        else build_p186_roundtrip_smoke(
            args.project_root,
            run_route_smoke=args.run_route_smoke,
        )
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload["STATUS"])
        print(f"SMOKE_READY={payload['smoke_ready']}")
        print(f"PARSED_RESPONSE_COUNT={payload['parsed_response_count']}")
        print(f"ROUTE_SMOKE_OK={payload.get('route_smoke_ok')}")

    return 0 if payload["smoke_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
