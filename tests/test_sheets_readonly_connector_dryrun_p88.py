from __future__ import annotations

import json

import pytest

from mvp_qaic_py.sheets.readonly_connector_dryrun import (
    DEFAULT_READONLY_RANGES,
    assert_sheets_readonly_connector_dryrun_safe,
    build_sheets_readonly_connector_dryrun,
    export_sheets_readonly_connector_dryrun,
    render_sheets_readonly_connector_dryrun_markdown,
)


def test_p88_sheets_readonly_dryrun_ready() -> None:
    payload = build_sheets_readonly_connector_dryrun()
    assert payload["status"] == "OK_P88_SHEETS_READONLY_CONNECTOR_DRYRUN_READY"
    assert payload["contract_status"] == "OK_P81R_P82_LIVE_SHEETS_CONTRACT_READY"
    assert payload["release_status"] == "OK_P87_OPERATOR_RELEASE_PACK_READY"
    assert payload["requested_range_count"] == len(DEFAULT_READONLY_RANGES)
    assert payload["unknown_range_count"] == 0


def test_p88_safety_flags_are_false() -> None:
    payload = build_sheets_readonly_connector_dryrun()
    assert payload["sheet_write"] is False
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["broker_execution"] is False
    assert payload["order_execution"] is False
    assert payload["auto_sizing_execution"] is False
    assert payload["google_rest_local_diag"] is False
    assert payload["live_google_api_call"] is False
    assert payload["write_requested"] is False


def test_p88_blocks_write_request() -> None:
    payload = build_sheets_readonly_connector_dryrun(write_requested=True)
    assert payload["status"] == "BLOCKED_P88_SHEETS_READONLY_CONNECTOR_DRYRUN"
    with pytest.raises(ValueError, match="Unsafe P88 flags enabled"):
        assert_sheets_readonly_connector_dryrun_safe(payload)


def test_p88_blocks_unknown_range() -> None:
    payload = build_sheets_readonly_connector_dryrun(ranges=("UNKNOWN!A1:B2",))
    assert payload["status"] == "BLOCKED_P88_SHEETS_READONLY_CONNECTOR_DRYRUN"
    assert payload["unknown_range_count"] == 1
    with pytest.raises(ValueError, match="Unknown ranges blocked"):
        assert_sheets_readonly_connector_dryrun_safe(payload)


def test_p88_markdown_contains_safety_and_ranges() -> None:
    markdown = render_sheets_readonly_connector_dryrun_markdown(
        build_sheets_readonly_connector_dryrun()
    )
    assert "P88 Sheets Readonly Connector Dry-Run" in markdown
    assert "NO_SHEET_WRITE" in markdown
    assert "NO_LIVE_GOOGLE_API_CALL" in markdown
    assert "GPT_INPUT_PAYLOADS!A1:M2" in markdown


def test_p88_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_sheets_readonly_connector_dryrun(tmp_path)
    assert result["status"] == "OK_P88_SHEETS_READONLY_CONNECTOR_DRYRUN_READY"
    payload = json.loads(
        (tmp_path / "P88_SHEETS_READONLY_CONNECTOR_DRYRUN.json").read_text(encoding="utf-8")
    )
    markdown = (tmp_path / "P88_SHEETS_READONLY_CONNECTOR_DRYRUN.md").read_text(encoding="utf-8")
    assert payload["status"] == "OK_P88_SHEETS_READONLY_CONNECTOR_DRYRUN_READY"
    assert "P88 Sheets Readonly Connector Dry-Run" in markdown
