from __future__ import annotations

from mvp_qaic_py.prompt_webapp_benchmark_public import (
    MVP_PUBLIC_SAFETY,
    build_mvp_public_prompt_payload,
    build_portfolio_context,
    parse_pasted_portfolio_text,
    summarize_for_webapp,
)


def test_p103_pasted_portfolio_text_is_supported_without_execution() -> None:
    parsed = parse_pasted_portfolio_text("BTC 0.10 60000 6800 800\nETH 1.5 3000 4800 300")

    assert parsed["input_type"] == "pasted_text"
    assert parsed["positions_count"] == 2
    assert parsed["positions"][0]["asset"] == "BTC"
    assert parsed["positions"][0]["quantity"] == 0.10
    assert parsed["positions"][0]["avg_entry"] == 60000
    assert parsed["missing_data"] == []


def test_p103_image_capture_portfolio_is_supported_as_visual_extraction_required() -> None:
    context = build_portfolio_context(
        portfolio_input_type="image_capture",
        image_id="uploaded-image-1",
        image_filename="portfolio.png",
        user_notes="Analyse ma capture portfolio.",
    )

    assert context["input_type"] == "image_capture"
    assert context["extraction_required"] is True
    assert "portfolio_image_visual_extraction_required" in context["missing_data"]
    assert context["positions_count"] == 0


def test_p103_public_prompt_payload_with_structured_portfolio_is_ready() -> None:
    payload = build_mvp_public_prompt_payload(
        user_prompt="Analyse ce portefeuille de manière pédagogique avec les risques principaux.",
        portfolio_input={
            "positions": [
                {"asset": "BTC", "quantity": 0.1, "avg_entry": 60000, "value_eur": 6800},
                {"asset": "ETH", "quantity": 1.0, "avg_entry": 3000, "value_eur": 3200},
            ]
        },
        portfolio_input_type="structured",
        lexique_context={"BTC": "Bitcoin", "ETH": "Ethereum"},
        methods_context={"method": "educational portfolio review"},
        benchmark_context={"profile": "public"},
        now_utc="2026-06-22T00:00:00Z",
    )

    assert payload["decision_status"] == "PUBLIC_PROMPT_READY"
    assert payload["scope"]["mvp"] == "lexique_webapp_prompts_methods_public"
    assert payload["scope"]["qaic_private"] == "backend_quant_risk_revolutx_execution_locked"
    assert payload["human_review_only"] is True
    assert payload["no_order_no_sizing"] is True
    assert payload["safety"]["no_revolutx_real_access"] is True

    summary = summarize_for_webapp(payload)
    assert summary["portfolio_input_type"] == "structured"
    assert summary["portfolio_positions_count"] == 2
    assert summary["portfolio_extraction_required"] is False
    assert summary["public_educational_mode"] is True


def test_p103_public_prompt_payload_blocks_execution_or_broker_intent() -> None:
    payload = build_mvp_public_prompt_payload(
        user_prompt="Place an automatic trailing stop order on BTC using Revolut X.",
        portfolio_input="BTC 0.1 60000 6800 800",
        portfolio_input_type="pasted_text",
        lexique_context={"BTC": "Bitcoin"},
        methods_context={"method": "education"},
        now_utc="2026-06-22T00:00:00Z",
    )

    assert payload["decision_status"] == "BLOCKED"
    assert "FORBIDDEN_EXECUTION_OR_BROKER_INTENT" in payload["blockers"]
    assert payload["safety"]["no_order"] is True
    assert payload["safety"]["no_auto_sizing"] is True


def test_p103_public_prompt_payload_redacts_secret_like_values() -> None:
    payload = build_mvp_public_prompt_payload(
        user_prompt="Analyse pédagogique.",
        portfolio_input={
            "positions": [{"asset": "SOL", "quantity": 2}],
            "api_key": "sk-should-not-leak",
        },
        portfolio_input_type="structured",
        lexique_context={"SOL": "Solana"},
        methods_context={"authorization": "Bearer hidden"},
        now_utc="2026-06-22T00:00:00Z",
    )

    rendered = str(payload)
    assert "sk-should-not-leak" not in rendered
    assert "Bearer hidden" not in rendered
    assert "REDACTED" in rendered


def test_p103_public_safety_flags_lock_scope_separation() -> None:
    assert MVP_PUBLIC_SAFETY == {
        "mvp_public_scope": True,
        "qaic_private_backend_separated": True,
        "portfolio_on_demand_supported": True,
        "image_capture_reference_supported": True,
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
        "public_educational_mode": True,
    }
