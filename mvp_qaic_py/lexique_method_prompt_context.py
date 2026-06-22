from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from mvp_qaic_py.webapp_prompt_benchmark_pack import (
    build_webapp_prompt_benchmark_pack,
)


CONTEXT_SAFETY: dict[str, bool] = {
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


def _norm(value: Any) -> str:
    return str(value or "").strip()


def _lower(value: Any) -> str:
    return _norm(value).lower()


def normalize_lexique_items(items: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, item in enumerate(items or [], start=1):
        if not isinstance(item, dict):
            continue

        term = _norm(item.get("term") or item.get("asset") or item.get("keyword"))
        if not term:
            continue

        aliases = item.get("aliases") or item.get("alias") or []
        if isinstance(aliases, str):
            aliases = [
                part.strip() for part in aliases.replace("|", ",").split(",") if part.strip()
            ]
        if not isinstance(aliases, list):
            aliases = []

        rows.append(
            {
                "id": _norm(item.get("id") or f"lexique_{index:04d}"),
                "term": term,
                "category": _norm(item.get("category") or "GENERAL"),
                "definition": _norm(item.get("definition") or item.get("description")),
                "aliases": [str(alias).strip() for alias in aliases if str(alias).strip()],
                "public_safe": item.get("public_safe", True) is not False,
                "source": _norm(item.get("source") or "local_context"),
            }
        )

    return rows


def normalize_method_items(items: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, item in enumerate(items or [], start=1):
        if not isinstance(item, dict):
            continue

        method_id = _norm(item.get("method_id") or item.get("id") or f"method_{index:04d}")
        title = _norm(item.get("title") or item.get("name") or method_id)
        if not title:
            continue

        tags = item.get("tags") or []
        if isinstance(tags, str):
            tags = [part.strip() for part in tags.replace("|", ",").split(",") if part.strip()]
        if not isinstance(tags, list):
            tags = []

        rows.append(
            {
                "method_id": method_id,
                "title": title,
                "summary": _norm(item.get("summary") or item.get("description")),
                "tags": [str(tag).strip() for tag in tags if str(tag).strip()],
                "risk_notes": _norm(item.get("risk_notes") or item.get("limits")),
                "public_safe": item.get("public_safe", True) is not False,
            }
        )

    return rows


def match_lexique_context(
    *,
    user_prompt: str,
    portfolio_assets: list[str] | None,
    lexique_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    prompt_lower = _lower(user_prompt)
    asset_set = {_lower(asset) for asset in portfolio_assets or [] if _norm(asset)}

    matched: list[dict[str, Any]] = []
    for item in lexique_items:
        terms = [_lower(item.get("term"))]
        terms.extend(_lower(alias) for alias in item.get("aliases", []))
        found = False
        for term in terms:
            if term and (term in prompt_lower or term in asset_set):
                found = True
                break
        if found and item.get("public_safe", True):
            matched.append(item)

    return matched


def match_method_context(
    *,
    user_prompt: str,
    method_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    prompt_lower = _lower(user_prompt)
    matched: list[dict[str, Any]] = []

    for item in method_items:
        terms = [_lower(item.get("title")), _lower(item.get("method_id"))]
        terms.extend(_lower(tag) for tag in item.get("tags", []))
        if any(term and term in prompt_lower for term in terms) and item.get("public_safe", True):
            matched.append(item)

    if not matched:
        matched = [item for item in method_items if item.get("public_safe", True)][:3]

    return matched


def extract_portfolio_assets_from_context(portfolio_context: dict[str, Any] | None) -> list[str]:
    assets: list[str] = []
    for row in (portfolio_context or {}).get("positions", []):
        if not isinstance(row, dict):
            continue
        asset = _norm(row.get("asset"))
        if asset:
            assets.append(asset.upper())
    return sorted(set(assets))


def build_context_cards(
    *,
    lexique_context: list[dict[str, Any]],
    method_context: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    lexique_cards = [
        {
            "card_id": f"lexique::{item['id']}",
            "title": item["term"],
            "subtitle": item["category"],
            "body": item["definition"],
            "source": item["source"],
        }
        for item in lexique_context
    ]

    method_cards = [
        {
            "card_id": f"method::{item['method_id']}",
            "title": item["title"],
            "subtitle": ", ".join(item.get("tags", [])),
            "body": item.get("summary", ""),
            "risk_notes": item.get("risk_notes", ""),
        }
        for item in method_context
    ]

    return {"lexique_cards": lexique_cards, "method_cards": method_cards}


def build_lexique_method_prompt_context_pack(
    *,
    prompt_payload: dict[str, Any],
    lexique_items: list[dict[str, Any]] | None = None,
    method_items: list[dict[str, Any]] | None = None,
    now_utc: str | None = None,
) -> dict[str, Any]:
    request = prompt_payload.get("prompt_request", {})
    user_prompt = request.get("user_prompt", "") if isinstance(request, dict) else ""
    portfolio_context = request.get("portfolio_context", {}) if isinstance(request, dict) else {}
    portfolio_assets = extract_portfolio_assets_from_context(portfolio_context)

    normalized_lexique = normalize_lexique_items(lexique_items)
    normalized_methods = normalize_method_items(method_items)

    matched_lexique = match_lexique_context(
        user_prompt=user_prompt,
        portfolio_assets=portfolio_assets,
        lexique_items=normalized_lexique,
    )
    matched_methods = match_method_context(
        user_prompt=user_prompt,
        method_items=normalized_methods,
    )
    cards = build_context_cards(
        lexique_context=matched_lexique,
        method_context=matched_methods,
    )

    webapp_pack = build_webapp_prompt_benchmark_pack(
        lexique_items=matched_lexique,
        method_items=matched_methods,
        now_utc=now_utc,
    )

    missing_context: list[str] = []
    if not matched_lexique:
        missing_context.append("matched_lexique_context")
    if not matched_methods:
        missing_context.append("matched_method_context")

    return {
        "runtime": "MVP_QAIC_LEXIQUE_METHOD_PROMPT_CONTEXT_WEBAPP",
        "version": "P105_LEXIQUE_METHOD_PROMPT_CONTEXT_WEBAPP_0_1_0",
        "created_at_utc": _now_iso(now_utc),
        "scope": {
            "mvp": "lexique_webapp_prompts_methods_benchmark_public",
            "qaic_private": "backend_quant_risk_revolutx_execution_locked",
        },
        "safety": dict(CONTEXT_SAFETY),
        "prompt_decision_status": prompt_payload.get("decision_status"),
        "portfolio_assets": portfolio_assets,
        "matched_lexique_count": len(matched_lexique),
        "matched_method_count": len(matched_methods),
        "missing_context": missing_context,
        "context_cards": cards,
        "webapp_pack_summary": {
            "route_count": len(webapp_pack.get("ui_schema", {}).get("routes", [])),
            "section_count": len(webapp_pack.get("ui_schema", {}).get("sections", [])),
            "prompt_template_count": len(webapp_pack.get("prompt_templates", [])),
        },
    }


def build_default_demo_lexique() -> list[dict[str, Any]]:
    return normalize_lexique_items(
        [
            {
                "term": "BTC",
                "category": "ASSET",
                "definition": "Bitcoin, crypto-actif de référence. Analyse publique uniquement dans le MVP.",
                "aliases": ["Bitcoin"],
            },
            {
                "term": "ETH",
                "category": "ASSET",
                "definition": "Ethereum, réseau smart contracts et actif crypto.",
                "aliases": ["Ethereum"],
            },
            {
                "term": "PnL",
                "category": "PORTFOLIO",
                "definition": "Profit and Loss. Ne jamais l'inventer si absent du portfolio fourni.",
                "aliases": ["profit", "perte"],
            },
        ]
    )


def build_default_demo_methods() -> list[dict[str, Any]]:
    return normalize_method_items(
        [
            {
                "method_id": "portfolio_educational_review",
                "title": "Portfolio educational review",
                "summary": "Revue pédagogique des expositions, concentrations, risques et données manquantes.",
                "tags": ["portfolio", "risk", "education"],
                "risk_notes": "Aucun conseil financier personnalisé ni exécution.",
            },
            {
                "method_id": "prompt_quality_benchmark",
                "title": "Prompt quality benchmark",
                "summary": "Score clarté, complétude, sécurité et utilité pédagogique.",
                "tags": ["benchmark", "prompt", "quality"],
            },
        ]
    )
