"""R21P operator handoff memo and cockpit trace map for MVP QAIC.

This module is a pure, import-safe payload builder. It binds the R21O final
review packet and R21N local preview payload into a deterministic operator
handoff trace map without starting runtime surfaces, producing HTML, calling
providers, touching broker/order/sizing paths, or writing Sheet/BQ targets.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from mvp_qaic_py.cockpit_queue_local_preview_r21n import build_local_preview_payload
from mvp_qaic_py.qaic_review_packet_final_r21o import build_review_packet_with_sources

HANDOFF_ID: Final[str] = "R21P_OPERATOR_HANDOFF_MEMO_AND_COCKPIT_TRACE_MAP_NO_RUNTIME"
READY_STATUS: Final[str] = "READY"

SOURCE_BINDINGS: Final[dict[str, bool]] = {
    "SOURCE_R21O_QAIC_REVIEW_PACKET_BOUND": True,
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
}

REQUIRED_TRACE_IDS: Final[tuple[str, ...]] = (
    "operator_handoff_memo",
    "r21o_review_packet",
    "r21n_local_preview",
    "brand_config_trace",
    "ui_tracker_trace",
    "tool_registry_cdc_trace",
    "cdc_contract_trace",
    "qaic_bridge_trace",
    "safety_lock_trace",
    "r21q_next_step",
)


@dataclass(frozen=True)
class CockpitTraceMapEntry:
    """Single deterministic R21P trace map entry."""

    trace_id: str
    title: str
    source_reference: str
    cockpit_token: str
    status: str
    human_review_required: bool
    qaic_execution_allowed: bool
    ordinal: int


@dataclass(frozen=True)
class OperatorHandoffTraceMap:
    """Top-level R21P handoff object."""

    handoff_id: str
    status: str
    source_bindings: dict[str, bool]
    trace_flags: dict[str, bool]
    safety_locks: dict[str, bool]
    traces: tuple[CockpitTraceMapEntry, ...]
    next_step: str


def _build_trace_entries() -> tuple[CockpitTraceMapEntry, ...]:
    """Build stable operator handoff trace map entries."""
    entries = (
        CockpitTraceMapEntry(
            "operator_handoff_memo",
            "Operator handoff memo",
            "docs/PRODUCT/R21P_OPERATOR_HANDOFF_MEMO_AND_COCKPIT_TRACE_MAP_NO_RUNTIME.md",
            "OPERATOR_HANDOFF_MEMO",
            "ready",
            True,
            False,
            10,
        ),
        CockpitTraceMapEntry(
            "r21o_review_packet",
            "R21O QAIC review packet final",
            "docs/PRODUCT/R21O_QAIC_REVIEW_PACKET_FINAL_NO_RUNTIME.md",
            "SOURCE_R21O_QAIC_REVIEW_PACKET_BOUND",
            "bound",
            True,
            False,
            20,
        ),
        CockpitTraceMapEntry(
            "r21n_local_preview",
            "R21N local cockpit preview payload",
            "docs/PRODUCT/R21N_LOCAL_COCKPIT_PREVIEW_NO_RUNTIME.md",
            "SOURCE_R21N_LOCAL_PREVIEW_BOUND",
            "bound",
            True,
            False,
            30,
        ),
        CockpitTraceMapEntry(
            "brand_config_trace",
            "Brand and config trace",
            "public/brand/mvp-qaic/mvp-qaic-web-assets-index.json",
            "BRAND_CONFIG_TRACE_COCKPIT_READY",
            "ready",
            True,
            False,
            40,
        ),
        CockpitTraceMapEntry(
            "ui_tracker_trace",
            "UI tracker trace",
            "docs/FINAL/CURRENT_REFERENCE_INDEX.md",
            "UI_TRACKER_TRACE_COCKPIT_READY",
            "ready",
            True,
            False,
            50,
        ),
        CockpitTraceMapEntry(
            "tool_registry_cdc_trace",
            "Tool registry CDC trace",
            "docs/FINAL/CURRENT_REFERENCE_INDEX.md",
            "TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY",
            "ready",
            True,
            False,
            60,
        ),
        CockpitTraceMapEntry(
            "cdc_contract_trace",
            "CDC contract trace",
            "docs/FINAL/CURRENT_REFERENCE_INDEX.md",
            "CDC_CONTRACT_TRACE_COCKPIT_READY",
            "ready",
            True,
            False,
            70,
        ),
        CockpitTraceMapEntry(
            "qaic_bridge_trace",
            "QAIC bridge trace",
            "docs/PRODUCT/R21O_QAIC_REVIEW_PACKET_FINAL_NO_RUNTIME.md",
            "QAIC_BRIDGE_TRACE_COCKPIT_READY",
            "ready",
            True,
            False,
            80,
        ),
        CockpitTraceMapEntry(
            "safety_lock_trace",
            "Review-only safety locks",
            "docs/FINAL/R21F_DRIVE_FIRST_REFERENCE_LOCK_MEMO_20260701.md",
            "REVIEW_ONLY_HANDOFF",
            "locked",
            True,
            False,
            90,
        ),
        CockpitTraceMapEntry(
            "r21q_next_step",
            "R21Q product continuation final seal",
            "R21Q_PRODUCT_CONTINUATION_FINAL_SEAL_NO_RUNTIME",
            "COCKPIT_TRACE_MAP",
            "next",
            True,
            False,
            100,
        ),
    )
    return tuple(sorted(entries, key=lambda entry: entry.ordinal))


def build_operator_handoff_trace_map() -> OperatorHandoffTraceMap:
    """Build the R21P operator handoff trace map."""
    return OperatorHandoffTraceMap(
        handoff_id=HANDOFF_ID,
        status="OPERATOR_HANDOFF_MEMO=READY; COCKPIT_TRACE_MAP=READY",
        source_bindings=dict(SOURCE_BINDINGS),
        trace_flags=dict(TRACE_FLAGS),
        safety_locks=dict(SAFETY_LOCKS),
        traces=_build_trace_entries(),
        next_step="R21Q_PRODUCT_CONTINUATION_FINAL_SEAL_NO_RUNTIME",
    )


def trace_map_to_dict(trace_map: OperatorHandoffTraceMap | None = None) -> dict[str, Any]:
    """Return the trace map as a JSON-friendly dictionary."""
    if trace_map is None:
        trace_map = build_operator_handoff_trace_map()

    return {
        "handoff_id": trace_map.handoff_id,
        "status": trace_map.status,
        "OPERATOR_HANDOFF_MEMO": READY_STATUS,
        "COCKPIT_TRACE_MAP": READY_STATUS,
        "source_bindings": dict(trace_map.source_bindings),
        "trace_flags": dict(trace_map.trace_flags),
        "safety_locks": dict(trace_map.safety_locks),
        "traces": [asdict(entry) for entry in trace_map.traces],
        "next_step": trace_map.next_step,
    }


def build_operator_handoff_with_sources() -> dict[str, Any]:
    """Build the R21P payload with bound source summaries."""
    r21o = build_review_packet_with_sources()
    r21n = build_local_preview_payload()
    trace_map = trace_map_to_dict()

    return {
        **trace_map,
        "source_summaries": {
            "r21o_review_packet": r21o["packet_id"],
            "r21n_local_preview": r21n["preview_id"],
            "r21o_next_step": r21o["next_step"],
            "r21n_status": r21n["status"],
        },
    }


def validate_operator_handoff_trace_map(payload: dict[str, Any] | None = None) -> tuple[str, ...]:
    """Return validation errors. Empty tuple means the R21P payload is valid."""
    if payload is None:
        payload = build_operator_handoff_with_sources()

    errors: list[str] = []
    if payload.get("handoff_id") != HANDOFF_ID:
        errors.append("handoff_id_mismatch")
    if payload.get("OPERATOR_HANDOFF_MEMO") != READY_STATUS:
        errors.append("operator_handoff_memo_not_ready")
    if payload.get("COCKPIT_TRACE_MAP") != READY_STATUS:
        errors.append("cockpit_trace_map_not_ready")

    source_bindings = payload.get("source_bindings")
    if not isinstance(source_bindings, dict):
        errors.append("missing_source_bindings")
    else:
        for key, expected in SOURCE_BINDINGS.items():
            if source_bindings.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    trace_flags = payload.get("trace_flags")
    if not isinstance(trace_flags, dict):
        errors.append("missing_trace_flags")
    else:
        for key, expected in TRACE_FLAGS.items():
            if trace_flags.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    safety_locks = payload.get("safety_locks")
    if not isinstance(safety_locks, dict):
        errors.append("missing_safety_locks")
    else:
        for key, expected in SAFETY_LOCKS.items():
            if safety_locks.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    traces = payload.get("traces")
    if not isinstance(traces, list):
        errors.append("missing_traces")
    else:
        trace_ids = {entry.get("trace_id") for entry in traces if isinstance(entry, dict)}
        if set(REQUIRED_TRACE_IDS) - trace_ids:
            errors.append("missing_trace_entries")
        ordinals = [entry.get("ordinal") for entry in traces if isinstance(entry, dict)]
        if ordinals != sorted(ordinals):
            errors.append("traces_not_deterministic")
        for entry in traces:
            if not isinstance(entry, dict):
                errors.append("invalid_trace_entry")
                continue
            if entry.get("human_review_required") is not True:
                errors.append(f"human_review_missing={entry.get('trace_id')}")
            if entry.get("qaic_execution_allowed") is not False:
                errors.append(f"execution_open={entry.get('trace_id')}")

    summaries = payload.get("source_summaries")
    if isinstance(summaries, dict):
        if summaries.get("r21o_review_packet") != "R21O_QAIC_REVIEW_PACKET_FINAL_NO_RUNTIME":
            errors.append("r21o_source_mismatch")
        if summaries.get("r21n_local_preview") != "R21N_LOCAL_COCKPIT_PREVIEW_NO_RUNTIME":
            errors.append("r21n_source_mismatch")

    if payload.get("next_step") != "R21Q_PRODUCT_CONTINUATION_FINAL_SEAL_NO_RUNTIME":
        errors.append("next_step_mismatch")

    return tuple(errors)


def render_operator_handoff_markdown(payload: dict[str, Any] | None = None) -> str:
    """Render the R21P handoff payload as markdown text only."""
    if payload is None:
        payload = build_operator_handoff_with_sources()

    lines = [
        "# R21P Operator Handoff Memo and Cockpit Trace Map - No Runtime",
        "",
        f"Status: `{payload['status']}`",
        "",
        "## Source Bindings",
    ]
    for key in sorted(payload["source_bindings"]):
        lines.append(f"- `{key}` = `{payload['source_bindings'][key]}`")

    lines.extend(["", "## Cockpit Trace Readiness"])
    for key in sorted(payload["trace_flags"]):
        lines.append(f"- `{key}` = `{payload['trace_flags'][key]}`")

    lines.extend(["", "## Safety Locks"])
    for key in sorted(payload["safety_locks"]):
        lines.append(f"- `{key}` = `{payload['safety_locks'][key]}`")

    lines.extend(["", "## Trace Map"])
    for entry in payload["traces"]:
        lines.append(
            "- "
            f"`{entry['trace_id']}` - {entry['title']} - "
            f"`{entry['cockpit_token']}` - `{entry['status']}`"
        )

    lines.extend(["", f"NEXT={payload['next_step']}"])
    return "\n".join(lines) + "\n"
