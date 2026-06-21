from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from qaic_core.contracts.migration import (
    contract_validation_result_to_dict,
    get_contract,
    validate_contract_record,
)

DECISION_JOURNAL_VERSION = "mvp_qaic.decision_journal_python.v1"

DECISION_JOURNAL_SAFETY_MARKERS: tuple[str, ...] = (
    "LOCAL_DECISION_JOURNAL_ONLY",
    "HUMAN_REVIEW_ONLY",
    "NO_GOOGLE_LIVE_WRITE",
    "NO_SHEET_WRITE",
    "NO_BROKER",
    "NO_ORDER",
    "NO_SIZING",
    "NO_SECRET",
    "EXPLICIT_PATH_REQUIRED_FOR_WRITE",
)


@dataclass(frozen=True)
class DecisionJournalEntry:
    journal_version: str
    run_id: str
    signal_id: str
    asset: str
    decision_status: str
    human_decision_only: bool
    no_order_no_sizing: bool
    risk_guard: str
    timestamp: str
    missing_data: tuple[str, ...] = field(default_factory=tuple)
    blockers: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)
    safety_markers: tuple[str, ...] = DECISION_JOURNAL_SAFETY_MARKERS


@dataclass(frozen=True)
class JournalWriteResult:
    journal_version: str
    wrote_file: bool
    path: str
    sha256: str
    bytes_written: int
    line_count: int
    validation_status: str
    safety_markers: tuple[str, ...] = DECISION_JOURNAL_SAFETY_MARKERS


def _as_tuple(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        if value.strip() == "":
            return ()
        return (value,)
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return tuple(str(item) for item in value if str(item).strip() != "")
    return (str(value),)


def _as_bool(value: object, *, default: bool = True) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    return bool(value)


def _now_utc_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def build_decision_journal_entry(
    record: Mapping[str, Any],
    *,
    run_id: str,
    timestamp: str | None = None,
    risk_guard: str | None = None,
    notes: Sequence[str] | None = None,
) -> DecisionJournalEntry:
    return DecisionJournalEntry(
        journal_version=DECISION_JOURNAL_VERSION,
        run_id=run_id,
        signal_id=str(record.get("signal_id", "")).strip(),
        asset=str(record.get("asset", "")).strip().upper(),
        decision_status=str(record.get("decision_status", "REVIEW_REQUIRED")).strip()
        or "REVIEW_REQUIRED",
        human_decision_only=_as_bool(record.get("human_decision_only"), default=True),
        no_order_no_sizing=_as_bool(record.get("no_order_no_sizing"), default=True),
        risk_guard=str(risk_guard or record.get("risk_guard", "")).strip(),
        timestamp=timestamp or _now_utc_iso(),
        missing_data=_as_tuple(record.get("missing_data")),
        blockers=_as_tuple(record.get("blockers")),
        notes=tuple(notes or _as_tuple(record.get("notes"))),
    )


def decision_journal_entry_to_dict(entry: DecisionJournalEntry) -> dict[str, object]:
    return {
        "journal_version": entry.journal_version,
        "run_id": entry.run_id,
        "signal_id": entry.signal_id,
        "asset": entry.asset,
        "decision_status": entry.decision_status,
        "human_decision_only": entry.human_decision_only,
        "no_order_no_sizing": entry.no_order_no_sizing,
        "risk_guard": entry.risk_guard,
        "timestamp": entry.timestamp,
        "missing_data": list(entry.missing_data),
        "blockers": list(entry.blockers),
        "notes": list(entry.notes),
        "safety_markers": list(entry.safety_markers),
    }


def _decision_contract_payload(entry: DecisionJournalEntry) -> dict[str, object]:
    return {
        "run_id": entry.run_id,
        "signal_id": entry.signal_id,
        "asset": entry.asset,
        "decision_status": entry.decision_status,
        "human_decision_only": entry.human_decision_only,
        "no_order_no_sizing": entry.no_order_no_sizing,
        "risk_guard": entry.risk_guard,
        "timestamp": entry.timestamp,
        "missing_data": list(entry.missing_data),
        "blockers": list(entry.blockers),
        "notes": list(entry.notes),
    }


def validate_decision_journal_entry(entry: DecisionJournalEntry) -> dict[str, object]:
    contract = get_contract("decision_journal.v1")
    result = validate_contract_record(_decision_contract_payload(entry), contract)
    return contract_validation_result_to_dict(result)


def summarize_decision_journal(
    entries: Sequence[DecisionJournalEntry],
) -> dict[str, object]:
    total = len(entries)
    blocked = sum(1 for entry in entries if entry.decision_status == "BLOCKED")
    review_required = sum(1 for entry in entries if entry.decision_status == "REVIEW_REQUIRED")
    pass_count = sum(1 for entry in entries if entry.decision_status == "PASS")
    assets = tuple(sorted({entry.asset for entry in entries if entry.asset}))

    return {
        "journal_version": DECISION_JOURNAL_VERSION,
        "entry_count": total,
        "blocked_count": blocked,
        "review_required_count": review_required,
        "pass_count": pass_count,
        "asset_count": len(assets),
        "assets": list(assets),
        "human_decision_only": True,
        "no_order_no_sizing": True,
        "safety_markers": list(DECISION_JOURNAL_SAFETY_MARKERS),
    }


def _canonical_json_line(record: Mapping[str, object]) -> str:
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def write_decision_journal_jsonl(
    *,
    entries: Sequence[DecisionJournalEntry],
    journal_dir: str | Path,
    file_name: str = "decision_journal.jsonl",
) -> JournalWriteResult:
    target_dir = Path(journal_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    for entry in entries:
        validation = validate_decision_journal_entry(entry)
        record = {
            "entry": decision_journal_entry_to_dict(entry),
            "validation": validation,
        }
        lines.append(_canonical_json_line(record))

    content = "\n".join(lines) + ("\n" if lines else "")
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    path = target_dir / file_name
    path.write_text(content, encoding="utf-8")

    validation_status = "PASS"
    if any(validate_decision_journal_entry(entry)["status"] != "PASS" for entry in entries):
        validation_status = "REVIEW_REQUIRED"

    return JournalWriteResult(
        journal_version=DECISION_JOURNAL_VERSION,
        wrote_file=True,
        path=str(path),
        sha256=digest,
        bytes_written=len(content.encode("utf-8")),
        line_count=len(lines),
        validation_status=validation_status,
    )


def journal_write_result_to_dict(result: JournalWriteResult) -> dict[str, object]:
    return {
        "journal_version": result.journal_version,
        "wrote_file": result.wrote_file,
        "path": result.path,
        "sha256": result.sha256,
        "bytes_written": result.bytes_written,
        "line_count": result.line_count,
        "validation_status": result.validation_status,
        "safety_markers": list(result.safety_markers),
    }
