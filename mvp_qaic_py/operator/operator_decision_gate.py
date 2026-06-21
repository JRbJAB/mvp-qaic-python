from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.operator.operator_output_pack import (
    build_operator_output_pack,
    render_operator_output_markdown,
)

SAFE_OPERATOR_DECISIONS: tuple[str, ...] = (
    "GO_LOCAL_OPERATOR_OUTPUT_PACK",
    "HOLD_HUMAN_REVIEW",
    "STOP_NO_ACTION",
)


def build_operator_decision_gate(
    *,
    operator: str = "JULIEN",
    decision: str = "GO_LOCAL_OPERATOR_OUTPUT_PACK",
) -> dict[str, Any]:
    pack = build_operator_output_pack(operator=operator, requested_action="REVIEW_ONLY")
    decision_allowed = decision in SAFE_OPERATOR_DECISIONS
    prerequisites_ok = (
        pack["status"] == "OK_P85A_OPERATOR_OUTPUT_PACK_READY"
        and pack["bridge_status"] == "OK_P83B_LOCAL_BRIDGE_DRYRUN_MODULE_READY"
        and pack["contract_status"] == "OK_P81R_P82_LIVE_SHEETS_CONTRACT_READY"
        and pack["write_route_count"] == 0
        and pack["blocked_route_count"] == 0
    )

    if not decision_allowed:
        status = "BLOCKED_P86_UNKNOWN_OPERATOR_DECISION"
        next_step = "REVIEW_DECISION_INPUT"
    elif decision == "GO_LOCAL_OPERATOR_OUTPUT_PACK" and prerequisites_ok:
        status = "OK_P86_OPERATOR_DECISION_GATE_GO"
        next_step = "P87_SHEETS_READONLY_CONNECTOR_DRYRUN_OR_P87_LOCAL_RELEASE_PACK"
    elif decision == "HOLD_HUMAN_REVIEW":
        status = "REVIEW_REQUIRED_P86_OPERATOR_HOLD"
        next_step = "WAIT_HUMAN_REVIEW"
    else:
        status = "STOPPED_P86_NO_ACTION"
        next_step = "NO_ACTION"

    return {
        "step": "P86_OPERATOR_DECISION_GATE_FAST_FUSE",
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "operator": operator,
        "decision": decision,
        "decision_allowed": decision_allowed,
        "prerequisites_ok": prerequisites_ok,
        "pack_status": pack["status"],
        "bridge_status": pack["bridge_status"],
        "contract_status": pack["contract_status"],
        "planned_route_count": pack["planned_route_count"],
        "ready_route_count": pack["ready_route_count"],
        "human_approval_required_count": pack["human_approval_required_count"],
        "blocked_route_count": pack["blocked_route_count"],
        "write_route_count": pack["write_route_count"],
        "operator_pack": pack,
        "sheet_write": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "google_rest_local_diag": False,
        "next": next_step,
    }


def render_operator_decision_gate_markdown(gate: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# MVP QAIC — P86 Operator Decision Gate",
            "",
            f"- status: `{gate['status']}`",
            f"- operator: `{gate['operator']}`",
            f"- decision: `{gate['decision']}`",
            f"- prerequisites_ok: `{gate['prerequisites_ok']}`",
            f"- pack_status: `{gate['pack_status']}`",
            f"- bridge_status: `{gate['bridge_status']}`",
            f"- contract_status: `{gate['contract_status']}`",
            f"- write_route_count: `{gate['write_route_count']}`",
            f"- blocked_route_count: `{gate['blocked_route_count']}`",
            f"- next: `{gate['next']}`",
            "",
            "## Safety",
            "",
            "- NO_SHEET_WRITE",
            "- NO_APPS_SCRIPT_EXECUTION",
            "- NO_CLASP_PUSH",
            "- NO_BROKER_ORDER_SIZING",
            "- NO_GOOGLE_REST_LOCAL_DIAG",
            "",
            "## Embedded operator pack",
            "",
            render_operator_output_markdown(gate["operator_pack"]),
            "",
        ]
    )


def export_operator_decision_gate(
    out_dir: str | Path,
    *,
    operator: str = "JULIEN",
    decision: str = "GO_LOCAL_OPERATOR_OUTPUT_PACK",
) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    gate = build_operator_decision_gate(operator=operator, decision=decision)
    md = render_operator_decision_gate_markdown(gate)
    json_path = target / "P86_OPERATOR_DECISION_GATE.json"
    md_path = target / "P86_OPERATOR_DECISION_GATE.md"
    json_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(md, encoding="utf-8")
    return {
        "status": gate["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": gate["next"],
    }
