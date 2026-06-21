from __future__ import annotations
import json

from mvp_qaic_py.release.operational_cockpit_live_write_evidence import (
    assert_p100a_operational_cockpit_live_write_safe,
    build_p100a_operational_cockpit_live_write_evidence,
    export_p100a_operational_cockpit_live_write_evidence,
    render_p100a_operational_cockpit_live_write_markdown,
)


def test_p100a_evidence_ready() -> None:
    payload = build_p100a_operational_cockpit_live_write_evidence()
    assert payload["status"] == "OK_P100A_OPERATIONAL_COCKPIT_LIVE_WRITE_VERIFIED"
    assert payload["source_p99_status"] == "OK_P99_MVP_FREEZE_RELEASE_HANDOFF_READY"
    assert payload["target_sheet_name"] == "QAIC_RUNTIME_COCKPIT_VIEW"
    assert payload["target_range"] == "QAIC_RUNTIME_COCKPIT_VIEW!A1:J40"
    assert payload["card_count"] == 17


def test_p100a_write_evidence_flags() -> None:
    payload = build_p100a_operational_cockpit_live_write_evidence()
    assert_p100a_operational_cockpit_live_write_safe(payload)
    result = payload["write_result"]
    assert result["sheet_view_write_executed"] is True
    assert result["old_static_rows_cleared"] is True
    assert result["readback_verified"] is True
    assert result["decision_bar_present"] is True
    assert result["action_now_present"] is True
    assert result["real_metric_gaps_declared"] is True


def test_p100a_safety_flags() -> None:
    payload = build_p100a_operational_cockpit_live_write_evidence()
    assert payload["decision_journal_write_in_p100a"] is False
    assert payload["apps_script_execution"] is False
    assert payload["clasp_push"] is False
    assert payload["broker_execution"] is False
    assert payload["order_execution"] is False
    assert payload["auto_sizing_execution"] is False
    assert payload["trading_action"] is False


def test_p100a_sections_include_real_work_domains() -> None:
    sections = set(build_p100a_operational_cockpit_live_write_evidence()["operational_sections"])
    assert "benchmark_ai_trade" in sections
    assert "prompt_quality" in sections
    assert "lexique" in sections
    assert "methods" in sections
    assert "signals" in sections
    assert "risk_guards" in sections
    assert "revolut_x_readonly" in sections


def test_p100a_markdown_contains_next_real_work() -> None:
    markdown = render_p100a_operational_cockpit_live_write_markdown(
        build_p100a_operational_cockpit_live_write_evidence()
    )
    assert "P100A Operational Cockpit Live Write Evidence" in markdown
    assert "P100B read benchmark pass/fail counts" in markdown
    assert "no broker/order/sizing" in markdown


def test_p100a_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_p100a_operational_cockpit_live_write_evidence(tmp_path)
    assert result["status"] == "OK_P100A_OPERATIONAL_COCKPIT_LIVE_WRITE_VERIFIED"
    payload = json.loads(
        (tmp_path / "P100A_OPERATIONAL_COCKPIT_LIVE_WRITE_EVIDENCE.json").read_text(
            encoding="utf-8"
        )
    )
    markdown = (tmp_path / "P100A_OPERATIONAL_COCKPIT_LIVE_WRITE_EVIDENCE.md").read_text(
        encoding="utf-8"
    )
    assert payload["card_count"] == 17
    assert "QAIC_RUNTIME_COCKPIT_VIEW" in markdown
