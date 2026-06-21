from __future__ import annotations

import json

import pytest

from mvp_qaic_py.sheets.write_capable_contract import (
    APPROVAL_TOKEN,
    assert_p90_contract_safe,
    build_sheets_write_capable_contract,
    export_sheets_write_capable_contract,
    render_sheets_write_capable_contract_markdown,
)


def test_p90_write_capable_ready_disabled_by_default() -> None:
    payload = build_sheets_write_capable_contract()
    assert payload["status"] == ("OK_P90_SHEETS_WRITE_CAPABLE_CONTRACT_READY_DISABLED_BY_DEFAULT")
    assert payload["write_capable"] is True
    assert payload["write_enabled_default"] is False
    assert payload["write_enabled_requested"] is False
    assert payload["sheet_write_executed"] is False
    assert payload["blockers"] == []


def test_p90_safety_flags_are_false() -> None:
    payload = build_sheets_write_capable_contract()
    assert payload["sheet_write"] is False
    assert payload["sheet_write_executed"] is False
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["broker_execution"] is False
    assert payload["order_execution"] is False
    assert payload["auto_sizing_execution"] is False
    assert payload["live_google_api_call"] is False


def test_p90_blocks_direct_decision_journal_write() -> None:
    payload = build_sheets_write_capable_contract(target_sheet="🧾 DECISION_JOURNAL")
    assert payload["status"] == "BLOCKED_P90_SHEETS_WRITE_CAPABLE_CONTRACT"
    assert "DIRECT_TARGET_BLOCKED" in payload["blockers"]
    with pytest.raises(ValueError, match="Blocked direct target"):
        assert_p90_contract_safe(payload)


def test_p90_write_enable_requires_approval_token() -> None:
    payload = build_sheets_write_capable_contract(write_enabled=True)
    assert payload["status"] == "BLOCKED_P90_SHEETS_WRITE_CAPABLE_CONTRACT"
    assert "MISSING_APPROVAL_TOKEN_FOR_WRITE_ENABLE" in payload["blockers"]


def test_p90_write_enable_request_ready_for_p91_with_token() -> None:
    payload = build_sheets_write_capable_contract(
        write_enabled=True,
        approval_token=APPROVAL_TOKEN,
    )
    assert payload["status"] == "REVIEW_REQUIRED_P90_WRITE_ENABLE_REQUEST_READY_FOR_P91"
    assert payload["sheet_write_executed"] is False
    assert payload["approval_token_ok"] is True


def test_p90_markdown_contains_write_capable_safety() -> None:
    markdown = render_sheets_write_capable_contract_markdown(build_sheets_write_capable_contract())
    assert "P90 Sheets Write-Capable Contract" in markdown
    assert "WRITE_ENABLED_DEFAULT_FALSE" in markdown
    assert "NO_SHEET_WRITE_EXECUTED" in markdown
    assert "📤 JOURNAL_APPEND_QUEUE" in markdown


def test_p90_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_sheets_write_capable_contract(tmp_path)
    assert result["status"] == ("OK_P90_SHEETS_WRITE_CAPABLE_CONTRACT_READY_DISABLED_BY_DEFAULT")
    payload = json.loads(
        (tmp_path / "P90_SHEETS_WRITE_CAPABLE_CONTRACT.json").read_text(encoding="utf-8")
    )
    markdown = (tmp_path / "P90_SHEETS_WRITE_CAPABLE_CONTRACT.md").read_text(encoding="utf-8")
    assert payload["write_capable"] is True
    assert "P90 Sheets Write-Capable Contract" in markdown
