from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

SPREADSHEET_ID = "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0"
SPREADSHEET_TITLE = "🛠️ MVP QAIC — Crypto Signal OS — DEV"
LIVE_VERIFIED_SHEET_COUNT = 131
DISQUALIFIED_LOCAL_DIAG = "LOCAL_POWERSHELL_GOOGLE_REST_DISQUALIFIED_FOR_P80_P81"

SAFETY_FLAGS: dict[str, bool] = {
    "sheet_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker_execution": False,
    "order_execution": False,
    "auto_sizing_execution": False,
    "google_rest_local_diag": False,
}

LEGACY_FAKE_REQUIRED_TABS: tuple[str, ...] = (
    "INPUT_TRADE_PLAN_REVIEW",
    "DECISION_JOURNAL_IMPORT",
    "OPERATOR_REVIEW_IMPORT",
    "RUNTIME_STATUS_VIEW",
    "HUMAN_APPROVAL_GATE",
)

LIVE_CANONICAL_GROUPS: dict[str, tuple[str, ...]] = {
    "trade_input_payload": (
        "GPT_INPUT_PAYLOADS",
        "GPT_TRADE_PLAN_RUNTIME_REQUIREMENTS",
        "🧪 GPT_RESPONSE_INTAKE",
    ),
    "decision_journal": ("🧾 DECISION_JOURNAL",),
    "operator_queues": (
        "🚀 PROMPT_RUN_QUEUE",
        "📥 RESPONSE_INTAKE_QUEUE",
        "📤 JOURNAL_APPEND_QUEUE",
    ),
    "runtime_status_bridge": (
        "QAIC_RUNTIME_BRIDGE_STATUS",
        "🤖 AI_RUNTIME_REFERENCE",
        "GPT_TOOL_BRIDGE",
    ),
    "human_approval_workflow": (
        "🚦 MVPQAIC_APPSHEET_GO_NO_GO_GATE",
        "🎛️ PROMPT_WORKFLOW_CONTROL",
    ),
    "benchmark_cockpit": ("🎛️ BENCHMARK_AI_TRADE",),
}

LIVE_HEADER_CONTRACTS: dict[str, tuple[str, ...]] = {
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

LIVE_VERIFIED_TABS: tuple[str, ...] = tuple(
    dict.fromkeys(tab for group in LIVE_CANONICAL_GROUPS.values() for tab in group)
)


def _norm_set(values: Iterable[str]) -> set[str]:
    return {str(value).strip() for value in values if str(value).strip()}


def safety_flags() -> dict[str, bool]:
    return dict(SAFETY_FLAGS)


def validate_p81r_live_mapping(available_tabs: Iterable[str]) -> dict[str, Any]:
    available = _norm_set(available_tabs)
    groups: list[dict[str, Any]] = []

    for group_name, candidates in LIVE_CANONICAL_GROUPS.items():
        present = [tab for tab in candidates if tab in available]
        groups.append(
            {
                "group": group_name,
                "status": "OK" if present else "MISSING_GROUP",
                "present_tabs": present,
                "accepted_any_of": list(candidates),
            }
        )

    missing_groups = [item["group"] for item in groups if item["status"] != "OK"]
    status = (
        "OK_P81R_LIVE_CANONICAL_MAPPING_READY"
        if not missing_groups
        else "REVIEW_REQUIRED_P81R_CANONICAL_GROUPS_MISSING"
    )

    return {
        "step": "P81R_LIVE_CANONICAL_MAPPING_REPAIR",
        "status": status,
        "spreadsheet_id": SPREADSHEET_ID,
        "spreadsheet_title": SPREADSHEET_TITLE,
        "live_verified_sheet_count": LIVE_VERIFIED_SHEET_COUNT,
        "legacy_fake_tabs_disqualified": list(LEGACY_FAKE_REQUIRED_TABS),
        "local_diag_status": DISQUALIFIED_LOCAL_DIAG,
        "required_group_count": len(LIVE_CANONICAL_GROUPS),
        "ok_group_count": len(LIVE_CANONICAL_GROUPS) - len(missing_groups),
        "missing_groups": missing_groups,
        "groups": groups,
        **SAFETY_FLAGS,
    }


def validate_p82_header_contract(
    observed_headers_by_tab: Mapping[str, Iterable[str]],
    *,
    requested_write: bool = False,
) -> dict[str, Any]:
    if requested_write:
        return {
            "step": "P82_HEADER_SAMPLE_READONLY_CONTRACT",
            "status": "BLOCKED_UNSAFE_WRITE_ATTEMPT",
            "reason": "P82 is read-only only.",
            **SAFETY_FLAGS,
        }

    gaps: list[dict[str, Any]] = []
    for tab, required_headers in LIVE_HEADER_CONTRACTS.items():
        observed = _norm_set(observed_headers_by_tab.get(tab, ()))
        missing = [header for header in required_headers if header not in observed]
        if missing:
            gaps.append({"tab": tab, "missing_headers": missing})

    return {
        "step": "P82_HEADER_SAMPLE_READONLY_CONTRACT",
        "status": "OK_HEADER_CONTRACT_READY" if not gaps else "REVIEW_REQUIRED_HEADER_GAP",
        "spreadsheet_id": SPREADSHEET_ID,
        "spreadsheet_title": SPREADSHEET_TITLE,
        "checked_tabs": list(LIVE_HEADER_CONTRACTS),
        "gap_count": len(gaps),
        "gaps": gaps,
        "local_diag_status": DISQUALIFIED_LOCAL_DIAG,
        **SAFETY_FLAGS,
    }


def validate_p81r_p82_contract(
    available_tabs: Iterable[str],
    observed_headers_by_tab: Mapping[str, Iterable[str]],
) -> dict[str, Any]:
    p81r = validate_p81r_live_mapping(available_tabs)
    p82 = validate_p82_header_contract(observed_headers_by_tab)
    status = (
        "OK_P81R_P82_LIVE_SHEETS_CONTRACT_READY"
        if p81r["status"].startswith("OK") and p82["status"].startswith("OK")
        else "REVIEW_REQUIRED_P81R_P82_CONTRACT_GAP"
    )
    return {
        "step": "P81R_P82_LIVE_SHEETS_CONTRACT",
        "status": status,
        "p81r": p81r,
        "p82": p82,
        **SAFETY_FLAGS,
    }
