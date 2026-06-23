from __future__ import annotations

import json
import subprocess
import sys

import pytest

from mvp_qaic_py.p138c_safe_partial_sheets_write import (
    EXPLICIT_GO_PHRASE,
    P138CRequest,
    build_row_for_headers,
    rehydrate_safe_candidates,
    required_output_headers,
    write_preflight_pack,
)


def _candidate(**overrides):
    base = {
        "migration_id": "MIG-001",
        "source_spreadsheet_id": "sheet123",
        "source_tab": "📘 PROMPT_LIBRARY",
        "source_row": 10,
        "source_hash": "hash1",
        "prompt_id": "prompt_01",
        "base_prompt_id": "",
        "parent_prompt_id": "",
        "prompt_family": "portfolio",
        "gem_id": "GEM_GENERAL_REVIEW",
        "prompt_profile": "P4",
        "record_type": "PROMPT_VARIANT",
        "status": "ACTIVE",
        "validation_status": "READY",
        "is_reference_locked": False,
        "raw_prompt_text": "Analyse ce portefeuille.",
        "prompt_text_field_used": "prompt_detail",
        "python_simplification_action": "NORMALIZE_AND_PREPARE_VALIDATED_UPSERT",
        "p137_correction_status": "REQUIRED",
        "p133_compatibility_status": "READY_FOR_VALIDATION",
        "target_sheet": "📘 PROMPT_LIBRARY",
        "target_row_strategy": "UPSERT_BY_PROMPT_ID_AFTER_VALIDATION",
        "write_status": "PLANNED_ONLY_NO_WRITE_BEFORE_VALIDATION",
        "human_review_status": "REQUIRED",
        "blockers": [],
    }
    base.update(overrides)
    return base


def _safe_row(**overrides):
    base = {
        "migration_id": "MIG-001",
        "source_hash": "hash1",
        "p138b_write_ready": True,
        "p138c_allowed_after_go": True,
        "protect_locked_reference": False,
        "blockers": [],
        "p138b_decision": "READY_FOR_VARIANT_WRITE_REVIEW",
        "p138b_write_action": "APPEND_OR_UPSERT_VARIANT_AFTER_GO",
        "p138b3_bucket": "SAFE_PARTIAL_WRITE_READY",
    }
    base.update(overrides)
    return base


def test_rehydrate_safe_candidates_merges_candidate_and_safe_scope():
    hydrated = rehydrate_safe_candidates([_safe_row()], [_candidate()])

    assert len(hydrated) == 1
    assert hydrated[0]["prompt_id"] == "prompt_01"
    assert hydrated[0]["p138c_allowed_after_go"] is True


def test_rehydrate_blocks_locked_reference_in_safe_scope():
    with pytest.raises(ValueError, match="locked reference"):
        rehydrate_safe_candidates([_safe_row(protect_locked_reference=True)], [_candidate()])


def test_required_output_headers_preserves_existing_and_adds_traceability():
    headers = required_output_headers(["prompt_id", "prompt_detail"])

    assert headers[:2] == ["prompt_id", "prompt_detail"]
    assert "migration_id" in headers
    assert "source_hash" in headers
    assert "p138c_run_id" in headers
    assert "migration_status" in headers


def test_build_row_maps_raw_prompt_and_p138c_audit_fields():
    headers = required_output_headers(["prompt_id", "prompt_detail"])
    row = build_row_for_headers(
        _candidate(),
        headers,
        run_id="RUN-1",
        written_at_utc="2026-06-23T00:00:00Z",
        explicit_go=EXPLICIT_GO_PHRASE,
    )
    mapping = dict(zip(headers, row, strict=False))

    assert mapping["prompt_id"] == "prompt_01"
    assert mapping["prompt_detail"] == "Analyse ce portefeuille."
    assert mapping["raw_prompt_text"] == "Analyse ce portefeuille."
    assert mapping["p138c_run_id"] == "RUN-1"
    assert mapping["migration_status"] == "MIGRATED_BY_P138C_SAFE_PARTIAL"


def test_write_preflight_pack(tmp_path):
    p138b3 = tmp_path / "p138b3"
    p138a2 = tmp_path / "p138a2"
    out = tmp_path / "out"
    p138b3.mkdir()
    p138a2.mkdir()
    (p138b3 / "P138B3_SAFE_PARTIAL_WRITE_READY.json").write_text(
        json.dumps([_safe_row()]),
        encoding="utf-8",
    )
    (p138a2 / "P138A_MIGRATION_CANDIDATES.json").write_text(
        json.dumps([_candidate()]),
        encoding="utf-8",
    )

    payload = write_preflight_pack(
        P138CRequest(
            p138b3_export_dir=p138b3,
            p138a2_export_dir=p138a2,
            output_dir=out,
            explicit_go=EXPLICIT_GO_PHRASE,
        )
    )

    assert payload["status"] == "P138C_PREFLIGHT_READY"
    assert payload["safe_candidate_count"] == 1
    assert (out / "P138C_PREFLIGHT_PAYLOAD.json").exists()
    assert (out / "P138C_HYDRATED_SAFE_CANDIDATES.csv").exists()
    assert (out / "P138C_RUNBOOK.md").exists()


def test_cli_preflight_only(tmp_path):
    p138b3 = tmp_path / "p138b3"
    p138a2 = tmp_path / "p138a2"
    out = tmp_path / "out"
    p138b3.mkdir()
    p138a2.mkdir()
    (p138b3 / "P138B3_SAFE_PARTIAL_WRITE_READY.json").write_text(
        json.dumps([_safe_row()]),
        encoding="utf-8",
    )
    (p138a2 / "P138A_MIGRATION_CANDIDATES.json").write_text(
        json.dumps([_candidate()]),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p138c_safe_partial_sheets_write",
            "--p138b3-export-dir",
            str(p138b3),
            "--p138a2-export-dir",
            str(p138a2),
            "--output-dir",
            str(out),
            "--explicit-go",
            EXPLICIT_GO_PHRASE,
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "P138C_PREFLIGHT_READY" in completed.stdout
    assert "apply=false" in completed.stdout
    assert "\\ud83d\\udcd8" in completed.stdout
