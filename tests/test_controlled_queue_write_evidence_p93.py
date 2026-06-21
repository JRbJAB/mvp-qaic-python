from __future__ import annotations

import json

from mvp_qaic_py.sheets.controlled_queue_write_evidence import (
    assert_p93_controlled_queue_write_safe,
    build_p93_controlled_queue_write_evidence,
    export_p93_controlled_queue_write_evidence,
    render_p93_controlled_queue_write_markdown,
)


def test_p93_controlled_queue_write_evidence_ready() -> None:
    payload = build_p93_controlled_queue_write_evidence()
    assert payload["status"] == "OK_P93_CONTROLLED_QUEUE_WRITE_ROW_VERIFIED"
    assert payload["sheet_name"] == "📤 JOURNAL_APPEND_QUEUE"
    assert payload["range"] == "A9:Z9"
    assert payload["journal_queue_id"] == "P93-CQW-20260621-200001"
    assert payload["human_review_decision"] == "DO_NOT_APPEND"
    assert payload["safe_to_append"] == "NO"
    assert payload["append_status"] == "CONTROLLED_QUEUE_WRITE_PENDING_REVIEW"
    assert payload["validation_status"] == "P93_CONTROLLED_QUEUE_WRITE_VALIDATED"


def test_p93_controlled_queue_write_safety() -> None:
    payload = build_p93_controlled_queue_write_evidence()
    assert_p93_controlled_queue_write_safe(payload)
    assert payload["sheet_write_executed"] is True
    assert payload["direct_decision_journal_write"] is False
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["broker_execution"] is False
    assert payload["order_execution"] is False
    assert payload["auto_sizing_execution"] is False


def test_p93_markdown_contains_evidence() -> None:
    markdown = render_p93_controlled_queue_write_markdown(
        build_p93_controlled_queue_write_evidence()
    )
    assert "P93 Controlled Queue Write Evidence" in markdown
    assert "OK_P93_CONTROLLED_QUEUE_WRITE_ROW_VERIFIED" in markdown
    assert "DO_NOT_APPEND" in markdown
    assert "A9:Z9" in markdown


def test_p93_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_p93_controlled_queue_write_evidence(tmp_path)
    assert result["status"] == "OK_P93_CONTROLLED_QUEUE_WRITE_ROW_VERIFIED"
    payload = json.loads(
        (tmp_path / "P93_CONTROLLED_QUEUE_WRITE_EVIDENCE.json").read_text(encoding="utf-8")
    )
    markdown = (tmp_path / "P93_CONTROLLED_QUEUE_WRITE_EVIDENCE.md").read_text(encoding="utf-8")
    assert payload["journal_queue_id"] == "P93-CQW-20260621-200001"
    assert "P93 Controlled Queue Write Evidence" in markdown
