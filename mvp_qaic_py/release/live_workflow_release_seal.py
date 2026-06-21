from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.sheets.approve_append_flip_evidence import (
    build_p95_live_approve_append_flip_evidence,
)
from mvp_qaic_py.sheets.approve_append_gate import build_approve_append_gate
from mvp_qaic_py.sheets.controlled_queue_write_evidence import (
    build_p93_controlled_queue_write_evidence,
)
from mvp_qaic_py.sheets.decision_journal_append_evidence import (
    build_p96b_live_journal_append_evidence,
)
from mvp_qaic_py.sheets.journal_append_dryrun import build_journal_append_dryrun
from mvp_qaic_py.sheets.live_write_smoke_evidence import (
    build_p91_live_write_smoke_evidence,
)
from mvp_qaic_py.sheets.write_pipeline_control import build_write_pipeline_control

RELEASE_STATUS = "OK_P97_LIVE_WORKFLOW_RELEASE_SEALED"
NEXT_STEP = "P98_RUNTIME_COCKPIT_AUDIT_OR_MVP_FREEZE"


def _status_from(payload: dict[str, Any]) -> str:
    return str(payload.get("status", "UNKNOWN"))


def build_live_workflow_release_seal() -> dict[str, Any]:
    p91 = build_p91_live_write_smoke_evidence()
    p92 = build_write_pipeline_control()
    p93 = build_p93_controlled_queue_write_evidence()
    p94 = build_approve_append_gate()
    p95 = build_p95_live_approve_append_flip_evidence()
    p96a = build_journal_append_dryrun()
    p96b = build_p96b_live_journal_append_evidence()

    steps = [
        {
            "step": "P91",
            "status": _status_from(p91),
            "scope": "live queue smoke row",
        },
        {
            "step": "P92",
            "status": _status_from(p92),
            "scope": "write pipeline control",
        },
        {
            "step": "P93",
            "status": _status_from(p93),
            "scope": "controlled queue row write",
        },
        {
            "step": "P94",
            "status": _status_from(p94),
            "scope": "approve append local gate",
        },
        {
            "step": "P95",
            "status": _status_from(p95),
            "scope": "queue approval flip",
        },
        {
            "step": "P96A",
            "status": _status_from(p96a),
            "scope": "journal append dry-run",
        },
        {
            "step": "P96B",
            "status": _status_from(p96b),
            "scope": "live Decision Journal append evidence",
        },
    ]

    blockers: list[str] = []
    if p96b.get("journal_id") != "DJ-P96B-P93-CQW-20260621-200001":
        blockers.append("P96B_JOURNAL_ID_MISMATCH")
    if p96b.get("queue_append_status_after") != "APPENDED_TO_DECISION_JOURNAL":
        blockers.append("QUEUE_NOT_MARKED_APPENDED")
    if p96b.get("decision_journal_range") != "BJ17:CN17":
        blockers.append("DECISION_JOURNAL_RANGE_MISMATCH")
    if p95.get("safe_to_append") != "YES":
        blockers.append("P95_SAFE_TO_APPEND_NOT_YES")
    if p94.get("sheet_write_executed") is not False:
        blockers.append("P94_MUST_REMAIN_LOCAL_ONLY")
    if p96a.get("decision_journal_write") is not False:
        blockers.append("P96A_MUST_REMAIN_DRYRUN_ONLY")

    safety = {
        "live_write_already_completed": True,
        "no_additional_live_write_in_p97": True,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "trading_action": False,
    }

    status = RELEASE_STATUS if not blockers else "BLOCKED_P97_LIVE_WORKFLOW_RELEASE_SEAL"

    return {
        "step": "P97_LIVE_WORKFLOW_RELEASE_SEAL",
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sealed_range": "P91_TO_P96B",
        "decision_journal_row": "🧾 DECISION_JOURNAL!BJ17:CN17",
        "queue_row": "📤 JOURNAL_APPEND_QUEUE!A9:Z9",
        "journal_id": p96b.get("journal_id"),
        "journal_queue_id": p96b.get("journal_queue_id"),
        "steps": steps,
        "safety": safety,
        "blockers": blockers,
        "next": NEXT_STEP if not blockers else "FIX_BLOCKERS_BEFORE_P98",
    }


def assert_live_workflow_release_seal_safe(payload: dict[str, Any]) -> None:
    if payload["status"] != RELEASE_STATUS:
        raise ValueError(f"P97 release seal not OK: {payload['status']}")
    if payload["blockers"]:
        raise ValueError(f"P97 blockers present: {payload['blockers']}")

    safety = payload["safety"]
    if safety["no_additional_live_write_in_p97"] is not True:
        raise ValueError("P97 must not execute additional live write")

    forbidden = (
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
        "trading_action",
    )
    enabled = [flag for flag in forbidden if safety.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe P97 flags enabled: {enabled}")


def render_live_workflow_release_seal_markdown(payload: dict[str, Any]) -> str:
    step_lines = [
        f"- {item['step']}: `{item['status']}` — {item['scope']}" for item in payload["steps"]
    ]
    return "\n".join(
        [
            "# MVP QAIC — P97 Live Workflow Release Seal",
            "",
            f"- status: `{payload['status']}`",
            f"- sealed_range: `{payload['sealed_range']}`",
            f"- decision_journal_row: `{payload['decision_journal_row']}`",
            f"- queue_row: `{payload['queue_row']}`",
            f"- journal_id: `{payload['journal_id']}`",
            f"- journal_queue_id: `{payload['journal_queue_id']}`",
            "",
            "## Sealed steps",
            "",
            *step_lines,
            "",
            "## Safety",
            "",
            "- no additional live write in P97",
            "- no Apps Script execution",
            "- no CLASP push",
            "- no broker/order/sizing",
            "- audit journal only; no trading action",
            "",
            "## Next",
            "",
            f"`{payload['next']}`",
            "",
        ]
    )


def export_live_workflow_release_seal(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_live_workflow_release_seal()
    assert_live_workflow_release_seal_safe(payload)
    markdown = render_live_workflow_release_seal_markdown(payload)
    json_path = target / "P97_LIVE_WORKFLOW_RELEASE_SEAL.json"
    md_path = target / "P97_LIVE_WORKFLOW_RELEASE_SEAL.md"
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
