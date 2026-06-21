from __future__ import annotations

import json

from mvp_qaic_py.sheets.approve_append_flip_evidence import (
    assert_p95_live_approve_append_flip_safe,
    build_p95_live_approve_append_flip_evidence,
    export_p95_live_approve_append_flip_evidence,
    render_p95_live_approve_append_flip_markdown,
)


def test_p95_live_approve_append_flip_evidence_ready() -> None:
    payload = build_p95_live_approve_append_flip_evidence()
    assert payload["status"] == "OK_P95_LIVE_APPROVE_APPEND_FLIP_VERIFIED"
    assert payload["sheet_name"] == "📤 JOURNAL_APPEND_QUEUE"
    assert payload["range"] == "A9:Z9"
    assert payload["journal_queue_id"] == "P93-CQW-20260621-200001"
    assert payload["human_review_decision"] == "APPROVE_APPEND"
    assert payload["safe_to_append"] == "YES"
    assert payload["append_status"] == "APPROVE_APPEND_PENDING_JOURNAL_APPEND"


def test_p95_safety_flags() -> None:
    payload = build_p95_live_approve_append_flip_evidence()
    assert_p95_live_approve_append_flip_safe(payload)
    assert payload["sheet_write_executed"] is True
    assert payload["journal_append_executed"] is False
    assert payload["direct_decision_journal_write"] is False
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["broker_execution"] is False
    assert payload["order_execution"] is False
    assert payload["auto_sizing_execution"] is False


def test_p95_markdown_contains_flip_evidence() -> None:
    markdown = render_p95_live_approve_append_flip_markdown(
        build_p95_live_approve_append_flip_evidence()
    )
    assert "P95 Live Approve Append Flip Evidence" in markdown
    assert "APPROVE_APPEND" in markdown
    assert "YES" in markdown
    assert "no journal append in P95" in markdown


def test_p95_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_p95_live_approve_append_flip_evidence(tmp_path)
    assert result["status"] == "OK_P95_LIVE_APPROVE_APPEND_FLIP_VERIFIED"
    payload = json.loads(
        (tmp_path / "P95_LIVE_APPROVE_APPEND_FLIP_EVIDENCE.json").read_text(encoding="utf-8")
    )
    markdown = (tmp_path / "P95_LIVE_APPROVE_APPEND_FLIP_EVIDENCE.md").read_text(encoding="utf-8")
    assert payload["safe_to_append"] == "YES"
    assert "P95 Live Approve Append Flip Evidence" in markdown
