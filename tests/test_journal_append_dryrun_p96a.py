from __future__ import annotations

import json

from mvp_qaic_py.sheets.journal_append_dryrun import (
    assert_journal_append_dryrun_safe,
    build_journal_append_dryrun,
    export_journal_append_dryrun,
    render_journal_append_dryrun_markdown,
)


def test_p96a_journal_append_dryrun_ready() -> None:
    payload = build_journal_append_dryrun()
    assert payload["status"] == "OK_P96A_JOURNAL_APPEND_DRYRUN_READY_NO_LIVE_WRITE"
    assert payload["target_sheet"] == "🧾 DECISION_JOURNAL"
    assert payload["source_sheet"] == "📤 JOURNAL_APPEND_QUEUE"
    assert payload["source_range"] == "A9:Z9"
    assert payload["journal_queue_id"] == "P93-CQW-20260621-200001"
    assert payload["journal_record"]["append_status"] == "DRYRUN_READY_FOR_JOURNAL_APPEND"


def test_p96a_does_not_write_any_live_surface() -> None:
    payload = build_journal_append_dryrun()
    assert_journal_append_dryrun_safe(payload)
    assert payload["sheet_write_executed"] is False
    assert payload["decision_journal_write"] is False
    assert payload["journal_append_executed"] is False
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["broker_execution"] is False
    assert payload["order_execution"] is False
    assert payload["auto_sizing_execution"] is False


def test_p96a_blocks_live_append_request() -> None:
    payload = build_journal_append_dryrun(request_live_append=True)
    assert payload["status"] == "BLOCKED_P96A_JOURNAL_APPEND_DRYRUN"
    assert "LIVE_APPEND_NOT_ALLOWED_IN_P96A" in payload["blockers"]


def test_p96a_blocks_unapproved_queue_row() -> None:
    payload = build_journal_append_dryrun(
        queue_row={
            "sheet_name": "📤 JOURNAL_APPEND_QUEUE",
            "range": "A9:Z9",
            "journal_queue_id": "P93-CQW-20260621-200001",
            "human_review_decision": "DO_NOT_APPEND",
            "safe_to_append": "NO",
            "append_status": "CONTROLLED_QUEUE_WRITE_PENDING_REVIEW",
            "validation_status": "P93_CONTROLLED_QUEUE_WRITE_VALIDATED",
            "risk_guard": "HUMAN_REVIEW_ONLY_NO_BROKER_NO_ORDER_NO_SIZING",
            "journal_append_executed": False,
        }
    )
    assert payload["status"] == "BLOCKED_P96A_JOURNAL_APPEND_DRYRUN"
    assert "APPROVE_APPEND_MISSING" in payload["blockers"]
    assert "SAFE_TO_APPEND_NOT_YES" in payload["blockers"]


def test_p96a_markdown_contains_dryrun_contract() -> None:
    markdown = render_journal_append_dryrun_markdown(build_journal_append_dryrun())
    assert "P96A Journal Append Dryrun" in markdown
    assert "dry-run only in P96A" in markdown
    assert "DRYRUN_READY_FOR_JOURNAL_APPEND" in markdown


def test_p96a_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_journal_append_dryrun(tmp_path)
    assert result["status"] == "OK_P96A_JOURNAL_APPEND_DRYRUN_READY_NO_LIVE_WRITE"
    payload = json.loads((tmp_path / "P96A_JOURNAL_APPEND_DRYRUN.json").read_text(encoding="utf-8"))
    markdown = (tmp_path / "P96A_JOURNAL_APPEND_DRYRUN.md").read_text(encoding="utf-8")
    assert payload["journal_record"]["journal_id"] == ("DJ-DRYRUN-P93-CQW-20260621-200001")
    assert "P96A Journal Append Dryrun" in markdown
