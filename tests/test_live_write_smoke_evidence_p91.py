from __future__ import annotations

import json

from mvp_qaic_py.sheets.live_write_smoke_evidence import (
    assert_p91_live_write_smoke_safe,
    build_p91_live_write_smoke_evidence,
    export_p91_live_write_smoke_evidence,
    render_p91_live_write_smoke_markdown,
)


def test_p91_live_write_smoke_evidence_ready() -> None:
    payload = build_p91_live_write_smoke_evidence()
    assert payload["status"] == "OK_P91_LIVE_WRITE_SMOKE_ROW_VERIFIED"
    assert payload["sheet_name"] == "📤 JOURNAL_APPEND_QUEUE"
    assert payload["range"] == "A8:Z8"
    assert payload["journal_queue_id"] == "P91-SMOKE-20260621-195001"
    assert payload["human_review_decision"] == "DO_NOT_APPEND"
    assert payload["safe_to_append"] == "NO"
    assert payload["append_status"] == "SMOKE_ONLY_DO_NOT_APPEND"
    assert payload["validation_status"] == "P91_SMOKE_VALIDATED"


def test_p91_live_write_smoke_safety() -> None:
    payload = build_p91_live_write_smoke_evidence()
    assert_p91_live_write_smoke_safe(payload)
    assert payload["sheet_write_executed"] is True
    assert payload["direct_decision_journal_write"] is False
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["broker_execution"] is False
    assert payload["order_execution"] is False
    assert payload["auto_sizing_execution"] is False


def test_p91_markdown_contains_live_write_evidence() -> None:
    markdown = render_p91_live_write_smoke_markdown(build_p91_live_write_smoke_evidence())
    assert "P91 Live Write Smoke Evidence" in markdown
    assert "OK_P91_LIVE_WRITE_SMOKE_ROW_VERIFIED" in markdown
    assert "DO_NOT_APPEND" in markdown
    assert "A8:Z8" in markdown


def test_p91_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_p91_live_write_smoke_evidence(tmp_path)
    assert result["status"] == "OK_P91_LIVE_WRITE_SMOKE_ROW_VERIFIED"
    payload = json.loads(
        (tmp_path / "P91_LIVE_WRITE_SMOKE_EVIDENCE.json").read_text(encoding="utf-8")
    )
    markdown = (tmp_path / "P91_LIVE_WRITE_SMOKE_EVIDENCE.md").read_text(encoding="utf-8")
    assert payload["journal_queue_id"] == "P91-SMOKE-20260621-195001"
    assert "P91 Live Write Smoke Evidence" in markdown
