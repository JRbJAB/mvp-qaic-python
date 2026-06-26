from __future__ import annotations

from pathlib import Path


def test_visible_migration_tracker_is_essential_only() -> None:
    text = Path("mvp_qaic_reflex_ui/migration_tracker.py").read_text(encoding="utf-8")
    assert "SHOW_ONLY_ESSENTIAL = True" in text
    assert "Mission Control: uniquement" in text
    assert "Fonctions Apps Script essentielles" in text
    assert "top limite, pas les 2738 brutes" in text
    assert "ROWS=15" not in text
    assert "AVG=45.67" not in text


def test_visible_migration_tracker_uses_global_matrix_but_aggregates_raw_functions() -> None:
    text = Path("mvp_qaic_reflex_ui/migration_tracker.py").read_text(encoding="utf-8")
    assert "MIGRATION_GLOBAL_MATRIX_SUMMARY.json" in text
    assert "MIGRATION_GLOBAL_MATRIX.json" in text
    assert "Inventaire analyse" in text
    assert "Essentiels affiches" in text
    assert "/migration/global" in text


def test_visible_migration_tracker_import_contract() -> None:
    import mvp_qaic_reflex_ui.migration_tracker as tracker

    assert callable(tracker.migration_tracker_panel)
    assert callable(tracker.migration_tracker)
