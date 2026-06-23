from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p168c_sheets_readonly_export_import_or_api_binding import (
    API_CONTRACT_FIELDS,
    MANIFEST_COLUMNS,
    build_api_contract_rows,
    build_binding_strategy,
    build_manifest_template,
    build_outputs,
    discover_latest_p168b_export,
)


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _seed_p168b_export(
    root: Path,
    name: str = "P168B_SHEETS_DATA_SNAPSHOT_LAYER_READONLY_20260623_020202",
    hierarchy_locked: bool = True,
) -> Path:
    export = root / "05_EXPORTS" / name
    export.mkdir(parents=True)
    (export / "P168B_SUMMARY.json").write_text(
        json.dumps({"status": "OK", "hierarchy_locked": hierarchy_locked}),
        encoding="utf-8",
    )
    rows = [
        {
            "priority": "P0",
            "source_key": "LIVE_SHEET_MVP_QAIC_DEV",
            "spreadsheet_id": "sheet1",
            "spreadsheet_title": "MVP",
            "tab_name": "CONFIG",
            "bounded_range": "A1:D200",
            "purpose": "config",
            "snapshot_filename": "CONFIG.csv",
            "required_before_python_port": "YES",
        },
        {
            "priority": "P0",
            "source_key": "LIVE_SHEET_MVP_QAIC_DEV",
            "spreadsheet_id": "sheet1",
            "spreadsheet_title": "MVP",
            "tab_name": "LEXIQUE_CRYPTO_APPROVED",
            "bounded_range": "A1:Z5000",
            "purpose": "lexique",
            "snapshot_filename": "LEXIQUE.csv",
            "required_before_python_port": "YES",
        },
        {
            "priority": "P0",
            "source_key": "LIVE_SHEET_MVP_QAIC_DEV",
            "spreadsheet_id": "sheet1",
            "spreadsheet_title": "MVP",
            "tab_name": "PROMPT_IMPROVEMENT_QUEUE",
            "bounded_range": "A1:Z5000",
            "purpose": "prompts",
            "snapshot_filename": "PROMPTS.csv",
            "required_before_python_port": "YES",
        },
        {
            "priority": "P1",
            "source_key": "LIVE_SHEET_MVP_QAIC_DEV",
            "spreadsheet_id": "sheet1",
            "spreadsheet_title": "MVP",
            "tab_name": "DECISION_JOURNAL",
            "bounded_range": "A1:Z5000",
            "purpose": "journal",
            "snapshot_filename": "JOURNAL.csv",
            "required_before_python_port": "YES",
        },
        {
            "priority": "P1",
            "source_key": "LIVE_SHEET_MVP_QAIC_DEV",
            "spreadsheet_id": "sheet1",
            "spreadsheet_title": "MVP",
            "tab_name": "GPT_QUALITY_DASHBOARD",
            "bounded_range": "A1:Z2000",
            "purpose": "quality",
            "snapshot_filename": "QUALITY.csv",
            "required_before_python_port": "REVIEW",
        },
        {
            "priority": "REFERENCE_ONLY",
            "source_key": "LIVE_SHEET_QAIC_CRYPTO_V25_DEV",
            "spreadsheet_id": "sheet2",
            "spreadsheet_title": "QAIC",
            "tab_name": "REFERENCE_ONLY_NO_MVP_PORT",
            "bounded_range": "N/A",
            "purpose": "reference only",
            "snapshot_filename": "NO.csv",
            "required_before_python_port": "NO",
        },
    ]
    _write_csv(export / "P168B_BOUNDED_READ_PLAN.csv", rows)
    return export


def test_discover_latest_p168b_export_is_deterministic_by_name(tmp_path: Path) -> None:
    _seed_p168b_export(tmp_path, "P168B_SHEETS_DATA_SNAPSHOT_LAYER_READONLY_20260623_010101")
    newest = _seed_p168b_export(
        tmp_path, "P168B_SHEETS_DATA_SNAPSHOT_LAYER_READONLY_20260623_020202"
    )
    assert discover_latest_p168b_export(tmp_path) == newest


def test_binding_strategy_prefers_local_export_import_now() -> None:
    rows = [
        {"tab_name": "CONFIG", "required_before_python_port": "YES", "priority": "P0"},
        {"tab_name": "REF", "required_before_python_port": "NO", "priority": "REFERENCE_ONLY"},
    ]
    strategy = build_binding_strategy(rows)
    assert strategy[0]["preferred_path_now"] == "LOCAL_EXPORT_IMPORT_FIRST"
    assert strategy[0]["api_binding_later"] == "GOOGLE_SHEETS_API_READONLY"
    assert strategy[0]["write_allowed"] == "NO"
    assert strategy[1]["binding_action"] == "REFERENCE_ONLY_NO_MVP_IMPORT"


def test_manifest_template_excludes_reference_only() -> None:
    rows = [
        {
            "tab_name": "CONFIG",
            "required_before_python_port": "YES",
            "snapshot_filename": "CONFIG.csv",
        },
        {"tab_name": "REF", "required_before_python_port": "NO", "snapshot_filename": "REF.csv"},
    ]
    manifest = build_manifest_template(rows)
    assert len(manifest) == 1
    assert list(manifest[0].keys()) == MANIFEST_COLUMNS
    assert manifest[0]["operator_review_status"] == "PENDING_EXPORT"


def test_api_contract_is_read_only() -> None:
    rows = [
        {
            "source_key": "S",
            "spreadsheet_id": "id",
            "tab_name": "CONFIG",
            "bounded_range": "A1:D200",
            "required_before_python_port": "YES",
        }
    ]
    contract = build_api_contract_rows(rows)
    assert list(contract[0].keys()) == API_CONTRACT_FIELDS
    assert contract[0]["read_only_scope"] == "spreadsheets.readonly"
    assert contract[0]["write_allowed"] == "NO"


def test_build_outputs_creates_review_only_binding_pack(tmp_path: Path) -> None:
    _seed_p168b_export(tmp_path)
    export = build_outputs(tmp_path)
    summary = json.loads((export / "P168C_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["blocker_count"] == 0
    assert summary["hierarchy_locked"] is True
    assert summary["preferred_path_now"] == "LOCAL_EXPORT_IMPORT_FIRST"
    assert summary["live_google_api_call_from_python"] is False
    assert summary["google_sheets_write"] is False
    assert summary["manifest_template_count"] == 5
    assert (export / "P168C_READONLY_BINDING_STRATEGY.csv").exists()
    assert (export / "P168C_API_BINDING_CONTRACT.md").exists()


def test_build_outputs_blocks_when_hierarchy_missing(tmp_path: Path) -> None:
    _seed_p168b_export(tmp_path, hierarchy_locked=False)
    export = build_outputs(tmp_path)
    summary = json.loads((export / "P168C_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["blocker_count"] >= 1
    assert "P168B_HIERARCHY_NOT_LOCKED" in summary["blockers"]
