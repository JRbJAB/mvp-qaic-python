import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from mvp_qaic_reflex_ui.migration_tracker import (
    MIGRATION_TRACKER_DOCS,
    MIGRATION_TRACKER_ROWS,
    build_migration_tracker_payload,
    migration_average_progress,
    migration_tracker_compact_panel,
    migration_tracker_summary_rows,
)
from mvp_qaic_reflex_ui.pages_landing import home


UNESCAPED_AMPERSAND = re.compile(r"&(?!amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9a-fA-F]+;)")


def test_p12c_svg_files_are_valid_xml_and_have_no_unescaped_ampersand():
    for path in (
        Path("assets/mvp_qaic_web_architecture_schema.svg"),
        Path("docs/WEB_ARCHITECTURE_SCHEMA.svg"),
    ):
        text = path.read_text(encoding="utf-8")
        assert not UNESCAPED_AMPERSAND.search(text)
        root = ET.fromstring(text)
        assert root.tag.endswith("svg")


def test_p12c_migration_tracker_docs_exist_and_match_payload():
    assert Path(MIGRATION_TRACKER_DOCS["json"]).exists()
    assert Path(MIGRATION_TRACKER_DOCS["markdown"]).exists()

    payload = json.loads(Path(MIGRATION_TRACKER_DOCS["json"]).read_text(encoding="utf-8"))

    assert payload["schema_version"] == "migration_tracker.v1"
    assert payload["tracker_status"] == "READY_COMPACT_MISSION_PANEL"
    assert payload["row_count"] == len(MIGRATION_TRACKER_ROWS)
    assert payload["safety"]["public_deploy"] is False
    assert payload["safety"]["broker_order_sizing"] is False


def test_p12c_migration_tracker_has_sheets_apps_script_and_functionality_rows():
    source_types = {row["source_type"] for row in MIGRATION_TRACKER_ROWS}
    source_names = {row["source_name"] for row in MIGRATION_TRACKER_ROWS}

    assert "SHEET_TAB" in source_types
    assert "APPS_SCRIPT_FILE" in source_types
    assert "APPS_SCRIPT_FUNCTION" in source_types
    assert "FUNCTIONALITY" in source_types
    assert "LEXIQUE_CRYPTO_APPROVED" in source_names
    assert "mvpqaic_09_p1_journal_core.gs" in source_names
    assert "MVPQAIC_CLASP_IMPORTS_ALL.csv" in source_names


def test_p12c_migration_tracker_progress_is_valid():
    assert len(MIGRATION_TRACKER_ROWS) >= 15
    average = migration_average_progress()

    assert average > 0
    assert average <= 100

    for row in MIGRATION_TRACKER_ROWS:
        assert row["migration_id"].startswith("MIG-")
        assert row["target"].startswith("/")
        assert 0 <= row["progress_percent"] <= 100
        assert row["priority"] in {"P0", "P1"}


def test_p12c_migration_tracker_payload_and_summary_are_safe():
    payload = build_migration_tracker_payload()
    summary = migration_tracker_summary_rows()

    assert payload["tracker_status"] == "READY_COMPACT_MISSION_PANEL"
    assert payload["public_deploy"] is False
    assert payload["broker_order_sizing"] is False
    assert payload["sheet_write"] is False
    assert payload["bigquery_write"] is False
    assert summary["sheet_write"] is False
    assert summary["bigquery_write"] is False


def test_p12c_migration_tracker_component_and_home_render():
    assert migration_tracker_compact_panel() is not None
    assert home() is not None

    source = Path("mvp_qaic_reflex_ui/pages_landing.py").read_text(encoding="utf-8")
    assert "migration_tracker_compact_panel()" in source
