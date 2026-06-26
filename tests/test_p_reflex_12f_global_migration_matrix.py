from __future__ import annotations
import csv
from pathlib import Path
from mvp_qaic_reflex_ui.migration_global_matrix import build_matrix, status_fr, write_outputs


def _write_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "record_type",
        "script_file_name",
        "script_id",
        "module_family",
        "function_name",
        "function_visibility",
        "line_number",
        "severity",
        "total_function_count",
        "risk_hit_count",
        "calls_spreadsheet",
        "writes_sheet_likely",
    ]
    rows = [
        {
            "record_type": "SCRIPT_INVENTORY",
            "script_file_name": "mvpqaic_23_gpt_response_intake_core.js",
            "module_family": "PROMPT_ENGINE",
            "severity": "HIGH",
            "total_function_count": "12",
            "risk_hit_count": "3",
            "calls_spreadsheet": "YES",
            "writes_sheet_likely": "YES",
        },
        {
            "record_type": "FUNCTION_INDEX",
            "script_file_name": "mvpqaic_23_gpt_response_intake_core.js",
            "module_family": "PROMPT_ENGINE",
            "function_name": "MVPQAIC_Run",
            "function_visibility": "PUBLIC",
            "line_number": "10",
            "severity": "INFO",
        },
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def test_global_migration_matrix_has_bilingual_status_and_all_scopes(tmp_path: Path) -> None:
    _write_csv(tmp_path / "docs" / "MVPQAIC_CLASP_IMPORTS_ALL.csv")
    payload = build_matrix(tmp_path)
    scopes = {r["scope"] for r in payload["rows"]}
    assert {
        "SHEETS_COCKPIT",
        "APPS_SCRIPT_FILE",
        "APPS_SCRIPT_FUNCTION",
        "FEATURE_CLUSTER",
        "FUTURE_ARCHITECTURE",
    }.issubset(scopes)
    assert payload["status_policy"].startswith("Keep machine statuses in English")
    assert status_fr("MIGRATE_NOW") == "À migrer maintenant"


def test_global_migration_matrix_writes_docs_outputs(tmp_path: Path) -> None:
    _write_csv(tmp_path / "docs" / "MVPQAIC_CLASP_IMPORTS_ALL.csv")
    payload = write_outputs(tmp_path)
    assert payload["summary"]["script_inventory_count"] == 1
    assert (tmp_path / "docs" / "MIGRATION_GLOBAL_MATRIX.csv").exists()
    assert (tmp_path / "docs" / "MIGRATION_GLOBAL_MATRIX.json").exists()
    assert (tmp_path / "docs" / "MIGRATION_GLOBAL_MATRIX.md").exists()
