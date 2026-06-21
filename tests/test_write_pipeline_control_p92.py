from __future__ import annotations

import json

import pytest

from mvp_qaic_py.sheets.write_pipeline_control import (
    P92_APPROVAL_TOKEN,
    assert_write_pipeline_control_safe,
    build_write_pipeline_control,
    export_write_pipeline_control,
    render_write_pipeline_control_markdown,
)


def test_p92_control_ready_no_live_write() -> None:
    payload = build_write_pipeline_control()
    assert payload["status"] == "OK_P92_WRITE_PIPELINE_CONTROL_READY_NO_LIVE_WRITE"
    assert payload["sheet_write_executed"] is False
    assert payload["p91_status"] == "OK_P91_LIVE_WRITE_SMOKE_ROW_VERIFIED"
    assert payload["last_smoke_row"] == "A8:Z8"
    assert payload["blockers"] == []


def test_p92_safety_flags() -> None:
    payload = build_write_pipeline_control()
    assert_write_pipeline_control_safe(payload)
    assert payload["direct_decision_journal_write"] is False
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["broker_execution"] is False
    assert payload["order_execution"] is False
    assert payload["auto_sizing_execution"] is False


def test_p92_blocks_direct_decision_journal_target() -> None:
    payload = build_write_pipeline_control(target_sheet="🧾 DECISION_JOURNAL")
    assert payload["status"] == "BLOCKED_P92_WRITE_PIPELINE_CONTROL"
    assert "DIRECT_DECISION_JOURNAL_WRITE_BLOCKED" in payload["blockers"]
    with pytest.raises(ValueError, match="Direct Decision Journal write"):
        assert_write_pipeline_control_safe(payload)


def test_p92_live_write_enable_requires_token() -> None:
    payload = build_write_pipeline_control(live_write_enabled=True)
    assert payload["status"] == "BLOCKED_P92_WRITE_PIPELINE_CONTROL"
    assert "MISSING_P92_APPROVAL_TOKEN" in payload["blockers"]


def test_p92_live_write_enable_ready_with_token() -> None:
    payload = build_write_pipeline_control(
        live_write_enabled=True,
        approval_token=P92_APPROVAL_TOKEN,
    )
    assert payload["status"] == "REVIEW_REQUIRED_P92_READY_FOR_CONTROLLED_QUEUE_WRITE"
    assert payload["sheet_write_executed"] is False


def test_p92_markdown_contains_control_status() -> None:
    markdown = render_write_pipeline_control_markdown(build_write_pipeline_control())
    assert "P92 Write Pipeline Control" in markdown
    assert "OK_P92_WRITE_PIPELINE_CONTROL_READY_NO_LIVE_WRITE" in markdown
    assert "no second live write" in markdown


def test_p92_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_write_pipeline_control(tmp_path)
    assert result["status"] == "OK_P92_WRITE_PIPELINE_CONTROL_READY_NO_LIVE_WRITE"
    payload = json.loads((tmp_path / "P92_WRITE_PIPELINE_CONTROL.json").read_text(encoding="utf-8"))
    markdown = (tmp_path / "P92_WRITE_PIPELINE_CONTROL.md").read_text(encoding="utf-8")
    assert payload["status"] == "OK_P92_WRITE_PIPELINE_CONTROL_READY_NO_LIVE_WRITE"
    assert "P92 Write Pipeline Control" in markdown
