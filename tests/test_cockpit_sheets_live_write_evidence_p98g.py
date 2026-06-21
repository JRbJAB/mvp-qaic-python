from __future__ import annotations
import json
from mvp_qaic_py.release.cockpit_sheets_live_write_evidence import (
    assert_p98g_cockpit_sheets_live_write_safe,
    build_p98g_cockpit_sheets_live_write_evidence,
    export_p98g_cockpit_sheets_live_write_evidence,
    render_p98g_cockpit_sheets_live_write_markdown,
)


def test_p98g_evidence_ready() -> None:
    payload = build_p98g_cockpit_sheets_live_write_evidence()
    assert payload["status"] == "OK_P98G_COCKPIT_SHEETS_LIVE_WRITE_VERIFIED"
    assert payload["target_sheet_name"] == "QAIC_RUNTIME_COCKPIT_VIEW"
    assert payload["target_range"] == "QAIC_RUNTIME_COCKPIT_VIEW!A1:H24"
    assert payload["card_count"] == 17
    assert payload["status_cell"] == "P98G_LIVE_COCKPIT_SHEET_CREATED"


def test_p98g_safety_flags() -> None:
    payload = build_p98g_cockpit_sheets_live_write_evidence()
    assert_p98g_cockpit_sheets_live_write_safe(payload)
    assert payload["sheet_view_write_executed"] is True
    assert payload["decision_journal_write_in_p98g"] is False
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["broker_execution"] is False
    assert payload["order_execution"] is False
    assert payload["auto_sizing_execution"] is False
    assert payload["trading_action"] is False


def test_p98g_required_cards_include_benchmark_and_revolut() -> None:
    cards = set(build_p98g_cockpit_sheets_live_write_evidence()["required_cards"])
    assert "benchmark_status" in cards
    assert "lexique_readiness" in cards
    assert "risk_guard_status" in cards
    assert "revolut_readonly_status" in cards


def test_p98g_markdown_contains_evidence() -> None:
    markdown = render_p98g_cockpit_sheets_live_write_markdown(
        build_p98g_cockpit_sheets_live_write_evidence()
    )
    assert "P98G Cockpit Sheets Live Write Evidence" in markdown
    assert "QAIC_RUNTIME_COCKPIT_VIEW" in markdown
    assert "benchmark_status" in markdown
    assert "no Decision Journal write in P98G" in markdown


def test_p98g_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_p98g_cockpit_sheets_live_write_evidence(tmp_path)
    assert result["status"] == "OK_P98G_COCKPIT_SHEETS_LIVE_WRITE_VERIFIED"
    payload = json.loads(
        (tmp_path / "P98G_COCKPIT_SHEETS_LIVE_WRITE_EVIDENCE.json").read_text(encoding="utf-8")
    )
    markdown = (tmp_path / "P98G_COCKPIT_SHEETS_LIVE_WRITE_EVIDENCE.md").read_text(encoding="utf-8")
    assert payload["card_count"] == 17
    assert "QAIC_RUNTIME_COCKPIT_VIEW" in markdown
