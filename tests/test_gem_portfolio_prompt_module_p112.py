from __future__ import annotations

from mvp_qaic_py.gem_portfolio_prompt_module import (
    GEM_PORTFOLIO_PROMPT_SAFETY,
    build_gem_prompt_payload,
    normalize_portfolio_input,
    render_gem_ready_prompt,
    summarize_gem_prompt_payload,
)


def test_p112_none_mode_requires_portfolio_input() -> None:
    portfolio = normalize_portfolio_input()

    assert portfolio["portfolio_input_mode"] == "NONE"
    assert "portfolio_input" in portfolio["missing_data"]
    assert portfolio["human_review_required"] is True
    assert portfolio["ocr_performed"] is False


def test_p112_pasted_text_mode() -> None:
    portfolio = normalize_portfolio_input(pasted_text="BTC 0.1 ETH 2 SOL 10")

    assert portfolio["portfolio_input_mode"] == "PASTED_TEXT"
    assert portfolio["pasted_text"] == "BTC 0.1 ETH 2 SOL 10"


def test_p112_structured_positions_mode_normalizes_symbols() -> None:
    portfolio = normalize_portfolio_input(
        structured_positions=[
            {"symbol": "btc", "quantity": 0.1, "avg_price": 60000, "value": 6800},
            {"symbol": " eth ", "quantity": 2, "avg_price": 3000, "value": 7000},
        ]
    )

    assert portfolio["portfolio_input_mode"] == "STRUCTURED"
    assert [item["symbol"] for item in portfolio["structured_positions"]] == ["BTC", "ETH"]


def test_p112_image_mode_never_claims_ocr() -> None:
    portfolio = normalize_portfolio_input(image_reference="portfolio_capture_001.png")

    assert portfolio["portfolio_input_mode"] == "IMAGE_REVIEW_REQUIRED"
    assert portfolio["ocr_performed"] is False
    assert "portfolio_image_visual_extraction" in portfolio["missing_data"]


def test_p112_payload_is_human_review_only_and_gem_ready() -> None:
    portfolio = normalize_portfolio_input(pasted_text="BTC 0.1 ETH 2 SOL 10")
    payload = build_gem_prompt_payload(
        user_goal="Review my portfolio",
        portfolio_input=portfolio,
        risk_profile="balanced",
        now_utc="2026-06-22T00:00:00Z",
    )
    summary = summarize_gem_prompt_payload(payload)

    assert payload["human_decision_only"] is True
    assert payload["no_order_no_sizing"] is True
    assert summary["prompt_id"] == "P112_GEM_PORTFOLIO_PROMPT_USUAL_MODULE"
    assert payload["safety"]["no_broker"] is True


def test_p112_render_prompt_contains_forbidden_execution_contract() -> None:
    portfolio = normalize_portfolio_input(image_reference="screen.png")
    payload = build_gem_prompt_payload(
        user_goal="Review image portfolio",
        portfolio_input=portfolio,
        risk_profile="balanced",
        now_utc="2026-06-22T00:00:00Z",
    )
    prompt = render_gem_ready_prompt(payload)

    assert "GEM Portfolio Review Prompt" in prompt
    assert "Do not place, prepare, size, replace, cancel, or automate any order" in prompt
    assert "IMAGE_REVIEW_REQUIRED" in prompt
    assert "do not claim OCR" in prompt


def test_p112_safety_flags_locked() -> None:
    assert GEM_PORTFOLIO_PROMPT_SAFETY == {
        "mvp_public_scope": True,
        "qaic_private_backend_separated": True,
        "human_review_only": True,
        "gem_ready_prompt_only": True,
        "no_ocr_claim": True,
        "no_image_visual_extraction_without_human": True,
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
