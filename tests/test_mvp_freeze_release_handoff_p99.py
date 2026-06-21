from __future__ import annotations

import json

from mvp_qaic_py.release.mvp_freeze_release_handoff import (
    assert_mvp_freeze_release_handoff_safe,
    build_mvp_freeze_release_handoff,
    export_mvp_freeze_release_handoff,
    render_mvp_freeze_release_handoff_markdown,
)


def test_p99_mvp_freeze_release_handoff_ready() -> None:
    payload = build_mvp_freeze_release_handoff()
    assert payload["status"] == "OK_P99_MVP_FREEZE_RELEASE_HANDOFF_READY"
    assert payload["source_p98g_status"] == "OK_P98G_COCKPIT_SHEETS_LIVE_WRITE_VERIFIED"
    assert payload["release_chain_count"] == 15
    assert payload["blockers"] == []


def test_p99_includes_release_artifacts() -> None:
    artifacts = build_mvp_freeze_release_handoff()["release_artifacts"]
    assert artifacts["cockpit_sheet"] == "QAIC_RUNTIME_COCKPIT_VIEW"
    assert artifacts["cockpit_range"] == "QAIC_RUNTIME_COCKPIT_VIEW!A1:H24"
    assert artifacts["decision_journal_range"] == "DECISION_JOURNAL!BJ17:CN17"
    assert artifacts["journal_queue_range"] == "JOURNAL_APPEND_QUEUE!A9:Z9"


def test_p99_release_chain_contains_p98e_r1_and_p98g() -> None:
    chain = build_mvp_freeze_release_handoff()["release_chain"]
    steps = {item["step"] for item in chain}
    assert "P98E-R1" in steps
    assert "P98G" in steps
    assert "P91" in steps
    assert "P97" in steps


def test_p99_safety_flags() -> None:
    payload = build_mvp_freeze_release_handoff()
    assert_mvp_freeze_release_handoff_safe(payload)
    safety = payload["safety"]
    assert safety["freeze_handoff_only"] is True
    assert safety["live_write_executed_in_p99"] is False
    assert safety["decision_journal_write_in_p99"] is False
    assert safety["sheet_write_in_p99"] is False
    assert safety["apps_script_execution"] is False
    assert safety["clasp_push"] is False
    assert safety["broker_execution"] is False
    assert safety["order_execution"] is False
    assert safety["auto_sizing_execution"] is False
    assert safety["trading_action"] is False


def test_p99_markdown_contains_freeze_handoff() -> None:
    markdown = render_mvp_freeze_release_handoff_markdown(build_mvp_freeze_release_handoff())
    assert "P99 MVP Freeze Release Handoff" in markdown
    assert "QAIC_RUNTIME_COCKPIT_VIEW" in markdown
    assert "P98G" in markdown
    assert "no broker/order/sizing" in markdown


def test_p99_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_mvp_freeze_release_handoff(tmp_path)
    assert result["status"] == "OK_P99_MVP_FREEZE_RELEASE_HANDOFF_READY"
    payload = json.loads(
        (tmp_path / "P99_MVP_FREEZE_RELEASE_HANDOFF.json").read_text(encoding="utf-8")
    )
    markdown = (tmp_path / "P99_MVP_FREEZE_RELEASE_HANDOFF.md").read_text(encoding="utf-8")
    assert payload["release_chain_count"] == 15
    assert "QAIC_RUNTIME_COCKPIT_VIEW" in markdown
