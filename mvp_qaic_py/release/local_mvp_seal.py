from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.release.operator_release_pack import build_operator_release_pack
from mvp_qaic_py.sheets.readonly_connector_dryrun import (
    build_sheets_readonly_connector_dryrun,
    render_sheets_readonly_connector_dryrun_markdown,
)

SEALED_STEPS: tuple[str, ...] = (
    "P81R_P82_LIVE_SHEETS_CONTRACT",
    "P83B_LOCAL_BRIDGE_DRYRUN",
    "P84A_OPERATOR_BRIDGE_SMOKE",
    "P85A_OPERATOR_OUTPUT_PACK",
    "P86_OPERATOR_DECISION_GATE",
    "P87_OPERATOR_RELEASE_PACK",
    "P88_SHEETS_READONLY_DRYRUN",
)


def build_local_mvp_seal() -> dict[str, Any]:
    release = build_operator_release_pack()
    sheets = build_sheets_readonly_connector_dryrun()
    ready = (
        release["status"] == "OK_P87_OPERATOR_RELEASE_PACK_READY"
        and sheets["status"] == "OK_P88_SHEETS_READONLY_CONNECTOR_DRYRUN_READY"
        and release["write_route_count"] == 0
        and sheets["write_requested"] is False
        and sheets["live_google_api_call"] is False
    )
    return {
        "step": "P89_LOCAL_MVP_SEAL_FAST_FUSE",
        "status": "OK_P89_LOCAL_MVP_SEALED" if ready else "BLOCKED_P89_LOCAL_MVP_SEAL",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sealed_steps": SEALED_STEPS,
        "sealed_step_count": len(SEALED_STEPS),
        "release_status": release["status"],
        "sheets_dryrun_status": sheets["status"],
        "contract_status": sheets["contract_status"],
        "bridge_status": release["bridge_status"],
        "gate_status": release["gate_status"],
        "write_route_count": release["write_route_count"],
        "human_approval_required_count": release["human_approval_required_count"],
        "sheet_write": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "google_rest_local_diag": False,
        "live_google_api_call": False,
        "operator_release_pack": release,
        "sheets_readonly_dryrun": sheets,
        "decision": "LOCAL_MVP_SEALED_READY_FOR_P90_OR_STOP",
        "next": "P90_GOOGLE_SHEETS_READONLY_CONNECTOR_LIVE_DECISION_OR_STOP",
    }


def render_local_mvp_seal_markdown(seal: dict[str, Any]) -> str:
    lines = [
        "# MVP QAIC — P89 Local MVP Seal",
        "",
        f"- status: `{seal['status']}`",
        f"- sealed_step_count: `{seal['sealed_step_count']}`",
        f"- release_status: `{seal['release_status']}`",
        f"- sheets_dryrun_status: `{seal['sheets_dryrun_status']}`",
        f"- contract_status: `{seal['contract_status']}`",
        f"- bridge_status: `{seal['bridge_status']}`",
        f"- gate_status: `{seal['gate_status']}`",
        f"- next: `{seal['next']}`",
        "",
        "## Safety",
        "",
        "- NO_SHEET_WRITE",
        "- NO_APPS_SCRIPT_EXECUTION",
        "- NO_CLASP_PUSH",
        "- NO_BROKER_ORDER_SIZING",
        "- NO_GOOGLE_REST_LOCAL_DIAG",
        "- NO_LIVE_GOOGLE_API_CALL",
        "",
        "## Sealed steps",
        "",
    ]
    for step in seal["sealed_steps"]:
        lines.append(f"- `{step}`")
    lines.extend(
        [
            "",
            "## Sheets dry-run snapshot",
            "",
            render_sheets_readonly_connector_dryrun_markdown(seal["sheets_readonly_dryrun"]),
            "",
        ]
    )
    return "\n".join(lines)


def export_local_mvp_seal(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    seal = build_local_mvp_seal()
    markdown = render_local_mvp_seal_markdown(seal)
    json_path = target / "P89_LOCAL_MVP_SEAL.json"
    md_path = target / "P89_LOCAL_MVP_SEAL.md"
    json_path.write_text(json.dumps(seal, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "status": seal["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": seal["next"],
    }
