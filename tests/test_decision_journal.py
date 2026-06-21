from __future__ import annotations

import json

from qaic_core.decision_journal import (
    DECISION_JOURNAL_SAFETY_MARKERS,
    build_decision_journal_entry,
    decision_journal_entry_to_dict,
    journal_write_result_to_dict,
    summarize_decision_journal,
    write_decision_journal_jsonl,
)
from qaic_core.decision_journal.journal import validate_decision_journal_entry


def complete_runtime_record() -> dict[str, object]:
    return {
        "signal_id": "SIG-BTC-001",
        "asset": "BTC",
        "decision_status": "REVIEW_REQUIRED",
        "human_decision_only": True,
        "no_order_no_sizing": True,
        "risk_guard": "HUMAN_REVIEW_ONLY,NO_BROKER,NO_ORDER,NO_SIZING",
        "missing_data": [],
        "blockers": [],
    }


def test_build_decision_journal_entry_from_runtime_record() -> None:
    entry = build_decision_journal_entry(
        complete_runtime_record(),
        run_id="RUN-001",
        timestamp="2026-06-21T00:00:00+00:00",
    )
    payload = decision_journal_entry_to_dict(entry)

    assert payload["journal_version"] == "mvp_qaic.decision_journal_python.v1"
    assert payload["run_id"] == "RUN-001"
    assert payload["signal_id"] == "SIG-BTC-001"
    assert payload["asset"] == "BTC"
    assert payload["decision_status"] == "REVIEW_REQUIRED"
    assert payload["human_decision_only"] is True
    assert payload["no_order_no_sizing"] is True


def test_decision_journal_entry_validates_against_migration_contract() -> None:
    entry = build_decision_journal_entry(
        complete_runtime_record(),
        run_id="RUN-VALID",
        timestamp="2026-06-21T00:00:00+00:00",
    )
    validation = validate_decision_journal_entry(entry)

    assert validation["contract_id"] == "decision_journal.v1"
    assert validation["status"] == "PASS"
    assert validation["blockers"] == []


def test_missing_signal_id_requires_review_in_contract_validation() -> None:
    record = complete_runtime_record()
    record["signal_id"] = ""

    entry = build_decision_journal_entry(
        record,
        run_id="RUN-MISSING",
        timestamp="2026-06-21T00:00:00+00:00",
    )
    validation = validate_decision_journal_entry(entry)

    assert validation["status"] == "REVIEW_REQUIRED"
    assert "signal_id" in validation["empty_fields"]
    assert "EMPTY_REQUIRED_FIELDS" in validation["blockers"]


def test_blocked_decision_preserves_blockers_and_missing_data() -> None:
    record = complete_runtime_record()
    record["decision_status"] = "BLOCKED"
    record["missing_data"] = ["current_price"]
    record["blockers"] = ["MISSING_CRITICAL_DATA"]

    entry = build_decision_journal_entry(
        record,
        run_id="RUN-BLOCKED",
        timestamp="2026-06-21T00:00:00+00:00",
        notes=["human review required"],
    )
    payload = decision_journal_entry_to_dict(entry)

    assert payload["decision_status"] == "BLOCKED"
    assert payload["missing_data"] == ["current_price"]
    assert payload["blockers"] == ["MISSING_CRITICAL_DATA"]
    assert payload["notes"] == ["human review required"]


def test_summarize_decision_journal_counts_statuses() -> None:
    first = build_decision_journal_entry(
        complete_runtime_record(),
        run_id="RUN-1",
        timestamp="2026-06-21T00:00:00+00:00",
    )
    second_record = complete_runtime_record()
    second_record["asset"] = "ETH"
    second_record["decision_status"] = "BLOCKED"
    second = build_decision_journal_entry(
        second_record,
        run_id="RUN-2",
        timestamp="2026-06-21T00:01:00+00:00",
    )

    summary = summarize_decision_journal([first, second])

    assert summary["entry_count"] == 2
    assert summary["blocked_count"] == 1
    assert summary["review_required_count"] == 1
    assert summary["asset_count"] == 2
    assert summary["assets"] == ["BTC", "ETH"]
    assert summary["human_decision_only"] is True
    assert summary["no_order_no_sizing"] is True


def test_write_decision_journal_jsonl_requires_explicit_tmp_path(tmp_path) -> None:
    entry = build_decision_journal_entry(
        complete_runtime_record(),
        run_id="RUN-WRITE",
        timestamp="2026-06-21T00:00:00+00:00",
    )

    result = write_decision_journal_jsonl(
        entries=[entry],
        journal_dir=tmp_path,
        file_name="journal.jsonl",
    )
    payload = journal_write_result_to_dict(result)

    assert payload["wrote_file"] is True
    assert payload["line_count"] == 1
    assert payload["validation_status"] == "PASS"
    assert isinstance(payload["sha256"], str)
    assert len(payload["sha256"]) == 64

    lines = (tmp_path / "journal.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    loaded = json.loads(lines[0])
    assert loaded["entry"]["run_id"] == "RUN-WRITE"
    assert loaded["validation"]["status"] == "PASS"


def test_write_decision_journal_jsonl_reports_review_required_for_invalid_entry(
    tmp_path,
) -> None:
    record = complete_runtime_record()
    record["signal_id"] = ""
    entry = build_decision_journal_entry(
        record,
        run_id="RUN-BAD",
        timestamp="2026-06-21T00:00:00+00:00",
    )

    result = write_decision_journal_jsonl(
        entries=[entry],
        journal_dir=tmp_path,
    )
    payload = journal_write_result_to_dict(result)

    assert payload["validation_status"] == "REVIEW_REQUIRED"
    loaded = json.loads((tmp_path / "decision_journal.jsonl").read_text(encoding="utf-8"))
    assert loaded["validation"]["status"] == "REVIEW_REQUIRED"


def test_decision_journal_safety_markers_are_explicit() -> None:
    assert DECISION_JOURNAL_SAFETY_MARKERS == (
        "LOCAL_DECISION_JOURNAL_ONLY",
        "HUMAN_REVIEW_ONLY",
        "NO_GOOGLE_LIVE_WRITE",
        "NO_SHEET_WRITE",
        "NO_BROKER",
        "NO_ORDER",
        "NO_SIZING",
        "NO_SECRET",
        "EXPLICIT_PATH_REQUIRED_FOR_WRITE",
    )
