from __future__ import annotations

from pathlib import Path


def test_r10_restores_table_ux_and_preserves_legacy_rows() -> None:
    text = Path("mvp_qaic_reflex_ui/migration_tracker.py").read_text(encoding="utf-8")
    assert "TABLE_UX_WITH_PERCENTAGES = True" in text
    assert "LEGACY_STATIC_ROWS" in text
    assert "LEXIQUE_CRYPTO_APPROVED" in text
    assert "MVPQAIC_CLASP_IMPORTS_ALL.csv" in text
    assert "Type" in text and "Source" in text and "Cible" in text and "Statut" in text
    assert "AVG=" in text and "ROWS=" in text


def test_r10_tracker_payload_contract() -> None:
    import mvp_qaic_reflex_ui.migration_tracker as tracker

    payload = tracker.build_migration_tracker_payload()
    assert payload["legacy_row_count"] == 15
    assert payload["table_ux_with_percentages"] is True
    assert payload["show_only_essential"] is True
    assert payload["row_count"] >= 15
    sources = {row["source"] for row in payload["rows"]}
    assert "LEXIQUE_CRYPTO_APPROVED" in sources
    assert "MVPQAIC_CLASP_IMPORTS_ALL.csv" in sources


def test_r10_no_raw_function_spam_marker() -> None:
    text = Path("mvp_qaic_reflex_ui/migration_tracker.py").read_text(encoding="utf-8")
    assert "dedoublonnees" in text
    assert "2738 fonctions brutes restent agregees" in text
