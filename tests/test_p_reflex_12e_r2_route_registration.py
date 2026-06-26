from __future__ import annotations

from pathlib import Path


def test_p12e_r2_route_registration_best_effort_or_fallback_module() -> None:
    repo = Path.cwd()
    package = repo / "mvp_qaic_reflex_ui"
    py_files = [p for p in package.rglob("*.py") if p.is_file()]
    combined = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in py_files)

    assert "/architecture-web/schema" in combined
    assert "/trackers/auto-update" in combined
    assert "schema_large_page" in combined
    assert "auto_update_trackers_page" in combined


def test_p12e_r2_main_app_has_no_broken_r2c_import_markers() -> None:
    app_path = Path("mvp_qaic_reflex_ui/mvp_qaic_reflex_ui.py")
    text = app_path.read_text(encoding="utf-8")
    assert "P_REFLEX_12E_R2C_BEGIN_IMPORTS" not in text
    assert "P_REFLEX_12E_R2C_BEGIN_ROUTES" not in text
    assert (
        "P_REFLEX_12E_R2D_BEGIN_SAFE_ROUTE_WIRING" in text
        or Path("mvp_qaic_reflex_ui/p_reflex_12e_r2_route_contract.py").exists()
    )
