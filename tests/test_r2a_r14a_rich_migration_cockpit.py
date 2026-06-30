from __future__ import annotations

import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "mvp_qaic_reflex_ui" / "private_cockpit_pages.py"
APP = ROOT / "mvp_qaic_reflex_ui" / "mvp_qaic_reflex_ui.py"


def test_r14a_rich_migration_cockpit_markers() -> None:
    text = PAGES.read_text(encoding="utf-8")
    assert "R2A_R14A_RICH_MIGRATION_COCKPIT" in text
    assert "MIGRATION_MODULES" in text
    assert "Prompt Portfolio" in text
    assert "Revolut X Execution" in text
    assert "cdc_tracker_page" in text
    assert "cdc_dev_tracker_page" in text
    assert "dev_tracking_page" in text


def test_r14a_routes_are_bound_in_app() -> None:
    text = APP.read_text(encoding="utf-8")
    for route in ["/", "/cdc-tracker", "/cdc-dev-tracker", "/dev-tracking"]:
        assert f'route="{route}"' in text
    assert "R2A_R14A_RICH_MIGRATION_COCKPIT_ROUTE_BINDINGS" in text


def test_r14a_imports() -> None:
    importlib.import_module("mvp_qaic_reflex_ui")
    importlib.import_module("mvp_qaic_reflex_ui.mvp_qaic_reflex_ui")
    pages = importlib.import_module("mvp_qaic_reflex_ui.private_cockpit_pages")
    assert callable(pages.home_page)
    assert callable(pages.cdc_tracker_page)
    assert callable(pages.cdc_dev_tracker_page)
    assert callable(pages.dev_tracking_page)
