from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mvp_qaic_py.contracts.sheets_live_contract import (
    SPREADSHEET_ID,
    SPREADSHEET_TITLE,
    validate_p81r_p82_contract,
)

SAFETY_FLAGS: dict[str, bool] = {
    "sheet_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker_execution": False,
    "order_execution": False,
    "auto_sizing_execution": False,
    "google_rest_local_diag": False,
}

LIVE_AVAILABLE_TABS: tuple[str, ...] = (
    "GPT_INPUT_PAYLOADS",
    "GPT_TRADE_PLAN_RUNTIME_REQUIREMENTS",
    "🧪 GPT_RESPONSE_INTAKE",
    "🧾 DECISION_JOURNAL",
    "🚀 PROMPT_RUN_QUEUE",
    "📥 RESPONSE_INTAKE_QUEUE",
    "📤 JOURNAL_APPEND_QUEUE",
    "QAIC_RUNTIME_BRIDGE_STATUS",
    "🤖 AI_RUNTIME_REFERENCE",
    "GPT_TOOL_BRIDGE",
    "🚦 MVPQAIC_APPSHEET_GO_NO_GO_GATE",
    "🎛️ PROMPT_WORKFLOW_CONTROL",
    "🎛️ BENCHMARK_AI_TRADE",
)

LIVE_HEADERS: dict[str, tuple[str, ...]] = {
    "GPT_INPUT_PAYLOADS": (
        "payload_id",
        "created_at",
        "prompt_id",
        "source_mode",
        "revolut_x_mode",
        "source_tables",
        "portfolio_snapshot_status",
        "generated_prompt",
        "expected_output_template",
        "status",
        "notes",
        "run_id",
        "validation_status",
    ),
    "QAIC_RUNTIME_BRIDGE_STATUS": (
        "stable_id",
        "component",
        "status",
        "current_mode",
        "target_mode",
        "source_table_or_system",
        "readiness_level",
        "blockers",
        "next_action",
        "safety_guard",
        "last_checked_at",
        "notes",
        "priority",
        "validation_status",
    ),
    "🎛️ BENCHMARK_AI_TRADE": (
        "section",
        "key",
        "value",
        "score_or_status",
        "source_url",
        "decision",
        "notes",
    ),
}


@dataclass(frozen=True)
class BridgeRoute:
    route_id: str
    source_tab: str
    target_tab: str | None
    mode: str
    write_allowed: bool
    human_approval_required: bool

    def to_dict(self, contract_ok: bool) -> dict[str, Any]:
        if not contract_ok:
            status = "BLOCKED_BY_CONTRACT"
        elif self.human_approval_required:
            status = "HUMAN_APPROVAL_REQUIRED"
        else:
            status = "READY"

        return {
            "route_id": self.route_id,
            "source_tab": self.source_tab,
            "target_tab": self.target_tab,
            "mode": self.mode,
            "write_allowed": self.write_allowed,
            "human_approval_required": self.human_approval_required,
            "status": status,
        }


LOCAL_BRIDGE_ROUTES: tuple[BridgeRoute, ...] = (
    BridgeRoute(
        "P83_ROUTE_PAYLOAD_TO_OPERATOR_REVIEW",
        "GPT_INPUT_PAYLOADS",
        "🚀 PROMPT_RUN_QUEUE",
        "DRY_RUN_ONLY",
        False,
        False,
    ),
    BridgeRoute(
        "P83_ROUTE_RESPONSE_INTAKE_TO_JOURNAL_QUEUE",
        "📥 RESPONSE_INTAKE_QUEUE",
        "📤 JOURNAL_APPEND_QUEUE",
        "DRY_RUN_ONLY",
        False,
        False,
    ),
    BridgeRoute(
        "P83_ROUTE_JOURNAL_QUEUE_TO_DECISION_JOURNAL",
        "📤 JOURNAL_APPEND_QUEUE",
        "🧾 DECISION_JOURNAL",
        "DRY_RUN_ONLY",
        False,
        True,
    ),
    BridgeRoute(
        "P83_ROUTE_RUNTIME_STATUS_READ",
        "QAIC_RUNTIME_BRIDGE_STATUS",
        None,
        "READ_ONLY",
        False,
        False,
    ),
)


def build_local_bridge_dryrun_payload(
    available_tabs: tuple[str, ...] = LIVE_AVAILABLE_TABS,
    observed_headers: dict[str, tuple[str, ...]] = LIVE_HEADERS,
) -> dict[str, Any]:
    contract = validate_p81r_p82_contract(available_tabs, observed_headers)
    contract_ok = contract["status"] == "OK_P81R_P82_LIVE_SHEETS_CONTRACT_READY"
    routes = [route.to_dict(contract_ok) for route in LOCAL_BRIDGE_ROUTES]

    status = (
        "OK_P83B_LOCAL_BRIDGE_DRYRUN_MODULE_READY"
        if contract_ok
        else "REVIEW_REQUIRED_P83B_CONTRACT_GAP"
    )

    return {
        "step": "P83B_LOCAL_BRIDGE_DRYRUN_MODULE",
        "status": status,
        "spreadsheet_id": SPREADSHEET_ID,
        "spreadsheet_title": SPREADSHEET_TITLE,
        "contract_status": contract["status"],
        "planned_route_count": len(routes),
        "planned_routes": routes,
        "write_route_count": sum(1 for route in routes if route["write_allowed"]),
        "human_approval_required_count": sum(
            1 for route in routes if route["human_approval_required"]
        ),
        "next": "P83C_PUSH_OR_P84_LOCAL_OPERATOR_BRIDGE_SMOKE"
        if contract_ok
        else "FIX_CONTRACT_GAP",
        **SAFETY_FLAGS,
    }


def assert_local_bridge_is_readonly(payload: dict[str, Any]) -> None:
    unsafe_flags = [
        "sheet_write",
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
        "google_rest_local_diag",
    ]
    enabled = [flag for flag in unsafe_flags if payload.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe bridge flags enabled: {enabled}")

    write_routes = [
        route for route in payload.get("planned_routes", []) if route.get("write_allowed")
    ]
    if write_routes:
        raise ValueError(f"Write routes are forbidden in P83B: {write_routes}")
