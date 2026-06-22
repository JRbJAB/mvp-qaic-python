import json
import subprocess
import sys

import pytest

from mvp_qaic_py.gem_response_decision_journal_bridge import (
    SAFETY_MARKERS,
    DecisionJournalBridgeRequest,
    build_bridge_contract,
    build_decision_journal_entry,
    load_response_capture,
    write_decision_journal_bridge_pack,
)


def _sample_capture(**overrides):
    payload = {
        "step": "P119_GEM_RESPONSE_CAPTURE_REVIEW_QUEUE",
        "version": "test",
        "decision_status": "REVIEW_REQUIRED",
        "status": "REVIEW_REQUIRED",
        "source_prompt_run_id": "P118-SAMPLE",
        "response_run_id": "P119-SAMPLE",
        "generated_at_utc": "2026-06-22T00:00:00Z",
        "missing_data": ["human_confirmed_asset_symbols", "current_prices"],
        "blockers": [],
        "review_queue_rows": [{"queue_id": "MISSING-001"}, {"queue_id": "MISSING-002"}],
        "structured_response": {"summary": "Need manual confirmation."},
    }
    payload.update(overrides)
    return payload


def test_p120_builds_review_required_journal_entry_from_p119_capture():
    entry = build_decision_journal_entry(
        _sample_capture(),
        journal_entry_id="P120-TEST",
        generated_at_utc="2026-06-22T00:00:00Z",
        notes="unit test",
    )

    assert entry["journal_status"] == "REVIEW_REQUIRED"
    assert entry["decision_status"] == "REVIEW_REQUIRED"
    assert entry["missing_data_count"] == 2
    assert entry["blocker_count"] == 0
    assert entry["review_queue_rows"] == 2
    assert entry["human_review_only"] is True
    assert entry["no_sheet_write"] is True
    assert "human_confirmed_asset_symbols" in entry["missing_data"]


def test_p120_builds_blocked_journal_entry_when_capture_has_blockers():
    entry = build_decision_journal_entry(
        _sample_capture(decision_status="BLOCKED", blockers=["FORBIDDEN_ACTION_TERM:place order"]),
        journal_entry_id="P120-BLOCKED",
    )

    assert entry["journal_status"] == "BLOCKED"
    assert entry["decision_status"] == "BLOCKED"
    assert entry["blocker_count"] == 1
    assert "Resolve blockers" in entry["required_human_action"]


def test_p120_write_bridge_pack_exports_json_csv_contract_manifest_report(tmp_path):
    capture_path = tmp_path / "P119_RESPONSE_CAPTURE.json"
    capture_path.write_text(json.dumps(_sample_capture()), encoding="utf-8")

    result = write_decision_journal_bridge_pack(
        DecisionJournalBridgeRequest(
            output_dir=tmp_path / "out",
            response_capture_json_file=capture_path,
            journal_entry_id="P120-EXPORT",
        )
    )

    out = tmp_path / "out"
    assert result["status"] == "EXPORTED"
    assert result["journal_status"] == "REVIEW_REQUIRED"
    assert (out / "P120_DECISION_JOURNAL_ENTRY.json").exists()
    assert (out / "P120_DECISION_JOURNAL_ENTRY.csv").exists()
    assert (out / "P120_SOURCE_CAPTURE_SNAPSHOT.json").exists()
    assert (out / "P120_BRIDGE_CONTRACT.json").exists()
    assert (out / "P120_BRIDGE_MANIFEST.json").exists()
    assert (out / "P120_BRIDGE_REPORT.md").exists()

    csv_text = (out / "P120_DECISION_JOURNAL_ENTRY.csv").read_text(encoding="utf-8-sig")
    assert "P120-EXPORT" in csv_text
    assert "human_confirmed_asset_symbols" in csv_text


def test_p120_rejects_non_p119_capture(tmp_path):
    capture_path = tmp_path / "bad.json"
    capture_path.write_text(json.dumps({"step": "OTHER"}), encoding="utf-8")

    with pytest.raises(ValueError, match="not a P119 response capture"):
        load_response_capture(capture_path)


def test_p120_contract_forbids_live_actions():
    contract = build_bridge_contract()
    forbidden = set(contract["forbidden"])

    assert "auto_apply_gem_response" in forbidden
    assert "apps_script_execution" in forbidden
    assert "sheet_write" in forbidden
    assert "clasp_push" in forbidden
    assert "broker_execution" in forbidden
    assert "order_execution" in forbidden
    assert "auto_sizing" in forbidden


def test_p120_cli_generates_bridge_pack(tmp_path):
    capture_path = tmp_path / "capture.json"
    capture_path.write_text(json.dumps(_sample_capture()), encoding="utf-8")
    output_dir = tmp_path / "bridge"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.gem_response_decision_journal_bridge",
            "--output-dir",
            str(output_dir),
            "--response-capture-json-file",
            str(capture_path),
            "--journal-entry-id",
            "P120-CLI",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "EXPORTED" in completed.stdout
    assert (output_dir / "P120_DECISION_JOURNAL_ENTRY.json").exists()


def test_p120_safety_markers_are_explicit():
    required = {
        "MVP_PUBLIC_SCOPE",
        "HUMAN_REVIEW_ONLY",
        "LOCAL_ONLY",
        "DECISION_JOURNAL_BRIDGE_LOCAL_ONLY",
        "NO_AUTO_APPLY_GEM_RESPONSE",
        "NO_INDEX_EDIT",
        "NO_CLASP",
        "NO_APPS_SCRIPT_EXECUTION",
        "NO_SHEET_WRITE",
        "NO_PUBLIC_DEPLOY",
        "NO_BROKER",
        "NO_ORDER",
        "NO_AUTO_SIZING",
        "NO_REVOLUTX_REAL_ACCESS_FROM_MVP",
    }

    assert required.issubset(set(SAFETY_MARKERS))
