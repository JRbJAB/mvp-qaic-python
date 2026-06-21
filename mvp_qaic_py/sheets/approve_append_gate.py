from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.sheets.controlled_queue_write_evidence import (
    build_p93_controlled_queue_write_evidence,
)

APPROVE_APPEND_TOKEN = "APPROVE_P94_APPEND_GATE"
CONTROLLED_QUEUE = "📤 JOURNAL_APPEND_QUEUE"
BLOCKED_DIRECT_TARGET = "🧾 DECISION_JOURNAL"


def build_approve_append_gate(
    *,
    queue_row: dict[str, Any] | None = None,
    approve_append_requested: bool = False,
    approval_token: str | None = None,
    target_sheet: str = CONTROLLED_QUEUE,
) -> dict[str, Any]:
    row = queue_row or build_p93_controlled_queue_write_evidence()
    blockers: list[str] = []

    if target_sheet != CONTROLLED_QUEUE:
        blockers.append("TARGET_NOT_CONTROLLED_QUEUE")
    if target_sheet == BLOCKED_DIRECT_TARGET:
        blockers.append("DIRECT_DECISION_JOURNAL_WRITE_BLOCKED")
    if row.get("sheet_name") != CONTROLLED_QUEUE:
        blockers.append("SOURCE_ROW_NOT_FROM_CONTROLLED_QUEUE")
    if row.get("journal_queue_id") != "P93-CQW-20260621-200001":
        blockers.append("UNEXPECTED_QUEUE_ROW")
    if row.get("safe_to_append") != "NO":
        blockers.append("SOURCE_ROW_NOT_IN_SAFE_HOLD_STATE")
    if row.get("human_review_decision") != "DO_NOT_APPEND":
        blockers.append("SOURCE_ROW_NOT_HUMAN_HOLD")
    if not row.get("risk_guard"):
        blockers.append("MISSING_RISK_GUARD")
    if row.get("direct_decision_journal_write") is True:
        blockers.append("DIRECT_DECISION_JOURNAL_WRITE_TRUE")

    approval_token_ok = approval_token == APPROVE_APPEND_TOKEN
    if approve_append_requested and not approval_token_ok:
        blockers.append("MISSING_APPROVE_APPEND_TOKEN")

    if blockers:
        status = "BLOCKED_P94_APPROVE_APPEND_GATE"
        next_step = "FIX_BLOCKERS_BEFORE_P95"
    elif approve_append_requested:
        status = "REVIEW_REQUIRED_P94_READY_FOR_P95_APPROVE_APPEND_FLIP"
        next_step = "P95_LIVE_FLIP_QUEUE_ROW_TO_APPROVE_APPEND_AFTER_EXPLICIT_GO"
    else:
        status = "OK_P94_APPROVE_APPEND_GATE_READY_HOLD_NO_LIVE_WRITE"
        next_step = "P95_LIVE_FLIP_QUEUE_ROW_TO_APPROVE_APPEND_AFTER_EXPLICIT_GO"

    return {
        "step": "P94_APPROVE_APPEND_GATE_LOCAL_FIRST",
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_range": row.get("range"),
        "journal_queue_id": row.get("journal_queue_id"),
        "target_sheet": target_sheet,
        "approve_append_requested": approve_append_requested,
        "approval_token_ok": approval_token_ok,
        "current_human_review_decision": row.get("human_review_decision"),
        "current_safe_to_append": row.get("safe_to_append"),
        "planned_human_review_decision": (
            "APPROVE_APPEND" if approve_append_requested else "DO_NOT_APPEND"
        ),
        "planned_safe_to_append": "YES" if approve_append_requested else "NO",
        "sheet_write_executed": False,
        "direct_decision_journal_write": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "blockers": blockers,
        "next": next_step,
    }


def assert_approve_append_gate_safe(payload: dict[str, Any]) -> None:
    if payload["sheet_write_executed"]:
        raise ValueError("P94 must not execute live write")
    forbidden = (
        "direct_decision_journal_write",
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
    )
    enabled = [flag for flag in forbidden if payload.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe P94 flags enabled: {enabled}")


def render_approve_append_gate_markdown(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# MVP QAIC — P94 Approve Append Gate",
            "",
            f"- status: `{payload['status']}`",
            f"- source_range: `{payload['source_range']}`",
            f"- journal_queue_id: `{payload['journal_queue_id']}`",
            f"- approve_append_requested: `{payload['approve_append_requested']}`",
            f"- approval_token_ok: `{payload['approval_token_ok']}`",
            f"- current_human_review_decision: `{payload['current_human_review_decision']}`",
            f"- current_safe_to_append: `{payload['current_safe_to_append']}`",
            f"- planned_human_review_decision: `{payload['planned_human_review_decision']}`",
            f"- planned_safe_to_append: `{payload['planned_safe_to_append']}`",
            f"- sheet_write_executed: `{payload['sheet_write_executed']}`",
            f"- blockers: `{payload['blockers']}`",
            "",
            "## Safety",
            "",
            "- no live write in P94",
            "- no direct Decision Journal write",
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


def export_approve_append_gate(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_approve_append_gate()
    assert_approve_append_gate_safe(payload)
    markdown = render_approve_append_gate_markdown(payload)
    json_path = target / "P94_APPROVE_APPEND_GATE.json"
    md_path = target / "P94_APPROVE_APPEND_GATE.md"
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
