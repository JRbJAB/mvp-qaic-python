"""R21M cockpit queue visual planning model for MVP QAIC.

This module binds the R21K data contract and R21L model binding into a
deterministic, text-only planning layer for future cockpit previews. It is
stdlib-only, import-safe, and side-effect free.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from mvp_qaic_py.cockpit_queue_data_contract_r21k import contract_to_dict
from mvp_qaic_py.cockpit_queue_model_binding_r21l import build_cockpit_queue_model

WORKFLOW_ID: Final[str] = "R21M_COCKPIT_QUEUE_VISUAL_PLANNING_NO_RUNTIME"
SOURCE_R21K_BOUND: Final[str] = "BOUND"
SOURCE_R21L_BOUND: Final[str] = "BOUND"
READY_STATUS: Final[str] = "READY"

REQUIRED_LANE_IDS: Final[tuple[str, ...]] = (
    "operator_queue_status",
    "qaic_bridge_trace",
    "brand_config_trace",
    "ui_tracker_trace",
    "tool_registry_cdc_trace",
    "cdc_contract_trace",
    "cockpit_data_contract_trace",
    "next_milestones",
)

PLANNING_FLAGS: Final[dict[str, bool | str]] = {
    "source_r21k_contract": SOURCE_R21K_BOUND,
    "source_r21l_model_binding": SOURCE_R21L_BOUND,
    "SOURCE_R21J_R6_VALIDATED": True,
    "COCKPIT_QUEUE_VISUAL_PLANNING": READY_STATUS,
    "COCKPIT_QUEUE_DATA_CONTRACT": SOURCE_R21K_BOUND,
    "COCKPIT_QUEUE_MODEL_BINDING": SOURCE_R21L_BOUND,
    "BRAND_CONFIG_TRACE_COCKPIT_READY": True,
    "UI_TRACKER_TRACE_COCKPIT_READY": True,
    "TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY": True,
    "CDC_CONTRACT_TRACE_COCKPIT_READY": True,
    "QAIC_BRIDGE_TRACE_COCKPIT_READY": True,
    "QAIT_CHARTE_TEMPLATE": SOURCE_R21K_BOUND,
    "MVP_QAIC_LOGO_VALIDATED": SOURCE_R21K_BOUND,
    "preserve_q_candlesticks_signal_line": True,
    "qaic_execution_allowed": False,
}

EXECUTION_LOCKS: Final[dict[str, bool]] = {
    "no_codex_runtime": True,
    "no_runtime": True,
    "no_docker": True,
    "no_reflex_run": True,
    "no_provider_call": True,
    "no_broker_order_sizing": True,
    "no_sheet_bq_write": True,
    "no_html_output": True,
    "no_export_directory_output": True,
    "human_review_required": True,
    "qaic_execution_allowed": False,
}


@dataclass(frozen=True)
class VisualCard:
    """Single deterministic planning card for a future cockpit lane."""

    card_id: str
    title: str
    status: str
    source_trace: str
    body: str
    visual_intent: str
    cockpit_ready: bool
    ordinal: int


@dataclass(frozen=True)
class VisualLane:
    """Planning lane composed of cards derived from R21K/R21L traces."""

    lane_id: str
    title: str
    source_binding: str
    cards: tuple[VisualCard, ...]
    cockpit_ready: bool
    ordinal: int


@dataclass(frozen=True)
class NextMilestone:
    """Future product step for the cockpit queue sequence."""

    milestone_id: str
    title: str
    status: str
    summary: str
    runtime_scope: str
    ordinal: int


@dataclass(frozen=True)
class CockpitQueueVisualPlanning:
    """Top-level R21M visual planning model."""

    workflow_id: str
    status: str
    source_r21k_contract: str
    source_r21l_model_binding: str
    traces: dict[str, bool | str]
    execution_locks: dict[str, bool]
    lanes: tuple[VisualLane, ...]
    next_milestones: tuple[NextMilestone, ...]


def _make_card(
    card_id: str,
    title: str,
    status: str,
    source_trace: str,
    body: str,
    visual_intent: str,
    ordinal: int,
) -> VisualCard:
    return VisualCard(
        card_id=card_id,
        title=title,
        status=status,
        source_trace=source_trace,
        body=body,
        visual_intent=visual_intent,
        cockpit_ready=True,
        ordinal=ordinal,
    )


def _build_lanes() -> tuple[VisualLane, ...]:
    """Build stable visual planning lanes."""
    return (
        VisualLane(
            lane_id="operator_queue_status",
            title="Operator queue status",
            source_binding="R21L.operator_queue",
            cards=(
                _make_card(
                    "operator_queue_status_card",
                    "Review queue",
                    "ready_for_human_review",
                    "SOURCE_R21J_R6_VALIDATED",
                    "R21J_R6 review queue is validated and surfaced through R21K/R21L.",
                    "Show queue readiness, human review requirement, and blocked execution.",
                    10,
                ),
            ),
            cockpit_ready=True,
            ordinal=10,
        ),
        VisualLane(
            lane_id="qaic_bridge_trace",
            title="QAIC bridge trace",
            source_binding="R21L.qaic_bridge",
            cards=(
                _make_card(
                    "qaic_bridge_trace_card",
                    "Review-only bridge",
                    "bound",
                    "QAIC_BRIDGE_TRACE_COCKPIT_READY",
                    "QAIC bridge is display/import trace only; execution remains closed.",
                    "Show the MVP-to-QAIC bridge as review-only evidence.",
                    20,
                ),
            ),
            cockpit_ready=True,
            ordinal=20,
        ),
        VisualLane(
            lane_id="brand_config_trace",
            title="Brand config trace",
            source_binding="R21L.brand_config",
            cards=(
                _make_card(
                    "brand_config_trace_card",
                    "Validated brand assets",
                    "bound",
                    "BRAND_CONFIG_TRACE_COCKPIT_READY",
                    "QAIT charte template and MVP QAIC official logo assets are bound.",
                    "Preserve the Q candlesticks signal line and validated logo identity.",
                    30,
                ),
            ),
            cockpit_ready=True,
            ordinal=30,
        ),
        VisualLane(
            lane_id="ui_tracker_trace",
            title="UI tracker trace",
            source_binding="R21L.ui_tracker",
            cards=(
                _make_card(
                    "ui_tracker_trace_card",
                    "Tracker route references",
                    "bound",
                    "UI_TRACKER_TRACE_COCKPIT_READY",
                    "Tracker registry routes are available as planning references only.",
                    "Show tracker readiness without starting a UI engine.",
                    40,
                ),
            ),
            cockpit_ready=True,
            ordinal=40,
        ),
        VisualLane(
            lane_id="tool_registry_cdc_trace",
            title="Tool registry CDC trace",
            source_binding="R21L.tool_registry_cdc",
            cards=(
                _make_card(
                    "tool_registry_cdc_trace_card",
                    "Registry source coverage",
                    "bound",
                    "TOOL_REGISTRY_CDC_TRACE_COCKPIT_READY",
                    "Tool registry sources are linked to CDC coverage for cockpit traceability.",
                    "Show source coverage and private project tool status.",
                    50,
                ),
            ),
            cockpit_ready=True,
            ordinal=50,
        ),
        VisualLane(
            lane_id="cdc_contract_trace",
            title="CDC contract trace",
            source_binding="R21L.cdc_contract",
            cards=(
                _make_card(
                    "cdc_contract_trace_card",
                    "Final CDC source",
                    "bound",
                    "CDC_CONTRACT_TRACE_COCKPIT_READY",
                    "The single final CDC contract v0.2.6 is the source trace.",
                    "Show CDC final-reference coverage and Drive-first audit lock.",
                    60,
                ),
            ),
            cockpit_ready=True,
            ordinal=60,
        ),
        VisualLane(
            lane_id="cockpit_data_contract_trace",
            title="Cockpit data contract trace",
            source_binding="R21K.contract + R21L.model",
            cards=(
                _make_card(
                    "cockpit_data_contract_trace_card",
                    "Contract and model binding",
                    "bound",
                    "COCKPIT_QUEUE_DATA_CONTRACT",
                    "R21K data contract and R21L model binding are both bound.",
                    "Show source contract readiness beside the cockpit model binding.",
                    70,
                ),
            ),
            cockpit_ready=True,
            ordinal=70,
        ),
        VisualLane(
            lane_id="next_milestones",
            title="Next milestones",
            source_binding="R21M.end_plan",
            cards=(
                _make_card(
                    "next_milestones_card",
                    "Visual end-plan",
                    "ready",
                    "COCKPIT_QUEUE_VISUAL_PLANNING",
                    "R21M through R21Q are planned, with runtime paused and separate.",
                    "Show the short product continuation sequence as a visual lane.",
                    80,
                ),
            ),
            cockpit_ready=True,
            ordinal=80,
        ),
    )


def _build_next_milestones() -> tuple[NextMilestone, ...]:
    """Build the R21M end-plan sequence."""
    return (
        NextMilestone(
            "R21M",
            "visual planning model",
            "ready",
            "Deterministic cockpit queue visual planning model.",
            "no runtime",
            10,
        ),
        NextMilestone(
            "R21N",
            "local cockpit preview only",
            "next",
            "Local cockpit preview planned from this data model only.",
            "no runtime",
            20,
        ),
        NextMilestone(
            "R21O",
            "QAIC review packet final",
            "planned",
            "Final QAIC review packet from bound cockpit traces.",
            "no execution",
            30,
        ),
        NextMilestone(
            "R21P",
            "operator handoff memo + cockpit trace map",
            "planned",
            "Operator handoff memo with trace map for review.",
            "human review only",
            40,
        ),
        NextMilestone(
            "R21Q",
            "product continuation final seal no-runtime",
            "planned",
            "Final no-runtime continuation seal.",
            "no runtime",
            50,
        ),
        NextMilestone(
            "REFLEX_RUNTIME",
            "Reflex runtime remains paused and separate",
            "paused",
            "Runtime work is not part of this R21M product/data layer.",
            "separate",
            60,
        ),
    )


def build_cockpit_queue_visual_planning() -> CockpitQueueVisualPlanning:
    """Build the R21M cockpit queue visual planning model."""
    r21k = contract_to_dict()
    r21l = build_cockpit_queue_model()
    traces = dict(PLANNING_FLAGS)
    traces["source_r21k_contract_id"] = r21k["contract_id"]
    traces["source_r21l_model_id"] = r21l["model_id"]

    return CockpitQueueVisualPlanning(
        workflow_id=WORKFLOW_ID,
        status="COCKPIT_QUEUE_VISUAL_PLANNING_READY_NO_RUNTIME",
        source_r21k_contract=SOURCE_R21K_BOUND,
        source_r21l_model_binding=SOURCE_R21L_BOUND,
        traces=traces,
        execution_locks=dict(EXECUTION_LOCKS),
        lanes=_build_lanes(),
        next_milestones=_build_next_milestones(),
    )


def model_to_dict(model: CockpitQueueVisualPlanning | None = None) -> dict[str, Any]:
    """Return the visual planning model as a JSON-friendly dictionary."""
    if model is None:
        model = build_cockpit_queue_visual_planning()

    return {
        "workflow_id": model.workflow_id,
        "status": model.status,
        "source_r21k_contract": model.source_r21k_contract,
        "source_r21l_model_binding": model.source_r21l_model_binding,
        "traces": dict(model.traces),
        "execution_locks": dict(model.execution_locks),
        "lanes": [
            {
                **asdict(lane),
                "cards": [asdict(card) for card in lane.cards],
            }
            for lane in model.lanes
        ],
        "next_milestones": [asdict(milestone) for milestone in model.next_milestones],
    }


def validate_cockpit_queue_visual_planning(
    model: CockpitQueueVisualPlanning | None = None,
) -> tuple[str, ...]:
    """Return validation errors. Empty tuple means the R21M model is valid."""
    if model is None:
        model = build_cockpit_queue_visual_planning()

    errors: list[str] = []
    payload = model_to_dict(model)
    traces = payload["traces"]
    locks = payload["execution_locks"]
    lane_ids = {lane["lane_id"] for lane in payload["lanes"]}

    if payload["workflow_id"] != WORKFLOW_ID:
        errors.append("workflow_id_mismatch")
    if payload["source_r21k_contract"] != SOURCE_R21K_BOUND:
        errors.append("source_r21k_not_bound")
    if payload["source_r21l_model_binding"] != SOURCE_R21L_BOUND:
        errors.append("source_r21l_not_bound")
    if not set(REQUIRED_LANE_IDS).issubset(lane_ids):
        errors.append("missing_visual_lanes")

    for key, expected in PLANNING_FLAGS.items():
        if traces.get(key) != expected:
            errors.append(f"{key}_mismatch")

    for key, expected in EXECUTION_LOCKS.items():
        if locks.get(key) is not expected:
            errors.append(f"{key}_mismatch")

    ordinals = [lane["ordinal"] for lane in payload["lanes"]]
    if ordinals != sorted(ordinals):
        errors.append("lanes_not_deterministic")

    return tuple(errors)


def render_visual_planning_markdown(
    model: CockpitQueueVisualPlanning | None = None,
) -> str:
    """Render the R21M model as markdown text only."""
    payload = model_to_dict(model)
    lines = [
        "# R21M Cockpit Queue Visual Planning - No Runtime",
        "",
        f"Workflow: `{payload['workflow_id']}`",
        f"Status: `{payload['status']}`",
        "",
        "## Cockpit Visual Plan",
    ]

    for lane in payload["lanes"]:
        lines.append(f"- `{lane['lane_id']}` - {lane['title']} - `{lane['source_binding']}`")
        for card in lane["cards"]:
            lines.append(f"  - `{card['card_id']}` - {card['title']} - `{card['status']}`")

    lines.extend(["", "## Trace Locks"])
    for key in sorted(payload["traces"]):
        lines.append(f"- `{key}` = `{payload['traces'][key]}`")

    lines.extend(["", "## Execution Locks"])
    for key in sorted(payload["execution_locks"]):
        lines.append(f"- `{key}` = `{payload['execution_locks'][key]}`")

    lines.extend(["", "## End-Plan"])
    for milestone in payload["next_milestones"]:
        lines.append(
            "- "
            f"`{milestone['milestone_id']}` - {milestone['title']} - "
            f"`{milestone['status']}` - {milestone['runtime_scope']}"
        )

    return "\n".join(lines) + "\n"
