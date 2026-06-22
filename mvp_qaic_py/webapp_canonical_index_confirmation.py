from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


CANONICAL_INDEX_CONFIRMATION_SAFETY: dict[str, bool] = {
    "mvp_public_scope": True,
    "qaic_private_backend_separated": True,
    "human_confirmation_required": True,
    "patch_plan_only": True,
    "no_index_html_edit": True,
    "no_index_html_generation": True,
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


def load_locator_audit(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def select_top_candidate(audit: dict[str, Any]) -> dict[str, Any] | None:
    top = audit.get("top_candidate")
    if isinstance(top, dict):
        return top

    candidates = audit.get("candidates", [])
    if not candidates:
        return None

    return sorted(
        [item for item in candidates if isinstance(item, dict)],
        key=lambda item: (
            -int(item.get("canonical_score", 0)),
            str(item.get("relative_path", "")).casefold(),
        ),
    )[0]


def build_confirmation_options() -> list[dict[str, Any]]:
    return [
        {
            "decision": "ACCEPT_TOP_CANDIDATE_AS_CANONICAL",
            "effect": "Allows a future patch-plan batch to target this UI shell after explicit confirmation.",
            "requires_human": True,
            "applies_now": False,
        },
        {
            "decision": "REJECT_TOP_CANDIDATE",
            "effect": "Keeps UI binding blocked and requires another locator/audit pass.",
            "requires_human": True,
            "applies_now": False,
        },
        {
            "decision": "SELECT_OTHER_CANDIDATE",
            "effect": "Requires the selected path to be supplied in a later confirmation batch.",
            "requires_human": True,
            "applies_now": False,
        },
        {
            "decision": "NEEDS_MORE_REVIEW",
            "effect": "Keeps all UI patching and public deploy blocked.",
            "requires_human": True,
            "applies_now": False,
        },
    ]


def build_binding_patch_plan(top_candidate: dict[str, Any] | None) -> list[dict[str, Any]]:
    target = top_candidate.get("relative_path") if top_candidate else "UNCONFIRMED"

    return [
        {
            "step_id": "bind_webapp_pack",
            "priority": "P0",
            "target_candidate": target,
            "action": "Plan data binding of webapp_pack.json to the confirmed canonical UI shell.",
            "apply_now": False,
        },
        {
            "step_id": "bind_context_pack",
            "priority": "P0",
            "target_candidate": target,
            "action": "Plan context_pack.json binding for lexique/method/prompt context cards.",
            "apply_now": False,
        },
        {
            "step_id": "bind_prompt_payload",
            "priority": "P0",
            "target_candidate": target,
            "action": "Plan prompt_payload.json binding for public human-review prompt flow.",
            "apply_now": False,
        },
        {
            "step_id": "preserve_admin_monitor_separation",
            "priority": "P1",
            "target_candidate": target,
            "action": "Keep ADMIN_MONITOR.html as internal admin/suivi only.",
            "apply_now": False,
        },
        {
            "step_id": "keep_public_deploy_blocked",
            "priority": "P0",
            "target_candidate": target,
            "action": "Do not public deploy until explicit separate authorization.",
            "apply_now": False,
        },
    ]


def build_confirmation_pack(
    audit: dict[str, Any],
    *,
    now_utc: str | None = None,
) -> dict[str, Any]:
    top_candidate = select_top_candidate(audit)
    candidate_count = int(audit.get("candidate_count", 0) or 0)
    probable_count = int(audit.get("probable_canonical_count", 0) or 0)
    possible_count = int(audit.get("possible_canonical_count", 0) or 0)

    reviews: list[str] = ["HUMAN_CONFIRMATION_REQUIRED_BEFORE_ANY_INDEX_PATCH"]
    blockers: list[str] = []

    if top_candidate is None:
        blockers.append("NO_TOP_CANDIDATE_AVAILABLE")
    if possible_count > 1:
        reviews.append("MULTIPLE_POSSIBLE_CANONICAL_INDEX_CANDIDATES")

    decision_status = "BLOCKED" if blockers else "REVIEW_REQUIRED"

    return {
        "runtime": "MVP_QAIC_HUMAN_CONFIRM_CANONICAL_INDEX_PATCH_PLAN",
        "version": "P110B_HUMAN_CONFIRM_CANONICAL_INDEX_PATCH_PLAN_0_1_0",
        "created_at_utc": _now_iso(now_utc),
        "decision_status": decision_status,
        "scope": {
            "mvp": "lexique_webapp_prompts_methods_benchmark_public",
            "qaic_private": "backend_quant_risk_revolutx_execution_locked",
        },
        "candidate_summary": {
            "candidate_count": candidate_count,
            "probable_canonical_count": probable_count,
            "possible_canonical_count": possible_count,
        },
        "top_candidate": top_candidate,
        "confirmation_options": build_confirmation_options(),
        "binding_patch_plan": build_binding_patch_plan(top_candidate),
        "blockers": blockers,
        "reviews": reviews,
        "allowed_next_actions": [
            "HUMAN_CONFIRM_TOP_CANDIDATE",
            "HUMAN_SELECT_OTHER_CANDIDATE",
            "PREPARE_PATCH_PLAN_AFTER_CONFIRMATION",
        ],
        "forbidden_next_actions": [
            "EDIT_INDEX_HTML_NOW",
            "OVERWRITE_INDEX_HTML",
            "GENERATE_PUBLIC_INDEX_HTML",
            "CLASP_PUSH",
            "APPS_SCRIPT_EXECUTION",
            "PUBLIC_DEPLOY_WITHOUT_APPROVAL",
            "BROKER_OR_TRADING_EXECUTION",
        ],
        "safety": dict(CANONICAL_INDEX_CONFIRMATION_SAFETY),
        "next": "P111_BINDING_PATCH_PLAN_AFTER_EXPLICIT_CANONICAL_INDEX_CONFIRMATION",
    }


def render_confirmation_markdown(pack: dict[str, Any]) -> str:
    top = pack.get("top_candidate") or {}
    top_path = top.get("full_path", "NONE")
    top_rel = top.get("relative_path", "NONE")
    top_score = top.get("canonical_score", "NONE")
    top_role = top.get("candidate_role", "NONE")

    options = "\n".join(
        "- `{decision}` | applies_now=`{applies_now}` | requires_human=`{requires_human}`".format(
            **item
        )
        for item in pack["confirmation_options"]
    )
    plan = "\n".join(
        "- **{priority} — {step_id}**: {action} apply_now=`{apply_now}`".format(**item)
        for item in pack["binding_patch_plan"]
    )
    forbidden = "\n".join(f"- `{item}`" for item in pack["forbidden_next_actions"])

    return f"""# P110B — Human Confirm Canonical Index + Patch Plan

## Decision status

`{pack["decision_status"]}`

## Top candidate to confirm

- relative_path: `{top_rel}`
- full_path: `{top_path}`
- score: `{top_score}`
- role: `{top_role}`

## Confirmation options

{options}

## Binding patch plan

{plan}

## Forbidden next actions

{forbidden}

## Safety

- HUMAN_CONFIRMATION_REQUIRED
- NO_INDEX_HTML_EDIT
- NO_INDEX_HTML_GENERATION
- NO_PUBLIC_DEPLOY
- NO_CLASP
- NO_APPS_SCRIPT_EXECUTION
- NO_SHEET_WRITE
- NO_BROKER_ORDER_SIZING
"""


def write_confirmation_csv(path: str | Path, pack: dict[str, Any]) -> None:
    fieldnames = [
        "field",
        "value",
    ]
    top = pack.get("top_candidate") or {}
    rows = [
        {"field": "decision_status", "value": pack["decision_status"]},
        {"field": "candidate_count", "value": pack["candidate_summary"]["candidate_count"]},
        {
            "field": "probable_canonical_count",
            "value": pack["candidate_summary"]["probable_canonical_count"],
        },
        {
            "field": "possible_canonical_count",
            "value": pack["candidate_summary"]["possible_canonical_count"],
        },
        {"field": "top_relative_path", "value": top.get("relative_path", "")},
        {"field": "top_full_path", "value": top.get("full_path", "")},
        {"field": "top_score", "value": top.get("canonical_score", "")},
        {"field": "top_role", "value": top.get("candidate_role", "")},
        {"field": "apply_now", "value": "FALSE"},
        {"field": "public_deploy", "value": "BLOCKED"},
    ]
    with Path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
