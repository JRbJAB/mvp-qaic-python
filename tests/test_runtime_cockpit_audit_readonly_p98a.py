from __future__ import annotations

import json

from mvp_qaic_py.release.runtime_cockpit_audit_readonly import (
    assert_runtime_cockpit_audit_readonly_safe,
    build_runtime_cockpit_audit_readonly,
    export_runtime_cockpit_audit_readonly,
    render_runtime_cockpit_audit_readonly_markdown,
)


def test_p98a_runtime_cockpit_audit_ready() -> None:
    payload = build_runtime_cockpit_audit_readonly()
    assert payload["status"] == "OK_P98A_RUNTIME_COCKPIT_AUDIT_READY_READONLY"
    assert payload["release_status"] == "OK_P97_LIVE_WORKFLOW_RELEASE_SEALED"
    assert payload["journal_id"] == "DJ-P96B-P93-CQW-20260621-200001"
    assert payload["decision_journal_range"] == "BJ17:CN17"
    assert payload["queue_range"] == "A9:Z9"
    assert payload["blockers"] == []


def test_p98a_readonly_safety_flags() -> None:
    payload = build_runtime_cockpit_audit_readonly()
    assert_runtime_cockpit_audit_readonly_safe(payload)
    safety = payload["safety"]
    assert safety["readonly_audit_only"] is True
    assert safety["live_write_executed_in_p98a"] is False
    assert safety["decision_journal_write_in_p98a"] is False
    assert safety["apps_script_execution"] is False
    assert safety["clasp_push"] is False
    assert safety["broker_execution"] is False
    assert safety["order_execution"] is False
    assert safety["auto_sizing_execution"] is False
    assert safety["trading_action"] is False


def test_p98a_surfaces_are_readonly() -> None:
    payload = build_runtime_cockpit_audit_readonly()
    surfaces = payload["surfaces"]
    assert len(surfaces) == 3
    assert all(surface["write_in_p98a"] is False for surface in surfaces)
    assert {surface["surface"] for surface in surfaces} == {
        "📤 JOURNAL_APPEND_QUEUE!A9:Z9",
        "🧾 DECISION_JOURNAL!BJ17:CN17",
        "repo release seal",
    }


def test_p98a_cockpit_cards() -> None:
    payload = build_runtime_cockpit_audit_readonly()
    cards = {card["card_id"]: card for card in payload["cockpit_cards"]}
    assert "P98A_RELEASE_STATUS" in cards
    assert "P98A_QUEUE_STATUS" in cards
    assert "P98A_JOURNAL_STATUS" in cards
    assert "P98A_SAFETY_STATUS" in cards
    assert "P98A_NEXT_DECISION" in cards


def test_p98a_markdown_contains_audit_contract() -> None:
    markdown = render_runtime_cockpit_audit_readonly_markdown(
        build_runtime_cockpit_audit_readonly()
    )
    assert "P98A Runtime Cockpit Audit READONLY" in markdown
    assert "read-only audit only" in markdown
    assert "no live write in P98A" in markdown
    assert "P98B_RUNTIME_COCKPIT_MODULE_OR_P99_MVP_FREEZE" in markdown


def test_p98a_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_runtime_cockpit_audit_readonly(tmp_path)
    assert result["status"] == "OK_P98A_RUNTIME_COCKPIT_AUDIT_READY_READONLY"
    payload = json.loads(
        (tmp_path / "P98A_RUNTIME_COCKPIT_AUDIT_READONLY.json").read_text(encoding="utf-8")
    )
    markdown = (tmp_path / "P98A_RUNTIME_COCKPIT_AUDIT_READONLY.md").read_text(encoding="utf-8")
    assert payload["journal_id"] == "DJ-P96B-P93-CQW-20260621-200001"
    assert "P98A Runtime Cockpit Audit READONLY" in markdown
