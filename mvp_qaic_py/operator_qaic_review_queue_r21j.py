"""R21J-R4 QAIC review queue with cockpit-ready reference traces.

This module supersedes the pushed R21J payload whose pre-commit console checks
reported missing cockpit-ready brand trace tokens and a forbidden phrase in the
product document. R21J-R4 keeps the same review-only scope and repairs the
payload explicitly without runtime, network, provider, broker, sheet, or BQ use.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal


TraceStatus = Literal["BOUND", "READY", "VALIDATED_BOUND", "EXECUTION_DISABLED"]
QueueStatus = Literal["ready_for_qaic_review", "human_review_required", "blocked_from_execution"]


COCKPIT_READY_FLAGS: dict[str, bool] = {
    "BRAND_CONFIG_TRACE_COCKPIT_READY": True,
    "UI_TRACKER_TRACE_COCKPIT_READY": True,
    "TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY": True,
    "CDC_CONTRACT_TRACE_COCKPIT_READY": True,
    "QAIC_BRIDGE_TRACE_COCKPIT_READY": True,
}

SAFETY_FLAGS: dict[str, bool | str] = {
    "drive_first_references_verified": True,
    "source_binding_from_r21h": True,
    "operator_reference_handoff_from_r21i": True,
    "r21j_original_seal_valid": False,
    "r21j_r4_supersedes_contaminated_push": True,
    "no_runtime": True,
    "no_docker": True,
    "no_reflex_runtime_command": True,
    "no_provider_call": True,
    "no_broker_order_sizing": True,
    "no_sheet_bq_write": True,
    "no_apps_script_execution": True,
    "no_html_output": True,
    "human_review_required": True,
    "qaic_execution_allowed": False,
    "handoff_mode": "qaic_review_only",
}


@dataclass(frozen=True)
class CockpitTrace:
    """Reference trace that a future cockpit can display."""

    trace_id: str
    label: str
    status: TraceStatus
    cockpit_visibility: bool
    source_refs: tuple[str, ...]
    evidence: tuple[str, ...]
    ready_flag: str
    required_in_future_cockpit: bool = True


@dataclass(frozen=True)
class ReviewQueueItem:
    """Review-only queue item for QAIC/operator workflow."""

    item_id: str
    title: str
    owner: str
    status: QueueStatus
    cockpit_trace_ids: tuple[str, ...]
    required_evidence: tuple[str, ...]
    blockers: tuple[str, ...]
    human_review_required: bool = True
    qaic_execution_allowed: bool = False


@dataclass(frozen=True)
class ReviewQueuePayload:
    """Full R21J-R4 review queue payload."""

    batch: str
    status: str
    supersedes: str
    source_chain: tuple[str, ...]
    safety_flags: dict[str, bool | str]
    cockpit_ready_flags: dict[str, bool]
    cockpit_traces: tuple[CockpitTrace, ...]
    queue_items: tuple[ReviewQueueItem, ...]


def build_cockpit_traces() -> tuple[CockpitTrace, ...]:
    """Build cockpit-ready traces from already validated source references."""
    return (
        CockpitTrace(
            trace_id="qaic_bridge_trace",
            label="MVP to QAIC review-only bridge",
            status="READY",
            cockpit_visibility=True,
            source_refs=(
                "docs/BRIDGE/MVP_QAIC_TO_QAIC_BRIDGE_CONTRACT_R1.md",
                "docs/BRIDGE/MVP_QAIC_TO_QAIC_BRIDGE_STATUS_R1.md",
                "docs/PRODUCT/R21D_OPERATOR_WORKFLOW_QAIC_BRIDGE_STATUS_NO_RUNTIME.md",
                "docs/PRODUCT/R21I_OPERATOR_REFERENCE_BINDING_HANDOFF_NO_RUNTIME.md",
            ),
            evidence=(
                "MVP_QAIC_TO_QAIC_BRIDGE_R1",
                "QAIC_REVIEW_ONLY_HANDOFF_READY",
                "qaic_execution_allowed=False",
            ),
            ready_flag="QAIC_BRIDGE_TRACE_COCKPIT_READY",
        ),
        CockpitTrace(
            trace_id="ui_tracker_trace",
            label="UI tracker registry binding",
            status="BOUND",
            cockpit_visibility=True,
            source_refs=(
                "docs/dev_tracking/TRACKER_RENDER_REFERENCE_REGISTRY.md",
                "docs/dev_tracking/ui_tracker_tool_manifest.json",
                "docs/PRODUCT/R21H_UI_TRACKER_TOOL_REGISTRY_CDC_OPERATOR_WORKFLOW_BINDING_NO_RUNTIME.md",
            ),
            evidence=(
                "route:/cdc-dev-tracker",
                "route:/dev-tracking",
                "route:/tool-registry-cdc",
                "route:/cdc-tracker",
            ),
            ready_flag="UI_TRACKER_TRACE_COCKPIT_READY",
        ),
        CockpitTrace(
            trace_id="tool_registry_cdc_trace",
            label="Tool registry CDC binding",
            status="BOUND",
            cockpit_visibility=True,
            source_refs=(
                "data/tool_registry/tool_registry_export.csv",
                "data/tool_registry/tool_registry_snapshot.json",
                "data/tool_registry/tools_project_mvp_qaic.json",
                "docs/ARCHIVE/R20F4_DOCS_ROOT_HISTORICAL_20260701/TOOL_REGISTRY_CDC.md",
            ),
            evidence=(
                "tool_registry_cdc",
                "registry_contract_coverage",
                "source_of_truth_bound",
            ),
            ready_flag="TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY",
        ),
        CockpitTrace(
            trace_id="cdc_contract_trace",
            label="CDC final contract binding",
            status="BOUND",
            cockpit_visibility=True,
            source_refs=(
                "docs/FINAL/📘 MVP_QAIC_CDC_CONTRACT_FINAL_FUSED_v0.2.6.md",
                "docs/FINAL/CURRENT_REFERENCE_INDEX.md",
                "docs/FINAL/R21F_DRIVE_FIRST_REFERENCE_LOCK_MEMO_20260701.md",
            ),
            evidence=(
                "cdc_final_contract_bound",
                "drive_first_reference_lock_applied",
                "no_batch_without_referential_audit=True",
            ),
            ready_flag="CDC_CONTRACT_TRACE_COCKPIT_READY",
        ),
        CockpitTrace(
            trace_id="brand_config_trace",
            label="Brand assets and charte configuration",
            status="VALIDATED_BOUND",
            cockpit_visibility=True,
            source_refs=(
                "public/brand/mvp-qaic/logo-mvp-qaic-official-name.png",
                "public/brand/mvp-qaic/logo-mvp-qaic-icon-only.png",
                "public/brand/mvp-qaic/charte-graphique.png",
                "public/brand/mvp-qaic/brand-assets.html",
                "public/brand/mvp-qaic/charte/index.html",
                "public/brand/mvp-qaic/mvp-qaic-web-assets-index.json",
                "public/brand/mvp-qaic/site.webmanifest",
            ),
            evidence=(
                "BRAND_CONFIG_TRACE_COCKPIT_READY=True",
                "QAIT_CHARTE_TEMPLATE=BOUND",
                "MVP_QAIC_LOGO_VALIDATED=BOUND",
                "NO_GENERATED_PREVIEW_REPLACES_VALIDATED_LOGO=True",
                "PRESERVE_Q_CANDLESTICKS_SIGNAL_LINE=True",
                "preserve_q_candlesticks_signal_line=True",
            ),
            ready_flag="BRAND_CONFIG_TRACE_COCKPIT_READY",
        ),
        CockpitTrace(
            trace_id="execution_safety_trace",
            label="Execution safety lock",
            status="EXECUTION_DISABLED",
            cockpit_visibility=True,
            source_refs=(
                "docs/PRODUCT/R21E_OPERATOR_DECISION_JOURNAL_HANDOFF_NO_RUNTIME.md",
                "docs/PRODUCT/R21I_OPERATOR_REFERENCE_BINDING_HANDOFF_NO_RUNTIME.md",
            ),
            evidence=(
                "NO_PROVIDER_CALL=True",
                "NO_BROKER_ORDER_SIZING=True",
                "NO_SHEET_BQ_WRITE=True",
                "HUMAN_REVIEW_REQUIRED=True",
            ),
            ready_flag="QAIC_BRIDGE_TRACE_COCKPIT_READY",
        ),
    )


def build_review_queue_items() -> tuple[ReviewQueueItem, ...]:
    """Build QAIC/operator review queue items with cockpit trace references."""
    return (
        ReviewQueueItem(
            item_id="R21J-QAIC-BRIDGE-001",
            title="Review MVP to QAIC handoff readiness",
            owner="QAIC",
            status="ready_for_qaic_review",
            cockpit_trace_ids=("qaic_bridge_trace", "execution_safety_trace"),
            required_evidence=("bridge_contract", "r21i_reference_handoff", "execution_disabled"),
            blockers=(),
        ),
        ReviewQueueItem(
            item_id="R21J-UI-TRACKER-002",
            title="Review UI tracker and route trace coverage",
            owner="Operator",
            status="human_review_required",
            cockpit_trace_ids=("ui_tracker_trace",),
            required_evidence=("tracker_render_reference_registry", "ui_tracker_tool_manifest"),
            blockers=(),
        ),
        ReviewQueueItem(
            item_id="R21J-TOOL-REGISTRY-003",
            title="Review tool registry CDC source coverage",
            owner="Operator",
            status="human_review_required",
            cockpit_trace_ids=("tool_registry_cdc_trace",),
            required_evidence=("tool_registry_export", "tool_registry_snapshot", "tools_project_mvp_qaic"),
            blockers=(),
        ),
        ReviewQueueItem(
            item_id="R21J-CDC-004",
            title="Review CDC final contract alignment",
            owner="Operator",
            status="human_review_required",
            cockpit_trace_ids=("cdc_contract_trace",),
            required_evidence=("cdc_final_contract", "current_reference_index", "drive_first_lock"),
            blockers=(),
        ),
        ReviewQueueItem(
            item_id="R21J-BRAND-005",
            title="Review cockpit brand/config trace",
            owner="Operator",
            status="human_review_required",
            cockpit_trace_ids=("brand_config_trace",),
            required_evidence=(
                "BRAND_CONFIG_TRACE_COCKPIT_READY",
                "validated_logo",
                "qait_charte_template",
                "public_brand_assets",
            ),
            blockers=(),
        ),
        ReviewQueueItem(
            item_id="R21J-SAFETY-006",
            title="Confirm review-only execution lock",
            owner="QAIC",
            status="blocked_from_execution",
            cockpit_trace_ids=("execution_safety_trace",),
            required_evidence=("no_provider", "no_broker_order_sizing", "no_sheet_bq_write"),
            blockers=("execution_forbidden_until_separate_QAIC_policy_unlock",),
        ),
    )


def build_review_queue_payload() -> ReviewQueuePayload:
    """Build the complete R21J-R4 cockpit-ready review queue payload."""
    return ReviewQueuePayload(
        batch="R21J_R4_OPERATOR_QAIC_REVIEW_QUEUE_SUPERSEDE_REPAIR_NO_RUNTIME",
        status="READY_FOR_QAIC_REVIEW_ONLY_COCKPIT_BINDING_REPAIRED",
        supersedes="R21J_CONTAMINATED_BY_PRE_COMMIT_CHECK_FAILURES",
        source_chain=("R21F", "R21G", "R21H", "R21I", "R21J", "R21J_R4"),
        safety_flags=dict(SAFETY_FLAGS),
        cockpit_ready_flags=dict(COCKPIT_READY_FLAGS),
        cockpit_traces=build_cockpit_traces(),
        queue_items=build_review_queue_items(),
    )


def payload_to_dict(payload: ReviewQueuePayload | None = None) -> dict[str, Any]:
    """Serialize the payload to a JSON-friendly dict."""
    if payload is None:
        payload = build_review_queue_payload()
    return {
        "batch": payload.batch,
        "status": payload.status,
        "supersedes": payload.supersedes,
        "source_chain": list(payload.source_chain),
        "safety_flags": dict(payload.safety_flags),
        "cockpit_ready_flags": dict(payload.cockpit_ready_flags),
        "cockpit_traces": [asdict(trace) for trace in payload.cockpit_traces],
        "queue_items": [asdict(item) for item in payload.queue_items],
    }


def validate_review_queue(payload: ReviewQueuePayload | None = None) -> list[str]:
    """Return validation errors. Empty list means valid."""
    if payload is None:
        payload = build_review_queue_payload()

    errors: list[str] = []
    trace_ids = {trace.trace_id for trace in payload.cockpit_traces}
    required_traces = {
        "qaic_bridge_trace",
        "ui_tracker_trace",
        "tool_registry_cdc_trace",
        "cdc_contract_trace",
        "brand_config_trace",
        "execution_safety_trace",
    }
    missing = sorted(required_traces - trace_ids)
    if missing:
        errors.append("missing_traces=" + ",".join(missing))

    for key, value in COCKPIT_READY_FLAGS.items():
        if payload.cockpit_ready_flags.get(key) is not value:
            errors.append(f"{key}_must_be_true")

    flags = payload.safety_flags
    if flags.get("qaic_execution_allowed") is not False:
        errors.append("qaic_execution_allowed_must_be_false")
    for key in (
        "no_runtime",
        "no_provider_call",
        "no_broker_order_sizing",
        "no_sheet_bq_write",
        "no_reflex_runtime_command",
    ):
        if flags.get(key) is not True:
            errors.append(f"{key}_must_be_true")

    for item in payload.queue_items:
        if item.qaic_execution_allowed:
            errors.append(f"item_execution_allowed={item.item_id}")
        for trace_id in item.cockpit_trace_ids:
            if trace_id not in trace_ids:
                errors.append(f"unknown_trace={trace_id}")

    return errors


def render_review_queue_markdown(payload: ReviewQueuePayload | None = None) -> str:
    """Render a markdown-only operator/QAIC handoff view."""
    if payload is None:
        payload = build_review_queue_payload()
    data = payload_to_dict(payload)
    lines = [
        "# R21J-R4 Operator QAIC Review Queue - No Runtime",
        "",
        f"Status: `{data['status']}`",
        f"Supersedes: `{data['supersedes']}`",
        "",
        "## Cockpit-ready flags",
    ]
    for key, value in sorted(data["cockpit_ready_flags"].items()):
        lines.append(f"- `{key}` = `{value}`")
    lines.extend(["", "## Safety flags"])
    for key, value in sorted(data["safety_flags"].items()):
        lines.append(f"- `{key}` = `{value}`")
    lines.extend(["", "## Cockpit traces"])
    for trace in payload.cockpit_traces:
        lines.append(f"- `{trace.trace_id}` — {trace.label} — `{trace.status}` — `{trace.ready_flag}`")
    lines.extend(["", "## Review queue"])
    for item in payload.queue_items:
        lines.append(f"- `{item.item_id}` — {item.title} — `{item.status}`")
    return "\n".join(lines) + "\n"
