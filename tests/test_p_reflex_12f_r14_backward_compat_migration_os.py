from __future__ import annotations

from pathlib import Path

from mvp_qaic_reflex_ui.migration_os import (
    ESSENTIAL_ONLY_POLICY,
    MIGRATION_GLOBAL_MATRIX,
    MIGRATION_GLOBAL_MATRIX_SUMMARY,
    SHOW_ONLY_ESSENTIAL,
    TABLE_UX_WITH_PERCENTAGES,
    build_migration_tracker_payload,
)


def test_r14_backward_compat_symbols_are_public() -> None:
    assert SHOW_ONLY_ESSENTIAL is True
    assert TABLE_UX_WITH_PERCENTAGES is True
    assert "Mission Control: uniquement" in ESSENTIAL_ONLY_POLICY
    assert MIGRATION_GLOBAL_MATRIX == "MIGRATION_GLOBAL_MATRIX.json"
    assert MIGRATION_GLOBAL_MATRIX_SUMMARY == "MIGRATION_GLOBAL_MATRIX_SUMMARY.json"


def test_r14_payload_table_contract_and_dedupe() -> None:
    payload = build_migration_tracker_payload()
    assert payload["legacy_row_count"] == 15
    assert payload["table_ux_with_percentages"] is True
    assert payload["show_only_essential"] is True
    assert payload["raw_matrix_visible"] is False
    assert payload["row_count"] < 150
    assert payload["function_index_count"] >= 2738
    sources = [row["source"] for row in payload["rows"]]
    assert len(sources) == len(set(sources))


def test_r14_visible_tracker_keeps_old_markers() -> None:
    text = Path("mvp_qaic_reflex_ui/migration_tracker.py").read_text(encoding="utf-8")
    assert "SHOW_ONLY_ESSENTIAL = True" in text
    assert "TABLE_UX_WITH_PERCENTAGES = True" in text
    assert "MIGRATION_GLOBAL_MATRIX_SUMMARY.json" in text
    assert "MIGRATION_GLOBAL_MATRIX.json" in text
    assert "Mission Control: uniquement" in text
    assert "Inventaire analyse" in text
    assert "dedoublonnees" in text
