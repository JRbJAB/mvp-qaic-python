from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_py.p187_real_manual_portfolio_case_review_gate import (
    build_manual_portfolio_case_review_gate,
    export_manual_portfolio_case_review_gate,
)


def test_manual_case_gate_waits_when_only_smoke_files_exist(tmp_path: Path) -> None:
    capture_dir = tmp_path / "00_OPERATOR_EXPORTS" / "P181_CAPTURE_INBOX"
    response_dir = tmp_path / "00_OPERATOR_EXPORTS" / "P181_GEM_RESPONSES"
    capture_dir.mkdir(parents=True)
    response_dir.mkdir(parents=True)
    (capture_dir / "P186_SMOKE_PORTFOLIO_CAPTURE.png").write_bytes(b"smoke")
    (response_dir / "P186_SMOKE_GEM_RESPONSE.json").write_text("{}", encoding="utf-8")

    payload = build_manual_portfolio_case_review_gate(tmp_path)

    assert payload["real_case_ready"] is False
    assert payload["capture_count"] == 0
    assert payload["response_count"] == 0
    assert "WAITING_REAL_OPERATOR_CAPTURE" in payload["blockers"]
    assert "WAITING_REAL_GEM_RESPONSE_PASTE" in payload["blockers"]
    assert payload["auto_apply_gem_response"] is False


def test_manual_case_gate_ready_with_real_capture_and_response(tmp_path: Path) -> None:
    capture_dir = tmp_path / "00_OPERATOR_EXPORTS" / "P181_CAPTURE_INBOX"
    response_dir = tmp_path / "00_OPERATOR_EXPORTS" / "P181_GEM_RESPONSES"
    capture_dir.mkdir(parents=True)
    response_dir.mkdir(parents=True)
    (capture_dir / "real_portfolio.png").write_bytes(b"real")
    (response_dir / "real_gem_response.json").write_text(
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

    payload = build_manual_portfolio_case_review_gate(tmp_path)

    assert payload["STATUS"] == "OK_P187_REAL_MANUAL_PORTFOLIO_CASE_READY_FOR_HUMAN_REVIEW"
    assert payload["real_case_ready"] is True
    assert payload["human_review_required"] is True
    assert payload["apply_allowed"] is False
    assert payload["blocker_count"] == 0
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_export_manual_case_gate_writes_expected_files(tmp_path: Path) -> None:
    export_dir = tmp_path / "05_EXPORTS" / "P187_TEST_EXPORT"

    payload = export_manual_portfolio_case_review_gate(tmp_path, export_dir=export_dir)

    assert payload["real_case_ready"] is False
    assert (export_dir / "P187_REAL_MANUAL_CASE_GATE.json").exists()
    assert (export_dir / "P187_SUMMARY.json").exists()
    assert (export_dir / "P187_REAL_MANUAL_CASE_GATE_REPORT.md").exists()
