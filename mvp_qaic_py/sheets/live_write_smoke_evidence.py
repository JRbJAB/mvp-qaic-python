from __future__ import annotations

import json
from pathlib import Path
from typing import Any

P91_LIVE_WRITE_SMOKE_ROW: dict[str, Any] = {
    "step": "P91_SINGLE_ROW_STAGING_WRITE_SMOKE",
    "status": "OK_P91_LIVE_WRITE_SMOKE_ROW_VERIFIED",
    "spreadsheet_id": "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0",
    "sheet_name": "📤 JOURNAL_APPEND_QUEUE",
    "range": "A8:Z8",
    "row_number": 8,
    "journal_queue_id": "P91-SMOKE-20260621-195001",
    "intake_queue_id": "P91-LIVE-SMOKE",
    "run_queue_id": "P91-LOCAL",
    "prompt_id": "p91_single_row_smoke",
    "prompt_title": "P91 Single Row Smoke",
    "journal_status": "SMOKE_ONLY",
    "human_review_decision": "DO_NOT_APPEND",
    "safe_to_append": "NO",
    "duplicate_status": "P91_SMOKE_UNIQUE",
    "append_status": "SMOKE_ONLY_DO_NOT_APPEND",
    "append_run_id": "P91-SMOKE-20260621-195001",
    "payload_id": "P91-SMOKE-PAYLOAD",
    "payload_hash": "P91-SMOKE-HASH-NA",
    "decision_status": "NO_ACTION",
    "validation_status": "P91_SMOKE_VALIDATED",
    "human_final_decision": "NO_ACTION",
    "risk_guard": "SAFE_SMOKE",
    "missing_data": "NONE_FOR_SMOKE",
    "blockers": "SMOKE_ROW_DO_NOT_APPEND",
    "source_trace": "chatgpt_connector|GO_P91_WRITE_SMOKE|target=JOURNAL_APPEND_QUEUE|row=8",
    "sheet_write_executed": True,
    "direct_decision_journal_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker_execution": False,
    "order_execution": False,
    "auto_sizing_execution": False,
}


def build_p91_live_write_smoke_evidence() -> dict[str, Any]:
    return dict(P91_LIVE_WRITE_SMOKE_ROW)


def assert_p91_live_write_smoke_safe(payload: dict[str, Any]) -> None:
    if payload["sheet_write_executed"] is not True:
        raise ValueError("P91 live write smoke was not executed")
    if payload["sheet_name"] != "📤 JOURNAL_APPEND_QUEUE":
        raise ValueError("Unexpected P91 target sheet")
    if payload["human_review_decision"] != "DO_NOT_APPEND":
        raise ValueError("P91 smoke row must not be append-approved")
    if payload["safe_to_append"] != "NO":
        raise ValueError("P91 smoke row safe_to_append must be NO")
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
        raise ValueError(f"Unsafe P91 flags enabled: {enabled}")


def render_p91_live_write_smoke_markdown(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# MVP QAIC — P91 Live Write Smoke Evidence",
            "",
            f"- status: `{payload['status']}`",
            f"- spreadsheet_id: `{payload['spreadsheet_id']}`",
            f"- sheet_name: `{payload['sheet_name']}`",
            f"- range: `{payload['range']}`",
            f"- journal_queue_id: `{payload['journal_queue_id']}`",
            f"- human_review_decision: `{payload['human_review_decision']}`",
            f"- safe_to_append: `{payload['safe_to_append']}`",
            f"- append_status: `{payload['append_status']}`",
            f"- validation_status: `{payload['validation_status']}`",
            "",
            "## Safety",
            "",
            "- sheet write executed: one smoke row only",
            "- direct Decision Journal write: false",
            "- Apps Script execution: false",
            "- CLASP push: false",
            "- broker/order/sizing: false",
            "",
            "## Next",
            "",
            "`P92_WRITE_PIPELINE_HARDENING_OR_P92_APPEND_QUEUE_CONTROLLED_WORKFLOW`",
            "",
        ]
    )


def export_p91_live_write_smoke_evidence(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_p91_live_write_smoke_evidence()
    assert_p91_live_write_smoke_safe(payload)
    markdown = render_p91_live_write_smoke_markdown(payload)
    json_path = target / "P91_LIVE_WRITE_SMOKE_EVIDENCE.json"
    md_path = target / "P91_LIVE_WRITE_SMOKE_EVIDENCE.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "status": payload["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": "P92_WRITE_PIPELINE_HARDENING_OR_P92_APPEND_QUEUE_CONTROLLED_WORKFLOW",
    }
