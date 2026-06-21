from __future__ import annotations

import json
from pathlib import Path
from typing import Any

P93_CONTROLLED_QUEUE_WRITE_ROW: dict[str, Any] = {
    "step": "P93_CONTROLLED_QUEUE_WRITE",
    "status": "OK_P93_CONTROLLED_QUEUE_WRITE_ROW_VERIFIED",
    "spreadsheet_id": "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0",
    "sheet_name": "📤 JOURNAL_APPEND_QUEUE",
    "range": "A9:Z9",
    "row_number": 9,
    "journal_queue_id": "P93-CQW-20260621-200001",
    "human_review_decision": "DO_NOT_APPEND",
    "safe_to_append": "NO",
    "append_status": "CONTROLLED_QUEUE_WRITE_PENDING_REVIEW",
    "validation_status": "P93_CONTROLLED_QUEUE_WRITE_VALIDATED",
    "decision_status": "REVIEW_REQUIRED",
    "risk_guard": "HUMAN_REVIEW_ONLY_NO_BROKER_NO_ORDER_NO_SIZING",
    "source_trace": "chatgpt_connector|GO_P93_CONTROLLED_QUEUE_WRITE|target=JOURNAL_APPEND_QUEUE|row=9",
    "sheet_write_executed": True,
    "direct_decision_journal_write": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker_execution": False,
    "order_execution": False,
    "auto_sizing_execution": False,
}


def build_p93_controlled_queue_write_evidence() -> dict[str, Any]:
    return dict(P93_CONTROLLED_QUEUE_WRITE_ROW)


def assert_p93_controlled_queue_write_safe(payload: dict[str, Any]) -> None:
    if payload["sheet_write_executed"] is not True:
        raise ValueError("P93 controlled queue write was not executed")
    if payload["sheet_name"] != "📤 JOURNAL_APPEND_QUEUE":
        raise ValueError("Unexpected P93 target sheet")
    if payload["range"] != "A9:Z9":
        raise ValueError("Unexpected P93 range")
    if payload["human_review_decision"] != "DO_NOT_APPEND":
        raise ValueError("P93 row must remain DO_NOT_APPEND")
    if payload["safe_to_append"] != "NO":
        raise ValueError("P93 row safe_to_append must be NO")
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
        raise ValueError(f"Unsafe P93 flags enabled: {enabled}")


def render_p93_controlled_queue_write_markdown(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# MVP QAIC — P93 Controlled Queue Write Evidence",
            "",
            f"- status: `{payload['status']}`",
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
            "- controlled queue write only",
            "- direct Decision Journal write: false",
            "- Apps Script execution: false",
            "- CLASP push: false",
            "- broker/order/sizing: false",
            "",
            "## Next",
            "",
            "`P94_APPROVE_APPEND_GATE_OR_WRITE_PIPELINE_RELEASE`",
            "",
        ]
    )


def export_p93_controlled_queue_write_evidence(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_p93_controlled_queue_write_evidence()
    assert_p93_controlled_queue_write_safe(payload)
    markdown = render_p93_controlled_queue_write_markdown(payload)
    json_path = target / "P93_CONTROLLED_QUEUE_WRITE_EVIDENCE.json"
    md_path = target / "P93_CONTROLLED_QUEUE_WRITE_EVIDENCE.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "status": payload["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": "P94_APPROVE_APPEND_GATE_OR_WRITE_PIPELINE_RELEASE",
    }
