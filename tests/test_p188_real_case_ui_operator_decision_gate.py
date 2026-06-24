from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_py.p188_real_case_ui_operator_decision_gate import (
    build_real_case_operator_decision_gate,
    export_real_case_operator_decision_gate,
)


def test_decision_gate_waits_without_real_inputs(tmp_path: Path) -> None:
    payload = build_real_case_operator_decision_gate(tmp_path)

    assert payload["decision_status"] == "WAITING_INPUTS"
    assert payload["real_case_ready"] is False
    assert payload["apply_allowed"] is False
    assert payload["human_review_required"] is True
    assert "WAITING_REAL_OPERATOR_CAPTURE" in payload["blockers"]
    assert "WAITING_REAL_GEM_RESPONSE_PASTE" in payload["blockers"]
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_decision_gate_ready_with_real_inputs(tmp_path: Path) -> None:
    capture_dir = tmp_path / "00_OPERATOR_EXPORTS" / "P181_CAPTURE_INBOX"
    response_dir = tmp_path / "00_OPERATOR_EXPORTS" / "P181_GEM_RESPONSES"
    capture_dir.mkdir(parents=True)
    response_dir.mkdir(parents=True)
    (capture_dir / "real_portfolio.png").write_bytes(b"real")
    (response_dir / "real_response.json").write_text(
        json.dumps(
            {
                "status": "REVIEW_REQUIRED",
                "image_usage_evidence": {"status": "IMAGE_USED"},
                "reference_currency": "USD",
                "missing_data": [],
                "blockers": ["NO_AUTO_APPLY"],
                "safety": {"no_order": True, "no_sizing": True},
            }
        ),
        encoding="utf-8",
    )

    payload = build_real_case_operator_decision_gate(tmp_path)

    assert payload["decision_status"] == "READY_FOR_HUMAN_DECISION"
    assert payload["real_case_ready"] is True
    assert payload["blocker_count"] == 0
    assert payload["recommended_next"] == "P189_REAL_CASE_REVIEW_DECISION_CAPTURE"


def test_export_decision_gate_writes_expected_files(tmp_path: Path) -> None:
    export_dir = tmp_path / "05_EXPORTS" / "P188_TEST_EXPORT"

    payload = export_real_case_operator_decision_gate(tmp_path, export_dir=export_dir)

    assert payload["decision_status"] == "WAITING_INPUTS"
    assert (export_dir / "P188_REAL_CASE_OPERATOR_DECISION_GATE.json").exists()
    assert (export_dir / "P188_SUMMARY.json").exists()
    assert (export_dir / "P188_REAL_CASE_OPERATOR_DECISION_GATE_REPORT.md").exists()
