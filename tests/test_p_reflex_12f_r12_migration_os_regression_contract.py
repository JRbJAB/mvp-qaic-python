from __future__ import annotations

from pathlib import Path


def test_r12_migration_os_payload_keeps_legacy_table_contract() -> None:
    from mvp_qaic_reflex_ui.migration_os import build_migration_tracker_payload

    payload = build_migration_tracker_payload()
    assert payload["legacy_row_count"] == 15
    assert payload["table_ux_with_percentages"] is True
    assert payload["show_only_essential"] is True
    assert payload["raw_matrix_visible"] is False
    assert payload["function_index_count"] >= 2738
    assert payload["row_count"] < 150


def test_r12_sources_are_unique_and_legacy_rows_are_preserved() -> None:
    from mvp_qaic_reflex_ui.migration_os import build_migration_tracker_payload

    payload = build_migration_tracker_payload()
    sources = [row["source"] for row in payload["rows"]]
    assert len(sources) == len(set(sources))
    for required in [
        "LEXIQUE_CRYPTO_APPROVED",
        "GPT_QUALITY_DASHBOARD",
        "PROMPT_IMPROVEMENT_QUEUE",
        "DECISION_JOURNAL",
        "QAIC_RUNTIME_COCKPIT_VIEW",
        "QAIC_RUNTIME_BRIDGE_STATUS",
        "BENCHMARK_AI_TRADE",
        "MVPQAIC_CLASP_IMPORTS_ALL.csv",
        "MVPQAIC_CLASP_IMPORTS_ALL_HEADERS.csv",
    ]:
        assert required in sources


def test_r12_visible_tracker_keeps_old_markers_for_regression_tests() -> None:
    text = Path("mvp_qaic_reflex_ui/migration_tracker.py").read_text(encoding="utf-8")
    assert "SHOW_ONLY_ESSENTIAL = True" in text
    assert "TABLE_UX_WITH_PERCENTAGES = True" in text
    assert "Mission Control: uniquement" in text
    assert "Inventaire analyse" in text
    assert "MIGRATION_GLOBAL_MATRIX_SUMMARY.json" in text
    assert "MIGRATION_GLOBAL_MATRIX.json" in text
    assert "dedoublonnees" in text
    assert "Type" in text and "Source" in text and "Cible" in text and "Statut" in text
