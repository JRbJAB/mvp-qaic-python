from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from mvp_qaic_py.bridge.local_bridge_dryrun import (
    assert_local_bridge_is_readonly,
    build_local_bridge_dryrun_payload,
)

SAFE_OPERATOR_ACTIONS: tuple[str, ...] = (
    "REVIEW_ONLY",
    "EXPORT_LOCAL_ONLY",
    "HUMAN_DECISION_PREP",
)


def build_operator_output_pack(
    *,
    operator: str = "JULIEN",
    requested_action: str = "REVIEW_ONLY",
) -> dict[str, Any]:
    bridge_payload = build_local_bridge_dryrun_payload()
    assert_local_bridge_is_readonly(bridge_payload)

    action_allowed = requested_action in SAFE_OPERATOR_ACTIONS
    blocked_reason = None if action_allowed else "UNSAFE_OR_UNKNOWN_OPERATOR_ACTION"

    routes = bridge_payload["planned_routes"]
    ready_routes = [route for route in routes if route["status"] == "READY"]
    human_routes = [route for route in routes if route["status"] == "HUMAN_APPROVAL_REQUIRED"]
    blocked_routes = [route for route in routes if str(route["status"]).startswith("BLOCKED")]

    status = (
        "OK_P85A_OPERATOR_OUTPUT_PACK_READY"
        if action_allowed and not blocked_routes
        else "BLOCKED_P85A_OPERATOR_OUTPUT_PACK"
    )

    return {
        "step": "P85A_OPERATOR_OUTPUT_PACK_LOCAL_ONLY",
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "operator": operator,
        "requested_action": requested_action,
        "action_allowed": action_allowed,
        "blocked_reason": blocked_reason,
        "bridge_status": bridge_payload["status"],
        "contract_status": bridge_payload["contract_status"],
        "planned_route_count": bridge_payload["planned_route_count"],
        "ready_route_count": len(ready_routes),
        "human_approval_required_count": len(human_routes),
        "blocked_route_count": len(blocked_routes),
        "write_route_count": bridge_payload["write_route_count"],
        "routes": routes,
        "operator_summary": {
            "decision_mode": "HUMAN_REVIEW_ONLY",
            "primary_action": "review routes and prepare human decision",
            "journal_action": "APPROVE_APPEND_REQUIRED_BEFORE_ANY_JOURNAL_APPEND",
            "runtime_bridge": "READ_ONLY",
        },
        "sheet_write": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "google_rest_local_diag": False,
        "next": "P85B_LOCAL_OUTPUT_RENDER_OR_P86_DECISION",
    }


def render_operator_output_markdown(pack: dict[str, Any]) -> str:
    lines = [
        "# MVP QAIC — P85A Operator Output Pack",
        "",
        f"- status: `{pack['status']}`",
        f"- operator: `{pack['operator']}`",
        f"- requested_action: `{pack['requested_action']}`",
        f"- bridge_status: `{pack['bridge_status']}`",
        f"- contract_status: `{pack['contract_status']}`",
        f"- planned_route_count: `{pack['planned_route_count']}`",
        f"- ready_route_count: `{pack['ready_route_count']}`",
        f"- human_approval_required_count: `{pack['human_approval_required_count']}`",
        f"- blocked_route_count: `{pack['blocked_route_count']}`",
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
        "## Routes",
        "",
        "| route_id | source | target | mode | status | write_allowed |",
        "|---|---|---|---|---|---|",
    ]

    for route in pack["routes"]:
        lines.append(
            "| {route_id} | {source_tab} | {target_tab} | {mode} | {status} | {write_allowed} |".format(
                route_id=route["route_id"],
                source_tab=route["source_tab"],
                target_tab=route["target_tab"] or "",
                mode=route["mode"],
                status=route["status"],
                write_allowed=route["write_allowed"],
            )
        )

    lines.extend(
        [
            "",
            "## Next",
            "",
            f"`{pack['next']}`",
            "",
        ]
    )
    return "\n".join(lines)
