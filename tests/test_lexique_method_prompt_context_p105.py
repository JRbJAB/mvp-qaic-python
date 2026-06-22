from __future__ import annotations

from mvp_qaic_py.lexique_method_prompt_context import (
    CONTEXT_SAFETY,
    build_context_cards,
    build_default_demo_lexique,
    build_default_demo_methods,
    build_lexique_method_prompt_context_pack,
    extract_portfolio_assets_from_context,
    match_lexique_context,
    match_method_context,
    normalize_lexique_items,
    normalize_method_items,
)
from mvp_qaic_py.prompt_webapp_benchmark_public import build_mvp_public_prompt_payload


def test_p105_normalizes_lexique_and_methods() -> None:
    lexique = normalize_lexique_items(
        [{"term": "BTC", "category": "ASSET", "definition": "Bitcoin", "aliases": "Bitcoin|XBT"}]
    )
    methods = normalize_method_items(
        [{"method_id": "risk_review", "title": "Risk review", "tags": "risk|portfolio"}]
    )

    assert lexique[0]["term"] == "BTC"
    assert lexique[0]["aliases"] == ["Bitcoin", "XBT"]
    assert methods[0]["tags"] == ["risk", "portfolio"]


def test_p105_matches_lexique_from_prompt_and_portfolio_assets() -> None:
    lexique = build_default_demo_lexique()
    matched = match_lexique_context(
        user_prompt="Analyse Bitcoin et le PnL.",
        portfolio_assets=["ETH"],
        lexique_items=lexique,
    )
    terms = {item["term"] for item in matched}

    assert {"BTC", "ETH", "PnL"} <= terms


def test_p105_matches_methods_with_default_fallback() -> None:
    methods = build_default_demo_methods()
    matched = match_method_context(user_prompt="Analyse mon portefeuille.", method_items=methods)

    assert matched
    assert matched[0]["public_safe"] is True


def test_p105_context_cards_are_webapp_ready() -> None:
    cards = build_context_cards(
        lexique_context=build_default_demo_lexique()[:1],
        method_context=build_default_demo_methods()[:1],
    )

    assert cards["lexique_cards"][0]["card_id"].startswith("lexique::")
    assert cards["method_cards"][0]["card_id"].startswith("method::")


def test_p105_builds_context_pack_from_p103_prompt_payload() -> None:
    prompt_payload = build_mvp_public_prompt_payload(
        user_prompt="Analyse BTC avec une méthode portfolio educational review.",
        portfolio_input="BTC 0.10 60000 6800 800",
        portfolio_input_type="pasted_text",
        lexique_context={"BTC": "Bitcoin"},
        methods_context={"method": "portfolio educational review"},
        now_utc="2026-06-22T00:00:00Z",
    )

    pack = build_lexique_method_prompt_context_pack(
        prompt_payload=prompt_payload,
        lexique_items=build_default_demo_lexique(),
        method_items=build_default_demo_methods(),
        now_utc="2026-06-22T00:00:00Z",
    )

    assert pack["scope"]["mvp"] == "lexique_webapp_prompts_methods_benchmark_public"
    assert pack["scope"]["qaic_private"] == "backend_quant_risk_revolutx_execution_locked"
    assert pack["portfolio_assets"] == ["BTC"]
    assert pack["matched_lexique_count"] >= 1
    assert pack["matched_method_count"] >= 1
    assert pack["context_cards"]["lexique_cards"]
    assert pack["context_cards"]["method_cards"]
    assert pack["safety"]["no_revolutx_real_access"] is True


def test_p105_extract_portfolio_assets_and_safety_flags() -> None:
    assets = extract_portfolio_assets_from_context(
        {"positions": [{"asset": "BTC"}, {"asset": "ETH"}, {"asset": "BTC"}]}
    )

    assert assets == ["BTC", "ETH"]
    assert CONTEXT_SAFETY == {
        "mvp_public_scope": True,
        "qaic_private_backend_separated": True,
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
