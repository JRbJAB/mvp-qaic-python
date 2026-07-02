"""R21R Reflex publication preview strategy audit for MVP QAIC.

This module is a pure, import-safe payload builder. It binds the R21Q product
continuation final seal to a docs-only strategy audit without creating a
runtime runner, launching Reflex execution, using Docker, calling providers,
touching broker/order/sizing paths, writing Sheet/BQ targets, emitting HTML, or
creating export artifacts.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from mvp_qaic_py.product_continuation_final_seal_r21q import (
    build_product_continuation_with_sources,
)

AUDIT_ID: Final[str] = "R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT_DOCS_ONLY"
READY_STATUS: Final[str] = "READY"
PAUSED_STATUS: Final[str] = "PAUSED"
STOPPED_STATUS: Final[str] = "STOPPED"
NEXT_STEP: Final[str] = "R21S_REFLEX_PREVIEW_RUNNER_SPEC_REVIEW_ONLY"

SOURCE_BINDINGS: Final[dict[str, bool]] = {
    "SOURCE_R21Q_PRODUCT_CONTINUATION_BOUND": True,
}

RUNTIME_BOUNDARY_FLAGS: Final[dict[str, bool | str]] = {
    "R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT": READY_STATUS,
    "REFLEX_RUNTIME_STATUS": PAUSED_STATUS,
    "REFLEX_RUNTIME_RUNNER_CHAIN": STOPPED_STATUS,
    "FALLBACK_STATIC_WYSIWYG_ALLOWED": True,
    "REFLEX_ALLOWED_NEXT_ONLY_AFTER_HUMAN_RUNNER_REVIEW": True,
}

PREVIEW_AUDIT_GATES: Final[dict[str, bool]] = {
    "NO_DOCS_NO_ACTION": True,
    "NO_HELP_NO_RUNTIME": True,
    "HELP_FLAG_MISSING_COMMAND_FORBIDDEN": True,
    "TCP_ONLY_NOT_PREVIEW_READY": True,
    "HTTP_FAIL_STOP_AND_DIAG": True,
    "PREVIEW_ONLY_AFTER_HTTP_PASS": True,
    "HTTP_FRONTEND_NON_EMPTY_REQUIRED": True,
    "REFLEX_CLI_HELP_CAPTURE_REQUIRED": True,
    "REFLEX_VERSION_CAPTURE_REQUIRED": True,
    "NO_FRONTEND_HOST_FLAG": True,
}

SAFETY_LOCKS: Final[dict[str, bool]] = {
    "NO_PUBLIC_DEPLOY": True,
    "NO_REFLEX_DEPLOY": True,
    "NO_RUNTIME": True,
    "NO_DOCKER": True,
    "NO_REFLEX_RUN": True,
    "NO_PROVIDER_CALL": True,
    "NO_BROKER_ORDER_SIZING": True,
    "NO_SHEET_BQ_WRITE": True,
    "NO_HTML_OUTPUT": True,
}

REQUIRED_AUDIT_IDS: Final[tuple[str, ...]] = (
    "r21q_product_continuation_bound",
    "runtime_paused_boundary",
    "preview_evidence_gate",
    "cli_help_version_capture_gate",
    "publication_deploy_lock",
    "r21s_next_step",
)


@dataclass(frozen=True)
class PreviewStrategyAuditEntry:
    """Single deterministic R21R preview strategy audit entry."""

    audit_entry_id: str
    title: str
    source_reference: str
    audit_token: str
    status: str
    human_review_required: bool
    qaic_execution_allowed: bool
    ordinal: int


@dataclass(frozen=True)
class PreviewStrategyAudit:
    """Top-level R21R preview strategy audit object."""

    audit_id: str
    status: str
    source_bindings: dict[str, bool]
    runtime_boundary_flags: dict[str, bool | str]
    preview_audit_gates: dict[str, bool]
    safety_locks: dict[str, bool]
    audit_entries: tuple[PreviewStrategyAuditEntry, ...]
    next_step: str


def _build_audit_entries() -> tuple[PreviewStrategyAuditEntry, ...]:
    """Build stable preview strategy audit entries."""
    entries = (
        PreviewStrategyAuditEntry(
            "r21q_product_continuation_bound",
            "R21Q product continuation final seal is bound",
            "docs/PRODUCT/R21Q_PRODUCT_CONTINUATION_FINAL_SEAL_NO_RUNTIME.md",
            "SOURCE_R21Q_PRODUCT_CONTINUATION_BOUND",
            "bound",
            True,
            False,
            10,
        ),
        PreviewStrategyAuditEntry(
            "runtime_paused_boundary",
            "Reflex runtime and runner chain remain stopped",
            "docs/FINAL/R21B_REFLEX_RUNTIME_CLOSURE_STRATEGY_AND_INSTRUCTIONS_MEMO_20260701.md",
            "REFLEX_RUNTIME_STATUS",
            "paused",
            True,
            False,
            20,
        ),
        PreviewStrategyAuditEntry(
            "preview_evidence_gate",
            "HTTP frontend evidence must pass and be non-empty",
            "docs/RUNTIME/REFLEX_CLI_CONTRACT_H8I.md",
            "HTTP_FRONTEND_NON_EMPTY_REQUIRED",
            "locked",
            True,
            False,
            30,
        ),
        PreviewStrategyAuditEntry(
            "cli_help_version_capture_gate",
            "CLI help and version capture are required in R21S review",
            "docs/RUNTIME/REFLEX_RUNNER_HARDENING_POLICY_R16F2H7I.md",
            "REFLEX_CLI_HELP_CAPTURE_REQUIRED",
            "required_next",
            True,
            False,
            40,
        ),
        PreviewStrategyAuditEntry(
            "publication_deploy_lock",
            "Publication deployment paths remain closed",
            "docs/PROCESS/ASSISTANT_REFLEX_INSTRUCTION_LOCK_R16F2H4.md",
            "NO_PUBLIC_DEPLOY",
            "locked",
            True,
            False,
            50,
        ),
        PreviewStrategyAuditEntry(
            "r21s_next_step",
            "R21S preview runner specification review only",
            NEXT_STEP,
            "NEXT",
            "next",
            True,
            False,
            60,
        ),
    )
    return tuple(sorted(entries, key=lambda entry: entry.ordinal))


def build_preview_strategy_audit() -> PreviewStrategyAudit:
    """Build the R21R preview strategy audit."""
    return PreviewStrategyAudit(
        audit_id=AUDIT_ID,
        status="R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT=READY",
        source_bindings=dict(SOURCE_BINDINGS),
        runtime_boundary_flags=dict(RUNTIME_BOUNDARY_FLAGS),
        preview_audit_gates=dict(PREVIEW_AUDIT_GATES),
        safety_locks=dict(SAFETY_LOCKS),
        audit_entries=_build_audit_entries(),
        next_step=NEXT_STEP,
    )


def audit_to_dict(audit: PreviewStrategyAudit | None = None) -> dict[str, Any]:
    """Return the preview strategy audit as a JSON-friendly dictionary."""
    if audit is None:
        audit = build_preview_strategy_audit()

    return {
        "audit_id": audit.audit_id,
        "status": audit.status,
        "R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT": READY_STATUS,
        "source_bindings": dict(audit.source_bindings),
        "runtime_boundary_flags": dict(audit.runtime_boundary_flags),
        "preview_audit_gates": dict(audit.preview_audit_gates),
        "safety_locks": dict(audit.safety_locks),
        "audit_entries": [asdict(entry) for entry in audit.audit_entries],
        "next_step": audit.next_step,
    }


def build_preview_strategy_audit_with_sources() -> dict[str, Any]:
    """Build the R21R payload with bound source summaries."""
    r21q = build_product_continuation_with_sources()
    audit = audit_to_dict()

    return {
        **audit,
        "source_summaries": {
            "r21q_product_continuation": r21q["seal_id"],
            "r21q_status": r21q["PRODUCT_CONTINUATION_FINAL_SEAL"],
            "r21q_next_step": r21q["next_step"],
        },
    }


def validate_preview_strategy_audit(payload: dict[str, Any] | None = None) -> tuple[str, ...]:
    """Return validation errors. Empty tuple means the R21R payload is valid."""
    if payload is None:
        payload = build_preview_strategy_audit_with_sources()

    errors: list[str] = []
    if payload.get("audit_id") != AUDIT_ID:
        errors.append("audit_id_mismatch")
    if payload.get("R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT") != READY_STATUS:
        errors.append("preview_strategy_audit_not_ready")

    source_bindings = payload.get("source_bindings")
    if not isinstance(source_bindings, dict):
        errors.append("missing_source_bindings")
    else:
        for key, expected in SOURCE_BINDINGS.items():
            if source_bindings.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    runtime_boundary_flags = payload.get("runtime_boundary_flags")
    if not isinstance(runtime_boundary_flags, dict):
        errors.append("missing_runtime_boundary_flags")
    else:
        for key, expected in RUNTIME_BOUNDARY_FLAGS.items():
            if runtime_boundary_flags.get(key) != expected:
                errors.append(f"{key}_mismatch")

    preview_audit_gates = payload.get("preview_audit_gates")
    if not isinstance(preview_audit_gates, dict):
        errors.append("missing_preview_audit_gates")
    else:
        for key, expected in PREVIEW_AUDIT_GATES.items():
            if preview_audit_gates.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    safety_locks = payload.get("safety_locks")
    if not isinstance(safety_locks, dict):
        errors.append("missing_safety_locks")
    else:
        for key, expected in SAFETY_LOCKS.items():
            if safety_locks.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    audit_entries = payload.get("audit_entries")
    if not isinstance(audit_entries, list):
        errors.append("missing_audit_entries")
    else:
        entry_ids = {entry.get("audit_entry_id") for entry in audit_entries if isinstance(entry, dict)}
        if set(REQUIRED_AUDIT_IDS) - entry_ids:
            errors.append("missing_audit_entries")
        ordinals = [entry.get("ordinal") for entry in audit_entries if isinstance(entry, dict)]
        if ordinals != sorted(ordinals):
            errors.append("audit_entries_not_deterministic")
        for entry in audit_entries:
            if not isinstance(entry, dict):
                errors.append("invalid_audit_entry")
                continue
            if entry.get("human_review_required") is not True:
                errors.append(f"human_review_missing={entry.get('audit_entry_id')}")
            if entry.get("qaic_execution_allowed") is not False:
                errors.append(f"execution_open={entry.get('audit_entry_id')}")

    summaries = payload.get("source_summaries")
    if isinstance(summaries, dict):
        if summaries.get("r21q_product_continuation") != (
            "R21Q_PRODUCT_CONTINUATION_FINAL_SEAL_NO_RUNTIME"
        ):
            errors.append("r21q_source_mismatch")
        if summaries.get("r21q_status") != READY_STATUS:
            errors.append("r21q_status_mismatch")

    if payload.get("next_step") != NEXT_STEP:
        errors.append("next_step_mismatch")

    return tuple(errors)


def render_preview_strategy_markdown(payload: dict[str, Any] | None = None) -> str:
    """Render the R21R preview strategy audit as markdown text only."""
    if payload is None:
        payload = build_preview_strategy_audit_with_sources()

    lines = [
        "# R21R Reflex Publication Preview Strategy Audit - Docs Only",
        "",
        f"Status: `{payload['status']}`",
        "",
        "## Source Bindings",
    ]
    for key in sorted(payload["source_bindings"]):
        lines.append(f"- `{key}` = `{payload['source_bindings'][key]}`")

    lines.extend(["", "## Runtime Boundary"])
    for key in sorted(payload["runtime_boundary_flags"]):
        lines.append(f"- `{key}` = `{payload['runtime_boundary_flags'][key]}`")

    lines.extend(["", "## Preview Audit Gates"])
    for key in sorted(payload["preview_audit_gates"]):
        lines.append(f"- `{key}` = `{payload['preview_audit_gates'][key]}`")

    lines.extend(["", "## Safety Locks"])
    for key in sorted(payload["safety_locks"]):
        lines.append(f"- `{key}` = `{payload['safety_locks'][key]}`")

    lines.extend(["", "## Audit Entries"])
    for entry in payload["audit_entries"]:
        lines.append(
            "- "
            f"`{entry['audit_entry_id']}` - {entry['title']} - "
            f"`{entry['audit_token']}` - `{entry['status']}`"
        )

    lines.extend(["", f"NEXT={payload['next_step']}"])
    return "\n".join(lines) + "\n"
