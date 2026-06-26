from __future__ import annotations
from pathlib import Path


def test_p12f_global_migration_route_or_contract_present() -> None:
    package = Path.cwd() / "mvp_qaic_reflex_ui"
    text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in package.glob("*.py"))
    assert "/migration/global" in text
    assert "global_migration_page" in text


def test_p12f_statuses_keep_machine_english_and_french_labels() -> None:
    from mvp_qaic_reflex_ui.migration_global_matrix import STATUS_LEGEND

    assert "MIGRATE_NOW" in STATUS_LEGEND
    assert STATUS_LEGEND["MIGRATE_NOW"]["fr"]
    assert "RETIRE_NO_VALUE" in STATUS_LEGEND
    assert "BIGQUERY_FUTURE_CANDIDATE" in STATUS_LEGEND
