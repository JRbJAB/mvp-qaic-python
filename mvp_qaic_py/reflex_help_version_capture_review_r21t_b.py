"""R21T-B operator-approved help/version capture review-only payload.

This module is deterministic metadata only. It records that operator-approved
Reflex help/version capture evidence exists and passed, while private preview
runtime work remains paused until a later reviewed runner build.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from mvp_qaic_py.reflex_private_preview_approval_review_r21t_a import (
    REQUIRED_OPERATOR_MARKER,
    build_private_preview_approval_review_with_sources,
)

REVIEW_ID: Final[str] = "R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW_ONLY"
READY_STATUS: Final[str] = "READY"
PAUSED_STATUS: Final[str] = "PAUSED"
STOPPED_AFTER_CAPTURE: Final[str] = "STOPPED_AFTER_HELP_VERSION_CAPTURE"
REFLEX_VERSION: Final[str] = "0.9.6.post1"
NEXT_STEP: Final[str] = "R21T_C_PRIVATE_PREVIEW_RUNNER_BUILD_REVIEW_ONLY"

SOURCE_BINDINGS: Final[dict[str, bool]] = {
    "SOURCE_R21T_A_APPROVAL_REVIEW_BOUND": True,
}

EVIDENCE_FILES: Final[dict[str, str]] = {
    "VERSION_CAPTURE_FILE": (
        "C:/JRb_TRADING_OS/_RUN_REPORTS/MVP_QAIC_PY/"
        "P_R21T_B_HELP_VERSION_CAPTURE_20260702_164150/REFLEX_VERSION.txt"
    ),
    "HELP_CAPTURE_FILE": (
        "C:/JRb_TRADING_OS/_RUN_REPORTS/MVP_QAIC_PY/"
        "P_R21T_B_HELP_VERSION_CAPTURE_20260702_164150/REFLEX_RUN_HELP.txt"
    ),
    "SUMMARY_EVIDENCE_FILE": (
        "C:/JRb_TRADING_OS/_RUN_REPORTS/MVP_QAIC_PY/"
        "P_R21T_B_HELP_VERSION_CAPTURE_20260702_164150/"
        "R21T_B_HELP_VERSION_EVIDENCE.txt"
    ),
}

HELP_VERSION_REVIEW_TOKENS: Final[dict[str, bool | str]] = {
    "R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW": READY_STATUS,
    "SOURCE_R21T_A_APPROVAL_REVIEW_BOUND": True,
    "HUMAN_APPROVED_PRIVATE_PREVIEW": True,
    "HUMAN_APPROVED_PRIVATE_PREVIEW_MARKER": REQUIRED_OPERATOR_MARKER,
    "HELP_VERSION_CAPTURE_EXECUTED": True,
    "REFLEX_VERSION_CAPTURED": True,
    "REFLEX_RUN_HELP_CAPTURED": True,
    "REFLEX_VERSION": REFLEX_VERSION,
    "HELP_ALLOWED_FLAGS_CAPTURED": True,
    "HELP_FORBIDDEN_FRONTEND_HOST_FOUND": False,
    "NO_FRONTEND_HOST_FLAG": True,
    "NO_RUNTIME_APP_START": True,
    "NO_PREVIEW_ATTEMPT": True,
    "NO_PORTS": True,
    "NO_BROWSER": True,
    "REFLEX_RUNTIME_STATUS": PAUSED_STATUS,
    "REFLEX_RUNTIME_RUNNER_CHAIN": STOPPED_AFTER_CAPTURE,
    "HTTP_FRONTEND_NON_EMPTY_REQUIRED": True,
    "TCP_ONLY_NOT_PREVIEW_READY": True,
    "PREVIEW_ONLY_AFTER_HTTP_PASS": True,
    "NO_PUBLIC_DEPLOY": True,
    "NO_REFLEX_DEPLOY": True,
    "NO_PROVIDER_CALL": True,
    "NO_BROKER_ORDER_SIZING": True,
    "NO_SHEET_BQ_WRITE": True,
    "NO_HTML_OUTPUT": True,
    "NEXT": NEXT_STEP,
}

REQUIRED_CAPTURE_ENTRY_IDS: Final[tuple[str, ...]] = (
    "r21t_a_approval_bound",
    "operator_marker_received",
    "version_capture_passed",
    "help_capture_passed",
    "forbidden_frontend_host_absent",
    "runtime_not_started",
    "preview_readiness_not_claimed",
    "safety_locks_closed",
    "r21t_c_next_step",
)


@dataclass(frozen=True)
class HelpVersionCaptureEntry:
    """Single R21T-B help/version capture review entry."""

    capture_entry_id: str
    title: str
    source_reference: str
    required_token: str
    required_state: str
    evidence_passed: bool
    preview_readiness_claimed: bool
    runtime_action_allowed: bool
    ordinal: int


@dataclass(frozen=True)
class HelpVersionCaptureReview:
    """Top-level R21T-B help/version capture review object."""

    review_id: str
    status: str
    source_bindings: dict[str, bool]
    evidence_files: dict[str, str]
    help_version_review_tokens: dict[str, bool | str]
    capture_entries: tuple[HelpVersionCaptureEntry, ...]
    next_step: str


def _build_capture_entries() -> tuple[HelpVersionCaptureEntry, ...]:
    """Build stable R21T-B help/version evidence entries."""
    entries = (
        HelpVersionCaptureEntry(
            "r21t_a_approval_bound",
            "R21T-B is bound to the R21T-A approval review-only gate",
            "docs/PRODUCT/R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW_ONLY.md",
            "SOURCE_R21T_A_APPROVAL_REVIEW_BOUND",
            "bound",
            True,
            False,
            False,
            10,
        ),
        HelpVersionCaptureEntry(
            "operator_marker_received",
            "The explicit private preview approval marker was received",
            REQUIRED_OPERATOR_MARKER,
            "HUMAN_APPROVED_PRIVATE_PREVIEW",
            "true",
            True,
            False,
            False,
            20,
        ),
        HelpVersionCaptureEntry(
            "version_capture_passed",
            "Reflex version capture matched the expected pinned version",
            EVIDENCE_FILES["VERSION_CAPTURE_FILE"],
            "REFLEX_VERSION_CAPTURED",
            REFLEX_VERSION,
            True,
            False,
            False,
            30,
        ),
        HelpVersionCaptureEntry(
            "help_capture_passed",
            "Captured Reflex help contained the allowed flag evidence",
            EVIDENCE_FILES["HELP_CAPTURE_FILE"],
            "REFLEX_RUN_HELP_CAPTURED",
            "captured",
            True,
            False,
            False,
            40,
        ),
        HelpVersionCaptureEntry(
            "forbidden_frontend_host_absent",
            "Captured help evidence did not include the forbidden frontend host flag",
            EVIDENCE_FILES["SUMMARY_EVIDENCE_FILE"],
            "HELP_FORBIDDEN_FRONTEND_HOST_FOUND",
            "false",
            True,
            False,
            False,
            50,
        ),
        HelpVersionCaptureEntry(
            "runtime_not_started",
            "No runtime app start, port use, browser use, or preview attempt occurred",
            "docs/FINAL/R21B_REFLEX_RUNTIME_CLOSURE_STRATEGY_AND_INSTRUCTIONS_MEMO_20260701.md",
            "NO_RUNTIME_APP_START",
            "true",
            True,
            False,
            False,
            60,
        ),
        HelpVersionCaptureEntry(
            "preview_readiness_not_claimed",
            "Help/version capture does not satisfy HTTP preview readiness",
            "docs/RUNTIME/REFLEX_READINESS_ANTI_LOOP_POLICY_R16F2H6.md",
            "PREVIEW_ONLY_AFTER_HTTP_PASS",
            "required",
            True,
            False,
            False,
            70,
        ),
        HelpVersionCaptureEntry(
            "safety_locks_closed",
            "Provider, broker/order/sizing, Sheet/BQ, HTML, and release paths stay closed",
            "docs/PROCESS/ASSISTANT_REFLEX_INSTRUCTION_LOCK_R16F2H4.md",
            "NO_PROVIDER_CALL",
            "closed",
            True,
            False,
            False,
            80,
        ),
        HelpVersionCaptureEntry(
            "r21t_c_next_step",
            "Next step is private preview runner build review only",
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


def build_help_version_capture_review() -> HelpVersionCaptureReview:
    """Build the R21T-B help/version capture review-only payload."""
    return HelpVersionCaptureReview(
        review_id=REVIEW_ID,
        status="R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW=READY",
        source_bindings=dict(SOURCE_BINDINGS),
        evidence_files=dict(EVIDENCE_FILES),
        help_version_review_tokens=dict(HELP_VERSION_REVIEW_TOKENS),
        capture_entries=_build_capture_entries(),
        next_step=NEXT_STEP,
    )


def help_version_capture_review_to_dict(
    review: HelpVersionCaptureReview | None = None,
) -> dict[str, Any]:
    """Return the help/version capture review as a JSON-friendly dictionary."""
    if review is None:
        review = build_help_version_capture_review()

    return {
        "review_id": review.review_id,
        "status": review.status,
        "R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW": READY_STATUS,
        "source_bindings": dict(review.source_bindings),
        "evidence_files": dict(review.evidence_files),
        "help_version_review_tokens": dict(review.help_version_review_tokens),
        "capture_entries": [asdict(entry) for entry in review.capture_entries],
        "next_step": review.next_step,
    }


def build_help_version_capture_review_with_sources() -> dict[str, Any]:
    """Build the R21T-B payload with bound R21T-A source summary."""
    r21t_a = build_private_preview_approval_review_with_sources()
    review = help_version_capture_review_to_dict()

    return {
        **review,
        "source_summaries": {
            "r21t_a_approval_review": r21t_a["approval_id"],
            "r21t_a_status": r21t_a["R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW"],
            "r21t_a_required_marker": REQUIRED_OPERATOR_MARKER,
        },
    }


def validate_help_version_capture_review(
    payload: dict[str, Any] | None = None,
) -> tuple[str, ...]:
    """Return validation errors. Empty tuple means the R21T-B payload is valid."""
    if payload is None:
        payload = build_help_version_capture_review_with_sources()

    errors: list[str] = []
    if payload.get("review_id") != REVIEW_ID:
        errors.append("review_id_mismatch")
    if payload.get("R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW") != READY_STATUS:
        errors.append("help_version_capture_review_not_ready")

    bindings = payload.get("source_bindings")
    if not isinstance(bindings, dict):
        errors.append("missing_source_bindings")
    else:
        for key, expected in SOURCE_BINDINGS.items():
            if bindings.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    tokens = payload.get("help_version_review_tokens")
    if not isinstance(tokens, dict):
        errors.append("missing_help_version_review_tokens")
    else:
        for key, expected in HELP_VERSION_REVIEW_TOKENS.items():
            if tokens.get(key) != expected:
                errors.append(f"{key}_mismatch")

    files = payload.get("evidence_files")
    if not isinstance(files, dict):
        errors.append("missing_evidence_files")
    else:
        for key, expected in EVIDENCE_FILES.items():
            if files.get(key) != expected:
                errors.append(f"{key}_mismatch")

    entries = payload.get("capture_entries")
    if not isinstance(entries, list):
        errors.append("missing_capture_entries")
    else:
        entry_ids = {entry.get("capture_entry_id") for entry in entries if isinstance(entry, dict)}
        if set(REQUIRED_CAPTURE_ENTRY_IDS) - entry_ids:
            errors.append("missing_capture_entries")
        ordinals = [entry.get("ordinal") for entry in entries if isinstance(entry, dict)]
        if ordinals != sorted(ordinals):
            errors.append("capture_entries_not_deterministic")
        for entry in entries:
            if not isinstance(entry, dict):
                errors.append("invalid_capture_entry")
                continue
            if entry.get("evidence_passed") is not True:
                errors.append(f"evidence_not_passed={entry.get('capture_entry_id')}")
            if entry.get("preview_readiness_claimed") is not False:
                errors.append(f"preview_readiness_claimed={entry.get('capture_entry_id')}")
            if entry.get("runtime_action_allowed") is not False:
                errors.append(f"runtime_action_open={entry.get('capture_entry_id')}")

    summaries = payload.get("source_summaries")
    if isinstance(summaries, dict):
        if summaries.get("r21t_a_approval_review") != (
            "R21T_A_HUMAN_APPROVAL_PRIVATE_PREVIEW_RUNNER_REVIEW_ONLY"
        ):
            errors.append("r21t_a_source_mismatch")
        if summaries.get("r21t_a_status") != READY_STATUS:
            errors.append("r21t_a_status_mismatch")
        if summaries.get("r21t_a_required_marker") != REQUIRED_OPERATOR_MARKER:
            errors.append("r21t_a_marker_mismatch")

    if payload.get("next_step") != NEXT_STEP:
        errors.append("next_step_mismatch")

    return tuple(errors)


def render_help_version_capture_markdown(payload: dict[str, Any] | None = None) -> str:
    """Render the R21T-B help/version capture review as markdown text only."""
    if payload is None:
        payload = build_help_version_capture_review_with_sources()

    lines = [
        "# R21T-B Operator-Approved Help/Version Capture - Review Only",
        "",
        f"Status: `{payload['status']}`",
        "",
        "R21T-B documents that the approved help/version capture evidence passed.",
        "It does not claim preview readiness and does not create a runtime runner.",
        "",
        "## Source Bindings",
    ]
    for key in sorted(payload["source_bindings"]):
        lines.append(f"- `{key}` = `{payload['source_bindings'][key]}`")

    lines.extend(["", "## Evidence Files"])
    for key in sorted(payload["evidence_files"]):
        lines.append(f"- `{key}` = `{payload['evidence_files'][key]}`")

    lines.extend(["", "## Help/Version Review Tokens"])
    for key in sorted(payload["help_version_review_tokens"]):
        lines.append(f"- `{key}` = `{payload['help_version_review_tokens'][key]}`")

    lines.extend(["", "## Capture Entries"])
    for entry in payload["capture_entries"]:
        lines.append(
            "- "
            f"`{entry['capture_entry_id']}` - {entry['title']} - "
            f"`{entry['required_token']}` - `{entry['required_state']}`"
        )

    lines.extend(
        [
            "",
            "## Review Decision",
            "`REFLEX_VERSION` is `0.9.6.post1`.",
            "`HELP_ALLOWED_FLAGS_CAPTURED` is `True`.",
            "`HELP_FORBIDDEN_FRONTEND_HOST_FOUND` is `False`.",
            "`NO_PREVIEW_ATTEMPT` is `True`.",
            "`REFLEX_RUNTIME_STATUS` remains `PAUSED`.",
            "",
            f"NEXT={payload['next_step']}",
        ]
    )
    return "\n".join(lines) + "\n"
