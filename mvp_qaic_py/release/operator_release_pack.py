from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.operator.operator_decision_gate import (
    build_operator_decision_gate,
    render_operator_decision_gate_markdown,
)


def build_operator_release_pack(
    *,
    operator: str = "JULIEN",
    decision: str = "GO_LOCAL_OPERATOR_OUTPUT_PACK",
) -> dict[str, Any]:
    gate = build_operator_decision_gate(operator=operator, decision=decision)
    gate_ok = gate["status"] == "OK_P86_OPERATOR_DECISION_GATE_GO"

    return {
        "step": "P87_OPERATOR_RELEASE_PACK_FAST_FUSE",
        "status": "OK_P87_OPERATOR_RELEASE_PACK_READY" if gate_ok else "BLOCKED_P87_RELEASE_PACK",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "operator": operator,
        "decision": decision,
        "gate_status": gate["status"],
        "pack_status": gate["pack_status"],
        "bridge_status": gate["bridge_status"],
        "contract_status": gate["contract_status"],
        "planned_route_count": gate["planned_route_count"],
        "ready_route_count": gate["ready_route_count"],
        "human_approval_required_count": gate["human_approval_required_count"],
        "blocked_route_count": gate["blocked_route_count"],
        "write_route_count": gate["write_route_count"],
        "release_summary": {
            "mode": "LOCAL_RELEASE_PACK_ONLY",
            "operator_decision": "HUMAN_REVIEW_ONLY",
            "journal_policy": "APPROVE_APPEND_REQUIRED",
            "runtime_bridge": "READ_ONLY",
            "next_recommended": "P88_SHEETS_READONLY_CONNECTOR_DRYRUN",
        },
        "operator_decision_gate": gate,
        "sheet_write": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "google_rest_local_diag": False,
        "next": "P88_SHEETS_READONLY_CONNECTOR_DRYRUN_OR_STOP_LOCAL_MVP_SEAL",
    }


def render_operator_release_pack_markdown(pack: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# MVP QAIC — P87 Operator Release Pack",
            "",
            f"- status: `{pack['status']}`",
            f"- operator: `{pack['operator']}`",
            f"- decision: `{pack['decision']}`",
            f"- gate_status: `{pack['gate_status']}`",
            f"- pack_status: `{pack['pack_status']}`",
            f"- bridge_status: `{pack['bridge_status']}`",
            f"- contract_status: `{pack['contract_status']}`",
            f"- planned_route_count: `{pack['planned_route_count']}`",
            f"- ready_route_count: `{pack['ready_route_count']}`",
            f"- human_approval_required_count: `{pack['human_approval_required_count']}`",
            f"- write_route_count: `{pack['write_route_count']}`",
            "",
            "## Safety",
            "",
            "- NO_SHEET_WRITE",
            "- NO_APPS_SCRIPT_EXECUTION",
            "- NO_CLASP_PUSH",
            "- NO_BROKER_ORDER_SIZING",
            "- NO_GOOGLE_REST_LOCAL_DIAG",
            "",
            "## Embedded decision gate",
            "",
            render_operator_decision_gate_markdown(pack["operator_decision_gate"]),
            "",
            "## Next",
            "",
            f"`{pack['next']}`",
            "",
        ]
    )


def export_operator_release_pack(
    out_dir: str | Path,
    *,
    operator: str = "JULIEN",
    decision: str = "GO_LOCAL_OPERATOR_OUTPUT_PACK",
) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    pack = build_operator_release_pack(operator=operator, decision=decision)
    markdown = render_operator_release_pack_markdown(pack)

    json_path = target / "P87_OPERATOR_RELEASE_PACK.json"
    md_path = target / "P87_OPERATOR_RELEASE_PACK.md"
    json_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")

    return {
        "status": pack["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": pack["next"],
    }
