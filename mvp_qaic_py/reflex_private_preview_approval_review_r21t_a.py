"""R21T-A private preview human approval gate review-only payload.

This module is deterministic metadata only. It records that the explicit
operator marker is required and absent, so private preview work remains closed.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from mvp_qaic_py.reflex_preview_runner_spec_r21s import (
    build_preview_runner_spec_with_sources,
)

APPROVAL_ID: Final[str] = "R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW_ONLY"
READY_STATUS: Final[str] = "READY"
PAUSED_STATUS: Final[str] = "PAUSED"
STOPPED_UNTIL_MARKER: Final[str] = "STOPPED_UNTIL_EXPLICIT_OPERATOR_MARKER"
REQUIRED_OPERATOR_MARKER: Final[str] = "HUMAN_APPROVED_PRIVATE_PREVIEW_TRUE"
NEXT_STEP: Final[str] = "R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW_ONLY"

SOURCE_BINDINGS: Final[dict[str, bool]] = {
    "SOURCE_R21S_PREVIEW_RUNNER_SPEC_BOUND": True,
}

APPROVAL_REVIEW_TOKENS: Final[dict[str, bool | str]] = {
    "R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW": READY_STATUS,
    "SOURCE_R21S_PREVIEW_RUNNER_SPEC_BOUND": True,
    "HUMAN_APPROVED_PRIVATE_PREVIEW": False,
    "HUMAN_APPROVED_PRIVATE_PREVIEW_REQUIRED": True,
    "EXPLICIT_OPERATOR_MARKER_REQUIRED": True,
    "REQUIRED_OPERATOR_MARKER": REQUIRED_OPERATOR_MARKER,
    "RUNNER_REVIEW_ONLY": True,
    "RUNNER_EXECUTED": False,
    "RUNTIME_EXECUTION_ALLOWED": False,
    "REFLEX_RUNTIME_STATUS": PAUSED_STATUS,
    "REFLEX_RUNTIME_RUNNER_CHAIN": STOPPED_UNTIL_MARKER,
    "REFLEX_CLI_HELP_CAPTURE_REQUIRED": True,
    "REFLEX_VERSION_CAPTURE_REQUIRED": True,
    "HELP_VERSION_CAPTURE_BEFORE_PREVIEW": True,
    "NO_FRONTEND_HOST_FLAG": True,
    "NO_PUBLIC_DEPLOY": True,
    "NO_REFLEX_DEPLOY": True,
    "HTTP_FRONTEND_NON_EMPTY_REQUIRED": True,
    "TCP_ONLY_NOT_PREVIEW_READY": True,
    "PREVIEW_ONLY_AFTER_HTTP_PASS": True,
    "HTTP_FAIL_STOP_AND_DIAG": True,
    "PS51_COMPATIBLE": True,
    "PROMPT_MD_REQUIRED": True,
    "RUNNER_SHORT_REQUIRED": True,
    "NO_GIANT_CONSOLE_PROMPT": True,
    "TARGETED_STAGING_ONLY": True,
    "NO_GIT_ADD_DOT": True,
    "NO_RESET": True,
    "DIRTY_START_STOP_NO_WRITE": True,
    "FAILED_TESTS_NO_COMMIT_NO_TAG_NO_PUSH": True,
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

REQUIRED_APPROVAL_ENTRY_IDS: Final[tuple[str, ...]] = (
    "r21s_spec_bound",
    "human_approval_absent",
    "operator_marker_required",
    "runtime_execution_closed",
    "help_version_before_preview",
    "http_preview_evidence_required",
    "source_hygiene_locked",
    "safety_locks_closed",
    "r21t_b_next_step",
)


@dataclass(frozen=True)
class PrivatePreviewApprovalEntry:
    """Single R21T-A approval gate review entry."""

    approval_entry_id: str
    title: str
    source_reference: str
    required_token: str
    required_state: str
    human_review_required: bool
    runtime_execution_allowed: bool
    marker_present: bool
    ordinal: int


@dataclass(frozen=True)
class PrivatePreviewApprovalReview:
    """Top-level R21T-A approval gate review object."""

    approval_id: str
    status: str
    source_bindings: dict[str, bool]
    approval_review_tokens: dict[str, bool | str]
    required_phases: tuple[str, ...]
    approval_entries: tuple[PrivatePreviewApprovalEntry, ...]
    next_step: str


def _build_approval_entries() -> tuple[PrivatePreviewApprovalEntry, ...]:
    """Build stable R21T-A approval gate entries."""
    entries = (
        PrivatePreviewApprovalEntry(
            "r21s_spec_bound",
            "R21T-A is bound to the sealed R21S preview runner spec",
            "docs/PRODUCT/R21S_REFLEX_PREVIEW_RUNNER_SPEC_REVIEW_ONLY.md",
            "SOURCE_R21S_PREVIEW_RUNNER_SPEC_BOUND",
            "bound",
            True,
            False,
            False,
            10,
        ),
        PrivatePreviewApprovalEntry(
            "human_approval_absent",
            "Private preview human approval remains false in R21T-A",
            APPROVAL_ID,
            "HUMAN_APPROVED_PRIVATE_PREVIEW",
            "false",
            True,
            False,
            False,
            20,
        ),
        PrivatePreviewApprovalEntry(
            "operator_marker_required",
            "The explicit operator marker is required before the next gate",
            REQUIRED_OPERATOR_MARKER,
            "EXPLICIT_OPERATOR_MARKER_REQUIRED",
            "required_absent",
            True,
            False,
            False,
            30,
        ),
        PrivatePreviewApprovalEntry(
            "runtime_execution_closed",
            "Runtime execution remains closed and the runner chain stays stopped",
            "docs/FINAL/R21B_REFLEX_RUNTIME_CLOSURE_STRATEGY_AND_INSTRUCTIONS_MEMO_20260701.md",
            "RUNTIME_EXECUTION_ALLOWED",
            "false",
            True,
            False,
            False,
            40,
        ),
        PrivatePreviewApprovalEntry(
            "help_version_before_preview",
            "CLI help and version capture are required before preview evidence",
            "docs/RUNTIME/REFLEX_CLI_CONTRACT_H8I.md",
            "HELP_VERSION_CAPTURE_BEFORE_PREVIEW",
            "required",
            True,
            False,
            False,
            50,
        ),
        PrivatePreviewApprovalEntry(
            "http_preview_evidence_required",
            "HTTP frontend evidence must pass and be non-empty before review",
            "docs/RUNTIME/REFLEX_READINESS_ANTI_LOOP_POLICY_R16F2H6.md",
            "HTTP_FRONTEND_NON_EMPTY_REQUIRED",
            "required",
            True,
            False,
            False,
            60,
        ),
        PrivatePreviewApprovalEntry(
            "source_hygiene_locked",
            "Dirty start and failed tests block source writes and release actions",
            "docs/dev_tracking/runner_quality/RUNNER_REFERENCE_STANDARD_R1.md",
            "FAILED_TESTS_NO_COMMIT_NO_TAG_NO_PUSH",
            "required",
            True,
            False,
            False,
            70,
        ),
        PrivatePreviewApprovalEntry(
            "safety_locks_closed",
            "Provider, broker/order/sizing, Sheet/BQ, public release, and HTML paths stay closed",
            "docs/PROCESS/ASSISTANT_REFLEX_INSTRUCTION_LOCK_R16F2H4.md",
            "NO_PROVIDER_CALL",
            "closed",
            True,
            False,
            False,
            80,
        ),
        PrivatePreviewApprovalEntry(
            "r21t_b_next_step",
            "Next step is operator-approved help and version capture review only",
            NEXT_STEP,
            "NEXT",
            "next",
            True,
            False,
            False,
            90,
        ),
    )
    return tuple(sorted(entries, key=lambda entry: entry.ordinal))


def build_private_preview_approval_review() -> PrivatePreviewApprovalReview:
    """Build the R21T-A approval gate review-only payload."""
    return PrivatePreviewApprovalReview(
        approval_id=APPROVAL_ID,
        status="R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW=READY",
        source_bindings=dict(SOURCE_BINDINGS),
        approval_review_tokens=dict(APPROVAL_REVIEW_TOKENS),
        required_phases=REQUIRED_PHASES,
        approval_entries=_build_approval_entries(),
        next_step=NEXT_STEP,
    )


def approval_review_to_dict(
    review: PrivatePreviewApprovalReview | None = None,
) -> dict[str, Any]:
    """Return the approval gate review as a JSON-friendly dictionary."""
    if review is None:
        review = build_private_preview_approval_review()

    return {
        "approval_id": review.approval_id,
        "status": review.status,
        "R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW": READY_STATUS,
        "source_bindings": dict(review.source_bindings),
        "approval_review_tokens": dict(review.approval_review_tokens),
        "required_phases": list(review.required_phases),
        "approval_entries": [asdict(entry) for entry in review.approval_entries],
        "next_step": review.next_step,
    }


def build_private_preview_approval_review_with_sources() -> dict[str, Any]:
    """Build the R21T-A payload with bound R21S source summary."""
    r21s = build_preview_runner_spec_with_sources()
    review = approval_review_to_dict()

    return {
        **review,
        "source_summaries": {
            "r21s_preview_runner_spec": r21s["spec_id"],
            "r21s_status": r21s["R21S_REFLEX_PREVIEW_RUNNER_SPEC"],
            "r21s_next_step": r21s["next_step"],
        },
    }


def validate_private_preview_approval_review(
    payload: dict[str, Any] | None = None,
) -> tuple[str, ...]:
    """Return validation errors. Empty tuple means the R21T-A payload is valid."""
    if payload is None:
        payload = build_private_preview_approval_review_with_sources()

    errors: list[str] = []
    if payload.get("approval_id") != APPROVAL_ID:
        errors.append("approval_id_mismatch")
    if payload.get("R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW") != READY_STATUS:
        errors.append("approval_review_not_ready")

    bindings = payload.get("source_bindings")
    if not isinstance(bindings, dict):
        errors.append("missing_source_bindings")
    else:
        for key, expected in SOURCE_BINDINGS.items():
            if bindings.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    tokens = payload.get("approval_review_tokens")
    if not isinstance(tokens, dict):
        errors.append("missing_approval_review_tokens")
    else:
        for key, expected in APPROVAL_REVIEW_TOKENS.items():
            if tokens.get(key) != expected:
                errors.append(f"{key}_mismatch")

    if tuple(payload.get("required_phases", ())) != REQUIRED_PHASES:
        errors.append("required_phases_mismatch")

    entries = payload.get("approval_entries")
    if not isinstance(entries, list):
        errors.append("missing_approval_entries")
    else:
        entry_ids = {entry.get("approval_entry_id") for entry in entries if isinstance(entry, dict)}
        if set(REQUIRED_APPROVAL_ENTRY_IDS) - entry_ids:
            errors.append("missing_approval_entries")
        ordinals = [entry.get("ordinal") for entry in entries if isinstance(entry, dict)]
        if ordinals != sorted(ordinals):
            errors.append("approval_entries_not_deterministic")
        for entry in entries:
            if not isinstance(entry, dict):
                errors.append("invalid_approval_entry")
                continue
            if entry.get("human_review_required") is not True:
                errors.append(f"human_review_missing={entry.get('approval_entry_id')}")
            if entry.get("runtime_execution_allowed") is not False:
                errors.append(f"runtime_execution_open={entry.get('approval_entry_id')}")
            if entry.get("marker_present") is not False:
                errors.append(f"marker_present={entry.get('approval_entry_id')}")

    summaries = payload.get("source_summaries")
    if isinstance(summaries, dict):
        if summaries.get("r21s_preview_runner_spec") != (
            "R21S_REFLEX_PREVIEW_RUNNER_SPEC_REVIEW_ONLY"
        ):
            errors.append("r21s_source_mismatch")
        if summaries.get("r21s_status") != READY_STATUS:
            errors.append("r21s_status_mismatch")
        if summaries.get("r21s_next_step") != (
            "R21T_HUMAN_APPROVED_PRIVATE_PREVIEW_ATTEMPT_ONLY"
        ):
            errors.append("r21s_next_step_mismatch")

    if payload.get("next_step") != NEXT_STEP:
        errors.append("next_step_mismatch")

    return tuple(errors)


def render_private_preview_approval_markdown(payload: dict[str, Any] | None = None) -> str:
    """Render the R21T-A approval gate review as markdown text only."""
    if payload is None:
        payload = build_private_preview_approval_review_with_sources()

    lines = [
        "# R21T-A Human Approval Private Preview Runner - Review Only",
        "",
        f"Status: `{payload['status']}`",
        "",
        "R21T-A is an approval gate only. The explicit operator marker remains",
        "required and absent, so no runtime runner is created or executed.",
        "",
        "## Source Bindings",
    ]
    for key in sorted(payload["source_bindings"]):
        lines.append(f"- `{key}` = `{payload['source_bindings'][key]}`")

    lines.extend(["", "## Approval Review Tokens"])
    for key in sorted(payload["approval_review_tokens"]):
        lines.append(f"- `{key}` = `{payload['approval_review_tokens'][key]}`")

    lines.extend(["", "## Required Runner Review Phases"])
    for phase in payload["required_phases"]:
        lines.append(f"- `{phase}`")

    lines.extend(["", "## Approval Entries"])
    for entry in payload["approval_entries"]:
        lines.append(
            "- "
            f"`{entry['approval_entry_id']}` - {entry['title']} - "
            f"`{entry['required_token']}` - `{entry['required_state']}`"
        )

    lines.extend(
        [
            "",
            "## Gate Decision",
            f"`{REQUIRED_OPERATOR_MARKER}` is required before R21T-B.",
            "`HUMAN_APPROVED_PRIVATE_PREVIEW` remains `False` in R21T-A.",
            "",
            f"NEXT={payload['next_step']}",
        ]
    )
    return "\n".join(lines) + "\n"
