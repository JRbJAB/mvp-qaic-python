from __future__ import annotations

import json

from mvp_qaic_py.operator.operator_decision_gate import (
    build_operator_decision_gate,
    export_operator_decision_gate,
    render_operator_decision_gate_markdown,
)


def test_p86_decision_gate_go_ready() -> None:
    gate = build_operator_decision_gate()
    assert gate["status"] == "OK_P86_OPERATOR_DECISION_GATE_GO"
    assert gate["prerequisites_ok"] is True
    assert gate["decision_allowed"] is True
    assert gate["write_route_count"] == 0
    assert gate["blocked_route_count"] == 0


def test_p86_blocks_unknown_decision() -> None:
    gate = build_operator_decision_gate(decision="APPEND_TO_SHEET")
    assert gate["status"] == "BLOCKED_P86_UNKNOWN_OPERATOR_DECISION"
    assert gate["decision_allowed"] is False


def test_p86_hold_review() -> None:
    gate = build_operator_decision_gate(decision="HOLD_HUMAN_REVIEW")
    assert gate["status"] == "REVIEW_REQUIRED_P86_OPERATOR_HOLD"
    assert gate["next"] == "WAIT_HUMAN_REVIEW"


def test_p86_safety_flags() -> None:
    gate = build_operator_decision_gate()
    assert gate["sheet_write"] is False
    assert gate["apps_script_execution"] is False
    assert gate["clasp_push"] is False
    assert gate["broker_execution"] is False
    assert gate["order_execution"] is False
    assert gate["auto_sizing_execution"] is False
    assert gate["google_rest_local_diag"] is False


def test_p86_markdown_contains_gate_and_safety() -> None:
    markdown = render_operator_decision_gate_markdown(build_operator_decision_gate())
    assert "P86 Operator Decision Gate" in markdown
    assert "OK_P86_OPERATOR_DECISION_GATE_GO" in markdown
    assert "NO_SHEET_WRITE" in markdown


def test_p86_export_writes_json_and_markdown(tmp_path) -> None:
    result = export_operator_decision_gate(tmp_path)
    assert result["status"] == "OK_P86_OPERATOR_DECISION_GATE_GO"
    payload = json.loads((tmp_path / "P86_OPERATOR_DECISION_GATE.json").read_text(encoding="utf-8"))
    markdown = (tmp_path / "P86_OPERATOR_DECISION_GATE.md").read_text(encoding="utf-8")
    assert payload["status"] == "OK_P86_OPERATOR_DECISION_GATE_GO"
    assert "P86 Operator Decision Gate" in markdown
