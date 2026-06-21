from __future__ import annotations

import json

from mvp_qaic_py.sheets.approve_append_gate import (
    APPROVE_APPEND_TOKEN,
    assert_approve_append_gate_safe,
    build_approve_append_gate,
    export_approve_append_gate,
    render_approve_append_gate_markdown,
)


def test_p94_gate_ready_hold_no_live_write() -> None:
    payload = build_approve_append_gate()
    assert payload["status"] == "OK_P94_APPROVE_APPEND_GATE_READY_HOLD_NO_LIVE_WRITE"
    assert payload["sheet_write_executed"] is False
    assert payload["current_human_review_decision"] == "DO_NOT_APPEND"
    assert payload["current_safe_to_append"] == "NO"
    assert payload["blockers"] == []


def test_p94_gate_blocks_missing_token_when_approval_requested() -> None:
    payload = build_approve_append_gate(approve_append_requested=True)
    assert payload["status"] == "BLOCKED_P94_APPROVE_APPEND_GATE"
    assert "MISSING_APPROVE_APPEND_TOKEN" in payload["blockers"]


def test_p94_gate_ready_for_p95_with_token_but_no_write() -> None:
    payload = build_approve_append_gate(
        approve_append_requested=True,
        approval_token=APPROVE_APPEND_TOKEN,
    )
    assert payload["status"] == "REVIEW_REQUIRED_P94_READY_FOR_P95_APPROVE_APPEND_FLIP"
    assert payload["planned_human_review_decision"] == "APPROVE_APPEND"
    assert payload["planned_safe_to_append"] == "YES"
    assert payload["sheet_write_executed"] is False


def test_p94_gate_blocks_direct_decision_journal_target() -> None:
    payload = build_approve_append_gate(target_sheet="🧾 DECISION_JOURNAL")
    assert payload["status"] == "BLOCKED_P94_APPROVE_APPEND_GATE"
    assert "DIRECT_DECISION_JOURNAL_WRITE_BLOCKED" in payload["blockers"]


def test_p94_safety_flags() -> None:
    payload = build_approve_append_gate()
    assert_approve_append_gate_safe(payload)
    assert payload["direct_decision_journal_write"] is False
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["broker_execution"] is False
    assert payload["order_execution"] is False
    assert payload["auto_sizing_execution"] is False


def test_p94_markdown_contains_decision_fields() -> None:
    markdown = render_approve_append_gate_markdown(build_approve_append_gate())
    assert "P94 Approve Append Gate" in markdown
    assert "DO_NOT_APPEND" in markdown
    assert "no direct Decision Journal write" in markdown


def test_p94_export(tmp_path) -> None:
    result = export_approve_append_gate(tmp_path)
    assert result["status"] == "OK_P94_APPROVE_APPEND_GATE_READY_HOLD_NO_LIVE_WRITE"
    payload = json.loads((tmp_path / "P94_APPROVE_APPEND_GATE.json").read_text(encoding="utf-8"))
    markdown = (tmp_path / "P94_APPROVE_APPEND_GATE.md").read_text(encoding="utf-8")
    assert payload["journal_queue_id"] == "P93-CQW-20260621-200001"
    assert "P94 Approve Append Gate" in markdown
