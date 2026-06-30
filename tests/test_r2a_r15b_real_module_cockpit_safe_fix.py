from __future__ import annotations

import importlib
from pathlib import Path


def test_r15b_app_and_pages_import() -> None:
    app_mod = importlib.import_module("mvp_qaic_reflex_ui.mvp_qaic_reflex_ui")
    pages_mod = importlib.import_module("mvp_qaic_reflex_ui.private_cockpit_pages")

    assert app_mod.R2A_R13B_PRIVATE_COCKPIT_APP_ENTRYPOINT is True
    assert app_mod.R2A_R15B_REAL_MODULE_COCKPIT_SAFE_FIX is True
    assert pages_mod.R2A_R15B_REAL_MODULE_COCKPIT_SAFE_FIX is True
    assert len(pages_mod.MIGRATION_MODULES) >= 6


def test_r15b_real_module_markers_and_safety() -> None:
    root = Path(__file__).resolve().parents[1]
    pages = (root / "mvp_qaic_reflex_ui" / "private_cockpit_pages.py").read_text(encoding="utf-8")
    app = (root / "mvp_qaic_reflex_ui" / "mvp_qaic_reflex_ui.py").read_text(encoding="utf-8")

    for marker in [
        "Prompt Portfolio",
        "CDC Tracker",
        "CDC + Dev Tracker",
        "GEM Response Review Queue",
        "Revolut X Execution Adapter",
        "Lexique / KB Reader",
        "NO_BROKER_NO_ORDER_NO_SIZING",
        "NO_LIVE_ACTION",
        "CDC TRACKER / PRIVATE ROUTE",
        "CDC + DEV TRACKER / PRIVATE ROUTE",
        "DEV TRACKING / MIGRATION OS",
    ]:
        assert marker in pages

    for route in [
        'route="/"',
        'route="/cdc-tracker"',
        'route="/cdc-dev-tracker"',
        'route="/dev-tracking"',
    ]:
        assert route in app
