from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.sheets.live_write_smoke_evidence import (
    build_p91_live_write_smoke_evidence,
)
from mvp_qaic_py.sheets.write_capable_contract import (
    APPROVAL_TOKEN,
    build_sheets_write_capable_contract,
)

CONTROLLED_TARGET = "📤 JOURNAL_APPEND_QUEUE"
BLOCKED_DIRECT_TARGET = "🧾 DECISION_JOURNAL"
P92_APPROVAL_TOKEN = "APPROVE_P92_CONTROLLED_WRITE_PIPELINE"


def build_write_pipeline_control(
    *,
    target_sheet: str = CONTROLLED_TARGET,
    operation: str = "APPEND_REVIEW_EVENT",
    live_write_enabled: bool = False,
    approval_token: str | None = None,
) -> dict[str, Any]:
    p90 = build_sheets_write_capable_contract(
        target_sheet=target_sheet,
        operation=operation,
        write_enabled=True,
        approval_token=APPROVAL_TOKEN,
    )
    p91 = build_p91_live_write_smoke_evidence()

    blockers: list[str] = []
    if p90["status"] != "REVIEW_REQUIRED_P90_WRITE_ENABLE_REQUEST_READY_FOR_P91":
        blockers.append("P90_WRITE_CAPABLE_CONTRACT_NOT_READY")
    if p91["status"] != "OK_P91_LIVE_WRITE_SMOKE_ROW_VERIFIED":
        blockers.append("P91_LIVE_WRITE_SMOKE_NOT_VERIFIED")
    if target_sheet == BLOCKED_DIRECT_TARGET:
        blockers.append("DIRECT_DECISION_JOURNAL_WRITE_BLOCKED")
    if target_sheet != CONTROLLED_TARGET:
        blockers.append("TARGET_NOT_CONTROLLED_QUEUE")
    if live_write_enabled and approval_token != P92_APPROVAL_TOKEN:
        blockers.append("MISSING_P92_APPROVAL_TOKEN")

    if blockers:
        status = "BLOCKED_P92_WRITE_PIPELINE_CONTROL"
        next_step = "FIX_BLOCKERS_BEFORE_ANY_WRITE"
    elif live_write_enabled:
        status = "REVIEW_REQUIRED_P92_READY_FOR_CONTROLLED_QUEUE_WRITE"
        next_step = "P93_CONTROLLED_QUEUE_WRITE_AFTER_EXPLICIT_GO"
    else:
        status = "OK_P92_WRITE_PIPELINE_CONTROL_READY_NO_LIVE_WRITE"
        next_step = "P93_CONTROLLED_QUEUE_WRITE_AFTER_EXPLICIT_GO"

    return {
        "step": "P92_WRITE_PIPELINE_CONTROL_FAST_FUSE",
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "target_sheet": target_sheet,
        "operation": operation,
        "live_write_enabled": live_write_enabled,
        "sheet_write_executed": False,
        "p90_status": p90["status"],
        "p91_status": p91["status"],
        "last_smoke_row": p91["range"],
        "last_smoke_id": p91["journal_queue_id"],
        "blockers": blockers,
        "approval_required_for_p93": True,
        "approval_token_ok": approval_token == P92_APPROVAL_TOKEN,
        "direct_decision_journal_write": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "planned_write_policy": {
            "target": CONTROLLED_TARGET,
            "mode": "QUEUE_ONLY",
            "human_review_decision_default": "DO_NOT_APPEND",
            "safe_to_append_default": "NO",
            "decision_journal_append": "BLOCKED_UNTIL_APPROVE_APPEND",
        },
        "next": next_step,
    }


def assert_write_pipeline_control_safe(payload: dict[str, Any]) -> None:
    if payload["sheet_write_executed"]:
        raise ValueError("P92 must not execute a second live write")
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
        raise ValueError(f"Unsafe P92 flags enabled: {enabled}")
    if payload["target_sheet"] == BLOCKED_DIRECT_TARGET:
        raise ValueError("Direct Decision Journal write is blocked")


def render_write_pipeline_control_markdown(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# MVP QAIC — P92 Write Pipeline Control",
            "",
            f"- status: `{payload['status']}`",
            f"- target_sheet: `{payload['target_sheet']}`",
            f"- operation: `{payload['operation']}`",
            f"- live_write_enabled: `{payload['live_write_enabled']}`",
            f"- sheet_write_executed: `{payload['sheet_write_executed']}`",
            f"- p90_status: `{payload['p90_status']}`",
            f"- p91_status: `{payload['p91_status']}`",
            f"- last_smoke_row: `{payload['last_smoke_row']}`",
            f"- blockers: `{payload['blockers']}`",
            "",
            "## Safety",
            "",
            "- no second live write",
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


def export_write_pipeline_control(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_write_pipeline_control()
    assert_write_pipeline_control_safe(payload)
    markdown = render_write_pipeline_control_markdown(payload)
    json_path = target / "P92_WRITE_PIPELINE_CONTROL.json"
    md_path = target / "P92_WRITE_PIPELINE_CONTROL.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "status": payload["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": payload["next"],
    }
