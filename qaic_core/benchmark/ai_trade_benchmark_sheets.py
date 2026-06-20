"""Pure one-tab Sheets contract and gated payload builders.

This module deliberately contains no Google client or network code.
"""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable

from .ai_trade_benchmark_model import BenchmarkDecision, BenchmarkRun

TARGET_SPREADSHEET_ID = "19KY8Y1ozS7ONaJu9_5NQmjO47l-xM798Xm-y1n7fNd0"
ALLOWED_TAB = "️ BENCHMARK_AI_TRADE"
ALLOWED_TABS = [ALLOWED_TAB]
FORBIDDEN_TABS = [
    "BENCHMARK_AI_TRADE_TOOLS",
    "BENCHMARK_AI_TRADE_SOURCES",
    "BENCHMARK_AI_TRADE_FEATURE_GAPS",
    "BENCHMARK_AI_TRADE_REVIEW_QUEUE",
    "BENCHMARK_AI_TRADE_RUN_LOG",
]
# Lower-case aliases are part of the serialized cockpit contract vocabulary.
allowed_tabs = ALLOWED_TABS
forbidden_tabs = FORBIDDEN_TABS


class SheetsContractError(ValueError):
    pass


class SheetsApplyGateError(SheetsContractError):
    """Controlled refusal raised when an apply request fails a safety gate."""


def assert_no_forbidden_tabs(tabs: Iterable[str]) -> None:
    forbidden = sorted(set(tabs).intersection(FORBIDDEN_TABS))
    if forbidden:
        raise SheetsContractError(f"Forbidden benchmark tab(s): {', '.join(forbidden)}")


def validate_allowed_tabs(tabs: Iterable[str]) -> bool:
    requested = list(tabs)
    assert_no_forbidden_tabs(requested)
    if requested != ALLOWED_TABS:
        raise SheetsContractError(f"Exactly one allowed tab is required: {ALLOWED_TAB}")
    return True


def _validate_apply_target(allowed_tab_name: str | Iterable[str]) -> str:
    if isinstance(allowed_tab_name, str):
        tabs = [allowed_tab_name]
    else:
        tabs = list(allowed_tab_name)
    validate_allowed_tabs(tabs)
    return tabs[0]


def validate_google_sheets_apply_gate(
    *,
    spreadsheet_id: str,
    allowed_tab_name: str | Iterable[str] = ALLOWED_TAB,
    run_id: str,
    backup_confirmed: bool = False,
    human_go: bool = False,
    apply: bool = False,
    dry_run: bool = True,
    credentials_path: str | Path | None = None,
    credentials_ref: str | None = None,
) -> dict[str, Any]:
    """Evaluate the offline gate without reading credentials or calling Google."""
    tab = _validate_apply_target(allowed_tab_name)
    if not str(run_id).strip():
        raise SheetsApplyGateError("Apply gate refused: run_id is required")

    reasons: list[str] = []
    if apply and not dry_run:
        if spreadsheet_id != TARGET_SPREADSHEET_ID:
            reasons.append("spreadsheet_id does not match the approved cockpit")
        if not backup_confirmed:
            reasons.append("backup_confirmed is required")
        if not human_go:
            reasons.append("human_go is required")
        if not (str(credentials_path or "").strip() or str(credentials_ref or "").strip()):
            reasons.append("credentials_path or credentials_ref must be declared")

    ready = apply and not reasons and not dry_run
    if ready:
        status = "APPLY_READY_BUT_NOT_EXECUTED"
    elif apply and reasons:
        status = "BLOCKED"
    else:
        status = "DRY_RUN" if dry_run else "NO_APPLY_REQUESTED"
    return {
        "status": status,
        "spreadsheet_id": spreadsheet_id,
        "run_id": run_id,
        "allowed_tabs": [tab],
        "apply": apply,
        "dry_run": dry_run,
        "backup_confirmed": backup_confirmed,
        "human_go": human_go,
        "credentials_declared": bool(credentials_path or credentials_ref),
        "blocked_reasons": reasons,
        "google_live_call": False,
        "sheet_write": False,
    }


def assert_google_sheets_apply_allowed(**gate_inputs: Any) -> dict[str, Any]:
    """Return an apply-ready decision or raise a controlled gate refusal."""
    decision = validate_google_sheets_apply_gate(**gate_inputs)
    if decision["status"] != "APPLY_READY_BUT_NOT_EXECUTED":
        reasons = decision["blocked_reasons"] or ["explicit apply mode is required"]
        raise SheetsApplyGateError("Apply blocked: " + "; ".join(reasons))
    return decision


def build_google_sheets_batch_update_payload(
    *, tab_name: str = ALLOWED_TAB, values: list[list[Any]]
) -> dict[str, Any]:
    """Build a serializable one-tab values update body; never execute it."""
    tab = _validate_apply_target(tab_name)
    return {
        "valueInputOption": "RAW",
        "data": [{"range": f"'{tab}'!A1:G", "majorDimension": "ROWS", "values": values}],
        "includeValuesInResponse": False,
    }


def build_google_sheets_apply_plan(
    *,
    spreadsheet_id: str,
    run: BenchmarkRun,
    allowed_tab_name: str | Iterable[str] = ALLOWED_TAB,
    run_id: str | None = None,
    backup_confirmed: bool = False,
    human_go: bool = False,
    apply: bool = False,
    dry_run: bool = True,
    credentials_path: str | Path | None = None,
    credentials_ref: str | None = None,
) -> dict[str, Any]:
    resolved_run_id = run_id if run_id is not None else run.run_id
    gate = validate_google_sheets_apply_gate(
        spreadsheet_id=spreadsheet_id,
        allowed_tab_name=allowed_tab_name,
        run_id=resolved_run_id,
        backup_confirmed=backup_confirmed,
        human_go=human_go,
        apply=apply,
        dry_run=dry_run,
        credentials_path=credentials_path,
        credentials_ref=credentials_ref,
    )
    tab = gate["allowed_tabs"][0]
    return {
        **gate,
        "forbidden_tabs": list(FORBIDDEN_TABS),
        "batch_update_payload": build_google_sheets_batch_update_payload(
            tab_name=tab, values=build_one_tab_values(run)
        ),
        "safety": asdict(run.safety),
    }


def render_apply_gate_audit(plan: dict[str, Any]) -> dict[str, Any]:
    """Return a compact audit record with no credential value or secret material."""
    return {
        key: plan[key]
        for key in (
            "status",
            "spreadsheet_id",
            "run_id",
            "allowed_tabs",
            "apply",
            "dry_run",
            "backup_confirmed",
            "human_go",
            "credentials_declared",
            "blocked_reasons",
            "google_live_call",
            "sheet_write",
        )
    }


def build_one_tab_values(run: BenchmarkRun) -> list[list[Any]]:
    counts = {decision: 0 for decision in BenchmarkDecision}
    for tool in run.tools:
        counts[tool.decision] += 1
    rows: list[list[Any]] = [
        ["section", "key", "value", "score_or_status", "source_url", "decision", "notes"],
        ["DASHBOARD", "status", run.status, run.status, "", "", ""],
        ["DASHBOARD", "candidate_count", len(run.tools), len(run.tools), "", "", ""],
        [
            "DASHBOARD",
            "inspire_count",
            counts[BenchmarkDecision.INSPIRE],
            counts[BenchmarkDecision.INSPIRE],
            "",
            "",
            "",
        ],
        [
            "DASHBOARD",
            "monitor_count",
            counts[BenchmarkDecision.MONITOR],
            counts[BenchmarkDecision.MONITOR],
            "",
            "",
            "",
        ],
        [
            "DASHBOARD",
            "review_required_count",
            counts[BenchmarkDecision.REVIEW_REQUIRED],
            counts[BenchmarkDecision.REVIEW_REQUIRED],
            "",
            "",
            "",
        ],
        [
            "DASHBOARD",
            "blocked_count",
            counts[BenchmarkDecision.BLOCKED],
            counts[BenchmarkDecision.BLOCKED],
            "",
            "",
            "",
        ],
        [
            "DASHBOARD",
            "safety",
            "HUMAN_REVIEW_ONLY",
            "SAFE",
            "",
            "",
            "NO_BROKER; NO_ORDER; NO_SIZING; NO_AUTO_SIGNAL_COPY",
        ],
        ["DASHBOARD", "run_id", run.run_id, "", "", "", ""],
        ["DASHBOARD", "generated_at", run.generated_at, "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["tool_id", "tool_name", "category", "overall_score", "source_url", "decision", "notes"],
    ]
    rows.extend(
        [
            [
                tool.tool_id,
                tool.tool_name,
                tool.category.value,
                tool.overall_score,
                tool.source_url,
                tool.decision.value,
                tool.notes,
            ]
            for tool in run.tools
        ]
    )
    return rows


def build_sheets_dry_run_plan(
    spreadsheet_id: str, run: BenchmarkRun, *, tab: str = ALLOWED_TAB, dry_run: bool = True
) -> dict[str, Any]:
    plan = build_google_sheets_apply_plan(
        spreadsheet_id=spreadsheet_id, run=run, allowed_tab_name=tab, dry_run=dry_run
    )
    plan["values"] = plan["batch_update_payload"]["data"][0]["values"]
    return plan


def build_apply_payload(
    *,
    spreadsheet_id: str,
    run: BenchmarkRun,
    backup_path: str | Path,
    tab: str = ALLOWED_TAB,
    apply: bool = False,
    human_go: bool = False,
) -> dict[str, Any]:
    if not apply:
        raise SheetsContractError("Apply refused: explicit --apply is required")
    if not spreadsheet_id.strip():
        raise SheetsContractError("Apply refused: spreadsheet_id is required")
    if not run.run_id.strip():
        raise SheetsContractError("Apply refused: run_id is required")
    if not str(backup_path).strip():
        raise SheetsContractError("Apply refused: backup local file path is required")
    if not Path(backup_path).is_file():
        raise SheetsContractError("Apply refused: backup local file must exist")
    if not human_go:
        raise SheetsContractError("Apply refused: explicit human_go is required")
    validate_allowed_tabs([tab])
    assert_google_sheets_apply_allowed(
        spreadsheet_id=spreadsheet_id,
        allowed_tab_name=tab,
        run_id=run.run_id,
        backup_confirmed=True,
        human_go=human_go,
        apply=apply,
        dry_run=False,
        credentials_ref="LEGACY_EXTERNAL_BACKUP_REFERENCE",
    )
    return {
        "spreadsheet_id": spreadsheet_id,
        "run_id": run.run_id,
        "tab": tab,
        "range": f"'{tab}'!A1:G",
        "values": build_one_tab_values(run),
        "dry_run": False,
        "apply": True,
        "status": "APPLY_READY_BUT_NOT_EXECUTED",
        "backup_path": str(backup_path),
        "human_go": True,
        "google_live_call": False,
        "sheet_write": False,
    }
