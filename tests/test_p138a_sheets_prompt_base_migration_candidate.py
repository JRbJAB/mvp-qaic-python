from __future__ import annotations

import csv
import json
import subprocess
import sys

from mvp_qaic_py.p138a_sheets_prompt_base_migration_candidate import (
    P138ARequest,
    build_migration_payload,
    build_process_simplification_spec,
    build_source_tab_contract,
    candidates_from_tab_values,
    canonical_prompt_registry_fields,
    normalize_prompt_library_row,
    write_p138a_pack,
)


def test_p138a_process_simplification_spec_contains_ultimate_python_rules():
    spec = build_process_simplification_spec()

    assert spec["status"] == "PYTHON_ULTIMATE_PROCESS_SIMPLIFICATION_READY"
    assert (
        "one canonical PromptMigrationCandidate table"
        in spec["ultimate_simplification_rules"]["single_registry"]
    )
    assert spec["sheets_write_policy"]["p138a"] == "NO_SHEETS_WRITE"
    assert spec["sheets_write_policy"]["p138c"] == "SHEETS_WRITE_AFTER_EXPLICIT_GO_ONLY"


def test_p138a_source_tab_contract_targets_old_sheets_base():
    contract = build_source_tab_contract()

    assert "📘 PROMPT_LIBRARY" in contract["source_tabs"]
    assert "GPT_PROMPT_RUNTIME_SPEC" in contract["source_tabs"]
    assert "QAIC_OUTPUT_CONTRACT" in contract["source_tabs"]
    assert "📘 PROMPT_LIBRARY" in contract["target_write_tabs_after_validation"]
    assert "prompt_template_to_copy" in contract["primary_prompt_fields"]


def test_p138a_normalizes_prompt_library_locked_reference():
    row = {
        "contract_id": "P2G-RUNTIME-PROMPT-005",
        "prompt_id": "prompt_05_full_trading_review",
        "prompt_family": "FULL_TRADING_REVIEW",
        "gem_profile": "GEM_GENERAL_REVIEW",
        "target_runtime": "P5 Full Review Runtime",
        "record_type": "PROMPT_CONTRACT",
        "prompt_version_role": "ULTIMATE_REFERENCE_LOCKED",
        "status": "ACTIVE",
        "validation_status": "READY_TO_TEST",
        "is_reference_locked": "YES",
        "prompt_template_to_copy": "# Prompt test\nHUMAN_REVIEW_ONLY",
        "base_prompt_id": "prompt_05_full_trading_review",
    }

    candidate = normalize_prompt_library_row(row, source_tab="📘 PROMPT_LIBRARY", source_row=12)

    assert candidate.prompt_id == "prompt_05_full_trading_review"
    assert candidate.is_reference_locked is True
    assert (
        candidate.python_simplification_action
        == "PRESERVE_LOCKED_REFERENCE_AND_CREATE_VALIDATED_VARIANT"
    )
    assert candidate.target_row_strategy == "CREATE_VARIANT_ROW_DO_NOT_OVERWRITE_REFERENCE"
    assert candidate.write_status == "PLANNED_ONLY_NO_WRITE_BEFORE_VALIDATION"
    assert candidate.p137_correction_status == "REQUIRED"
    assert candidate.p133_compatibility_status == "READY_FOR_VALIDATION"
    assert candidate.blockers == ()


def test_p138a_detects_header_and_extracts_candidates():
    values = [
        ["banner", "metadata"],
        ["contract_id", "prompt_id", "prompt_detail", "gem_profile", "record_type"],
        ["C1", "prompt_01", "# Prompt 01", "GEM_PORTFOLIO_REVIEW", "PROMPT_CONTRACT"],
        ["C2", "prompt_02", "# Prompt 02", "GEM_MARKET_REVIEW", "PROMPT_VARIANT"],
    ]

    candidates = candidates_from_tab_values(values, source_tab="📘 PROMPT_LIBRARY")

    assert len(candidates) == 2
    assert candidates[0].prompt_id == "prompt_01"
    assert candidates[1].record_type == "PROMPT_VARIANT"


def test_p138a_missing_prompt_text_blocks():
    row = {
        "prompt_id": "prompt_empty",
        "gem_profile": "GEM_GENERAL_REVIEW",
        "record_type": "PROMPT_CONTRACT",
    }

    candidate = normalize_prompt_library_row(row, source_tab="📘 PROMPT_LIBRARY", source_row=99)

    assert "PROMPT_TEXT_MISSING" in candidate.blockers
    assert candidate.p137_correction_status == "BLOCKED_NO_PROMPT_TEXT"
    assert candidate.p133_compatibility_status == "BLOCKED"


def test_p138a_payload_without_csv_requires_source_export(tmp_path):
    payload = build_migration_payload(
        P138ARequest(
            output_dir=tmp_path / "out",
            csv_dir=tmp_path / "missing",
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert payload["status"] == "P138A_SOURCE_SHEETS_EXPORT_REQUIRED_FOR_FULL_CANDIDATE"
    assert payload["candidate_count"] == 0
    assert payload["validation_gate"]["blocks_if_source_export_missing"] is True
    assert payload["write_policy"]["sheets_write_in_p138a"] is False


def test_p138a_write_pack_from_csv_dir(tmp_path):
    csv_dir = tmp_path / "csv"
    csv_dir.mkdir()
    csv_file = csv_dir / "PROMPT_LIBRARY.csv"
    with csv_file.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["contract_id", "prompt_id", "prompt_detail", "gem_profile", "record_type"])
        writer.writerow(
            ["C1", "prompt_01", "# Prompt 01", "GEM_PORTFOLIO_REVIEW", "PROMPT_CONTRACT"]
        )

    out = tmp_path / "out"
    payload = write_p138a_pack(
        P138ARequest(
            output_dir=out,
            csv_dir=csv_dir,
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert payload["status"] == "P138A_MIGRATION_CANDIDATE_READY"
    assert payload["candidate_count"] == 1
    assert (out / "P138A_MIGRATION_PAYLOAD.json").exists()
    assert (out / "P138A_MIGRATION_CANDIDATES.csv").exists()
    assert (out / "P138A_PROCESS_SIMPLIFICATION_SPEC.md").exists()
    assert (out / "P138A_VALIDATION_PLAN.md").exists()


def test_p138a_canonical_fields_include_future_write_traceability():
    fields = canonical_prompt_registry_fields()

    assert "source_tab" in fields
    assert "source_row" in fields
    assert "source_hash" in fields
    assert "write_status" in fields
    assert "target_sheet" in fields
    assert "target_row_strategy" in fields


def test_p138a_cli_dry_run_export(tmp_path):
    out = tmp_path / "out"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p138a_sheets_prompt_base_migration_candidate",
            "--output-dir",
            str(out),
            "--generated-at-utc",
            "2026-06-22T00:00:00Z",
            "--dry-run-export",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "P138A_SOURCE_SHEETS_EXPORT_REQUIRED_FOR_FULL_CANDIDATE" in completed.stdout
    assert (out / "P138A_MIGRATION_PAYLOAD.json").exists()
    payload = json.loads((out / "P138A_MIGRATION_PAYLOAD.json").read_text(encoding="utf-8"))
    assert payload["write_policy"]["sheets_write_in_p138a"] is False
    assert (
        payload["process_simplification_spec"]["status"]
        == "PYTHON_ULTIMATE_PROCESS_SIMPLIFICATION_READY"
    )
