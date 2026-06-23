from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

P154_PREFIX = "P154_PROMPT_CORRECTION_APPLY_PLAN_OR_STOP_"
P155_PREFIX = "P155_PROMPT_CORRECTION_WORKBENCH_OR_STOP_"
EXPECTED_P154_STATUS = "P154_PROMPT_CORRECTION_APPLY_PLAN_READY_REVIEW_ONLY"
ACCEPTED_P154_GLOBAL_STATUS_PREFIX = "OK_P154_PROMPT_CORRECTION_APPLY_PLAN_OR_STOP"
P155_STATUS = "P155_PROMPT_CORRECTION_WORKBENCH_READY_REVIEW_ONLY"
PROMPT_SOURCE_ID = "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"
NEXT_STEP = "P156_PROMPT_PATCH_CANDIDATE_OR_STOP_AFTER_HUMAN_REVIEW"

SAFETY_FLAGS: dict[str, bool] = {
    "APPLY_ALLOWED": False,
    "PROMPT_SOURCE_MODIFIED": False,
    "HUMAN_REVIEW_REQUIRED": True,
    "GOOGLE_SHEETS_WRITE": False,
    "LIVE_GOOGLE_SHEETS_READ": False,
    "PUBLIC_DEPLOY": False,
    "NO_APPS_SCRIPT_EXECUTION": True,
    "NO_CLASP_PUSH": True,
    "NO_BROKER": True,
    "NO_ORDER": True,
    "NO_SIZING": True,
    "NO_AUTO_APPLY_GEM_RESPONSE": True,
}

WORKBENCH_COLUMNS = [
    "workbench_id",
    "source_plan_row_number",
    "source_action_id",
    "source_action_type",
    "source_priority",
    "source_target",
    "source_summary",
    "source_current_value",
    "source_proposed_value",
    "source_rationale",
    "human_decision",
    "accept_patch",
    "reject_reason",
    "manual_note",
    "ready_for_prompt_patch",
    "apply_now",
    "apply_allowed",
    "prompt_source_modified",
    "human_review_required",
    "safety_status",
]


@dataclass(frozen=True)
class P154Source:
    source_dir: Path
    summary: dict[str, Any]
    plan_rows: list[dict[str, str]]


class P155BlockedError(RuntimeError):
    """Raised when P155 must stop instead of producing a review workbench."""


def utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%d_%H%M%S")


def latest_export_dir(exports_root: Path, prefix: str) -> Path:
    candidates = [
        path for path in exports_root.iterdir() if path.is_dir() and path.name.startswith(prefix)
    ]
    if not candidates:
        raise FileNotFoundError(f"No export directory found for prefix: {prefix}")
    return max(candidates, key=lambda path: (path.stat().st_mtime, path.name))


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"CSV header missing: {path}")
        return [dict(row) for row in reader]


def normalize_summary(raw_summary: dict[str, Any]) -> dict[str, Any]:
    """Return a case-insensitive-friendly flat summary payload.

    P154 was produced by a previous batch and may serialize JSON keys in lowercase,
    uppercase, or under a top-level ``summary`` object depending on the exact writer.
    P155 must validate the contract, not the incidental JSON casing.
    """
    normalized: dict[str, Any] = {}
    for nested_key in ("summary", "SUMMARY", "p154_summary", "P154_SUMMARY"):
        nested = raw_summary.get(nested_key)
        if isinstance(nested, dict):
            normalized.update(nested)
    normalized.update(raw_summary)
    return normalized


SUMMARY_KEY_ALIASES: dict[str, tuple[str, ...]] = {
    # P154 real exports may expose the readiness status as P154_STATUS,
    # source_p154_status, or only as status/STATUS depending on the previous writer.
    # P155 must validate the safety contract, not block on incidental field naming.
    "P154_STATUS": (
        "P154_STATUS",
        "p154_status",
        "SOURCE_P154_STATUS",
        "source_p154_status",
        "status",
        "STATUS",
    ),
}


def summary_value(summary: dict[str, Any], key: str, default: Any = None) -> Any:
    candidate_names = SUMMARY_KEY_ALIASES.get(key, (key,))
    for candidate_name in candidate_names:
        if candidate_name in summary:
            return summary[candidate_name]
        lower_key = candidate_name.lower()
        for candidate_key, candidate_value in summary.items():
            if str(candidate_key).lower() == lower_key:
                return candidate_value
    return default


def p154_status_candidates(summary: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for candidate_name in SUMMARY_KEY_ALIASES["P154_STATUS"]:
        value = summary_value(summary, candidate_name)
        if value is None:
            continue
        text = str(value).strip()
        if text and text not in values:
            values.append(text)
    return values


def p154_status_ready(summary: dict[str, Any]) -> bool:
    for candidate in p154_status_candidates(summary):
        if candidate == EXPECTED_P154_STATUS:
            return True
        if candidate.startswith(ACCEPTED_P154_GLOBAL_STATUS_PREFIX):
            return True
    return False


def source_p154_status(summary: dict[str, Any]) -> str:
    candidates = p154_status_candidates(summary)
    for candidate in candidates:
        if candidate == EXPECTED_P154_STATUS:
            return candidate
    for candidate in candidates:
        if candidate.startswith(ACCEPTED_P154_GLOBAL_STATUS_PREFIX):
            return candidate
    return candidates[0] if candidates else ""


def load_p154_source(source_dir: Path) -> P154Source:
    summary_path = source_dir / "P154_SUMMARY.json"
    report_path = source_dir / "P154_PROMPT_CORRECTION_APPLY_PLAN_REPORT.json"
    plan_path = source_dir / "P154_PROMPT_CORRECTION_APPLY_PLAN.csv"
    if not summary_path.exists() and not report_path.exists():
        raise FileNotFoundError(f"Missing P154 summary/report in: {source_dir}")
    if not plan_path.exists():
        raise FileNotFoundError(f"Missing P154 plan CSV: {plan_path}")

    if summary_path.exists():
        summary = normalize_summary(load_json(summary_path))
    else:
        summary = normalize_summary(load_json(report_path))
    return P154Source(source_dir=source_dir, summary=summary, plan_rows=load_csv_rows(plan_path))


def bool_from_summary(summary: dict[str, Any], key: str, expected: bool) -> bool:
    value = summary_value(summary, key)
    if isinstance(value, bool):
        return value is expected
    if isinstance(value, int):
        return bool(value) is expected
    if isinstance(value, str):
        text = value.strip().lower()
        if text in {"true", "yes", "y", "1"}:
            return expected is True
        if text in {"false", "no", "n", "0"}:
            return expected is False
    return False


def int_from_summary(summary: dict[str, Any], key: str, default: int = 0) -> int:
    value = summary_value(summary, key, default)
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def str_from_summary(summary: dict[str, Any], key: str, default: str = "") -> str:
    value = summary_value(summary, key, default)
    if value is None:
        return default
    return str(value)


def validate_p154_for_p155(source: P154Source) -> list[str]:
    blockers: list[str] = []
    summary = source.summary
    if not p154_status_ready(summary):
        blockers.append("P154_STATUS_NOT_READY_REVIEW_ONLY")
    if str_from_summary(summary, "PROMPT_SOURCE_ID") != PROMPT_SOURCE_ID:
        blockers.append("PROMPT_SOURCE_ID_MISMATCH")
    if not bool_from_summary(summary, "APPLY_ALLOWED", False):
        blockers.append("P154_APPLY_ALLOWED_NOT_FALSE")
    if int_from_summary(summary, "APPLY_NOW_YES_COUNT") != 0:
        blockers.append("P154_APPLY_NOW_YES_COUNT_NOT_ZERO")
    if not bool_from_summary(summary, "PROMPT_SOURCE_MODIFIED", False):
        blockers.append("P154_PROMPT_SOURCE_MODIFIED_NOT_FALSE")
    if int_from_summary(summary, "BLOCKER_COUNT") != 0:
        blockers.append("P154_BLOCKER_COUNT_NOT_ZERO")
    if not bool_from_summary(summary, "HUMAN_REVIEW_REQUIRED", True):
        blockers.append("P154_HUMAN_REVIEW_REQUIRED_NOT_TRUE")
    if not source.plan_rows:
        blockers.append("P154_PLAN_ROWS_EMPTY")
    return blockers


def pick(row: dict[str, str], names: tuple[str, ...], default: str = "") -> str:
    normalized = {key.lower(): value for key, value in row.items()}
    for name in names:
        value = normalized.get(name.lower())
        if value not in (None, ""):
            return str(value)
    return default


def build_workbench_rows(plan_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    workbench_rows: list[dict[str, str]] = []
    for index, row in enumerate(plan_rows, start=1):
        source_action_type = pick(
            row,
            (
                "action_type",
                "correction_type",
                "plan_type",
                "category",
                "action_category",
                "recommendation_type",
            ),
            "REVIEW_ITEM",
        )
        workbench_rows.append(
            {
                "workbench_id": f"P155-WB-{index:03d}",
                "source_plan_row_number": str(index),
                "source_action_id": pick(
                    row,
                    ("action_id", "correction_id", "plan_id", "id"),
                    f"P154-PLAN-{index:03d}",
                ),
                "source_action_type": source_action_type,
                "source_priority": pick(row, ("priority", "severity", "risk_level"), "REVIEW"),
                "source_target": pick(
                    row,
                    (
                        "target_field",
                        "target",
                        "prompt_section",
                        "field",
                        "json_field",
                        "field_name",
                    ),
                    "REVIEW_TARGET_UNKNOWN",
                ),
                "source_summary": pick(
                    row,
                    (
                        "summary",
                        "action_summary",
                        "correction_summary",
                        "issue",
                        "description",
                    ),
                    "Review P154 source row before any prompt patch.",
                ),
                "source_current_value": pick(
                    row,
                    ("current_value", "before", "existing_value", "observed_value"),
                ),
                "source_proposed_value": pick(
                    row,
                    ("proposed_value", "after", "recommended_value", "patch_candidate"),
                ),
                "source_rationale": pick(row, ("rationale", "reason", "why", "note")),
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
        )
    return workbench_rows


def count_action_type(rows: list[dict[str, str]], tokens: tuple[str, ...]) -> int:
    count = 0
    for row in rows:
        value = row.get("source_action_type", "").upper()
        if any(token in value for token in tokens):
            count += 1
    return count


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_text(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")


def build_summary(
    *,
    source: P154Source,
    output_dir: Path,
    workbench_rows: list[dict[str, str]],
    generated_at: str,
) -> dict[str, Any]:
    prompt_edit_candidates = int_from_summary(source.summary, "PROMPT_EDIT_CANDIDATE_COUNT")
    field_clarifications = int_from_summary(source.summary, "FIELD_CLARIFICATION_COUNT")
    if prompt_edit_candidates == 0:
        prompt_edit_candidates = count_action_type(workbench_rows, ("PROMPT", "EDIT", "PATCH"))
    if field_clarifications == 0:
        field_clarifications = count_action_type(workbench_rows, ("FIELD", "CLARIFICATION"))

    return {
        "STATUS": "OK_P155_PROMPT_CORRECTION_WORKBENCH_OR_STOP_EXPORT_READY",
        "P155_STATUS": P155_STATUS,
        "PROMPT_SOURCE_ID": PROMPT_SOURCE_ID,
        "SOURCE_P154_DIR": str(source.source_dir),
        "SOURCE_P154_STATUS": source_p154_status(source.summary),
        "OUTPUT_DIR": str(output_dir),
        "GENERATED_AT_UTC": generated_at,
        "WORKBENCH_ROW_COUNT": len(workbench_rows),
        "PENDING_HUMAN_REVIEW_COUNT": len(workbench_rows),
        "PROMPT_EDIT_CANDIDATE_COUNT": prompt_edit_candidates,
        "FIELD_CLARIFICATION_COUNT": field_clarifications,
        "APPLY_NOW_YES_COUNT": 0,
        "BLOCKER_COUNT": 0,
        "NEXT": NEXT_STEP,
        **SAFETY_FLAGS,
    }


def render_decision_markdown(summary: dict[str, Any]) -> str:
    return f"""
# P155 Human Review Decision

Status: `{summary["P155_STATUS"]}`

## Decision

No prompt correction is applied by P155. The workbench is a human review surface only.

## Required human action

Review each row in `P155_PROMPT_CORRECTION_WORKBENCH.csv`, then decide whether a later
batch may prepare a prompt patch candidate.

## Hard gates

- `APPLY_ALLOWED=false`
- `APPLY_NOW_YES_COUNT=0`
- `PROMPT_SOURCE_MODIFIED=false`
- `HUMAN_REVIEW_REQUIRED=true`
- `GOOGLE_SHEETS_WRITE=false`
- `PUBLIC_DEPLOY=false`
- `NO_AUTO_APPLY_GEM_RESPONSE=true`

## Next

`{summary["NEXT"]}`
"""


def render_checklist(summary: dict[str, Any]) -> str:
    return f"""
# P155 Operator Review Checklist

## Source

- Prompt source: `{summary["PROMPT_SOURCE_ID"]}`
- P154 source: `{summary["SOURCE_P154_DIR"]}`
- P154 status: `{summary["SOURCE_P154_STATUS"]}`

## Workbench

- Rows to review: `{summary["WORKBENCH_ROW_COUNT"]}`
- Pending human review: `{summary["PENDING_HUMAN_REVIEW_COUNT"]}`
- Prompt edit candidates: `{summary["PROMPT_EDIT_CANDIDATE_COUNT"]}`
- Field clarifications: `{summary["FIELD_CLARIFICATION_COUNT"]}`

## Operator checklist

1. Open `P155_PROMPT_CORRECTION_WORKBENCH.csv`.
2. Review every `PENDING_REVIEW` row.
3. Keep `apply_now=NO` unless a later controlled batch explicitly changes the contract.
4. Use `manual_note` for ambiguity or rejected correction rationale.
5. Only mark `ready_for_prompt_patch=YES` after human review.
6. Do not edit the P132/P133 source prompt manually from this batch output.

## Stop conditions

Stop if any row would require live data access, public deployment, broker action, order,
sizing, auto-application, or Sheets write.
"""


def build_and_write_export(repo_root: Path, source_dir: Path | None = None) -> dict[str, Any]:
    exports_root = repo_root / "05_EXPORTS"
    exports_root.mkdir(parents=True, exist_ok=True)
    resolved_source_dir = source_dir or latest_export_dir(exports_root, P154_PREFIX)
    source = load_p154_source(resolved_source_dir)
    blockers = validate_p154_for_p155(source)
    if blockers:
        raise P155BlockedError(";".join(blockers))

    generated_at = utc_stamp()
    output_dir = exports_root / f"{P155_PREFIX}{generated_at}"
    output_dir.mkdir(parents=True, exist_ok=False)

    workbench_rows = build_workbench_rows(source.plan_rows)
    summary = build_summary(
        source=source,
        output_dir=output_dir,
        workbench_rows=workbench_rows,
        generated_at=generated_at,
    )
    report = {
        "report_type": "P155_PROMPT_CORRECTION_WORKBENCH_REPORT",
        "summary": summary,
        "workbench_columns": WORKBENCH_COLUMNS,
        "source_plan_row_count": len(source.plan_rows),
        "safety_contract": SAFETY_FLAGS,
    }

    write_csv(
        output_dir / "P155_PROMPT_CORRECTION_WORKBENCH.csv", workbench_rows, WORKBENCH_COLUMNS
    )
    write_json(output_dir / "P155_PROMPT_CORRECTION_WORKBENCH_REPORT.json", report)
    write_json(output_dir / "P155_SUMMARY.json", summary)
    write_text(output_dir / "P155_HUMAN_REVIEW_DECISION.md", render_decision_markdown(summary))
    write_text(output_dir / "P155_OPERATOR_REVIEW_CHECKLIST.md", render_checklist(summary))
    return summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build P155 prompt correction workbench.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--source-p154-dir", default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    source_dir = Path(args.source_p154_dir).resolve() if args.source_p154_dir else None
    summary = build_and_write_export(repo_root=repo_root, source_dir=source_dir)
    print(summary["P155_STATUS"])
    print(f"prompt_source_id={summary['PROMPT_SOURCE_ID']}")
    print(f"source_p154_status={summary['SOURCE_P154_STATUS']}")
    print(f"workbench_row_count={summary['WORKBENCH_ROW_COUNT']}")
    print(f"pending_human_review_count={summary['PENDING_HUMAN_REVIEW_COUNT']}")
    print(f"apply_allowed={str(summary['APPLY_ALLOWED']).lower()}")
    print(f"apply_now_yes_count={summary['APPLY_NOW_YES_COUNT']}")
    print(f"blocker_count={summary['BLOCKER_COUNT']}")
    print(f"google_sheets_write={str(summary['GOOGLE_SHEETS_WRITE']).lower()}")
    print(f"public_deploy={str(summary['PUBLIC_DEPLOY']).lower()}")
    print(f"prompt_source_modified={str(summary['PROMPT_SOURCE_MODIFIED']).lower()}")
    print(f"output_dir={summary['OUTPUT_DIR']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
