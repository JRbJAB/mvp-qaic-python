"""R21T-E private preview operator script dry-build payload.

This module is deterministic metadata only. It records that the R21T-E
PowerShell operator script artifact exists, remains dry-build/no-run only, and
was not executed by this batch.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Final

from mvp_qaic_py.reflex_private_preview_operator_script_review_r21t_d import (
    REFLEX_VERSION,
    REVIEW_ID as R21T_D_REVIEW_ID,
    build_private_preview_operator_script_review_with_sources,
)

DRY_BUILD_ID: Final[str] = "R21T_E_PRIVATE_PREVIEW_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN"
READY_STATUS: Final[str] = "READY"
PAUSED_STATUS: Final[str] = "PAUSED"
STOPPED_AFTER_OPERATOR_SCRIPT_DRY_BUILD: Final[str] = (
    "STOPPED_AFTER_OPERATOR_SCRIPT_DRY_BUILD"
)
NEXT_STEP: Final[str] = "R21T_F_PRIVATE_PREVIEW_OPERATOR_SCRIPT_REVIEW_AND_ARMING_NO_RUN"

DOC_PATH: Final[Path] = Path(
    "docs/PRODUCT/R21T_E_PRIVATE_PREVIEW_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN.md"
)
PS1_PATH: Final[Path] = Path("tools/reflex_private_preview_operator_r21t_e_no_run.ps1")
MODULE_PATH: Final[Path] = Path(
    "mvp_qaic_py/reflex_private_preview_operator_script_dry_build_r21t_e.py"
)
TEST_PATH: Final[Path] = Path(
    "tests/test_r21t_e_private_preview_operator_script_dry_build.py"
)
R21T_E_FILES: Final[tuple[Path, ...]] = (DOC_PATH, PS1_PATH, MODULE_PATH, TEST_PATH)

SOURCE_BINDINGS: Final[dict[str, bool]] = {
    "SOURCE_R21T_D_OPERATOR_SCRIPT_REVIEW_BOUND": True,
}

DRY_BUILD_TOKENS: Final[dict[str, bool | str]] = {
    "R21T_E_PRIVATE_PREVIEW_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN": READY_STATUS,
    "SOURCE_R21T_D_OPERATOR_SCRIPT_REVIEW_BOUND": True,
    "SCRIPT_DRY_BUILD_ONLY": True,
    "SCRIPT_FILE_CREATED": True,
    "PS1_CREATED": True,
    "SCRIPT_EXECUTED": False,
    "RUNNER_EXECUTED": False,
    "RUNTIME_EXECUTION_ALLOWED": False,
    "NO_RUNTIME_EXECUTION": True,
    "NO_DOCKER_EXECUTION": True,
    "NO_REFLEX_APP_START": True,
    "NO_PREVIEW_ATTEMPT": True,
    "NO_PORTS_OPENED": True,
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
    "REFLEX_RUNTIME_RUNNER_CHAIN": STOPPED_AFTER_OPERATOR_SCRIPT_DRY_BUILD,
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

OPERATOR_DRY_BUILD_SECTIONS: Final[tuple[str, ...]] = (
    "STRICT_PREFLIGHT_DRY_PLAN",
    "HARD_TIMEOUT_NATIVE_CALLS_REQUIRED_LATER",
    "PINNED_IMAGE_PREFLIGHT_REQUIRED_LATER",
    "PRIVATE_PORT_PREFLIGHT_REQUIRED_LATER",
    "FULL_HEAD_COPY_BY_ARCHIVE_TAR_REQUIRED_LATER",
    "POLICY_GUARD_CHECKS_REQUIRED_LATER",
    "HELP_VERSION_EVIDENCE_REUSE",
    "PREVIEW_READINESS_PROBES_REQUIRED_LATER",
    "FAILURE_STOP_DIAGNOSTICS_REQUIRED_LATER",
    "SUMMARY_NO_RUN_ONLY",
)

REQUIRED_DRY_BUILD_ENTRY_IDS: Final[tuple[str, ...]] = (
    "r21t_d_operator_script_review_bound",
    "dry_build_only_boundary",
    "ps1_artifact_created",
    "script_not_executed",
    "runtime_paths_closed",
    "help_version_evidence_reused",
    "private_preview_readiness_not_claimed",
    "hardening_requirements_preserved",
    "safety_locks_closed",
    "r21t_f_next_step",
)


@dataclass(frozen=True)
class OperatorScriptDryBuildEntry:
    """Single R21T-E operator-script dry-build metadata entry."""

    dry_build_entry_id: str
    title: str
    source_reference: str
    required_token: str
    required_state: str
    dry_build_only: bool
    script_execution_allowed: bool
    runtime_execution_allowed: bool
    preview_readiness_claimed: bool
    ordinal: int


@dataclass(frozen=True)
class OperatorScriptDryBuild:
    """Top-level R21T-E operator-script dry-build object."""

    dry_build_id: str
    status: str
    source_bindings: dict[str, bool]
    dry_build_tokens: dict[str, bool | str]
    dry_build_sections: tuple[str, ...]
    dry_build_entries: tuple[OperatorScriptDryBuildEntry, ...]
    files_created: tuple[str, ...]
    next_step: str


def _build_dry_build_entries() -> tuple[OperatorScriptDryBuildEntry, ...]:
    """Build stable R21T-E dry-build metadata entries."""
    entries = (
        OperatorScriptDryBuildEntry(
            "r21t_d_operator_script_review_bound",
            "R21T-E is bound to the R21T-D operator script review-only gate",
            "docs/PRODUCT/R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW_ONLY.md",
            "SOURCE_R21T_D_OPERATOR_SCRIPT_REVIEW_BOUND",
            "bound",
            True,
            False,
            False,
            False,
            10,
        ),
        OperatorScriptDryBuildEntry(
            "dry_build_only_boundary",
            "The operator script artifact is dry-build/no-run only",
            DRY_BUILD_ID,
            "SCRIPT_DRY_BUILD_ONLY",
            "true",
            True,
            False,
            False,
            False,
            20,
        ),
        OperatorScriptDryBuildEntry(
            "ps1_artifact_created",
            "The PowerShell 5.1 compatible no-run script artifact exists",
            str(PS1_PATH),
            "PS1_CREATED",
            "true",
            True,
            False,
            False,
            False,
            30,
        ),
        OperatorScriptDryBuildEntry(
            "script_not_executed",
            "R21T-E creates the script but does not execute it",
            str(TEST_PATH),
            "SCRIPT_EXECUTED",
            "false",
            True,
            False,
            False,
            False,
            40,
        ),
        OperatorScriptDryBuildEntry(
            "runtime_paths_closed",
            "Runtime, Docker, Reflex app, ports, preview, and browser paths remain closed",
            "docs/FINAL/R21B_REFLEX_RUNTIME_CLOSURE_STRATEGY_AND_INSTRUCTIONS_MEMO_20260701.md",
            "NO_RUNTIME_EXECUTION",
            "true",
            True,
            False,
            False,
            False,
            50,
        ),
        OperatorScriptDryBuildEntry(
            "help_version_evidence_reused",
            "R21T-E reuses passed help/version evidence and keeps the forbidden flag absent",
            "docs/RUNTIME/REFLEX_CLI_CONTRACT_H8I.md",
            "HELP_VERSION_CAPTURE_PASSED",
            "true",
            True,
            False,
            False,
            False,
            60,
        ),
        OperatorScriptDryBuildEntry(
            "private_preview_readiness_not_claimed",
            "Preview readiness still requires non-empty HTTP frontend evidence later",
            "docs/RUNTIME/REFLEX_READINESS_ANTI_LOOP_POLICY_R16F2H6.md",
            "HTTP_FRONTEND_NON_EMPTY_REQUIRED",
            "required",
            True,
            False,
            False,
            False,
            70,
        ),
        OperatorScriptDryBuildEntry(
            "hardening_requirements_preserved",
            "Hard timeout, image, port, archive, policy, and report requirements remain required",
            "docs/RUNTIME/REFLEX_RUNNER_HARDENING_POLICY_R16F2H7I.md",
            "HARD_TIMEOUT_REQUIRED",
            "required",
            True,
            False,
            False,
            False,
            80,
        ),
        OperatorScriptDryBuildEntry(
            "safety_locks_closed",
            "Release, provider, trading, Sheet/BQ, HTML, and export paths remain closed",
            "docs/PROCESS/ASSISTANT_REFLEX_INSTRUCTION_LOCK_R16F2H4.md",
            "NO_PROVIDER_CALL",
            "closed",
            True,
            False,
            False,
            False,
            90,
        ),
        OperatorScriptDryBuildEntry(
            "r21t_f_next_step",
            "Next step is review and arming with no run",
            NEXT_STEP,
            "NEXT",
            "next",
            True,
            False,
            False,
            False,
            100,
        ),
    )
    return tuple(sorted(entries, key=lambda entry: entry.ordinal))


def build_private_preview_operator_script_dry_build() -> OperatorScriptDryBuild:
    """Build the R21T-E private preview operator script dry-build payload."""
    return OperatorScriptDryBuild(
        dry_build_id=DRY_BUILD_ID,
        status="R21T_E_PRIVATE_PREVIEW_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN=READY",
        source_bindings=dict(SOURCE_BINDINGS),
        dry_build_tokens=dict(DRY_BUILD_TOKENS),
        dry_build_sections=OPERATOR_DRY_BUILD_SECTIONS,
        dry_build_entries=_build_dry_build_entries(),
        files_created=tuple(str(path) for path in R21T_E_FILES),
        next_step=NEXT_STEP,
    )


def operator_script_dry_build_to_dict(
    dry_build: OperatorScriptDryBuild | None = None,
) -> dict[str, Any]:
    """Return the R21T-E dry-build payload as a JSON-friendly dictionary."""
    if dry_build is None:
        dry_build = build_private_preview_operator_script_dry_build()

    return {
        "dry_build_id": dry_build.dry_build_id,
        "status": dry_build.status,
        "R21T_E_PRIVATE_PREVIEW_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN": READY_STATUS,
        "source_bindings": dict(dry_build.source_bindings),
        "dry_build_tokens": dict(dry_build.dry_build_tokens),
        "dry_build_sections": list(dry_build.dry_build_sections),
        "dry_build_entries": [
            asdict(entry) for entry in dry_build.dry_build_entries
        ],
        "files_created": list(dry_build.files_created),
        "next_step": dry_build.next_step,
    }


def build_private_preview_operator_script_dry_build_with_sources() -> dict[str, Any]:
    """Build the R21T-E payload with bound R21T-D source summary."""
    r21t_d = build_private_preview_operator_script_review_with_sources()
    dry_build = operator_script_dry_build_to_dict()

    return {
        **dry_build,
        "source_summaries": {
            "r21t_d_operator_script_review": r21t_d["review_id"],
            "r21t_d_status": r21t_d["R21T_D_PRIVATE_PREVIEW_RUNNER_OPERATOR_SCRIPT_REVIEW"],
            "r21t_d_reflex_version": r21t_d["operator_script_review_tokens"][
                "REFLEX_VERSION"
            ],
            "r21t_d_next_step": r21t_d["next_step"],
        },
    }


def validate_private_preview_operator_script_dry_build(
    payload: dict[str, Any] | None = None,
) -> tuple[str, ...]:
    """Return validation errors. Empty tuple means the R21T-E payload is valid."""
    if payload is None:
        payload = build_private_preview_operator_script_dry_build_with_sources()

    errors: list[str] = []
    if payload.get("dry_build_id") != DRY_BUILD_ID:
        errors.append("dry_build_id_mismatch")
    if payload.get("R21T_E_PRIVATE_PREVIEW_OPERATOR_SCRIPT_DRY_BUILD_NO_RUN") != READY_STATUS:
        errors.append("dry_build_not_ready")

    bindings = payload.get("source_bindings")
    if not isinstance(bindings, dict):
        errors.append("missing_source_bindings")
    else:
        for key, expected in SOURCE_BINDINGS.items():
            if bindings.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    tokens = payload.get("dry_build_tokens")
    if not isinstance(tokens, dict):
        errors.append("missing_dry_build_tokens")
    else:
        for key, expected in DRY_BUILD_TOKENS.items():
            if tokens.get(key) != expected:
                errors.append(f"{key}_mismatch")

    if tuple(payload.get("dry_build_sections", ())) != OPERATOR_DRY_BUILD_SECTIONS:
        errors.append("dry_build_sections_mismatch")
    if tuple(payload.get("files_created", ())) != tuple(str(path) for path in R21T_E_FILES):
        errors.append("files_created_mismatch")

    entries = payload.get("dry_build_entries")
    if not isinstance(entries, list):
        errors.append("missing_dry_build_entries")
    else:
        entry_ids = {
            entry.get("dry_build_entry_id") for entry in entries if isinstance(entry, dict)
        }
        if set(REQUIRED_DRY_BUILD_ENTRY_IDS) - entry_ids:
            errors.append("missing_dry_build_entries")
        ordinals = [entry.get("ordinal") for entry in entries if isinstance(entry, dict)]
        if ordinals != sorted(ordinals):
            errors.append("dry_build_entries_not_deterministic")
        for entry in entries:
            if not isinstance(entry, dict):
                errors.append("invalid_dry_build_entry")
                continue
            if entry.get("dry_build_only") is not True:
                errors.append(f"dry_build_only_missing={entry.get('dry_build_entry_id')}")
            if entry.get("script_execution_allowed") is not False:
                errors.append(f"script_execution_open={entry.get('dry_build_entry_id')}")
            if entry.get("runtime_execution_allowed") is not False:
                errors.append(f"runtime_execution_open={entry.get('dry_build_entry_id')}")
            if entry.get("preview_readiness_claimed") is not False:
                errors.append(
                    f"preview_readiness_claimed={entry.get('dry_build_entry_id')}"
                )

    summaries = payload.get("source_summaries")
    if isinstance(summaries, dict):
        if summaries.get("r21t_d_operator_script_review") != R21T_D_REVIEW_ID:
            errors.append("r21t_d_source_mismatch")
        if summaries.get("r21t_d_status") != READY_STATUS:
            errors.append("r21t_d_status_mismatch")
        if summaries.get("r21t_d_reflex_version") != REFLEX_VERSION:
            errors.append("r21t_d_version_mismatch")
        if summaries.get("r21t_d_next_step") != DRY_BUILD_ID:
            errors.append("r21t_d_next_step_mismatch")

    if payload.get("next_step") != NEXT_STEP:
        errors.append("next_step_mismatch")

    return tuple(errors)


def render_private_preview_operator_script_dry_build_markdown(
    payload: dict[str, Any] | None = None,
) -> str:
    """Render the R21T-E operator script dry build as markdown text only."""
    if payload is None:
        payload = build_private_preview_operator_script_dry_build_with_sources()

    lines = [
        "# R21T-E Private Preview Operator Script Dry Build - No Run",
        "",
        f"Status: `{payload['status']}`",
        "",
        "R21T-E creates the operator script artifact as dry-build/no-run only.",
        "It does not execute the script, runner, runtime, or preview path.",
        "",
        "## Source Bindings",
    ]
    for key in sorted(payload["source_bindings"]):
        lines.append(f"- `{key}` = `{payload['source_bindings'][key]}`")

    lines.extend(["", "## Dry-Build Tokens"])
    for key in sorted(payload["dry_build_tokens"]):
        lines.append(f"- `{key}` = `{payload['dry_build_tokens'][key]}`")

    lines.extend(["", "## Dry-Build Sections"])
    for section in payload["dry_build_sections"]:
        lines.append(f"- `{section}`")

    lines.extend(["", "## Files Created"])
    for path in payload["files_created"]:
        lines.append(f"- `{path}`")

    lines.extend(["", "## Dry-Build Entries"])
    for entry in payload["dry_build_entries"]:
        lines.append(
            "- "
            f"`{entry['dry_build_entry_id']}` - {entry['title']} - "
            f"`{entry['required_token']}` - `{entry['required_state']}`"
        )

    lines.extend(
        [
            "",
            "## Dry-Build Decision",
            "`SCRIPT_DRY_BUILD_ONLY` is `True`.",
            "`SCRIPT_FILE_CREATED` is `True`.",
            "`PS1_CREATED` is `True`.",
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
