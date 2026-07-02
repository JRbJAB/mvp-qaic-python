"""R21T-G final operator marker gate metadata.

This module is deterministic metadata only. It binds to the R21T-F arming
review and records that the final operator marker is required, absent, and not
accepted. It exposes no runtime, script, Docker, preview, browser, provider,
trading, Sheet/BQ, release, or HTML output behavior.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Final

from mvp_qaic_py.reflex_private_preview_operator_script_arming_review_r21t_f import (
    ARMING_REVIEW_ID as R21T_F_ARMING_REVIEW_ID,
    REFLEX_VERSION,
    build_private_preview_operator_script_arming_review_with_sources,
)

MARKER_GATE_ID: Final[str] = "R21T_G_FINAL_OPERATOR_MARKER_GATE_NO_RUN"
READY_STATUS: Final[str] = "READY"
PAUSED_STATUS: Final[str] = "PAUSED"
STOPPED_AT_FINAL_OPERATOR_MARKER_GATE_NO_RUN: Final[str] = (
    "STOPPED_AT_FINAL_OPERATOR_MARKER_GATE_NO_RUN"
)
REQUIRED_FINAL_OPERATOR_MARKER: Final[str] = (
    "R21T_G_OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN_TRUE"
)
NEXT_STEP: Final[str] = "WAIT_FOR_R21T_G_OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN_TRUE"

DOC_PATH: Final[Path] = Path("docs/PRODUCT/R21T_G_FINAL_OPERATOR_MARKER_GATE_NO_RUN.md")
MODULE_PATH: Final[Path] = Path(
    "mvp_qaic_py/reflex_private_preview_final_operator_marker_gate_r21t_g.py"
)
TEST_PATH: Final[Path] = Path("tests/test_r21t_g_final_operator_marker_gate.py")
R21T_G_FILES: Final[tuple[Path, ...]] = (DOC_PATH, MODULE_PATH, TEST_PATH)

SOURCE_BINDINGS: Final[dict[str, bool]] = {
    "SOURCE_R21T_F_ARMING_REVIEW_BOUND": True,
}

MARKER_GATE_TOKENS: Final[dict[str, bool | str]] = {
    "R21T_G_FINAL_OPERATOR_MARKER_GATE_NO_RUN": READY_STATUS,
    "SOURCE_R21T_F_ARMING_REVIEW_BOUND": True,
    "MARKER_GATE_ONLY": True,
    "REQUIRED_FINAL_OPERATOR_MARKER": REQUIRED_FINAL_OPERATOR_MARKER,
    "FINAL_OPERATOR_MARKER_PRESENT": False,
    "FINAL_OPERATOR_MARKER_ACCEPTED": False,
    "OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN": False,
    "ARMING_REVIEW_PASSED": True,
    "ARMING_READY": False,
    "RUNTIME_ARMED": False,
    "SCRIPT_EXECUTION_ALLOWED": False,
    "RUNTIME_EXECUTION_ALLOWED": False,
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
    "REFLEX_RUNTIME_RUNNER_CHAIN": STOPPED_AT_FINAL_OPERATOR_MARKER_GATE_NO_RUN,
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

MARKER_GATE_SECTIONS: Final[tuple[str, ...]] = (
    "R21T_F_ARMING_REVIEW_BINDING",
    "FINAL_OPERATOR_MARKER_REQUIRED_EXACT",
    "FINAL_OPERATOR_MARKER_ABSENT",
    "FINAL_OPERATOR_MARKER_NOT_ACCEPTED",
    "OPERATOR_APPROVAL_FALSE",
    "ARMING_REVIEW_PASSED_BUT_ARMING_NOT_READY",
    "RUNTIME_AND_SCRIPT_EXECUTION_CLOSED",
    "READINESS_REQUIRES_HTTP_FRONTEND",
    "RUNNER_HARDENING_REQUIREMENTS_PRESERVED",
    "SAFETY_LOCKS_CLOSED",
    "WAIT_FOR_OPERATOR_MARKER",
)

REQUIRED_MARKER_ENTRY_IDS: Final[tuple[str, ...]] = (
    "r21t_f_arming_review_bound",
    "marker_gate_only",
    "final_operator_marker_required_exact",
    "final_operator_marker_absent",
    "final_operator_marker_not_accepted",
    "operator_approval_false",
    "arming_review_passed",
    "arming_not_ready",
    "runtime_not_armed",
    "script_and_runtime_execution_closed",
    "readiness_requires_http",
    "safety_locks_closed",
)


@dataclass(frozen=True)
class FinalOperatorMarkerGateEntry:
    """Single R21T-G marker gate metadata entry."""

    marker_entry_id: str
    title: str
    source_reference: str
    required_token: str
    required_state: str
    marker_gate_only: bool
    final_operator_marker_present: bool
    final_operator_marker_accepted: bool
    operator_approved_private_preview_run: bool
    runtime_armed: bool
    script_execution_allowed: bool
    runtime_execution_allowed: bool
    ordinal: int


@dataclass(frozen=True)
class FinalOperatorMarkerGate:
    """Top-level R21T-G marker gate object."""

    marker_gate_id: str
    status: str
    source_bindings: dict[str, bool]
    marker_gate_tokens: dict[str, bool | str]
    marker_gate_sections: tuple[str, ...]
    marker_gate_entries: tuple[FinalOperatorMarkerGateEntry, ...]
    files_created: tuple[str, ...]
    next_step: str


def _build_marker_gate_entries() -> tuple[FinalOperatorMarkerGateEntry, ...]:
    """Build stable R21T-G marker gate metadata entries."""
    closed = {
        "marker_gate_only": True,
        "final_operator_marker_present": False,
        "final_operator_marker_accepted": False,
        "operator_approved_private_preview_run": False,
        "runtime_armed": False,
        "script_execution_allowed": False,
        "runtime_execution_allowed": False,
    }
    entries = (
        FinalOperatorMarkerGateEntry(
            "r21t_f_arming_review_bound",
            "R21T-G is bound to the R21T-F arming review",
            "docs/PRODUCT/R21T_F_PRIVATE_PREVIEW_OPERATOR_SCRIPT_REVIEW_AND_ARMING_NO_RUN.md",
            "SOURCE_R21T_F_ARMING_REVIEW_BOUND",
            "bound",
            ordinal=10,
            **closed,
        ),
        FinalOperatorMarkerGateEntry(
            "marker_gate_only",
            "R21T-G is marker gate metadata only",
            MARKER_GATE_ID,
            "MARKER_GATE_ONLY",
            "true",
            ordinal=20,
            **closed,
        ),
        FinalOperatorMarkerGateEntry(
            "final_operator_marker_required_exact",
            "The required final operator marker is exact",
            REQUIRED_FINAL_OPERATOR_MARKER,
            "REQUIRED_FINAL_OPERATOR_MARKER",
            REQUIRED_FINAL_OPERATOR_MARKER,
            ordinal=30,
            **closed,
        ),
        FinalOperatorMarkerGateEntry(
            "final_operator_marker_absent",
            "The required final operator marker is absent",
            REQUIRED_FINAL_OPERATOR_MARKER,
            "FINAL_OPERATOR_MARKER_PRESENT",
            "false",
            ordinal=40,
            **closed,
        ),
        FinalOperatorMarkerGateEntry(
            "final_operator_marker_not_accepted",
            "The required final operator marker is not accepted",
            REQUIRED_FINAL_OPERATOR_MARKER,
            "FINAL_OPERATOR_MARKER_ACCEPTED",
            "false",
            ordinal=50,
            **closed,
        ),
        FinalOperatorMarkerGateEntry(
            "operator_approval_false",
            "Operator approval for the private preview run remains false",
            REQUIRED_FINAL_OPERATOR_MARKER,
            "OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN",
            "false",
            ordinal=60,
            **closed,
        ),
        FinalOperatorMarkerGateEntry(
            "arming_review_passed",
            "R21T-F arming review passed as a metadata review",
            R21T_F_ARMING_REVIEW_ID,
            "ARMING_REVIEW_PASSED",
            "true",
            ordinal=70,
            **closed,
        ),
        FinalOperatorMarkerGateEntry(
            "arming_not_ready",
            "Arming remains not ready at the marker gate",
            MARKER_GATE_ID,
            "ARMING_READY",
            "false",
            ordinal=80,
            **closed,
        ),
        FinalOperatorMarkerGateEntry(
            "runtime_not_armed",
            "Runtime remains unarmed and paused",
            "docs/FINAL/R21B_REFLEX_RUNTIME_CLOSURE_STRATEGY_AND_INSTRUCTIONS_MEMO_20260701.md",
            "RUNTIME_ARMED",
            "false",
            ordinal=90,
            **closed,
        ),
        FinalOperatorMarkerGateEntry(
            "script_and_runtime_execution_closed",
            "Script and runtime execution remain closed",
            MARKER_GATE_ID,
            "SCRIPT_EXECUTION_ALLOWED",
            "false",
            ordinal=100,
            **closed,
        ),
        FinalOperatorMarkerGateEntry(
            "readiness_requires_http",
            "Preview readiness still requires non-empty HTTP frontend evidence",
            "docs/RUNTIME/REFLEX_CLI_CONTRACT_H8I.md",
            "HTTP_FRONTEND_NON_EMPTY_REQUIRED",
            "required",
            ordinal=110,
            **closed,
        ),
        FinalOperatorMarkerGateEntry(
            "safety_locks_closed",
            "Provider, trading, Sheet/BQ, release, and HTML paths remain closed",
            "docs/PROCESS/ASSISTANT_REFLEX_INSTRUCTION_LOCK_R16F2H4.md",
            "NO_PROVIDER_CALL",
            "closed",
            ordinal=120,
            **closed,
        ),
    )
    return tuple(sorted(entries, key=lambda entry: entry.ordinal))


def build_final_operator_marker_gate() -> FinalOperatorMarkerGate:
    """Build the R21T-G final operator marker gate payload."""
    return FinalOperatorMarkerGate(
        marker_gate_id=MARKER_GATE_ID,
        status="R21T_G_FINAL_OPERATOR_MARKER_GATE_NO_RUN=READY",
        source_bindings=dict(SOURCE_BINDINGS),
        marker_gate_tokens=dict(MARKER_GATE_TOKENS),
        marker_gate_sections=MARKER_GATE_SECTIONS,
        marker_gate_entries=_build_marker_gate_entries(),
        files_created=tuple(str(path) for path in R21T_G_FILES),
        next_step=NEXT_STEP,
    )


def final_operator_marker_gate_to_dict(
    marker_gate: FinalOperatorMarkerGate | None = None,
) -> dict[str, Any]:
    """Return the R21T-G marker gate payload as a JSON-friendly dictionary."""
    if marker_gate is None:
        marker_gate = build_final_operator_marker_gate()

    return {
        "marker_gate_id": marker_gate.marker_gate_id,
        "status": marker_gate.status,
        "R21T_G_FINAL_OPERATOR_MARKER_GATE_NO_RUN": READY_STATUS,
        "source_bindings": dict(marker_gate.source_bindings),
        "marker_gate_tokens": dict(marker_gate.marker_gate_tokens),
        "marker_gate_sections": list(marker_gate.marker_gate_sections),
        "marker_gate_entries": [
            asdict(entry) for entry in marker_gate.marker_gate_entries
        ],
        "files_created": list(marker_gate.files_created),
        "next_step": marker_gate.next_step,
    }


def build_final_operator_marker_gate_with_sources() -> dict[str, Any]:
    """Build the R21T-G payload with bound R21T-F source summary."""
    r21t_f = build_private_preview_operator_script_arming_review_with_sources()
    marker_gate = final_operator_marker_gate_to_dict()

    return {
        **marker_gate,
        "source_summaries": {
            "r21t_f_arming_review": r21t_f["arming_review_id"],
            "r21t_f_status": r21t_f[
                "R21T_F_PRIVATE_PREVIEW_OPERATOR_SCRIPT_REVIEW_AND_ARMING_NO_RUN"
            ],
            "r21t_f_final_operator_marker": r21t_f["arming_review_tokens"][
                "REQUIRED_FINAL_OPERATOR_MARKER"
            ],
            "r21t_f_final_operator_marker_present": r21t_f["arming_review_tokens"][
                "FINAL_OPERATOR_MARKER_PRESENT"
            ],
            "r21t_f_arming_ready": r21t_f["arming_review_tokens"]["ARMING_READY"],
            "r21t_f_runtime_armed": r21t_f["arming_review_tokens"][
                "RUNTIME_ARMED"
            ],
            "r21t_f_script_execution_allowed": r21t_f["arming_review_tokens"][
                "SCRIPT_EXECUTION_ALLOWED"
            ],
            "r21t_f_runtime_execution_allowed": r21t_f["arming_review_tokens"][
                "RUNTIME_EXECUTION_ALLOWED"
            ],
            "r21t_f_reflex_version": r21t_f["arming_review_tokens"][
                "REFLEX_VERSION"
            ],
            "r21t_f_next_step": r21t_f["next_step"],
        },
    }


def validate_final_operator_marker_gate(
    payload: dict[str, Any] | None = None,
) -> tuple[str, ...]:
    """Return validation errors. Empty tuple means the R21T-G payload is valid."""
    if payload is None:
        payload = build_final_operator_marker_gate_with_sources()

    errors: list[str] = []
    if payload.get("marker_gate_id") != MARKER_GATE_ID:
        errors.append("marker_gate_id_mismatch")
    if payload.get("R21T_G_FINAL_OPERATOR_MARKER_GATE_NO_RUN") != READY_STATUS:
        errors.append("marker_gate_not_ready")

    bindings = payload.get("source_bindings")
    if not isinstance(bindings, dict):
        errors.append("missing_source_bindings")
    else:
        for key, expected in SOURCE_BINDINGS.items():
            if bindings.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    tokens = payload.get("marker_gate_tokens")
    if not isinstance(tokens, dict):
        errors.append("missing_marker_gate_tokens")
    else:
        for key, expected in MARKER_GATE_TOKENS.items():
            if tokens.get(key) != expected:
                errors.append(f"{key}_mismatch")
        if tokens.get("FINAL_OPERATOR_MARKER_PRESENT") is not False:
            errors.append("final_operator_marker_present")
        if tokens.get("FINAL_OPERATOR_MARKER_ACCEPTED") is not False:
            errors.append("final_operator_marker_accepted")
        if tokens.get("OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN") is not False:
            errors.append("operator_approved_private_preview_run")

    if tuple(payload.get("marker_gate_sections", ())) != MARKER_GATE_SECTIONS:
        errors.append("marker_gate_sections_mismatch")
    if tuple(payload.get("files_created", ())) != tuple(str(path) for path in R21T_G_FILES):
        errors.append("files_created_mismatch")

    entries = payload.get("marker_gate_entries")
    if not isinstance(entries, list):
        errors.append("missing_marker_gate_entries")
    else:
        entry_ids = {
            entry.get("marker_entry_id") for entry in entries if isinstance(entry, dict)
        }
        if set(REQUIRED_MARKER_ENTRY_IDS) - entry_ids:
            errors.append("missing_marker_gate_entries")
        ordinals = [entry.get("ordinal") for entry in entries if isinstance(entry, dict)]
        if ordinals != sorted(ordinals):
            errors.append("marker_gate_entries_not_deterministic")
        for entry in entries:
            if not isinstance(entry, dict):
                errors.append("invalid_marker_gate_entry")
                continue
            entry_id = entry.get("marker_entry_id")
            if entry.get("marker_gate_only") is not True:
                errors.append(f"marker_gate_only_missing={entry_id}")
            if entry.get("final_operator_marker_present") is not False:
                errors.append(f"final_operator_marker_present={entry_id}")
            if entry.get("final_operator_marker_accepted") is not False:
                errors.append(f"final_operator_marker_accepted={entry_id}")
            if entry.get("operator_approved_private_preview_run") is not False:
                errors.append(f"operator_approval_open={entry_id}")
            if entry.get("runtime_armed") is not False:
                errors.append(f"runtime_armed_open={entry_id}")
            if entry.get("script_execution_allowed") is not False:
                errors.append(f"script_execution_open={entry_id}")
            if entry.get("runtime_execution_allowed") is not False:
                errors.append(f"runtime_execution_open={entry_id}")

    summaries = payload.get("source_summaries")
    if isinstance(summaries, dict):
        if summaries.get("r21t_f_arming_review") != R21T_F_ARMING_REVIEW_ID:
            errors.append("r21t_f_source_mismatch")
        if summaries.get("r21t_f_status") != READY_STATUS:
            errors.append("r21t_f_status_mismatch")
        if summaries.get("r21t_f_final_operator_marker") != REQUIRED_FINAL_OPERATOR_MARKER:
            errors.append("r21t_f_marker_mismatch")
        if summaries.get("r21t_f_final_operator_marker_present") is not False:
            errors.append("r21t_f_marker_present")
        if summaries.get("r21t_f_arming_ready") is not False:
            errors.append("r21t_f_arming_ready")
        if summaries.get("r21t_f_runtime_armed") is not False:
            errors.append("r21t_f_runtime_armed")
        if summaries.get("r21t_f_script_execution_allowed") is not False:
            errors.append("r21t_f_script_execution_open")
        if summaries.get("r21t_f_runtime_execution_allowed") is not False:
            errors.append("r21t_f_runtime_execution_open")
        if summaries.get("r21t_f_reflex_version") != REFLEX_VERSION:
            errors.append("r21t_f_version_mismatch")
        if summaries.get("r21t_f_next_step") != MARKER_GATE_ID:
            errors.append("r21t_f_next_step_mismatch")

    if payload.get("next_step") != NEXT_STEP:
        errors.append("next_step_mismatch")

    return tuple(errors)


def render_final_operator_marker_gate_markdown(
    payload: dict[str, Any] | None = None,
) -> str:
    """Render the R21T-G marker gate as markdown text only."""
    if payload is None:
        payload = build_final_operator_marker_gate_with_sources()

    lines = [
        "# R21T-G Final Operator Marker Gate - No Run",
        "",
        f"Status: `{payload['status']}`",
        "",
        "R21T-G records deterministic marker-gate metadata only. The required",
        "operator marker is exact, absent, and not accepted.",
        "",
        "## Source Bindings",
    ]
    for key in sorted(payload["source_bindings"]):
        lines.append(f"- `{key}` = `{payload['source_bindings'][key]}`")

    lines.extend(["", "## Marker Gate Tokens"])
    for key in sorted(payload["marker_gate_tokens"]):
        lines.append(f"- `{key}` = `{payload['marker_gate_tokens'][key]}`")

    lines.extend(["", "## Marker Gate Sections"])
    for section in payload["marker_gate_sections"]:
        lines.append(f"- `{section}`")

    lines.extend(["", "## Files Created"])
    for path in payload["files_created"]:
        lines.append(f"- `{path}`")

    lines.extend(["", "## Marker Gate Entries"])
    for entry in payload["marker_gate_entries"]:
        lines.append(
            "- "
            f"`{entry['marker_entry_id']}` - {entry['title']} - "
            f"`{entry['required_token']}` - `{entry['required_state']}`"
        )

    lines.extend(
        [
            "",
            "## Marker Gate Decision",
            "`MARKER_GATE_ONLY` is `True`.",
            "`FINAL_OPERATOR_MARKER_PRESENT` is `False`.",
            "`FINAL_OPERATOR_MARKER_ACCEPTED` is `False`.",
            "`OPERATOR_APPROVED_PRIVATE_PREVIEW_RUN` is `False`.",
            "`ARMING_READY` is `False`.",
            "`RUNTIME_ARMED` is `False`.",
            "`SCRIPT_EXECUTION_ALLOWED` is `False`.",
            "`RUNTIME_EXECUTION_ALLOWED` is `False`.",
            f"`REQUIRED_FINAL_OPERATOR_MARKER` is `{REQUIRED_FINAL_OPERATOR_MARKER}`.",
            "`REFLEX_RUNTIME_STATUS` remains `PAUSED`.",
            "",
            f"NEXT={payload['next_step']}",
        ]
    )
    return "\n".join(lines) + "\n"
