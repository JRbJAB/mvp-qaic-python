from __future__ import annotations

from mvp_qaic_py.webapp_prompt_benchmark_pack import (
    WEBAPP_SAFETY,
    build_sample_payloads,
    build_webapp_prompt_benchmark_pack,
    default_prompt_templates,
    default_ui_schema,
    summarize_pack,
)


def test_p104_ui_schema_contains_required_public_sections() -> None:
    schema = default_ui_schema()
    section_ids = {section["section_id"] for section in schema["sections"]}
    routes = {route["path"] for route in schema["routes"]}

    assert "prompt_input" in section_ids
    assert "portfolio_input" in section_ids
    assert "benchmark_scores" in section_ids
    assert "human_review_output" in section_ids
    assert "/portfolio-review" in routes


def test_p104_prompt_templates_cover_portfolio_and_benchmark() -> None:
    templates = default_prompt_templates()
    template_ids = {template["template_id"] for template in templates}

    assert "portfolio_public_review" in template_ids
    assert "prompt_quality_benchmark" in template_ids
    assert all("safety" in template for template in templates)


def test_p104_sample_payloads_include_ready_review_and_blocked_cases() -> None:
    samples = build_sample_payloads(now_utc="2026-06-22T00:00:00Z")
    statuses = {sample["decision_status"] for sample in samples}

    assert "PUBLIC_PROMPT_READY" in statuses
    assert "REVIEW_REQUIRED" in statuses
    assert "BLOCKED" in statuses


def test_p104_webapp_pack_is_public_safe_and_complete() -> None:
    pack = build_webapp_prompt_benchmark_pack(now_utc="2026-06-22T00:00:00Z")
    summary = summarize_pack(pack)

    assert pack["scope"]["mvp"] == "lexique_webapp_prompts_methods_benchmark_public"
    assert pack["scope"]["qaic_private"] == "backend_quant_risk_revolutx_execution_locked"
    assert summary["route_count"] >= 5
    assert summary["section_count"] >= 8
    assert summary["template_count"] >= 3
    assert summary["sample_count"] == 3
    assert summary["benchmark_card_count"] == 4
    assert summary["no_revolutx_real_access"] is True
    assert summary["no_order_no_sizing"] is True


def test_p104_webapp_safety_flags_locked() -> None:
    assert WEBAPP_SAFETY == {
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
