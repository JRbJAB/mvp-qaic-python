from __future__ import annotations

from pathlib import Path


def test_r13a_private_cockpit_pages_module_has_distinct_routes() -> None:
    from mvp_qaic_reflex_ui import private_cockpit_pages as pages

    assert pages.R2A_R13A_PRIVATE_COCKPIT_ROUTES is True
    assert pages.R2A_R13B_PRIVATE_COCKPIT_ROUTES is True
    assert callable(pages.home_page)
    assert callable(pages.cdc_tracker_page)
    assert callable(pages.cdc_dev_tracker_page)
    assert callable(pages.dev_tracking_page)


def test_r13a_app_registers_private_cockpit_routes() -> None:
    root = Path(__file__).resolve().parents[1]
    text = (root / "mvp_qaic_reflex_ui" / "mvp_qaic_reflex_ui.py").read_text(
        encoding="utf-8", errors="replace"
    )
    assert "R2A_R13B_BEGIN_PRIVATE_COCKPIT_SOURCE_ROUTES" in text
    for route in ["/", "/cdc-tracker", "/cdc-dev-tracker", "/dev-tracking"]:
        assert f'route="{route}"' in text


def test_r13a_pages_define_business_labels() -> None:
    root = Path(__file__).resolve().parents[1]
    text = (root / "mvp_qaic_reflex_ui" / "private_cockpit_pages.py").read_text(encoding="utf-8")
    for marker in [
        "MVP QAIC - Migration & Prompt Cockpit",
        "CDC Tracker",
        "CDC + Dev Tracker",
        "Dev Tracking - Migration OS",
        "Prompt portfolio",
        "No public deploy, no broker, no order, no sizing, no live action",
    ]:
        assert marker in text
