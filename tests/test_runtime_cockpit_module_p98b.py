from __future__ import annotations

import json

from mvp_qaic_py.release.runtime_cockpit_module import (
    assert_runtime_cockpit_module_safe,
    build_runtime_cockpit_module,
    export_runtime_cockpit_module,
    render_runtime_cockpit_module_markdown,
)


def test_p98b_runtime_cockpit_module_ready() -> None:
    payload = build_runtime_cockpit_module()
    assert payload["status"] == "OK_P98B_RUNTIME_COCKPIT_MODULE_LOCAL_READY"
    assert payload["source_audit_status"] == "OK_P98A_RUNTIME_COCKPIT_AUDIT_READY_READONLY"
    assert payload["journal_id"] == "DJ-P96B-P93-CQW-20260621-200001"
    assert payload["blockers"] == []


def test_p98b_planning_visual_and_operating_summary() -> None:
    payload = build_runtime_cockpit_module()
    assert len(payload["visual_plan"]) == 3
    assert "[1 GPT/Input]" in payload["visual_plan"][0]
    assert payload["operating_summary"]["tool_mode"] == "human_review_only_decision_support"
    assert (
        "controlled journal logging after explicit GO"
        in payload["operating_summary"]["allowed_actions"]
    )


def test_p98b_cards_and_surfaces() -> None:
    payload = build_runtime_cockpit_module()
    cards = {card["card_id"]: card for card in payload["cockpit_status_cards"]}
    assert cards["LIVE_WORKFLOW_STATUS"]["value"] == "SEALED_P91_TO_P97"
    assert cards["QUEUE_ROW_STATUS"]["value"] == "APPENDED_TO_DECISION_JOURNAL"
    assert len(payload["cockpit_surfaces"]) == 3
    assert all(surface["write_in_p98b"] is False for surface in payload["cockpit_surfaces"])


def test_p98b_safety_flags() -> None:
    payload = build_runtime_cockpit_module()
    assert_runtime_cockpit_module_safe(payload)
    safety = payload["safety"]
    assert safety["local_module_only"] is True
    assert safety["live_write_executed_in_p98b"] is False
    assert safety["decision_journal_write_in_p98b"] is False
    assert safety["apps_script_execution"] is False
    assert safety["clasp_push"] is False
    assert safety["broker_execution"] is False
    assert safety["order_execution"] is False
    assert safety["auto_sizing_execution"] is False
    assert safety["trading_action"] is False


def test_p98b_markdown_contains_visual_summary() -> None:
    markdown = render_runtime_cockpit_module_markdown(build_runtime_cockpit_module())
    assert "P98B Runtime Cockpit Module Local" in markdown
    assert "Planning visuel" in markdown
    assert "Mode de fonctionnement" in markdown
    assert "no live write in P98B" in markdown


def test_p98b_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_runtime_cockpit_module(tmp_path)
    assert result["status"] == "OK_P98B_RUNTIME_COCKPIT_MODULE_LOCAL_READY"
    payload = json.loads(
        (tmp_path / "P98B_RUNTIME_COCKPIT_MODULE.json").read_text(encoding="utf-8")
    )
    markdown = (tmp_path / "P98B_RUNTIME_COCKPIT_MODULE.md").read_text(encoding="utf-8")
    assert payload["journal_id"] == "DJ-P96B-P93-CQW-20260621-200001"
    assert "Planning visuel" in markdown
