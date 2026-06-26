from __future__ import annotations

from pathlib import Path

from mvp_qaic_reflex_ui.migration_os import (
    ESSENTIAL_ONLY_POLICY,
    LEGACY_TRACKER_ROWS,
    SHOW_ONLY_ESSENTIAL,
    build_migration_tracker_payload,
)


def test_migration_os_preserves_legacy_table_contract() -> None:
    payload = build_migration_tracker_payload()
    rows = payload["rows"]
    assert SHOW_ONLY_ESSENTIAL is True
    assert ESSENTIAL_ONLY_POLICY == "LEGACY_15_PLUS_LIVE_ESSENTIALS_TABLE_UX"
    assert payload["legacy_row_count"] == 15
    assert rows[:15]
    assert [row["source"] for row in rows[:15]] == [row["source"] for row in LEGACY_TRACKER_ROWS]
    for row in rows:
        assert {"type", "source", "target", "progress", "status"}.issubset(row)


def test_migration_os_does_not_expose_raw_2738_functions_in_visible_rows() -> None:
    payload = build_migration_tracker_payload()
    assert payload["function_index_count"] >= 2738
    assert payload["row_count"] < 150
    sources = [row["source"] for row in payload["rows"]]
    assert len(sources) == len(set(sources))


def test_visible_tracker_keeps_old_ux_markers_and_r9b_contract_strings() -> None:
    text = Path("mvp_qaic_reflex_ui/migration_tracker.py").read_text(encoding="utf-8")
    assert "Type" in text
    assert "Source" in text
    assert "Cible" in text
    assert "Statut" in text
    assert "AVG=" in text
    assert "ROWS=" in text
    assert "Mission Control: uniquement" in text
    assert "Inventaire analyse" in text
