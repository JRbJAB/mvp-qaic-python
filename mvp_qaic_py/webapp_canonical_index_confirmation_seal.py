from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


CANONICAL_INDEX_CONFIRMATION_SEAL_SAFETY: dict[str, bool] = {
    "mvp_public_scope": True,
    "qaic_private_backend_separated": True,
    "canonical_index_confirmation_only": True,
    "binding_target_contract_only": True,
    "after_p112_reconcile": True,
    "no_index_html_edit": True,
    "no_index_html_generation": True,
    "no_source_patch_apply": True,
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


def load_confirmation_pack(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def extract_top_candidate(pack: dict[str, Any]) -> dict[str, Any] | None:
    top = pack.get("top_candidate")
    if isinstance(top, dict) and top.get("relative_path"):
        return top
    return None


def build_canonical_confirmation_decision(
    pack: dict[str, Any],
    *,
    human_decision: str = "ACCEPT_TOP_CANDIDATE_AS_CANONICAL",
    now_utc: str | None = None,
) -> dict[str, Any]:
    top = extract_top_candidate(pack)
    blockers: list[str] = []
    reviews: list[str] = ["P111_R1_RECONCILE_AFTER_P112_ALREADY_SEALED"]

    if top is None:
        blockers.append("NO_TOP_CANDIDATE_TO_CONFIRM")
    if human_decision != "ACCEPT_TOP_CANDIDATE_AS_CANONICAL":
        blockers.append("TOP_CANDIDATE_NOT_ACCEPTED")

    candidate_score = int(top.get("canonical_score", 0)) if top else 0
    if candidate_score < 80:
        reviews.append("TOP_CANDIDATE_SCORE_BELOW_STRONG_THRESHOLD")

    decision_status = "BLOCKED" if blockers else "CONFIRMED_CANONICAL_TARGET_CONTRACT_READY"

    return {
        "runtime": "MVP_QAIC_CANONICAL_INDEX_CONFIRMATION_SEAL_AFTER_P112",
        "version": "P111_R1_CANONICAL_INDEX_CONFIRMATION_SEAL_AFTER_P112_0_1_0",
        "created_at_utc": _now_iso(now_utc),
        "decision_status": decision_status,
        "human_decision": human_decision,
        "confirmed_canonical_candidate": top,
        "binding_target_contract": {
            "target_relative_path": top.get("relative_path") if top else None,
            "target_full_path": top.get("full_path") if top else None,
            "target_role": top.get("candidate_role") if top else None,
            "target_score": top.get("canonical_score") if top else None,
            "allowed_to_edit_now": False,
            "patch_allowed_now": False,
            "future_patch_requires_separate_batch": True,
            "reconciled_after_p112": True,
        },
        "blockers": blockers,
        "reviews": reviews,
        "allowed_next_actions": [
            "CONTINUE_WITH_P113_PORTFOLIO_INPUT_NORMALIZER_AND_IMAGE_REVIEW_WORKFLOW",
            "KEEP_P112_AS_ALREADY_SEALED_PROMPT_MODULE",
            "PREPARE_FUTURE_BINDING_PATCH_PLAN_ONLY",
        ],
        "forbidden_next_actions": [
            "ROLLBACK_P112_WITHOUT_REASON",
            "EDIT_INDEX_HTML_NOW",
            "OVERWRITE_INDEX_HTML",
            "GENERATE_PUBLIC_INDEX_HTML",
            "CLASP_PUSH",
            "APPS_SCRIPT_EXECUTION",
            "PUBLIC_DEPLOY_WITHOUT_APPROVAL",
            "BROKER_OR_TRADING_EXECUTION",
        ],
        "safety": dict(CANONICAL_INDEX_CONFIRMATION_SEAL_SAFETY),
        "next": "P113_PORTFOLIO_INPUT_NORMALIZER_AND_IMAGE_REVIEW_WORKFLOW",
    }


def render_confirmation_seal_markdown(decision: dict[str, Any]) -> str:
    target = decision.get("confirmed_canonical_candidate") or {}
    allowed = "\n".join(f"- `{item}`" for item in decision["allowed_next_actions"])
    forbidden = "\n".join(f"- `{item}`" for item in decision["forbidden_next_actions"])

    return f"""# P111-R1 — Canonical Index Confirmation Seal After P112

## Decision status

`{decision["decision_status"]}`

## Why R1

P112 was already sealed before P111. This R1 reconciles the sequence without rollback.

## Human decision

`{decision["human_decision"]}`

## Confirmed canonical target

- relative_path: `{target.get("relative_path", "NONE")}`
- full_path: `{target.get("full_path", "NONE")}`
- role: `{target.get("candidate_role", "NONE")}`
- score: `{target.get("canonical_score", "NONE")}`
- allowed_to_edit_now: `false`

## Binding target contract

- patch_allowed_now: `false`
- future_patch_requires_separate_batch: `true`
- reconciled_after_p112: `true`
- public_deploy: `BLOCKED`

## Allowed next actions

{allowed}

## Forbidden next actions

{forbidden}

## Safety

- NO_INDEX_HTML_EDIT
- NO_INDEX_HTML_GENERATION
- NO_SOURCE_PATCH_APPLY
- NO_PUBLIC_DEPLOY
- NO_CLASP
- NO_APPS_SCRIPT_EXECUTION
- NO_SHEET_WRITE
- NO_BROKER_ORDER_SIZING
"""


def write_decision_summary_csv(path: str | Path, decision: dict[str, Any]) -> None:
    target = decision.get("confirmed_canonical_candidate") or {}
    rows = [
        {"field": "decision_status", "value": decision["decision_status"]},
        {"field": "human_decision", "value": decision["human_decision"]},
        {"field": "target_relative_path", "value": target.get("relative_path", "")},
        {"field": "target_full_path", "value": target.get("full_path", "")},
        {"field": "target_score", "value": target.get("canonical_score", "")},
        {"field": "allowed_to_edit_now", "value": "FALSE"},
        {"field": "patch_allowed_now", "value": "FALSE"},
        {"field": "reconciled_after_p112", "value": "TRUE"},
        {"field": "public_deploy", "value": "BLOCKED"},
    ]
    with Path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["field", "value"])
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
