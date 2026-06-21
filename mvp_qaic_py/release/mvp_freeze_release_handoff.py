from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.release.cockpit_sheets_live_write_evidence import (
    build_p98g_cockpit_sheets_live_write_evidence,
)

P99_STATUS = "OK_P99_MVP_FREEZE_RELEASE_HANDOFF_READY"
NEXT_STEP = "POST_P99_OPERATOR_ACCEPTANCE_OR_P100_BACKLOG_SELECTOR"

RELEASE_CHAIN: tuple[dict[str, str], ...] = (
    {"step": "P91", "name": "live write smoke evidence", "status": "SEALED"},
    {"step": "P92", "name": "write pipeline control", "status": "SEALED"},
    {"step": "P93/P93R3", "name": "controlled queue write evidence", "status": "SEALED"},
    {"step": "P94/P94R2", "name": "approve append gate", "status": "SEALED"},
    {"step": "P95", "name": "live approve append flip evidence", "status": "SEALED"},
    {"step": "P96A", "name": "journal append dryrun", "status": "SEALED"},
    {"step": "P96B", "name": "live journal append evidence", "status": "SEALED"},
    {"step": "P97", "name": "live workflow release seal", "status": "SEALED"},
    {"step": "P98A", "name": "runtime cockpit audit readonly", "status": "SEALED"},
    {"step": "P98B", "name": "runtime cockpit module local", "status": "SEALED"},
    {"step": "P98C", "name": "extended cockpit scope audit readonly", "status": "SEALED"},
    {"step": "P98D", "name": "runtime cockpit extended module local", "status": "SEALED"},
    {"step": "P98E-R1", "name": "cockpit UI export repair", "status": "SEALED_VALID_REFERENCE"},
    {"step": "P98F", "name": "cockpit sheets view dryrun", "status": "SEALED"},
    {"step": "P98G", "name": "cockpit sheets live write evidence", "status": "SEALED"},
)


def build_mvp_freeze_release_handoff() -> dict[str, Any]:
    p98g = build_p98g_cockpit_sheets_live_write_evidence()
    blockers: list[str] = []
    if p98g.get("status") != "OK_P98G_COCKPIT_SHEETS_LIVE_WRITE_VERIFIED":
        blockers.append("P98G_COCKPIT_SHEETS_LIVE_WRITE_NOT_VERIFIED")
    if p98g.get("target_sheet_name") != "QAIC_RUNTIME_COCKPIT_VIEW":
        blockers.append("P98G_COCKPIT_VIEW_TARGET_MISMATCH")
    if p98g.get("card_count") != 17:
        blockers.append("P98G_CARD_COUNT_MISMATCH")
    release_artifacts = {
        "google_sheet": "MVP QAIC Crypto Signal OS DEV",
        "spreadsheet_id": "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0",
        "cockpit_sheet": "QAIC_RUNTIME_COCKPIT_VIEW",
        "cockpit_range": "QAIC_RUNTIME_COCKPIT_VIEW!A1:H24",
        "decision_journal_range": "DECISION_JOURNAL!BJ17:CN17",
        "journal_queue_range": "JOURNAL_APPEND_QUEUE!A9:Z9",
        "repo_branch": "master",
        "p98g_reference": p98g.get("run_id"),
    }
    operator_handoff = {
        "mvp_status": "FROZEN_READY_FOR_OPERATOR_ACCEPTANCE",
        "tool_mode": "HUMAN_REVIEW_ONLY_DECISION_SUPPORT",
        "what_is_ready": [
            "live journal append workflow P91-P97",
            "extended cockpit scope P98A-P98G",
            "Google Sheets cockpit view QAIC_RUNTIME_COCKPIT_VIEW",
            "local Python evidence and tests",
            "GitHub remote commit/tag chain",
        ],
        "what_remains_after_freeze": [
            "operator acceptance smoke",
            "optional cockpit styling hardening",
            "future metric readers for benchmark and quality sheets",
            "future P100 backlog selector",
        ],
    }
    safety = {
        "freeze_handoff_only": True,
        "live_write_executed_in_p99": False,
        "decision_journal_write_in_p99": False,
        "sheet_write_in_p99": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "trading_action": False,
    }
    status = P99_STATUS if not blockers else "BLOCKED_P99_MVP_FREEZE_RELEASE_HANDOFF"
    return {
        "step": "P99_MVP_FREEZE_RELEASE_HANDOFF",
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "release_chain_count": len(RELEASE_CHAIN),
        "release_chain": list(RELEASE_CHAIN),
        "release_artifacts": release_artifacts,
        "operator_handoff": operator_handoff,
        "source_p98g_status": p98g.get("status"),
        "safety": safety,
        "blockers": blockers,
        "next": NEXT_STEP if not blockers else "FIX_BLOCKERS_BEFORE_FREEZE",
    }


def assert_mvp_freeze_release_handoff_safe(payload: dict[str, Any]) -> None:
    if payload["status"] != P99_STATUS:
        raise ValueError(f"P99 handoff not OK: {payload['status']}")
    if payload["blockers"]:
        raise ValueError(f"P99 blockers present: {payload['blockers']}")
    if payload["release_chain_count"] != 15:
        raise ValueError("P99 must freeze the full P91-P98G chain")
    if payload["source_p98g_status"] != "OK_P98G_COCKPIT_SHEETS_LIVE_WRITE_VERIFIED":
        raise ValueError("P99 requires P98G verified source status")
    safety = payload["safety"]
    expected_false = (
        "live_write_executed_in_p99",
        "decision_journal_write_in_p99",
        "sheet_write_in_p99",
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
        "trading_action",
    )
    enabled = [flag for flag in expected_false if safety.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe P99 flags enabled: {enabled}")
    if safety.get("freeze_handoff_only") is not True:
        raise ValueError("P99 must remain freeze handoff only")


def render_mvp_freeze_release_handoff_markdown(payload: dict[str, Any]) -> str:
    chain_lines = [
        f"- `{item['step']}` - {item['name']} - `{item['status']}`"
        for item in payload["release_chain"]
    ]
    ready_lines = [f"- {item}" for item in payload["operator_handoff"]["what_is_ready"]]
    remains_lines = [
        f"- {item}" for item in payload["operator_handoff"]["what_remains_after_freeze"]
    ]
    artifacts = payload["release_artifacts"]
    return "\n".join(
        [
            "# MVP QAIC - P99 MVP Freeze Release Handoff",
            "",
            f"- status: `{payload['status']}`",
            f"- source_p98g_status: `{payload['source_p98g_status']}`",
            f"- release_chain_count: `{payload['release_chain_count']}`",
            f"- next: `{payload['next']}`",
            "",
            "## Release artifacts",
            "",
            f"- Google Sheet: `{artifacts['google_sheet']}`",
            f"- Cockpit Sheet: `{artifacts['cockpit_sheet']}`",
            f"- Cockpit Range: `{artifacts['cockpit_range']}`",
            f"- Decision Journal Range: `{artifacts['decision_journal_range']}`",
            f"- Journal Queue Range: `{artifacts['journal_queue_range']}`",
            "",
            "## Frozen chain",
            "",
            *chain_lines,
            "",
            "## Ready for operator",
            "",
            *ready_lines,
            "",
            "## After freeze",
            "",
            *remains_lines,
            "",
            "## Safety",
            "",
            "- freeze handoff only",
            "- no live write in P99",
            "- no Decision Journal write in P99",
            "- no Sheet write in P99",
            "- no Apps Script execution",
            "- no CLASP push",
            "- no broker/order/sizing",
            "",
        ]
    )


def export_mvp_freeze_release_handoff(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_mvp_freeze_release_handoff()
    assert_mvp_freeze_release_handoff_safe(payload)
    markdown = render_mvp_freeze_release_handoff_markdown(payload)
    json_path = target / "P99_MVP_FREEZE_RELEASE_HANDOFF.json"
    md_path = target / "P99_MVP_FREEZE_RELEASE_HANDOFF.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "status": payload["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": payload["next"],
    }
