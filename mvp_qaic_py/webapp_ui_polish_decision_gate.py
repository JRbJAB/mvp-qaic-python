from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from mvp_qaic_py.webapp_canonical_binding_admin import (
    build_admin_status,
    build_canonical_binding_contract,
)


UI_POLISH_DECISION_SAFETY: dict[str, bool] = {
    "mvp_public_scope": True,
    "qaic_private_backend_separated": True,
    "canonical_webapp_index_do_not_overwrite": True,
    "ui_polish_decision_gate_only": True,
    "public_deploy_blocked_until_explicit_approval": True,
    "no_index_html_edit": True,
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


def bounded_index_candidate_names() -> tuple[str, ...]:
    return (
        "Index.html",
        "MVPQAIC_Index.html",
        "index.html",
        "source/Index.html",
        "source/MVPQAIC_Index.html",
        "webapp/Index.html",
        "apps_script/Index.html",
        "03_DEV/APPS_SCRIPT_MIRROR/Index.html",
    )


def detect_canonical_index_candidates(repo_root: str | Path) -> list[dict[str, Any]]:
    root = Path(repo_root)
    candidates: list[dict[str, Any]] = []

    for relative_name in bounded_index_candidate_names():
        path = root / relative_name
        if path.exists() and path.is_file():
            candidates.append(
                {
                    "relative_path": relative_name.replace("\\", "/"),
                    "exists": True,
                    "size_bytes": path.stat().st_size,
                    "role": "possible_canonical_index",
                    "allowed_to_edit": False,
                }
            )

    return candidates


def build_ui_polish_requirements() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "ui_shell_preserve_canonical_index",
            "priority": "P0",
            "description": "Preserve validated WebApp Index.html. Python must not overwrite it.",
        },
        {
            "requirement_id": "bind_data_packs",
            "priority": "P0",
            "description": "Bind generated webapp_pack, context_pack, prompt_payload, benchmark and admin status to the existing UI shell.",
        },
        {
            "requirement_id": "portfolio_input_modes_visible",
            "priority": "P1",
            "description": "Expose portfolio modes: none, pasted_text, structured, image_capture.",
        },
        {
            "requirement_id": "benchmark_cards_visible",
            "priority": "P1",
            "description": "Expose quality, public safety, data completeness and public usefulness scores.",
        },
        {
            "requirement_id": "missing_data_and_blockers_visible",
            "priority": "P1",
            "description": "Expose missing_data and blockers clearly before any human review output.",
        },
        {
            "requirement_id": "admin_monitor_internal_only",
            "priority": "P1",
            "description": "Keep ADMIN_MONITOR.html as internal local admin/suivi, not public UI shell.",
        },
        {
            "requirement_id": "public_deploy_explicit_gate",
            "priority": "P0",
            "description": "Public deploy remains blocked until explicit human approval.",
        },
    ]


def build_ui_polish_decision_pack(
    *,
    repo_root: str | Path,
    now_utc: str | None = None,
) -> dict[str, Any]:
    binding_contract = build_canonical_binding_contract(now_utc=now_utc)
    admin_status = build_admin_status(now_utc=now_utc)
    candidates = detect_canonical_index_candidates(repo_root)
    requirements = build_ui_polish_requirements()

    blockers: list[str] = []
    reviews: list[str] = []

    if not binding_contract["safety"]["canonical_webapp_index_do_not_overwrite"]:
        blockers.append("CANONICAL_INDEX_OVERWRITE_POLICY_MISSING")

    if not binding_contract["safety"]["no_public_deploy"]:
        blockers.append("PUBLIC_DEPLOY_NOT_BLOCKED")

    if not candidates:
        reviews.append("CANONICAL_INDEX_CANDIDATE_NOT_FOUND_IN_REPO_LOCAL_SCAN")

    decision_status = (
        "BLOCKED"
        if blockers
        else "REVIEW_REQUIRED"
        if reviews
        else "UI_POLISH_READY_FOR_HUMAN_REVIEW"
    )

    return {
        "runtime": "MVP_QAIC_UI_POLISH_CANONICAL_INDEX_DECISION_GATE",
        "version": "P108_UI_POLISH_CANONICAL_INDEX_DECISION_GATE_0_1_0",
        "created_at_utc": _now_iso(now_utc),
        "decision_status": decision_status,
        "scope": {
            "mvp": "lexique_webapp_prompts_methods_benchmark_public",
            "qaic_private": "backend_quant_risk_revolutx_execution_locked",
        },
        "canonical_ui_policy": binding_contract["canonical_ui"],
        "canonical_index_candidates": candidates,
        "requirements": requirements,
        "admin_status": {
            "status": admin_status["status"],
            "routes_count": admin_status["routes_count"],
            "sections_count": admin_status["sections_count"],
            "decision_status": admin_status["decision_status"],
        },
        "blockers": blockers,
        "reviews": reviews,
        "allowed_next_actions": [
            "HUMAN_REVIEW_CANONICAL_INDEX",
            "PREPARE_UI_POLISH_PATCH_PLAN_ONLY",
            "BIND_JSON_DATA_PACKS_TO_CANONICAL_UI_AFTER_APPROVAL",
        ],
        "forbidden_next_actions": [
            "OVERWRITE_INDEX_HTML",
            "GENERATE_NEW_PUBLIC_INDEX_HTML",
            "CLASP_PUSH",
            "APPS_SCRIPT_EXECUTION",
            "PUBLIC_DEPLOY_WITHOUT_APPROVAL",
            "BROKER_OR_TRADING_EXECUTION",
        ],
        "safety": dict(UI_POLISH_DECISION_SAFETY),
        "next": "P109_CANONICAL_INDEX_READONLY_AUDIT_OR_UI_POLISH_PATCH_PLAN",
    }


def render_ui_polish_requirements_markdown(pack: dict[str, Any]) -> str:
    reqs = "\n".join(
        f"- **{item['priority']} — {item['requirement_id']}**: {item['description']}"
        for item in pack["requirements"]
    )
    candidates = (
        "\n".join(
            f"- `{item['relative_path']}` ({item['size_bytes']} bytes)"
            for item in pack["canonical_index_candidates"]
        )
        or "- `REVIEW_REQUIRED`: no local candidate found in bounded scan."
    )

    return f"""# MVP QAIC — P108 UI Polish Decision Gate

## Decision status

`{pack["decision_status"]}`

## Canonical UI policy

- File: `{pack["canonical_ui_policy"]["file_name"]}`
- Policy: `{pack["canonical_ui_policy"]["policy"]}`
- Python role: `{pack["canonical_ui_policy"]["python_role"]}`

## Canonical index candidates

{candidates}

## UI polish requirements

{reqs}

## Allowed next actions

{chr(10).join(f"- `{item}`" for item in pack["allowed_next_actions"])}

## Forbidden next actions

{chr(10).join(f"- `{item}`" for item in pack["forbidden_next_actions"])}

## Safety

- NO_INDEX_HTML_EDIT
- NO_REVOLUTX_REAL_ACCESS
- NO_BROKER
- NO_ORDER
- NO_AUTO_SIZING
- NO_SHEET_WRITE
- NO_APPS_SCRIPT_EXECUTION
- NO_CLASP
- NO_PUBLIC_DEPLOY
"""


def summarize_ui_polish_decision(pack: dict[str, Any]) -> dict[str, Any]:
    return {
        "decision_status": pack["decision_status"],
        "candidate_count": len(pack["canonical_index_candidates"]),
        "requirement_count": len(pack["requirements"]),
        "blocker_count": len(pack["blockers"]),
        "review_count": len(pack["reviews"]),
        "no_index_html_edit": pack["safety"]["no_index_html_edit"],
        "no_public_deploy": pack["safety"]["no_public_deploy"],
        "next": pack["next"],
    }
