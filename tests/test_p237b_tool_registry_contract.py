from pathlib import Path
import csv
import json


def test_p237b_tool_registry_files_exist():
    root = Path.cwd()
    assert (root / "docs" / "TOOL_REGISTRY_CDC.md").exists()
    assert (root / "docs" / "TOOL_REGISTRY_SCHEMA.md").exists()
    assert (root / "docs" / "TOOL_REGISTRY_CHANGELOG.md").exists()
    assert (root / "data" / "tool_registry" / "tools_global.json").exists()
    assert (root / "data" / "tool_registry" / "tools_project_mvp_qaic.json").exists()
    assert (root / "data" / "tool_registry" / "tool_registry_snapshot.json").exists()
    assert (root / "data" / "tool_registry" / "tool_registry_export.csv").exists()


def test_p237b_tool_registry_safety_invariants():
    root = Path.cwd()
    snapshot = json.loads(
        (root / "data" / "tool_registry" / "tool_registry_snapshot.json").read_text(
            encoding="utf-8"
        )
    )
    assert snapshot["repo_root"].endswith(r"C:\JRb_TRADING_OS\MVP_QAIC_PY")
    assert snapshot["reflex_page_written"] is False
    assert snapshot["reflex_routing_modified"] is False
    assert snapshot["external_writes"] is False
    assert snapshot["userprofile_write"] is False
    assert snapshot["safety"]["apps_script_execution"] is False
    assert snapshot["safety"]["sheet_write"] is False
    assert snapshot["safety"]["bigquery_write"] is False
    assert snapshot["safety"]["broker"] is False
    assert snapshot["safety"]["order"] is False
    assert snapshot["safety"]["sizing"] is False


def test_p237b_tool_registry_csv_has_core_tools():
    root = Path.cwd()
    csv_path = root / "data" / "tool_registry" / "tool_registry_export.csv"
    rows = list(csv.DictReader(csv_path.open("r", encoding="utf-8-sig")))
    ids = {row["tool_id"] for row in rows}
    assert "python" in ids
    assert "reflex" in ids
    assert "git" in ids
    assert "mvp_qaic_private_webapp" in ids
