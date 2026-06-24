from __future__ import annotations

import csv
import json
from pathlib import Path

from mvp_qaic_py.p165_initial_system_functional_source_access_layer import (
    build_and_write_export,
    build_function_index,
    build_module_inventory,
    build_prompt_engine_recovery,
    read_csv_dicts,
)


HEADERS = [
    "import_batch_id",
    "imported_at",
    "exported_at",
    "record_type",
    "project_name",
    "apps_script_id",
    "script_id",
    "script_file_name",
    "module_family",
    "detected_version",
    "function_name",
    "function_visibility",
    "function_prefix",
    "line_number",
    "dependency_type",
    "dependency_target",
    "severity",
    "security_flag",
    "file_path",
    "file_size_bytes",
    "line_count",
    "char_count",
    "hash_sha256",
    "public_function_count",
    "internal_function_count",
    "total_function_count",
    "risk_hit_count",
    "has_mvpqaic_reference",
    "has_network_logic",
    "has_bigquery_logic",
    "has_drive_logic",
    "has_properties_logic",
    "has_trigger_logic",
    "has_delete_or_clear_risk",
    "calls_spreadsheet",
    "calls_urlfetch",
    "calls_bigquery",
    "calls_trigger",
    "calls_properties",
    "calls_drive",
    "writes_sheet_likely",
    "network_flags",
    "bigquery_flags",
    "ingestion_flags",
    "trigger_flags",
    "secret_flags",
    "drive_flags",
    "raw_key",
    "raw_value",
    "notes",
    "created_at",
    "updated_at",
]


def _write_csv(path: Path) -> None:
    rows = [
        {
            "record_type": "SCRIPT_INVENTORY",
            "script_file_name": "mvpqaic_11_p1_prompt_quality_core.js",
            "module_family": "PROMPT_ENGINE",
            "detected_version": "0.4.7",
            "public_function_count": "2",
            "internal_function_count": "3",
            "total_function_count": "5",
            "risk_hit_count": "0",
            "calls_spreadsheet": "YES",
            "writes_sheet_likely": "YES",
        },
        {
            "record_type": "FUNCTION_INDEX",
            "script_file_name": "mvpqaic_11_p1_prompt_quality_core.js",
            "module_family": "PROMPT_ENGINE",
            "function_name": "MVPQAIC_PromptAdaptiveRunAllFast",
            "function_visibility": "PUBLIC",
            "line_number": "42",
        },
        {
            "record_type": "FUNCTION_INDEX",
            "script_file_name": "mvpqaic_09_p1_journal_core.js",
            "module_family": "JOURNAL",
            "function_name": "MVPQAIC_DecisionJournalAppend",
            "function_visibility": "PUBLIC",
            "line_number": "99",
        },
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def test_p165_builds_module_and_function_inventory(tmp_path: Path) -> None:
    csv_path = tmp_path / "MVPQAIC_CLASP_IMPORTS_ALL.csv"
    _write_csv(csv_path)
    records = read_csv_dicts(csv_path)

    modules = build_module_inventory(records)
    functions = build_function_index(records)

    assert len(modules) == 1
    assert modules[0]["module_family"] == "PROMPT_ENGINE"
    assert len(functions) == 2
    assert functions[0]["functional_role"] == "PROMPT_OR_AI"
    assert functions[0]["migration_priority"] == "P0"


def test_p165_recovers_prompt_engine_candidates(tmp_path: Path) -> None:
    csv_path = tmp_path / "MVPQAIC_CLASP_IMPORTS_ALL.csv"
    _write_csv(csv_path)
    records = read_csv_dicts(csv_path)

    prompt_rows = build_prompt_engine_recovery(records)

    assert prompt_rows
    assert any(row["function_name"] == "MVPQAIC_PromptAdaptiveRunAllFast" for row in prompt_rows)


def test_p165_writes_python_source_access_exports(tmp_path: Path) -> None:
    csv_path = tmp_path / "MVPQAIC_CLASP_IMPORTS_ALL.csv"
    _write_csv(csv_path)

    summary = build_and_write_export(tmp_path, str(csv_path))

    export_dir = Path(summary.EXPORT_DIR)
    assert summary.PYTHON_SOURCE_ACCESS_LAYER_CREATED is True
    assert summary.INITIAL_SHEET_APPS_SCRIPT_RECOVERY_READY is True
    assert summary.APPS_SCRIPT_FUNCTION_COUNT == 2
    assert summary.PROMPT_ENGINE_FUNCTION_COUNT >= 1
    assert summary.RUNTIME_PROMPT_MODIFIED is False
    assert summary.APPLY_ALLOWED is False
    assert summary.BLOCKER_COUNT == 0
    assert (export_dir / "P165_R3_SOURCE_REGISTRY.csv").exists()
    assert (export_dir / "P165_R3_APPS_SCRIPT_FUNCTION_INDEX.csv").exists()
    assert (export_dir / "P165_R3_FUNCTIONAL_MIGRATION_MAP.csv").exists()
    assert (export_dir / "P165_R3_SHEETS_DATA_ACCESS_PLAN.csv").exists()

    payload = json.loads((export_dir / "P165_R3_SUMMARY.json").read_text(encoding="utf-8"))
    assert payload["P132_P133_DEMOTED_TO_RUNTIME_CONTRACT_ONLY"] is True
    assert payload["NEXT"] == "P166_REFERENCE_PROMPT_REBUILD_FROM_SOURCE_INDEX_OR_LIVE_EXPORT"
