from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mvp_qaic_py.release.local_mvp_seal import build_local_mvp_seal
from mvp_qaic_py.sheets.readonly_connector_dryrun import (
    build_sheets_readonly_connector_dryrun,
)

WRITE_TARGET_ALLOWLIST: tuple[str, ...] = (
    "🚀 PROMPT_RUN_QUEUE",
    "📥 RESPONSE_INTAKE_QUEUE",
    "📤 JOURNAL_APPEND_QUEUE",
    "QAIC_RUNTIME_BRIDGE_STATUS",
)

BLOCKED_DIRECT_WRITE_TARGETS: tuple[str, ...] = (
    "🧾 DECISION_JOURNAL",
    "🎛️ BENCHMARK_AI_TRADE",
)

WRITE_OPERATIONS_ALLOWLIST: tuple[str, ...] = (
    "APPEND_ROW",
    "UPDATE_STATUS_CELL",
    "APPEND_REVIEW_EVENT",
)

APPROVAL_TOKEN = "APPROVE_P91_WRITE_SMOKE"


def build_sheets_write_capable_contract(
    *,
    target_sheet: str = "📤 JOURNAL_APPEND_QUEUE",
    operation: str = "APPEND_REVIEW_EVENT",
    write_enabled: bool = False,
    approval_token: str | None = None,
) -> dict[str, Any]:
    seal = build_local_mvp_seal()
    readonly = build_sheets_readonly_connector_dryrun()

    target_allowed = target_sheet in WRITE_TARGET_ALLOWLIST
    target_blocked = target_sheet in BLOCKED_DIRECT_WRITE_TARGETS
    operation_allowed = operation in WRITE_OPERATIONS_ALLOWLIST
    approval_ok = approval_token == APPROVAL_TOKEN

    blockers: list[str] = []
    if seal["status"] != "OK_P89_LOCAL_MVP_SEALED":
        blockers.append("LOCAL_MVP_NOT_SEALED")
    if readonly["status"] != "OK_P88_SHEETS_READONLY_CONNECTOR_DRYRUN_READY":
        blockers.append("READONLY_DRYRUN_NOT_READY")
    if target_blocked:
        blockers.append("DIRECT_TARGET_BLOCKED")
    if not target_allowed:
        blockers.append("TARGET_NOT_ALLOWLISTED")
    if not operation_allowed:
        blockers.append("OPERATION_NOT_ALLOWLISTED")
    if write_enabled and not approval_ok:
        blockers.append("MISSING_APPROVAL_TOKEN_FOR_WRITE_ENABLE")

    if blockers:
        status = "BLOCKED_P90_SHEETS_WRITE_CAPABLE_CONTRACT"
        next_step = "FIX_CONTRACT_BLOCKERS_OR_STOP"
    elif write_enabled:
        status = "REVIEW_REQUIRED_P90_WRITE_ENABLE_REQUEST_READY_FOR_P91"
        next_step = "P91_SINGLE_ROW_STAGING_WRITE_SMOKE_AFTER_EXPLICIT_GO"
    else:
        status = "OK_P90_SHEETS_WRITE_CAPABLE_CONTRACT_READY_DISABLED_BY_DEFAULT"
        next_step = "P91_SINGLE_ROW_STAGING_WRITE_SMOKE_AFTER_EXPLICIT_GO"

    return {
        "step": "P90_SHEETS_WRITE_CAPABLE_CONTRACT_FAST_FUSE",
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "write_capable": True,
        "write_enabled_default": False,
        "write_enabled_requested": write_enabled,
        "sheet_write_executed": False,
        "live_google_api_call": False,
        "target_sheet": target_sheet,
        "target_allowed": target_allowed,
        "target_blocked": target_blocked,
        "operation": operation,
        "operation_allowed": operation_allowed,
        "approval_required_for_p91": True,
        "approval_token_ok": approval_ok,
        "write_target_allowlist": WRITE_TARGET_ALLOWLIST,
        "blocked_direct_write_targets": BLOCKED_DIRECT_WRITE_TARGETS,
        "write_operations_allowlist": WRITE_OPERATIONS_ALLOWLIST,
        "blockers": blockers,
        "local_mvp_seal_status": seal["status"],
        "readonly_dryrun_status": readonly["status"],
        "sheet_write": False,
        "apps_script_execution": False,
        "clasp_push": False,
        "broker_execution": False,
        "order_execution": False,
        "auto_sizing_execution": False,
        "google_rest_local_diag": False,
        "next": next_step,
    }


def assert_p90_contract_safe(payload: dict[str, Any]) -> None:
    unsafe_flags = (
        "sheet_write",
        "sheet_write_executed",
        "apps_script_execution",
        "clasp_push",
        "broker_execution",
        "order_execution",
        "auto_sizing_execution",
        "google_rest_local_diag",
        "live_google_api_call",
    )
    enabled = [flag for flag in unsafe_flags if payload.get(flag)]
    if enabled:
        raise ValueError(f"Unsafe P90 flags enabled: {enabled}")
    if payload["target_blocked"]:
        raise ValueError(f"Blocked direct target: {payload['target_sheet']}")


def render_sheets_write_capable_contract_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# MVP QAIC — P90 Sheets Write-Capable Contract",
        "",
        f"- status: `{payload['status']}`",
        f"- write_capable: `{payload['write_capable']}`",
        f"- write_enabled_default: `{payload['write_enabled_default']}`",
        f"- write_enabled_requested: `{payload['write_enabled_requested']}`",
        f"- sheet_write_executed: `{payload['sheet_write_executed']}`",
        f"- target_sheet: `{payload['target_sheet']}`",
        f"- operation: `{payload['operation']}`",
        f"- blockers: `{payload['blockers']}`",
        f"- next: `{payload['next']}`",
        "",
        "## Safety",
        "",
        "- WRITE_CAPABLE_TRUE",
        "- WRITE_ENABLED_DEFAULT_FALSE",
        "- NO_SHEET_WRITE_EXECUTED",
        "- NO_APPS_SCRIPT_EXECUTION",
        "- NO_CLASP_PUSH",
        "- NO_BROKER_ORDER_SIZING",
        "- NO_LIVE_GOOGLE_API_CALL",
        "",
        "## Allowlist targets",
        "",
    ]
    for target in payload["write_target_allowlist"]:
        lines.append(f"- `{target}`")
    lines.extend(["", "## Blocked direct targets", ""])
    for target in payload["blocked_direct_write_targets"]:
        lines.append(f"- `{target}`")
    lines.extend(["", "## Next", "", f"`{payload['next']}`", ""])
    return "\n".join(lines)


def export_sheets_write_capable_contract(out_dir: str | Path) -> dict[str, str]:
    target = Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    payload = build_sheets_write_capable_contract()
    assert_p90_contract_safe(payload)
    markdown = render_sheets_write_capable_contract_markdown(payload)
    json_path = target / "P90_SHEETS_WRITE_CAPABLE_CONTRACT.json"
    md_path = target / "P90_SHEETS_WRITE_CAPABLE_CONTRACT.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "status": payload["status"],
        "json": str(json_path),
        "markdown": str(md_path),
        "next": payload["next"],
    }
