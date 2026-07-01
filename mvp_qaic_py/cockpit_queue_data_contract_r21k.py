"""R21K cockpit queue data contract for MVP QAIC.

This module is pure stdlib and side-effect free. It defines the cockpit-ready
queue contract that consumes the validated R21J_R6 review queue state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

CONTRACT_ID: Final[str] = "R21K_COCKPIT_QUEUE_DATA_CONTRACT_NO_RUNTIME"
SOURCE_CHAIN: Final[str] = "R21J_R6_VALIDATED_BY_READONLY_HEAD_AUDIT"
SOURCE_TAG: Final[str] = "mvp-qaic-r21j-r6-docs-only-supersede-seal-no-runtime-20260701"

POLICY_FLAGS: Final[dict[str, bool | str]] = {
    "no_code_runner": True,
    "no_ui_process_start": True,
    "no_container_process": True,
    "no_provider_call": True,
    "no_broker_order_sizing": True,
    "no_sheet_bq_write": True,
    "no_markup_file_output": True,
    "no_export_directory_output": True,
    "human_review_required": True,
    "qaic_execution_allowed": False,
    "handoff_mode": "qaic_review_only",
}


@dataclass(frozen=True)
class CockpitField:
    """Single cockpit data field definition."""

    key: str
    label: str
    value_type: str
    required: bool
    source_reference: str
    trace_group: str
    display_hint: str


@dataclass(frozen=True)
class QueueItem:
    """Single review queue row for future cockpit consumption."""

    item_id: str
    title: str
    status: str
    owner: str
    source_reference: str
    cockpit_trace_group: str
    blocking: bool
    human_review_required: bool


@dataclass(frozen=True)
class CockpitQueueContract:
    """Data contract exposed to future cockpit surfaces."""

    contract_id: str
    source_chain: str
    source_tag: str
    status: str
    policy_flags: dict[str, bool | str]
    cockpit_ready_flags: dict[str, bool]
    fields: tuple[CockpitField, ...]
    queue_items: tuple[QueueItem, ...]


def build_cockpit_fields() -> tuple[CockpitField, ...]:
    """Build the stable field contract used by cockpit queues."""
    return (
        CockpitField(
            key="qaic_bridge_trace",
            label="QAIC bridge trace",
            value_type="object",
            required=True,
            source_reference="docs/BRIDGE/MVP_QAIC_TO_QAIC_BRIDGE_STATUS_R1.md",
            trace_group="QAIC_BRIDGE_TRACE_COCKPIT_READY",
            display_hint="Show review-only bridge status and execution-disabled state.",
        ),
        CockpitField(
            key="brand_config_trace",
            label="Brand and visual config trace",
            value_type="object",
            required=True,
            source_reference="public/brand/mvp-qaic/",
            trace_group="BRAND_CONFIG_TRACE_COCKPIT_READY",
            display_hint="Show validated logo, QAIT charte template, and visual preservation locks.",
        ),
        CockpitField(
            key="ui_tracker_trace",
            label="UI tracker reference trace",
            value_type="object",
            required=True,
            source_reference="docs/dev_tracking/TRACKER_RENDER_REFERENCE_REGISTRY.md",
            trace_group="UI_TRACKER_TRACE_COCKPIT_READY",
            display_hint="Show tracker registry binding and cockpit route readiness.",
        ),
        CockpitField(
            key="tool_registry_cdc_trace",
            label="Tool registry CDC trace",
            value_type="object",
            required=True,
            source_reference="data/tool_registry/tools_project_mvp_qaic.json",
            trace_group="TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY",
            display_hint="Show tool registry coverage from the CDC-bound source.",
        ),
        CockpitField(
            key="cdc_contract_trace",
            label="CDC final contract trace",
            value_type="object",
            required=True,
            source_reference="docs/FINAL/MVP_QAIC_CDC_CONTRACT_FINAL_FUSED_v0.2.6.md",
            trace_group="CDC_CONTRACT_TRACE_COCKPIT_READY",
            display_hint="Show CDC source coverage and contract status.",
        ),
        CockpitField(
            key="operator_review_queue",
            label="Operator QAIC review queue",
            value_type="array",
            required=True,
            source_reference="docs/PRODUCT/R21J_OPERATOR_QAIC_REVIEW_QUEUE_NO_RUNTIME.md",
            trace_group="OPERATOR_QAIC_REVIEW_QUEUE_COCKPIT_READY",
            display_hint="Show each review item, owner, blocker state, and human review status.",
        ),
    )


def build_queue_items() -> tuple[QueueItem, ...]:
    """Build the minimum cockpit queue items for QAIC review-only handoff."""
    return (
        QueueItem(
            item_id="R21K-QAIC-BRIDGE",
            title="MVP to QAIC review-only bridge",
            status="ready_for_review",
            owner="MVP_QAIC",
            source_reference="R21I_OPERATOR_REFERENCE_BINDING_HANDOFF_NO_RUNTIME",
            cockpit_trace_group="QAIC_BRIDGE_TRACE_COCKPIT_READY",
            blocking=False,
            human_review_required=True,
        ),
        QueueItem(
            item_id="R21K-BRAND-CONFIG",
            title="Validated brand and cockpit visual config",
            status="ready_for_cockpit_trace",
            owner="Operator",
            source_reference="QAIT_CHARTE_TEMPLATE + MVP_QAIC_LOGO_VALIDATED",
            cockpit_trace_group="BRAND_CONFIG_TRACE_COCKPIT_READY",
            blocking=False,
            human_review_required=True,
        ),
        QueueItem(
            item_id="R21K-UI-TRACKER",
            title="UI tracker and registry references",
            status="bound",
            owner="MVP_QAIC",
            source_reference="R21H_UI_TRACKER_TOOL_REGISTRY_CDC_BINDING",
            cockpit_trace_group="UI_TRACKER_TRACE_COCKPIT_READY",
            blocking=False,
            human_review_required=True,
        ),
        QueueItem(
            item_id="R21K-CDC-CONTRACT",
            title="CDC final contract coverage",
            status="bound",
            owner="MVP_QAIC",
            source_reference="CDC_CONTRACT_TRACE_COCKPIT_READY",
            cockpit_trace_group="CDC_CONTRACT_TRACE_COCKPIT_READY",
            blocking=False,
            human_review_required=True,
        ),
    )


def build_cockpit_queue_contract() -> CockpitQueueContract:
    """Build the cockpit queue data contract."""
    return CockpitQueueContract(
        contract_id=CONTRACT_ID,
        source_chain=SOURCE_CHAIN,
        source_tag=SOURCE_TAG,
        status="COCKPIT_QUEUE_DATA_CONTRACT_READY_NO_RUNTIME",
        policy_flags=dict(POLICY_FLAGS),
        cockpit_ready_flags={
            "BRAND_CONFIG_TRACE_COCKPIT_READY": True,
            "UI_TRACKER_TRACE_COCKPIT_READY": True,
            "TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY": True,
            "CDC_CONTRACT_TRACE_COCKPIT_READY": True,
            "QAIC_BRIDGE_TRACE_COCKPIT_READY": True,
            "OPERATOR_QAIC_REVIEW_QUEUE_COCKPIT_READY": True,
            "QAIT_CHARTE_TEMPLATE_BOUND": True,
            "MVP_QAIC_LOGO_VALIDATED_BOUND": True,
            "preserve_q_candlesticks_signal_line": True,
        },
        fields=build_cockpit_fields(),
        queue_items=build_queue_items(),
    )


def contract_to_dict(contract: CockpitQueueContract | None = None) -> dict[str, Any]:
    """Return the contract as a JSON-friendly dictionary."""
    if contract is None:
        contract = build_cockpit_queue_contract()
    return {
        "contract_id": contract.contract_id,
        "source_chain": contract.source_chain,
        "source_tag": contract.source_tag,
        "status": contract.status,
        "policy_flags": dict(contract.policy_flags),
        "cockpit_ready_flags": dict(contract.cockpit_ready_flags),
        "fields": [asdict(field) for field in contract.fields],
        "queue_items": [asdict(item) for item in contract.queue_items],
    }


def validate_cockpit_queue_contract(contract: CockpitQueueContract | None = None) -> dict[str, bool | str]:
    """Validate the R21K contract without side effects."""
    if contract is None:
        contract = build_cockpit_queue_contract()

    field_groups = {field.trace_group for field in contract.fields}
    queue_groups = {item.cockpit_trace_group for item in contract.queue_items}
    flags = contract.cockpit_ready_flags

    required_groups = {
        "BRAND_CONFIG_TRACE_COCKPIT_READY",
        "UI_TRACKER_TRACE_COCKPIT_READY",
        "TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY",
        "CDC_CONTRACT_TRACE_COCKPIT_READY",
        "QAIC_BRIDGE_TRACE_COCKPIT_READY",
    }

    policy = contract.policy_flags
    return {
        "contract_id": contract.contract_id,
        "status_ready": contract.status == "COCKPIT_QUEUE_DATA_CONTRACT_READY_NO_RUNTIME",
        "required_groups_present": required_groups.issubset(field_groups | queue_groups | set(flags)),
        "brand_config_ready": bool(flags.get("BRAND_CONFIG_TRACE_COCKPIT_READY")),
        "ui_tracker_ready": bool(flags.get("UI_TRACKER_TRACE_COCKPIT_READY")),
        "tool_registry_cdc_ready": bool(flags.get("TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY")),
        "cdc_contract_ready": bool(flags.get("CDC_CONTRACT_TRACE_COCKPIT_READY")),
        "qaic_bridge_ready": bool(flags.get("QAIC_BRIDGE_TRACE_COCKPIT_READY")),
        "qait_charte_template_bound": bool(flags.get("QAIT_CHARTE_TEMPLATE_BOUND")),
        "mvp_qaic_logo_validated_bound": bool(flags.get("MVP_QAIC_LOGO_VALIDATED_BOUND")),
        "qaic_execution_allowed": policy.get("qaic_execution_allowed") is True,
        "safe_for_review_only": policy.get("qaic_execution_allowed") is False,
        "no_provider_call": policy.get("no_provider_call") is True,
        "no_broker_order_sizing": policy.get("no_broker_order_sizing") is True,
        "no_sheet_bq_write": policy.get("no_sheet_bq_write") is True,
    }
