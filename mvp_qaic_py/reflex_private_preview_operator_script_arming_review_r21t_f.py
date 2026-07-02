"""R21T-F private preview operator script arming review metadata.

This module is deterministic metadata only. It binds to the R21T-E dry-build
operator script artifact and records that arming is not ready and no script or
runtime execution is allowed by this batch.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Final

from mvp_qaic_py.reflex_private_preview_operator_script_dry_build_r21t_e import (
    DRY_BUILD_ID as R21T_E_DRY_BUILD_ID,
    PS1_PATH as R21T_E_PS1_PATH,
    REFLEX_VERSION,
    build_private_preview_operator_script_dry_build_with_sources,
)

ARMING_REVIEW_ID: Final[str] = (
    "R21T_F_PRIVATE_PREVIEW_OPERATOR_SCRIPT_REVIEW_AND_ARMING_NO_RUN"
)
READY_STATUS: Final[str] = "READY"
PAUSED_STATUS: Final[str] = "PAUSED"
STOPPED_AFTER_ARMING_REVIEW_NO_RUN: Final[str] = (
    "STOPPED_AFTER_ARMING_REVIEW_NO_RUN"
)
REQUIRED_FINAL_OPERATOR_MARKER: Final[str] = (
    "R21T_G_OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN_TRUE"
)
NEXT_STEP: Final[str] = "R21T_G_FINAL_OPERATOR_MARKER_GATE_NO_RUN"

DOC_PATH: Final[Path] = Path(
    "docs/PRODUCT/R21T_F_PRIVATE_PREVIEW_OPERATOR_SCRIPT_REVIEW_AND_ARMING_NO_RUN.md"
)
MODULE_PATH: Final[Path] = Path(
    "mvp_qaic_py/reflex_private_preview_operator_script_arming_review_r21t_f.py"
)
TEST_PATH: Final[Path] = Path(
    "tests/test_r21t_f_private_preview_operator_script_arming_review.py"
)
R21T_F_FILES: Final[tuple[Path, ...]] = (DOC_PATH, MODULE_PATH, TEST_PATH)

SOURCE_BINDINGS: Final[dict[str, bool]] = {
    "SOURCE_R21T_E_DRY_BUILD_BOUND": True,
    "OPERATOR_SCRIPT_EXISTS": True,
    "OPERATOR_SCRIPT_EXECUTED": False,
}

ARMING_REVIEW_TOKENS: Final[dict[str, bool | str]] = {
    "R21T_F_PRIVATE_PREVIEW_OPERATOR_SCRIPT_REVIEW_AND_ARMING_NO_RUN": READY_STATUS,
    "SOURCE_R21T_E_DRY_BUILD_BOUND": True,
    "OPERATOR_SCRIPT_EXISTS": True,
    "OPERATOR_SCRIPT_EXECUTED": False,
    "ARMING_REVIEW_ONLY": True,
    "ARMING_READY": False,
    "RUNTIME_ARMED": False,
    "RUNTIME_EXECUTION_ALLOWED": False,
    "SCRIPT_EXECUTION_ALLOWED": False,
    "NO_RUNTIME_EXECUTION": True,
    "NO_DOCKER_EXECUTION": True,
    "NO_REFLEX_APP_START": True,
    "NO_PREVIEW_ATTEMPT": True,
    "NO_PORTS_OPENED": True,
    "NO_BROWSER": True,
    "REFLEX_VERSION": REFLEX_VERSION,
    "HELP_VERSION_CAPTURE_PASSED": True,
    "NO_FRONTEND_HOST_FLAG": True,
    "HTTP_FRONTEND_NON_EMPTY_REQUIRED": True,
    "TCP_ONLY_NOT_PREVIEW_READY": True,
    "PREVIEW_ONLY_AFTER_HTTP_PASS": True,
    "REFLEX_RUNTIME_STATUS": PAUSED_STATUS,
    "REFLEX_RUNTIME_RUNNER_CHAIN": STOPPED_AFTER_ARMING_REVIEW_NO_RUN,
    "REQUIRED_FINAL_OPERATOR_MARKER": REQUIRED_FINAL_OPERATOR_MARKER,
    "FINAL_OPERATOR_MARKER_PRESENT": False,
    "PS51_COMPATIBLE": True,
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

ARMING_REVIEW_SECTIONS: Final[tuple[str, ...]] = (
    "R21T_E_DRY_BUILD_BINDING",
    "OPERATOR_SCRIPT_EXISTENCE_REVIEW",
    "SCRIPT_NOT_EXECUTED",
    "ARMING_REVIEW_ONLY_BOUNDARY",
    "FINAL_OPERATOR_MARKER_GATE_REQUIRED",
    "RUNTIME_REMAINS_PAUSED",
    "READINESS_REQUIRES_HTTP_FRONTEND",
    "RUNNER_HARDENING_REQUIREMENTS_PRESERVED",
    "SAFETY_LOCKS_CLOSED",
    "R21T_G_NEXT_GATE",
)

REQUIRED_ARMING_ENTRY_IDS: Final[tuple[str, ...]] = (
    "r21t_e_dry_build_bound",
    "operator_script_exists",
    "operator_script_not_executed",
    "arming_review_only",
    "arming_not_ready",
    "runtime_not_armed",
    "script_execution_closed",
    "final_operator_marker_required_absent",
    "readiness_requires_http",
    "safety_locks_closed",
)


@dataclass(frozen=True)
class OperatorScriptArmingReviewEntry:
    """Single R21T-F arming review metadata entry."""

    arming_entry_id: str
    title: str
    source_reference: str
    required_token: str
    required_state: str
    arming_review_only: bool
    arming_ready: bool
    runtime_armed: bool
    script_execution_allowed: bool
    ordinal: int


@dataclass(frozen=True)
class OperatorScriptArmingReview:
    """Top-level R21T-F arming review object."""

    arming_review_id: str
    status: str
    source_bindings: dict[str, bool]
    arming_review_tokens: dict[str, bool | str]
    arming_review_sections: tuple[str, ...]
    arming_review_entries: tuple[OperatorScriptArmingReviewEntry, ...]
    files_created: tuple[str, ...]
    next_step: str


def _build_arming_review_entries() -> tuple[OperatorScriptArmingReviewEntry, ...]:
    """Build stable R21T-F arming review metadata entries."""
    entries = (
        OperatorScriptArmingReviewEntry(
            "r21t_e_dry_build_bound",
            "R21T-F is bound to the R21T-E dry-build artifact",
            "docs/PRODUCT/R21T_E_PRIVATE_PREVIEW_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN.md",
            "SOURCE_R21T_E_DRY_BUILD_BOUND",
            "bound",
            True,
            False,
            False,
            False,
            10,
        ),
        OperatorScriptArmingReviewEntry(
            "operator_script_exists",
            "The R21T-E PowerShell operator script exists as a reviewed artifact",
            str(R21T_E_PS1_PATH),
            "OPERATOR_SCRIPT_EXISTS",
            "true",
            True,
            False,
            False,
            False,
            20,
        ),
        OperatorScriptArmingReviewEntry(
            "operator_script_not_executed",
            "The R21T-E PowerShell operator script was not executed by R21T-F",
            str(TEST_PATH),
            "OPERATOR_SCRIPT_EXECUTED",
            "false",
            True,
            False,
            False,
            False,
            30,
        ),
        OperatorScriptArmingReviewEntry(
            "arming_review_only",
            "R21T-F is arming review metadata only",
            ARMING_REVIEW_ID,
            "ARMING_REVIEW_ONLY",
            "true",
            True,
            False,
            False,
            False,
            40,
        ),
        OperatorScriptArmingReviewEntry(
            "arming_not_ready",
            "Arming readiness remains false",
            ARMING_REVIEW_ID,
            "ARMING_READY",
            "false",
            True,
            False,
            False,
            False,
            50,
        ),
        OperatorScriptArmingReviewEntry(
            "runtime_not_armed",
            "Runtime remains unarmed and paused",
            "docs/FINAL/R21B_REFLEX_RUNTIME_CLOSURE_STRATEGY_AND_INSTRUCTIONS_MEMO_20260701.md",
            "RUNTIME_ARMED",
            "false",
            True,
            False,
            False,
            False,
            60,
        ),
        OperatorScriptArmingReviewEntry(
            "script_execution_closed",
            "Script execution remains closed until the R21T-G marker gate",
            REQUIRED_FINAL_OPERATOR_MARKER,
            "SCRIPT_EXECUTION_ALLOWED",
            "false",
            True,
            False,
            False,
            False,
            70,
        ),
        OperatorScriptArmingReviewEntry(
            "final_operator_marker_required_absent",
            "The final operator marker is required and absent",
            REQUIRED_FINAL_OPERATOR_MARKER,
            "FINAL_OPERATOR_MARKER_PRESENT",
            "false",
            True,
            False,
            False,
            False,
            80,
        ),
        OperatorScriptArmingReviewEntry(
            "readiness_requires_http",
            "Preview remains gated by non-empty HTTP frontend evidence",
            "docs/RUNTIME/REFLEX_CLI_CONTRACT_H8I.md",
            "HTTP_FRONTEND_NON_EMPTY_REQUIRED",
            "required",
            True,
            False,
            False,
            False,
            90,
        ),
        OperatorScriptArmingReviewEntry(
            "safety_locks_closed",
            "Release, provider, trading, Sheet/BQ, and HTML paths remain closed",
            "docs/PROCESS/ASSISTANT_REFLEX_INSTRUCTION_LOCK_R16F2H4.md",
            "NO_PROVIDER_CALL",
            "closed",
            True,
            False,
            False,
            False,
            100,
        ),
    )
    return tuple(sorted(entries, key=lambda entry: entry.ordinal))


def build_private_preview_operator_script_arming_review() -> OperatorScriptArmingReview:
    """Build the R21T-F private preview operator script arming review payload."""
    return OperatorScriptArmingReview(
        arming_review_id=ARMING_REVIEW_ID,
        status="R21T_F_PRIVATE_PREVIEW_OPERATOR_SCRIPT_REVIEW_AND_ARMING_NO_RUN=READY",
        source_bindings=dict(SOURCE_BINDINGS),
        arming_review_tokens=dict(ARMING_REVIEW_TOKENS),
        arming_review_sections=ARMING_REVIEW_SECTIONS,
        arming_review_entries=_build_arming_review_entries(),
        files_created=tuple(str(path) for path in R21T_F_FILES),
        next_step=NEXT_STEP,
    )


def operator_script_arming_review_to_dict(
    arming_review: OperatorScriptArmingReview | None = None,
) -> dict[str, Any]:
    """Return the R21T-F arming review payload as a JSON-friendly dictionary."""
    if arming_review is None:
        arming_review = build_private_preview_operator_script_arming_review()

    return {
        "arming_review_id": arming_review.arming_review_id,
        "status": arming_review.status,
        "R21T_F_PRIVATE_PREVIEW_OPERATOR_SCRIPT_REVIEW_AND_ARMING_NO_RUN": (
            READY_STATUS
        ),
        "source_bindings": dict(arming_review.source_bindings),
        "arming_review_tokens": dict(arming_review.arming_review_tokens),
        "arming_review_sections": list(arming_review.arming_review_sections),
        "arming_review_entries": [
            asdict(entry) for entry in arming_review.arming_review_entries
        ],
        "files_created": list(arming_review.files_created),
        "next_step": arming_review.next_step,
    }


def build_private_preview_operator_script_arming_review_with_sources() -> dict[str, Any]:
    """Build the R21T-F payload with bound R21T-E source summary."""
    r21t_e = build_private_preview_operator_script_dry_build_with_sources()
    arming_review = operator_script_arming_review_to_dict()

    return {
        **arming_review,
        "source_summaries": {
            "r21t_e_dry_build": r21t_e["dry_build_id"],
            "r21t_e_status": r21t_e[
                "R21T_E_PRIVATE_PREVIEW_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN"
            ],
            "r21t_e_script_executed": r21t_e["dry_build_tokens"][
                "SCRIPT_EXECUTED"
            ],
            "r21t_e_runtime_execution_allowed": r21t_e["dry_build_tokens"][
                "RUNTIME_EXECUTION_ALLOWED"
            ],
            "r21t_e_reflex_version": r21t_e["dry_build_tokens"]["REFLEX_VERSION"],
            "r21t_e_next_step": r21t_e["next_step"],
        },
    }


def validate_private_preview_operator_script_arming_review(
    payload: dict[str, Any] | None = None,
) -> tuple[str, ...]:
    """Return validation errors. Empty tuple means the R21T-F payload is valid."""
    if payload is None:
        payload = build_private_preview_operator_script_arming_review_with_sources()

    errors: list[str] = []
    if payload.get("arming_review_id") != ARMING_REVIEW_ID:
        errors.append("arming_review_id_mismatch")
    if (
        payload.get("R21T_F_PRIVATE_PREVIEW_OPERATOR_SCRIPT_REVIEW_AND_ARMING_NO_RUN")
        != READY_STATUS
    ):
        errors.append("arming_review_not_ready")

    bindings = payload.get("source_bindings")
    if not isinstance(bindings, dict):
        errors.append("missing_source_bindings")
    else:
        for key, expected in SOURCE_BINDINGS.items():
            if bindings.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    tokens = payload.get("arming_review_tokens")
    if not isinstance(tokens, dict):
        errors.append("missing_arming_review_tokens")
    else:
        for key, expected in ARMING_REVIEW_TOKENS.items():
            if tokens.get(key) != expected:
                errors.append(f"{key}_mismatch")

    if tuple(payload.get("arming_review_sections", ())) != ARMING_REVIEW_SECTIONS:
        errors.append("arming_review_sections_mismatch")
    if tuple(payload.get("files_created", ())) != tuple(str(path) for path in R21T_F_FILES):
        errors.append("files_created_mismatch")

    entries = payload.get("arming_review_entries")
    if not isinstance(entries, list):
        errors.append("missing_arming_review_entries")
    else:
        entry_ids = {
            entry.get("arming_entry_id") for entry in entries if isinstance(entry, dict)
        }
        if set(REQUIRED_ARMING_ENTRY_IDS) - entry_ids:
            errors.append("missing_arming_review_entries")
        ordinals = [entry.get("ordinal") for entry in entries if isinstance(entry, dict)]
        if ordinals != sorted(ordinals):
            errors.append("arming_review_entries_not_deterministic")
        for entry in entries:
            if not isinstance(entry, dict):
                errors.append("invalid_arming_review_entry")
                continue
            entry_id = entry.get("arming_entry_id")
            if entry.get("arming_review_only") is not True:
                errors.append(f"arming_review_only_missing={entry_id}")
            if entry.get("arming_ready") is not False:
                errors.append(f"arming_ready_open={entry_id}")
            if entry.get("runtime_armed") is not False:
                errors.append(f"runtime_armed_open={entry_id}")
            if entry.get("script_execution_allowed") is not False:
                errors.append(f"script_execution_open={entry_id}")

    summaries = payload.get("source_summaries")
    if isinstance(summaries, dict):
        if summaries.get("r21t_e_dry_build") != R21T_E_DRY_BUILD_ID:
            errors.append("r21t_e_source_mismatch")
        if summaries.get("r21t_e_status") != READY_STATUS:
            errors.append("r21t_e_status_mismatch")
        if summaries.get("r21t_e_script_executed") is not False:
            errors.append("r21t_e_script_execution_mismatch")
        if summaries.get("r21t_e_runtime_execution_allowed") is not False:
            errors.append("r21t_e_runtime_execution_mismatch")
        if summaries.get("r21t_e_reflex_version") != REFLEX_VERSION:
            errors.append("r21t_e_version_mismatch")
        if summaries.get("r21t_e_next_step") != ARMING_REVIEW_ID:
            errors.append("r21t_e_next_step_mismatch")

    if payload.get("next_step") != NEXT_STEP:
        errors.append("next_step_mismatch")

    return tuple(errors)


def render_private_preview_operator_script_arming_review_markdown(
    payload: dict[str, Any] | None = None,
) -> str:
    """Render the R21T-F arming review as markdown text only."""
    if payload is None:
        payload = build_private_preview_operator_script_arming_review_with_sources()

    lines = [
        "# R21T-F Private Preview Operator Script Review and Arming - No Run",
        "",
        f"Status: `{payload['status']}`",
        "",
        "R21T-F reviews the R21T-E operator script artifact and records arming",
        "metadata only. It does not execute the script, arm runtime, or claim",
        "preview readiness.",
        "",
        "## Source Bindings",
    ]
    for key in sorted(payload["source_bindings"]):
        lines.append(f"- `{key}` = `{payload['source_bindings'][key]}`")

    lines.extend(["", "## Arming Review Tokens"])
    for key in sorted(payload["arming_review_tokens"]):
        lines.append(f"- `{key}` = `{payload['arming_review_tokens'][key]}`")

    lines.extend(["", "## Arming Review Sections"])
    for section in payload["arming_review_sections"]:
        lines.append(f"- `{section}`")

    lines.extend(["", "## Files Created"])
    for path in payload["files_created"]:
        lines.append(f"- `{path}`")

    lines.extend(["", "## Arming Review Entries"])
    for entry in payload["arming_review_entries"]:
        lines.append(
            "- "
            f"`{entry['arming_entry_id']}` - {entry['title']} - "
            f"`{entry['required_token']}` - `{entry['required_state']}`"
        )

    lines.extend(
        [
            "",
            "## Arming Decision",
            "`ARMING_REVIEW_ONLY` is `True`.",
            "`ARMING_READY` is `False`.",
            "`RUNTIME_ARMED` is `False`.",
            "`SCRIPT_EXECUTION_ALLOWED` is `False`.",
            "`FINAL_OPERATOR_MARKER_PRESENT` is `False`.",
            f"`REQUIRED_FINAL_OPERATOR_MARKER` is `{REQUIRED_FINAL_OPERATOR_MARKER}`.",
            "`REFLEX_RUNTIME_STATUS` remains `PAUSED`.",
            "",
            f"NEXT={payload['next_step']}",
        ]
    )
    return "\n".join(lines) + "\n"
