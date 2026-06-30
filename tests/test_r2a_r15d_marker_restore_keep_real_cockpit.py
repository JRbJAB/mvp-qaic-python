"""R2A-R15D: restore missing legacy marker without regressing real module cockpit."""

from __future__ import annotations

from pathlib import Path


def test_r15d_restores_missing_r13b_route_marker() -> None:
    from mvp_qaic_reflex_ui import private_cockpit_pages as pages

    assert pages.R2A_R13A_PRIVATE_COCKPIT_ROUTES is True
    assert pages.R2A_R13B_PRIVATE_COCKPIT_ROUTES is True
    assert pages.R2A_R15D_REAL_MODULE_COCKPIT_MARKER_RESTORE is True


def test_r15d_keeps_real_module_cockpit_contract() -> None:
    root = Path(__file__).resolve().parents[1]
    pages_text = (root / "mvp_qaic_reflex_ui" / "private_cockpit_pages.py").read_text(
        encoding="utf-8"
    )
    app_text = (root / "mvp_qaic_reflex_ui" / "mvp_qaic_reflex_ui.py").read_text(encoding="utf-8")

    for marker in [
        "R2A_R15B_REAL_MODULE_COCKPIT_SAFE_FIX",
        "Prompt Portfolio",
        "CDC Tracker",
        "Dev Tracker",
        "GEM Response Review Queue",
        "Revolut X Execution Adapter",
        "Lexique / KB Reader",
        "No public deploy, no broker, no order, no sizing, no live action",
    ]:
        assert marker in pages_text

    for route in ["/", "/cdc-tracker", "/cdc-dev-tracker", "/dev-tracking"]:
        assert f'route="{route}"' in app_text

    assert "R2A_R15D_REAL_MODULE_COCKPIT_MARKER_RESTORE" in app_text
