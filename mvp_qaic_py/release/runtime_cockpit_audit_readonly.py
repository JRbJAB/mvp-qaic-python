from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.release.live_workflow_release_seal import (
    build_live_workflow_release_seal,
)
from mvp_qaic_py.sheets.decision_journal_append_evidence import (
    build_p96b_live_journal_append_evidence,
)

P98A_STATUS = "OK_P98A_RUNTIME_COCKPIT_AUDIT_READY_READONLY"
NEXT_STEP = "P98B_RUNTIME_COCKPIT_MODULE_OR_P99_MVP_FREEZE"


def build_runtime_cockpit_audit_readonly() -> dict[str, Any]:
    release = build_live_workflow_release_seal()
    p96b = build_p96b_live_journal_append_evidence()
    blockers: list[str] = []

    if release.get("status") != "OK_P97_LIVE_WORKFLOW_RELEASE_SEALED":
        blockers.append("P97_RELEASE_NOT_SEALED")
    if p96b.get("status") != "OK_P96B_LIVE_JOURNAL_APPEND_VERIFIED":
        blockers.append("P96B_APPEND_NOT_VERIFIED")
    if p96b.get("queue_append_status_after") != "APPENDED_TO_DECISION_JOURNAL":
        blockers.append("QUEUE_NOT_MARKED_APPENDED")
    if p96b.get("decision_journal_range") != "BJ17:CN17":
        blockers.append("DECISION_JOURNAL_RANGE_MISMATCH")

    cockpit_cards = [
        {
            "card_id": "P98A_RELEASE_STATUS",
            "label": "Release status",
            "value": release.get("status"),
            "expected_ui": "green when OK_P97_LIVE_WORKFLOW_RELEASE_SEALED",
        },
        {
            "card_id": "P98A_QUEUE_STATUS",
            "label": "Queue row A9",
            "value": p96b.get("queue_append_status_after"),
            "expected_ui": "APPENDED_TO_DECISION_JOURNAL",
        },
        {
            "card_id": "P98A_JOURNAL_STATUS",
            "label": "Decision Journal append",
            "value": p96b.get("journal_id"),
            "expected_ui": "show journal id and BJ17:CN17",
        },
        {
            "card_id": "P98A_SAFETY_STATUS",
            "label": "Safety",
            "value": "NO_BROKER_NO_ORDER_NO_SIZING_NO_APPS_SCRIPT_NO_CLASP",
            "expected_ui": "always visible",
        },
        {
            "card_id": "P98A_NEXT_DECISION",
            "label": "Next decision",
            "value": NEXT_STEP,
            "expected_ui": "operator chooses cockpit module or MVP freeze",
        },
    ]

    surfaces = [
        {
            "surface": "📤 JOURNAL_APPEND_QUEUE!A9:Z9",
            "status": p96b.get("queue_append_status_after"),
            "write_in_p98a": False,
        },
        {
            "surface": "🧾 DECISION_JOURNAL!BJ17:CN17",
            "status": p96b.get("validation_status"),
            "write_in_p98a": False,
        },
        {
            "surface": "repo release seal",
            "status": release.get("status"),
            "write_in_p98a": False,
        },
    ]

    safety = {
        "readonly_audit_only": True,
        "live_write_executed_in_p98a": False,
        "decision_journal_write_in_p98a": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "trading_action": False,
    }

    status = P98A_STATUS if not blockers else "BLOCKED_P98A_RUNTIME_COCKPIT_AUDIT"

    return {
        "step": "P98A_RUNTIME_COCKPIT_AUDIT_READONLY",
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "scope": "P91_TO_P97_RUNTIME_COCKPIT_AUDIT_ONLY",
        "release_status": release.get("status"),
        "journal_id": p96b.get("journal_id"),
        "journal_queue_id": p96b.get("journal_queue_id"),
        "decision_journal_range": p96b.get("decision_journal_range"),
        "queue_range": p96b.get("queue_range"),
        "cockpit_cards": cockpit_cards,
        "surfaces": surfaces,
        "safety": safety,
        "blockers": blockers,
        "next": NEXT_STEP if not blockers else "FIX_BLOCKERS_BEFORE_P98B_OR_P99",
    }


def assert_runtime_cockpit_audit_readonly_safe(payload: dict[str, Any]) -> None:
    if payload["status"] != P98A_STATUS:
        raise ValueError(f"P98A audit not OK: {payload['status']}")
    if payload["blockers"]:
        raise ValueError(f"P98A blockers present: {payload['blockers']}")

    safety = payload["safety"]
    expected_false = (
        "live_write_executed_in_p98a",
        "decision_journal_write_in_p98a",
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
        "trading_action",
    )
    enabled = [flag for flag in expected_false if safety.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe P98A flags enabled: {enabled}")
    if safety.get("readonly_audit_only") is not True:
        raise ValueError("P98A must remain readonly audit only")

    for surface in payload["surfaces"]:
        if surface.get("write_in_p98a") is not False:
            raise ValueError(f"P98A surface write requested: {surface}")


def render_runtime_cockpit_audit_readonly_markdown(payload: dict[str, Any]) -> str:
    cards = [
        f"- {card['card_id']}: `{card['value']}` — {card['expected_ui']}"
        for card in payload["cockpit_cards"]
    ]
    surfaces = [
        f"- {surface['surface']}: `{surface['status']}` / write_in_p98a={surface['write_in_p98a']}"
        for surface in payload["surfaces"]
    ]
    return "\n".join(
        [
            "# MVP QAIC — P98A Runtime Cockpit Audit READONLY",
            "",
            f"- status: `{payload['status']}`",
            f"- scope: `{payload['scope']}`",
            f"- release_status: `{payload['release_status']}`",
            f"- journal_id: `{payload['journal_id']}`",
            f"- decision_journal_range: `{payload['decision_journal_range']}`",
            f"- queue_range: `{payload['queue_range']}`",
            "",
            "## Cockpit cards",
            "",
            *cards,
            "",
            "## Surfaces",
            "",
            *surfaces,
            "",
            "## Safety",
            "",
            "- read-only audit only",
            "- no live write in P98A",
            "- no Decision Journal write in P98A",
            "- no Apps Script execution",
            "- no CLASP push",
            "- no broker/order/sizing",
            "",
            "## Next",
            "",
            f"`{payload['next']}`",
            "",
        ]
    )


def export_runtime_cockpit_audit_readonly(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_runtime_cockpit_audit_readonly()
    assert_runtime_cockpit_audit_readonly_safe(payload)
    markdown = render_runtime_cockpit_audit_readonly_markdown(payload)
    json_path = target / "P98A_RUNTIME_COCKPIT_AUDIT_READONLY.json"
    md_path = target / "P98A_RUNTIME_COCKPIT_AUDIT_READONLY.md"
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
