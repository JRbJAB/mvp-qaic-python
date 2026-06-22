from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


P138B3_VERSION = "MVP_QAIC_P138B3_WRITE_READINESS_TRIAGE_20260622"
DEFAULT_RUN_ID = "P138B3-WRITE-READINESS-TRIAGE"

SAFETY_MARKERS: tuple[str, ...] = (
    "P138B3_WRITE_READINESS_TRIAGE_BEFORE_P138C",
    "NO_SHEETS_WRITE_IN_P138B3",
    "WRITE_IN_SHEETS_ONLY_AFTER_VALIDATION_GO",
    "SAFE_PARTIAL_WRITE_READY_SCOPE_ONLY",
    "BLOCKED_ROWS_EXCLUDED_FROM_WRITE",
    "DUPLICATES_REVIEW_EXCLUDED_FROM_WRITE",
    "LOCKED_REFERENCES_PROTECTED",
    "VARIANTS_WRITTEN_AS_VARIANTS_ONLY",
    "NO_PROMPT_SOURCE_OVERWRITE",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_AUTO_APPLY_GEM_RESPONSE",
    "HUMAN_REVIEW_REQUIRED",
)

READY_DECISIONS: tuple[str, ...] = (
    "READY_FOR_CANONICAL_WRITE_REVIEW",
    "READY_FOR_VARIANT_WRITE_REVIEW",
)

BLOCKED_DECISIONS: tuple[str, ...] = ("BLOCKED_REVIEW",)

DUPLICATE_DECISIONS: tuple[str, ...] = ("REVIEW_DUPLICATE_PROMPT_ID",)

PROTECTED_REFERENCE_DECISIONS: tuple[str, ...] = ("PROTECT_LOCKED_REFERENCE",)


@dataclass(frozen=True)
class P138B3Request:
    p138b_export_dir: Path
    output_dir: Path
    run_id: str = DEFAULT_RUN_ID
    generated_at_utc: str | None = None


@dataclass(frozen=True)
class TriageBucket:
    name: str
    count: int
    write_allowed_in_p138c_after_go: bool
    description: str


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n", encoding="utf-8"
    )


def load_p138b_export(p138b_export_dir: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payload_path = p138b_export_dir / "P138B_VALIDATION_PAYLOAD.json"
    write_plan_path = p138b_export_dir / "P138B_WRITE_PLAN.json"
    if not payload_path.exists():
        raise FileNotFoundError(f"Missing P138B payload: {payload_path}")
    if not write_plan_path.exists():
        raise FileNotFoundError(f"Missing P138B write plan JSON: {write_plan_path}")
    payload = _load_json(payload_path)
    write_plan = _load_json(write_plan_path)
    if not isinstance(payload, dict):
        raise ValueError("P138B payload must be a dict")
    if not isinstance(write_plan, list):
        raise ValueError("P138B write plan must be a list")
    return payload, [dict(row) for row in write_plan]


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() in {"true", "1", "yes", "y", "oui"}


def _normalise_blockers(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    text = str(value or "").strip()
    if not text:
        return []
    return [part.strip() for part in text.split("|") if part.strip()]


def triage_rows(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    safe_ready: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    duplicate_review: list[dict[str, Any]] = []
    protected_references: list[dict[str, Any]] = []
    other_review: list[dict[str, Any]] = []

    for row in rows:
        decision = str(row.get("p138b_decision") or "").strip()
        write_ready = _as_bool(row.get("p138b_write_ready"))
        p138c_allowed = _as_bool(row.get("p138c_allowed_after_go"))
        blockers = _normalise_blockers(row.get("blockers"))

        enriched = dict(row)
        enriched["blockers"] = blockers
        enriched["p138b_write_ready"] = write_ready
        enriched["p138c_allowed_after_go"] = p138c_allowed

        if decision in READY_DECISIONS and write_ready and p138c_allowed and not blockers:
            enriched["p138b3_bucket"] = "SAFE_PARTIAL_WRITE_READY"
            safe_ready.append(enriched)
        elif decision in BLOCKED_DECISIONS or blockers:
            enriched["p138b3_bucket"] = "BLOCKED_REVIEW"
            blocked.append(enriched)
        elif decision in DUPLICATE_DECISIONS:
            enriched["p138b3_bucket"] = "DUPLICATE_REVIEW"
            duplicate_review.append(enriched)
        elif decision in PROTECTED_REFERENCE_DECISIONS:
            enriched["p138b3_bucket"] = "PROTECTED_REFERENCE_NO_WRITE"
            protected_references.append(enriched)
        else:
            enriched["p138b3_bucket"] = "OTHER_REVIEW"
            other_review.append(enriched)

    return {
        "safe_partial_write_ready": safe_ready,
        "blocked_review": blocked,
        "duplicate_review": duplicate_review,
        "protected_references": protected_references,
        "other_review": other_review,
    }


def build_triage_payload(request: P138B3Request) -> dict[str, Any]:
    generated_at = request.generated_at_utc or _utc_now_iso()
    p138b_payload, write_plan = load_p138b_export(request.p138b_export_dir)
    buckets = triage_rows(write_plan)

    safe_ready = buckets["safe_partial_write_ready"]
    blocked = buckets["blocked_review"]
    duplicates = buckets["duplicate_review"]
    protected = buckets["protected_references"]
    other = buckets["other_review"]

    decision_counts = Counter(str(row.get("p138b_decision") or "") for row in write_plan)
    action_counts = Counter(str(row.get("p138b_write_action") or "") for row in write_plan)

    p138c_safe_partial_scope_ready = len(safe_ready) > 0
    p138c_full_scope_ready = len(safe_ready) == len(write_plan) and len(write_plan) > 0

    buckets_summary = [
        TriageBucket(
            name="SAFE_PARTIAL_WRITE_READY",
            count=len(safe_ready),
            write_allowed_in_p138c_after_go=p138c_safe_partial_scope_ready,
            description="Rows that can enter a partial P138C write scope after explicit human GO.",
        ),
        TriageBucket(
            name="BLOCKED_REVIEW",
            count=len(blocked),
            write_allowed_in_p138c_after_go=False,
            description="Rows excluded from write until blockers are resolved.",
        ),
        TriageBucket(
            name="DUPLICATE_REVIEW",
            count=len(duplicates),
            write_allowed_in_p138c_after_go=False,
            description="Rows excluded from write until duplicate arbitration is done.",
        ),
        TriageBucket(
            name="PROTECTED_REFERENCE_NO_WRITE",
            count=len(protected),
            write_allowed_in_p138c_after_go=False,
            description="Locked/reference rows protected from overwrite.",
        ),
        TriageBucket(
            name="OTHER_REVIEW",
            count=len(other),
            write_allowed_in_p138c_after_go=False,
            description="Rows requiring manual review before any write.",
        ),
    ]

    return {
        "step": "P138B3_WRITE_READINESS_TRIAGE_BEFORE_P138C",
        "version": P138B3_VERSION,
        "status": "P138B3_TRIAGE_DONE_SAFE_PARTIAL_SCOPE_READY"
        if p138c_safe_partial_scope_ready
        else "P138B3_TRIAGE_DONE_REVIEW_REQUIRED_BEFORE_WRITE",
        "generated_at_utc": generated_at,
        "run_id": request.run_id,
        "source_p138b_export_dir": str(request.p138b_export_dir),
        "source_p138b_status": p138b_payload.get("status"),
        "candidate_count": len(write_plan),
        "safe_partial_write_ready_count": len(safe_ready),
        "blocked_review_count": len(blocked),
        "duplicate_review_count": len(duplicates),
        "protected_reference_count": len(protected),
        "other_review_count": len(other),
        "p138c_safe_partial_scope_ready": p138c_safe_partial_scope_ready,
        "p138c_full_scope_ready": p138c_full_scope_ready,
        "p138c_write_mode_recommendation": "SAFE_PARTIAL_WRITE_READY_AFTER_GO"
        if p138c_safe_partial_scope_ready
        else "REVIEW_REQUIRED_BEFORE_WRITE",
        "p138c_excluded_count": len(blocked) + len(duplicates) + len(protected) + len(other),
        "decision_counts": dict(decision_counts),
        "write_action_counts": dict(action_counts),
        "buckets": [asdict(bucket) for bucket in buckets_summary],
        "sheets_write_policy": {
            "p138b3_sheets_write": False,
            "p138c_sheets_write_after_explicit_go": True,
            "safe_partial_write_only": p138c_safe_partial_scope_ready,
            "full_scope_write_allowed": p138c_full_scope_ready,
            "blocked_rows_excluded": True,
            "duplicate_rows_excluded": True,
            "locked_references_excluded": True,
            "no_blind_overwrite": True,
        },
        "safety_markers": list(SAFETY_MARKERS),
        "outputs": {
            "safe_partial_write_ready": "P138B3_SAFE_PARTIAL_WRITE_READY.csv",
            "blocked_review": "P138B3_BLOCKED_REVIEW.csv",
            "duplicate_review": "P138B3_DUPLICATE_REVIEW.csv",
            "protected_references": "P138B3_PROTECTED_REFERENCES.csv",
            "triage_payload": "P138B3_TRIAGE_PAYLOAD.json",
            "p138c_scope": "P138B3_P138C_WRITE_SCOPE.md",
            "prewrite_checklist": "P138B3_P138C_PREWRITE_CHECKLIST.md",
        },
    }


def _csv_fields(rows: list[dict[str, Any]]) -> list[str]:
    base = [
        "p138b3_bucket",
        "migration_id",
        "prompt_id",
        "source_tab",
        "source_row",
        "source_hash",
        "gem_id",
        "record_type",
        "target_sheet",
        "target_row_strategy",
        "p138b_decision",
        "p138b_write_action",
        "p138b_write_ready",
        "p138c_allowed_after_go",
        "protect_locked_reference",
        "duplicate_prompt_id_count",
        "duplicate_source_hash_count",
        "blockers",
        "review_notes",
    ]
    seen = set(base)
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                base.append(key)
    return base


def _write_rows_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = _csv_fields(rows)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            blockers = out.get("blockers")
            if isinstance(blockers, list):
                out["blockers"] = " | ".join(str(item) for item in blockers)
            writer.writerow({field: out.get(field, "") for field in fields})


def _write_scope_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# P138B3 — P138C Write Scope",
        "",
        f"Status: `{payload['status']}`",
        f"Recommendation: `{payload['p138c_write_mode_recommendation']}`",
        "",
        "## Counts",
        "",
        f"- Candidates: `{payload['candidate_count']}`",
        f"- Safe partial write-ready: `{payload['safe_partial_write_ready_count']}`",
        f"- Blocked review: `{payload['blocked_review_count']}`",
        f"- Duplicate review: `{payload['duplicate_review_count']}`",
        f"- Protected references: `{payload['protected_reference_count']}`",
        f"- Other review: `{payload['other_review_count']}`",
        f"- Excluded from P138C scope: `{payload['p138c_excluded_count']}`",
        "",
        "## P138C rule",
        "",
        "P138C may write only the rows contained in `P138B3_SAFE_PARTIAL_WRITE_READY.csv`, and only after explicit GO.",
        "All blocked, duplicate, protected-reference and other-review rows are excluded from write.",
        "",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_checklist_md(path: Path, payload: dict[str, Any]) -> None:
    checks = [
        ("Open P138B3_SAFE_PARTIAL_WRITE_READY.csv", payload["safe_partial_write_ready_count"] > 0),
        ("Confirm partial write scope is intended", payload["p138c_safe_partial_scope_ready"]),
        ("Confirm no blocked rows are included in write scope", True),
        ("Confirm no duplicate-review rows are included in write scope", True),
        ("Confirm no protected references are overwritten", True),
        ("Confirm explicit GO before P138C", False),
    ]
    lines = [
        "# P138B3 — P138C Prewrite Checklist",
        "",
        "| Check | Current status |",
        "|---|---:|",
    ]
    for label, value in checks:
        lines.append(f"| {label} | `{value}` |")
    lines.extend(["", "Safety markers:", ""])
    lines.extend(f"- `{marker}`" for marker in payload["safety_markers"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_p138b3_pack(request: P138B3Request) -> dict[str, Any]:
    _ensure_dir(request.output_dir)
    payload = build_triage_payload(request)
    _, write_plan = load_p138b_export(request.p138b_export_dir)
    buckets = triage_rows(write_plan)

    _write_json(request.output_dir / "P138B3_TRIAGE_PAYLOAD.json", payload)
    _write_rows_csv(
        request.output_dir / "P138B3_SAFE_PARTIAL_WRITE_READY.csv",
        buckets["safe_partial_write_ready"],
    )
    _write_json(
        request.output_dir / "P138B3_SAFE_PARTIAL_WRITE_READY.json",
        buckets["safe_partial_write_ready"],
    )
    _write_rows_csv(request.output_dir / "P138B3_BLOCKED_REVIEW.csv", buckets["blocked_review"])
    _write_rows_csv(request.output_dir / "P138B3_DUPLICATE_REVIEW.csv", buckets["duplicate_review"])
    _write_rows_csv(
        request.output_dir / "P138B3_PROTECTED_REFERENCES.csv", buckets["protected_references"]
    )
    _write_rows_csv(request.output_dir / "P138B3_OTHER_REVIEW.csv", buckets["other_review"])
    _write_scope_md(request.output_dir / "P138B3_P138C_WRITE_SCOPE.md", payload)
    _write_checklist_md(request.output_dir / "P138B3_P138C_PREWRITE_CHECKLIST.md", payload)

    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="P138B3 triage P138B write readiness before P138C")
    parser.add_argument("--p138b-export-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--generated-at-utc", default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = write_p138b3_pack(
        P138B3Request(
            p138b_export_dir=args.p138b_export_dir,
            output_dir=args.output_dir,
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(payload["status"])
    print(f"candidate_count={payload['candidate_count']}")
    print(f"safe_partial_write_ready_count={payload['safe_partial_write_ready_count']}")
    print(f"blocked_review_count={payload['blocked_review_count']}")
    print(f"duplicate_review_count={payload['duplicate_review_count']}")
    print(f"protected_reference_count={payload['protected_reference_count']}")
    print(f"p138c_safe_partial_scope_ready={payload['p138c_safe_partial_scope_ready']}")
    print(f"p138c_write_mode_recommendation={payload['p138c_write_mode_recommendation']}")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
