from mvp_qaic_reflex_ui import mvp_qaic_reflex_ui as ui
from mvp_qaic_reflex_ui.layout import navigation_items
from mvp_qaic_reflex_ui.theme import (
    LANDING_SECTIONS,
    SAFETY_FLAGS,
    UI_THEME,
    get_landing_sections,
    get_primary_routes,
    get_theme_contract,
)


def test_p07_priority_landing_sections_exist():
    section_ids = {section["section_id"] for section in LANDING_SECTIONS}

    assert "home_mission_control" in section_ids
    assert "dev_tracking" in section_ids
    assert "cdc_tracker" in section_ids
    assert "architecture_web" in section_ids
    assert "documentation_registry" in section_ids
    assert "architecture_registry" in section_ids


def test_p07_priority_routes_exist_and_are_unique():
    routes = get_primary_routes()

    assert "/" in routes
    assert "/dev-tracking" in routes
    assert "/cdc-tracker" in routes
    assert "/architecture-web" in routes
    assert "/documentation-registry" in routes
    assert "/architecture-registry" in routes
    assert len(routes) == len(set(routes))


def test_p07_navigation_contains_primary_and_secondary_routes():
    routes = {item["route"] for item in navigation_items()}

    assert "/prompt-lab" in routes
    assert "/gem-portfolio" in routes
    assert "/qaic-bridge" in routes
    assert "/settings-safety" in routes
    assert "/architecture-registry" in routes


def test_p07_theme_contract_and_safety_flags_are_stable():
    contract = get_theme_contract()

    assert UI_THEME["app_name"] == "MVP QAIC"
    assert UI_THEME["default_mode"] == "system"
    assert SAFETY_FLAGS["human_review_only"] is True
    assert SAFETY_FLAGS["no_auto_order"] is True
    assert SAFETY_FLAGS["no_auto_sizing"] is True
    assert contract["primary_section_count"] >= 6


def test_p07_pages_return_reflex_components():
    assert ui.index() is not None
    assert ui.mission_control() is not None
    assert ui.dev_tracking() is not None
    assert ui.cdc_tracker() is not None
    assert ui.architecture_web() is not None
    assert ui.documentation_registry() is not None
    assert ui.architecture_registry() is not None
    assert ui.prompt_lab() is not None
    assert ui.gem_portfolio() is not None
    assert ui.qaic_bridge() is not None


def test_p07_landing_sections_are_copy_safe_dicts():
    copied = get_landing_sections()
    copied[0]["title"] = "MUTATED"

    assert LANDING_SECTIONS[0]["title"] == "Home / Mission Control"
