from __future__ import annotations

import json
import subprocess
import sys

from mvp_qaic_py.p138b_validate_migration_candidates import (
    P138BRequest,
    build_validation_payload,
    validate_candidates,
    write_p138b_pack,
)


def _candidate(**overrides):
    base = {
        "migration_id": "MIG-001",
        "prompt_id": "prompt_01",
        "source_tab": "📘 PROMPT_LIBRARY",
        "source_row": 10,
        "source_hash": "abc",
        "gem_id": "GEM_GENERAL_REVIEW",
        "record_type": "PROMPT_VARIANT",
        "target_sheet": "📘 PROMPT_LIBRARY",
        "target_row_strategy": "UPSERT_BY_PROMPT_ID_AFTER_VALIDATION",
        "is_reference_locked": False,
        "blockers": [],
    }
    base.update(overrides)
    return base


def test_p138b_ready_variant_candidate_is_write_ready_after_go():
    decision = validate_candidates([_candidate()])[0]

    assert decision.p138b_decision == "READY_FOR_VARIANT_WRITE_REVIEW"
    assert decision.p138b_write_ready is True
    assert decision.p138c_allowed_after_go is True
    assert decision.protect_locked_reference is False


def test_p138b_blocks_missing_prompt_text_candidate():
    decision = validate_candidates([_candidate(blockers=["PROMPT_TEXT_MISSING"])])[0]

    assert decision.p138b_decision == "BLOCKED_REVIEW"
    assert decision.p138b_write_ready is False
    assert "PROMPT_TEXT_MISSING" in decision.blockers


def test_p138b_protects_locked_reference():
    decision = validate_candidates(
        [
            _candidate(
                record_type="PROMPT_CONTRACT",
                is_reference_locked=True,
                target_row_strategy="CREATE_VARIANT_ROW_DO_NOT_OVERWRITE_REFERENCE",
            )
        ]
    )[0]

    assert decision.p138b_decision == "PROTECT_LOCKED_REFERENCE"
    assert decision.p138b_write_ready is False
    assert decision.protect_locked_reference is True


def test_p138b_duplicate_prompt_id_requires_review_for_canonical_rows():
    candidates = [
        _candidate(
            migration_id="MIG-1",
            prompt_id="prompt_x",
            source_hash="h1",
            record_type="PROMPT_CONTRACT",
        ),
        _candidate(
            migration_id="MIG-2",
            prompt_id="prompt_x",
            source_hash="h2",
            record_type="PROMPT_CONTRACT",
        ),
    ]

    decisions = validate_candidates(candidates)

    assert all(decision.duplicate_prompt_id_count == 2 for decision in decisions)
    assert all(decision.p138b_decision == "REVIEW_DUPLICATE_PROMPT_ID" for decision in decisions)


def test_p138b_payload_summarizes_write_gate(tmp_path):
    source = tmp_path / "candidates.json"
    source.write_text(
        json.dumps([_candidate(), _candidate(blockers=["PROMPT_TEXT_MISSING"])]), encoding="utf-8"
    )

    payload = build_validation_payload(
        P138BRequest(
            candidates_json=source,
            output_dir=tmp_path / "out",
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert payload["status"] == "P138B_VALIDATION_DONE_WRITE_PLAN_READY_FOR_REVIEW"
    assert payload["candidate_count"] == 2
    assert payload["write_ready_count"] == 1
    assert payload["blocked_count"] == 1
    assert payload["p138c_ready_for_write_after_go"] is False
    assert payload["sheets_write_policy"]["p138b_sheets_write"] is False


def test_p138b_writes_expected_export_files(tmp_path):
    source = tmp_path / "candidates.json"
    source.write_text(json.dumps([_candidate()]), encoding="utf-8")
    out = tmp_path / "out"

    payload = write_p138b_pack(
        P138BRequest(
            candidates_json=source,
            output_dir=out,
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert payload["write_ready_count"] == 1
    assert (out / "P138B_VALIDATION_PAYLOAD.json").exists()
    assert (out / "P138B_WRITE_PLAN.csv").exists()
    assert (out / "P138B_BLOCKERS.csv").exists()
    assert (out / "P138B_MIGRATION_DECISION_MATRIX.md").exists()
    assert (out / "P138B_WRITE_GUARD.md").exists()


def test_p138b_cli(tmp_path):
    source = tmp_path / "candidates.json"
    source.write_text(json.dumps([_candidate()]), encoding="utf-8")
    out = tmp_path / "out"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p138b_validate_migration_candidates",
            "--candidates-json",
            str(source),
            "--output-dir",
            str(out),
            "--generated-at-utc",
            "2026-06-22T00:00:00Z",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "P138B_VALIDATION_DONE_WRITE_PLAN_READY_FOR_REVIEW" in completed.stdout
    assert "write_ready_count=1" in completed.stdout
