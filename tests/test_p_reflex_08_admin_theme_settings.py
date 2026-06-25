from mvp_qaic_reflex_ui import mvp_qaic_reflex_ui as ui
from mvp_qaic_reflex_ui.layout import navigation_items
from mvp_qaic_reflex_ui.pages_admin import (
    admin_center,
    admin_data_binding,
    admin_routes,
    admin_runtime,
    admin_safety,
    admin_theme,
)
from mvp_qaic_reflex_ui.theme import (
    ADMIN_SECTIONS,
    SAFETY_FLAGS,
    THEME_OPTIONS,
    UI_THEME,
    get_admin_routes,
    get_all_routes,
    get_theme_contract,
)


def test_p08_admin_sections_are_declared():
    section_ids = {section["section_id"] for section in ADMIN_SECTIONS}

    assert "admin_center" in section_ids
    assert "admin_runtime" in section_ids
    assert "admin_theme" in section_ids
    assert "admin_safety" in section_ids
    assert "admin_routes" in section_ids
    assert "admin_data_binding" in section_ids


def test_p08_admin_routes_are_stable():
    routes = get_admin_routes()

    assert "/admin" in routes
    assert "/admin/runtime" in routes
    assert "/admin/theme" in routes
    assert "/admin/safety" in routes
    assert "/admin/routes" in routes
    assert "/admin/data-binding" in routes
    assert len(routes) == len(set(routes))


def test_p08_theme_options_cover_ui_governance():
    assert "light" in THEME_OPTIONS["modes"]
    assert "dark" in THEME_OPTIONS["modes"]
    assert "system" in THEME_OPTIONS["modes"]
    assert UI_THEME["default_mode"] == "system"
    assert UI_THEME["primary_accent"] in THEME_OPTIONS["accents"]
    assert UI_THEME["density"] in THEME_OPTIONS["density"]


def test_p08_safety_flags_remain_locked():
    assert SAFETY_FLAGS["human_review_only"] is True
    assert SAFETY_FLAGS["no_auto_order"] is True
    assert SAFETY_FLAGS["no_auto_sizing"] is True
    assert SAFETY_FLAGS["no_broker_execution"] is True
    assert SAFETY_FLAGS["no_public_deploy"] is True
    assert SAFETY_FLAGS["no_sheet_write"] is True
    assert SAFETY_FLAGS["no_bigquery_write"] is True


def test_p08_theme_contract_counts_admin_sections():
    contract = get_theme_contract()

    assert contract["admin_section_count"] == len(ADMIN_SECTIONS)
    assert contract["admin_section_count"] >= 6
    assert "theme_options" in contract


def test_p08_navigation_contains_admin_routes():
    routes = {item["route"] for item in navigation_items()}
    all_routes = set(get_all_routes())

    assert "/admin" in routes
    assert "/admin/theme" in routes
    assert "/admin/safety" in routes
    assert all_routes.issubset(routes)


def test_p08_admin_pages_return_components():
    assert admin_center() is not None
    assert admin_runtime() is not None
    assert admin_theme() is not None
    assert admin_safety() is not None
    assert admin_routes() is not None
    assert admin_data_binding() is not None


def test_p08_app_exports_index_and_admin_pages():
    assert ui.index() is not None
    assert ui.admin_center() is not None
    assert ui.admin_theme() is not None
    assert ui.admin_safety() is not None
