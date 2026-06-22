import json
import subprocess
import sys

import pytest

from mvp_qaic_py.gem_response_review_queue import (
    SAFETY_MARKERS,
    GemResponseCaptureRequest,
    build_capture_contract,
    build_response_capture,
    detect_forbidden_action_blockers,
    write_response_review_pack,
)


def test_p119_captures_structured_raw_json_and_missing_data(tmp_path):
    response = {
        "decision_status": "REVIEW_REQUIRED",
        "missing_data": ["human_confirmed_asset_symbols", "current_prices"],
        "blockers": [],
        "summary": "Need confirmation.",
    }

    result = write_response_review_pack(
        GemResponseCaptureRequest(
            output_dir=tmp_path,
            raw_response=json.dumps(response),
            source_prompt_run_id="P118-SAMPLE",
            response_run_id="P119-TEST",
        )
    )

    assert result["status"] == "EXPORTED"
    assert result["decision_status"] == "REVIEW_REQUIRED"
    assert result["missing_data_count"] == 2
    assert result["queue_rows"] == 2

    queue = (tmp_path / "P119_REVIEW_QUEUE.csv").read_text(encoding="utf-8-sig")
    assert "human_confirmed_asset_symbols" in queue
    assert "current_prices" in queue


def test_p119_captures_json_from_text_file_with_bom_and_code_fence(tmp_path):
    response_file = tmp_path / "response.txt"
    response_file.write_text(
        '\ufeff```json\n{"decision_status":"REVIEW_REQUIRED","missing_data":["portfolio_total_value_eur"],"blockers":[]}\n```\n',
        encoding="utf-8",
    )

    result = write_response_review_pack(
        GemResponseCaptureRequest(
            output_dir=tmp_path / "out",
            response_text_file=str(response_file),
            response_run_id="P119-FENCE",
        )
    )

    queue = (tmp_path / "out" / "P119_REVIEW_QUEUE.csv").read_text(encoding="utf-8-sig")
    assert result["missing_data_count"] == 1
    assert "portfolio_total_value_eur" in queue


def test_p119_blocks_forbidden_order_language(tmp_path):
    raw = "The answer says: place an order and use auto sizing after TP1."

    capture = build_response_capture(
        GemResponseCaptureRequest(
            output_dir=tmp_path,
            raw_response=raw,
            response_run_id="P119-BLOCK",
        )
    )

    assert capture["decision_status"] == "BLOCKED"
    assert capture["blockers"]
    assert any("place an order" in blocker for blocker in capture["blockers"])
    assert any(row["review_status"] == "BLOCKED" for row in capture["review_queue_rows"])


def test_p119_rejects_multiple_input_sources(tmp_path):
    response_file = tmp_path / "response.txt"
    response_file.write_text("hello", encoding="utf-8")

    with pytest.raises(ValueError, match="Use only one GEM response input source"):
        build_response_capture(
            GemResponseCaptureRequest(
                output_dir=tmp_path,
                raw_response="hello",
                response_text_file=str(response_file),
            )
        )


def test_p119_forbidden_action_detector_terms():
    blockers = detect_forbidden_action_blockers(
        "execute order then cancel order with broker execution"
    )
    assert "FORBIDDEN_ACTION_TERM:execute order" in blockers
    assert "FORBIDDEN_ACTION_TERM:cancel order" in blockers
    assert "FORBIDDEN_ACTION_TERM:broker execution" in blockers


def test_p119_contract_forbids_live_actions():
    contract = build_capture_contract()
    forbidden = set(contract["forbidden"])

    assert "auto_apply_gem_response" in forbidden
    assert "apps_script_execution" in forbidden
    assert "sheet_write" in forbidden
    assert "clasp_push" in forbidden
    assert "broker_execution" in forbidden
    assert "order_execution" in forbidden
    assert "auto_sizing" in forbidden


def test_p119_cli_generates_review_pack(tmp_path):
    output_dir = tmp_path / "capture"
    response = json.dumps(
        {"decision_status": "REVIEW_REQUIRED", "missing_data": ["prices"], "blockers": []}
    )

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mvp_qaic_py.gem_response_review_queue",
            "--output-dir",
            str(output_dir),
            "--raw-response",
            response,
            "--source-prompt-run-id",
            "P118-CLI",
            "--response-run-id",
            "P119-CLI",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "EXPORTED" in completed.stdout
    assert (output_dir / "P119_REVIEW_QUEUE.csv").exists()


def test_p119_safety_markers_are_explicit():
    required = {
        "MVP_PUBLIC_SCOPE",
        "HUMAN_REVIEW_ONLY",
        "LOCAL_ONLY",
        "GEM_RESPONSE_CAPTURE_ONLY",
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
