from __future__ import annotations

import json

from mvp_qaic_py.release.extended_cockpit_scope_audit import (
    assert_extended_cockpit_scope_audit_safe,
    build_extended_cockpit_scope_audit,
    export_extended_cockpit_scope_audit,
    render_extended_cockpit_scope_audit_markdown,
)


def test_p98c_extended_cockpit_scope_audit_ready() -> None:
    payload = build_extended_cockpit_scope_audit()
    assert payload["status"] == "OK_P98C_EXTENDED_COCKPIT_SCOPE_AUDIT_READY_READONLY"
    assert payload["source_p98b_status"] == "OK_P98B_RUNTIME_COCKPIT_MODULE_LOCAL_READY"
    assert payload["surface_count"] == 17
    assert payload["blockers"] == []


def test_p98c_includes_benchmark_and_core_functions() -> None:
    payload = build_extended_cockpit_scope_audit()
    surface_ids = {surface["surface_id"] for surface in payload["surfaces"]}
    assert "BENCHMARK_AI_TRADE" in surface_ids
    assert "LEXIQUE_MASTER" in surface_ids
    assert "METHOD_LIBRARY" in surface_ids
    assert "SIGNAL_LIBRARY" in surface_ids
    assert "RISK_PLAYBOOK" in surface_ids
    assert "REVOLUT_X_READONLY_CONTRACT" in surface_ids
    assert "PORTFOLIO_SNAPSHOT" in surface_ids
    assert "QAIC_RUNTIME_BRIDGE_STATUS" in surface_ids


def test_p98c_benchmark_classification_and_card() -> None:
    payload = build_extended_cockpit_scope_audit()
    benchmark = next(
        surface for surface in payload["surfaces"] if surface["surface_id"] == "BENCHMARK_AI_TRADE"
    )
    assert benchmark["classification"] == "READY_FOR_SCOPE_MAPPING"
    assert benchmark["target_card"] == "benchmark_status"
    assert benchmark["write_in_p98c"] is False
    assert benchmark["live_read_in_p98c"] is False


def test_p98c_required_p98d_cards() -> None:
    payload = build_extended_cockpit_scope_audit()
    cards = set(payload["required_p98d_cards"])
    assert "benchmark_status" in cards
    assert "lexique_readiness" in cards
    assert "method_library_status" in cards
    assert "signal_library_coverage" in cards
    assert "risk_guard_status" in cards
    assert "prompt_quality_status" in cards
    assert "revolut_readonly_status" in cards
    assert "portfolio_snapshot_status" in cards


def test_p98c_readonly_safety_flags() -> None:
    payload = build_extended_cockpit_scope_audit()
    assert_extended_cockpit_scope_audit_safe(payload)
    safety = payload["safety"]
    assert safety["readonly_audit_only"] is True
    assert safety["local_module_only"] is True
    assert safety["live_write_executed_in_p98c"] is False
    assert safety["decision_journal_write_in_p98c"] is False
    assert safety["apps_script_execution"] is False
    assert safety["clasp_push"] is False
    assert safety["broker_execution"] is False
    assert safety["order_execution"] is False
    assert safety["auto_sizing_execution"] is False
    assert safety["trading_action"] is False


def test_p98c_markdown_contains_extended_scope() -> None:
    markdown = render_extended_cockpit_scope_audit_markdown(build_extended_cockpit_scope_audit())
    assert "P98C Extended Cockpit Scope Audit READONLY" in markdown
    assert "BENCHMARK_AI_TRADE" in markdown
    assert "benchmark_status" in markdown
    assert "no live write in P98C" in markdown


def test_p98c_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_extended_cockpit_scope_audit(tmp_path)
    assert result["status"] == "OK_P98C_EXTENDED_COCKPIT_SCOPE_AUDIT_READY_READONLY"
    payload = json.loads(
        (tmp_path / "P98C_EXTENDED_COCKPIT_SCOPE_AUDIT_READONLY.json").read_text(encoding="utf-8")
    )
    markdown = (tmp_path / "P98C_EXTENDED_COCKPIT_SCOPE_AUDIT_READONLY.md").read_text(
        encoding="utf-8"
    )
    assert payload["surface_count"] == 17
    assert "BENCHMARK_AI_TRADE" in markdown
