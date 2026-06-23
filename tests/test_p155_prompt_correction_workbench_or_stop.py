from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import pytest

from mvp_qaic_py.p155_prompt_correction_workbench_or_stop import (
    P155BlockedError,
    build_and_write_export,
    build_workbench_rows,
    load_p154_source,
    p154_status_ready,
    summary_value,
    validate_p154_for_p155,
)


def write_p154_export(
    repo_root: Path,
    *,
    apply_allowed: bool = False,
    lowercase_summary: bool = False,
    nested_summary: bool = False,
    global_status_only: bool = False,
) -> Path:
    source_dir = (
        repo_root / "05_EXPORTS" / "P154_PROMPT_CORRECTION_APPLY_PLAN_OR_STOP_20260623_144922"
    )
    source_dir.mkdir(parents=True)
    summary: dict[str, Any] = {
        "P154_STATUS": "P154_PROMPT_CORRECTION_APPLY_PLAN_READY_REVIEW_ONLY",
        "PROMPT_SOURCE_ID": "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW",
        "PLAN_ROW_COUNT": 4,
        "PROMPT_EDIT_CANDIDATE_COUNT": 1,
        "FIELD_CLARIFICATION_COUNT": 2,
        "APPLY_ALLOWED": apply_allowed,
        "APPLY_NOW_YES_COUNT": 0,
        "PROMPT_SOURCE_MODIFIED": False,
        "BLOCKER_COUNT": 0,
        "HUMAN_REVIEW_REQUIRED": True,
    }
    if global_status_only:
        summary.pop("P154_STATUS", None)
        summary["STATUS"] = "OK_P154_PROMPT_CORRECTION_APPLY_PLAN_OR_STOP_COMMIT_TAG_PUSH_SEALED"
    if lowercase_summary:
        summary = {key.lower(): value for key, value in summary.items()}
    payload = {"summary": summary} if nested_summary else summary
    (source_dir / "P154_SUMMARY.json").write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    rows = [
        {
            "action_id": "P154-A001",
            "action_type": "PROMPT_EDIT_CANDIDATE",
            "priority": "HIGH",
            "target_field": "risk_notes",
            "summary": "Clarify that image evidence must be used.",
            "current_value": "weak instruction",
            "proposed_value": "explicit instruction",
            "rationale": "real GEM response needs better grounding",
        },
        {
            "action_id": "P154-A002",
            "action_type": "FIELD_CLARIFICATION",
            "priority": "MEDIUM",
            "target_field": "portfolio_total_usd",
            "summary": "Clarify missing values.",
        },
        {
            "action_id": "P154-A003",
            "action_type": "FIELD_CLARIFICATION",
            "priority": "MEDIUM",
            "target_field": "asset_rows",
            "summary": "Clarify OCR uncertainty.",
        },
        {
            "action_id": "P154-A004",
            "action_type": "REVIEW_NOTE",
            "priority": "LOW",
            "target_field": "operator_summary",
            "summary": "Add operator note.",
        },
    ]
    with (source_dir / "P154_PROMPT_CORRECTION_APPLY_PLAN.csv").open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return source_dir


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_p155_export_builds_pending_review_workbench(tmp_path: Path) -> None:
    source_dir = write_p154_export(tmp_path)

    summary = build_and_write_export(repo_root=tmp_path, source_dir=source_dir)

    assert summary["P155_STATUS"] == "P155_PROMPT_CORRECTION_WORKBENCH_READY_REVIEW_ONLY"
    assert summary["WORKBENCH_ROW_COUNT"] == 4
    assert summary["PENDING_HUMAN_REVIEW_COUNT"] == 4
    assert summary["PROMPT_EDIT_CANDIDATE_COUNT"] == 1
    assert summary["FIELD_CLARIFICATION_COUNT"] == 2
    assert summary["APPLY_ALLOWED"] is False
    assert summary["APPLY_NOW_YES_COUNT"] == 0
    assert summary["PROMPT_SOURCE_MODIFIED"] is False
    assert summary["BLOCKER_COUNT"] == 0
    assert summary["HUMAN_REVIEW_REQUIRED"] is True

    output_dir = Path(summary["OUTPUT_DIR"])
    assert (output_dir / "P155_HUMAN_REVIEW_DECISION.md").exists()
    assert (output_dir / "P155_OPERATOR_REVIEW_CHECKLIST.md").exists()
    assert (output_dir / "P155_PROMPT_CORRECTION_WORKBENCH_REPORT.json").exists()
    assert (output_dir / "P155_SUMMARY.json").exists()

    rows = read_csv(output_dir / "P155_PROMPT_CORRECTION_WORKBENCH.csv")
    assert len(rows) == 4
    assert {row["human_decision"] for row in rows} == {"PENDING_REVIEW"}
    assert {row["accept_patch"] for row in rows} == {"NO"}
    assert {row["ready_for_prompt_patch"] for row in rows} == {"NO"}
    assert {row["apply_now"] for row in rows} == {"NO"}
    assert {row["apply_allowed"] for row in rows} == {"false"}


def test_p155_accepts_lowercase_p154_summary_keys(tmp_path: Path) -> None:
    source_dir = write_p154_export(tmp_path, lowercase_summary=True)

    summary = build_and_write_export(repo_root=tmp_path, source_dir=source_dir)

    assert summary["SOURCE_P154_STATUS"] == "P154_PROMPT_CORRECTION_APPLY_PLAN_READY_REVIEW_ONLY"
    assert summary["WORKBENCH_ROW_COUNT"] == 4
    assert summary["APPLY_ALLOWED"] is False


def test_p155_accepts_nested_lowercase_p154_summary(tmp_path: Path) -> None:
    source_dir = write_p154_export(tmp_path, lowercase_summary=True, nested_summary=True)
    source = load_p154_source(source_dir)

    assert (
        summary_value(source.summary, "PROMPT_SOURCE_ID") == "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"
    )
    assert validate_p154_for_p155(source) == []


# R5 guard: p154_status_ready must be imported; R4 committed despite F821/NameError.
def test_p155_accepts_p154_global_sealed_status_when_safety_gates_pass(tmp_path: Path) -> None:
    source_dir = write_p154_export(tmp_path, global_status_only=True)
    source = load_p154_source(source_dir)

    assert p154_status_ready(source.summary) is True
    assert validate_p154_for_p155(source) == []


def test_p155_blocks_if_p154_allows_apply(tmp_path: Path) -> None:
    source_dir = write_p154_export(tmp_path, apply_allowed=True)

    with pytest.raises(P155BlockedError, match="P154_APPLY_ALLOWED_NOT_FALSE"):
        build_and_write_export(repo_root=tmp_path, source_dir=source_dir)


def test_validate_p154_blocks_empty_plan(tmp_path: Path) -> None:
    source_dir = write_p154_export(tmp_path)
    (source_dir / "P154_PROMPT_CORRECTION_APPLY_PLAN.csv").write_text(
        "action_id,action_type\n",
        encoding="utf-8",
    )
    source = load_p154_source(source_dir)

    assert "P154_PLAN_ROWS_EMPTY" in validate_p154_for_p155(source)


def test_build_workbench_rows_keeps_source_values_and_safe_defaults() -> None:
    rows = build_workbench_rows(
        [
            {
                "action_id": "ACT-1",
                "action_type": "PROMPT_EDIT_CANDIDATE",
                "target_field": "field_a",
                "summary": "change something",
                "proposed_value": "new text",
            }
        ]
    )

    assert rows == [
        {
            "workbench_id": "P155-WB-001",
            "source_plan_row_number": "1",
            "source_action_id": "ACT-1",
            "source_action_type": "PROMPT_EDIT_CANDIDATE",
            "source_priority": "REVIEW",
            "source_target": "field_a",
            "source_summary": "change something",
            "source_current_value": "",
            "source_proposed_value": "new text",
            "source_rationale": "",
            "human_decision": "PENDING_REVIEW",
            "accept_patch": "NO",
            "reject_reason": "",
            "manual_note": "",
            "ready_for_prompt_patch": "NO",
            "apply_now": "NO",
            "apply_allowed": "false",
            "prompt_source_modified": "false",
            "human_review_required": "true",
            "safety_status": "HUMAN_REVIEW_ONLY_NO_APPLY",
        }
    ]
