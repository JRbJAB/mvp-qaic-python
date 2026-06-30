from pathlib import Path


def test_r15c_restores_backward_compat_markers() -> None:
    root = Path(__file__).resolve().parents[1]
    app = (root / "mvp_qaic_reflex_ui" / "mvp_qaic_reflex_ui.py").read_text(encoding="utf-8")
    pages = (root / "mvp_qaic_reflex_ui" / "private_cockpit_pages.py").read_text(encoding="utf-8")

    for marker in [
        "R2A_R13B_BEGIN_PRIVATE_COCKPIT_SOURCE_ROUTES",
        "R2A_R14A_RICH_MIGRATION_COCKPIT_ROUTE_BINDINGS",
        "R2A_R14B_RICH_COCKPIT_COMPAT_FIX",
        "R2A_R15C_COMPAT_MARKERS_RESTORED",
    ]:
        assert marker in app

    for marker in [
        "R2A_R13A_PRIVATE_COCKPIT_ROUTES",
        "MVP QAIC - Migration & Prompt Cockpit",
        "CDC Tracker",
        "CDC + Dev Tracker",
        "Dev Tracking - Migration OS",
        "Prompt portfolio",
        "No public deploy, no broker, no order, no sizing, no live action",
        "CDC TRACKER / PRIVATE ROUTE",
        "CDC + DEV TRACKER / PRIVATE ROUTE",
        "DEV TRACKING / MIGRATION OS",
        "R2A_R15C_COMPAT_MARKERS_RESTORED",
    ]:
        assert marker in pages
