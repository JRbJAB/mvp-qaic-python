from __future__ import annotations

from pathlib import Path

from mvp_qaic_py.p181abc_operator_ui_prompt_capture_sessions import build_p181abc_audit


def test_p181abc_operator_ui_audit_ready() -> None:
    payload = build_p181abc_audit(Path.cwd())

    assert payload["STATUS"] == "OK_P181ABC_OPERATOR_UI_PROMPT_CAPTURE_SESSIONS_READY"
    assert payload["operator_ui_ready"] is True
    assert payload["route_count"] == 9
    assert payload["missing_token_count"] == 0
    assert payload["public_serve"] is False
    assert payload["google_sheets_write"] is False
    assert payload["gem_call_executed"] is False
    assert payload["auto_apply_gem_response"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False
