from __future__ import annotations

import json

from mvp_qaic_py.release.runtime_cockpit_extended_module import (
    assert_runtime_cockpit_extended_module_safe,
    build_runtime_cockpit_extended_module,
    export_runtime_cockpit_extended_module,
    render_runtime_cockpit_extended_module_markdown,
)


def test_p98d_runtime_cockpit_extended_module_ready() -> None:
    payload = build_runtime_cockpit_extended_module()
    assert payload["status"] == "OK_P98D_RUNTIME_COCKPIT_EXTENDED_MODULE_LOCAL_READY"
    assert payload["source_p98b_status"] == "OK_P98B_RUNTIME_COCKPIT_MODULE_LOCAL_READY"
    assert payload["source_p98c_status"] == "OK_P98C_EXTENDED_COCKPIT_SCOPE_AUDIT_READY_READONLY"
    assert payload["card_count"] == 17
    assert payload["blockers"] == []


def test_p98d_includes_all_extended_business_cards() -> None:
    payload = build_runtime_cockpit_extended_module()
    cards = {card["card_id"]: card for card in payload["cards"]}
    for expected in (
        "benchmark_status",
        "latest_payload_status",
        "run_queue_status",
        "response_intake_status",
        "journal_queue_status",
        "decision_journal_status",
        "prompt_quality_status",
        "prompt_improvement_backlog",
        "prompt_library_readiness",
        "lexique_readiness",
        "method_library_status",
        "signal_library_coverage",
        "risk_guard_status",
        "trade_plan_methods_status",
        "revolut_readonly_status",
        "portfolio_snapshot_status",
        "runtime_bridge_status",
    ):
        assert expected in cards


def test_p98d_benchmark_card_is_scope_ready() -> None:
    payload = build_runtime_cockpit_extended_module()
    benchmark = next(card for card in payload["cards"] if card["card_id"] == "benchmark_status")
    assert benchmark["surface_id"] == "BENCHMARK_AI_TRADE"
    assert benchmark["state"] == "SCOPE_READY"
    assert benchmark["write_in_p98d"] is False
    assert benchmark["live_read_in_p98d"] is False


def test_p98d_visual_sections_are_operator_oriented() -> None:
    payload = build_runtime_cockpit_extended_module()
    sections = {section["section_id"]: section for section in payload["visual_sections"]}
    assert "JOURNAL_AND_RUNTIME" in sections
    assert "QUALITY_AND_BENCHMARK" in sections
    assert "KNOWLEDGE_METHODS_SIGNALS_RISK" in sections
    assert "PORTFOLIO_AND_READONLY_BROKER" in sections
    assert "benchmark_status" in sections["QUALITY_AND_BENCHMARK"]["cards"]


def test_p98d_safety_flags() -> None:
    payload = build_runtime_cockpit_extended_module()
    assert_runtime_cockpit_extended_module_safe(payload)
    safety = payload["safety"]
    assert safety["local_module_only"] is True
    assert safety["live_write_executed_in_p98d"] is False
    assert safety["decision_journal_write_in_p98d"] is False
    assert safety["apps_script_execution"] is False
    assert safety["clasp_push"] is False
    assert safety["broker_execution"] is False
    assert safety["order_execution"] is False
    assert safety["auto_sizing_execution"] is False
    assert safety["trading_action"] is False


def test_p98d_markdown_contains_extended_visual_plan() -> None:
    markdown = render_runtime_cockpit_extended_module_markdown(
        build_runtime_cockpit_extended_module()
    )
    assert "P98D Runtime Cockpit Extended Module Local" in markdown
    assert "Planning visuel cockpit etendu" in markdown
    assert "benchmark_status" in markdown
    assert "no live write in P98D" in markdown


def test_p98d_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_runtime_cockpit_extended_module(tmp_path)
    assert result["status"] == "OK_P98D_RUNTIME_COCKPIT_EXTENDED_MODULE_LOCAL_READY"
    payload = json.loads(
        (tmp_path / "P98D_RUNTIME_COCKPIT_EXTENDED_MODULE.json").read_text(encoding="utf-8")
    )
    markdown = (tmp_path / "P98D_RUNTIME_COCKPIT_EXTENDED_MODULE.md").read_text(encoding="utf-8")
    assert payload["card_count"] == 17
    assert "benchmark_status" in markdown
