from __future__ import annotations

import json
from pathlib import Path

from mvp_qaic_py.gem_multimodal_response_capture_gate import (
    SAMPLE_GEM_RESPONSE,
    GemMultimodalResponseGateRequest,
    extract_json_text,
    parse_gem_response,
    validate_payload,
    write_response_capture_gate,
)


def _write_response(tmp_path: Path, payload: dict, *, minified: bool = True) -> Path:
    path = tmp_path / "gem_response.json"
    if minified:
        path.write_text(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
        )
    else:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def test_p133_extracts_raw_json_from_minified_response():
    payload, warnings, json_text = parse_gem_response(
        json.dumps(SAMPLE_GEM_RESPONSE, ensure_ascii=False, separators=(",", ":"))
    )
    assert payload["status"] == "REVIEW_REQUIRED"
    assert warnings == []
    assert "\n" not in json_text


def test_p133_extracts_json_from_fenced_block():
    raw = (
        "Résumé\n```json\n"
        + json.dumps(SAMPLE_GEM_RESPONSE, ensure_ascii=False, indent=2)
        + "\n```"
    )
    json_text, warnings = extract_json_text(raw)
    assert json.loads(json_text)["reference_currency"] == "USD"
    assert warnings == []


def test_p133_gate_passes_real_like_gem_response_with_human_review():
    text = json.dumps(SAMPLE_GEM_RESPONSE, ensure_ascii=False, separators=(",", ":"))
    payload, _, json_text = parse_gem_response(text)
    validation = validate_payload(payload, json_text)
    assert validation["gate_status"] == "PASS_WITH_HUMAN_REVIEW"
    assert validation["detected"]["image_used"] is True
    assert validation["detected"]["image_evidence_status"] == "IMAGE_USED"
    assert validation["detected"]["reference_currency"] == "USD"
    assert validation["arithmetic"]["asset_value_sum_usd"] == 655.66
    assert validation["arithmetic"]["value_delta_usd"] == 0.0
    assert validation["arithmetic"]["allocation_sum_pct"] == 100.0
    assert validation["arithmetic"]["pnl_delta_usd"] == 0.0


def test_p133_flags_minified_json_as_advisory_not_blocker():
    text = json.dumps(SAMPLE_GEM_RESPONSE, ensure_ascii=False, separators=(",", ":"))
    payload, _, json_text = parse_gem_response(text)
    validation = validate_payload(payload, json_text)
    assert validation["gate_status"] == "PASS_WITH_HUMAN_REVIEW"
    assert validation["detected"]["minified_json_detected"] is True
    assert "gem_response_json_minified_single_line_operator_unfriendly" in validation["advisory"]


def test_p133_blocks_when_image_not_used():
    payload = dict(SAMPLE_GEM_RESPONSE)
    payload["image_used"] = False
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    parsed, _, json_text = parse_gem_response(text)
    validation = validate_payload(parsed, json_text)
    assert validation["gate_status"] == "BLOCKED"
    assert "image_used_not_true" in validation["failures"]


def test_p133_blocks_when_currency_not_usd():
    payload = dict(SAMPLE_GEM_RESPONSE)
    payload["reference_currency"] = "EUR"
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    parsed, _, json_text = parse_gem_response(text)
    validation = validate_payload(parsed, json_text)
    assert validation["gate_status"] == "BLOCKED"
    assert "reference_currency_not_usd" in validation["failures"]


def test_p133_blocks_when_arithmetic_mismatch():
    payload = json.loads(json.dumps(SAMPLE_GEM_RESPONSE))
    payload["assets"][1]["value_usd"] = 400.00
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    parsed, _, json_text = parse_gem_response(text)
    validation = validate_payload(parsed, json_text)
    assert validation["gate_status"] == "BLOCKED"
    assert "asset_value_sum_mismatch" in validation["failures"]


def test_p133_blocks_translated_top_level_json_keys():
    payload = dict(SAMPLE_GEM_RESPONSE)
    payload["statut"] = payload.pop("status")
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    parsed, _, json_text = parse_gem_response(text)
    validation = validate_payload(parsed, json_text)
    assert validation["gate_status"] == "BLOCKED"
    assert any(item.startswith("translated_json_keys_detected") for item in validation["failures"])


def test_p133_writes_human_readable_report_and_pretty_json(tmp_path):
    response_path = _write_response(tmp_path, SAMPLE_GEM_RESPONSE, minified=True)
    out = tmp_path / "out"

    manifest = write_response_capture_gate(
        GemMultimodalResponseGateRequest(
            response_text_path=response_path,
            output_dir=out,
            run_id="TEST-P133",
            generated_at_utc="2026-06-22T00:00:00Z",
        )
    )

    assert manifest["status"] == "GEM_MULTIMODAL_RESPONSE_CAPTURE_GATE_READY"
    assert manifest["gate_status"] == "PASS_WITH_HUMAN_REVIEW"
    assert manifest["pretty_json_required"] is True
    assert manifest["no_minified_json_for_operator_review"] is True

    pretty = (out / "P133_GEM_RESPONSE_PRETTY.json").read_text(encoding="utf-8")
    assert "\n  " in pretty
    assert '"reference_currency": "USD"' in pretty

    md = (out / "P133_GEM_RESPONSE_HUMAN_REVIEW.md").read_text(encoding="utf-8")
    assert "Rapport lisible" in md
    assert "655.66" in md
    assert "JSON minifié détecté" in md
    assert "NO_AUTO_APPLY_GEM_RESPONSE" in md

    csv_text = (out / "P133_OPERATOR_SUMMARY.csv").read_text(encoding="utf-8")
    assert "gate_status,PASS_WITH_HUMAN_REVIEW" in csv_text


def test_p133_missing_no_auto_apply_root_is_advisory_for_p132_r1_contract():
    text = json.dumps(SAMPLE_GEM_RESPONSE, ensure_ascii=False, indent=2)
    payload, _, json_text = parse_gem_response(text)
    validation = validate_payload(payload, json_text)
    assert validation["gate_status"] == "PASS_WITH_HUMAN_REVIEW"
    assert "no_auto_apply_root_field_missing_future_schema_recommendation" in validation["advisory"]


def test_p133_requires_no_auto_apply_root_true_if_present():
    payload = dict(SAMPLE_GEM_RESPONSE)
    payload["no_auto_apply"] = False
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    parsed, _, json_text = parse_gem_response(text)
    validation = validate_payload(parsed, json_text)
    assert validation["gate_status"] == "BLOCKED"
    assert "no_auto_apply_root_field_not_true" in validation["failures"]


def test_p133_accepts_no_auto_apply_root_true_when_present():
    payload = dict(SAMPLE_GEM_RESPONSE)
    payload["no_auto_apply"] = True
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    parsed, _, json_text = parse_gem_response(text)
    validation = validate_payload(parsed, json_text)
    assert validation["gate_status"] == "PASS_WITH_HUMAN_REVIEW"
    assert (
        "no_auto_apply_root_field_missing_future_schema_recommendation"
        not in validation["advisory"]
    )
