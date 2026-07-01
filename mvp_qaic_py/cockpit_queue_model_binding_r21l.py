"""R21L cockpit queue model binding for MVP QAIC.

This module binds the R21K cockpit queue data contract into cockpit-consumable
sections, cards, and rows. It is pure stdlib, import-safe, and side-effect free.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from mvp_qaic_py.cockpit_queue_data_contract_r21k import (
    build_cockpit_queue_contract,
    contract_to_dict,
    validate_cockpit_queue_contract,
)

MODEL_ID: Final[str] = "R21L_COCKPIT_QUEUE_MODEL_BINDING_NO_RUNTIME"
SOURCE_CONTRACT_ID: Final[str] = "R21K_COCKPIT_QUEUE_DATA_CONTRACT_NO_RUNTIME"
SOURCE_CONTRACT_STATUS: Final[str] = "COCKPIT_QUEUE_DATA_CONTRACT_READY_NO_RUNTIME"
SOURCE_R21J_STATE: Final[str] = "R21J_R6_VALIDATED_BY_READONLY_HEAD_AUDIT"
SOURCE_R21J_TAG: Final[str] = "mvp-qaic-r21j-r6-docs-only-supersede-seal-no-runtime-20260701"

REQUIRED_SECTION_IDS: Final[tuple[str, ...]] = (
    "qaic_bridge",
    "operator_queue",
    "ui_tracker",
    "tool_registry_cdc",
    "cdc_contract",
    "brand_config",
    "safety_locks",
)

REQUIRED_TRACES: Final[dict[str, bool]] = {
    "SOURCE_R21K_CONTRACT_VALIDATED": True,
    "SOURCE_R21J_R6_VALIDATED": True,
    "BRAND_CONFIG_TRACE_COCKPIT_READY": True,
    "UI_TRACKER_TRACE_COCKPIT_READY": True,
    "TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY": True,
    "CDC_CONTRACT_TRACE_COCKPIT_READY": True,
    "QAIC_BRIDGE_TRACE_COCKPIT_READY": True,
    "COCKPIT_QUEUE_MODEL_BINDING": True,
    "qaic_execution_allowed": False,
    "human_review_required": True,
}


@dataclass(frozen=True)
class CockpitSection:
    """Deterministic cockpit section derived from an R21K trace group."""

    section_id: str
    title: str
    source_trace: str
    source_reference: str
    card_ids: tuple[str, ...]
    row_filter: str
    cockpit_ready: bool
    ordinal: int


@dataclass(frozen=True)
class CockpitCard:
    """Cockpit card definition for grouping review rows."""

    card_id: str
    section_id: str
    title: str
    status: str
    source_trace: str
    cockpit_ready: bool
    human_review_required: bool
    ordinal: int


@dataclass(frozen=True)
class CockpitRow:
    """Single stable row ready for cockpit display."""

    row_id: str
    section_id: str
    card_id: str
    label: str
    status: str
    source_contract_field: str
    source_queue_item: str
    source_trace: str
    source_reference: str
    cockpit_ready: bool
    human_review_required: bool
    qaic_execution_allowed: bool
    ordinal: int


def _source_contract_payload() -> dict[str, Any]:
    """Return the R21K source payload as a dictionary."""
    return contract_to_dict(build_cockpit_queue_contract())


def _section_definitions() -> tuple[CockpitSection, ...]:
    """Build stable cockpit section definitions."""
    return (
        CockpitSection(
            section_id="qaic_bridge",
            title="QAIC bridge",
            source_trace="QAIC_BRIDGE_TRACE_COCKPIT_READY",
            source_reference="docs/PRODUCT/R21I_OPERATOR_REFERENCE_BINDING_HANDOFF_NO_RUNTIME.md",
            card_ids=("qaic_bridge_status",),
            row_filter="qaic_bridge_trace",
            cockpit_ready=True,
            ordinal=10,
        ),
        CockpitSection(
            section_id="operator_queue",
            title="Operator queue",
            source_trace="OPERATOR_QAIC_REVIEW_QUEUE_COCKPIT_READY",
            source_reference="docs/PRODUCT/R21J_OPERATOR_QAIC_REVIEW_QUEUE_NO_RUNTIME.md",
            card_ids=("operator_review_items",),
            row_filter="operator_review_queue",
            cockpit_ready=True,
            ordinal=20,
        ),
        CockpitSection(
            section_id="ui_tracker",
            title="UI tracker",
            source_trace="UI_TRACKER_TRACE_COCKPIT_READY",
            source_reference="docs/dev_tracking/TRACKER_RENDER_REFERENCE_REGISTRY.md",
            card_ids=("ui_tracker_routes",),
            row_filter="ui_tracker_trace",
            cockpit_ready=True,
            ordinal=30,
        ),
        CockpitSection(
            section_id="tool_registry_cdc",
            title="Tool registry CDC",
            source_trace="TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY",
            source_reference="data/tool_registry/tools_project_mvp_qaic.json",
            card_ids=("tool_registry_sources",),
            row_filter="tool_registry_cdc_trace",
            cockpit_ready=True,
            ordinal=40,
        ),
        CockpitSection(
            section_id="cdc_contract",
            title="CDC contract",
            source_trace="CDC_CONTRACT_TRACE_COCKPIT_READY",
            source_reference="docs/FINAL/MVP_QAIC_CDC_CONTRACT_FINAL_FUSED_v0.2.6.md",
            card_ids=("cdc_contract_source",),
            row_filter="cdc_contract_trace",
            cockpit_ready=True,
            ordinal=50,
        ),
        CockpitSection(
            section_id="brand_config",
            title="Brand config",
            source_trace="BRAND_CONFIG_TRACE_COCKPIT_READY",
            source_reference="public/brand/mvp-qaic/mvp-qaic-web-assets-index.json",
            card_ids=("brand_config_assets",),
            row_filter="brand_config_trace",
            cockpit_ready=True,
            ordinal=60,
        ),
        CockpitSection(
            section_id="safety_locks",
            title="Safety locks",
            source_trace="QAIC_BRIDGE_TRACE_COCKPIT_READY",
            source_reference="docs/PRODUCT/R21K_COCKPIT_QUEUE_DATA_CONTRACT_NO_RUNTIME.md",
            card_ids=("review_only_locks",),
            row_filter="policy_flags",
            cockpit_ready=True,
            ordinal=70,
        ),
    )


def _card_definitions() -> tuple[CockpitCard, ...]:
    """Build stable cockpit card definitions."""
    return (
        CockpitCard("qaic_bridge_status", "qaic_bridge", "Bridge status", "ready", "QAIC_BRIDGE_TRACE_COCKPIT_READY", True, True, 10),
        CockpitCard("operator_review_items", "operator_queue", "Review items", "ready", "OPERATOR_QAIC_REVIEW_QUEUE_COCKPIT_READY", True, True, 20),
        CockpitCard("ui_tracker_routes", "ui_tracker", "Tracker routes", "bound", "UI_TRACKER_TRACE_COCKPIT_READY", True, True, 30),
        CockpitCard("tool_registry_sources", "tool_registry_cdc", "Registry sources", "bound", "TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY", True, True, 40),
        CockpitCard("cdc_contract_source", "cdc_contract", "Final CDC source", "bound", "CDC_CONTRACT_TRACE_COCKPIT_READY", True, True, 50),
        CockpitCard("brand_config_assets", "brand_config", "Validated assets", "bound", "BRAND_CONFIG_TRACE_COCKPIT_READY", True, True, 60),
        CockpitCard("review_only_locks", "safety_locks", "Review-only locks", "locked", "QAIC_BRIDGE_TRACE_COCKPIT_READY", True, True, 70),
    )


def _field_by_key(source_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {field["key"]: field for field in source_payload["fields"]}


def _queue_item_by_group(source_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    items: dict[str, dict[str, Any]] = {}
    for item in source_payload["queue_items"]:
        items.setdefault(item["cockpit_trace_group"], item)
    return items


def _row_definitions(source_payload: dict[str, Any] | None = None) -> tuple[CockpitRow, ...]:
    """Build stable cockpit rows by binding R21K fields and queue items."""
    if source_payload is None:
        source_payload = _source_contract_payload()

    fields = _field_by_key(source_payload)
    queue_items = _queue_item_by_group(source_payload)
    policy = source_payload["policy_flags"]

    rows = (
        CockpitRow(
            row_id="R21L-QAIC-BRIDGE-001",
            section_id="qaic_bridge",
            card_id="qaic_bridge_status",
            label="MVP to QAIC bridge is review-only",
            status="ready_for_review",
            source_contract_field="qaic_bridge_trace",
            source_queue_item=queue_items["QAIC_BRIDGE_TRACE_COCKPIT_READY"]["item_id"],
            source_trace="QAIC_BRIDGE_TRACE_COCKPIT_READY",
            source_reference=fields["qaic_bridge_trace"]["source_reference"],
            cockpit_ready=True,
            human_review_required=True,
            qaic_execution_allowed=False,
            ordinal=10,
        ),
        CockpitRow(
            row_id="R21L-OPERATOR-QUEUE-002",
            section_id="operator_queue",
            card_id="operator_review_items",
            label="Operator QAIC review queue is bound from R21K",
            status="ready_for_review",
            source_contract_field="operator_review_queue",
            source_queue_item="R21K_QUEUE_ITEMS",
            source_trace="OPERATOR_QAIC_REVIEW_QUEUE_COCKPIT_READY",
            source_reference=fields["operator_review_queue"]["source_reference"],
            cockpit_ready=True,
            human_review_required=True,
            qaic_execution_allowed=False,
            ordinal=20,
        ),
        CockpitRow(
            row_id="R21L-UI-TRACKER-003",
            section_id="ui_tracker",
            card_id="ui_tracker_routes",
            label="UI tracker routes are cockpit-ready references",
            status="bound",
            source_contract_field="ui_tracker_trace",
            source_queue_item=queue_items["UI_TRACKER_TRACE_COCKPIT_READY"]["item_id"],
            source_trace="UI_TRACKER_TRACE_COCKPIT_READY",
            source_reference=fields["ui_tracker_trace"]["source_reference"],
            cockpit_ready=True,
            human_review_required=True,
            qaic_execution_allowed=False,
            ordinal=30,
        ),
        CockpitRow(
            row_id="R21L-TOOL-REGISTRY-004",
            section_id="tool_registry_cdc",
            card_id="tool_registry_sources",
            label="Tool registry CDC sources are bound",
            status="bound",
            source_contract_field="tool_registry_cdc_trace",
            source_queue_item="R21K-TOOL-REGISTRY",
            source_trace="TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY",
            source_reference=fields["tool_registry_cdc_trace"]["source_reference"],
            cockpit_ready=True,
            human_review_required=True,
            qaic_execution_allowed=False,
            ordinal=40,
        ),
        CockpitRow(
            row_id="R21L-CDC-CONTRACT-005",
            section_id="cdc_contract",
            card_id="cdc_contract_source",
            label="Final CDC contract is bound",
            status="bound",
            source_contract_field="cdc_contract_trace",
            source_queue_item=queue_items["CDC_CONTRACT_TRACE_COCKPIT_READY"]["item_id"],
            source_trace="CDC_CONTRACT_TRACE_COCKPIT_READY",
            source_reference=fields["cdc_contract_trace"]["source_reference"],
            cockpit_ready=True,
            human_review_required=True,
            qaic_execution_allowed=False,
            ordinal=50,
        ),
        CockpitRow(
            row_id="R21L-BRAND-CONFIG-006",
            section_id="brand_config",
            card_id="brand_config_assets",
            label="Validated brand assets and charte are bound",
            status="bound",
            source_contract_field="brand_config_trace",
            source_queue_item=queue_items["BRAND_CONFIG_TRACE_COCKPIT_READY"]["item_id"],
            source_trace="BRAND_CONFIG_TRACE_COCKPIT_READY",
            source_reference=fields["brand_config_trace"]["source_reference"],
            cockpit_ready=True,
            human_review_required=True,
            qaic_execution_allowed=False,
            ordinal=60,
        ),
        CockpitRow(
            row_id="R21L-SAFETY-LOCKS-007",
            section_id="safety_locks",
            card_id="review_only_locks",
            label="Execution and write locks remain closed",
            status="locked",
            source_contract_field="policy_flags",
            source_queue_item="R21K_POLICY_FLAGS",
            source_trace="QAIC_BRIDGE_TRACE_COCKPIT_READY",
            source_reference="docs/PRODUCT/R21K_COCKPIT_QUEUE_DATA_CONTRACT_NO_RUNTIME.md",
            cockpit_ready=True,
            human_review_required=policy["human_review_required"] is True,
            qaic_execution_allowed=policy["qaic_execution_allowed"] is True,
            ordinal=70,
        ),
    )
    return tuple(sorted(rows, key=lambda row: row.ordinal))


def list_cockpit_sections() -> tuple[dict[str, object], ...]:
    """Return deterministic cockpit sections."""
    return tuple(asdict(section) for section in _section_definitions())


def list_cockpit_rows() -> tuple[dict[str, object], ...]:
    """Return deterministic cockpit rows."""
    return tuple(asdict(row) for row in _row_definitions())


def build_cockpit_queue_model() -> dict[str, object]:
    """Build the R21L cockpit queue model from the R21K contract."""
    source_payload = _source_contract_payload()
    source_validation = validate_cockpit_queue_contract()
    sections = _section_definitions()
    cards = _card_definitions()
    rows = _row_definitions(source_payload)

    return {
        "model_id": MODEL_ID,
        "status": "COCKPIT_QUEUE_MODEL_BOUND_NO_RUNTIME",
        "source_contract": {
            "contract_id": source_payload["contract_id"],
            "status": source_payload["status"],
            "source_chain": source_payload["source_chain"],
            "source_tag": source_payload["source_tag"],
            "validated": source_validation["status_ready"] is True
            and source_validation["required_groups_present"] is True,
        },
        "source_r21j": {
            "state": SOURCE_R21J_STATE,
            "tag": SOURCE_R21J_TAG,
            "validated": True,
        },
        "traces": dict(REQUIRED_TRACES),
        "source_policy_flags": dict(source_payload["policy_flags"]),
        "sections": [asdict(section) for section in sections],
        "cards": [asdict(card) for card in cards],
        "rows": [asdict(row) for row in rows],
    }


def validate_cockpit_queue_model(model: dict[str, object] | None = None) -> tuple[str, ...]:
    """Return validation errors. Empty tuple means valid."""
    if model is None:
        model = build_cockpit_queue_model()

    errors: list[str] = []
    source_contract = model.get("source_contract")
    if not isinstance(source_contract, dict):
        errors.append("missing_source_contract")
    else:
        if source_contract.get("contract_id") != SOURCE_CONTRACT_ID:
            errors.append("source_contract_id_mismatch")
        if source_contract.get("status") != SOURCE_CONTRACT_STATUS:
            errors.append("source_contract_status_mismatch")
        if source_contract.get("validated") is not True:
            errors.append("source_contract_not_validated")

    traces = model.get("traces")
    if not isinstance(traces, dict):
        errors.append("missing_traces")
    else:
        for key, expected in REQUIRED_TRACES.items():
            if traces.get(key) is not expected:
                errors.append(f"{key}_mismatch")

    sections = model.get("sections")
    if not isinstance(sections, list):
        errors.append("missing_sections")
        section_ids: set[str] = set()
    else:
        section_ids = {str(section.get("section_id")) for section in sections if isinstance(section, dict)}
        missing_sections = sorted(set(REQUIRED_SECTION_IDS) - section_ids)
        if missing_sections:
            errors.append("missing_sections=" + ",".join(missing_sections))

    rows = model.get("rows")
    if not isinstance(rows, list):
        errors.append("missing_rows")
    else:
        ordinals = [row.get("ordinal") for row in rows if isinstance(row, dict)]
        if ordinals != sorted(ordinals):
            errors.append("rows_not_deterministic")
        for row in rows:
            if not isinstance(row, dict):
                errors.append("invalid_row")
                continue
            if row.get("section_id") not in section_ids:
                errors.append(f"row_unknown_section={row.get('row_id')}")
            if row.get("cockpit_ready") is not True:
                errors.append(f"row_not_cockpit_ready={row.get('row_id')}")
            if row.get("qaic_execution_allowed") is not False:
                errors.append(f"row_allows_execution={row.get('row_id')}")
            if row.get("human_review_required") is not True:
                errors.append(f"row_missing_human_review={row.get('row_id')}")

    return tuple(errors)


def render_cockpit_queue_model_markdown(model: dict[str, object] | None = None) -> str:
    """Render a markdown-only cockpit model handoff."""
    if model is None:
        model = build_cockpit_queue_model()

    lines = [
        "# R21L Cockpit Queue Model Binding - No Runtime",
        "",
        f"Status: `{model['status']}`",
        "",
        "## Traces",
    ]
    traces = model["traces"]
    if isinstance(traces, dict):
        for key in sorted(traces):
            lines.append(f"- `{key}` = `{traces[key]}`")

    lines.extend(["", "## Sections"])
    sections = model["sections"]
    if isinstance(sections, list):
        for section in sections:
            lines.append(f"- `{section['section_id']}` - {section['title']} - `{section['source_trace']}`")

    lines.extend(["", "## Rows"])
    rows = model["rows"]
    if isinstance(rows, list):
        for row in rows:
            lines.append(f"- `{row['row_id']}` - {row['label']} - `{row['status']}`")

    return "\n".join(lines) + "\n"
