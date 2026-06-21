from __future__ import annotations

import json
from pathlib import Path
from typing import Any

P96B_LIVE_JOURNAL_APPEND_ROW: dict[str, Any] = {
    "step": "P96B_LIVE_JOURNAL_APPEND",
    "status": "OK_P96B_LIVE_JOURNAL_APPEND_VERIFIED",
    "spreadsheet_id": "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0",
    "decision_journal_sheet": "🧾 DECISION_JOURNAL",
    "decision_journal_range": "BJ17:CN17",
    "decision_journal_row_number": 17,
    "queue_sheet": "📤 JOURNAL_APPEND_QUEUE",
    "queue_range": "A9:Z9",
    "queue_row_number": 9,
    "decision_id": "P96B-P93-CQW-20260621-200001",
    "journal_id": "DJ-P96B-P93-CQW-20260621-200001",
    "journal_queue_id": "P93-CQW-20260621-200001",
    "timestamp": "2026-06-21T21:20:00+02:00",
    "prompt_used": "P96B_JOURNAL_APPEND_FROM_QUEUE_A9",
    "asset": "MVP_QAIC_RUNTIME",
    "scenario": "P96B_LIVE_JOURNAL_APPEND",
    "decision_status": "APPROVED_FOR_APPEND_GATE",
    "data_quality": "PASS",
    "missing_data": "NONE_FOR_APPEND_GATE",
    "final_human_decision": "APPROVE_APPEND",
    "source": "📤 JOURNAL_APPEND_QUEUE!A9:Z9",
    "run_id": "P96B-APPEND-20260621-212000",
    "validation_status": "P96B_LIVE_JOURNAL_APPEND_VALIDATED",
    "created_at": "2026-06-21T21:20:00+02:00",
    "payload_id": "P93-CONTROLLED-PAYLOAD",
    "prompt_id": "p93_controlled_queue_write",
    "gpt_response_audit_status": "P96B_APPEND_EVIDENCE_FROM_APPROVED_QUEUE",
    "analysis_level": "JOURNAL_APPEND_EVIDENCE",
    "human_final_decision": "APPROVE_APPEND",
    "signals_summary": "P95 approved append gate; source row safe_to_append=YES",
    "blockers": "NONE",
    "notes": "P96B controlled journal append. No broker/order/sizing. Source queue row A9.",
    "signal_id": "NONE",
    "score_id": "NONE",
    "risk_guard": "HUMAN_REVIEW_ONLY_NO_BROKER_NO_ORDER_NO_SIZING",
    "raw_response": (
        "P96B live journal append from approved queue row. Audit journal only; no trading action."
    ),
    "human_review_note": ("GO_P96B_LIVE_JOURNAL_APPEND received; source queue row A9 approved."),
    "payload_hash": "P96B-HASH-NA",
    "version": "MVP_QAIC_P96B_LIVE_JOURNAL_APPEND_0.1.0_CONTROLLED_SAFE",
    "safety": ("HUMAN_REVIEW_ONLY | NO_BROKER | NO_ORDER | NO_SIZING | NO_APPS_SCRIPT | NO_CLASP"),
    "queue_append_status_after": "APPENDED_TO_DECISION_JOURNAL",
    "queue_append_run_id_after": "P96B-APPEND-20260621-212000",
    "queue_journal_id_after": "DJ-P96B-P93-CQW-20260621-200001",
    "sheet_write_executed": True,
    "decision_journal_write": True,
    "journal_append_executed": True,
    "queue_status_updated": True,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker_execution": False,
    "order_execution": False,
    "auto_sizing_execution": False,
}


def build_p96b_live_journal_append_evidence() -> dict[str, Any]:
    return dict(P96B_LIVE_JOURNAL_APPEND_ROW)


def assert_p96b_live_journal_append_safe(payload: dict[str, Any]) -> None:
    if payload["sheet_write_executed"] is not True:
        raise ValueError("P96B live sheet write was not executed")
    if payload["decision_journal_write"] is not True:
        raise ValueError("P96B Decision Journal write was not executed")
    if payload["journal_append_executed"] is not True:
        raise ValueError("P96B journal append was not executed")
    if payload["queue_status_updated"] is not True:
        raise ValueError("P96B queue status was not updated")
    if payload["decision_journal_sheet"] != "🧾 DECISION_JOURNAL":
        raise ValueError("Unexpected P96B Decision Journal sheet")
    if payload["decision_journal_range"] != "BJ17:CN17":
        raise ValueError("Unexpected P96B Decision Journal range")
    if payload["queue_sheet"] != "📤 JOURNAL_APPEND_QUEUE":
        raise ValueError("Unexpected P96B queue sheet")
    if payload["queue_range"] != "A9:Z9":
        raise ValueError("Unexpected P96B queue range")
    if payload["final_human_decision"] != "APPROVE_APPEND":
        raise ValueError("P96B must be human-approved append")
    if payload["validation_status"] != "P96B_LIVE_JOURNAL_APPEND_VALIDATED":
        raise ValueError("Unexpected P96B validation status")
    if payload["blockers"] != "NONE":
        raise ValueError("P96B append blockers must be NONE")
    forbidden = (
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
    )
    enabled = [flag for flag in forbidden if payload.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe P96B flags enabled: {enabled}")


def render_p96b_live_journal_append_markdown(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# MVP QAIC — P96B Live Journal Append Evidence",
            "",
            f"- status: `{payload['status']}`",
            f"- decision_journal_range: `{payload['decision_journal_range']}`",
            f"- queue_range: `{payload['queue_range']}`",
            f"- journal_id: `{payload['journal_id']}`",
            f"- journal_queue_id: `{payload['journal_queue_id']}`",
            f"- final_human_decision: `{payload['final_human_decision']}`",
            f"- validation_status: `{payload['validation_status']}`",
            f"- queue_append_status_after: `{payload['queue_append_status_after']}`",
            "",
            "## Safety",
            "",
            "- controlled Decision Journal append only",
            "- no Apps Script execution",
            "- no CLASP push",
            "- no broker/order/sizing",
            "- audit journal only; no trading action",
            "",
            "## Next",
            "",
            "`P97_RELEASE_SEAL_OR_RUNTIME_COCKPIT_AUDIT`",
            "",
        ]
    )


def export_p96b_live_journal_append_evidence(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_p96b_live_journal_append_evidence()
    assert_p96b_live_journal_append_safe(payload)
    markdown = render_p96b_live_journal_append_markdown(payload)
    json_path = target / "P96B_LIVE_JOURNAL_APPEND_EVIDENCE.json"
    md_path = target / "P96B_LIVE_JOURNAL_APPEND_EVIDENCE.md"
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "status": payload["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": "P97_RELEASE_SEAL_OR_RUNTIME_COCKPIT_AUDIT",
    }
