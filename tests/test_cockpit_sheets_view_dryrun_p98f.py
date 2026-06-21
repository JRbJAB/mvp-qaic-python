from __future__ import annotations

import json

from mvp_qaic_py.release.cockpit_sheets_view_dryrun import (
    assert_cockpit_sheets_view_dryrun_safe,
    build_cockpit_sheets_view_dryrun,
    export_cockpit_sheets_view_dryrun,
    render_cockpit_sheets_view_dryrun_markdown,
)


def test_p98f_cockpit_sheets_view_dryrun_ready() -> None:
    payload = build_cockpit_sheets_view_dryrun()
    assert payload["status"] == "OK_P98F_COCKPIT_SHEETS_VIEW_DRYRUN_READY"
    assert payload["source_p98e_status"] == "OK_P98E_COCKPIT_UI_EXPORT_LOCAL_READY"
    assert payload["target_sheet_name"] == "QAIC_RUNTIME_COCKPIT_VIEW"
    assert payload["card_count"] == 17
    assert payload["blockers"] == []


def test_p98f_plan_is_dryrun_only_no_sheet_write() -> None:
    payload = build_cockpit_sheets_view_dryrun()
    assert_cockpit_sheets_view_dryrun_safe(payload)
    plan = payload["sheets_view_plan"]
    assert plan["target_action"] == "DRYRUN_ONLY_NO_SHEET_WRITE"
    assert plan["create_sheet_in_p98f"] is False
    assert plan["update_cells_in_p98f"] is False
    assert plan["write_rows_in_p98f"] is False
    assert plan["planned_row_count"] == 17


def test_p98f_includes_all_required_cockpit_cards() -> None:
    payload = build_cockpit_sheets_view_dryrun()
    card_ids = {row["card_id"] for row in payload["sheets_view_plan"]["planned_rows"]}
    assert "benchmark_status" in card_ids
    assert "lexique_readiness" in card_ids
    assert "method_library_status" in card_ids
    assert "signal_library_coverage" in card_ids
    assert "risk_guard_status" in card_ids
    assert "portfolio_snapshot_status" in card_ids
    assert "revolut_readonly_status" in card_ids
    assert "decision_journal_status" in card_ids


def test_p98f_safety_flags() -> None:
    payload = build_cockpit_sheets_view_dryrun()
    safety = payload["safety"]
    assert safety["local_dryrun_only"] is True
    assert safety["live_write_executed_in_p98f"] is False
    assert safety["decision_journal_write_in_p98f"] is False
    assert safety["sheet_create_or_update_in_p98f"] is False
    assert safety["apps_script_execution"] is False
    assert safety["clasp_push"] is False
    assert safety["broker_execution"] is False
    assert safety["order_execution"] is False
    assert safety["auto_sizing_execution"] is False
    assert safety["trading_action"] is False


def test_p98f_markdown_contains_sheets_view_plan() -> None:
    markdown = render_cockpit_sheets_view_dryrun_markdown(build_cockpit_sheets_view_dryrun())
    assert "P98F Cockpit Sheets View Dryrun" in markdown
    assert "QAIC_RUNTIME_COCKPIT_VIEW" in markdown
    assert "DRYRUN_ONLY_NO_SHEET_WRITE" in markdown
    assert "benchmark_status" in markdown
    assert "no Sheet create/update in P98F" in markdown


def test_p98f_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_cockpit_sheets_view_dryrun(tmp_path)
    assert result["status"] == "OK_P98F_COCKPIT_SHEETS_VIEW_DRYRUN_READY"
    payload = json.loads(
        (tmp_path / "P98F_COCKPIT_SHEETS_VIEW_DRYRUN.json").read_text(encoding="utf-8")
    )
    markdown = (tmp_path / "P98F_COCKPIT_SHEETS_VIEW_DRYRUN.md").read_text(encoding="utf-8")
    assert payload["sheets_view_plan"]["planned_row_count"] == 17
    assert "QAIC_RUNTIME_COCKPIT_VIEW" in markdown
