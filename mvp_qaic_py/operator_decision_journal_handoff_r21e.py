"""R21E operator decision journal handoff for MVP QAIC.

No runtime, no provider call, no broker/order/sizing, no Sheet/BQ write.
This module prepares review-only local handoff records from the operator
workflow to the decision journal and the QAIC review bridge.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import UTC, datetime
from typing import Any

SCHEMA_ID = "R21E_OPERATOR_DECISION_JOURNAL_HANDOFF_NO_RUNTIME"
HANDOFF_MODE = "REVIEW_ONLY_LOCAL_HANDOFF"
QAIC_IMPORT_MODE = "LOCAL_REVIEW_ONLY"
DEFAULT_SOURCE = "MVP_QAIC_OPERATOR_WORKFLOW"

SAFETY_FLAGS: dict[str, bool] = {
    "no_runtime": True,
    "no_provider_call": True,
    "no_broker_order_sizing": True,
    "no_sheet_bq_write": True,
    "human_review_required": True,
    "qaic_execution_allowed": False,
}


@dataclass(frozen=True)
class DecisionJournalHandoff:
    """Single review-only handoff record for the operator decision journal."""

    schema_id: str
    created_at_utc: str
    source: str
    operator_decision: str
    qaic_bridge_status: str
    handoff_mode: str
    qaic_import_mode: str
    human_review_required: bool
    qaic_execution_allowed: bool
    no_runtime: bool
    no_provider_call: bool
    no_broker_order_sizing: bool
    no_sheet_bq_write: bool
    notes: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def utc_now_iso() -> str:
    """Return a stable UTC timestamp for local records."""

    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_decision_journal_entry(
    operator_decision: str,
    qaic_bridge_status: str,
    notes: str = "",
    source: str = DEFAULT_SOURCE,
    created_at_utc: str | None = None,
) -> dict[str, Any]:
    """Build a review-only decision journal handoff entry."""

    entry = DecisionJournalHandoff(
        schema_id=SCHEMA_ID,
        created_at_utc=created_at_utc or utc_now_iso(),
        source=source.strip(),
        operator_decision=operator_decision.strip(),
        qaic_bridge_status=qaic_bridge_status.strip(),
        handoff_mode=HANDOFF_MODE,
        qaic_import_mode=QAIC_IMPORT_MODE,
        human_review_required=SAFETY_FLAGS["human_review_required"],
        qaic_execution_allowed=SAFETY_FLAGS["qaic_execution_allowed"],
        no_runtime=SAFETY_FLAGS["no_runtime"],
        no_provider_call=SAFETY_FLAGS["no_provider_call"],
        no_broker_order_sizing=SAFETY_FLAGS["no_broker_order_sizing"],
        no_sheet_bq_write=SAFETY_FLAGS["no_sheet_bq_write"],
        notes=notes.strip(),
    ).to_dict()
    return entry


def validate_decision_journal_entry(entry: dict[str, Any]) -> list[str]:
    """Return validation errors for a decision journal handoff entry."""

    errors: list[str] = []
    required = [
        "schema_id",
        "created_at_utc",
        "source",
        "operator_decision",
        "qaic_bridge_status",
        "handoff_mode",
        "qaic_import_mode",
    ]
    for key in required:
        if not str(entry.get(key, "")).strip():
            errors.append(f"missing_or_empty:{key}")

    if entry.get("schema_id") != SCHEMA_ID:
        errors.append("invalid_schema_id")
    if entry.get("handoff_mode") != HANDOFF_MODE:
        errors.append("invalid_handoff_mode")
    if entry.get("qaic_import_mode") != QAIC_IMPORT_MODE:
        errors.append("invalid_qaic_import_mode")

    for key, expected in SAFETY_FLAGS.items():
        if entry.get(key) is not expected:
            errors.append(f"invalid_safety_flag:{key}")

    forbidden_true = [
        "runtime_used",
        "provider_call_used",
        "broker_order_sizing_used",
        "sheet_bq_write_used",
        "apps_script_execution_used",
    ]
    for key in forbidden_true:
        if entry.get(key) is True:
            errors.append(f"forbidden_true:{key}")

    return errors


def build_review_queue_item(entry: dict[str, Any]) -> dict[str, str]:
    """Build a compact row suitable for a local review queue."""

    errors = validate_decision_journal_entry(entry)
    return {
        "schema_id": str(entry.get("schema_id", "")),
        "created_at_utc": str(entry.get("created_at_utc", "")),
        "operator_decision": str(entry.get("operator_decision", "")),
        "qaic_bridge_status": str(entry.get("qaic_bridge_status", "")),
        "review_state": "blocked" if errors else "ready_for_human_review",
        "validation_errors": ";".join(errors),
        "handoff_mode": str(entry.get("handoff_mode", "")),
        "qaic_execution_allowed": str(entry.get("qaic_execution_allowed", "")),
    }


def render_handoff_markdown(entry: dict[str, Any]) -> str:
    """Render a plain Markdown handoff summary without HTML."""

    errors = validate_decision_journal_entry(entry)
    lines = [
        "# R21E Operator Decision Journal Handoff",
        "",
        f"- Schema: {entry.get('schema_id', '')}",
        f"- Created UTC: {entry.get('created_at_utc', '')}",
        f"- Source: {entry.get('source', '')}",
        f"- Operator decision: {entry.get('operator_decision', '')}",
        f"- QAIC bridge status: {entry.get('qaic_bridge_status', '')}",
        f"- Handoff mode: {entry.get('handoff_mode', '')}",
        f"- QAIC import mode: {entry.get('qaic_import_mode', '')}",
        "",
        "## Safety flags",
    ]
    for key in sorted(SAFETY_FLAGS):
        lines.append(f"- {key}: {entry.get(key)}")
    lines.extend(
        [
            "",
            "## Validation",
            f"- Status: {'PASS' if not errors else 'BLOCKED'}",
            f"- Errors: {'none' if not errors else '; '.join(errors)}",
            "",
            "## Notes",
            entry.get("notes", "") or "none",
            "",
        ]
    )
    return "\n".join(lines)


def build_sample_entry() -> dict[str, Any]:
    """Return a deterministic sample entry for docs and tests."""

    return build_decision_journal_entry(
        operator_decision="prepare_qaic_review",
        qaic_bridge_status="READY_FOR_QAIC_REVIEW_ONLY_HANDOFF",
        notes="No runtime. No provider call. Human review required before any QAIC import.",
        created_at_utc="2026-07-01T00:00:00Z",
    )