from __future__ import annotations

from pathlib import Path


def test_p12h1d_r2_start_script_syncs_repo_to_runtime() -> None:
    text = Path("scripts/START_REFLEX_LOCAL_SAFE.ps1").read_text(encoding="utf-8")
    assert "P_REFLEX_12H1D_R2_BEGIN_RUNTIME_SYNC" in text
    assert "SYNC REPO SOURCE TO RUNTIME" in text
    assert '$syncDirs = @("mvp_qaic_reflex_ui", "docs")' in text
    assert "SYNCED_DIR=$dir" in text
    assert "QAIC_REPO_ROOT" in text
    assert "Set-Location -LiteralPath $RuntimeRoot" in text


def test_p12h1d_r2_route_source_exists_in_repo_package() -> None:
    workbench = Path("mvp_qaic_reflex_ui/migration_decision_workbench.py").read_text(
        encoding="utf-8"
    )
    app = Path("mvp_qaic_reflex_ui/mvp_qaic_reflex_ui.py").read_text(encoding="utf-8")
    landing = Path("mvp_qaic_reflex_ui/pages_landing.py").read_text(encoding="utf-8")
    assert 'MIGRATION_DECISION_WORKBENCH_ROUTE = "/migration/decisions"' in workbench
    assert "migration_decision_workbench_page" in app
    assert "migration_decision_workbench_compact_panel()" in landing
