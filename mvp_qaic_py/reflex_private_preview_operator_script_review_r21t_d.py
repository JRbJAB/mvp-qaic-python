"""R21T-D private preview operator script review-only payload.

This module is deterministic metadata only. It describes the later operator
script sections without creating a script, launching runtime work, using ports,
or claiming preview readiness.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from mvp_qaic_py.reflex_private_preview_runner_build_review_r21t_c import (
    REFLEX_VERSION,
    build_private_preview_runner_build_review_with_sources,
)

REVIEW_ID: Final[str] = "R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW_ONLY"
READY_STATUS: Final[str] = "READY"
PAUSED_STATUS: Final[str] = "PAUSED"
STOPPED_AFTER_OPERATOR_SCRIPT_REVIEW: Final[str] = (
    "STOPPED_AFTER_OPERATOR_SCRIPT_REVIEW"
)
NEXT_STEP: Final[str] = "R21T_E_PRIVATE_PREVIEW_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN"

SOURCE_BINDINGS: Final[dict[str, bool]] = {
    "SOURCE_R21T_C_BUILD_REVIEW_BOUND": True,
}

OPERATOR_SCRIPT_REVIEW_TOKENS: Final[dict[str, bool | str]] = {
    "R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW": READY_STATUS,
    "SOURCE_R21T_C_BUILD_REVIEW_BOUND": True,
    "OPERATOR_SCRIPT_REVIEW_ONLY": True,
    "SCRIPT_FILE_CREATED": False,
    "PS1_CREATED": False,
    "SCRIPT_EXECUTED": False,
    "RUNNER_EXECUTED": False,
    "RUNTIME_EXECUTION_ALLOWED": False,
    "NO_RUNTIME_EXECUTION": True,
    "NO_DOCKER_CALL": True,
    "NO_REFLEX_APP_START": True,
    "NO_PREVIEW_ATTEMPT": True,
    "NO_PORTS": True,
    "NO_BROWSER": True,
    "REFLEX_VERSION": REFLEX_VERSION,
    "HELP_VERSION_CAPTURE_PASSED": True,
    "HELP_FORBIDDEN_FRONTEND_HOST_FOUND": False,
    "NO_FRONTEND_HOST_FLAG": True,
    "PRIVATE_MAPPING_REQUIRED": True,
    "HTTP_FRONTEND_NON_EMPTY_REQUIRED": True,
    "TCP_ONLY_NOT_PREVIEW_READY": True,
    "PREVIEW_ONLY_AFTER_HTTP_PASS": True,
    "REFLEX_RUNTIME_STATUS": PAUSED_STATUS,
    "REFLEX_RUNTIME_RUNNER_CHAIN": STOPPED_AFTER_OPERATOR_SCRIPT_REVIEW,
    "PS51_COMPATIBLE": True,
    "PROMPT_MD_REQUIRED": True,
    "RUNNER_SHORT_REQUIRED": True,
    "NO_GIANT_CONSOLE_PROMPT": True,
    "HARD_TIMEOUT_REQUIRED": True,
    "IMAGE_PREFLIGHT_REQUIRED": True,
    "PORT_PREFLIGHT_REQUIRED": True,
    "GIT_ARCHIVE_HEAD_COPY_REQUIRED": True,
    "POLICY_GUARDS_REQUIRED": True,
    "TRANSIENT_REPORTS_UNDER_RUN_REPORTS": True,
    "TARGETED_STAGING_ONLY": True,
    "NO_GIT_ADD_DOT": True,
    "NO_RESET": True,
    "NO_PUBLIC_DEPLOY": True,
    "NO_REFLEX_DEPLOY": True,
    "NO_PROVIDER_CALL": True,
    "NO_BROKER_ORDER_SIZING": True,
    "NO_SHEET_BQ_WRITE": True,
    "NO_HTML_OUTPUT": True,
    "NEXT": NEXT_STEP,
}

OPERATOR_SCRIPT_SECTIONS: Final[tuple[str, ...]] = (
    "STRICT_PREFLIGHT",
    "HARD_TIMEOUT_NATIVE_CALLS",
    "PINNED_IMAGE_CHECK",
    "PRIVATE_PORT_CHECKS",
    "FULL_HEAD_COPY_BY_ARCHIVE_TAR",
    "POLICY_GUARD_CHECKS",
    "HELP_VERSION_EVIDENCE_REUSE",
    "PREVIEW_READINESS_PROBES",
    "FAILURE_STOP_DIAGNOSTICS",
    "SUMMARY",
)

REQUIRED_OPERATOR_ENTRY_IDS: Final[tuple[str, ...]] = (
    "r21t_c_build_review_bound",
    "operator_script_review_only_boundary",
    "strict_preflight_metadata_only",
    "hard_timeout_native_calls_metadata_only",
    "pinned_image_check_metadata_only",
    "private_port_checks_metadata_only",
    "full_head_copy_archive_tar_metadata_only",
    "policy_guard_checks_metadata_only",
    "help_version_evidence_reuse_metadata_only",
    "preview_readiness_probes_metadata_only",
    "failure_stop_diagnostics_metadata_only",
    "script_generation_closed",
    "safety_locks_closed",
    "r21t_e_next_step",
)


@dataclass(frozen=True)
class OperatorScriptReviewEntry:
    """Single R21T-D operator script review metadata entry."""

    operator_entry_id: str
    title: str
    source_reference: str
    required_token: str
    required_state: str
    metadata_only: bool
    script_action_allowed: bool
    runtime_action_allowed: bool
    preview_readiness_claimed: bool
    ordinal: int


@dataclass(frozen=True)
class OperatorScriptReview:
    """Top-level R21T-D operator script review object."""

    review_id: str
    status: str
    source_bindings: dict[str, bool]
    operator_script_review_tokens: dict[str, bool | str]
    operator_script_sections: tuple[str, ...]
    operator_entries: tuple[OperatorScriptReviewEntry, ...]
    next_step: str


def _build_operator_entries() -> tuple[OperatorScriptReviewEntry, ...]:
    """Build stable R21T-D future-operator-script metadata entries."""
    entries = (
        OperatorScriptReviewEntry(
            "r21t_c_build_review_bound",
            "R21T-D is bound to the R21T-C private preview runner build review",
            "docs/PRODUCT/R21T_C_PRIVATE_PREVIEW_RUNNER_BUILD_REVIEW_ONLY.md",
            "SOURCE_R21T_C_BUILD_REVIEW_BOUND",
            "bound",
            True,
            False,
            False,
            False,
            10,
        ),
        OperatorScriptReviewEntry(
            "operator_script_review_only_boundary",
            "R21T-D describes future operator script sections as metadata only",
            REVIEW_ID,
            "OPERATOR_SCRIPT_REVIEW_ONLY",
            "true",
            True,
            False,
            False,
            False,
            20,
        ),
        OperatorScriptReviewEntry(
            "strict_preflight_metadata_only",
            "Future strict preflight checks are required before any later action",
            "docs/dev_tracking/runner_quality/RUNNER_REFERENCE_STANDARD_R1.md",
            "HARD_TIMEOUT_REQUIRED",
            "required",
            True,
            False,
            False,
            False,
            30,
        ),
        OperatorScriptReviewEntry(
            "hard_timeout_native_calls_metadata_only",
            "Future native calls must have hard timeouts and captured outcomes",
            "docs/RUNTIME/REFLEX_RUNNER_HARDENING_POLICY_R16F2H7I.md",
            "HARD_TIMEOUT_REQUIRED",
            "required",
            True,
            False,
            False,
            False,
            40,
        ),
        OperatorScriptReviewEntry(
            "pinned_image_check_metadata_only",
            "Future image preflight remains a review requirement only in R21T-D",
            "docs/RUNTIME/REFLEX_CLI_CONTRACT_H8I.md",
            "IMAGE_PREFLIGHT_REQUIRED",
            "required",
            True,
            False,
            False,
            False,
            50,
        ),
        OperatorScriptReviewEntry(
            "private_port_checks_metadata_only",
            "Future private port checks remain metadata only and do not use ports now",
            "docs/RUNTIME/REFLEX_READINESS_ANTI_LOOP_POLICY_R16F2H6.md",
            "PORT_PREFLIGHT_REQUIRED",
            "required",
            True,
            False,
            False,
            False,
            60,
        ),
        OperatorScriptReviewEntry(
            "full_head_copy_archive_tar_metadata_only",
            "Future source copy requires a full HEAD archive and tar extraction approach",
            "docs/RUNTIME/REFLEX_RUNNER_HARDENING_POLICY_R16F2H7I.md",
            "GIT_ARCHIVE_HEAD_COPY_REQUIRED",
            "required",
            True,
            False,
            False,
            False,
            70,
        ),
        OperatorScriptReviewEntry(
            "policy_guard_checks_metadata_only",
            "Future policy guard checks stay mandatory before any later operator action",
            "docs/RUNTIME/REFLEX_TECH_PROCESS_LOCK_R16F2H6.md",
            "POLICY_GUARDS_REQUIRED",
            "required",
            True,
            False,
            False,
            False,
            80,
        ),
        OperatorScriptReviewEntry(
            "help_version_evidence_reuse_metadata_only",
            "R21T-D reuses passed help/version evidence without repeating capture work",
            "docs/PRODUCT/R21T_B_OPERATOR_APPROVED_HELP_VERSION_CAPTURE_REVIEW_ONLY.md",
            "HELP_VERSION_CAPTURE_PASSED",
            "true",
            True,
            False,
            False,
            False,
            90,
        ),
        OperatorScriptReviewEntry(
            "preview_readiness_probes_metadata_only",
            "Future readiness probes require non-empty HTTP frontend evidence",
            "docs/RUNTIME/REFLEX_CLI_CONTRACT_H8I.md",
            "HTTP_FRONTEND_NON_EMPTY_REQUIRED",
            "required",
            True,
            False,
            False,
            False,
            100,
        ),
        OperatorScriptReviewEntry(
            "failure_stop_diagnostics_metadata_only",
            "Future failure handling must stop and record diagnostics instead of relaunching",
            "docs/FINAL/R21B_REFLEX_RUNTIME_CLOSURE_STRATEGY_AND_INSTRUCTIONS_MEMO_20260701.md",
            "REFLEX_RUNTIME_RUNNER_CHAIN",
            STOPPED_AFTER_OPERATOR_SCRIPT_REVIEW,
            True,
            False,
            False,
            False,
            110,
        ),
        OperatorScriptReviewEntry(
            "script_generation_closed",
            "R21T-D creates no script file and executes no script or runner",
            REVIEW_ID,
            "SCRIPT_FILE_CREATED",
            "false",
            True,
            False,
            False,
            False,
            120,
        ),
        OperatorScriptReviewEntry(
            "safety_locks_closed",
            "Provider, broker/order/sizing, Sheet/BQ, HTML, and release paths stay closed",
            "docs/PROCESS/ASSISTANT_REFLEX_INSTRUCTION_LOCK_R16F2H4.md",
            "NO_PROVIDER_CALL",
            "closed",
            True,
            False,
            False,
            False,
            130,
        ),
        OperatorScriptReviewEntry(
            "r21t_e_next_step",
            "Next step is operator script dry build with no run",
            NEXT_STEP,
            "NEXT",
            "next",
            True,
            False,
            False,
            False,
            140,
        ),
    )
    return tuple(sorted(entries, key=lambda entry: entry.ordinal))


def build_private_preview_operator_script_review() -> OperatorScriptReview:
    """Build the R21T-D private preview operator script review-only payload."""
    return OperatorScriptReview(
        review_id=REVIEW_ID,
        status="R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW=READY",
        source_bindings=dict(SOURCE_BINDINGS),
        operator_script_review_tokens=dict(OPERATOR_SCRIPT_REVIEW_TOKENS),
        operator_script_sections=OPERATOR_SCRIPT_SECTIONS,
        operator_entries=_build_operator_entries(),
        next_step=NEXT_STEP,
    )


def operator_script_review_to_dict(
    review: OperatorScriptReview | None = None,
) -> dict[str, Any]:
    """Return the R21T-D operator script review as a JSON-friendly dictionary."""
    if review is None:
        review = build_private_preview_operator_script_review()

    return {
        "review_id": review.review_id,
        "status": review.status,
        "R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW": READY_STATUS,
        "source_bindings": dict(review.source_bindings),
        "operator_script_review_tokens": dict(review.operator_script_review_tokens),
        "operator_script_sections": list(review.operator_script_sections),
        "operator_entries": [asdict(entry) for entry in review.operator_entries],
        "next_step": review.next_step,
    }


def build_private_preview_operator_script_review_with_sources() -> dict[str, Any]:
    """Build the R21T-D payload with bound R21T-C source summary."""
    r21t_c = build_private_preview_runner_build_review_with_sources()
    review = operator_script_review_to_dict()

    return {
        **review,
        "source_summaries": {
            "r21t_c_runner_build_review": r21t_c["review_id"],
            "r21t_c_status": r21t_c["R21T_C_PRIVATE_PREVIEW_RUNNER_BUILD_REVIEW"],
            "r21t_c_reflex_version": r21t_c["build_review_tokens"]["REFLEX_VERSION"],
            "r21t_c_next_step": r21t_c["next_step"],
        },
    }


def validate_private_preview_operator_script_review(
    payload: dict[str, Any] | None = None,
) -> tuple[str, ...]:
    """Return validation errors. Empty tuple means the R21T-D payload is valid."""
    if payload is None:
        payload = build_private_preview_operator_script_review_with_sources()

    errors: list[str] = []
    if payload.get("review_id") != REVIEW_ID:
        errors.append("review_id_mismatch")
    if payload.get("R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW") != READY_STATUS:
        errors.append("operator_script_review_not_ready")

    bindings = payload.get("source_bindings")
    if not isinstance(bindings, dict):
        errors.append("missing_source_bindings")
    else:
        for key, expected in SOURCE_BINDINGS.items():
            if bindings.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    tokens = payload.get("operator_script_review_tokens")
    if not isinstance(tokens, dict):
        errors.append("missing_operator_script_review_tokens")
    else:
        for key, expected in OPERATOR_SCRIPT_REVIEW_TOKENS.items():
            if tokens.get(key) != expected:
                errors.append(f"{key}_mismatch")

    if tuple(payload.get("operator_script_sections", ())) != OPERATOR_SCRIPT_SECTIONS:
        errors.append("operator_script_sections_mismatch")

    entries = payload.get("operator_entries")
    if not isinstance(entries, list):
        errors.append("missing_operator_entries")
    else:
        entry_ids = {
            entry.get("operator_entry_id") for entry in entries if isinstance(entry, dict)
        }
        if set(REQUIRED_OPERATOR_ENTRY_IDS) - entry_ids:
            errors.append("missing_operator_entries")
        ordinals = [entry.get("ordinal") for entry in entries if isinstance(entry, dict)]
        if ordinals != sorted(ordinals):
            errors.append("operator_entries_not_deterministic")
        for entry in entries:
            if not isinstance(entry, dict):
                errors.append("invalid_operator_entry")
                continue
            if entry.get("metadata_only") is not True:
                errors.append(f"metadata_only_missing={entry.get('operator_entry_id')}")
            if entry.get("script_action_allowed") is not False:
                errors.append(f"script_action_open={entry.get('operator_entry_id')}")
            if entry.get("runtime_action_allowed") is not False:
                errors.append(f"runtime_action_open={entry.get('operator_entry_id')}")
            if entry.get("preview_readiness_claimed") is not False:
                errors.append(
                    f"preview_readiness_claimed={entry.get('operator_entry_id')}"
                )

    summaries = payload.get("source_summaries")
    if isinstance(summaries, dict):
        if summaries.get("r21t_c_runner_build_review") != (
            "R21T_C_PRIVATE_PREVIEW_RUNNER_BUILD_REVIEW_ONLY"
        ):
            errors.append("r21t_c_source_mismatch")
        if summaries.get("r21t_c_status") != READY_STATUS:
            errors.append("r21t_c_status_mismatch")
        if summaries.get("r21t_c_reflex_version") != REFLEX_VERSION:
            errors.append("r21t_c_version_mismatch")
        if summaries.get("r21t_c_next_step") != REVIEW_ID:
            errors.append("r21t_c_next_step_mismatch")

    if payload.get("next_step") != NEXT_STEP:
        errors.append("next_step_mismatch")

    return tuple(errors)


def render_private_preview_operator_script_markdown(
    payload: dict[str, Any] | None = None,
) -> str:
    """Render the R21T-D operator script review as markdown text only."""
    if payload is None:
        payload = build_private_preview_operator_script_review_with_sources()

    lines = [
        "# R21T-D Private Preview Runner Operator Script - Review Only",
        "",
        f"Status: `{payload['status']}`",
        "",
        "R21T-D records future operator script sections as metadata only.",
        "It creates no script file and does not claim preview readiness.",
        "",
        "## Source Bindings",
    ]
    for key in sorted(payload["source_bindings"]):
        lines.append(f"- `{key}` = `{payload['source_bindings'][key]}`")

    lines.extend(["", "## Operator Script Review Tokens"])
    for key in sorted(payload["operator_script_review_tokens"]):
        lines.append(f"- `{key}` = `{payload['operator_script_review_tokens'][key]}`")

    lines.extend(["", "## Future Operator Script Sections"])
    for section in payload["operator_script_sections"]:
        lines.append(f"- `{section}`")

    lines.extend(["", "## Operator Review Entries"])
    for entry in payload["operator_entries"]:
        lines.append(
            "- "
            f"`{entry['operator_entry_id']}` - {entry['title']} - "
            f"`{entry['required_token']}` - `{entry['required_state']}`"
        )

    lines.extend(
        [
            "",
            "## Review Decision",
            "`OPERATOR_SCRIPT_REVIEW_ONLY` is `True`.",
            "`SCRIPT_FILE_CREATED` is `False`.",
            "`PS1_CREATED` is `False`.",
            "`SCRIPT_EXECUTED` is `False`.",
            "`RUNNER_EXECUTED` is `False`.",
            "`NO_RUNTIME_EXECUTION` is `True`.",
            "`NO_PREVIEW_ATTEMPT` is `True`.",
            "`REFLEX_RUNTIME_STATUS` remains `PAUSED`.",
            "",
            f"NEXT={payload['next_step']}",
        ]
    )
    return "\n".join(lines) + "\n"
