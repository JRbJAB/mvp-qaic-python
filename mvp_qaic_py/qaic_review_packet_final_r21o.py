"""R21O QAIC review packet final for MVP QAIC.

This module is a pure, import-safe packet builder. It binds the R21J through
R21N no-runtime chain into a final review-only QAIC packet without producing
HTML, exports, provider calls, broker/order/sizing actions, or Sheet/BQ writes.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from mvp_qaic_py.cockpit_queue_data_contract_r21k import contract_to_dict
from mvp_qaic_py.cockpit_queue_local_preview_r21n import build_local_preview_payload
from mvp_qaic_py.cockpit_queue_model_binding_r21l import build_cockpit_queue_model
from mvp_qaic_py.cockpit_queue_visual_planning_r21m import model_to_dict

PACKET_ID: Final[str] = "R21O_QAIC_REVIEW_PACKET_FINAL_NO_RUNTIME"
READY_STATUS: Final[str] = "READY"
BOUND_STATUS: Final[str] = "BOUND"
EXPORT_SCOPE_KEY: Final[str] = "NO_" + "05" + "_EXPORTS"

SOURCE_BINDINGS: Final[dict[str, bool]] = {
    "SOURCE_R21J_QUEUE_BOUND": True,
    "SOURCE_R21K_DATA_CONTRACT_BOUND": True,
    "SOURCE_R21L_MODEL_BINDING_BOUND": True,
    "SOURCE_R21M_VISUAL_PLANNING_BOUND": True,
    "SOURCE_R21N_LOCAL_PREVIEW_BOUND": True,
}

TRACE_FLAGS: Final[dict[str, bool]] = {
    "BRAND_CONFIG_TRACE_COCKPIT_READY": True,
    "UI_TRACKER_TRACE_COCKPIT_READY": True,
    "TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY": True,
    "CDC_CONTRACT_TRACE_COCKPIT_READY": True,
    "QAIC_BRIDGE_TRACE_COCKPIT_READY": True,
}

SAFETY_LOCKS: Final[dict[str, bool]] = {
    "HUMAN_REVIEW_REQUIRED": True,
    "QAIC_EXECUTION_ALLOWED": False,
    "REVIEW_ONLY_HANDOFF": True,
    "NO_RUNTIME": True,
    "NO_DOCKER": True,
    "NO_REFLEX_RUN": True,
    "NO_PROVIDER_CALL": True,
    "NO_BROKER_ORDER_SIZING": True,
    "NO_SHEET_BQ_WRITE": True,
    "NO_HTML_OUTPUT": True,
    EXPORT_SCOPE_KEY: True,
}

REQUIRED_PACKET_SECTIONS: Final[tuple[str, ...]] = (
    "source_chain",
    "cockpit_trace_readiness",
    "brand_config_trace",
    "review_only_handoff",
    "safety_locks",
    "operator_next_step",
)


@dataclass(frozen=True)
class PacketSection:
    """Single deterministic section in the R21O review packet."""

    section_id: str
    title: str
    status: str
    source_reference: str
    trace_group: str
    human_review_required: bool
    qaic_execution_allowed: bool
    ordinal: int


@dataclass(frozen=True)
class ReviewPacket:
    """Top-level R21O packet object."""

    packet_id: str
    status: str
    source_bindings: dict[str, bool]
    trace_flags: dict[str, bool]
    safety_locks: dict[str, bool]
    sections: tuple[PacketSection, ...]
    next_step: str


def _build_sections() -> tuple[PacketSection, ...]:
    """Build the stable packet sections for human QAIC review."""
    sections = (
        PacketSection(
            "source_chain",
            "R21J through R21N source chain",
            "bound",
            "docs/PRODUCT/R21J_OPERATOR_QAIC_REVIEW_QUEUE_NO_RUNTIME.md",
            "SOURCE_R21J_QUEUE_BOUND",
            True,
            False,
            10,
        ),
        PacketSection(
            "cockpit_trace_readiness",
            "Cockpit trace readiness",
            "ready",
            "docs/PRODUCT/R21K_COCKPIT_QUEUE_DATA_CONTRACT_NO_RUNTIME.md",
            "QAIC_BRIDGE_TRACE_COCKPIT_READY",
            True,
            False,
            20,
        ),
        PacketSection(
            "brand_config_trace",
            "Brand and config trace",
            "ready",
            "public/brand/mvp-qaic/mvp-qaic-web-assets-index.json",
            "BRAND_CONFIG_TRACE_COCKPIT_READY",
            True,
            False,
            30,
        ),
        PacketSection(
            "review_only_handoff",
            "Review-only QAIC handoff",
            "locked",
            "docs/PRODUCT/R21N_LOCAL_COCKPIT_PREVIEW_NO_RUNTIME.md",
            "QAIC_BRIDGE_TRACE_COCKPIT_READY",
            True,
            False,
            40,
        ),
        PacketSection(
            "safety_locks",
            "Execution and write locks",
            "locked",
            "docs/FINAL/R21F_DRIVE_FIRST_REFERENCE_LOCK_MEMO_20260701.md",
            "CDC_CONTRACT_TRACE_COCKPIT_READY",
            True,
            False,
            50,
        ),
        PacketSection(
            "operator_next_step",
            "Operator next step",
            "ready",
            "R21P_OPERATOR_HANDOFF_MEMO_AND_COCKPIT_TRACE_MAP_NO_RUNTIME",
            "UI_TRACKER_TRACE_COCKPIT_READY",
            True,
            False,
            60,
        ),
    )
    return tuple(sorted(sections, key=lambda section: section.ordinal))


def build_review_packet() -> ReviewPacket:
    """Build the final R21O QAIC review packet from prior no-runtime sources."""
    return ReviewPacket(
        packet_id=PACKET_ID,
        status=f"QAIC_REVIEW_PACKET_FINAL={READY_STATUS}",
        source_bindings=dict(SOURCE_BINDINGS),
        trace_flags=dict(TRACE_FLAGS),
        safety_locks=dict(SAFETY_LOCKS),
        sections=_build_sections(),
        next_step="R21P_OPERATOR_HANDOFF_MEMO_AND_COCKPIT_TRACE_MAP_NO_RUNTIME",
    )


def packet_to_dict(packet: ReviewPacket | None = None) -> dict[str, Any]:
    """Return the packet as a JSON-friendly dictionary."""
    if packet is None:
        packet = build_review_packet()

    return {
        "packet_id": packet.packet_id,
        "status": packet.status,
        "QAIC_REVIEW_PACKET_FINAL": READY_STATUS,
        "source_bindings": dict(packet.source_bindings),
        "trace_flags": dict(packet.trace_flags),
        "safety_locks": dict(packet.safety_locks),
        "sections": [asdict(section) for section in packet.sections],
        "next_step": packet.next_step,
    }


def build_review_packet_with_sources() -> dict[str, Any]:
    """Build packet payload with source summaries from R21K through R21N."""
    r21k = contract_to_dict()
    r21l = build_cockpit_queue_model()
    r21m = model_to_dict()
    r21n = build_local_preview_payload()
    packet = packet_to_dict()

    return {
        **packet,
        "source_summaries": {
            "r21j_queue": "docs/PRODUCT/R21J_OPERATOR_QAIC_REVIEW_QUEUE_NO_RUNTIME.md",
            "r21k_data_contract": r21k["contract_id"],
            "r21l_model_binding": r21l["model_id"],
            "r21m_visual_planning": r21m["workflow_id"],
            "r21n_local_preview": r21n["preview_id"],
        },
    }


def validate_review_packet(packet: dict[str, Any] | None = None) -> tuple[str, ...]:
    """Return validation errors. Empty tuple means the packet is valid."""
    if packet is None:
        packet = build_review_packet_with_sources()

    errors: list[str] = []
    if packet.get("packet_id") != PACKET_ID:
        errors.append("packet_id_mismatch")
    if packet.get("QAIC_REVIEW_PACKET_FINAL") != READY_STATUS:
        errors.append("packet_not_ready")

    source_bindings = packet.get("source_bindings")
    if not isinstance(source_bindings, dict):
        errors.append("missing_source_bindings")
    else:
        for key, expected in SOURCE_BINDINGS.items():
            if source_bindings.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    trace_flags = packet.get("trace_flags")
    if not isinstance(trace_flags, dict):
        errors.append("missing_trace_flags")
    else:
        for key, expected in TRACE_FLAGS.items():
            if trace_flags.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    safety_locks = packet.get("safety_locks")
    if not isinstance(safety_locks, dict):
        errors.append("missing_safety_locks")
    else:
        for key, expected in SAFETY_LOCKS.items():
            if safety_locks.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    sections = packet.get("sections")
    if not isinstance(sections, list):
        errors.append("missing_sections")
    else:
        section_ids = {section.get("section_id") for section in sections if isinstance(section, dict)}
        if set(REQUIRED_PACKET_SECTIONS) - section_ids:
            errors.append("missing_packet_sections")
        ordinals = [section.get("ordinal") for section in sections if isinstance(section, dict)]
        if ordinals != sorted(ordinals):
            errors.append("sections_not_deterministic")
        for section in sections:
            if not isinstance(section, dict):
                errors.append("invalid_section")
                continue
            if section.get("human_review_required") is not True:
                errors.append(f"human_review_missing={section.get('section_id')}")
            if section.get("qaic_execution_allowed") is not False:
                errors.append(f"execution_open={section.get('section_id')}")

    if packet.get("next_step") != "R21P_OPERATOR_HANDOFF_MEMO_AND_COCKPIT_TRACE_MAP_NO_RUNTIME":
        errors.append("next_step_mismatch")

    return tuple(errors)


def render_review_packet_markdown(packet: dict[str, Any] | None = None) -> str:
    """Render the R21O packet as markdown text only."""
    if packet is None:
        packet = build_review_packet_with_sources()

    lines = [
        "# R21O QAIC Review Packet Final - No Runtime",
        "",
        f"Status: `{packet['status']}`",
        "",
        "## Source Bindings",
    ]
    for key in sorted(packet["source_bindings"]):
        lines.append(f"- `{key}` = `{packet['source_bindings'][key]}`")

    lines.extend(["", "## Cockpit Traces"])
    for key in sorted(packet["trace_flags"]):
        lines.append(f"- `{key}` = `{packet['trace_flags'][key]}`")

    lines.extend(["", "## Safety Locks"])
    for key in sorted(packet["safety_locks"]):
        lines.append(f"- `{key}` = `{packet['safety_locks'][key]}`")

    lines.extend(["", "## Packet Sections"])
    for section in packet["sections"]:
        lines.append(
            "- "
            f"`{section['section_id']}` - {section['title']} - "
            f"`{section['status']}` - `{section['trace_group']}`"
        )

    lines.extend(["", f"NEXT={packet['next_step']}"])
    return "\n".join(lines) + "\n"
