"""R21I operator reference binding handoff for MVP QAIC.

This module is a deterministic, offline-only handoff surface. It consumes the
reference binding sealed in R21H as a contract boundary and exposes a compact
QAIC review-only handoff model.

It intentionally performs no runtime start, network call, provider call, broker
action, sizing, sheet write, BigQuery write, or Apps Script execution.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


WORKFLOW_ID = "R21I_OPERATOR_REFERENCE_BINDING_HANDOFF_NO_RUNTIME"
SOURCE_BINDING = "R21H_UI_TRACKER_TOOL_REGISTRY_CDC_OPERATOR_WORKFLOW_BINDING"
HANDOFF_MODE = "qaic_review_only_local_handoff"


SAFETY_FLAGS: dict[str, bool] = {
    "no_runtime": True,
    "no_docker": True,
    "no_reflex_run": True,
    "no_provider_call": True,
    "no_broker_order_sizing": True,
    "no_sheet_bq_write": True,
    "no_apps_script_execution": True,
    "human_review_required": True,
    "qaic_execution_allowed": False,
}


@dataclass(frozen=True)
class ReferenceHandoffItem:
    """One source-of-truth reference exposed to the operator handoff."""

    key: str
    family: str
    source_path: str
    operator_value: str
    qaic_review_usage: str


@dataclass(frozen=True)
class OperatorReferenceHandoff:
    """Review-only operator handoff model for QAIC consumption."""

    workflow_id: str
    status: str
    source_binding: str
    handoff_mode: str
    bridge_contract: str
    safety_flags: dict[str, bool]
    references: tuple[ReferenceHandoffItem, ...]
    operator_next_step: str
    qaic_next_step: str


def build_reference_items() -> tuple[ReferenceHandoffItem, ...]:
    """Return the R21I handoff references derived from R21G/R21H evidence."""
    return (
        ReferenceHandoffItem(
            key="ui_tracker_render_registry",
            family="ui_tracker",
            source_path="docs/dev_tracking/TRACKER_RENDER_REFERENCE_REGISTRY.md",
            operator_value="cdc_dev_tracker | dev_tracker | tool_registry_cdc | cdc_tracker",
            qaic_review_usage="Check which cockpit/tracker surface is bound to the reviewed operator workflow.",
        ),
        ReferenceHandoffItem(
            key="ui_tracker_tool_manifest",
            family="ui_tracker",
            source_path="docs/dev_tracking/ui_tracker_tool_manifest.json",
            operator_value="tracker manifest for UI tool references",
            qaic_review_usage="Verify tracker tool metadata before any later runtime or preview decision.",
        ),
        ReferenceHandoffItem(
            key="tool_registry_project",
            family="tool_registry",
            source_path="data/tool_registry/tools_project_mvp_qaic.json",
            operator_value="project tool registry source",
            qaic_review_usage="Verify tool roles and guardrails used by MVP QAIC handoff surfaces.",
        ),
        ReferenceHandoffItem(
            key="tool_registry_snapshot",
            family="tool_registry",
            source_path="data/tool_registry/tool_registry_snapshot.json",
            operator_value="tool registry snapshot",
            qaic_review_usage="Compare static handoff claims against the recorded registry snapshot.",
        ),
        ReferenceHandoffItem(
            key="cdc_final_contract",
            family="cdc",
            source_path="docs/FINAL/MVP_QAIC_CDC_CONTRACT_FINAL_FUSED_v0.2.6.md",
            operator_value="final CDC contract suffix; resolved locally because filename may carry an emoji prefix",
            qaic_review_usage="Use the final CDC contract as the requirement boundary for QAIC review.",
        ),
        ReferenceHandoffItem(
            key="mvp_to_qaic_bridge_contract",
            family="bridge",
            source_path="docs/BRIDGE/MVP_QAIC_TO_QAIC_BRIDGE_CONTRACT_R1.md",
            operator_value="MVP_QAIC_TO_QAIC_BRIDGE_R1",
            qaic_review_usage="Confirm the handoff remains review-only and does not enable execution.",
        ),
        ReferenceHandoffItem(
            key="r21h_binding_model",
            family="operator_workflow",
            source_path="mvp_qaic_py/operator_workflow_reference_binding_r21h.py",
            operator_value="sealed R21H binding model",
            qaic_review_usage="Use R21H as the direct predecessor and source binding for this handoff.",
        ),
    )


def build_operator_reference_handoff() -> OperatorReferenceHandoff:
    """Build the deterministic R21I review-only handoff model."""
    return OperatorReferenceHandoff(
        workflow_id=WORKFLOW_ID,
        status="READY_FOR_QAIC_REFERENCE_REVIEW_ONLY_HANDOFF",
        source_binding=SOURCE_BINDING,
        handoff_mode=HANDOFF_MODE,
        bridge_contract="MVP_QAIC_TO_QAIC_BRIDGE_R1",
        safety_flags=dict(SAFETY_FLAGS),
        references=build_reference_items(),
        operator_next_step="Review the bound references and approve or block the QAIC review-only packet.",
        qaic_next_step="Review the packet without provider call, broker action, sizing, sheet write, or runtime start.",
    )


def handoff_to_dict(handoff: OperatorReferenceHandoff | None = None) -> dict[str, Any]:
    """Serialize the R21I handoff model to a JSON-friendly dictionary."""
    if handoff is None:
        handoff = build_operator_reference_handoff()

    return {
        "workflow_id": handoff.workflow_id,
        "status": handoff.status,
        "source_binding": handoff.source_binding,
        "handoff_mode": handoff.handoff_mode,
        "bridge_contract": handoff.bridge_contract,
        "safety_flags": dict(handoff.safety_flags),
        "references": [asdict(item) for item in handoff.references],
        "operator_next_step": handoff.operator_next_step,
        "qaic_next_step": handoff.qaic_next_step,
    }


def validate_handoff(handoff: OperatorReferenceHandoff | None = None) -> list[str]:
    """Validate the handoff safety and reference coverage."""
    if handoff is None:
        handoff = build_operator_reference_handoff()

    issues: list[str] = []
    flags = handoff.safety_flags

    expected_true = (
        "no_runtime",
        "no_docker",
        "no_reflex_run",
        "no_provider_call",
        "no_broker_order_sizing",
        "no_sheet_bq_write",
        "no_apps_script_execution",
        "human_review_required",
    )
    for key in expected_true:
        if flags.get(key) is not True:
            issues.append(f"{key}_must_be_true")

    if flags.get("qaic_execution_allowed") is not False:
        issues.append("qaic_execution_allowed_must_be_false")

    families = {item.family for item in handoff.references}
    for family in ("ui_tracker", "tool_registry", "cdc", "bridge", "operator_workflow"):
        if family not in families:
            issues.append(f"missing_family_{family}")

    if handoff.source_binding != SOURCE_BINDING:
        issues.append("source_binding_mismatch")

    if handoff.handoff_mode != HANDOFF_MODE:
        issues.append("handoff_mode_mismatch")

    return issues


def render_handoff_markdown(handoff: OperatorReferenceHandoff | None = None) -> str:
    """Render a compact markdown handoff for copy/review workflows."""
    if handoff is None:
        handoff = build_operator_reference_handoff()

    lines = [
        f"# {handoff.workflow_id}",
        "",
        f"Status: {handoff.status}",
        f"Source binding: {handoff.source_binding}",
        f"Handoff mode: {handoff.handoff_mode}",
        f"Bridge contract: {handoff.bridge_contract}",
        "",
        "## Safety flags",
    ]
    for key, value in sorted(handoff.safety_flags.items()):
        lines.append(f"- {key}={value}")

    lines.extend(["", "## Bound references"])
    for item in handoff.references:
        lines.append(f"- {item.key} [{item.family}]")
        lines.append(f"  - source: `{item.source_path}`")
        lines.append(f"  - operator value: {item.operator_value}")
        lines.append(f"  - QAIC review usage: {item.qaic_review_usage}")

    lines.extend(
        [
            "",
            "## Next steps",
            f"- Operator: {handoff.operator_next_step}",
            f"- QAIC: {handoff.qaic_next_step}",
        ]
    )
    return "\n".join(lines) + "\n"


__all__ = [
    "HANDOFF_MODE",
    "SAFETY_FLAGS",
    "SOURCE_BINDING",
    "WORKFLOW_ID",
    "OperatorReferenceHandoff",
    "ReferenceHandoffItem",
    "build_operator_reference_handoff",
    "build_reference_items",
    "handoff_to_dict",
    "render_handoff_markdown",
    "validate_handoff",
]
