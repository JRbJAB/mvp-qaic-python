from __future__ import annotations

from mvp_qaic_reflex_ui import migration_os
from mvp_qaic_reflex_ui import migration_tracker


def test_r15_public_symbols_are_backward_compatible() -> None:
    assert migration_os.SHOW_ONLY_ESSENTIAL is True
    assert migration_os.TABLE_UX_WITH_PERCENTAGES is True
    assert migration_os.ESSENTIAL_ONLY_POLICY
    assert len(migration_os.LEGACY_TRACKER_ROWS) == 15
    assert migration_os.MIGRATION_GLOBAL_MATRIX == "MIGRATION_GLOBAL_MATRIX.json"
    assert migration_os.MIGRATION_GLOBAL_MATRIX_SUMMARY == "MIGRATION_GLOBAL_MATRIX_SUMMARY.json"
    assert migration_tracker.SHOW_ONLY_ESSENTIAL is True
    assert migration_tracker.TABLE_UX_WITH_PERCENTAGES is True


def test_r15_payload_keeps_legacy_table_and_limits_raw_functions() -> None:
    payload = migration_os.build_migration_tracker_payload()
    assert payload["legacy_row_count"] == 15
    assert payload["table_ux_with_percentages"] is True
    assert payload["show_only_essential"] is True
    assert payload["function_index_count"] >= 2738
    assert payload["row_count"] < 150
    assert payload["row_count"] >= 15
    assert payload["columns"] == ["Type", "Source", "Cible", "%", "Statut"]
    sources = [row["source"] for row in payload["rows"]]
    assert len(sources) == len(set(sources))
    assert "LEXIQUE_CRYPTO_APPROVED" in sources
    assert "MVPQAIC_CLASP_IMPORTS_ALL.csv" in sources


def test_r15_tracker_text_markers_are_kept_for_operator_audit() -> None:
    text = migration_tracker.__loader__.get_source(migration_tracker.__name__)  # type: ignore[union-attr]
    assert "Mission Control: uniquement" in text
    assert "Inventaire analyse" in text
    assert "dedoublonnees" in text
    assert "MIGRATION_GLOBAL_MATRIX.json" in text
    assert "MIGRATION_GLOBAL_MATRIX_SUMMARY.json" in text
