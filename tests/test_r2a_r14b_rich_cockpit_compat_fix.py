from pathlib import Path


def test_r14b_restores_r13b_app_marker() -> None:
    from mvp_qaic_reflex_ui import mvp_qaic_reflex_ui as app_module

    assert app_module.R2A_R13B_PRIVATE_COCKPIT_APP_ENTRYPOINT is True
    assert app_module.R2A_R14B_RICH_COCKPIT_COMPAT_FIX is True


def test_r14b_keeps_r13b_route_markers_and_rich_cockpit() -> None:
    root = Path(__file__).resolve().parents[1]
    pages = (root / "mvp_qaic_reflex_ui" / "private_cockpit_pages.py").read_text(encoding="utf-8")
    for marker in [
        "CDC TRACKER / PRIVATE ROUTE",
        "CDC + DEV TRACKER / PRIVATE ROUTE",
        "DEV TRACKING / MIGRATION OS",
        "R2A_R14A_RICH_MIGRATION_COCKPIT",
    ]:
        assert marker in pages
