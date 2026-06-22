import json

from mvp_qaic_py.gem_prompt_runner_pack import (
    SAFETY_MARKERS,
    build_expected_gem_output_schema,
    build_gem_prompt_runner_pack,
    export_gem_prompt_runner_pack,
)


def test_p114_image_review_pack_requires_human_confirmation():
    payload = build_gem_prompt_runner_pack(
        input_mode="IMAGE_REVIEW_REQUIRED",
        image_reference="portfolio_capture.png",
        notes="Capture reference only.",
        run_id="P114-TEST",
        generated_at_utc="2026-06-22T00:00:00Z",
    )

    assert payload["status"] == "REVIEW_REQUIRED"
    assert payload["human_review_only"] is True
    assert payload["no_order_no_sizing"] is True
    assert payload["no_ocr_claim"] is True
    assert "NO_OCR_CLAIM" in payload["safety_markers"]
    assert "NO_IMAGE_VISUAL_EXTRACTION_WITHOUT_HUMAN" in payload["safety_markers"]
    assert "NO_REVOLUTX_REAL_ACCESS" in payload["safety_markers"]

    normalized = payload["normalized_portfolio_input"]
    assert normalized["human_review_required"] is True
    assert "human_confirmed_asset_symbols" in normalized["missing_data"]
    assert "human_confirmed_quantities" in normalized["missing_data"]
    assert "human_confirmed_values" in normalized["missing_data"]

    prompt = payload["gem_prompt_markdown"]
    assert "Do not claim OCR" in prompt
    assert "Do not invent assets" in prompt
    assert "NO_BROKER" in prompt or "NO_ORDER" in prompt


def test_p114_pasted_text_draft_keeps_review_required_and_no_sizing():
    payload = build_gem_prompt_runner_pack(
        input_mode="PASTED_TEXT_DRAFT",
        pasted_text="BTC 0.10 value EUR 6500; ETH 1.2 value EUR 4200",
        run_id="P114-PASTED",
        generated_at_utc="2026-06-22T00:00:00Z",
    )

    assert payload["status"] == "REVIEW_REQUIRED"
    assert payload["input"]["pasted_text"].startswith("BTC")
    assert payload["no_order_no_sizing"] is True
    assert "NO_AUTO_SIZING" in payload["safety_markers"]
    assert payload["normalized_portfolio_input"]["human_review_required"] is True


def test_p114_expected_schema_has_hard_safety_fields():
    schema = build_expected_gem_output_schema()

    required = set(schema["required"])
    assert "decision_status" in required
    assert "missing_data" in required
    assert "blockers" in required
    assert "human_decision_only" in required
    assert "no_order_no_sizing" in required
    assert schema["properties"]["human_decision_only"]["const"] is True
    assert schema["properties"]["no_order_no_sizing"]["const"] is True


def test_p114_export_pack_writes_copy_paste_json_contract(tmp_path):
    result = export_gem_prompt_runner_pack(
        tmp_path,
        input_mode="IMAGE_REVIEW_REQUIRED",
        image_reference="capture.png",
        run_id="P114-EXPORT",
        generated_at_utc="2026-06-22T00:00:00Z",
    )

    assert result["status"] == "EXPORTED"

    expected_files = {
        "P114_GEM_RUNNER_PAYLOAD_SAMPLE.json",
        "P114_GEM_PROMPT_COPY_PASTE.md",
        "P114_EXPECTED_GEM_OUTPUT_SCHEMA.json",
        "P114_RUNNER_REPORT.md",
        "P114_RUNNER_CONTRACT.json",
    }
    assert expected_files == {path.name for path in tmp_path.iterdir()}

    payload = json.loads(
        (tmp_path / "P114_GEM_RUNNER_PAYLOAD_SAMPLE.json").read_text(encoding="utf-8")
    )
    contract = json.loads((tmp_path / "P114_RUNNER_CONTRACT.json").read_text(encoding="utf-8"))
    prompt = (tmp_path / "P114_GEM_PROMPT_COPY_PASTE.md").read_text(encoding="utf-8")

    assert payload["run_id"] == "P114-EXPORT"
    assert payload["human_review_only"] is True
    assert payload["no_revolutx_real_access"] is True
    assert "broker_execution" in contract["forbidden"]
    assert "order_execution" in contract["forbidden"]
    assert "auto_sizing" in contract["forbidden"]
    assert "Expected output JSON schema" in prompt


def test_p114_safety_marker_contract_is_complete():
    required_markers = {
        "MVP_PUBLIC_SCOPE",
        "HUMAN_REVIEW_ONLY",
        "NO_OCR_CLAIM",
        "NO_IMAGE_VISUAL_EXTRACTION_WITHOUT_HUMAN",
        "NO_INVENTED_POSITION",
        "NO_INVENTED_PRICE",
        "NO_INVENTED_VALUE",
        "NO_REVOLUTX_REAL_ACCESS",
        "NO_BROKER",
        "NO_ORDER",
        "NO_CANCEL",
        "NO_REPLACE_ORDER",
        "NO_AUTO_SIZING",
        "NO_SECRET_LOG",
        "NO_SHEET_WRITE",
        "NO_APPS_SCRIPT_EXECUTION",
        "NO_CLASP",
        "NO_PUBLIC_DEPLOY",
    }

    assert required_markers.issubset(set(SAFETY_MARKERS))
