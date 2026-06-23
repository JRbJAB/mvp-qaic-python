"""P156 prompt patch candidate or stop after human review.

Local/private MVP QAIC gate:
- reads the latest P155 human workbench export
- produces a P156 stop report while human review is still pending
- never modifies the prompt source
- never applies a patch
- never writes Google Sheets or deploys anything
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

VERSION = "MVP_QAIC_P156_PROMPT_PATCH_CANDIDATE_OR_STOP_0.1.0"
EXPORT_PREFIX = "P156_PROMPT_PATCH_CANDIDATE_OR_STOP_AFTER_HUMAN_REVIEW"
P155_PREFIX = "P155_PROMPT_CORRECTION_WORKBENCH_OR_STOP"

PROMPT_SOURCE_ID = "P132_P133_PORTFOLIO_MULTIMODAL_REVIEW"

PENDING_VALUES = {
    "",
    "PENDING",
    "PENDING_HUMAN_REVIEW",
    "HUMAN_REVIEW_REQUIRED",
    "REVIEW_REQUIRED",
    "TODO",
    "TO_REVIEW",
    "WAITING_HUMAN_REVIEW",
}

ACCEPT_VALUES = {
    "ACCEPT",
    "ACCEPT_PATCH",
    "APPROVE",
    "APPROVED",
    "READY_FOR_PROMPT_PATCH",
    "YES",
    "Y",
    "TRUE",
}

REJECT_OR_HOLD_VALUES = {
    "REJECT",
    "REJECTED",
    "NEEDS_EDIT",
    "DEFER",
    "DEFERRED",
    "NO",
    "N",
    "FALSE",
}


@dataclass(frozen=True)
class P155Source:
    source_dir: Path
    summary: dict[str, Any]
    rows: list[dict[str, str]]
    workbench_file: Path | None


def _utc_timestamp() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _get_ci(mapping: dict[str, Any], *keys: str, default: Any = None) -> Any:
    lowered = {str(k).lower(): v for k, v in mapping.items()}
    for key in keys:
        if key in mapping:
            return mapping[key]
        key_lower = key.lower()
        if key_lower in lowered:
            return lowered[key_lower]
    return default


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"true", "yes", "y", "1", "ok"}


def _as_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def _find_latest_export(repo_root: Path, prefix: str) -> Path:
    exports_dir = repo_root / "05_EXPORTS"
    if not exports_dir.exists():
        raise FileNotFoundError(f"exports directory not found: {exports_dir}")
    candidates = [
        path for path in exports_dir.iterdir() if path.is_dir() and path.name.startswith(prefix)
    ]
    if not candidates:
        raise FileNotFoundError(f"no export directory found for prefix {prefix}")
    return max(candidates, key=lambda path: path.stat().st_mtime)


def _find_workbench_csv(source_dir: Path) -> Path | None:
    preferred = sorted(source_dir.glob("*WORKBENCH*.csv"))
    if preferred:
        return preferred[0]
    csv_files = sorted(source_dir.glob("*.csv"))
    return csv_files[0] if csv_files else None


def _read_csv_rows(path: Path | None) -> list[dict[str, str]]:
    if path is None or not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def load_p155_source(source_dir: Path) -> P155Source:
    summary_path = source_dir / "P155_SUMMARY.json"
    if not summary_path.exists():
        json_candidates = sorted(source_dir.glob("*SUMMARY*.json"))
        if not json_candidates:
            raise FileNotFoundError(f"P155 summary JSON not found in {source_dir}")
        summary_path = json_candidates[0]

    summary = _read_json(summary_path)
    workbench_file = _find_workbench_csv(source_dir)
    rows = _read_csv_rows(workbench_file)
    return P155Source(
        source_dir=source_dir, summary=summary, rows=rows, workbench_file=workbench_file
    )


def p155_safety_gate_ok(summary: dict[str, Any]) -> bool:
    status = str(_get_ci(summary, "P155_STATUS", "p155_status", default=""))
    source_id = str(_get_ci(summary, "PROMPT_SOURCE_ID", "prompt_source_id", default=""))
    apply_allowed = _as_bool(_get_ci(summary, "APPLY_ALLOWED", "apply_allowed", default=True))
    prompt_source_modified = _as_bool(
        _get_ci(summary, "PROMPT_SOURCE_MODIFIED", "prompt_source_modified", default=True)
    )
    blocker_count = _as_int(
        _get_ci(summary, "BLOCKER_COUNT", "blocker_count", default=999), default=999
    )
    google_sheets_write = _as_bool(
        _get_ci(summary, "GOOGLE_SHEETS_WRITE", "google_sheets_write", default=True)
    )
    public_deploy = _as_bool(_get_ci(summary, "PUBLIC_DEPLOY", "public_deploy", default=True))

    return (
        status == "P155_PROMPT_CORRECTION_WORKBENCH_READY_REVIEW_ONLY"
        and source_id == PROMPT_SOURCE_ID
        and apply_allowed is False
        and prompt_source_modified is False
        and blocker_count == 0
        and google_sheets_write is False
        and public_deploy is False
    )


def _decision_value(row: dict[str, str]) -> str:
    decision_fields = [
        "human_decision",
        "review_decision",
        "operator_decision",
        "decision",
        "accept_patch",
        "ready_for_prompt_patch",
        "apply_now",
    ]
    lowered = {str(k).lower(): v for k, v in row.items()}
    for field in decision_fields:
        if field in lowered:
            return str(lowered[field]).strip().upper()
    return ""


def row_decision_state(row: dict[str, str]) -> str:
    value = _decision_value(row)
    if value in ACCEPT_VALUES:
        return "ACCEPTED_FOR_PATCH_CANDIDATE"
    if value in REJECT_OR_HOLD_VALUES:
        return "REJECTED_OR_DEFERRED"
    if value in PENDING_VALUES:
        return "PENDING_HUMAN_REVIEW"
    return "PENDING_HUMAN_REVIEW"


def summarize_workbench(source: P155Source) -> dict[str, int]:
    rows = source.rows
    if not rows:
        pending_summary = _as_int(
            _get_ci(
                source.summary,
                "PENDING_HUMAN_REVIEW_COUNT",
                "pending_human_review_count",
                default=0,
            )
        )
        total_summary = _as_int(
            _get_ci(source.summary, "WORKBENCH_ROW_COUNT", "workbench_row_count", default=0)
        )
        return {
            "workbench_row_count": total_summary,
            "pending_human_review_count": pending_summary,
            "accepted_for_patch_candidate_count": 0,
            "rejected_or_deferred_count": 0,
        }

    states = [row_decision_state(row) for row in rows]
    return {
        "workbench_row_count": len(rows),
        "pending_human_review_count": states.count("PENDING_HUMAN_REVIEW"),
        "accepted_for_patch_candidate_count": states.count("ACCEPTED_FOR_PATCH_CANDIDATE"),
        "rejected_or_deferred_count": states.count("REJECTED_OR_DEFERRED"),
    }


def _decision_readback_rows(source: P155Source) -> list[dict[str, Any]]:
    if not source.rows:
        return []

    output: list[dict[str, Any]] = []
    for index, row in enumerate(source.rows, start=1):
        output.append(
            {
                "row_index": index,
                "decision_state": row_decision_state(row),
                "raw_human_decision": _decision_value(row),
                "prompt_source_id": row.get("prompt_source_id")
                or row.get("PROMPT_SOURCE_ID")
                or PROMPT_SOURCE_ID,
                "action_id": row.get("action_id") or row.get("ACTION_ID") or row.get("id") or "",
                "correction_type": row.get("correction_type") or row.get("CORRECTION_TYPE") or "",
                "field_name": row.get("field_name") or row.get("FIELD_NAME") or "",
                "summary": row.get("summary")
                or row.get("SUMMARY")
                or row.get("action_summary")
                or "",
            }
        )
    return output


def build_export(repo_root: Path, source_dir: Path | None = None) -> dict[str, Any]:
    source_dir = source_dir or _find_latest_export(repo_root, P155_PREFIX)
    source = load_p155_source(source_dir)

    if not p155_safety_gate_ok(source.summary):
        raise RuntimeError("P155_SOURCE_SAFETY_GATE_FAILED")

    counts = summarize_workbench(source)
    pending = counts["pending_human_review_count"]
    accepted = counts["accepted_for_patch_candidate_count"]

    patch_candidate_created = pending == 0 and accepted > 0
    p156_status = (
        "P156_PROMPT_PATCH_CANDIDATE_READY_REVIEW_ONLY"
        if patch_candidate_created
        else "P156_STOP_WAITING_HUMAN_REVIEW"
    )
    next_action = (
        "P157_PROMPT_PATCH_VALIDATION_OR_STOP"
        if patch_candidate_created
        else "FILL_P155_WORKBENCH_THEN_RETRY_P156"
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = repo_root / "05_EXPORTS" / f"{EXPORT_PREFIX}_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=False)

    summary: dict[str, Any] = {
        "version": VERSION,
        "generated_at": _utc_timestamp(),
        "status": "OK_P156_PROMPT_PATCH_CANDIDATE_OR_STOP_EXPORT_READY",
        "p156_status": p156_status,
        "prompt_source_id": PROMPT_SOURCE_ID,
        "source_p155_dir": str(source_dir),
        "source_p155_status": _get_ci(source.summary, "P155_STATUS", "p155_status", default=""),
        "workbench_row_count": counts["workbench_row_count"],
        "pending_human_review_count": pending,
        "accepted_for_patch_candidate_count": accepted,
        "rejected_or_deferred_count": counts["rejected_or_deferred_count"],
        "patch_candidate_created": patch_candidate_created,
        "apply_allowed": False,
        "apply_now_yes_count": 0,
        "prompt_source_modified": False,
        "blocker_count": 0 if patch_candidate_created else 1,
        "human_review_required": True,
        "google_sheets_write": False,
        "live_google_sheets_read": False,
        "public_deploy": False,
        "no_apps_script_execution": True,
        "no_clasp_push": True,
        "no_broker": True,
        "no_order": True,
        "no_sizing": True,
        "no_auto_apply_gem_response": True,
        "next": next_action,
        "output_dir": str(output_dir),
    }

    report = {
        "summary": summary,
        "decision_readback": _decision_readback_rows(source),
        "notes": [
            "P156 is an after-human-review gate.",
            "When P155 still contains pending rows, P156 must stop and produce no prompt patch candidate.",
            "No prompt source file is modified by this module.",
        ],
    }

    readback_rows = report["decision_readback"]
    if not readback_rows:
        readback_rows = [
            {
                "row_index": "",
                "decision_state": "PENDING_HUMAN_REVIEW",
                "raw_human_decision": "",
                "prompt_source_id": PROMPT_SOURCE_ID,
                "action_id": "",
                "correction_type": "",
                "field_name": "",
                "summary": "No workbench CSV rows were readable; using P155 summary counts.",
            }
        ]

    _write_json(output_dir / "P156_SUMMARY.json", summary)
    _write_json(output_dir / "P156_PROMPT_PATCH_CANDIDATE_OR_STOP_REPORT.json", report)
    _write_csv(
        output_dir / "P156_WORKBENCH_DECISION_READBACK.csv",
        readback_rows,
        [
            "row_index",
            "decision_state",
            "raw_human_decision",
            "prompt_source_id",
            "action_id",
            "correction_type",
            "field_name",
            "summary",
        ],
    )

    if patch_candidate_created:
        candidate_md = f"""# P156 Prompt Patch Candidate — Review Only

Status: `{p156_status}`

Accepted rows: `{accepted}`
Pending rows: `{pending}`

This is a prompt patch candidate only. It does not modify the source prompt and it does not apply anything automatically.

Safety:
- apply_allowed=false
- prompt_source_modified=false
- google_sheets_write=false
- public_deploy=false
- no broker / no order / no sizing
"""
        (output_dir / "P156_PROMPT_PATCH_CANDIDATE.md").write_text(candidate_md, encoding="utf-8")
    else:
        stop_md = f"""# P156 Stop — Waiting Human Review

Status: `{p156_status}`

P155 workbench rows: `{counts["workbench_row_count"]}`
Pending human review rows: `{pending}`

No prompt patch candidate was created because the P155 workbench still requires human decisions.

Next:
`{next_action}`

Safety:
- apply_allowed=false
- apply_now_yes_count=0
- prompt_source_modified=false
- google_sheets_write=false
- public_deploy=false
- no broker / no order / no sizing
"""
        (output_dir / "P156_STOP_WAITING_HUMAN_REVIEW.md").write_text(stop_md, encoding="utf-8")

    handoff_md = f"""# P156 Handoff

`{p156_status}`

Source P155:
`{source_dir}`

Next:
`{next_action}`

This batch is local/private and review-only.
"""
    (output_dir / "P156_HANDOFF.md").write_text(handoff_md, encoding="utf-8")

    return summary


def main() -> int:
    repo_root = Path.cwd()
    if not (repo_root / "pyproject.toml").exists() or not (repo_root / "mvp_qaic_py").exists():
        raise SystemExit("Run from MVP_QAIC_PY repository root.")

    summary = build_export(repo_root=repo_root)
    print(summary["p156_status"])
    print(f"prompt_source_id={summary['prompt_source_id']}")
    print(f"source_p155_status={summary['source_p155_status']}")
    print(f"workbench_row_count={summary['workbench_row_count']}")
    print(f"pending_human_review_count={summary['pending_human_review_count']}")
    print(f"accepted_for_patch_candidate_count={summary['accepted_for_patch_candidate_count']}")
    print(f"patch_candidate_created={str(summary['patch_candidate_created']).lower()}")
    print(f"apply_allowed={str(summary['apply_allowed']).lower()}")
    print(f"apply_now_yes_count={summary['apply_now_yes_count']}")
    print(f"blocker_count={summary['blocker_count']}")
    print(f"google_sheets_write={str(summary['google_sheets_write']).lower()}")
    print(f"public_deploy={str(summary['public_deploy']).lower()}")
    print(f"prompt_source_modified={str(summary['prompt_source_modified']).lower()}")
    print(f"output_dir={summary['output_dir']}")
    print(f"next={summary['next']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
