from __future__ import annotations

from mvp_qaic_py.portfolio_input_normalizer import (
    PORTFOLIO_INPUT_NORMALIZER_SAFETY,
    build_image_review_checklist,
    detect_numeric_tokens,
    detect_symbols_from_text,
    normalize_portfolio_input_workflow,
    normalize_structured_positions,
    parse_pasted_text_draft_positions,
    render_portfolio_review_markdown,
)


def test_p113_detect_symbols_from_text_known_assets() -> None:
    symbols = detect_symbols_from_text("BTC 0.1 ETH 2 SOL 10 total value 15000")

    assert symbols == ["BTC", "ETH", "SOL"]


def test_p113_detect_numeric_tokens_without_assigning_meaning() -> None:
    tokens = detect_numeric_tokens("BTC 0.1 value 6800 +5.5%")

    assert tokens == ["0.1", "6800", "+5.5%"]


def test_p113_parse_pasted_text_keeps_draft_review_required() -> None:
    rows = parse_pasted_text_draft_positions("BTC 0.1 6800\nETH 2 7000")

    assert len(rows) == 2
    assert rows[0]["symbols_detected"] == ["BTC"]
    assert rows[0]["review_required"] is True
    assert rows[0]["confidence"] == "DRAFT_REVIEW_REQUIRED"


def test_p113_structured_positions_normalize_symbols() -> None:
    positions = normalize_structured_positions(
        [{"symbol": " btc ", "quantity": 0.1}, {"symbol": "", "quantity": 2}]
    )

    assert positions[0]["symbol"] == "BTC"
    assert positions[0]["review_required"] is False
    assert positions[1]["review_required"] is True
    assert positions[1]["missing_fields"] == ["symbol"]


def test_p113_image_workflow_requires_human_review_and_no_ocr() -> None:
    workflow = normalize_portfolio_input_workflow(image_reference="screen.png")

    assert workflow["portfolio_input_mode"] == "IMAGE_REVIEW_REQUIRED"
    assert workflow["ocr_performed"] is False
    assert workflow["human_review_required"] is True
    assert "portfolio_image_visual_extraction" in workflow["missing_data"]
    assert workflow["image_review_checklist"]


def test_p113_pasted_text_workflow_is_gem_prompt_ready_but_review_required() -> None:
    workflow = normalize_portfolio_input_workflow(
        pasted_text="BTC 0.1 6800\nETH 2 7000",
        user_goal="Prepare GEM prompt",
        now_utc="2026-06-22T00:00:00Z",
    )

    assert workflow["portfolio_input_mode"] == "PASTED_TEXT_DRAFT"
    assert workflow["asset_candidates"] == ["BTC", "ETH"]
    assert workflow["gem_prompt_ready"] is True
    assert workflow["human_decision_only"] is True


def test_p113_markdown_contains_safety_contract() -> None:
    workflow = normalize_portfolio_input_workflow(image_reference="screen.png")
    markdown = render_portfolio_review_markdown(workflow)

    assert "P113" in markdown
    assert "NO_OCR_CLAIM" in markdown
    assert "NO_INVENTED_POSITION" in markdown
    assert "NO_ORDER" in markdown


def test_p113_image_checklist_blocks_inference() -> None:
    checklist = build_image_review_checklist("screen.png")

    assert any("Do not infer hidden rows" in item for item in checklist)
    assert any("Do not generate an order" in item for item in checklist)


def test_p113_safety_flags_locked() -> None:
    assert PORTFOLIO_INPUT_NORMALIZER_SAFETY == {
        "mvp_public_scope": True,
        "qaic_private_backend_separated": True,
        "human_review_only": True,
        "portfolio_input_normalizer_only": True,
        "image_review_workflow_only": True,
        "no_ocr_claim": True,
        "no_image_visual_extraction_without_human": True,
        "no_invented_position": True,
        "no_invented_price": True,
        "no_invented_value": True,
        "no_revolutx_real_access": True,
        "no_broker": True,
        "no_order": True,
        "no_cancel": True,
        "no_replace_order": True,
        "no_auto_sizing": True,
        "no_secret_log": True,
        "no_sheet_write": True,
        "no_apps_script_execution": True,
        "no_clasp": True,
        "no_public_deploy": True,
    }
