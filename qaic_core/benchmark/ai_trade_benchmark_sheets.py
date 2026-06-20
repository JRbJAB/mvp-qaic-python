"""Pure one-tab Sheets contract and gated payload builders.

This module deliberately contains no Google client or network code.
"""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable

from .ai_trade_benchmark_model import BenchmarkDecision, BenchmarkRun

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
    if not spreadsheet_id.strip():
        raise SheetsContractError("spreadsheet_id is required")
    validate_allowed_tabs([tab])
    return {
        "spreadsheet_id": spreadsheet_id,
        "run_id": run.run_id,
        "allowed_tabs": [tab],
        "forbidden_tabs": list(FORBIDDEN_TABS),
        "dry_run": dry_run,
        "apply": False,
        "values": build_one_tab_values(run),
        "safety": asdict(run.safety),
    }


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
    return {
        "spreadsheet_id": spreadsheet_id,
        "run_id": run.run_id,
        "tab": tab,
        "range": f"'{tab}'!A1:G",
        "values": build_one_tab_values(run),
        "dry_run": False,
        "apply": True,
        "backup_path": str(backup_path),
        "human_go": True,
    }
