from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_py.p184_real_gem_session_review_response_parser import (
    build_real_gem_session_review,
    export_real_gem_session_review,
    parse_gem_response_text,
)


def test_parse_gem_response_text_full_json_validates_safety() -> None:
    text = json.dumps(
        {
            "status": "REVIEW_REQUIRED",
            "image_usage_evidence": {"status": "IMAGE_USED"},
            "reference_currency": "USD",
            "missing_data": [],
            "blockers": ["NO_AUTO_APPLY"],
            "safety": {
                "no_order": True,
                "no_sizing": True,
                "auto_apply_gem_response": False,
            },
        }
    )

    payload = parse_gem_response_text(text, source_name="sample.json")

    assert payload["json_found"] is True
    assert payload["extraction_mode"] == "FULL_JSON"
    assert payload["has_review_required"] is True
    assert payload["has_image_used"] is True
    assert payload["has_no_order"] is True
    assert payload["has_no_sizing"] is True
    assert payload["has_auto_apply_block"] is True
    assert payload["has_reference_currency"] is True
    assert payload["human_review_required"] is True
    assert payload["apply_allowed"] is False
    assert payload["gem_call_executed"] is False
    assert payload["broker"] is False
    assert payload["order"] is False
    assert payload["sizing"] is False


def test_build_real_gem_session_review_waiting_when_no_response(tmp_path: Path) -> None:
    payload = build_real_gem_session_review(tmp_path)

    assert payload["STATUS"] == "OK_P184_REAL_GEM_SESSION_REVIEW_RESPONSE_PARSER_READY"
    assert payload["parser_ready"] is True
    assert payload["parsed_response_count"] == 0
    assert payload["review_status"] == "WAITING_REAL_GEM_RESPONSE"
    assert payload["gem_call_executed"] is False


def test_export_real_gem_session_review_parses_local_response(tmp_path: Path) -> None:
    response_dir = tmp_path / "00_OPERATOR_EXPORTS" / "P181_GEM_RESPONSES"
    response_dir.mkdir(parents=True)
    (response_dir / "desktop.ini").write_text("ignore", encoding="utf-8")
    (response_dir / "gem_response.json").write_text(
        json.dumps(
            {
                "status": "REVIEW_REQUIRED",
                "image_used": True,
                "image_usage_evidence": {"status": "IMAGE_USED"},
                "reference_currency": "USD",
                "missing_data": [],
                "blockers": ["NO_AUTO_APPLY"],
                "no_order": True,
                "no_sizing": True,
            }
        ),
        encoding="utf-8",
    )
    export_dir = tmp_path / "05_EXPORTS" / "P184_TEST_EXPORT"

    payload = export_real_gem_session_review(tmp_path, export_dir=export_dir)

    assert payload["parser_ready"] is True
    assert payload["parsed_response_count"] == 1
    assert payload["parsed_responses"][0]["source_name"] == "gem_response.json"
    assert (export_dir / "P184_REAL_GEM_SESSION_REVIEW.json").exists()
    assert (export_dir / "P184_SUMMARY.json").exists()
    assert (export_dir / "P184_PARSED_RESPONSES.csv").exists()
    assert (export_dir / "P184_REAL_GEM_SESSION_REVIEW_REPORT.md").exists()
