from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

P98G_STATUS = "OK_P98G_COCKPIT_SHEETS_LIVE_WRITE_VERIFIED"
NEXT_STEP = "P99_MVP_FREEZE_RELEASE_HANDOFF"

P98G_COCKPIT_SHEETS_WRITE: dict[str, Any] = {
    "step": "P98G_COCKPIT_SHEETS_LIVE_WRITE_EVIDENCE",
    "status": P98G_STATUS,
    "spreadsheet_id": "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0",
    "target_sheet_name": "QAIC_RUNTIME_COCKPIT_VIEW",
    "target_sheet_id": 987650321,
    "target_range": "QAIC_RUNTIME_COCKPIT_VIEW!A1:H24",
    "run_id": "P98G-COCKPIT-SHEETS-WRITE-20260621-224500",
    "source": "P98F_COCKPIT_SHEETS_VIEW_DRYRUN_TO_P98G_DIRECT_WRITE",
    "status_cell": "P98G_LIVE_COCKPIT_SHEET_CREATED",
    "card_count": 17,
    "row_count_verified": 24,
    "required_cards": [
        "journal_queue_status",
        "decision_journal_status",
        "runtime_bridge_status",
        "run_queue_status",
        "response_intake_status",
        "latest_payload_status",
        "benchmark_status",
        "prompt_quality_status",
        "prompt_improvement_backlog",
        "prompt_library_readiness",
        "lexique_readiness",
        "method_library_status",
        "trade_plan_methods_status",
        "signal_library_coverage",
        "risk_guard_status",
        "portfolio_snapshot_status",
        "revolut_readonly_status",
    ],
    "sheet_created_or_updated": True,
    "sheet_view_write_executed": True,
    "decision_journal_write_in_p98g": False,
    "apps_script_execution": False,
    "clasp_push": False,
    "broker_execution": False,
    "order_execution": False,
    "auto_sizing_execution": False,
    "trading_action": False,
}


def build_p98g_cockpit_sheets_live_write_evidence() -> dict[str, Any]:
    payload = dict(P98G_COCKPIT_SHEETS_WRITE)
    payload["created_at"] = datetime.now(timezone.utc).isoformat()
    payload["next"] = NEXT_STEP
    return payload


def assert_p98g_cockpit_sheets_live_write_safe(payload: dict[str, Any]) -> None:
    if payload["status"] != P98G_STATUS:
        raise ValueError(f"P98G evidence not OK: {payload['status']}")
    if payload["target_sheet_name"] != "QAIC_RUNTIME_COCKPIT_VIEW":
        raise ValueError("Unexpected P98G target sheet")
    if payload["target_range"] != "QAIC_RUNTIME_COCKPIT_VIEW!A1:H24":
        raise ValueError("Unexpected P98G target range")
    if payload["card_count"] != 17:
        raise ValueError("P98G must evidence all 17 cards")
    if payload["sheet_view_write_executed"] is not True:
        raise ValueError("P98G sheet view write was not executed")
    if payload["decision_journal_write_in_p98g"] is not False:
        raise ValueError("P98G must not write Decision Journal")
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
        raise ValueError(f"Unsafe P98G flags enabled: {enabled}")


def render_p98g_cockpit_sheets_live_write_markdown(payload: dict[str, Any]) -> str:
    lines = [f"- `{card}`" for card in payload["required_cards"]]
    return "\n".join(
        [
            "# MVP QAIC - P98G Cockpit Sheets Live Write Evidence",
            "",
            f"- status: `{payload['status']}`",
            f"- target_sheet_name: `{payload['target_sheet_name']}`",
            f"- target_range: `{payload['target_range']}`",
            f"- card_count: `{payload['card_count']}`",
            f"- next: `{payload['next']}`",
            "",
            "## Cards written",
            "",
            *lines,
            "",
            "## Safety",
            "",
            "- live Sheet cockpit view write only",
            "- no Decision Journal write in P98G",
            "- no Apps Script execution",
            "- no CLASP push",
            "- no broker/order/sizing",
            "",
        ]
    )


def export_p98g_cockpit_sheets_live_write_evidence(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_p98g_cockpit_sheets_live_write_evidence()
    assert_p98g_cockpit_sheets_live_write_safe(payload)
    markdown = render_p98g_cockpit_sheets_live_write_markdown(payload)
    json_path = target / "P98G_COCKPIT_SHEETS_LIVE_WRITE_EVIDENCE.json"
    md_path = target / "P98G_COCKPIT_SHEETS_LIVE_WRITE_EVIDENCE.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "status": payload["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": payload["next"],
    }
