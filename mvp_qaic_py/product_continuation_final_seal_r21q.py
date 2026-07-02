"""R21Q product continuation final seal for MVP QAIC.

This module is a pure, import-safe payload builder. It binds the R21O final
review packet and R21P operator handoff trace map into a deterministic
continuation seal without starting runtime surfaces, producing HTML, calling
providers, touching broker/order/sizing paths, or writing Sheet/BQ targets.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from mvp_qaic_py.operator_handoff_trace_map_r21p import build_operator_handoff_with_sources
from mvp_qaic_py.qaic_review_packet_final_r21o import build_review_packet_with_sources

SEAL_ID: Final[str] = "R21Q_PRODUCT_CONTINUATION_FINAL_SEAL_NO_RUNTIME"
READY_STATUS: Final[str] = "READY"
PAUSED_STATUS: Final[str] = "PAUSED"
ALLOWED_STATUS: Final[str] = "ALLOWED"

SOURCE_BINDINGS: Final[dict[str, bool]] = {
    "SOURCE_R21O_QAIC_REVIEW_PACKET_BOUND": True,
    "SOURCE_R21P_OPERATOR_HANDOFF_BOUND": True,
}

PRODUCT_CHAIN_FLAGS: Final[dict[str, bool | str]] = {
    "PRODUCT_CONTINUATION_FINAL_SEAL": READY_STATUS,
    "QAIC_REVIEW_PACKET_FINAL": READY_STATUS,
    "OPERATOR_HANDOFF_MEMO": READY_STATUS,
    "COCKPIT_TRACE_MAP": READY_STATUS,
    "PRODUCT_CHAIN_NO_RUNTIME": True,
    "REFLEX_RUNTIME_STATUS": PAUSED_STATUS,
    "FALLBACK_STATIC_WYSIWYG_ALLOWED": True,
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

REQUIRED_SEAL_IDS: Final[tuple[str, ...]] = (
    "product_continuation_final_seal",
    "r21o_review_packet_final",
    "r21p_operator_handoff",
    "review_only_safety_lock",
    "runtime_pause_boundary",
    "r21r_next_step",
)

NEXT_STEP: Final[str] = "R21R_REFLEX_PUBLICATION_PREVIEW_STRATEGY_AUDIT_DOCS_ONLY"


@dataclass(frozen=True)
class ContinuationSealEntry:
    """Single deterministic R21Q continuation seal entry."""

    seal_entry_id: str
    title: str
    source_reference: str
    continuation_token: str
    status: str
    human_review_required: bool
    qaic_execution_allowed: bool
    ordinal: int


@dataclass(frozen=True)
class ProductContinuationFinalSeal:
    """Top-level R21Q continuation seal object."""

    seal_id: str
    status: str
    source_bindings: dict[str, bool]
    product_chain_flags: dict[str, bool | str]
    safety_locks: dict[str, bool]
    seal_entries: tuple[ContinuationSealEntry, ...]
    next_step: str


def _build_seal_entries() -> tuple[ContinuationSealEntry, ...]:
    """Build stable continuation seal entries."""
    entries = (
        ContinuationSealEntry(
            "product_continuation_final_seal",
            "R21Q product continuation final seal",
            "docs/PRODUCT/R21Q_PRODUCT_CONTINUATION_FINAL_SEAL_NO_RUNTIME.md",
            "PRODUCT_CONTINUATION_FINAL_SEAL",
            "ready",
            True,
            False,
            10,
        ),
        ContinuationSealEntry(
            "r21o_review_packet_final",
            "R21O QAIC review packet final",
            "docs/PRODUCT/R21O_QAIC_REVIEW_PACKET_FINAL_NO_RUNTIME.md",
            "SOURCE_R21O_QAIC_REVIEW_PACKET_BOUND",
            "bound",
            True,
            False,
            20,
        ),
        ContinuationSealEntry(
            "r21p_operator_handoff",
            "R21P operator handoff memo and cockpit trace map",
            "docs/PRODUCT/R21P_OPERATOR_HANDOFF_MEMO_AND_COCKPIT_TRACE_MAP_NO_RUNTIME.md",
            "SOURCE_R21P_OPERATOR_HANDOFF_BOUND",
            "bound",
            True,
            False,
            30,
        ),
        ContinuationSealEntry(
            "review_only_safety_lock",
            "Human review and review-only handoff lock",
            "docs/FINAL/R21F_DRIVE_FIRST_REFERENCE_LOCK_MEMO_20260701.md",
            "REVIEW_ONLY_HANDOFF",
            "locked",
            True,
            False,
            40,
        ),
        ContinuationSealEntry(
            "runtime_pause_boundary",
            "Reflex runtime remains paused and separate",
            "docs/FINAL/CURRENT_REFERENCE_INDEX.md",
            "REFLEX_RUNTIME_STATUS",
            "paused",
            True,
            False,
            50,
        ),
        ContinuationSealEntry(
            "r21r_next_step",
            "R21R publication preview strategy audit",
            NEXT_STEP,
            "NEXT",
            "next",
            True,
            False,
            60,
        ),
    )
    return tuple(sorted(entries, key=lambda entry: entry.ordinal))


def build_product_continuation_final_seal() -> ProductContinuationFinalSeal:
    """Build the R21Q product continuation final seal."""
    return ProductContinuationFinalSeal(
        seal_id=SEAL_ID,
        status="PRODUCT_CONTINUATION_FINAL_SEAL=READY",
        source_bindings=dict(SOURCE_BINDINGS),
        product_chain_flags=dict(PRODUCT_CHAIN_FLAGS),
        safety_locks=dict(SAFETY_LOCKS),
        seal_entries=_build_seal_entries(),
        next_step=NEXT_STEP,
    )


def seal_to_dict(seal: ProductContinuationFinalSeal | None = None) -> dict[str, Any]:
    """Return the continuation seal as a JSON-friendly dictionary."""
    if seal is None:
        seal = build_product_continuation_final_seal()

    return {
        "seal_id": seal.seal_id,
        "status": seal.status,
        "PRODUCT_CONTINUATION_FINAL_SEAL": READY_STATUS,
        "source_bindings": dict(seal.source_bindings),
        "product_chain_flags": dict(seal.product_chain_flags),
        "safety_locks": dict(seal.safety_locks),
        "seal_entries": [asdict(entry) for entry in seal.seal_entries],
        "next_step": seal.next_step,
    }


def build_product_continuation_with_sources() -> dict[str, Any]:
    """Build the R21Q payload with bound source summaries."""
    r21o = build_review_packet_with_sources()
    r21p = build_operator_handoff_with_sources()
    seal = seal_to_dict()

    return {
        **seal,
        "source_summaries": {
            "r21o_review_packet": r21o["packet_id"],
            "r21o_status": r21o["QAIC_REVIEW_PACKET_FINAL"],
            "r21p_operator_handoff": r21p["handoff_id"],
            "r21p_operator_handoff_status": r21p["OPERATOR_HANDOFF_MEMO"],
            "r21p_cockpit_trace_map_status": r21p["COCKPIT_TRACE_MAP"],
            "r21p_next_step": r21p["next_step"],
        },
    }


def validate_product_continuation_final_seal(payload: dict[str, Any] | None = None) -> tuple[str, ...]:
    """Return validation errors. Empty tuple means the R21Q payload is valid."""
    if payload is None:
        payload = build_product_continuation_with_sources()

    errors: list[str] = []
    if payload.get("seal_id") != SEAL_ID:
        errors.append("seal_id_mismatch")
    if payload.get("PRODUCT_CONTINUATION_FINAL_SEAL") != READY_STATUS:
        errors.append("product_continuation_final_seal_not_ready")

    source_bindings = payload.get("source_bindings")
    if not isinstance(source_bindings, dict):
        errors.append("missing_source_bindings")
    else:
        for key, expected in SOURCE_BINDINGS.items():
            if source_bindings.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    product_chain_flags = payload.get("product_chain_flags")
    if not isinstance(product_chain_flags, dict):
        errors.append("missing_product_chain_flags")
    else:
        for key, expected in PRODUCT_CHAIN_FLAGS.items():
            if product_chain_flags.get(key) != expected:
                errors.append(f"{key}_mismatch")

    safety_locks = payload.get("safety_locks")
    if not isinstance(safety_locks, dict):
        errors.append("missing_safety_locks")
    else:
        for key, expected in SAFETY_LOCKS.items():
            if safety_locks.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    seal_entries = payload.get("seal_entries")
    if not isinstance(seal_entries, list):
        errors.append("missing_seal_entries")
    else:
        entry_ids = {entry.get("seal_entry_id") for entry in seal_entries if isinstance(entry, dict)}
        if set(REQUIRED_SEAL_IDS) - entry_ids:
            errors.append("missing_seal_entries")
        ordinals = [entry.get("ordinal") for entry in seal_entries if isinstance(entry, dict)]
        if ordinals != sorted(ordinals):
            errors.append("seal_entries_not_deterministic")
        for entry in seal_entries:
            if not isinstance(entry, dict):
                errors.append("invalid_seal_entry")
                continue
            if entry.get("human_review_required") is not True:
                errors.append(f"human_review_missing={entry.get('seal_entry_id')}")
            if entry.get("qaic_execution_allowed") is not False:
                errors.append(f"execution_open={entry.get('seal_entry_id')}")

    summaries = payload.get("source_summaries")
    if isinstance(summaries, dict):
        if summaries.get("r21o_review_packet") != "R21O_QAIC_REVIEW_PACKET_FINAL_NO_RUNTIME":
            errors.append("r21o_source_mismatch")
        if summaries.get("r21p_operator_handoff") != "R21P_OPERATOR_HANDOFF_MEMO_AND_COCKPIT_TRACE_MAP_NO_RUNTIME":
            errors.append("r21p_source_mismatch")

    if payload.get("next_step") != NEXT_STEP:
        errors.append("next_step_mismatch")

    return tuple(errors)


def render_product_continuation_markdown(payload: dict[str, Any] | None = None) -> str:
    """Render the R21Q continuation seal as markdown text only."""
    if payload is None:
        payload = build_product_continuation_with_sources()

    lines = [
        "# R21Q Product Continuation Final Seal - No Runtime",
        "",
        f"Status: `{payload['status']}`",
        "",
        "## Source Bindings",
    ]
    for key in sorted(payload["source_bindings"]):
        lines.append(f"- `{key}` = `{payload['source_bindings'][key]}`")

    lines.extend(["", "## Product Chain"])
    for key in sorted(payload["product_chain_flags"]):
        lines.append(f"- `{key}` = `{payload['product_chain_flags'][key]}`")

    lines.extend(["", "## Safety Locks"])
    for key in sorted(payload["safety_locks"]):
        lines.append(f"- `{key}` = `{payload['safety_locks'][key]}`")

    lines.extend(["", "## Continuation Seal"])
    for entry in payload["seal_entries"]:
        lines.append(
            "- "
            f"`{entry['seal_entry_id']}` - {entry['title']} - "
            f"`{entry['continuation_token']}` - `{entry['status']}`"
        )

    lines.extend(["", f"NEXT={payload['next_step']}"])
    return "\n".join(lines) + "\n"
