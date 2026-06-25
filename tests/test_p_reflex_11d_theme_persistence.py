from pathlib import Path

from mvp_qaic_reflex_ui.pages_admin import admin_theme
from mvp_qaic_reflex_ui.theme_persistence import (
    THEME_ALLOWED_VALUES,
    THEME_LOCAL_STORAGE_KEY,
    THEME_PERSISTENCE_MODE,
    THEME_PERSISTENCE_SCRIPT,
    build_theme_persistence_payload,
    theme_persistence_component,
    theme_persistence_summary_rows,
)


def test_p11d_theme_persistence_payload_is_browser_local_only():
    payload = build_theme_persistence_payload()

    assert payload["persistence_status"] == "READY_BROWSER_LOCAL_STORAGE"
    assert payload["storage_key"] == "mvp_qaic_ui_theme_preference_v1"
    assert payload["persistence_mode"] == "BROWSER_LOCAL_STORAGE"
    assert payload["allowed_values"] == ["light", "dark", "system"]
    assert payload["default_value"] == "system"
    assert payload["server_write"] is False
    assert payload["sheet_write"] is False
    assert payload["bigquery_write"] is False
    assert payload["public_deploy"] is False
    assert payload["live_action"] is False
    assert payload["human_review_approved"] is True


def test_p11d_theme_persistence_constants_are_stable():
    assert THEME_LOCAL_STORAGE_KEY == "mvp_qaic_ui_theme_preference_v1"
    assert THEME_PERSISTENCE_MODE == "BROWSER_LOCAL_STORAGE"
    assert THEME_ALLOWED_VALUES == ("light", "dark", "system")


def test_p11d_theme_persistence_script_contains_required_browser_hooks():
    assert "window.localStorage.setItem(KEY, mode)" in THEME_PERSISTENCE_SCRIPT
    assert "window.MVP_QAIC_THEME_PERSISTENCE" in THEME_PERSISTENCE_SCRIPT
    assert "mvp-qaic-theme-persist-light" in THEME_PERSISTENCE_SCRIPT
    assert "mvp-qaic-theme-persist-dark" in THEME_PERSISTENCE_SCRIPT
    assert "mvp-qaic-theme-persist-system" in THEME_PERSISTENCE_SCRIPT
    assert "mvpQaicThemeMode" in THEME_PERSISTENCE_SCRIPT
    assert "mvpQaicEffectiveTheme" in THEME_PERSISTENCE_SCRIPT


def test_p11d_theme_persistence_summary_rows_are_safe():
    rows = theme_persistence_summary_rows()

    assert rows["persistence_status"] == "READY_BROWSER_LOCAL_STORAGE"
    assert rows["persistence_mode"] == "BROWSER_LOCAL_STORAGE"
    assert rows["default_value"] == "system"
    assert rows["server_write"] is False
    assert rows["sheet_write"] is False
    assert rows["bigquery_write"] is False


def test_p11d_theme_persistence_component_and_admin_page_render():
    assert theme_persistence_component() is not None
    assert admin_theme() is not None


def test_p11d_admin_page_wires_theme_persistence():
    source = Path("mvp_qaic_reflex_ui/pages_admin.py").read_text(encoding="utf-8")

    assert "theme_persistence_component()" in source
    assert "theme_persistence_summary_rows()" in source
    assert "Browser persistence" in source
