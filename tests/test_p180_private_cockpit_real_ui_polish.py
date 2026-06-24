from __future__ import annotations

from pathlib import Path

from mvp_qaic_py.p180_private_cockpit_real_ui_polish import build_real_ui_polish_audit


def test_real_ui_polish_audit_repo_runner_ready() -> None:
    payload = build_real_ui_polish_audit(Path.cwd())

    assert payload["STATUS"] == "OK_P180_PRIVATE_COCKPIT_REAL_UI_POLISH_READY"
    assert payload["ui_polish_ready"] is True
    assert payload["route_count"] == 6
    assert payload["missing_token_count"] == 0
    assert payload["public_serve"] is False
    assert payload["google_sheets_write"] is False
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False
