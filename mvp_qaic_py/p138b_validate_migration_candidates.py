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


P138B_VERSION = "MVP_QAIC_P138B_VALIDATE_MIGRATION_CANDIDATES_20260622"
DEFAULT_RUN_ID = "P138B-VALIDATE-MIGRATION-CANDIDATES"

SAFETY_MARKERS: tuple[str, ...] = (
    "P138B_VALIDATE_MIGRATION_CANDIDATES_BEFORE_SHEETS_WRITE",
    "NO_SHEETS_WRITE_IN_P138B",
    "WRITE_IN_SHEETS_ONLY_AFTER_VALIDATION_GO",
    "PYTHON_ULTIMATE_PROCESS_SIMPLIFICATION",
    "PYTHON_OPTIMIZES_ORIGIN_SHEETS_PROCESS",
    "DEDUP_BEFORE_WRITE",
    "LOCKED_REFERENCES_PROTECTED",
    "VARIANTS_WRITTEN_AS_VARIANTS_ONLY",
    "NO_PROMPT_SOURCE_OVERWRITE",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_AUTO_APPLY_GEM_RESPONSE",
    "HUMAN_REVIEW_REQUIRED",
)

WRITE_PLAN_FIELDS: tuple[str, ...] = (
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
)


@dataclass(frozen=True)
class P138BRequest:
    candidates_json: Path
    output_dir: Path
    run_id: str = DEFAULT_RUN_ID
    generated_at_utc: str | None = None


@dataclass(frozen=True)
class P138BDecision:
    migration_id: str
    prompt_id: str
    source_tab: str
    source_row: int
    source_hash: str
    gem_id: str
    record_type: str
    target_sheet: str
    target_row_strategy: str
    p138b_decision: str
    p138b_write_action: str
    p138b_write_ready: bool
    p138c_allowed_after_go: bool
    protect_locked_reference: bool
    duplicate_prompt_id_count: int
    duplicate_source_hash_count: int
    blockers: tuple[str, ...]
    review_notes: str


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() in {"true", "yes", "1", "y", "oui"}


def _as_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value if str(item).strip())
    text = str(value).strip()
    if not text:
        return ()
    if "|" in text:
        return tuple(part.strip() for part in text.split("|") if part.strip())
    return (text,)


def load_candidates(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and "migration_candidates" in payload:
        candidates = payload["migration_candidates"]
    elif isinstance(payload, list):
        candidates = payload
    else:
        raise ValueError("Unsupported P138A candidates JSON shape")
    if not isinstance(candidates, list):
        raise ValueError("migration_candidates must be a list")
    return [dict(candidate) for candidate in candidates]


def _candidate_key(candidate: dict[str, Any], field: str) -> str:
    return str(candidate.get(field) or "").strip()


def build_duplicate_counters(candidates: list[dict[str, Any]]) -> tuple[Counter[str], Counter[str]]:
    prompt_counter: Counter[str] = Counter()
    hash_counter: Counter[str] = Counter()
    for candidate in candidates:
        prompt_id = _candidate_key(candidate, "prompt_id")
        source_hash = _candidate_key(candidate, "source_hash")
        if prompt_id:
            prompt_counter[prompt_id] += 1
        if source_hash:
            hash_counter[source_hash] += 1
    return prompt_counter, hash_counter


def classify_candidate(
    candidate: dict[str, Any],
    *,
    prompt_counter: Counter[str],
    hash_counter: Counter[str],
) -> P138BDecision:
    prompt_id = _candidate_key(candidate, "prompt_id")
    source_hash = _candidate_key(candidate, "source_hash")
    blockers = list(_as_tuple(candidate.get("blockers")))
    record_type = _candidate_key(candidate, "record_type")
    target_strategy = _candidate_key(candidate, "target_row_strategy")
    is_locked = _as_bool(candidate.get("is_reference_locked"))

    prompt_dupes = prompt_counter.get(prompt_id, 0) if prompt_id else 0
    hash_dupes = hash_counter.get(source_hash, 0) if source_hash else 0

    review_notes: list[str] = []

    if not prompt_id:
        blockers.append("PROMPT_ID_MISSING")
    if not source_hash:
        blockers.append("SOURCE_HASH_MISSING")
    if prompt_dupes > 1:
        review_notes.append(f"duplicate_prompt_id_count={prompt_dupes}")
    if hash_dupes > 1:
        review_notes.append(f"duplicate_source_hash_count={hash_dupes}")

    if blockers:
        decision = "BLOCKED_REVIEW"
        write_action = "NO_WRITE_BLOCKED"
        write_ready = False
        p138c_allowed = False
        review_notes.append("blockers_must_be_resolved_before_write")
    elif is_locked or "REFERENCE" in target_strategy.upper():
        decision = "PROTECT_LOCKED_REFERENCE"
        write_action = "NO_OVERWRITE_REFERENCE_CREATE_VARIANT_ONLY_IF_CORRECTED"
        write_ready = False
        p138c_allowed = False
        review_notes.append("locked_reference_preserved")
    elif "VARIANT" in record_type.upper() or "VARIANT" in target_strategy.upper():
        decision = "READY_FOR_VARIANT_WRITE_REVIEW"
        write_action = "APPEND_OR_UPSERT_VARIANT_AFTER_GO"
        write_ready = True
        p138c_allowed = True
    elif prompt_dupes > 1:
        decision = "REVIEW_DUPLICATE_PROMPT_ID"
        write_action = "NO_WRITE_UNTIL_DUPLICATE_DECISION"
        write_ready = False
        p138c_allowed = False
    else:
        decision = "READY_FOR_CANONICAL_WRITE_REVIEW"
        write_action = "UPSERT_BY_PROMPT_ID_AFTER_GO"
        write_ready = True
        p138c_allowed = True

    return P138BDecision(
        migration_id=_candidate_key(candidate, "migration_id"),
        prompt_id=prompt_id,
        source_tab=_candidate_key(candidate, "source_tab"),
        source_row=int(candidate.get("source_row") or 0),
        source_hash=source_hash,
        gem_id=_candidate_key(candidate, "gem_id"),
        record_type=record_type,
        target_sheet=_candidate_key(candidate, "target_sheet"),
        target_row_strategy=target_strategy,
        p138b_decision=decision,
        p138b_write_action=write_action,
        p138b_write_ready=write_ready,
        p138c_allowed_after_go=p138c_allowed,
        protect_locked_reference=is_locked,
        duplicate_prompt_id_count=prompt_dupes,
        duplicate_source_hash_count=hash_dupes,
        blockers=tuple(dict.fromkeys(blockers)),
        review_notes=" | ".join(review_notes),
    )


def validate_candidates(candidates: list[dict[str, Any]]) -> list[P138BDecision]:
    prompt_counter, hash_counter = build_duplicate_counters(candidates)
    return [
        classify_candidate(candidate, prompt_counter=prompt_counter, hash_counter=hash_counter)
        for candidate in candidates
    ]


def build_validation_payload(request: P138BRequest) -> dict[str, Any]:
    generated_at = request.generated_at_utc or _utc_now_iso()
    candidates = load_candidates(request.candidates_json)
    decisions = validate_candidates(candidates)
    decisions_dict = [asdict(decision) for decision in decisions]

    counts = Counter(decision.p138b_decision for decision in decisions)
    blockers_count = sum(1 for decision in decisions if decision.blockers)
    write_ready_count = sum(1 for decision in decisions if decision.p138b_write_ready)
    protected_reference_count = sum(
        1 for decision in decisions if decision.protect_locked_reference
    )

    blocked_count = counts.get("BLOCKED_REVIEW", 0)
    duplicate_review_count = counts.get("REVIEW_DUPLICATE_PROMPT_ID", 0)
    p138c_ready = write_ready_count > 0 and blocked_count == 0 and duplicate_review_count == 0

    return {
        "step": "P138B_VALIDATE_MIGRATION_CANDIDATES_BEFORE_SHEETS_WRITE",
        "version": P138B_VERSION,
        "status": "P138B_VALIDATION_DONE_WRITE_PLAN_READY_FOR_REVIEW",
        "generated_at_utc": generated_at,
        "run_id": request.run_id,
        "source_candidates_json": str(request.candidates_json),
        "candidate_count": len(candidates),
        "write_ready_count": write_ready_count,
        "blocked_count": blocked_count,
        "blocker_count": blockers_count,
        "protected_reference_count": protected_reference_count,
        "duplicate_review_count": duplicate_review_count,
        "decision_counts": dict(counts),
        "p138c_ready_for_write_after_go": p138c_ready,
        "p138c_gate": {
            "requires_explicit_go": True,
            "requires_human_review": True,
            "requires_no_blocked_candidates": blocked_count == 0,
            "requires_no_duplicate_review": duplicate_review_count == 0,
            "allows_partial_write_ready_subset_after_review": write_ready_count > 0,
        },
        "sheets_write_policy": {
            "p138b_sheets_write": False,
            "p138c_sheets_write_after_explicit_go": True,
            "no_blind_overwrite": True,
            "locked_references_protected": True,
        },
        "safety_markers": list(SAFETY_MARKERS),
        "write_plan_fields": list(WRITE_PLAN_FIELDS),
        "decisions": decisions_dict,
    }


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n", encoding="utf-8"
    )


def _write_write_plan_csv(path: Path, decisions: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=WRITE_PLAN_FIELDS)
        writer.writeheader()
        for decision in decisions:
            row = dict(decision)
            row["blockers"] = " | ".join(row.get("blockers") or [])
            writer.writerow({field: row.get(field, "") for field in WRITE_PLAN_FIELDS})


def _write_blockers_csv(path: Path, decisions: list[dict[str, Any]]) -> None:
    fields = ["migration_id", "prompt_id", "source_tab", "source_row", "blockers", "review_notes"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for decision in decisions:
            blockers = decision.get("blockers") or []
            if blockers:
                writer.writerow(
                    {
                        "migration_id": decision.get("migration_id", ""),
                        "prompt_id": decision.get("prompt_id", ""),
                        "source_tab": decision.get("source_tab", ""),
                        "source_row": decision.get("source_row", ""),
                        "blockers": " | ".join(blockers),
                        "review_notes": decision.get("review_notes", ""),
                    }
                )


def _write_decision_matrix_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# P138B — Migration Decision Matrix",
        "",
        f"Status: `{payload['status']}`",
        f"Candidates: `{payload['candidate_count']}`",
        f"Write-ready: `{payload['write_ready_count']}`",
        f"Blocked: `{payload['blocked_count']}`",
        f"Protected references: `{payload['protected_reference_count']}`",
        f"P138C ready after GO: `{payload['p138c_ready_for_write_after_go']}`",
        "",
        "## Decision counts",
        "",
    ]
    for key, value in sorted(payload["decision_counts"].items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Write policy",
            "",
            "- Aucun write Sheets en P138B.",
            "- P138C écrit seulement après GO explicite.",
            "- Aucun overwrite aveugle.",
            "- Les références verrouillées sont protégées.",
            "- Les variantes corrigées sont écrites comme variantes, pas comme remplacement de référence.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_write_guard_md(path: Path, payload: dict[str, Any]) -> None:
    gate = payload["p138c_gate"]
    lines = [
        "# P138B — Sheets Write Guard",
        "",
        "## Règle de write final",
        "",
        "Le write Sheets définitif est autorisé uniquement en P138C, après validation humaine et GO explicite.",
        "",
        "## Gate P138C",
        "",
    ]
    for key, value in gate.items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Safety markers", ""])
    lines.extend(f"- `{marker}`" for marker in payload["safety_markers"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_p138b_pack(request: P138BRequest) -> dict[str, Any]:
    _ensure_dir(request.output_dir)
    payload = build_validation_payload(request)
    decisions = payload["decisions"]

    _write_json(request.output_dir / "P138B_VALIDATION_PAYLOAD.json", payload)
    _write_write_plan_csv(request.output_dir / "P138B_WRITE_PLAN.csv", decisions)
    _write_json(request.output_dir / "P138B_WRITE_PLAN.json", decisions)
    _write_blockers_csv(request.output_dir / "P138B_BLOCKERS.csv", decisions)
    _write_decision_matrix_md(request.output_dir / "P138B_MIGRATION_DECISION_MATRIX.md", payload)
    _write_write_guard_md(request.output_dir / "P138B_WRITE_GUARD.md", payload)

    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="P138B validate migration candidates before Sheets write"
    )
    parser.add_argument("--candidates-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--generated-at-utc", default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = write_p138b_pack(
        P138BRequest(
            candidates_json=args.candidates_json,
            output_dir=args.output_dir,
            run_id=args.run_id,
            generated_at_utc=args.generated_at_utc,
        )
    )
    print(payload["status"])
    print(f"candidate_count={payload['candidate_count']}")
    print(f"write_ready_count={payload['write_ready_count']}")
    print(f"blocked_count={payload['blocked_count']}")
    print(f"p138c_ready_for_write_after_go={payload['p138c_ready_for_write_after_go']}")
    print(f"output_dir={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
