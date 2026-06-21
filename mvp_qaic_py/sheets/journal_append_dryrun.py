from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.sheets.approve_append_flip_evidence import (
    build_p95_live_approve_append_flip_evidence,
)

JOURNAL_APPEND_QUEUE = "📤 JOURNAL_APPEND_QUEUE"
DECISION_JOURNAL = "🧾 DECISION_JOURNAL"
P96A_APPROVAL_TOKEN = "P96A_DRYRUN_ONLY"


def _build_journal_record(queue_row: dict[str, Any]) -> dict[str, Any]:
    return {
        "journal_id": "DJ-DRYRUN-P93-CQW-20260621-200001",
        "journal_queue_id": queue_row["journal_queue_id"],
        "source_range": queue_row["range"],
        "source_sheet": queue_row["sheet_name"],
        "decision_status": queue_row["decision_status"],
        "validation_status": queue_row["validation_status"],
        "human_final_decision": queue_row["human_final_decision"],
        "signal_id": queue_row.get("signal_id", "NONE"),
        "score_id": queue_row.get("score_id", "NONE"),
        "risk_guard": queue_row["risk_guard"],
        "missing_data": queue_row["missing_data"],
        "blockers": queue_row["blockers"],
        "append_status": "DRYRUN_READY_FOR_JOURNAL_APPEND",
        "source_trace": queue_row["source_trace"],
    }


def build_journal_append_dryrun(
    *,
    queue_row: dict[str, Any] | None = None,
    request_live_append: bool = False,
    approval_token: str | None = None,
) -> dict[str, Any]:
    row = queue_row or build_p95_live_approve_append_flip_evidence()
    blockers: list[str] = []

    if row.get("sheet_name") != JOURNAL_APPEND_QUEUE:
        blockers.append("SOURCE_NOT_JOURNAL_APPEND_QUEUE")
    if row.get("range") != "A9:Z9":
        blockers.append("UNEXPECTED_SOURCE_RANGE")
    if row.get("journal_queue_id") != "P93-CQW-20260621-200001":
        blockers.append("UNEXPECTED_QUEUE_ID")
    if row.get("human_review_decision") != "APPROVE_APPEND":
        blockers.append("APPROVE_APPEND_MISSING")
    if row.get("safe_to_append") != "YES":
        blockers.append("SAFE_TO_APPEND_NOT_YES")
    if row.get("append_status") != "APPROVE_APPEND_PENDING_JOURNAL_APPEND":
        blockers.append("QUEUE_NOT_PENDING_JOURNAL_APPEND")
    if row.get("validation_status") != "P95_APPROVE_APPEND_FLIP_VALIDATED":
        blockers.append("P95_VALIDATION_MISSING")
    if not row.get("risk_guard"):
        blockers.append("MISSING_RISK_GUARD")
    if row.get("journal_append_executed") is True:
        blockers.append("SOURCE_ALREADY_APPENDED")
    if request_live_append:
        blockers.append("LIVE_APPEND_NOT_ALLOWED_IN_P96A")

    approval_token_ok = approval_token == P96A_APPROVAL_TOKEN
    if request_live_append and not approval_token_ok:
        blockers.append("MISSING_P96A_DRYRUN_TOKEN")

    if blockers:
        status = "BLOCKED_P96A_JOURNAL_APPEND_DRYRUN"
        next_step = "FIX_BLOCKERS_BEFORE_P96B"
        journal_record: dict[str, Any] | None = None
    else:
        status = "OK_P96A_JOURNAL_APPEND_DRYRUN_READY_NO_LIVE_WRITE"
        next_step = "P96B_LIVE_JOURNAL_APPEND_AFTER_EXPLICIT_GO"
        journal_record = _build_journal_record(row)

    return {
        "step": "P96A_JOURNAL_APPEND_DRYRUN_LOCAL_FIRST",
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_sheet": row.get("sheet_name"),
        "source_range": row.get("range"),
        "journal_queue_id": row.get("journal_queue_id"),
        "target_sheet": DECISION_JOURNAL,
        "request_live_append": request_live_append,
        "approval_token_ok": approval_token_ok,
        "planned_append_status": "DRYRUN_READY_FOR_JOURNAL_APPEND",
        "journal_record": journal_record,
        "sheet_write_executed": False,
        "decision_journal_write": False,
        "journal_append_executed": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "blockers": blockers,
        "next": next_step,
    }


def assert_journal_append_dryrun_safe(payload: dict[str, Any]) -> None:
    if payload["sheet_write_executed"]:
        raise ValueError("P96A must not write to Sheets")
    if payload["decision_journal_write"]:
        raise ValueError("P96A must not write Decision Journal")
    if payload["journal_append_executed"]:
        raise ValueError("P96A must not append journal")
    forbidden = (
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
    )
    enabled = [flag for flag in forbidden if payload.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe P96A flags enabled: {enabled}")


def render_journal_append_dryrun_markdown(payload: dict[str, Any]) -> str:
    record = payload.get("journal_record") or {}
    return "\n".join(
        [
            "# MVP QAIC — P96A Journal Append Dryrun",
            "",
            f"- status: `{payload['status']}`",
            f"- source_sheet: `{payload['source_sheet']}`",
            f"- source_range: `{payload['source_range']}`",
            f"- journal_queue_id: `{payload['journal_queue_id']}`",
            f"- target_sheet: `{payload['target_sheet']}`",
            f"- planned_append_status: `{payload['planned_append_status']}`",
            f"- decision_journal_write: `{payload['decision_journal_write']}`",
            f"- journal_append_executed: `{payload['journal_append_executed']}`",
            f"- blockers: `{payload['blockers']}`",
            "",
            "## Dryrun journal record",
            "",
            f"- journal_id: `{record.get('journal_id')}`",
            f"- human_final_decision: `{record.get('human_final_decision')}`",
            f"- risk_guard: `{record.get('risk_guard')}`",
            f"- append_status: `{record.get('append_status')}`",
            "",
            "## Safety",
            "",
            "- dry-run only in P96A",
            "- no Decision Journal write",
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


def export_journal_append_dryrun(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_journal_append_dryrun()
    assert_journal_append_dryrun_safe(payload)
    markdown = render_journal_append_dryrun_markdown(payload)
    json_path = target / "P96A_JOURNAL_APPEND_DRYRUN.json"
    md_path = target / "P96A_JOURNAL_APPEND_DRYRUN.md"
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
