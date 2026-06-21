from __future__ import annotations

import json

from mvp_qaic_py.release.cockpit_ui_export import (
    assert_cockpit_ui_export_safe,
    build_cockpit_ui_export,
    export_cockpit_ui_export,
    render_cockpit_ui_export_html,
    render_cockpit_ui_export_markdown,
)


def test_p98e_cockpit_ui_export_ready() -> None:
    payload = build_cockpit_ui_export()
    assert payload["status"] == "OK_P98E_COCKPIT_UI_EXPORT_LOCAL_READY"
    assert payload["source_p98d_status"] == "OK_P98D_RUNTIME_COCKPIT_EXTENDED_MODULE_LOCAL_READY"
    assert payload["card_count"] == 17
    assert payload["blockers"] == []


def test_p98e_renders_json_markdown_html_formats() -> None:
    payload = build_cockpit_ui_export()
    assert payload["ui_export"]["export_formats"] == ["json", "markdown", "html"]
    assert payload["ui_export"]["cards_rendered"] == 17
    assert payload["ui_export"]["render_mode"] == "local_static_readonly"


def test_p98e_html_contains_extended_cockpit_cards() -> None:
    html_text = render_cockpit_ui_export_html(build_cockpit_ui_export())
    assert "MVP QAIC" in html_text
    assert "benchmark_status" in html_text
    assert "lexique_readiness" in html_text
    assert "revolut_readonly_status" in html_text
    assert "NO_BROKER" in html_text


def test_p98e_markdown_contains_export_plan() -> None:
    markdown = render_cockpit_ui_export_markdown(build_cockpit_ui_export())
    assert "P98E Cockpit UI Export Local" in markdown
    assert "P98E_COCKPIT_UI_EXPORT.html" in markdown
    assert "no live write in P98E" in markdown


def test_p98e_safety_flags() -> None:
    payload = build_cockpit_ui_export()
    assert_cockpit_ui_export_safe(payload)
    safety = payload["safety"]
    assert safety["local_export_only"] is True
    assert safety["live_write_executed_in_p98e"] is False
    assert safety["decision_journal_write_in_p98e"] is False
    assert safety["apps_script_execution"] is False
    assert safety["clasp_push"] is False
    assert safety["broker_execution"] is False
    assert safety["order_execution"] is False
    assert safety["auto_sizing_execution"] is False
    assert safety["trading_action"] is False


def test_p98e_export_writes_json_markdown_html(tmp_path) -> None:
    result = export_cockpit_ui_export(tmp_path)
    assert result["status"] == "OK_P98E_COCKPIT_UI_EXPORT_LOCAL_READY"
    payload = json.loads((tmp_path / "P98E_COCKPIT_UI_EXPORT.json").read_text(encoding="utf-8"))
    markdown = (tmp_path / "P98E_COCKPIT_UI_EXPORT.md").read_text(encoding="utf-8")
    html_text = (tmp_path / "P98E_COCKPIT_UI_EXPORT.html").read_text(encoding="utf-8")
    assert payload["card_count"] == 17
    assert "P98E Cockpit UI Export Local" in markdown
    assert "benchmark_status" in html_text
