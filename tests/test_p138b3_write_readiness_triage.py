from __future__ import annotations

import json
import subprocess
import sys

from mvp_qaic_py.p138b3_write_readiness_triage import (
    P138B3Request,
    build_triage_payload,
    triage_rows,
    write_p138b3_pack,
)


def _row(**overrides):
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
        "p138b_decision": "READY_FOR_VARIANT_WRITE_REVIEW",
        "p138b_write_action": "APPEND_OR_UPSERT_VARIANT_AFTER_GO",
        "p138b_write_ready": True,
        "p138c_allowed_after_go": True,
        "protect_locked_reference": False,
        "duplicate_prompt_id_count": 1,
        "duplicate_source_hash_count": 1,
        "blockers": [],
        "review_notes": "",
    }
    base.update(overrides)
    return base


def _write_p138b_export(base_dir, rows):
    base_dir.mkdir(parents=True, exist_ok=True)
    (base_dir / "P138B_VALIDATION_PAYLOAD.json").write_text(
        json.dumps({"status": "P138B_VALIDATION_DONE_WRITE_PLAN_READY_FOR_REVIEW"}),
        encoding="utf-8",
    )
    (base_dir / "P138B_WRITE_PLAN.json").write_text(json.dumps(rows), encoding="utf-8")


def test_p138b3_triage_buckets_safe_ready_blocked_duplicate_reference():
    buckets = triage_rows(
        [
            _row(),
            _row(p138b_decision="BLOCKED_REVIEW", blockers=["PROMPT_TEXT_MISSING"]),
            _row(p138b_decision="REVIEW_DUPLICATE_PROMPT_ID", p138b_write_ready=False),
            _row(
                p138b_decision="PROTECT_LOCKED_REFERENCE",
                p138b_write_ready=False,
                protect_locked_reference=True,
            ),
        ]
    )

    assert len(buckets["safe_partial_write_ready"]) == 1
    assert len(buckets["blocked_review"]) == 1
    assert len(buckets["duplicate_review"]) == 1
    assert len(buckets["protected_references"]) == 1


def test_p138b3_payload_recommends_safe_partial_scope(tmp_path):
    export_dir = tmp_path / "p138b"
    _write_p138b_export(
        export_dir,
        [
            _row(),
            _row(p138b_decision="BLOCKED_REVIEW", blockers=["PROMPT_TEXT_MISSING"]),
        ],
    )

    payload = build_triage_payload(
        P138B3Request(
            p138b_export_dir=export_dir,
            output_dir=tmp_path / "out",
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert payload["status"] == "P138B3_TRIAGE_DONE_SAFE_PARTIAL_SCOPE_READY"
    assert payload["safe_partial_write_ready_count"] == 1
    assert payload["blocked_review_count"] == 1
    assert payload["p138c_safe_partial_scope_ready"] is True
    assert payload["p138c_full_scope_ready"] is False
    assert payload["sheets_write_policy"]["p138b3_sheets_write"] is False


def test_p138b3_payload_review_required_when_no_safe_rows(tmp_path):
    export_dir = tmp_path / "p138b"
    _write_p138b_export(export_dir, [_row(p138b_decision="BLOCKED_REVIEW", blockers=["X"])])

    payload = build_triage_payload(
        P138B3Request(
            p138b_export_dir=export_dir,
            output_dir=tmp_path / "out",
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert payload["status"] == "P138B3_TRIAGE_DONE_REVIEW_REQUIRED_BEFORE_WRITE"
    assert payload["p138c_safe_partial_scope_ready"] is False


def test_p138b3_writes_expected_export_files(tmp_path):
    export_dir = tmp_path / "p138b"
    _write_p138b_export(export_dir, [_row()])

    out = tmp_path / "out"
    payload = write_p138b3_pack(
        P138B3Request(
            p138b_export_dir=export_dir,
            output_dir=out,
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert payload["safe_partial_write_ready_count"] == 1
    assert (out / "P138B3_TRIAGE_PAYLOAD.json").exists()
    assert (out / "P138B3_SAFE_PARTIAL_WRITE_READY.csv").exists()
    assert (out / "P138B3_BLOCKED_REVIEW.csv").exists()
    assert (out / "P138B3_DUPLICATE_REVIEW.csv").exists()
    assert (out / "P138B3_PROTECTED_REFERENCES.csv").exists()
    assert (out / "P138B3_P138C_WRITE_SCOPE.md").exists()
    assert (out / "P138B3_P138C_PREWRITE_CHECKLIST.md").exists()


def test_p138b3_cli(tmp_path):
    export_dir = tmp_path / "p138b"
    _write_p138b_export(export_dir, [_row()])
    out = tmp_path / "out"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.p138b3_write_readiness_triage",
            "--p138b-export-dir",
            str(export_dir),
            "--output-dir",
            str(out),
            "--generated-at-utc",
            "2026-06-22T00:00:00Z",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "P138B3_TRIAGE_DONE_SAFE_PARTIAL_SCOPE_READY" in completed.stdout
    assert "safe_partial_write_ready_count=1" in completed.stdout
