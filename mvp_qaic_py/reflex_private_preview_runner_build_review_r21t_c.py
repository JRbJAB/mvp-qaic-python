"""R21T-C private preview runner build review-only payload.

This module is deterministic metadata only. It describes the later private
preview runner shape without creating a runner, launching runtime work, using
ports, or claiming preview readiness.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from mvp_qaic_py.reflex_help_version_capture_review_r21t_b import (
    REFLEX_VERSION,
    build_help_version_capture_review_with_sources,
)

REVIEW_ID: Final[str] = "R21T_C_PRIVATE_PREVIEW_RUNNER_BUILD_REVIEW_ONLY"
READY_STATUS: Final[str] = "READY"
PAUSED_STATUS: Final[str] = "PAUSED"
STOPPED_AFTER_BUILD_REVIEW: Final[str] = "STOPPED_AFTER_RUNNER_BUILD_REVIEW"
NEXT_STEP: Final[str] = "R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW_ONLY"

SOURCE_BINDINGS: Final[dict[str, bool]] = {
    "SOURCE_R21T_B_HELP_VERSION_CAPTURE_BOUND": True,
}

BUILD_REVIEW_TOKENS: Final[dict[str, bool | str]] = {
    "R21T_C_PRIVATE_PREVIEW_RUNNER_BUILD_REVIEW": READY_STATUS,
    "SOURCE_R21T_B_HELP_VERSION_CAPTURE_BOUND": True,
    "HUMAN_APPROVED_PRIVATE_PREVIEW": True,
    "HELP_VERSION_CAPTURE_PASSED": True,
    "REFLEX_VERSION": REFLEX_VERSION,
    "HELP_FORBIDDEN_FRONTEND_HOST_FOUND": False,
    "BUILD_REVIEW_ONLY": True,
    "RUNNER_FILE_CREATED": False,
    "PS1_CREATED": False,
    "RUNNER_EXECUTED": False,
    "NO_RUNTIME_EXECUTION": True,
    "NO_DOCKER_CALL": True,
    "NO_REFLEX_APP_START": True,
    "NO_PREVIEW_ATTEMPT": True,
    "NO_PORTS": True,
    "NO_BROWSER": True,
    "REFLEX_RUNTIME_STATUS": PAUSED_STATUS,
    "REFLEX_RUNTIME_RUNNER_CHAIN": STOPPED_AFTER_BUILD_REVIEW,
    "PRIVATE_MAPPING_REQUIRED": True,
    "HTTP_FRONTEND_NON_EMPTY_REQUIRED": True,
    "TCP_ONLY_NOT_PREVIEW_READY": True,
    "PREVIEW_ONLY_AFTER_HTTP_PASS": True,
    "NO_FRONTEND_HOST_FLAG": True,
    "NO_PUBLIC_DEPLOY": True,
    "NO_REFLEX_DEPLOY": True,
    "NO_PROVIDER_CALL": True,
    "NO_BROKER_ORDER_SIZING": True,
    "NO_SHEET_BQ_WRITE": True,
    "NO_HTML_OUTPUT": True,
    "TARGETED_STAGING_ONLY": True,
    "NO_GIT_ADD_DOT": True,
    "NO_RESET": True,
    "NEXT": NEXT_STEP,
}

BUILD_REVIEW_PHASES: Final[tuple[str, ...]] = (
    "PREFLIGHT",
    "HELP_VERSION_EVIDENCE_REUSE",
    "SOURCE_COPY_STRATEGY",
    "POLICY_GUARD_CHECKS",
    "PRIVATE_ONLY_PREVIEW_READINESS_CHECKS",
    "HTTP_NON_EMPTY_FRONTEND_EVIDENCE_REQUIREMENT",
    "FAILURE_STOP_CONDITIONS",
    "SUMMARY",
)

REQUIRED_BUILD_ENTRY_IDS: Final[tuple[str, ...]] = (
    "r21t_b_help_version_bound",
    "human_approval_and_help_capture_inherited",
    "future_preflight_metadata_only",
    "future_source_copy_strategy_metadata_only",
    "future_policy_guard_checks_metadata_only",
    "future_private_readiness_checks_metadata_only",
    "future_http_non_empty_frontend_evidence_required",
    "future_failure_stop_conditions_metadata_only",
    "review_boundary_closed",
    "safety_locks_closed",
    "r21t_d_next_step",
)


@dataclass(frozen=True)
class RunnerBuildReviewEntry:
    """Single R21T-C private preview runner build review entry."""

    build_entry_id: str
    title: str
    source_reference: str
    required_token: str
    required_state: str
    metadata_only: bool
    runtime_action_allowed: bool
    preview_readiness_claimed: bool
    ordinal: int


@dataclass(frozen=True)
class RunnerBuildReview:
    """Top-level R21T-C private preview runner build review object."""

    review_id: str
    status: str
    source_bindings: dict[str, bool]
    build_review_tokens: dict[str, bool | str]
    build_review_phases: tuple[str, ...]
    build_entries: tuple[RunnerBuildReviewEntry, ...]
    next_step: str


def _build_runner_build_entries() -> tuple[RunnerBuildReviewEntry, ...]:
    """Build stable R21T-C future-runner metadata entries."""
    entries = (
        RunnerBuildReviewEntry(
            "r21t_b_help_version_bound",
            "R21T-C is bound to the R21T-B help/version capture review",
            "docs/PRODUCT/R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW_ONLY.md",
            "SOURCE_R21T_B_HELP_VERSION_CAPTURE_BOUND",
            "bound",
            True,
            False,
            False,
            10,
        ),
        RunnerBuildReviewEntry(
            "human_approval_and_help_capture_inherited",
            "Human approval and passed help/version capture are inherited as review inputs",
            "docs/PRODUCT/R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW_ONLY.md",
            "HELP_VERSION_CAPTURE_PASSED",
            "true",
            True,
            False,
            False,
            20,
        ),
        RunnerBuildReviewEntry(
            "future_preflight_metadata_only",
            "Future runner preflight remains a metadata phase in R21T-C",
            "docs/dev_tracking/runner_quality/RUNNER_REFERENCE_STANDARD_R1.md",
            "BUILD_REVIEW_ONLY",
            "metadata_only",
            True,
            False,
            False,
            30,
        ),
        RunnerBuildReviewEntry(
            "future_source_copy_strategy_metadata_only",
            "Future source copy strategy requires a full tracked-source snapshot outside the repo",
            "docs/RUNTIME/REFLEX_RUNNER_HARDENING_POLICY_R16F2H7I.md",
            "TARGETED_STAGING_ONLY",
            "metadata_only",
            True,
            False,
            False,
            40,
        ),
        RunnerBuildReviewEntry(
            "future_policy_guard_checks_metadata_only",
            "Future policy guard checks remain required before any later operator action",
            "docs/RUNTIME/REFLEX_TECH_PROCESS_LOCK_R16F2H6.md",
            "NO_RUNTIME_EXECUTION",
            "metadata_only",
            True,
            False,
            False,
            50,
        ),
        RunnerBuildReviewEntry(
            "future_private_readiness_checks_metadata_only",
            "Future private-only readiness checks must not treat TCP evidence as preview readiness",
            "docs/RUNTIME/REFLEX_READINESS_ANTI_LOOP_POLICY_R16F2H6.md",
            "TCP_ONLY_NOT_PREVIEW_READY",
            "required",
            True,
            False,
            False,
            60,
        ),
        RunnerBuildReviewEntry(
            "future_http_non_empty_frontend_evidence_required",
            "Future preview review requires non-empty HTTP frontend evidence",
            "docs/RUNTIME/REFLEX_CLI_CONTRACT_H8I.md",
            "HTTP_FRONTEND_NON_EMPTY_REQUIRED",
            "required",
            True,
            False,
            False,
            70,
        ),
        RunnerBuildReviewEntry(
            "future_failure_stop_conditions_metadata_only",
            "Future failure conditions stop instead of relaunching runtime work",
            "docs/FINAL/R21B_REFLEX_RUNTIME_CLOSURE_STRATEGY_AND_INSTRUCTIONS_MEMO_20260701.md",
            "REFLEX_RUNTIME_RUNNER_CHAIN",
            STOPPED_AFTER_BUILD_REVIEW,
            True,
            False,
            False,
            80,
        ),
        RunnerBuildReviewEntry(
            "review_boundary_closed",
            "R21T-C creates no runner file, script, runtime start, ports, browser, or preview attempt",
            REVIEW_ID,
            "RUNNER_FILE_CREATED",
            "false",
            True,
            False,
            False,
            90,
        ),
        RunnerBuildReviewEntry(
            "safety_locks_closed",
            "Provider, broker/order/sizing, Sheet/BQ, HTML, and release paths stay closed",
            "docs/PROCESS/ASSISTANT_REFLEX_INSTRUCTION_LOCK_R16F2H4.md",
            "NO_PROVIDER_CALL",
            "closed",
            True,
            False,
            False,
            100,
        ),
        RunnerBuildReviewEntry(
            "r21t_d_next_step",
            "Next step is operator script review only",
            NEXT_STEP,
            "NEXT",
            "next",
            True,
            False,
            False,
            110,
        ),
    )
    return tuple(sorted(entries, key=lambda entry: entry.ordinal))


def build_private_preview_runner_build_review() -> RunnerBuildReview:
    """Build the R21T-C private preview runner build review-only payload."""
    return RunnerBuildReview(
        review_id=REVIEW_ID,
        status="R21T_C_PRIVATE_PREVIEW_RUNNER_BUILD_REVIEW=READY",
        source_bindings=dict(SOURCE_BINDINGS),
        build_review_tokens=dict(BUILD_REVIEW_TOKENS),
        build_review_phases=BUILD_REVIEW_PHASES,
        build_entries=_build_runner_build_entries(),
        next_step=NEXT_STEP,
    )


def runner_build_review_to_dict(
    review: RunnerBuildReview | None = None,
) -> dict[str, Any]:
    """Return the R21T-C runner build review as a JSON-friendly dictionary."""
    if review is None:
        review = build_private_preview_runner_build_review()

    return {
        "review_id": review.review_id,
        "status": review.status,
        "R21T_C_PRIVATE_PREVIEW_RUNNER_BUILD_REVIEW": READY_STATUS,
        "source_bindings": dict(review.source_bindings),
        "build_review_tokens": dict(review.build_review_tokens),
        "build_review_phases": list(review.build_review_phases),
        "build_entries": [asdict(entry) for entry in review.build_entries],
        "next_step": review.next_step,
    }


def build_private_preview_runner_build_review_with_sources() -> dict[str, Any]:
    """Build the R21T-C payload with bound R21T-B source summary."""
    r21t_b = build_help_version_capture_review_with_sources()
    review = runner_build_review_to_dict()

    return {
        **review,
        "source_summaries": {
            "r21t_b_help_version_review": r21t_b["review_id"],
            "r21t_b_status": r21t_b["R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW"],
            "r21t_b_reflex_version": r21t_b["help_version_review_tokens"]["REFLEX_VERSION"],
            "r21t_b_next_step": r21t_b["next_step"],
        },
    }


def validate_private_preview_runner_build_review(
    payload: dict[str, Any] | None = None,
) -> tuple[str, ...]:
    """Return validation errors. Empty tuple means the R21T-C payload is valid."""
    if payload is None:
        payload = build_private_preview_runner_build_review_with_sources()

    errors: list[str] = []
    if payload.get("review_id") != REVIEW_ID:
        errors.append("review_id_mismatch")
    if payload.get("R21T_C_PRIVATE_PREVIEW_RUNNER_BUILD_REVIEW") != READY_STATUS:
        errors.append("runner_build_review_not_ready")

    bindings = payload.get("source_bindings")
    if not isinstance(bindings, dict):
        errors.append("missing_source_bindings")
    else:
        for key, expected in SOURCE_BINDINGS.items():
            if bindings.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    tokens = payload.get("build_review_tokens")
    if not isinstance(tokens, dict):
        errors.append("missing_build_review_tokens")
    else:
        for key, expected in BUILD_REVIEW_TOKENS.items():
            if tokens.get(key) != expected:
                errors.append(f"{key}_mismatch")

    if tuple(payload.get("build_review_phases", ())) != BUILD_REVIEW_PHASES:
        errors.append("build_review_phases_mismatch")

    entries = payload.get("build_entries")
    if not isinstance(entries, list):
        errors.append("missing_build_entries")
    else:
        entry_ids = {entry.get("build_entry_id") for entry in entries if isinstance(entry, dict)}
        if set(REQUIRED_BUILD_ENTRY_IDS) - entry_ids:
            errors.append("missing_build_entries")
        ordinals = [entry.get("ordinal") for entry in entries if isinstance(entry, dict)]
        if ordinals != sorted(ordinals):
            errors.append("build_entries_not_deterministic")
        for entry in entries:
            if not isinstance(entry, dict):
                errors.append("invalid_build_entry")
                continue
            if entry.get("metadata_only") is not True:
                errors.append(f"metadata_only_missing={entry.get('build_entry_id')}")
            if entry.get("runtime_action_allowed") is not False:
                errors.append(f"runtime_action_open={entry.get('build_entry_id')}")
            if entry.get("preview_readiness_claimed") is not False:
                errors.append(f"preview_readiness_claimed={entry.get('build_entry_id')}")

    summaries = payload.get("source_summaries")
    if isinstance(summaries, dict):
        if summaries.get("r21t_b_help_version_review") != (
            "R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW_ONLY"
        ):
            errors.append("r21t_b_source_mismatch")
        if summaries.get("r21t_b_status") != READY_STATUS:
            errors.append("r21t_b_status_mismatch")
        if summaries.get("r21t_b_reflex_version") != REFLEX_VERSION:
            errors.append("r21t_b_version_mismatch")
        if summaries.get("r21t_b_next_step") != REVIEW_ID:
            errors.append("r21t_b_next_step_mismatch")

    if payload.get("next_step") != NEXT_STEP:
        errors.append("next_step_mismatch")

    return tuple(errors)


def render_private_preview_runner_build_markdown(
    payload: dict[str, Any] | None = None,
) -> str:
    """Render the R21T-C runner build review as markdown text only."""
    if payload is None:
        payload = build_private_preview_runner_build_review_with_sources()

    lines = [
        "# R21T-C Private Preview Runner Build - Review Only",
        "",
        f"Status: `{payload['status']}`",
        "",
        "R21T-C records future private preview runner phases as metadata only.",
        "It creates no script or runner file and does not claim preview readiness.",
        "",
        "## Source Bindings",
    ]
    for key in sorted(payload["source_bindings"]):
        lines.append(f"- `{key}` = `{payload['source_bindings'][key]}`")

    lines.extend(["", "## Build Review Tokens"])
    for key in sorted(payload["build_review_tokens"]):
        lines.append(f"- `{key}` = `{payload['build_review_tokens'][key]}`")

    lines.extend(["", "## Future Runner Phases"])
    for phase in payload["build_review_phases"]:
        lines.append(f"- `{phase}`")

    lines.extend(["", "## Build Review Entries"])
    for entry in payload["build_entries"]:
        lines.append(
            "- "
            f"`{entry['build_entry_id']}` - {entry['title']} - "
            f"`{entry['required_token']}` - `{entry['required_state']}`"
        )

    lines.extend(
        [
            "",
            "## Review Decision",
            "`BUILD_REVIEW_ONLY` is `True`.",
            "`RUNNER_FILE_CREATED` is `False`.",
            "`PS1_CREATED` is `False`.",
            "`RUNNER_EXECUTED` is `False`.",
            "`NO_RUNTIME_EXECUTION` is `True`.",
            "`NO_PREVIEW_ATTEMPT` is `True`.",
            "`REFLEX_RUNTIME_STATUS` remains `PAUSED`.",
            "",
            f"NEXT={payload['next_step']}",
        ]
    )
    return "\n".join(lines) + "\n"
