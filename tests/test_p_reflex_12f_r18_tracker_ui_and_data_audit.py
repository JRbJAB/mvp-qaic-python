from __future__ import annotations

from pathlib import Path

from mvp_qaic_reflex_ui.migration_os import build_migration_tracker_payload

LEGACY_15 = [
    "LEXIQUE_CRYPTO_APPROVED",
    "GPT_QUALITY_DASHBOARD",
    "PROMPT_IMPROVEMENT_QUEUE",
    "DECISION_JOURNAL",
    "QAIC_RUNTIME_COCKPIT_VIEW",
    "QAIC_RUNTIME_BRIDGE_STATUS",
    "BENCHMARK_AI_TRADE",
    "mvpqaic_09_p1_journal_core.gs",
    "Decision journal append / duplicate guard",
    "P132/P133 GEM portfolio multimodal prompt",
    "Prompt correction loop P153/P154/P155/P159",
    "Safety gates no-order/no-sizing/no-public-deploy",
    "WEB_ARCHITECTURE_CDC.md / SITEMAP.json / SCHEMA.svg",
    "MVPQAIC_CLASP_IMPORTS_ALL.csv",
    "MVPQAIC_CLASP_IMPORTS_ALL_HEADERS.csv",
]

ESSENTIAL_SOURCES = {
    "Mission Control",
    "Dev Tracking",
    "CDC Tracker",
    "Migration Tracker",
    "Prompt Cockpit",
    "Runtime Bridge Status",
    "Runtime Cockpit",
    "Lexique / Knowledge Base",
    "WebApp Readiness",
    "Revolut X Readonly Views",
    "Legacy Script Registry",
    "BigQuery Historical Snapshots",
    "BigQuery Decision Facts",
    "JOURNAL",
    "KNOWLEDGE_SEARCH",
    "PROMPT_ENGINE",
    "QAIC_BRIDGE",
    "SCRIPT_REGISTRY",
    "AUDIT_INVENTORY",
    "mvpqaic_01_knowledge_engine.js",
    "mvpqaic_09_p1_journal_core.js",
    "mvpqaic_11_p1_prompt_quality_core.js",
    "mvpqaic_31_lexique_master_search_cockpit_core.js",
    "Fonctions essentielles JOURNAL",
    "Fonctions essentielles KNOWLEDGE_SEARCH",
    "Fonctions essentielles PROMPT_ENGINE",
}


def test_r18_tracker_table_ui_contract_is_locked() -> None:
    text = Path("mvp_qaic_reflex_ui/migration_tracker.py").read_text(encoding="utf-8")
    assert "TRACKER_TABLE_UI_LOCKED = True" in text
    assert "TRACKER_GRID_COLUMNS_LOCKED" in text
    assert "PROGRESS_BLUE_LINE_UI_LOCKED = True" in text
    assert "STATUS_COLOR_UI_LOCKED = True" in text
    assert "Type" in text and "Source" in text and "Cible" in text and "Statut" in text
    assert "grid_template_columns" in text
    assert "#2563eb" in text


def test_r18_original_15_rows_are_exactly_preserved_first() -> None:
    payload = build_migration_tracker_payload()
    sources = [row["source"] for row in payload["rows"]]
    assert payload["legacy_row_count"] == 15
    assert sources[:15] == LEGACY_15


def test_r18_essential_scope_data_is_available_for_next_steps() -> None:
    payload = build_migration_tracker_payload()
    rows = payload["rows"]
    sources = {row["source"] for row in rows}
    types = {row["type"] for row in rows}
    missing = ESSENTIAL_SOURCES - sources
    assert not missing
    assert "SHEETS_COCKPIT" in types
    assert "FEATURE_CLUSTER" in types
    assert "APPS_SCRIPT_FILE" in types
    assert "APPS_SCRIPT_FUNCTION_GROUP" in types
    assert "FUTURE_ARCHITECTURE" in types
    assert payload["function_index_count"] >= 2738
    assert payload["row_count"] < 150
    assert len(sources) == len(rows)
