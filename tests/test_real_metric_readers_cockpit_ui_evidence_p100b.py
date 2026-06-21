from __future__ import annotations

import json

from mvp_qaic_py.release.real_metric_readers_cockpit_ui_evidence import (
    assert_p100b_real_metric_readers_safe,
    build_p100b_real_metric_readers_cockpit_ui_evidence,
    export_p100b_real_metric_readers_cockpit_ui_evidence,
    render_p100b_real_metric_readers_markdown,
)


def test_p100b_evidence_ready() -> None:
    payload = build_p100b_real_metric_readers_cockpit_ui_evidence()
    assert payload["status"] == "OK_P100B_REAL_METRIC_READERS_COCKPIT_UI_LIVE_WRITE_VERIFIED"
    assert payload["benchmark_ai_trade_migrated"] is True
    assert payload["cockpit_range_written"] == "QAIC_RUNTIME_COCKPIT_VIEW!A1:J22"
    assert payload["bridge_rows_written"] == "QAIC_RUNTIME_BRIDGE_STATUS!A8:N11"


def test_p100b_benchmark_metrics_are_real_read_values() -> None:
    payload = build_p100b_real_metric_readers_cockpit_ui_evidence()
    benchmark = payload["source_readers"]["BENCHMARK_AI_TRADE"]
    assert benchmark["reader_status"] == "OK"
    assert benchmark["candidate_count"] == 14
    assert benchmark["inspire"] == 6
    assert benchmark["monitor"] == 4
    assert benchmark["review_required"] == 1
    assert benchmark["blocked"] == 3
    assert benchmark["safety"] == "PASS"


def test_p100b_quality_metrics_are_real_read_values() -> None:
    payload = build_p100b_real_metric_readers_cockpit_ui_evidence()
    quality = payload["source_readers"]["GPT_QUALITY_DASHBOARD"]
    assert quality["journal_rows"] == 2
    assert quality["prompt_ids"] == 1
    assert quality["top_missing_data"] == 15
    assert quality["top_blockers"] == 15
    assert quality["prompt_actions"] == 1
    assert "PnL" in quality["top_missing_sample"]


def test_p100b_knowledge_readers_present() -> None:
    readers = build_p100b_real_metric_readers_cockpit_ui_evidence()["source_readers"]
    assert readers["METHOD_LIBRARY"]["observed_method_count"] == 18
    assert readers["SIGNAL_LIBRARY"]["observed_signal_count"] == 58
    assert readers["RISK_PLAYBOOK"]["observed_risk_profile_count"] == 10
    assert readers["REVOLUT_X_READONLY_CONTRACT"]["security_guard"] == "read_only_no_order"
    assert readers["PORTFOLIO_SNAPSHOT"]["position_rows"] == 0


def test_p100b_safety_flags() -> None:
    payload = build_p100b_real_metric_readers_cockpit_ui_evidence()
    assert_p100b_real_metric_readers_safe(payload)
    writes = payload["writes_executed"]
    assert writes["cockpit_values_written"] is True
    assert writes["cockpit_ui_format_written"] is True
    assert writes["runtime_bridge_status_written"] is True
    assert writes["decision_journal_write_in_p100b"] is False
    assert writes["apps_script_execution"] is False
    assert writes["clasp_push"] is False
    assert writes["broker_execution"] is False
    assert writes["order_execution"] is False
    assert writes["auto_sizing_execution"] is False
    assert writes["trading_action"] is False


def test_p100b_markdown_contains_metrics_and_ui() -> None:
    markdown = render_p100b_real_metric_readers_markdown(
        build_p100b_real_metric_readers_cockpit_ui_evidence()
    )
    assert "P100B Real Metric Readers" in markdown
    assert "BENCHMARK_AI_TRADE" in markdown
    assert "candidate_count=14" in markdown
    assert "cockpit_ui_format_written" in markdown
    assert "no broker/order/sizing" in markdown


def test_p100b_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_p100b_real_metric_readers_cockpit_ui_evidence(tmp_path)
    assert result["status"] == "OK_P100B_REAL_METRIC_READERS_COCKPIT_UI_LIVE_WRITE_VERIFIED"
    payload = json.loads(
        (tmp_path / "P100B_REAL_METRIC_READERS_COCKPIT_UI_EVIDENCE.json").read_text(
            encoding="utf-8"
        )
    )
    markdown = (tmp_path / "P100B_REAL_METRIC_READERS_COCKPIT_UI_EVIDENCE.md").read_text(
        encoding="utf-8"
    )
    assert payload["source_readers"]["BENCHMARK_AI_TRADE"]["candidate_count"] == 14
    assert "QAIC_RUNTIME_COCKPIT_VIEW" in markdown
