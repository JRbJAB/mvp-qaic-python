from __future__ import annotations

import json

from mvp_qaic_py.sheets.decision_journal_append_evidence import (
    assert_p96b_live_journal_append_safe,
    build_p96b_live_journal_append_evidence,
    export_p96b_live_journal_append_evidence,
    render_p96b_live_journal_append_markdown,
)


def test_p96b_live_journal_append_evidence_ready() -> None:
    payload = build_p96b_live_journal_append_evidence()
    assert payload["status"] == "OK_P96B_LIVE_JOURNAL_APPEND_VERIFIED"
    assert payload["decision_journal_sheet"] == "🧾 DECISION_JOURNAL"
    assert payload["decision_journal_range"] == "BJ17:CN17"
    assert payload["queue_sheet"] == "📤 JOURNAL_APPEND_QUEUE"
    assert payload["queue_range"] == "A9:Z9"
    assert payload["journal_id"] == "DJ-P96B-P93-CQW-20260621-200001"
    assert payload["journal_queue_id"] == "P93-CQW-20260621-200001"
    assert payload["final_human_decision"] == "APPROVE_APPEND"
    assert payload["validation_status"] == "P96B_LIVE_JOURNAL_APPEND_VALIDATED"


def test_p96b_write_flags_are_expected_but_no_broker_action() -> None:
    payload = build_p96b_live_journal_append_evidence()
    assert_p96b_live_journal_append_safe(payload)
    assert payload["sheet_write_executed"] is True
    assert payload["decision_journal_write"] is True
    assert payload["journal_append_executed"] is True
    assert payload["queue_status_updated"] is True
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["broker_execution"] is False
    assert payload["order_execution"] is False
    assert payload["auto_sizing_execution"] is False


def test_p96b_queue_status_after_append() -> None:
    payload = build_p96b_live_journal_append_evidence()
    assert payload["queue_append_status_after"] == "APPENDED_TO_DECISION_JOURNAL"
    assert payload["queue_journal_id_after"] == "DJ-P96B-P93-CQW-20260621-200001"
    assert payload["blockers"] == "NONE"


def test_p96b_markdown_contains_append_evidence() -> None:
    markdown = render_p96b_live_journal_append_markdown(build_p96b_live_journal_append_evidence())
    assert "P96B Live Journal Append Evidence" in markdown
    assert "BJ17:CN17" in markdown
    assert "APPROVE_APPEND" in markdown
    assert "audit journal only" in markdown


def test_p96b_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_p96b_live_journal_append_evidence(tmp_path)
    assert result["status"] == "OK_P96B_LIVE_JOURNAL_APPEND_VERIFIED"
    payload = json.loads(
        (tmp_path / "P96B_LIVE_JOURNAL_APPEND_EVIDENCE.json").read_text(encoding="utf-8")
    )
    markdown = (tmp_path / "P96B_LIVE_JOURNAL_APPEND_EVIDENCE.md").read_text(encoding="utf-8")
    assert payload["journal_id"] == "DJ-P96B-P93-CQW-20260621-200001"
    assert "P96B Live Journal Append Evidence" in markdown
