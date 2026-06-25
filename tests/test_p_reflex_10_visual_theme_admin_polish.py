from pathlib import Path

from mvp_qaic_reflex_ui import mvp_qaic_reflex_ui as ui
from mvp_qaic_reflex_ui.pages_admin import admin_center, admin_theme
from mvp_qaic_reflex_ui.pages_landing import home
from mvp_qaic_reflex_ui.visual_theme import (
    CONTENT_MAX_WIDTH,
    DESIGN_TOKENS,
    admin_summary_panel,
    color_mode_toggle,
    metric_grid,
    mission_control_hero,
    theme_runtime_panel,
)


def test_p10_global_theme_contract_is_present_in_app_source():
    source = Path("mvp_qaic_reflex_ui/mvp_qaic_reflex_ui.py").read_text(encoding="utf-8")

    assert "theme=rx.theme(" in source
    assert 'appearance="inherit"' in source
    assert 'accent_color="blue"' in source
    assert 'panel_background="solid"' in source
    assert 'radius="large"' in source
    assert 'scaling="100%"' in source


def test_p10_official_color_mode_toggle_is_used():
    source = Path("mvp_qaic_reflex_ui/visual_theme.py").read_text(encoding="utf-8")

    assert "rx.toggle_color_mode" in source
    assert "rx.color_mode_cond" in source
    assert color_mode_toggle() is not None


def test_p10_design_tokens_cover_core_visual_system():
    assert DESIGN_TOKENS["app_background"]
    assert DESIGN_TOKENS["sidebar_background"]
    assert DESIGN_TOKENS["topbar_background"]
    assert DESIGN_TOKENS["surface_background"]
    assert DESIGN_TOKENS["border"]
    assert DESIGN_TOKENS["accent"]
    assert DESIGN_TOKENS["radius_card"] == "16px"
    assert CONTENT_MAX_WIDTH == "1480px"


def test_p10_visual_components_render():
    assert mission_control_hero() is not None
    assert theme_runtime_panel() is not None
    assert admin_summary_panel() is not None

    metrics = (
        {
            "label": "Runtime",
            "value": "LOCAL",
            "detail": "Private runtime.",
            "tone": "success",
        },
    )
    assert metric_grid(metrics) is not None


def test_p10_landing_and_admin_pages_render():
    assert home() is not None
    assert admin_center() is not None
    assert admin_theme() is not None
    assert ui.index() is not None


def test_p10_layout_uses_visual_theme_tokens():
    source = Path("mvp_qaic_reflex_ui/layout.py").read_text(encoding="utf-8")

    assert "APP_BACKGROUND" in source
    assert "SIDEBAR_BACKGROUND" in source
    assert "TOPBAR_BACKGROUND" in source
    assert "CONTENT_MAX_WIDTH" in source
    assert "color_mode_toggle()" in source
