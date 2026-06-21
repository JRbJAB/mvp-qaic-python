from __future__ import annotations

import json
from pathlib import Path
from typing import Any

P95_LIVE_APPROVE_APPEND_FLIP_ROW: dict[str, Any] = {
    "step": "P95_LIVE_APPROVE_APPEND_FLIP",
    "status": "OK_P95_LIVE_APPROVE_APPEND_FLIP_VERIFIED",
    "spreadsheet_id": "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0",
    "sheet_name": "📤 JOURNAL_APPEND_QUEUE",
    "range": "A9:Z9",
    "row_number": 9,
    "journal_queue_id": "P93-CQW-20260621-200001",
    "journal_status": "APPROVE_APPEND_GATE_OPEN",
    "human_review_decision": "APPROVE_APPEND",
    "safe_to_append": "YES",
    "append_status": "APPROVE_APPEND_PENDING_JOURNAL_APPEND",
    "append_run_id": "P95-FLIP-20260621-210001",
    "decision_status": "APPROVED_FOR_APPEND_GATE",
    "validation_status": "P95_APPROVE_APPEND_FLIP_VALIDATED",
    "human_final_decision": "APPROVE_APPEND",
    "risk_guard": "HUMAN_REVIEW_ONLY_NO_BROKER_NO_ORDER_NO_SIZING",
    "missing_data": "NONE_FOR_APPEND_GATE",
    "blockers": "NONE",
    "source_trace": (
        "chatgpt_connector|GO_P93_CONTROLLED_QUEUE_WRITE|row=9|"
        "GO_P95_LIVE_FLIP_QUEUE_ROW_TO_APPROVE_APPEND|row=9"
    ),
    "sheet_write_executed": True,
    "journal_append_executed": False,
    "direct_decision_journal_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker_execution": False,
    "order_execution": False,
    "auto_sizing_execution": False,
}


def build_p95_live_approve_append_flip_evidence() -> dict[str, Any]:
    return dict(P95_LIVE_APPROVE_APPEND_FLIP_ROW)


def assert_p95_live_approve_append_flip_safe(payload: dict[str, Any]) -> None:
    if payload["sheet_write_executed"] is not True:
        raise ValueError("P95 live approval flip was not executed")
    if payload["journal_append_executed"] is not False:
        raise ValueError("P95 must not append to Decision Journal")
    if payload["sheet_name"] != "📤 JOURNAL_APPEND_QUEUE":
        raise ValueError("Unexpected P95 target sheet")
    if payload["range"] != "A9:Z9":
        raise ValueError("Unexpected P95 range")
    if payload["human_review_decision"] != "APPROVE_APPEND":
        raise ValueError("P95 row must be APPROVE_APPEND")
    if payload["safe_to_append"] != "YES":
        raise ValueError("P95 row safe_to_append must be YES")
    if payload["append_status"] != "APPROVE_APPEND_PENDING_JOURNAL_APPEND":
        raise ValueError("Unexpected P95 append status")
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
        raise ValueError(f"Unsafe P95 flags enabled: {enabled}")


def render_p95_live_approve_append_flip_markdown(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# MVP QAIC — P95 Live Approve Append Flip Evidence",
            "",
            f"- status: `{payload['status']}`",
            f"- sheet_name: `{payload['sheet_name']}`",
            f"- range: `{payload['range']}`",
            f"- journal_queue_id: `{payload['journal_queue_id']}`",
            f"- human_review_decision: `{payload['human_review_decision']}`",
            f"- safe_to_append: `{payload['safe_to_append']}`",
            f"- append_status: `{payload['append_status']}`",
            f"- validation_status: `{payload['validation_status']}`",
            f"- journal_append_executed: `{payload['journal_append_executed']}`",
            "",
            "## Safety",
            "",
            "- queue row approval flip only",
            "- no direct Decision Journal write",
            "- no journal append in P95",
            "- no Apps Script execution",
            "- no CLASP push",
            "- no broker/order/sizing",
            "",
            "## Next",
            "",
            "`P96_JOURNAL_APPEND_DRYRUN_OR_LIVE_AFTER_EXPLICIT_GO`",
            "",
        ]
    )


def export_p95_live_approve_append_flip_evidence(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_p95_live_approve_append_flip_evidence()
    assert_p95_live_approve_append_flip_safe(payload)
    markdown = render_p95_live_approve_append_flip_markdown(payload)
    json_path = target / "P95_LIVE_APPROVE_APPEND_FLIP_EVIDENCE.json"
    md_path = target / "P95_LIVE_APPROVE_APPEND_FLIP_EVIDENCE.md"
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "status": payload["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": "P96_JOURNAL_APPEND_DRYRUN_OR_LIVE_AFTER_EXPLICIT_GO",
    }
