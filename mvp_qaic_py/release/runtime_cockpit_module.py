from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.release.runtime_cockpit_audit_readonly import (
    build_runtime_cockpit_audit_readonly,
)

P98B_STATUS = "OK_P98B_RUNTIME_COCKPIT_MODULE_LOCAL_READY"
NEXT_STEP = "P99_MVP_FREEZE_RELEASE_HANDOFF_OR_P98C_COCKPIT_UI_EXPORT"


def build_runtime_cockpit_module() -> dict[str, Any]:
    audit = build_runtime_cockpit_audit_readonly()
    blockers: list[str] = []

    if audit.get("status") != "OK_P98A_RUNTIME_COCKPIT_AUDIT_READY_READONLY":
        blockers.append("P98A_AUDIT_NOT_READY")
    if audit.get("journal_id") != "DJ-P96B-P93-CQW-20260621-200001":
        blockers.append("P96B_JOURNAL_ID_MISMATCH")
    if audit.get("decision_journal_range") != "BJ17:CN17":
        blockers.append("DECISION_JOURNAL_RANGE_MISMATCH")
    if audit.get("queue_range") != "A9:Z9":
        blockers.append("QUEUE_RANGE_MISMATCH")

    cockpit_status_cards = [
        {
            "slot": "TOP_LEFT",
            "card_id": "LIVE_WORKFLOW_STATUS",
            "title": "Workflow live",
            "value": "SEALED_P91_TO_P97",
            "state": "OK",
            "operator_meaning": "La chaine queue -> approbation -> journal est fermee et auditee.",
        },
        {
            "slot": "TOP_CENTER",
            "card_id": "QUEUE_ROW_STATUS",
            "title": "Queue A9",
            "value": "APPENDED_TO_DECISION_JOURNAL",
            "state": "OK",
            "operator_meaning": "La ligne approuvee a ete journalisee.",
        },
        {
            "slot": "TOP_RIGHT",
            "card_id": "DECISION_JOURNAL_STATUS",
            "title": "Journal",
            "value": "DJ-P96B-P93-CQW-20260621-200001",
            "state": "OK",
            "operator_meaning": "Append visible dans Decision Journal BJ17:CN17.",
        },
        {
            "slot": "MIDDLE_LEFT",
            "card_id": "SAFETY_STATUS",
            "title": "Securite",
            "value": "NO_BROKER_NO_ORDER_NO_SIZING",
            "state": "LOCKED",
            "operator_meaning": "Cockpit decisionnel uniquement, aucune execution trading.",
        },
        {
            "slot": "MIDDLE_CENTER",
            "card_id": "NEXT_DECISION",
            "title": "Prochaine decision",
            "value": NEXT_STEP,
            "state": "REVIEW",
            "operator_meaning": "Choisir freeze MVP ou export UI cockpit.",
        },
    ]

    visual_plan = [
        "[1 GPT/Input] -> [2 Prompt Queue] -> [3 Response Intake] -> [4 Journal Queue]",
        "[4 Journal Queue] -> [5 Human Approval Gate] -> [6 Dryrun Append] -> [7 Decision Journal]",
        "[7 Decision Journal] -> [8 Release Seal] -> [9 Cockpit Readonly] -> [10 Freeze/UX]",
    ]

    operating_summary = {
        "tool_mode": "human_review_only_decision_support",
        "main_loop": [
            "prepare payload/prompt",
            "capture response/intake",
            "queue journal candidate",
            "human approval gate",
            "dry-run validation",
            "controlled journal append",
            "release/cockpit audit",
        ],
        "allowed_actions": [
            "local validation",
            "read-only cockpit audit",
            "controlled journal logging after explicit GO",
        ],
        "blocked_actions": [
            "broker execution",
            "order placement",
            "auto sizing",
            "Apps Script execution without explicit gate",
            "CLASP push without explicit gate",
        ],
    }

    cockpit_surfaces = [
        {
            "surface_id": "SOURCE_QUEUE",
            "label": "Journal Append Queue",
            "source": "📤 JOURNAL_APPEND_QUEUE!A9:Z9",
            "display_fields": ["journal_queue_id", "safe_to_append", "append_status", "journal_id"],
            "write_in_p98b": False,
        },
        {
            "surface_id": "DECISION_JOURNAL",
            "label": "Decision Journal",
            "source": "🧾 DECISION_JOURNAL!BJ17:CN17",
            "display_fields": ["decision_id", "validation_status", "journal_id", "safety"],
            "write_in_p98b": False,
        },
        {
            "surface_id": "RELEASE_SEAL",
            "label": "Release Seal",
            "source": "repo: P97 release seal",
            "display_fields": ["status", "sealed_range", "next"],
            "write_in_p98b": False,
        },
    ]

    safety = {
        "local_module_only": True,
        "live_write_executed_in_p98b": False,
        "decision_journal_write_in_p98b": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "trading_action": False,
    }

    status = P98B_STATUS if not blockers else "BLOCKED_P98B_RUNTIME_COCKPIT_MODULE"

    return {
        "step": "P98B_RUNTIME_COCKPIT_MODULE_LOCAL",
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_audit_status": audit.get("status"),
        "journal_id": audit.get("journal_id"),
        "journal_queue_id": audit.get("journal_queue_id"),
        "visual_plan": visual_plan,
        "operating_summary": operating_summary,
        "cockpit_status_cards": cockpit_status_cards,
        "cockpit_surfaces": cockpit_surfaces,
        "safety": safety,
        "blockers": blockers,
        "next": NEXT_STEP if not blockers else "FIX_BLOCKERS_BEFORE_P99_OR_P98C",
    }


def assert_runtime_cockpit_module_safe(payload: dict[str, Any]) -> None:
    if payload["status"] != P98B_STATUS:
        raise ValueError(f"P98B module not OK: {payload['status']}")
    if payload["blockers"]:
        raise ValueError(f"P98B blockers present: {payload['blockers']}")

    safety = payload["safety"]
    expected_false = (
        "live_write_executed_in_p98b",
        "decision_journal_write_in_p98b",
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
        "trading_action",
    )
    enabled = [flag for flag in expected_false if safety.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe P98B flags enabled: {enabled}")
    if safety.get("local_module_only") is not True:
        raise ValueError("P98B must remain local module only")

    for surface in payload["cockpit_surfaces"]:
        if surface.get("write_in_p98b") is not False:
            raise ValueError(f"P98B surface write requested: {surface}")


def render_runtime_cockpit_module_markdown(payload: dict[str, Any]) -> str:
    visual_lines = [f"- `{line}`" for line in payload["visual_plan"]]
    cards = [
        f"- {card['slot']} / {card['card_id']}: `{card['value']}` ({card['state']}) — {card['operator_meaning']}"
        for card in payload["cockpit_status_cards"]
    ]
    surfaces = [
        f"- {surface['surface_id']}: `{surface['source']}` / write_in_p98b={surface['write_in_p98b']}"
        for surface in payload["cockpit_surfaces"]
    ]
    loop_lines = [f"- {item}" for item in payload["operating_summary"]["main_loop"]]
    blocked_lines = [f"- {item}" for item in payload["operating_summary"]["blocked_actions"]]

    return "\n".join(
        [
            "# MVP QAIC — P98B Runtime Cockpit Module Local",
            "",
            f"- status: `{payload['status']}`",
            f"- journal_id: `{payload['journal_id']}`",
            f"- next: `{payload['next']}`",
            "",
            "## Planning visuel",
            "",
            *visual_lines,
            "",
            "## Mode de fonctionnement",
            "",
            *loop_lines,
            "",
            "## Cartes cockpit",
            "",
            *cards,
            "",
            "## Surfaces cockpit",
            "",
            *surfaces,
            "",
            "## Actions bloquees",
            "",
            *blocked_lines,
            "",
            "## Safety",
            "",
            "- local module only",
            "- no live write in P98B",
            "- no Decision Journal write in P98B",
            "- no Apps Script execution",
            "- no CLASP push",
            "- no broker/order/sizing",
            "",
        ]
    )


def export_runtime_cockpit_module(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_runtime_cockpit_module()
    assert_runtime_cockpit_module_safe(payload)
    markdown = render_runtime_cockpit_module_markdown(payload)
    json_path = target / "P98B_RUNTIME_COCKPIT_MODULE.json"
    md_path = target / "P98B_RUNTIME_COCKPIT_MODULE.md"
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "status": payload["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": payload["next"],
    }
