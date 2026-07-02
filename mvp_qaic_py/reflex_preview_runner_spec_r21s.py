"""R21S Reflex preview runner specification review-only payload.

This module is deterministic metadata only. It specifies the future private
preview runner review boundary while keeping runtime activity closed.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from mvp_qaic_py.reflex_publication_preview_strategy_r21r import (
    build_preview_strategy_audit_with_sources,
)

SPEC_ID: Final[str] = "R21S_REFLEX_PREVIEW_RUNNER_SPEC_REVIEW_ONLY"
READY_STATUS: Final[str] = "READY"
PAUSED_STATUS: Final[str] = "PAUSED"
STOPPED_UNTIL_APPROVAL: Final[str] = "STOPPED_UNTIL_HUMAN_APPROVAL"
NEXT_STEP: Final[str] = "R21T_HUMAN_APPROVED_PRIVATE_PREVIEW_ATTEMPT_ONLY"

SOURCE_BINDINGS: Final[dict[str, bool]] = {
    "SOURCE_R21R_PREVIEW_STRATEGY_BOUND": True,
}

REVIEW_ONLY_TOKENS: Final[dict[str, bool | str]] = {
    "R21S_REFLEX_PREVIEW_RUNNER_SPEC": READY_STATUS,
    "SOURCE_R21R_PREVIEW_STRATEGY_BOUND": True,
    "RUNNER_SPEC_REVIEW_ONLY": True,
    "RUNNER_EXECUTED": False,
    "REFLEX_RUNTIME_STATUS": PAUSED_STATUS,
    "REFLEX_RUNTIME_RUNNER_CHAIN": STOPPED_UNTIL_APPROVAL,
    "HUMAN_APPROVED_PRIVATE_PREVIEW_REQUIRED": True,
    "REFLEX_CLI_HELP_CAPTURE_REQUIRED": True,
    "REFLEX_VERSION_CAPTURE_REQUIRED": True,
    "NO_FRONTEND_HOST_FLAG": True,
    "NO_PUBLIC_DEPLOY": True,
    "NO_REFLEX_DEPLOY": True,
    "PS51_COMPATIBLE": True,
    "PROMPT_MD_REQUIRED": True,
    "RUNNER_SHORT_REQUIRED": True,
    "NO_GIANT_CONSOLE_PROMPT": True,
    "TARGETED_STAGING_ONLY": True,
    "NO_GIT_ADD_DOT": True,
    "NO_RESET": True,
    "DIRTY_START_STOP_NO_WRITE": True,
    "FAILED_TESTS_NO_COMMIT_NO_TAG_NO_PUSH": True,
    "HTTP_FRONTEND_NON_EMPTY_REQUIRED": True,
    "TCP_ONLY_NOT_PREVIEW_READY": True,
    "PREVIEW_ONLY_AFTER_HTTP_PASS": True,
    "HTTP_FAIL_STOP_AND_DIAG": True,
    "NO_RUNTIME": True,
    "NO_DOCKER": True,
    "NO_REFLEX_RUN": True,
    "NO_PROVIDER_CALL": True,
    "NO_BROKER_ORDER_SIZING": True,
    "NO_SHEET_BQ_WRITE": True,
    "NO_HTML_OUTPUT": True,
    "NEXT": NEXT_STEP,
}

REQUIRED_PHASES: Final[tuple[str, ...]] = (
    "RUNNER_PREFLIGHT",
    "EVIDENCE_COLLECTION",
    "VALIDATION",
    "SUMMARY",
)

REQUIRED_SPEC_ENTRY_IDS: Final[tuple[str, ...]] = (
    "r21r_strategy_bound",
    "runtime_boundary_closed",
    "human_approval_required",
    "cli_help_version_required",
    "http_frontend_required",
    "source_repo_hygiene_required",
    "safety_locks_closed",
    "r21t_next_step",
)


@dataclass(frozen=True)
class PreviewRunnerSpecEntry:
    """Single R21S review-only specification entry."""

    spec_entry_id: str
    title: str
    source_reference: str
    required_token: str
    required_state: str
    human_review_required: bool
    runtime_execution_allowed: bool
    ordinal: int


@dataclass(frozen=True)
class PreviewRunnerSpec:
    """Top-level R21S preview runner specification object."""

    spec_id: str
    status: str
    source_bindings: dict[str, bool]
    review_only_tokens: dict[str, bool | str]
    required_phases: tuple[str, ...]
    spec_entries: tuple[PreviewRunnerSpecEntry, ...]
    next_step: str


def _build_spec_entries() -> tuple[PreviewRunnerSpecEntry, ...]:
    """Build stable review-only spec entries."""
    entries = (
        PreviewRunnerSpecEntry(
            "r21r_strategy_bound",
            "R21S is bound to the sealed R21R preview strategy audit",
            "docs/PRODUCT/R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT_DOCS_ONLY.md",
            "SOURCE_R21R_PREVIEW_STRATEGY_BOUND",
            "bound",
            True,
            False,
            10,
        ),
        PreviewRunnerSpecEntry(
            "runtime_boundary_closed",
            "Reflex runtime and runner chain stay paused pending approval",
            "docs/FINAL/R21B_REFLEX_RUNTIME_CLOSURE_STRATEGY_AND_INSTRUCTIONS_MEMO_20260701.md",
            "REFLEX_RUNTIME_RUNNER_CHAIN",
            STOPPED_UNTIL_APPROVAL,
            True,
            False,
            20,
        ),
        PreviewRunnerSpecEntry(
            "human_approval_required",
            "R21T may start only after explicit human approval",
            NEXT_STEP,
            "HUMAN_APPROVED_PRIVATE_PREVIEW_REQUIRED",
            "required",
            True,
            False,
            30,
        ),
        PreviewRunnerSpecEntry(
            "cli_help_version_required",
            "R21T must capture CLI help and version before any private preview attempt",
            "docs/RUNTIME/REFLEX_CLI_CONTRACT_H8I.md",
            "REFLEX_CLI_HELP_CAPTURE_REQUIRED",
            "required_before_attempt",
            True,
            False,
            40,
        ),
        PreviewRunnerSpecEntry(
            "http_frontend_required",
            "HTTP frontend body must pass and be non-empty before preview review",
            "docs/RUNTIME/REFLEX_READINESS_ANTI_LOOP_POLICY_R16F2H6.md",
            "HTTP_FRONTEND_NON_EMPTY_REQUIRED",
            "required",
            True,
            False,
            50,
        ),
        PreviewRunnerSpecEntry(
            "source_repo_hygiene_required",
            "Dirty start or failed tests stop release actions and source writes",
            "docs/dev_tracking/runner_quality/RUNNER_REFERENCE_STANDARD_R1.md",
            "FAILED_TESTS_NO_COMMIT_NO_TAG_NO_PUSH",
            "required",
            True,
            False,
            60,
        ),
        PreviewRunnerSpecEntry(
            "safety_locks_closed",
            "Provider, broker/order/sizing, Sheet/BQ, public release, and HTML outputs stay closed",
            "docs/PROCESS/ASSISTANT_REFLEX_INSTRUCTION_LOCK_R16F2H4.md",
            "NO_PROVIDER_CALL",
            "closed",
            True,
            False,
            70,
        ),
        PreviewRunnerSpecEntry(
            "r21t_next_step",
            "Next step is human-approved private preview attempt only",
            NEXT_STEP,
            "NEXT",
            "next",
            True,
            False,
            80,
        ),
    )
    return tuple(sorted(entries, key=lambda entry: entry.ordinal))


def build_preview_runner_spec() -> PreviewRunnerSpec:
    """Build the R21S review-only preview runner specification."""
    return PreviewRunnerSpec(
        spec_id=SPEC_ID,
        status="R21S_REFLEX_PREVIEW_RUNNER_SPEC=READY",
        source_bindings=dict(SOURCE_BINDINGS),
        review_only_tokens=dict(REVIEW_ONLY_TOKENS),
        required_phases=REQUIRED_PHASES,
        spec_entries=_build_spec_entries(),
        next_step=NEXT_STEP,
    )


def spec_to_dict(spec: PreviewRunnerSpec | None = None) -> dict[str, Any]:
    """Return the review-only specification as a JSON-friendly dictionary."""
    if spec is None:
        spec = build_preview_runner_spec()

    return {
        "spec_id": spec.spec_id,
        "status": spec.status,
        "R21S_REFLEX_PREVIEW_RUNNER_SPEC": READY_STATUS,
        "source_bindings": dict(spec.source_bindings),
        "review_only_tokens": dict(spec.review_only_tokens),
        "required_phases": list(spec.required_phases),
        "spec_entries": [asdict(entry) for entry in spec.spec_entries],
        "next_step": spec.next_step,
    }


def build_preview_runner_spec_with_sources() -> dict[str, Any]:
    """Build the R21S payload with bound R21R source summary."""
    r21r = build_preview_strategy_audit_with_sources()
    spec = spec_to_dict()

    return {
        **spec,
        "source_summaries": {
            "r21r_preview_strategy": r21r["audit_id"],
            "r21r_status": r21r["R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT"],
            "r21r_next_step": r21r["next_step"],
        },
    }


def validate_preview_runner_spec(payload: dict[str, Any] | None = None) -> tuple[str, ...]:
    """Return validation errors. Empty tuple means the R21S payload is valid."""
    if payload is None:
        payload = build_preview_runner_spec_with_sources()

    errors: list[str] = []
    if payload.get("spec_id") != SPEC_ID:
        errors.append("spec_id_mismatch")
    if payload.get("R21S_REFLEX_PREVIEW_RUNNER_SPEC") != READY_STATUS:
        errors.append("spec_not_ready")

    bindings = payload.get("source_bindings")
    if not isinstance(bindings, dict):
        errors.append("missing_source_bindings")
    else:
        for key, expected in SOURCE_BINDINGS.items():
            if bindings.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    tokens = payload.get("review_only_tokens")
    if not isinstance(tokens, dict):
        errors.append("missing_review_only_tokens")
    else:
        for key, expected in REVIEW_ONLY_TOKENS.items():
            if tokens.get(key) != expected:
                errors.append(f"{key}_mismatch")

    phases = payload.get("required_phases")
    if tuple(phases) != REQUIRED_PHASES:
        errors.append("required_phases_mismatch")

    entries = payload.get("spec_entries")
    if not isinstance(entries, list):
        errors.append("missing_spec_entries")
    else:
        entry_ids = {entry.get("spec_entry_id") for entry in entries if isinstance(entry, dict)}
        if set(REQUIRED_SPEC_ENTRY_IDS) - entry_ids:
            errors.append("missing_spec_entries")
        ordinals = [entry.get("ordinal") for entry in entries if isinstance(entry, dict)]
        if ordinals != sorted(ordinals):
            errors.append("spec_entries_not_deterministic")
        for entry in entries:
            if not isinstance(entry, dict):
                errors.append("invalid_spec_entry")
                continue
            if entry.get("human_review_required") is not True:
                errors.append(f"human_review_missing={entry.get('spec_entry_id')}")
            if entry.get("runtime_execution_allowed") is not False:
                errors.append(f"runtime_execution_open={entry.get('spec_entry_id')}")

    summaries = payload.get("source_summaries")
    if isinstance(summaries, dict):
        if summaries.get("r21r_preview_strategy") != (
            "R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT_DOCS_ONLY"
        ):
            errors.append("r21r_source_mismatch")
        if summaries.get("r21r_status") != READY_STATUS:
            errors.append("r21r_status_mismatch")
        if summaries.get("r21r_next_step") != SPEC_ID:
            errors.append("r21r_next_step_mismatch")

    if payload.get("next_step") != NEXT_STEP:
        errors.append("next_step_mismatch")

    return tuple(errors)


def render_preview_runner_spec_markdown(payload: dict[str, Any] | None = None) -> str:
    """Render the R21S preview runner specification as markdown text only."""
    if payload is None:
        payload = build_preview_runner_spec_with_sources()

    lines = [
        "# R21S Reflex Preview Runner Spec - Review Only",
        "",
        f"Status: `{payload['status']}`",
        "",
        "R21S is a review-only specification. It is not a runtime runner,",
        "does not create a PowerShell runner, and does not capture live CLI evidence.",
        "",
        "## Source Bindings",
    ]
    for key in sorted(payload["source_bindings"]):
        lines.append(f"- `{key}` = `{payload['source_bindings'][key]}`")

    lines.extend(["", "## Review-Only Tokens"])
    for key in sorted(payload["review_only_tokens"]):
        lines.append(f"- `{key}` = `{payload['review_only_tokens'][key]}`")

    lines.extend(["", "## Required Runner Review Phases"])
    for phase in payload["required_phases"]:
        lines.append(f"- `{phase}`")

    lines.extend(["", "## Spec Entries"])
    for entry in payload["spec_entries"]:
        lines.append(
            "- "
            f"`{entry['spec_entry_id']}` - {entry['title']} - "
            f"`{entry['required_token']}` - `{entry['required_state']}`"
        )

    lines.extend(
        [
            "",
            "## R21T Gate",
            "R21T may only happen after explicit human approval.",
            "R21T must capture version and help evidence before any private preview attempt.",
            "",
            f"NEXT={payload['next_step']}",
        ]
    )
    return "\n".join(lines) + "\n"
