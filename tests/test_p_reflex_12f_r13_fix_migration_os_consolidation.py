from __future__ import annotations

from pathlib import Path


def test_r13_contract_markers_and_no_raw_spam() -> None:
    text = Path("mvp_qaic_reflex_ui/migration_tracker.py").read_text(encoding="utf-8")
    assert "SHOW_ONLY_ESSENTIAL = True" in text
    assert "TABLE_UX_WITH_PERCENTAGES = True" in text
    assert "MIGRATION_GLOBAL_MATRIX_SUMMARY.json" in text
    assert "MIGRATION_GLOBAL_MATRIX.json" in text
    assert "Mission Control: uniquement" in text
    assert "Inventaire analyse" in text
    assert "dedoublonnees" in text
    assert "from mvp_qaic_reflex_ui.migration_os import" in text


def test_r13_payload_is_stable_unique_and_table_ready() -> None:
    from mvp_qaic_reflex_ui.migration_os import build_migration_tracker_payload

    payload = build_migration_tracker_payload()
    assert payload["legacy_row_count"] == 15
    assert payload["table_ux_with_percentages"] is True
    assert payload["show_only_essential"] is True
    assert payload["function_index_count"] >= 2738
    assert payload["row_count"] < 150
    sources = [row["source"] for row in payload["rows"]]
    assert len(sources) == len(set(sources))
    assert "LEXIQUE_CRYPTO_APPROVED" in sources
    assert "MVPQAIC_CLASP_IMPORTS_ALL.csv" in sources
