from __future__ import annotations

import json

from mvp_qaic_py.release.live_workflow_release_seal import (
    assert_live_workflow_release_seal_safe,
    build_live_workflow_release_seal,
    export_live_workflow_release_seal,
    render_live_workflow_release_seal_markdown,
)


def test_p97_live_workflow_release_seal_ready() -> None:
    payload = build_live_workflow_release_seal()
    assert payload["status"] == "OK_P97_LIVE_WORKFLOW_RELEASE_SEALED"
    assert payload["sealed_range"] == "P91_TO_P96B"
    assert payload["decision_journal_row"] == "🧾 DECISION_JOURNAL!BJ17:CN17"
    assert payload["queue_row"] == "📤 JOURNAL_APPEND_QUEUE!A9:Z9"
    assert payload["journal_id"] == "DJ-P96B-P93-CQW-20260621-200001"
    assert payload["blockers"] == []


def test_p97_includes_all_sealed_steps() -> None:
    payload = build_live_workflow_release_seal()
    steps = [item["step"] for item in payload["steps"]]
    assert steps == ["P91", "P92", "P93", "P94", "P95", "P96A", "P96B"]


def test_p97_safety_flags() -> None:
    payload = build_live_workflow_release_seal()
    assert_live_workflow_release_seal_safe(payload)
    safety = payload["safety"]
    assert safety["live_write_already_completed"] is True
    assert safety["no_additional_live_write_in_p97"] is True
    assert safety["apps_script_execution"] is False
    assert safety["clasp_push"] is False
    assert safety["broker_execution"] is False
    assert safety["order_execution"] is False
    assert safety["auto_sizing_execution"] is False
    assert safety["trading_action"] is False


def test_p97_markdown_contains_release_seal() -> None:
    markdown = render_live_workflow_release_seal_markdown(build_live_workflow_release_seal())
    assert "P97 Live Workflow Release Seal" in markdown
    assert "P91_TO_P96B" in markdown
    assert "no additional live write in P97" in markdown
    assert "no broker/order/sizing" in markdown


def test_p97_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_live_workflow_release_seal(tmp_path)
    assert result["status"] == "OK_P97_LIVE_WORKFLOW_RELEASE_SEALED"
    payload = json.loads(
        (tmp_path / "P97_LIVE_WORKFLOW_RELEASE_SEAL.json").read_text(encoding="utf-8")
    )
    markdown = (tmp_path / "P97_LIVE_WORKFLOW_RELEASE_SEAL.md").read_text(encoding="utf-8")
    assert payload["journal_id"] == "DJ-P96B-P93-CQW-20260621-200001"
    assert "P97 Live Workflow Release Seal" in markdown
