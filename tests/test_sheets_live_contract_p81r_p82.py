from __future__ import annotations

from mvp_qaic_py.contracts.sheets_live_contract import (
    LEGACY_FAKE_REQUIRED_TABS,
    LIVE_CANONICAL_GROUPS,
    validate_p81r_live_mapping,
    validate_p81r_p82_contract,
    validate_p82_header_contract,
)

LIVE_AVAILABLE_TABS = [
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
]

LIVE_HEADERS = {
    "GPT_INPUT_PAYLOADS": [
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
    ],
    "QAIC_RUNTIME_BRIDGE_STATUS": [
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
    ],
    "🎛️ BENCHMARK_AI_TRADE": [
        "section",
        "key",
        "value",
        "score_or_status",
        "source_url",
        "decision",
        "notes",
    ],
}


def test_p81r_live_canonical_mapping_passes_without_legacy_fake_tabs() -> None:
    result = validate_p81r_live_mapping(LIVE_AVAILABLE_TABS)
    assert result["status"] == "OK_P81R_LIVE_CANONICAL_MAPPING_READY"
    assert result["ok_group_count"] == len(LIVE_CANONICAL_GROUPS)
    assert result["missing_groups"] == []
    for fake_tab in LEGACY_FAKE_REQUIRED_TABS:
        assert fake_tab not in LIVE_AVAILABLE_TABS


def test_p81r_missing_entire_group_requires_review() -> None:
    tabs = [
        tab
        for tab in LIVE_AVAILABLE_TABS
        if tab
        not in {
            "QAIC_RUNTIME_BRIDGE_STATUS",
            "🤖 AI_RUNTIME_REFERENCE",
            "GPT_TOOL_BRIDGE",
        }
    ]
    result = validate_p81r_live_mapping(tabs)
    assert result["status"] == "REVIEW_REQUIRED_P81R_CANONICAL_GROUPS_MISSING"
    assert result["missing_groups"] == ["runtime_status_bridge"]


def test_p82_header_contract_passes_with_live_verified_headers() -> None:
    result = validate_p82_header_contract(LIVE_HEADERS)
    assert result["status"] == "OK_HEADER_CONTRACT_READY"
    assert result["gap_count"] == 0
    assert result["sheet_write"] is False
    assert result["broker_execution"] is False
    assert result["order_execution"] is False


def test_p82_header_gap_requires_review() -> None:
    headers = dict(LIVE_HEADERS)
    headers["GPT_INPUT_PAYLOADS"] = ["payload_id", "created_at"]
    result = validate_p82_header_contract(headers)
    assert result["status"] == "REVIEW_REQUIRED_HEADER_GAP"
    assert result["gap_count"] == 1
    assert "prompt_id" in result["gaps"][0]["missing_headers"]


def test_p82_write_attempt_is_blocked() -> None:
    result = validate_p82_header_contract(LIVE_HEADERS, requested_write=True)
    assert result["status"] == "BLOCKED_UNSAFE_WRITE_ATTEMPT"
    assert result["sheet_write"] is False


def test_p81r_p82_combined_contract_ready() -> None:
    result = validate_p81r_p82_contract(LIVE_AVAILABLE_TABS, LIVE_HEADERS)
    assert result["status"] == "OK_P81R_P82_LIVE_SHEETS_CONTRACT_READY"
