from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.release.mvp_freeze_release_handoff import build_mvp_freeze_release_handoff

P100A_STATUS = "OK_P100A_OPERATIONAL_COCKPIT_LIVE_WRITE_VERIFIED"
NEXT_STEP = "P100B_REAL_METRIC_READERS_FAST_FUSE_OR_OPERATOR_ACCEPTANCE_SMOKE"

P100A_OPERATIONAL_COCKPIT_WRITE: dict[str, Any] = {
    "step": "P100A_RUNTIME_COCKPIT_OPERATIONAL_REBUILD_LIVE_WRITE_FAST_FUSE",
    "status": P100A_STATUS,
    "spreadsheet_id": "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0",
    "target_sheet_name": "QAIC_RUNTIME_COCKPIT_VIEW",
    "target_sheet_id": 987650321,
    "target_range": "QAIC_RUNTIME_COCKPIT_VIEW!A1:J40",
    "verified_range": "QAIC_RUNTIME_COCKPIT_VIEW!A1:J30",
    "run_id": "P100A-OP-REBUILD-20260621-231000",
    "write_mode": "LIVE_WRITE_FAST_FUSE",
    "operator_intent": "replace weak static cockpit with operational decision page",
    "status_cell": "FROZEN_READY_FOR_OPERATOR_ACCEPTANCE",
    "card_count": 17,
    "row_count_verified": 23,
    "operational_sections": [
        "decision_now",
        "mvp_state",
        "live_writes_done",
        "safety_lock",
        "workflow_journal",
        "queue_control",
        "benchmark_ai_trade",
        "prompt_quality",
        "prompt_improvement",
        "prompt_library",
        "lexique",
        "methods",
        "signals",
        "risk_guards",
        "portfolio_context",
        "revolut_x_readonly",
        "operator_acceptance",
        "backlog_selector",
    ],
    "write_result": {
        "sheet_created_or_updated": True,
        "sheet_view_write_executed": True,
        "old_static_rows_cleared": True,
        "readback_verified": True,
        "decision_bar_present": True,
        "action_now_present": True,
        "real_metric_gaps_declared": True,
    },
    "next_real_work": [
        "P100B read benchmark pass/fail counts",
        "P100B read prompt quality blockers and missing data",
        "P100B read lexique/method/signal/risk readiness counts",
        "operator acceptance smoke",
    ],
    "decision_journal_write_in_p100a": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker_execution": False,
    "order_execution": False,
    "auto_sizing_execution": False,
    "trading_action": False,
}


def build_p100a_operational_cockpit_live_write_evidence() -> dict[str, Any]:
    p99 = build_mvp_freeze_release_handoff()
    payload = dict(P100A_OPERATIONAL_COCKPIT_WRITE)
    payload["created_at"] = datetime.now(timezone.utc).isoformat()
    payload["source_p99_status"] = p99.get("status")
    payload["source_p99_release_artifacts"] = p99.get("release_artifacts")
    payload["next"] = NEXT_STEP
    return payload


def assert_p100a_operational_cockpit_live_write_safe(payload: dict[str, Any]) -> None:
    if payload["status"] != P100A_STATUS:
        raise ValueError(f"P100A evidence not OK: {payload['status']}")
    if payload["source_p99_status"] != "OK_P99_MVP_FREEZE_RELEASE_HANDOFF_READY":
        raise ValueError("P100A requires P99 freeze source status")
    if payload["target_sheet_name"] != "QAIC_RUNTIME_COCKPIT_VIEW":
        raise ValueError("Unexpected P100A target sheet")
    if payload["target_range"] != "QAIC_RUNTIME_COCKPIT_VIEW!A1:J40":
        raise ValueError("Unexpected P100A target range")
    if payload["card_count"] != 17:
        raise ValueError("P100A must evidence all 17 cockpit cards")
    result = payload["write_result"]
    required_true = (
        "sheet_created_or_updated",
        "sheet_view_write_executed",
        "old_static_rows_cleared",
        "readback_verified",
        "decision_bar_present",
        "action_now_present",
        "real_metric_gaps_declared",
    )
    missing = [flag for flag in required_true if result.get(flag) is not True]
    if missing:
        raise ValueError(f"P100A missing write evidence flags: {missing}")
    if payload["decision_journal_write_in_p100a"] is not False:
        raise ValueError("P100A must not write Decision Journal")
    expected_false = (
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
        "trading_action",
    )
    enabled = [flag for flag in expected_false if payload.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe P100A flags enabled: {enabled}")


def render_p100a_operational_cockpit_live_write_markdown(payload: dict[str, Any]) -> str:
    sections = [f"- `{item}`" for item in payload["operational_sections"]]
    next_work = [f"- {item}" for item in payload["next_real_work"]]
    return "\n".join(
        [
            "# MVP QAIC - P100A Operational Cockpit Live Write Evidence",
            "",
            f"- status: `{payload['status']}`",
            f"- source_p99_status: `{payload['source_p99_status']}`",
            f"- target_sheet_name: `{payload['target_sheet_name']}`",
            f"- target_range: `{payload['target_range']}`",
            f"- run_id: `{payload['run_id']}`",
            f"- next: `{payload['next']}`",
            "",
            "## Operational sections written",
            "",
            *sections,
            "",
            "## Next real work",
            "",
            *next_work,
            "",
            "## Safety",
            "",
            "- live Sheet cockpit view write only",
            "- no Decision Journal write in P100A",
            "- no Apps Script execution",
            "- no CLASP push",
            "- no broker/order/sizing",
            "",
        ]
    )


def export_p100a_operational_cockpit_live_write_evidence(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_p100a_operational_cockpit_live_write_evidence()
    assert_p100a_operational_cockpit_live_write_safe(payload)
    markdown = render_p100a_operational_cockpit_live_write_markdown(payload)
    json_path = target / "P100A_OPERATIONAL_COCKPIT_LIVE_WRITE_EVIDENCE.json"
    md_path = target / "P100A_OPERATIONAL_COCKPIT_LIVE_WRITE_EVIDENCE.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "status": payload["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": payload["next"],
    }
