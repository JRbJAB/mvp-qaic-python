"""R21T-H marker accepted arming metadata.

This module is deterministic metadata only. It binds to the R21T-G marker gate
and records that the exact operator marker is present and accepted. It exposes
no runtime, script, Docker, preview, browser, provider, trading, Sheet/BQ,
release, or HTML output behavior for this batch.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Final

from mvp_qaic_py.reflex_private_preview_final_operator_marker_gate_r21t_g import (
    MARKER_GATE_ID as R21T_G_MARKER_GATE_ID,
    REFLEX_VERSION,
    REQUIRED_FINAL_OPERATOR_MARKER,
    build_final_operator_marker_gate_with_sources,
)

MARKER_ACCEPTED_ARMING_ID: Final[str] = "R21T_H_MARKER_ACCEPTED_ARMING_NO_RUN"
READY_STATUS: Final[str] = "READY"
ARMED_BUT_NOT_STARTED_STATUS: Final[str] = "ARMED_BUT_NOT_STARTED"
STOPPED_AFTER_MARKER_ACCEPTED_ARMING_NO_RUN: Final[str] = (
    "STOPPED_AFTER_MARKER_ACCEPTED_ARMING_NO_RUN"
)
NEXT_STEP: Final[str] = "R21T_I_OPERATOR_APPROVED_PRIVATE_PREVIEW_RUNTIME_RUN"

DOC_PATH: Final[Path] = Path("docs/PRODUCT/R21T_H_MARKER_ACCEPTED_ARMING_NO_RUN.md")
MODULE_PATH: Final[Path] = Path(
    "mvp_qaic_py/reflex_private_preview_marker_accepted_arming_no_run_r21t_h.py"
)
TEST_PATH: Final[Path] = Path("tests/test_r21t_h_marker_accepted_arming_no_run.py")
R21T_H_FILES: Final[tuple[Path, ...]] = (DOC_PATH, MODULE_PATH, TEST_PATH)

SOURCE_BINDINGS: Final[dict[str, bool]] = {
    "SOURCE_R21T_G_MARKER_GATE_BOUND": True,
}

MARKER_ACCEPTED_ARMING_TOKENS: Final[dict[str, bool | str]] = {
    "R21T_H_MARKER_ACCEPTED_ARMING_NO_RUN": READY_STATUS,
    "SOURCE_R21T_G_MARKER_GATE_BOUND": True,
    "REQUIRED_FINAL_OPERATOR_MARKER": REQUIRED_FINAL_OPERATOR_MARKER,
    "FINAL_OPERATOR_MARKER_PRESENT": True,
    "FINAL_OPERATOR_MARKER_ACCEPTED": True,
    "OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN": True,
    "ARMING_READY": True,
    "RUNTIME_ARMED": False,
    "SCRIPT_EXECUTION_ALLOWED_FOR_NEXT": True,
    "SCRIPT_EXECUTION_ALLOWED_IN_THIS_BATCH": False,
    "RUNTIME_EXECUTION_ALLOWED_FOR_NEXT": True,
    "RUNTIME_EXECUTION_ALLOWED_IN_THIS_BATCH": False,
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
    "REFLEX_RUNTIME_STATUS": ARMED_BUT_NOT_STARTED_STATUS,
    "REFLEX_RUNTIME_RUNNER_CHAIN": STOPPED_AFTER_MARKER_ACCEPTED_ARMING_NO_RUN,
    "PS51_COMPATIBLE": True,
    "HARD_TIMEOUT_REQUIRED": True,
    "IMAGE_PREFLIGHT_REQUIRED": True,
    "PORT_PREFLIGHT_REQUIRED": True,
    "GIT_ARCHIVE_HEAD_COPY_REQUIRED": True,
    "POLICY_GUARDS_REQUIRED": True,
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

MARKER_ACCEPTED_ARMING_SECTIONS: Final[tuple[str, ...]] = (
    "R21T_G_MARKER_GATE_BINDING",
    "FINAL_OPERATOR_MARKER_PRESENT",
    "FINAL_OPERATOR_MARKER_ACCEPTED",
    "OPERATOR_APPROVAL_TRUE",
    "ARMING_READY_FOR_NEXT_BATCH",
    "RUNTIME_ARMED_FALSE_THIS_BATCH",
    "SCRIPT_PERMISSION_NEXT_ONLY",
    "RUNTIME_PERMISSION_NEXT_ONLY",
    "THIS_BATCH_EXECUTION_CLOSED",
    "READINESS_REQUIRES_HTTP_FRONTEND",
    "RUNNER_HARDENING_REQUIREMENTS_PRESERVED",
    "SAFETY_LOCKS_CLOSED",
)

REQUIRED_ARMING_ENTRY_IDS: Final[tuple[str, ...]] = (
    "r21t_g_marker_gate_bound",
    "final_operator_marker_exact",
    "final_operator_marker_present",
    "final_operator_marker_accepted",
    "operator_approval_true",
    "arming_ready_next_batch",
    "runtime_not_armed_this_batch",
    "script_permission_next_only",
    "runtime_permission_next_only",
    "this_batch_execution_closed",
    "readiness_requires_http",
    "safety_locks_closed",
)


@dataclass(frozen=True)
class MarkerAcceptedArmingEntry:
    """Single R21T-H marker accepted arming metadata entry."""

    arming_entry_id: str
    title: str
    source_reference: str
    required_token: str
    required_state: str
    source_r21t_g_marker_gate_bound: bool
    final_operator_marker_present: bool
    final_operator_marker_accepted: bool
    operator_approved_private_preview_run: bool
    arming_ready: bool
    runtime_armed: bool
    script_execution_allowed_for_next: bool
    script_execution_allowed_in_this_batch: bool
    runtime_execution_allowed_for_next: bool
    runtime_execution_allowed_in_this_batch: bool
    ordinal: int


@dataclass(frozen=True)
class MarkerAcceptedArming:
    """Top-level R21T-H marker accepted arming object."""

    marker_accepted_arming_id: str
    status: str
    source_bindings: dict[str, bool]
    marker_accepted_arming_tokens: dict[str, bool | str]
    marker_accepted_arming_sections: tuple[str, ...]
    marker_accepted_arming_entries: tuple[MarkerAcceptedArmingEntry, ...]
    files_created: tuple[str, ...]
    next_step: str


def _build_marker_accepted_arming_entries() -> tuple[MarkerAcceptedArmingEntry, ...]:
    """Build stable R21T-H marker accepted arming metadata entries."""
    boundary = {
        "source_r21t_g_marker_gate_bound": True,
        "final_operator_marker_present": True,
        "final_operator_marker_accepted": True,
        "operator_approved_private_preview_run": True,
        "arming_ready": True,
        "runtime_armed": False,
        "script_execution_allowed_for_next": True,
        "script_execution_allowed_in_this_batch": False,
        "runtime_execution_allowed_for_next": True,
        "runtime_execution_allowed_in_this_batch": False,
    }
    entries = (
        MarkerAcceptedArmingEntry(
            "r21t_g_marker_gate_bound",
            "R21T-H is bound to the R21T-G marker gate",
            "docs/PRODUCT/R21T_G_FINAL_OPERATOR_MARKER_GATE_NO_RUN.md",
            "SOURCE_R21T_G_MARKER_GATE_BOUND",
            "bound",
            ordinal=10,
            **boundary,
        ),
        MarkerAcceptedArmingEntry(
            "final_operator_marker_exact",
            "The required final operator marker remains exact",
            REQUIRED_FINAL_OPERATOR_MARKER,
            "REQUIRED_FINAL_OPERATOR_MARKER",
            REQUIRED_FINAL_OPERATOR_MARKER,
            ordinal=20,
            **boundary,
        ),
        MarkerAcceptedArmingEntry(
            "final_operator_marker_present",
            "The required final operator marker is present",
            REQUIRED_FINAL_OPERATOR_MARKER,
            "FINAL_OPERATOR_MARKER_PRESENT",
            "true",
            ordinal=30,
            **boundary,
        ),
        MarkerAcceptedArmingEntry(
            "final_operator_marker_accepted",
            "The required final operator marker is accepted",
            REQUIRED_FINAL_OPERATOR_MARKER,
            "FINAL_OPERATOR_MARKER_ACCEPTED",
            "true",
            ordinal=40,
            **boundary,
        ),
        MarkerAcceptedArmingEntry(
            "operator_approval_true",
            "Operator approval for the private preview run is true",
            REQUIRED_FINAL_OPERATOR_MARKER,
            "OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN",
            "true",
            ordinal=50,
            **boundary,
        ),
        MarkerAcceptedArmingEntry(
            "arming_ready_next_batch",
            "Arming readiness is true for the next batch",
            MARKER_ACCEPTED_ARMING_ID,
            "ARMING_READY",
            "true",
            ordinal=60,
            **boundary,
        ),
        MarkerAcceptedArmingEntry(
            "runtime_not_armed_this_batch",
            "Runtime remains not armed in this batch",
            MARKER_ACCEPTED_ARMING_ID,
            "RUNTIME_ARMED",
            "false",
            ordinal=70,
            **boundary,
        ),
        MarkerAcceptedArmingEntry(
            "script_permission_next_only",
            "Script execution permission is true only for the next batch",
            MARKER_ACCEPTED_ARMING_ID,
            "SCRIPT_EXECUTION_ALLOWED_FOR_NEXT",
            "true",
            ordinal=80,
            **boundary,
        ),
        MarkerAcceptedArmingEntry(
            "runtime_permission_next_only",
            "Runtime execution permission is true only for the next batch",
            MARKER_ACCEPTED_ARMING_ID,
            "RUNTIME_EXECUTION_ALLOWED_FOR_NEXT",
            "true",
            ordinal=90,
            **boundary,
        ),
        MarkerAcceptedArmingEntry(
            "this_batch_execution_closed",
            "This batch remains closed for script and runtime execution",
            MARKER_ACCEPTED_ARMING_ID,
            "SCRIPT_EXECUTION_ALLOWED_IN_THIS_BATCH",
            "false",
            ordinal=100,
            **boundary,
        ),
        MarkerAcceptedArmingEntry(
            "readiness_requires_http",
            "Preview readiness still requires non-empty HTTP frontend evidence",
            "docs/RUNTIME/REFLEX_CLI_CONTRACT_H8I.md",
            "HTTP_FRONTEND_NON_EMPTY_REQUIRED",
            "required",
            ordinal=110,
            **boundary,
        ),
        MarkerAcceptedArmingEntry(
            "safety_locks_closed",
            "Provider, trading, Sheet/BQ, release, and HTML paths remain closed",
            "docs/PROCESS/ASSISTANT_REFLEX_INSTRUCTION_LOCK_R16F2H4.md",
            "NO_PROVIDER_CALL",
            "closed",
            ordinal=120,
            **boundary,
        ),
    )
    return tuple(sorted(entries, key=lambda entry: entry.ordinal))


def build_marker_accepted_arming() -> MarkerAcceptedArming:
    """Build the R21T-H marker accepted arming payload."""
    return MarkerAcceptedArming(
        marker_accepted_arming_id=MARKER_ACCEPTED_ARMING_ID,
        status="R21T_H_MARKER_ACCEPTED_ARMING_NO_RUN=READY",
        source_bindings=dict(SOURCE_BINDINGS),
        marker_accepted_arming_tokens=dict(MARKER_ACCEPTED_ARMING_TOKENS),
        marker_accepted_arming_sections=MARKER_ACCEPTED_ARMING_SECTIONS,
        marker_accepted_arming_entries=_build_marker_accepted_arming_entries(),
        files_created=tuple(str(path) for path in R21T_H_FILES),
        next_step=NEXT_STEP,
    )


def marker_accepted_arming_to_dict(
    marker_accepted_arming: MarkerAcceptedArming | None = None,
) -> dict[str, Any]:
    """Return the R21T-H arming payload as a JSON-friendly dictionary."""
    if marker_accepted_arming is None:
        marker_accepted_arming = build_marker_accepted_arming()

    return {
        "marker_accepted_arming_id": marker_accepted_arming.marker_accepted_arming_id,
        "status": marker_accepted_arming.status,
        "R21T_H_MARKER_ACCEPTED_ARMING_NO_RUN": READY_STATUS,
        "source_bindings": dict(marker_accepted_arming.source_bindings),
        "marker_accepted_arming_tokens": dict(
            marker_accepted_arming.marker_accepted_arming_tokens
        ),
        "marker_accepted_arming_sections": list(
            marker_accepted_arming.marker_accepted_arming_sections
        ),
        "marker_accepted_arming_entries": [
            asdict(entry)
            for entry in marker_accepted_arming.marker_accepted_arming_entries
        ],
        "files_created": list(marker_accepted_arming.files_created),
        "next_step": marker_accepted_arming.next_step,
    }


def build_marker_accepted_arming_with_sources() -> dict[str, Any]:
    """Build the R21T-H payload with bound R21T-G source summary."""
    r21t_g = build_final_operator_marker_gate_with_sources()
    marker_accepted_arming = marker_accepted_arming_to_dict()

    return {
        **marker_accepted_arming,
        "source_summaries": {
            "r21t_g_marker_gate": r21t_g["marker_gate_id"],
            "r21t_g_status": r21t_g["R21T_G_FINAL_OPERATOR_MARKER_GATE_NO_RUN"],
            "r21t_g_required_final_operator_marker": r21t_g["marker_gate_tokens"][
                "REQUIRED_FINAL_OPERATOR_MARKER"
            ],
            "r21t_g_final_operator_marker_present_before_acceptance": r21t_g[
                "marker_gate_tokens"
            ]["FINAL_OPERATOR_MARKER_PRESENT"],
            "r21t_g_final_operator_marker_accepted_before_acceptance": r21t_g[
                "marker_gate_tokens"
            ]["FINAL_OPERATOR_MARKER_ACCEPTED"],
            "r21t_g_operator_approved_before_acceptance": r21t_g[
                "marker_gate_tokens"
            ]["OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN"],
            "r21t_g_arming_ready_before_acceptance": r21t_g["marker_gate_tokens"][
                "ARMING_READY"
            ],
            "r21t_g_runtime_armed": r21t_g["marker_gate_tokens"]["RUNTIME_ARMED"],
            "r21t_g_reflex_version": r21t_g["marker_gate_tokens"]["REFLEX_VERSION"],
            "r21t_g_next_step": r21t_g["next_step"],
        },
    }


def validate_marker_accepted_arming(
    payload: dict[str, Any] | None = None,
) -> tuple[str, ...]:
    """Return validation errors. Empty tuple means the R21T-H payload is valid."""
    if payload is None:
        payload = build_marker_accepted_arming_with_sources()

    errors: list[str] = []
    if payload.get("marker_accepted_arming_id") != MARKER_ACCEPTED_ARMING_ID:
        errors.append("marker_accepted_arming_id_mismatch")
    if payload.get("R21T_H_MARKER_ACCEPTED_ARMING_NO_RUN") != READY_STATUS:
        errors.append("marker_accepted_arming_not_ready")

    bindings = payload.get("source_bindings")
    if not isinstance(bindings, dict):
        errors.append("missing_source_bindings")
    else:
        for key, expected in SOURCE_BINDINGS.items():
            if bindings.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    tokens = payload.get("marker_accepted_arming_tokens")
    if not isinstance(tokens, dict):
        errors.append("missing_marker_accepted_arming_tokens")
    else:
        for key, expected in MARKER_ACCEPTED_ARMING_TOKENS.items():
            if tokens.get(key) != expected:
                errors.append(f"{key}_mismatch")
        if tokens.get("FINAL_OPERATOR_MARKER_PRESENT") is not True:
            errors.append("final_operator_marker_not_present")
        if tokens.get("FINAL_OPERATOR_MARKER_ACCEPTED") is not True:
            errors.append("final_operator_marker_not_accepted")
        if tokens.get("OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN") is not True:
            errors.append("operator_approval_not_true")
        if tokens.get("SCRIPT_EXECUTION_ALLOWED_FOR_NEXT") is not True:
            errors.append("script_next_not_open")
        if tokens.get("SCRIPT_EXECUTION_ALLOWED_IN_THIS_BATCH") is not False:
            errors.append("script_this_batch_open")
        if tokens.get("RUNTIME_EXECUTION_ALLOWED_FOR_NEXT") is not True:
            errors.append("runtime_next_not_open")
        if tokens.get("RUNTIME_EXECUTION_ALLOWED_IN_THIS_BATCH") is not False:
            errors.append("runtime_this_batch_open")

    if tuple(payload.get("marker_accepted_arming_sections", ())) != (
        MARKER_ACCEPTED_ARMING_SECTIONS
    ):
        errors.append("marker_accepted_arming_sections_mismatch")
    if tuple(payload.get("files_created", ())) != tuple(str(path) for path in R21T_H_FILES):
        errors.append("files_created_mismatch")

    entries = payload.get("marker_accepted_arming_entries")
    if not isinstance(entries, list):
        errors.append("missing_marker_accepted_arming_entries")
    else:
        entry_ids = {
            entry.get("arming_entry_id") for entry in entries if isinstance(entry, dict)
        }
        if set(REQUIRED_ARMING_ENTRY_IDS) - entry_ids:
            errors.append("missing_marker_accepted_arming_entries")
        ordinals = [entry.get("ordinal") for entry in entries if isinstance(entry, dict)]
        if ordinals != sorted(ordinals):
            errors.append("marker_accepted_arming_entries_not_deterministic")
        for entry in entries:
            if not isinstance(entry, dict):
                errors.append("invalid_marker_accepted_arming_entry")
                continue
            entry_id = entry.get("arming_entry_id")
            if entry.get("source_r21t_g_marker_gate_bound") is not True:
                errors.append(f"source_r21t_g_missing={entry_id}")
            if entry.get("final_operator_marker_present") is not True:
                errors.append(f"final_operator_marker_not_present={entry_id}")
            if entry.get("final_operator_marker_accepted") is not True:
                errors.append(f"final_operator_marker_not_accepted={entry_id}")
            if entry.get("operator_approved_private_preview_run") is not True:
                errors.append(f"operator_approval_not_true={entry_id}")
            if entry.get("arming_ready") is not True:
                errors.append(f"arming_not_ready={entry_id}")
            if entry.get("runtime_armed") is not False:
                errors.append(f"runtime_armed_open={entry_id}")
            if entry.get("script_execution_allowed_for_next") is not True:
                errors.append(f"script_next_not_open={entry_id}")
            if entry.get("script_execution_allowed_in_this_batch") is not False:
                errors.append(f"script_this_batch_open={entry_id}")
            if entry.get("runtime_execution_allowed_for_next") is not True:
                errors.append(f"runtime_next_not_open={entry_id}")
            if entry.get("runtime_execution_allowed_in_this_batch") is not False:
                errors.append(f"runtime_this_batch_open={entry_id}")

    summaries = payload.get("source_summaries")
    if isinstance(summaries, dict):
        if summaries.get("r21t_g_marker_gate") != R21T_G_MARKER_GATE_ID:
            errors.append("r21t_g_source_mismatch")
        if summaries.get("r21t_g_status") != READY_STATUS:
            errors.append("r21t_g_status_mismatch")
        if (
            summaries.get("r21t_g_required_final_operator_marker")
            != REQUIRED_FINAL_OPERATOR_MARKER
        ):
            errors.append("r21t_g_marker_mismatch")
        if summaries.get("r21t_g_reflex_version") != REFLEX_VERSION:
            errors.append("r21t_g_version_mismatch")

    if payload.get("next_step") != NEXT_STEP:
        errors.append("next_step_mismatch")

    return tuple(errors)


def render_marker_accepted_arming_markdown(
    payload: dict[str, Any] | None = None,
) -> str:
    """Render the R21T-H marker accepted arming as markdown text only."""
    if payload is None:
        payload = build_marker_accepted_arming_with_sources()

    lines = [
        "# R21T-H Marker Accepted Arming - No Run",
        "",
        f"Status: `{payload['status']}`",
        "",
        "R21T-H records deterministic marker acceptance and next-batch arming",
        "metadata only. This batch remains closed for execution.",
        "",
        "## Source Bindings",
    ]
    for key in sorted(payload["source_bindings"]):
        lines.append(f"- `{key}` = `{payload['source_bindings'][key]}`")

    lines.extend(["", "## Marker Accepted Arming Tokens"])
    for key in sorted(payload["marker_accepted_arming_tokens"]):
        value = payload["marker_accepted_arming_tokens"][key]
        lines.append(f"- `{key}` = `{value}`")

    lines.extend(["", "## Marker Accepted Arming Sections"])
    for section in payload["marker_accepted_arming_sections"]:
        lines.append(f"- `{section}`")

    lines.extend(["", "## Files Created"])
    for path in payload["files_created"]:
        lines.append(f"- `{path}`")

    lines.extend(["", "## Marker Accepted Arming Entries"])
    for entry in payload["marker_accepted_arming_entries"]:
        lines.append(
            "- "
            f"`{entry['arming_entry_id']}` - {entry['title']} - "
            f"`{entry['required_token']}` - `{entry['required_state']}`"
        )

    lines.extend(
        [
            "",
            "## Arming Decision",
            "`SOURCE_R21T_G_MARKER_GATE_BOUND` is `True`.",
            "`FINAL_OPERATOR_MARKER_PRESENT` is `True`.",
            "`FINAL_OPERATOR_MARKER_ACCEPTED` is `True`.",
            "`OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN` is `True`.",
            "`ARMING_READY` is `True`.",
            "`RUNTIME_ARMED` is `False`.",
            "`SCRIPT_EXECUTION_ALLOWED_FOR_NEXT` is `True`.",
            "`SCRIPT_EXECUTION_ALLOWED_IN_THIS_BATCH` is `False`.",
            "`RUNTIME_EXECUTION_ALLOWED_FOR_NEXT` is `True`.",
            "`RUNTIME_EXECUTION_ALLOWED_IN_THIS_BATCH` is `False`.",
            f"`REQUIRED_FINAL_OPERATOR_MARKER` is `{REQUIRED_FINAL_OPERATOR_MARKER}`.",
            "`REFLEX_RUNTIME_STATUS` is `ARMED_BUT_NOT_STARTED`.",
            "",
            f"NEXT={payload['next_step']}",
        ]
    )
    return "\n".join(lines) + "\n"
