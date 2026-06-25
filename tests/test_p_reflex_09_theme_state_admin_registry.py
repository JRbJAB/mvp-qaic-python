from mvp_qaic_reflex_ui.admin_data_registry import (
    REGISTRY_DOMAINS,
    admin_registry_summary_rows,
    build_admin_data_registry_payload,
    registry_domain_rows,
)
from mvp_qaic_reflex_ui.admin_theme_state import (
    DEFAULT_THEME_STATE,
    ThemeSettingsState,
    build_theme_state_payload,
    theme_state_summary_rows,
    validate_theme_choice,
)
from mvp_qaic_reflex_ui.pages_admin import admin_data_binding, admin_runtime, admin_theme


def test_p09_theme_state_payload_is_local_and_safe():
    payload = build_theme_state_payload()

    assert payload["theme_state_status"] == "READY_INTERACTIVE_LOCAL"
    assert payload["write_mode"] == "IN_MEMORY_ONLY"
    assert payload["public_deploy"] is False
    assert payload["live_action"] is False
    assert payload["human_review_only"] is True
    assert payload["current"] == DEFAULT_THEME_STATE


def test_p09_theme_choice_validation():
    assert validate_theme_choice("mode", "light") is True
    assert validate_theme_choice("mode", "dark") is True
    assert validate_theme_choice("mode", "system") is True
    assert validate_theme_choice("accent", "cyan") is True
    assert validate_theme_choice("density", "spacious") is True
    assert validate_theme_choice("mode", "invalid") is False
    assert validate_theme_choice("unknown", "light") is False


def test_p09_theme_state_class_exposes_event_handlers():
    assert hasattr(ThemeSettingsState, "set_light_mode")
    assert hasattr(ThemeSettingsState, "set_dark_mode")
    assert hasattr(ThemeSettingsState, "set_system_mode")
    assert hasattr(ThemeSettingsState, "set_blue_accent")
    assert hasattr(ThemeSettingsState, "set_cyan_accent")
    assert hasattr(ThemeSettingsState, "reset_theme")


def test_p09_theme_state_summary_rows_are_stable():
    rows = theme_state_summary_rows()

    assert rows["status"] == "READY_INTERACTIVE_LOCAL"
    assert rows["mode"] == "system"
    assert rows["accent"] == "blue"
    assert rows["density"] == "comfortable"
    assert rows["write_mode"] == "IN_MEMORY_ONLY"


def test_p09_admin_data_registry_payload_is_readonly():
    payload = build_admin_data_registry_payload()

    assert payload["registry_status"] == "READY_LOCAL_READONLY"
    assert payload["domain_count"] == len(REGISTRY_DOMAINS)
    assert payload["route_count"] >= 17
    assert payload["landing_section_count"] >= 6
    assert payload["admin_section_count"] >= 6
    assert payload["write_allowed"] is False
    assert payload["live_action"] is False


def test_p09_registry_summary_rows_and_domains_are_stable():
    rows = admin_registry_summary_rows()
    domains = registry_domain_rows()

    assert rows["registry_status"] == "READY_LOCAL_READONLY"
    assert rows["binding_mode"] == "LOCAL_READONLY"
    assert rows["write_allowed"] is False
    assert "runtime" in domains
    assert "theme" in domains
    assert "safety" in domains


def test_p09_admin_pages_render_with_new_panels():
    assert admin_theme() is not None
    assert admin_runtime() is not None
    assert admin_data_binding() is not None
