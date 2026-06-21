from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.bridge.local_bridge_dryrun import LIVE_AVAILABLE_TABS, LIVE_HEADERS
from mvp_qaic_py.contracts.sheets_live_contract import (
    SPREADSHEET_ID,
    SPREADSHEET_TITLE,
    validate_p81r_p82_contract,
)
from mvp_qaic_py.release.operator_release_pack import build_operator_release_pack

DEFAULT_READONLY_RANGES: tuple[str, ...] = (
    "GPT_INPUT_PAYLOADS!A1:M2",
    "'🚀 PROMPT_RUN_QUEUE'!A1:I3",
    "'📥 RESPONSE_INTAKE_QUEUE'!A1:I3",
    "'📤 JOURNAL_APPEND_QUEUE'!A1:I3",
    "QAIC_RUNTIME_BRIDGE_STATUS!A1:N3",
)


def build_sheets_readonly_connector_dryrun(
    *,
    ranges: tuple[str, ...] = DEFAULT_READONLY_RANGES,
    spreadsheet_id: str = SPREADSHEET_ID,
    write_requested: bool = False,
) -> dict[str, Any]:
    contract = validate_p81r_p82_contract(LIVE_AVAILABLE_TABS, LIVE_HEADERS)
    release = build_operator_release_pack()
    unknown_ranges = [item for item in ranges if item not in DEFAULT_READONLY_RANGES]
    id_ok = spreadsheet_id == SPREADSHEET_ID
    contract_ok = contract["status"] == "OK_P81R_P82_LIVE_SHEETS_CONTRACT_READY"
    release_ok = release["status"] == "OK_P87_OPERATOR_RELEASE_PACK_READY"

    blocked = bool(
        write_requested or unknown_ranges or not id_ok or not contract_ok or not release_ok
    )
    status = (
        "OK_P88_SHEETS_READONLY_CONNECTOR_DRYRUN_READY"
        if not blocked
        else "BLOCKED_P88_SHEETS_READONLY_CONNECTOR_DRYRUN"
    )

    range_plan = [
        {
            "range": item,
            "mode": "READ_ONLY_DRYRUN",
            "google_api_call": False,
            "sheet_write": False,
            "status": "READY" if item not in unknown_ranges else "BLOCKED_UNKNOWN_RANGE",
        }
        for item in ranges
    ]

    return {
        "step": "P88_SHEETS_READONLY_CONNECTOR_DRYRUN_FAST_FUSE",
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "spreadsheet_id": spreadsheet_id,
        "spreadsheet_title": SPREADSHEET_TITLE,
        "contract_status": contract["status"],
        "release_status": release["status"],
        "requested_range_count": len(ranges),
        "unknown_range_count": len(unknown_ranges),
        "unknown_ranges": unknown_ranges,
        "range_plan": range_plan,
        "write_requested": write_requested,
        "sheet_write": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "google_rest_local_diag": False,
        "live_google_api_call": False,
        "next": "P89_SHEETS_READONLY_CONNECTOR_IMPLEMENTATION_DECISION_OR_STOP_MVP_LOCAL_SEAL",
    }


def assert_sheets_readonly_connector_dryrun_safe(payload: dict[str, Any]) -> None:
    unsafe_flags = (
        "sheet_write",
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
        "google_rest_local_diag",
        "live_google_api_call",
        "write_requested",
    )
    enabled = [flag for flag in unsafe_flags if payload.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe P88 flags enabled: {enabled}")
    if payload["unknown_range_count"] != 0:
        raise ValueError(f"Unknown ranges blocked: {payload['unknown_ranges']}")


def render_sheets_readonly_connector_dryrun_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# MVP QAIC — P88 Sheets Readonly Connector Dry-Run",
        "",
        f"- status: `{payload['status']}`",
        f"- spreadsheet_id: `{payload['spreadsheet_id']}`",
        f"- contract_status: `{payload['contract_status']}`",
        f"- release_status: `{payload['release_status']}`",
        f"- requested_range_count: `{payload['requested_range_count']}`",
        f"- unknown_range_count: `{payload['unknown_range_count']}`",
        "",
        "## Safety",
        "",
        "- NO_SHEET_WRITE",
        "- NO_APPS_SCRIPT_EXECUTION",
        "- NO_CLASP_PUSH",
        "- NO_BROKER_ORDER_SIZING",
        "- NO_GOOGLE_REST_LOCAL_DIAG",
        "- NO_LIVE_GOOGLE_API_CALL",
        "",
        "## Ranges",
        "",
        "| range | mode | status |",
        "|---|---|---|",
    ]
    for item in payload["range_plan"]:
        lines.append(f"| {item['range']} | {item['mode']} | {item['status']} |")
    lines.extend(["", "## Next", "", f"`{payload['next']}`", ""])
    return "\n".join(lines)


def export_sheets_readonly_connector_dryrun(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_sheets_readonly_connector_dryrun()
    assert_sheets_readonly_connector_dryrun_safe(payload)
    markdown = render_sheets_readonly_connector_dryrun_markdown(payload)
    json_path = target / "P88_SHEETS_READONLY_CONNECTOR_DRYRUN.json"
    md_path = target / "P88_SHEETS_READONLY_CONNECTOR_DRYRUN.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "status": payload["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": payload["next"],
    }
