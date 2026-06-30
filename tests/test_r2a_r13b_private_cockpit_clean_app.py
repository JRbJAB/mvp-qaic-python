from __future__ import annotations

import compileall
import importlib
from pathlib import Path


def test_r13b_app_file_is_valid_python() -> None:
    root = Path(__file__).resolve().parents[1]
    app_file = root / "mvp_qaic_reflex_ui" / "mvp_qaic_reflex_ui.py"
    assert compileall.compile_file(str(app_file), quiet=1)


def test_r13b_app_imports_cleanly() -> None:
    module = importlib.import_module("mvp_qaic_reflex_ui.mvp_qaic_reflex_ui")
    assert module.R2A_R13B_PRIVATE_COCKPIT_APP_ENTRYPOINT is True
    assert module.app is not None


def test_r13b_preview_routes_are_distinct_source_pages() -> None:
    root = Path(__file__).resolve().parents[1]
    pages = (root / "mvp_qaic_reflex_ui" / "private_cockpit_pages.py").read_text(encoding="utf-8")
    for marker in [
        "CDC TRACKER / PRIVATE ROUTE",
        "CDC + DEV TRACKER / PRIVATE ROUTE",
        "DEV TRACKING / MIGRATION OS",
    ]:
        assert marker in pages
