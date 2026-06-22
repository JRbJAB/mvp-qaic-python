from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from mvp_qaic_py.prompt_webapp_benchmark_public import (
    MVP_PUBLIC_SAFETY,
    build_mvp_public_prompt_payload,
    summarize_for_webapp,
)


WEBAPP_SAFETY: dict[str, bool] = {
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


def _now_iso(now_utc: str | None = None) -> str:
    if now_utc:
        return now_utc
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_prompt_templates() -> list[dict[str, Any]]:
    return [
        {
            "template_id": "portfolio_public_review",
            "title": "Analyse portefeuille pédagogique",
            "input_modes": ["pasted_text", "structured", "image_capture"],
            "safety": "human_review_only_no_order_no_sizing",
            "prompt": (
                "Analyse ce portefeuille de manière pédagogique. Identifie les risques, "
                "les données manquantes, les concentrations et les points à vérifier. "
                "N'invente aucun prix, TP, SL, PnL ou sizing."
            ),
        },
        {
            "template_id": "asset_method_review",
            "title": "Analyse méthode + actif",
            "input_modes": ["none", "pasted_text", "structured", "image_capture"],
            "safety": "education_only",
            "prompt": (
                "Explique la méthode applicable à cet actif, les limites, les signaux "
                "à vérifier et les erreurs fréquentes."
            ),
        },
        {
            "template_id": "prompt_quality_benchmark",
            "title": "Benchmark qualité prompt",
            "input_modes": ["none", "pasted_text", "structured", "image_capture"],
            "safety": "public_safe_benchmark",
            "prompt": (
                "Évalue la qualité du prompt selon clarté, données manquantes, risque "
                "d'hallucination, sécurité publique et exploitabilité pédagogique."
            ),
        },
    ]


def default_ui_schema() -> dict[str, Any]:
    return {
        "app_id": "mvp_qaic_public_prompt_webapp",
        "sections": [
            {
                "section_id": "prompt_input",
                "title": "Prompt",
                "component": "textarea",
                "required": True,
            },
            {
                "section_id": "portfolio_input",
                "title": "Portfolio optionnel",
                "component": "tabs",
                "modes": [
                    {
                        "mode": "none",
                        "label": "Aucun portfolio",
                        "component": "empty_state",
                    },
                    {
                        "mode": "pasted_text",
                        "label": "Copier-coller",
                        "component": "textarea",
                    },
                    {
                        "mode": "structured",
                        "label": "JSON structuré",
                        "component": "json_editor",
                    },
                    {
                        "mode": "image_capture",
                        "label": "Capture image",
                        "component": "image_upload_reference",
                        "requires_visual_extraction": True,
                    },
                ],
            },
            {
                "section_id": "lexique_context",
                "title": "Lexique",
                "component": "context_cards",
            },
            {
                "section_id": "method_context",
                "title": "Méthodes",
                "component": "context_cards",
            },
            {
                "section_id": "benchmark_scores",
                "title": "Benchmark",
                "component": "score_cards",
            },
            {
                "section_id": "missing_data",
                "title": "Données manquantes",
                "component": "checklist",
            },
            {
                "section_id": "blockers",
                "title": "Blocages sécurité",
                "component": "alert_list",
            },
            {
                "section_id": "human_review_output",
                "title": "Sortie revue humaine",
                "component": "markdown_panel",
            },
        ],
        "routes": [
            {"path": "/", "view": "home"},
            {"path": "/prompts", "view": "prompt_library"},
            {"path": "/benchmark", "view": "benchmark"},
            {"path": "/lexique", "view": "lexique"},
            {"path": "/methodes", "view": "methods"},
            {"path": "/portfolio-review", "view": "portfolio_prompt_review"},
        ],
    }


def build_sample_payloads(now_utc: str | None = None) -> list[dict[str, Any]]:
    samples = [
        build_mvp_public_prompt_payload(
            user_prompt="Analyse ce portefeuille de manière pédagogique avec les risques principaux.",
            portfolio_input="BTC 0.10 60000 6800 800\nETH 1.0 3000 3200 200",
            portfolio_input_type="pasted_text",
            lexique_context={"BTC": "Bitcoin", "ETH": "Ethereum"},
            methods_context={"method": "portfolio educational review"},
            benchmark_context={"profile": "public"},
            now_utc=now_utc,
        ),
        build_mvp_public_prompt_payload(
            user_prompt="Analyse ma capture de portefeuille sans inventer les données cachées.",
            portfolio_input_type="image_capture",
            image_id="sample-image-ref",
            image_filename="portfolio_capture.png",
            lexique_context={"portfolio": "allocation crypto"},
            methods_context={"method": "visual portfolio extraction"},
            benchmark_context={"profile": "image"},
            now_utc=now_utc,
        ),
        build_mvp_public_prompt_payload(
            user_prompt="Place an automatic order on BTC.",
            portfolio_input="BTC 0.10 60000 6800 800",
            portfolio_input_type="pasted_text",
            lexique_context={"BTC": "Bitcoin"},
            methods_context={"method": "safety test"},
            benchmark_context={"profile": "blocker"},
            now_utc=now_utc,
        ),
    ]

    return samples


def build_webapp_prompt_benchmark_pack(
    *,
    lexique_items: list[dict[str, Any]] | None = None,
    method_items: list[dict[str, Any]] | None = None,
    prompt_templates: list[dict[str, Any]] | None = None,
    now_utc: str | None = None,
) -> dict[str, Any]:
    samples = build_sample_payloads(now_utc=now_utc)
    summaries = [summarize_for_webapp(sample) for sample in samples]

    return {
        "runtime": "MVP_QAIC_WEBAPP_UI_PROMPT_BENCHMARK_DATA_PACK",
        "version": "P104_WEBAPP_UI_PROMPT_BENCHMARK_DATA_PACK_0_1_0",
        "created_at_utc": _now_iso(now_utc),
        "scope": {
            "mvp": "lexique_webapp_prompts_methods_benchmark_public",
            "qaic_private": "backend_quant_risk_revolutx_execution_locked",
        },
        "safety": dict(WEBAPP_SAFETY),
        "inherits_p103_safety": dict(MVP_PUBLIC_SAFETY),
        "ui_schema": default_ui_schema(),
        "prompt_templates": prompt_templates or default_prompt_templates(),
        "lexique_items": lexique_items or [],
        "method_items": method_items or [],
        "sample_payloads": samples,
        "sample_summaries": summaries,
        "benchmark_cards": [
            {
                "card_id": "quality_score",
                "label": "Qualité prompt",
                "source": "benchmark.quality_score",
            },
            {
                "card_id": "public_safety_score",
                "label": "Sécurité publique",
                "source": "benchmark.public_safety_score",
            },
            {
                "card_id": "data_completeness_score",
                "label": "Complétude données",
                "source": "benchmark.data_completeness_score",
            },
            {
                "card_id": "public_usefulness_score",
                "label": "Utilité pédagogique",
                "source": "benchmark.public_usefulness_score",
            },
        ],
        "api_contract": {
            "input": {
                "user_prompt": "string",
                "portfolio_input_type": "none|pasted_text|structured|image_capture",
                "portfolio_input": "optional text/json",
                "image_id": "optional",
                "image_filename": "optional",
                "lexique_context": "optional object",
                "methods_context": "optional object",
            },
            "output": {
                "decision_status": "PUBLIC_PROMPT_READY|REVIEW_REQUIRED|BLOCKED",
                "missing_data": "list[string]",
                "blockers": "list[string]",
                "benchmark": "object",
                "webapp_ui": "object",
            },
        },
    }


def summarize_pack(pack: dict[str, Any]) -> dict[str, Any]:
    ui_schema = pack.get("ui_schema", {})
    return {
        "runtime": pack.get("runtime"),
        "version": pack.get("version"),
        "route_count": len(ui_schema.get("routes", [])),
        "section_count": len(ui_schema.get("sections", [])),
        "template_count": len(pack.get("prompt_templates", [])),
        "sample_count": len(pack.get("sample_payloads", [])),
        "benchmark_card_count": len(pack.get("benchmark_cards", [])),
        "no_revolutx_real_access": pack.get("safety", {}).get("no_revolutx_real_access") is True,
        "no_order_no_sizing": (
            pack.get("safety", {}).get("no_order") is True
            and pack.get("safety", {}).get("no_auto_sizing") is True
        ),
    }
